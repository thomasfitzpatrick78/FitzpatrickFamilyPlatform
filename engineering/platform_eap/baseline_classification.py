from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from engineering.platform_eap.ai_session_readiness import (
    AISessionReadinessValidator,
    READY,
    READY_WITH_WARNINGS,
    write_readiness_report,
)


CLEAN = "Clean"
EXPECTED_GENERATED_EVIDENCE = "Expected Generated Evidence"
DIRTY = "Dirty"

PRODUCER_COMMAND = "./platform-eap ai-session readiness"
GOVERNED_EVIDENCE_PATHS = (
    "reports/engineering/ai_session_readiness/ai_session_readiness_report.json",
    "reports/engineering/ai_session_readiness/ai_session_readiness_report.md",
)
AUTHORITY_REQUIREMENTS = {
    "docs/milestones/Milestone_15/EO_15_1_Architecture_Gatekeeper_Baseline_Decision.md": (
        "Architecture Gatekeeper Approved; Published",
        "Expected Generated Evidence",
        "Dirty",
    ),
    "docs/milestones/Milestone_15/EO_15_1_Engineering_Lifecycle_Transition_Review_Operationalization_Work_Package.md": (
        "Architecture Gatekeeper Approved; Published",
        "Expected Generated Evidence",
        "Dirty",
    ),
    "docs/engineering-organization/ai-collaboration/AI_Session_Initialization_Standard.md": (
        "Expected Generated Evidence",
        "./platform-eap ai-session baseline",
        "--work-package",
    ),
}
WORK_PACKAGE_PERMISSION_FIELD = "Expected Generated Evidence Baseline"
WORK_PACKAGE_PERMISSION_PERMITTED = "Permitted"
WORK_PACKAGE_PERMISSION_PROHIBITED = "Prohibited"


@dataclass(frozen=True)
class BaselineFinding:
    severity: str
    message: str
    evidence: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class BaselineClassification:
    state: str
    command: str
    head: str | None
    work_package: str | None
    changed_paths: tuple[str, ...]
    evidence_hashes: dict[str, str]
    findings: tuple[BaselineFinding, ...]

    @property
    def errors(self) -> tuple[BaselineFinding, ...]:
        return tuple(finding for finding in self.findings if finding.severity == "ERROR")


GitRunner = Callable[[list[str]], tuple[bool, str]]


def _default_git_runner(root: Path) -> GitRunner:
    def run(args: list[str]) -> tuple[bool, str]:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        return completed.returncode == 0, completed.stdout.rstrip("\n")

    return run


