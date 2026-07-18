from __future__ import annotations

import json
import shutil
from pathlib import Path

from engineering.platform_eap import cli
from engineering.platform_eap.ai_session_readiness import (
    AISessionReadinessValidator,
    DEFAULT_CONFIGURATION,
    NOT_READY,
    READY,
    READY_WITH_WARNINGS,
    write_readiness_report,
)


BASELINE_HEAD = "7cfc8752ba6b48e8dbfb90f38d14a96fd3c92bbd"


def _fake_git(status: str = ""):
    def run(args: list[str]) -> tuple[bool, str]:
        if args[:2] == ["branch", "--show-current"]:
            return True, "main"
        if args[:2] == ["rev-parse", "HEAD"]:
            return True, BASELINE_HEAD
        if args[:3] == ["diff", "--name-only", "--diff-filter=U"]:
            return True, ""
        if args and args[0] == "status":
            return True, status
        return False, "unsupported test git command"

    return run


def _copy_fixture_file(root: Path, relative: str) -> None:
    source = cli.ROOT / relative
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _ready_fixture(tmp_path: Path) -> Path:
    root = tmp_path / DEFAULT_CONFIGURATION.expected_repository
    root.mkdir()
    (root / ".git").mkdir()
    required = set(DEFAULT_CONFIGURATION.permanent_governance)
    required.update(DEFAULT_CONFIGURATION.collaboration_artifacts)
    required.update(DEFAULT_CONFIGURATION.templates)
    required.add(DEFAULT_CONFIGURATION.role_catalog)
    required.update(DEFAULT_CONFIGURATION.planning_artifacts.values())
    for requirement in DEFAULT_CONFIGURATION.workstreams:
        required.add(f"{DEFAULT_CONFIGURATION.continuity_root}/{requirement.filename}")
    for relative in sorted(required):
        _copy_fixture_file(root, relative)
    for relative in (
        DEFAULT_CONFIGURATION.planning_artifacts["roadmap"],
        DEFAULT_CONFIGURATION.planning_artifacts["backlog"],
    ):
        path = root / relative
        path.write_text(
            path.read_text(encoding="utf-8").replace("**Milestone:** Milestone 12", "**Milestone:** Milestone 14", 1),
            encoding="utf-8",
        )
    return root


def _validate(root: Path, status: str = ""):
    return AISessionReadinessValidator(
        root,
        git_runner=_fake_git(status),
        generated_at=lambda: "2026-07-17T12:00:00+00:00",
    ).validate()


def _replace(root: Path, relative: str, old: str, new: str) -> None:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def _remove_field(root: Path, filename: str, field_name: str) -> None:
    path = root / DEFAULT_CONFIGURATION.continuity_root / filename
    lines = path.read_text(encoding="utf-8").splitlines()
    filtered = [line for line in lines if not line.startswith(f"| {field_name} |")]
    assert len(filtered) == len(lines) - 1
    path.write_text("\n".join(filtered) + "\n", encoding="utf-8")


def _messages(result) -> list[str]:
    return [check.message for domain in result.domains for check in domain.checks]


def test_ai_session_readiness_fully_ready_repository(tmp_path):
    result = _validate(_ready_fixture(tmp_path))
    assert result.readiness == READY
    assert not result.errors
    assert not result.warnings
    assert {domain.name for domain in result.domains} == {
        "Repository Identity",
        "Permanent Governance",
        "AI Collaboration Capability",
        "Role Readiness",
        "Active Milestone Readiness",
        "Workstream Continuity",
        "Architecture Traceability",
        "Parallel Workstream Consistency",
        "Readiness and Freshness",
    }


def test_ai_session_readiness_warns_for_active_source_changes(tmp_path):
    result = _validate(_ready_fixture(tmp_path), " M docs/example.md")
    assert result.readiness == READY_WITH_WARNINGS
    assert not result.errors
    assert any("active source changes" in warning.message for warning in result.warnings)


def test_ai_session_readiness_detects_missing_permanent_governance(tmp_path):
    root = _ready_fixture(tmp_path)
    (root / DEFAULT_CONFIGURATION.permanent_governance[0]).unlink()
    result = _validate(root)
    assert result.readiness == NOT_READY
    assert any("Permanent_Project_Operating_Model.md" in message and "missing" in message for message in _messages(result))


