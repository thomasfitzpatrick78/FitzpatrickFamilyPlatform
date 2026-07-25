from __future__ import annotations

from pathlib import Path

import pytest

from engineering.platform_eap import cli
from engineering.platform_eap.transition_review import validate_transition_review


RELATIVE = "docs/milestones/Milestone_16/Milestone_16_Transition_Review.md"


def _review() -> str:
    return """# Milestone 16 Transition Review

**Status:** Prepared for review

**Milestone:** Milestone 16

## Milestone Accomplishment Review

Repository evidence records the completed scope.

## Deferred Work & Waiting on External Events

Deferred work retains an owner and next gate.

## Engineering Learning Review

The review records evidence-based learning.

## Engineering Decision Register Updates

No approval is inferred from this capture.

## Portfolio Health Review

Current state and planned state remain distinct.

## Milestone 17 Portfolio Summary

The next milestone summary remains subject to portfolio approval.
"""


def _write(root: Path, text: str) -> None:
    path = root / RELATIVE
    path.parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")


def test_transition_review_validates_six_populated_sections_without_approving_status(tmp_path):
    _write(tmp_path, _review())
    result = validate_transition_review(tmp_path, RELATIVE)
    assert result.status == "PASS"
    assert result.declared_status == "Prepared for review"
    assert any("does not approve" in finding.message for finding in result.findings)


def test_transition_review_rejects_missing_section(tmp_path):
    _write(tmp_path, _review().replace("## Engineering Learning Review\n\nThe review records evidence-based learning.\n\n", ""))
    result = validate_transition_review(tmp_path, RELATIVE)
    assert result.status == "FAIL"
    assert any("Engineering Learning Review" in finding.message for finding in result.findings)


def test_transition_review_rejects_empty_section(tmp_path):
    _write(tmp_path, _review().replace("Repository evidence records the completed scope.", "TBD"))
    result = validate_transition_review(tmp_path, RELATIVE)
    assert result.status == "FAIL"
    assert any("no substantive evidence" in finding.message for finding in result.findings)


@pytest.mark.parametrize(
    "placeholder",
    (
        "N/A",
        "- TBD",
        "- [ ] TODO: add evidence here",
        "[TBD](https://example.invalid/placeholder)",
        "| Item | Evidence |\n|------|----------|\n| Accomplishment | TBD |",
        "<!-- TODO: provide evidence -->",
        "<p>TBD</p>",
    ),
)
def test_transition_review_rejects_markdown_placeholder_only_section(tmp_path, placeholder):
    _write(tmp_path, _review().replace("Repository evidence records the completed scope.", placeholder))
    result = validate_transition_review(tmp_path, RELATIVE)
    assert result.status == "FAIL"
    assert any("no substantive evidence" in finding.message for finding in result.findings)


def test_transition_review_rejects_reordered_sections(tmp_path):
    text = _review()
    first = "## Milestone Accomplishment Review\n\nRepository evidence records the completed scope.\n\n"
    second = "## Deferred Work & Waiting on External Events\n\nDeferred work retains an owner and next gate.\n\n"
    _write(tmp_path, text.replace(first + second, second + first))
    result = validate_transition_review(tmp_path, RELATIVE)
    assert result.status == "FAIL"
    assert any("out of order" in finding.message for finding in result.findings)


def test_transition_review_requires_corresponding_next_milestone_summary(tmp_path):
    _write(tmp_path, _review().replace("Milestone 17 Portfolio Summary", "Milestone 18 Portfolio Summary"))
    result = validate_transition_review(tmp_path, RELATIVE)
    assert result.status == "FAIL"
    assert any("immediate next milestone" in finding.message for finding in result.findings)


def test_transition_review_requires_matching_path_and_metadata_milestone(tmp_path):
    _write(tmp_path, _review().replace("**Milestone:** Milestone 16", "**Milestone:** Milestone 15"))
    result = validate_transition_review(tmp_path, RELATIVE)
    assert result.status == "FAIL"
    assert any("directory, and filename" in finding.message for finding in result.findings)


def test_transition_review_rejects_unsafe_or_noncanonical_path(tmp_path):
    result = validate_transition_review(tmp_path, "../outside.md")
    assert result.status == "FAIL"
    assert any("safe repository-relative" in finding.message for finding in result.findings)


def test_transition_review_cli_writes_existing_report_evidence(tmp_path, monkeypatch, capsys):
    _write(tmp_path, _review())
    monkeypatch.setattr(cli, "ROOT", tmp_path)
    monkeypatch.setattr(cli, "REPORT_ROOT", tmp_path / "reports" / "engineering")
    assert cli.main(["milestone", "transition-review", RELATIVE]) == 0
    assert "Status: PASS" in capsys.readouterr().out
    report_root = tmp_path / "reports/engineering/transition_review"
    assert (report_root / "transition_review_report.md").is_file()
    assert (report_root / "transition_review_report.json").is_file()