def _status_entries(output: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in output.splitlines():
        if len(line) < 4:
            entries.append(("??", line.strip()))
            continue
        code = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        entries.append((code, path))
    return entries


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class GeneratedEvidenceBaselineClassifier:
    def __init__(
        self,
        root: Path,
        *,
        git_runner: GitRunner | None = None,
        work_package_path: str | None = None,
    ) -> None:
        self.root = root.resolve()
        self.git_runner = git_runner or _default_git_runner(self.root)
        self.work_package_path = work_package_path

    def classify(self) -> BaselineClassification:
        findings: list[BaselineFinding] = []
        head = self._repository_gate(findings)
        status_ok, status_output = self.git_runner(["status", "--porcelain=v1", "--untracked-files=all"])
        if not status_ok:
            findings.append(BaselineFinding("ERROR", "Working-tree status could not be inspected."))
            return self._result(DIRTY, head, (), {}, findings)

        entries = _status_entries(status_output)
        changed_paths = tuple(sorted(path for _, path in entries if path))
        if findings:
            return self._result(DIRTY, head, changed_paths, {}, findings)
        if not entries:
            findings.append(BaselineFinding("PASS", "No repository changes are present."))
            return self._result(CLEAN, head, (), {}, findings)

        expected_paths = set(GOVERNED_EVIDENCE_PATHS)
        actual_paths = set(changed_paths)
        allowed_codes = all(code == " M" for code, _ in entries)
        if actual_paths != expected_paths or len(entries) != len(expected_paths) or not allowed_codes:
            findings.append(
                BaselineFinding(
                    "ERROR",
                    "Repository changes are not exactly the two unstaged governed readiness outputs.",
                    changed_paths,
                )
            )
            return self._result(DIRTY, head, changed_paths, {}, findings)

        if not self._work_package_permits_expected_evidence(findings):
            return self._result(DIRTY, head, changed_paths, {}, findings)

        if not self._authority_is_current(findings):
            return self._result(DIRTY, head, changed_paths, {}, findings)

        verified, hashes, verification_findings = self._verify_generated_evidence(head)
        findings.extend(verification_findings)
        if not verified:
            return self._result(DIRTY, head, changed_paths, hashes, findings)
        findings.append(
            BaselineFinding(
                "PASS",
                "Only governed readiness outputs changed and both reproduce byte-for-byte from the governed producer at current HEAD.",
                changed_paths,
            )
        )
        return self._result(EXPECTED_GENERATED_EVIDENCE, head, changed_paths, hashes, findings)

    def _repository_gate(self, findings: list[BaselineFinding]) -> str | None:
        if self.root.name != "FitzpatrickFamilyPlatform" or not (self.root / ".git").exists():
            findings.append(BaselineFinding("ERROR", "Repository identity is not FitzpatrickFamilyPlatform."))

        commands = (
            (["branch", "--show-current"], "main", "Current branch must be main."),
            (["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], "origin/main", "Tracking branch must be origin/main."),
            (["rev-list", "--left-right", "--count", "HEAD...@{upstream}"], "0\t0", "Local and tracking heads must have ahead/behind 0/0."),
            (["diff", "--name-only", "--diff-filter=U"], "", "Unresolved merge conflicts are not permitted."),
        )
        for args, expected, message in commands:
            ok, output = self.git_runner(list(args))
            normalized = output.strip()
            if not ok or normalized != expected:
                evidence = (normalized,) if normalized else ()
                findings.append(BaselineFinding("ERROR", message, evidence))

        head_ok, head_output = self.git_runner(["rev-parse", "HEAD"])
        head = head_output.strip() if head_ok and re.fullmatch(r"[0-9a-fA-F]{40}", head_output.strip()) else None
        if head is None:
            findings.append(BaselineFinding("ERROR", "Current HEAD could not be resolved."))
        return head

    def _authority_is_current(self, findings: list[BaselineFinding]) -> bool:
        valid = True
        for relative, tokens in AUTHORITY_REQUIREMENTS.items():
            path = self.root / relative
            if not path.is_file():
                findings.append(BaselineFinding("ERROR", "Generated-evidence authority artifact is missing.", (relative,)))
                valid = False
                continue
            text = path.read_text(encoding="utf-8")
            missing = tuple(token for token in tokens if token not in text)
            if missing:
                findings.append(
                    BaselineFinding(
                        "ERROR",
                        "Generated-evidence authority artifact does not contain the required published policy evidence.",
                        (relative, *missing),
                    )
                )
                valid = False
        return valid

    def _work_package_permits_expected_evidence(self, findings: list[BaselineFinding]) -> bool:
        relative = self.work_package_path
        if not relative:
            findings.append(
                BaselineFinding(
                    "ERROR",
                    "Expected Generated Evidence requires an explicit authoritative work-package context.",
                )
            )
            return False
        candidate = Path(relative)
        safe = (
            not candidate.is_absolute()
            and ".." not in candidate.parts
            and "." not in candidate.parts
            and "\\" not in relative
            and len(candidate.parts) == 4
            and candidate.parts[:2] == ("docs", "milestones")
            and bool(re.fullmatch(r"Milestone_\d+", candidate.parts[2]))
            and bool(re.fullmatch(r"[A-Za-z0-9_]+_Work_Package\.md", candidate.name))
        )
        if not safe:
            findings.append(
                BaselineFinding(
                    "ERROR",
                    "Work-package context must be a canonical repository-relative milestone work-package path.",
                    (relative,),
                )
            )
            return False
        path = self.root / candidate
        if not path.is_file():
            findings.append(BaselineFinding("ERROR", "Work-package context does not exist.", (relative,)))
            return False
        tracked_ok, tracked_output = self.git_runner(["ls-files", "--error-unmatch", "--", relative])
        if not tracked_ok:
            evidence = (relative, tracked_output.strip()) if tracked_output.strip() else (relative,)
            findings.append(BaselineFinding("ERROR", "Work-package context is not tracked at current HEAD.", evidence))
            return False
        text = path.read_text(encoding="utf-8")
        permission_values = [
            value.strip()
            for value in re.findall(
                rf"^\*\*{re.escape(WORK_PACKAGE_PERMISSION_FIELD)}:\*\*\s*(.+?)\s*$",
                text,
                re.MULTILINE,
            )
        ]
        if len(permission_values) != 1:
            findings.append(
                BaselineFinding(
                    "ERROR",
                    "The authoritative work package must contain exactly one governed Expected Generated Evidence permission declaration.",
                    (relative,),
                )
            )
            return False
        value = permission_values[0]
        if value != WORK_PACKAGE_PERMISSION_PERMITTED:
            if value == WORK_PACKAGE_PERMISSION_PROHIBITED:
                message = "The authoritative work package prohibits an Expected Generated Evidence baseline."
            else:
                message = (
                    "The authoritative work package does not contain the exact governed Expected Generated Evidence permission."
                )
            findings.append(BaselineFinding("ERROR", message, (relative,)))
            return False
        findings.append(
            BaselineFinding(
                "PASS",
                "The tracked authoritative work package explicitly permits an Expected Generated Evidence baseline.",
                (relative,),
            )
        )
        return True

    def _verify_generated_evidence(
        self,
        head: str | None,
    ) -> tuple[bool, dict[str, str], list[BaselineFinding]]:
        findings: list[BaselineFinding] = []
        hashes = {
            relative: _sha256(self.root / relative)
            for relative in GOVERNED_EVIDENCE_PATHS
            if (self.root / relative).is_file()
        }
        if len(hashes) != len(GOVERNED_EVIDENCE_PATHS):
            findings.append(BaselineFinding("ERROR", "One or more governed readiness outputs are missing."))
            return False, hashes, findings

        json_path = self.root / GOVERNED_EVIDENCE_PATHS[0]
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            findings.append(BaselineFinding("ERROR", f"Governed readiness JSON is not parseable: {exc}."))
            return False, hashes, findings

        repository = payload.get("repository") if isinstance(payload, dict) else None
        generated_at = payload.get("generated_at") if isinstance(payload, dict) else None
        evidence_shape_ok = (
            isinstance(payload, dict)
            and payload.get("command") == PRODUCER_COMMAND
            and payload.get("readiness") in {READY, READY_WITH_WARNINGS}
            and payload.get("errors") == []
            and isinstance(generated_at, str)
            and bool(generated_at)
            and isinstance(repository, dict)
            and repository.get("head") == head
        )
        if not evidence_shape_ok:
            findings.append(
                BaselineFinding(
                    "ERROR",
                    "Governed readiness evidence lacks current-HEAD attribution, a permitted readiness state, zero errors, or the exact producer command.",
                    GOVERNED_EVIDENCE_PATHS,
                )
            )
            return False, hashes, findings

        try:
            with tempfile.TemporaryDirectory(prefix="platform-eap-readiness-") as temporary:
                expected_root = Path(temporary)
                result = AISessionReadinessValidator(
                    self.root,
                    git_runner=self.git_runner,
                    generated_at=lambda: generated_at,
                ).validate()
                expected_markdown, expected_json = write_readiness_report(result, expected_root)
                expected_by_relative = {
                    GOVERNED_EVIDENCE_PATHS[0]: expected_json,
                    GOVERNED_EVIDENCE_PATHS[1]: expected_markdown,
                }
                mismatches = [
                    relative
                    for relative, expected in expected_by_relative.items()
                    if (self.root / relative).read_bytes() != expected.read_bytes()
                ]
        except (OSError, UnicodeError, ValueError) as exc:
            findings.append(BaselineFinding("ERROR", f"Governed readiness evidence could not be reproduced: {exc}."))
            return False, hashes, findings

        if mismatches:
            findings.append(
                BaselineFinding(
                    "ERROR",
                    "Governed readiness outputs do not reproduce from the governed producer at current HEAD.",
                    tuple(mismatches),
                )
            )
            return False, hashes, findings
        return True, hashes, findings

    def _result(
        self,
        state: str,
        head: str | None,
        changed_paths: tuple[str, ...],
        evidence_hashes: dict[str, str],
        findings: list[BaselineFinding],
    ) -> BaselineClassification:
        return BaselineClassification(
            state=state,
            command=PRODUCER_COMMAND,
            head=head,
            work_package=self.work_package_path,
            changed_paths=changed_paths,
            evidence_hashes=evidence_hashes,
            findings=tuple(findings),
        )