def test_ai_session_readiness_detects_missing_capability_charter(tmp_path):
    root = _ready_fixture(tmp_path)
    charter = next(path for path in DEFAULT_CONFIGURATION.collaboration_artifacts if "Capability_Charter" in path)
    (root / charter).unlink()
    result = _validate(root)
    assert result.readiness == NOT_READY
    assert any("Capability_Charter.md" in message and "missing" in message for message in _messages(result))


def test_ai_session_readiness_detects_missing_required_template(tmp_path):
    root = _ready_fixture(tmp_path)
    (root / DEFAULT_CONFIGURATION.templates[0]).unlink()
    result = _validate(root)
    assert result.readiness == NOT_READY
    assert any("Review_Template.md" in message and "missing" in message for message in _messages(result))


def test_ai_session_readiness_detects_missing_active_continuity_brief(tmp_path):
    root = _ready_fixture(tmp_path)
    (root / DEFAULT_CONFIGURATION.continuity_root / "Bravo_Continuity_Brief.md").unlink()
    result = _validate(root)
    assert result.readiness == NOT_READY
    assert any("Bravo continuity brief is missing" in message for message in _messages(result))


def test_ai_session_readiness_detects_duplicate_active_brief(tmp_path):
    root = _ready_fixture(tmp_path)
    source = root / DEFAULT_CONFIGURATION.continuity_root / "Alpha_Continuity_Brief.md"
    shutil.copy2(source, source.with_name("Alpha_Duplicate_Continuity_Brief.md"))
    result = _validate(root)
    assert result.readiness == NOT_READY
    assert any("Alpha must have exactly one Active continuity brief; found 2" in message for message in _messages(result))


def test_ai_session_readiness_detects_invalid_lifecycle_state(tmp_path):
    root = _ready_fixture(tmp_path)
    relative = f"{DEFAULT_CONFIGURATION.continuity_root}/Alpha_Continuity_Brief.md"
    _replace(root, relative, "**Status:** Active", "**Status:** Improvised")
    result = _validate(root)
    assert result.readiness == NOT_READY
    assert any("Invalid continuity lifecycle state: Improvised" in message for message in _messages(result))


def test_ai_session_readiness_detects_missing_assigned_role(tmp_path):
    root = _ready_fixture(tmp_path)
    _remove_field(root, "Alpha_Continuity_Brief.md", "Assigned role")
    result = _validate(root)
    assert any("missing required field: Assigned role" in message for message in _messages(result))


def test_ai_session_readiness_detects_missing_next_gate(tmp_path):
    root = _ready_fixture(tmp_path)
    _remove_field(root, "Alpha_Continuity_Brief.md", "Next gate")
    result = _validate(root)
    assert any("missing required field: Next gate" in message for message in _messages(result))


def test_ai_session_readiness_detects_missing_permitted_actions(tmp_path):
    root = _ready_fixture(tmp_path)
    _remove_field(root, "Alpha_Continuity_Brief.md", "Permitted actions")
    result = _validate(root)
    assert any("missing required field: Permitted actions" in message for message in _messages(result))


def test_ai_session_readiness_detects_missing_prohibited_actions(tmp_path):
    root = _ready_fixture(tmp_path)
    _remove_field(root, "Alpha_Continuity_Brief.md", "Prohibited actions")
    result = _validate(root)
    assert any("missing required field: Prohibited actions" in message for message in _messages(result))


def test_ai_session_readiness_detects_missing_stop_conditions(tmp_path):
    root = _ready_fixture(tmp_path)
    _remove_field(root, "Alpha_Continuity_Brief.md", "Stop conditions")
    result = _validate(root)
    assert any("missing required field: Stop conditions" in message for message in _messages(result))


def test_ai_session_readiness_detects_invalid_role_reference(tmp_path):
    root = _ready_fixture(tmp_path)
    relative = f"{DEFAULT_CONFIGURATION.continuity_root}/Alpha_Continuity_Brief.md"
    _replace(root, relative, "| Assigned role | Codex Implementation Engineer. |", "| Assigned role | Imaginary Executor. |")
    result = _validate(root)
    assert any("invalid assigned role reference: Imaginary Executor" in message for message in _messages(result))


def test_ai_session_readiness_detects_broken_architecture_traceability(tmp_path):
    root = _ready_fixture(tmp_path)
    relative = f"{DEFAULT_CONFIGURATION.continuity_root}/Alpha_Continuity_Brief.md"
    _replace(root, relative, "EO-14.1 and EO-14.4 specifications", "unidentified specifications")
    result = _validate(root)
    assert any("Alpha does not trace to authoritative evidence: EO-14.1" in message for message in _messages(result))


