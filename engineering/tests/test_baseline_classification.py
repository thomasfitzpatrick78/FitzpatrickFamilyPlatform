from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from engineering.platform_eap import cli
from engineering.platform_eap.ai_session_readiness import (
    AISessionReadinessValidator,
    DEFAULT_CONFIGURATION,
    write_readiness_report,
)
from engineering.platform_eap.baseline_classification import (
    AUTHORITY_REQUIREMENTS,
    CLEAN,
    DIRTY,
    EXPECTED_GENERATED_EVIDENCE,
    GOVERNED_EVIDENCE_PATHS,
    GeneratedEvidenceBaselineClassifier,
)


HEAD = "8d69bfe4f8328f86602ebf22d53d813123ebfadb"
WORK_PACKAGE = (
    "docs/milestones/Milestone_15/"
    "EO_15_1_Engineering_Lifecycle_Transition_Review_Operationalization_Work_Package.md"
)


def _fake_git(full_status: str = ""):
    def run(args: list[str]) -> tuple[bool, str]:
        if args == ["branch", "--show-current"]:
            return True, "main"
        if args == ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"]:
            return True, "origin/main"
        if args == ["rev-list", "--left-right", "--count", "HEAD...@{upstream}"]:
            return True, "0\t0"
        if args == ["rev-parse", "HEAD"]:
            return True, HEAD
        if args == ["diff", "--name-only", "--diff-filter=U"]:
            return True, ""
        if args == ["status", "--porcelain=v1", "--untracked-files=all"]:
            return True, full_status
        if args == ["ls-files", "--error-unmatch", "--", WORK_PACKAGE]:
            return True, WORK_PACKAGE
        if args and args[0] == "status":
            return True, ""
        return False, "unsupported test git command"

    return run


def _copy(root: Path, relative: str) -> None:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cli.ROOT / relative, target)


def _fixture(tmp_path: Path) -> Path:
    root = tmp_path / "FitzpatrickFamilyPlatform"
    root.mkdir()
    (root / ".git").mkdir()
    required = set(DEFAULT_CONFIGURATION.permanent_governance)
    required.update(DEFAULT_CONFIGURATION.collaboration_artifacts)
    required.update(DEFAULT_CONFIGURATION.templates)
    required.add(DEFAULT_CONFIGURATION.role_catalog)
    required.update(DEFAULT_CONFIGURATION.planning_artifacts.values())
    required.update(AUTHORITY_REQUIREMENTS)
    for requirement in DEFAULT_CONFIGURATION.workstreams:
        required.add(f"{DEFAULT_CONFIGURATION.continuity_root}/{requirement.filename}")
    for relative in sorted(required):
        _copy(root, relative)
    return root


def _write_expected_reports(root: Path, git_runner) -> None:
    result = AISessionReadinessValidator(
        root,
        git_runner=git_runner,
        generated_at=lambda: "2026-07-25T21:30:00+00:00",
    ).validate()
    write_readiness_report(result, root / "reports/engineering/ai_session_readiness")


def _expected_status() -> str:
    return "\n".join(f" M {relative}" for relative in GOVERNED_EVIDENCE_PATHS)


def test_clean_baseline_has_no_changes(tmp_path):
    result = GeneratedEvidenceBaselineClassifier(_fixture(tmp_path), git_runner=_fake_git()).classify()
    assert result.state == CLEAN
    assert not result.errors


def test_expected_generated_evidence_requires_reproducible_current_head_outputs(tmp_path):
    root = _fixture(tmp_path)
    runner = _fake_git(_expected_status())
    _write_expected_reports(root, runner)
    result = GeneratedEvidenceBaselineClassifier(
        root,
        git_runner=runner,
        work_package_path=WORK_PACKAGE,
    ).classify()
    assert result.state == EXPECTED_GENERATED_EVIDENCE
    assert not result.errors
    assert set(result.evidence_hashes) == set(GOVERNED_EVIDENCE_PATHS)


def test_path_only_allowlisting_does_not_trust_edited_report(tmp_path):
    root = _fixture(tmp_path)
    runner = _fake_git(_expected_status())
    _write_expected_reports(root, runner)
    markdown = root / GOVERNED_EVIDENCE_PATHS[1]
    markdown.write_text(markdown.read_text(encoding="utf-8") + "unattributed edit\n", encoding="utf-8")
    result = GeneratedEvidenceBaselineClassifier(
        root,
        git_runner=runner,
        work_package_path=WORK_PACKAGE,
    ).classify()
    assert result.state == DIRTY
    assert any("do not reproduce" in finding.message for finding in result.errors)


def test_additional_or_untracked_path_is_dirty(tmp_path):
    root = _fixture(tmp_path)
    status = _expected_status() + "\n?? notes.txt"
    result = GeneratedEvidenceBaselineClassifier(root, git_runner=_fake_git(status)).classify()
    assert result.state == DIRTY
    assert "notes.txt" in result.changed_paths


