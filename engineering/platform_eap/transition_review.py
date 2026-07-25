from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_REVIEW_SECTIONS = (
    "Milestone Accomplishment Review",
    "Deferred Work & Waiting on External Events",
    "Engineering Learning Review",
    "Engineering Decision Register Updates",
    "Portfolio Health Review",
)
PORTFOLIO_SUMMARY_PATTERN = re.compile(r"^Milestone\s+\d+\s+Portfolio Summary$")
PLACEHOLDER_WORDS = {
    "add",
    "comment",
    "complete",
    "details",
    "evidence",
    "fill",
    "here",
    "insert",
    "item",
    "later",
    "n/a",
    "na",
    "none",
    "note",
    "owner",
    "pending",
    "placeholder",
    "provide",
    "required",
    "status",
    "tbd",
    "todo",
    "unknown",
    "value",
}


@dataclass(frozen=True)
class TransitionReviewFinding:
    severity: str
    message: str
    path: str | None = None


@dataclass(frozen=True)
class TransitionReviewValidation:
    status: str
    milestone: str | None
    declared_status: str | None
    findings: tuple[TransitionReviewFinding, ...]


def _metadata_value(text: str, field_name: str) -> str | None:
    match = re.search(rf"^\*\*{re.escape(field_name)}:\*\*\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def _safe_review_path(root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts or "\\" in relative:
        raise ValueError("Transition Review path must be a safe repository-relative path.")
    if len(candidate.parts) != 4 or candidate.parts[:2] != ("docs", "milestones"):
        raise ValueError("Transition Review path must be directly under docs/milestones/Milestone_<n>/.")
    if not re.fullmatch(r"Milestone_\d+", candidate.parts[2]):
        raise ValueError("Transition Review directory must use the Milestone_<n> convention.")
    if not re.fullmatch(r"Milestone_\d+_Transition_Review\.md", candidate.name):
        raise ValueError("Transition Review filename must use the Milestone_<n>_Transition_Review.md convention.")
    resolved_root = root.resolve()
    resolved = (resolved_root / candidate).resolve()
    if resolved_root not in resolved.parents:
        raise ValueError("Transition Review path escapes the repository.")
    return resolved


def _table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def _evidence_fragments(body: str) -> list[str]:
    without_comments = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    without_html = re.sub(r"<[^>]+>", "", without_comments)
    lines = without_html.splitlines()
    fragments: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("|") and line.endswith("|"):
            table_lines: list[str] = []
            while index < len(lines):
                candidate = lines[index].strip()
                if not candidate.startswith("|") or not candidate.endswith("|"):
                    break
                table_lines.append(candidate)
                index += 1
            rows = [_table_cells(candidate) for candidate in table_lines]
            if len(rows) >= 2 and _table_separator(rows[1]):
                rows = rows[2:]
            elif len(rows) >= 2:
                rows = rows[1:]
            for cells in rows:
                if _table_separator(cells):
                    continue
                fragments.extend(cells[1:] if len(cells) > 1 else cells)
            continue
        normalized = re.sub(r"^(?:#{1,6}\s+|>\s*|[-+*]\s+|\d+[.)]\s+)", "", line)
        normalized = re.sub(r"^\[[ xX]\]\s*", "", normalized)
        normalized = re.sub(r"!?\[([^\]]*)\]\([^)]+\)", r"\1", normalized)
        fragments.append(normalized)
        index += 1
    return fragments


def _has_substantive_evidence(body: str) -> bool:
    for fragment in _evidence_fragments(body):
        tokens = re.findall(r"[a-z0-9]+(?:[/._-][a-z0-9]+)*", fragment.lower())
        if any(token not in PLACEHOLDER_WORDS for token in tokens):
            return True
    return False


def validate_transition_review(root: Path, relative: str) -> TransitionReviewValidation:
    findings: list[TransitionReviewFinding] = []
    try:
        path = _safe_review_path(root, relative)
    except ValueError as exc:
        return TransitionReviewValidation(
            status="FAIL",
            milestone=None,
            declared_status=None,
            findings=(TransitionReviewFinding("ERROR", str(exc), relative),),
        )
    if not path.is_file():
        return TransitionReviewValidation(
            status="FAIL",
            milestone=None,
            declared_status=None,
            findings=(TransitionReviewFinding("ERROR", "Transition Review artifact does not exist.", relative),),
        )

    text = path.read_text(encoding="utf-8")
    milestone = _metadata_value(text, "Milestone")
    declared_status = _metadata_value(text, "Status")
    path_milestone_number = int(path.parent.name.removeprefix("Milestone_"))
    filename_milestone_number = int(path.stem.removeprefix("Milestone_").removesuffix("_Transition_Review"))
    if not milestone:
        findings.append(TransitionReviewFinding("ERROR", "Transition Review milestone metadata is missing.", relative))
        milestone_number = None
    else:
        milestone_match = re.fullmatch(r"Milestone\s+(\d+)", milestone)
        milestone_number = int(milestone_match.group(1)) if milestone_match else None
        if milestone_number is None:
            findings.append(TransitionReviewFinding("ERROR", "Transition Review milestone metadata is invalid.", relative))
        elif milestone_number != path_milestone_number or milestone_number != filename_milestone_number:
            findings.append(
                TransitionReviewFinding(
                    "ERROR",
                    "Transition Review milestone metadata, directory, and filename do not identify the same milestone.",
                    relative,
                )
            )
    if not declared_status:
        findings.append(TransitionReviewFinding("ERROR", "Transition Review status metadata is missing.", relative))
    else:
        findings.append(
            TransitionReviewFinding(
                "INFO",
                f"Declared review status is {declared_status}; structural validation does not approve that status.",
                relative,
            )
        )

    headings = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE))
    section_names = [match.group(1) for match in headings]
    portfolio_sections = [name for name in section_names if PORTFOLIO_SUMMARY_PATTERN.fullmatch(name)]
    expected = (*REQUIRED_REVIEW_SECTIONS, portfolio_sections[0] if len(portfolio_sections) == 1 else "<next-milestone portfolio summary>")
    governed_sections = [name for name in section_names if name in REQUIRED_REVIEW_SECTIONS or PORTFOLIO_SUMMARY_PATTERN.fullmatch(name)]

    for required in REQUIRED_REVIEW_SECTIONS:
        count = section_names.count(required)
        if count != 1:
            findings.append(
                TransitionReviewFinding(
                    "ERROR",
                    f"Transition Review must contain exactly one '{required}' section; found {count}.",
                    relative,
                )
            )
    if len(portfolio_sections) != 1:
        findings.append(
            TransitionReviewFinding(
                "ERROR",
                f"Transition Review must contain exactly one next-milestone Portfolio Summary section; found {len(portfolio_sections)}.",
                relative,
            )
        )
    elif milestone_number is not None:
        summary_number = int(re.search(r"\d+", portfolio_sections[0]).group())
        if summary_number != milestone_number + 1:
            findings.append(
                TransitionReviewFinding(
                    "ERROR",
                    f"Portfolio Summary must identify the immediate next milestone, Milestone {milestone_number + 1}.",
                    relative,
                )
            )
    if tuple(governed_sections) != expected:
        findings.append(
            TransitionReviewFinding(
                "ERROR",
                "The six governed Transition Review sections are missing, duplicated, or out of order.",
                relative,
            )
        )

    for index, match in enumerate(headings):
        name = match.group(1)
        if name not in REQUIRED_REVIEW_SECTIONS and not PORTFOLIO_SUMMARY_PATTERN.fullmatch(name):
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        body = text[match.end():end].strip()
        if not _has_substantive_evidence(body):
            findings.append(
                TransitionReviewFinding("ERROR", f"Transition Review section '{name}' has no substantive evidence.", relative)
            )

    if not any(finding.severity == "ERROR" for finding in findings):
        findings.append(
            TransitionReviewFinding(
                "INFO",
                "All six governed Transition Review sections are present, ordered, and populated; architecture, product, closeout, release, and live approvals remain separate.",
                relative,
            )
        )
    status = "FAIL" if any(finding.severity == "ERROR" for finding in findings) else "PASS"
    return TransitionReviewValidation(status, milestone, declared_status, tuple(findings))