def test_ai_session_readiness_detects_charlie_missing_bravo_dependency(tmp_path):
    root = _ready_fixture(tmp_path)
    relative = f"{DEFAULT_CONFIGURATION.continuity_root}/Charlie_Continuity_Brief.md"
    _replace(root, relative, "| Dependencies | Bravo telemetry contract;", "| Dependencies |")
    result = _validate(root)
    assert any("Charlie is missing required dependency: Bravo" in message for message in _messages(result))


def test_ai_session_readiness_detects_circular_workstream_dependency(tmp_path):
    root = _ready_fixture(tmp_path)
    relative = f"{DEFAULT_CONFIGURATION.continuity_root}/Alpha_Continuity_Brief.md"
    _replace(root, relative, "| Dependencies | Architecture Integration;", "| Dependencies | Charlie;")
    result = _validate(root)
    assert any("Circular active-workstream dependency detected" in message for message in _messages(result))


def test_ai_session_readiness_command_routing(tmp_path, monkeypatch, capsys):
    root = _ready_fixture(tmp_path)
    monkeypatch.setattr(cli, "ROOT", root)
    monkeypatch.setattr(cli, "REPORT_ROOT", root / "reports" / "engineering")
    monkeypatch.setattr(
        cli,
        "AISessionReadinessValidator",
        lambda repository_root: AISessionReadinessValidator(repository_root, git_runner=_fake_git()),
    )
    exit_code = cli.main(["ai-session", "readiness"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "# AI Session Readiness Validation" in output
    assert "Overall readiness: READY" in output
    assert "Domain: Workstream Continuity - PASS" in output
    assert "Markdown report:" in output
    assert "JSON report:" in output


def test_ai_session_readiness_cli_exit_behavior(tmp_path, monkeypatch, capsys):
    root = _ready_fixture(tmp_path)
    (root / DEFAULT_CONFIGURATION.permanent_governance[0]).unlink()
    monkeypatch.setattr(cli, "ROOT", root)
    monkeypatch.setattr(cli, "REPORT_ROOT", root / "reports" / "engineering")
    monkeypatch.setattr(
        cli,
        "AISessionReadinessValidator",
        lambda repository_root: AISessionReadinessValidator(repository_root, git_runner=_fake_git()),
    )
    assert cli.main(["ai-session", "readiness"]) == 1
    assert "Overall readiness: NOT READY" in capsys.readouterr().out


def test_ai_session_readiness_cli_warning_exit_behavior(tmp_path, monkeypatch, capsys):
    root = _ready_fixture(tmp_path)
    monkeypatch.setattr(cli, "ROOT", root)
    monkeypatch.setattr(cli, "REPORT_ROOT", root / "reports" / "engineering")
    monkeypatch.setattr(
        cli,
        "AISessionReadinessValidator",
        lambda repository_root: AISessionReadinessValidator(
            repository_root,
            git_runner=_fake_git(" M docs/example.md"),
        ),
    )
    assert cli.main(["ai-session", "readiness"]) == 0
    assert "Overall readiness: READY WITH WARNINGS" in capsys.readouterr().out


def test_ai_session_readiness_cli_unexpected_failure_exit_behavior(tmp_path, monkeypatch, capsys):
    root = _ready_fixture(tmp_path)

    def fail(_repository_root):
        raise RuntimeError("test execution failure")

    monkeypatch.setattr(cli, "ROOT", root)
    monkeypatch.setattr(cli, "AISessionReadinessValidator", fail)
    assert cli.main(["ai-session", "readiness"]) == 3
    output = capsys.readouterr().out
    assert "Status: EXECUTION FAILURE" in output
    assert "test execution failure" in output


def test_ai_session_readiness_markdown_and_json_reports(tmp_path):
    result = _validate(_ready_fixture(tmp_path))
    markdown, machine = write_readiness_report(result, tmp_path / "reports")
    markdown_text = markdown.read_text(encoding="utf-8")
    payload = json.loads(machine.read_text(encoding="utf-8"))
    assert "**Readiness:** READY" in markdown_text
    assert "## Architecture Traceability" in markdown_text
    assert payload["readiness"] == READY
    assert payload["errors"] == []
    assert len(payload["domains"]) == 9


def test_ai_session_readiness_validator_does_not_mutate_repository(tmp_path):
    root = _ready_fixture(tmp_path)
    before = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
    result = _validate(root)
    after = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
    assert result.readiness == READY
    assert after == before