def test_staged_generated_evidence_is_ambiguous_and_dirty(tmp_path):
    root = _fixture(tmp_path)
    status = "\n".join(f"M  {relative}" for relative in GOVERNED_EVIDENCE_PATHS)
    result = GeneratedEvidenceBaselineClassifier(root, git_runner=_fake_git(status)).classify()
    assert result.state == DIRTY


def test_work_package_prohibition_forces_dirty(tmp_path):
    root = _fixture(tmp_path)
    runner = _fake_git(_expected_status())
    work_package = root / WORK_PACKAGE
    work_package.write_text(
        work_package.read_text(encoding="utf-8").replace(
            "**Expected Generated Evidence Baseline:** Permitted",
            "**Expected Generated Evidence Baseline:** Prohibited",
            1,
        ),
        encoding="utf-8",
    )
    _write_expected_reports(root, runner)
    result = GeneratedEvidenceBaselineClassifier(
        root,
        git_runner=runner,
        work_package_path=WORK_PACKAGE,
    ).classify()
    assert result.state == DIRTY
    assert any("authoritative work package prohibits" in finding.message for finding in result.errors)


def test_expected_generated_evidence_without_work_package_context_is_dirty(tmp_path):
    root = _fixture(tmp_path)
    runner = _fake_git(_expected_status())
    _write_expected_reports(root, runner)
    result = GeneratedEvidenceBaselineClassifier(root, git_runner=runner).classify()
    assert result.state == DIRTY
    assert any("requires an explicit authoritative work-package context" in finding.message for finding in result.errors)


def test_authority_drift_forces_dirty(tmp_path):
    root = _fixture(tmp_path)
    runner = _fake_git(_expected_status())
    _write_expected_reports(root, runner)
    authority = root / next(iter(AUTHORITY_REQUIREMENTS))
    authority.write_text("authority removed\n", encoding="utf-8")
    result = GeneratedEvidenceBaselineClassifier(
        root,
        git_runner=runner,
        work_package_path=WORK_PACKAGE,
    ).classify()
    assert result.state == DIRTY
    assert any("authority artifact" in finding.message for finding in result.errors)


def test_baseline_cli_routes_machine_readable_output(tmp_path, monkeypatch, capsys):
    root = _fixture(tmp_path)
    monkeypatch.setattr(
        cli,
        "GeneratedEvidenceBaselineClassifier",
        lambda _root, work_package_path=None: GeneratedEvidenceBaselineClassifier(
            root,
            git_runner=_fake_git(),
            work_package_path=work_package_path,
        ),
    )
    assert cli.main(["ai-session", "baseline", "--json"]) == 0
    assert '"state": "Clean"' in capsys.readouterr().out


def test_baseline_cli_enforces_work_package_prohibition_end_to_end(tmp_path, monkeypatch, capsys):
    root = _fixture(tmp_path)
    runner = _fake_git(_expected_status())
    work_package = root / WORK_PACKAGE
    work_package.write_text(
        work_package.read_text(encoding="utf-8").replace(
            "**Expected Generated Evidence Baseline:** Permitted",
            "**Expected Generated Evidence Baseline:** Prohibited",
            1,
        ),
        encoding="utf-8",
    )
    _write_expected_reports(root, runner)

    def factory(_root, *, work_package_path=None):
        return GeneratedEvidenceBaselineClassifier(
            root,
            git_runner=runner,
            work_package_path=work_package_path,
        )

    monkeypatch.setattr(cli, "GeneratedEvidenceBaselineClassifier", factory)
    assert cli.main(["ai-session", "baseline", "--work-package", WORK_PACKAGE]) == 1
    output = capsys.readouterr().out
    assert "Baseline state: Dirty" in output
    assert "authoritative work package prohibits" in output


@pytest.mark.parametrize(
    "duplicate_value",
    ["Permitted", "Prohibited"],
    ids=["duplicate-permission", "conflicting-permission"],
)
def test_baseline_cli_rejects_ambiguous_work_package_permission_end_to_end(
    tmp_path,
    monkeypatch,
    capsys,
    duplicate_value,
):
    root = _fixture(tmp_path)
    runner = _fake_git(_expected_status())
    work_package = root / WORK_PACKAGE
    work_package.write_text(
        work_package.read_text(encoding="utf-8")
        + f"\n**Expected Generated Evidence Baseline:** {duplicate_value}\n",
        encoding="utf-8",
    )
    _write_expected_reports(root, runner)

    def factory(_root, *, work_package_path=None):
        return GeneratedEvidenceBaselineClassifier(
            root,
            git_runner=runner,
            work_package_path=work_package_path,
        )

    monkeypatch.setattr(cli, "GeneratedEvidenceBaselineClassifier", factory)
    assert cli.main(["ai-session", "baseline", "--work-package", WORK_PACKAGE]) == 1
    output = capsys.readouterr().out
    assert "Baseline state: Dirty" in output
    assert "must contain exactly one governed Expected Generated Evidence permission declaration" in output
