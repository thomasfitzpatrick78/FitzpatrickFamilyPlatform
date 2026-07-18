import json
from pathlib import Path

import pytest

from engineering.platform_eap import cli


GENERATED_AT = "2026-07-17T20:00:00+00:00"


def readiness_payload(state: str) -> dict[str, object]:
    errors: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    if state == "READY WITH WARNINGS":
        warnings = [{"check_id": "repository.working-tree", "severity": "WARNING"}]
    elif state == "NOT READY":
        errors = [{"check_id": "governance.required", "severity": "ERROR"}]
    return {
        "capability": "AI Session Readiness Validation",
        "command": "./platform-eap ai-session readiness",
        "readiness": state,
        "generated_at": GENERATED_AT,
        "repository": {"name": "FitzpatrickFamilyPlatform"},
        "domains": [
            {"name": "Repository Identity", "status": "PASS", "checks": []},
            {"name": "Permanent Governance", "status": "PASS", "checks": []},
            {"name": "AI Collaboration Capability", "status": "PASS", "checks": []},
        ],
        "errors": errors,
        "warnings": warnings,
    }


def write_payload(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


@pytest.mark.parametrize(
    ("state", "blocking_status", "report_status"),
    [
        ("READY", "NONBLOCKING", "PASS"),
        ("READY WITH WARNINGS", "NONBLOCKING WITH CONDITIONS", "PASS WITH WARNINGS"),
        ("NOT READY", "BLOCKING", "PASS WITH WARNINGS"),
    ],
)
def test_engineering_metrics_consumes_governed_readiness_states(tmp_path, state, blocking_status, report_status):
    report_path = tmp_path / "readiness.json"
    write_payload(report_path, readiness_payload(state))

    report = cli.engineering_metrics(report_path)

    assert report.status == report_status
    assert report.ai_session_readiness is not None
    assert report.ai_session_readiness.status == state
    assert report.ai_session_readiness.blocking_status == blocking_status
    assert report.ai_session_readiness.evidence_status == "current"
    assert report.ai_session_readiness.evidence_usable is True


def test_missing_readiness_report_is_unknown_and_actionable(tmp_path):
    report = cli.engineering_metrics(tmp_path / "missing.json")
    metric = report.ai_session_readiness

    assert metric is not None
    assert metric.status == "UNKNOWN"
    assert metric.evidence_status == "unavailable"
    assert metric.evidence_usable is False
    assert metric.blocking_status == "UNKNOWN"
    assert "./platform-eap ai-session readiness" in metric.caveat
    assert report.status == "PASS WITH WARNINGS"


def test_markdown_without_json_is_unknown(tmp_path):
    (tmp_path / "ai_session_readiness_report.md").write_text("# governed markdown\n", encoding="utf-8")
    metric = cli.load_ai_session_readiness_metric(tmp_path / "ai_session_readiness_report.json")

    assert metric.status == "UNKNOWN"
    assert metric.evidence_status == "unavailable"


def test_malformed_readiness_json_is_unknown_without_crashing(tmp_path):
    report_path = tmp_path / "readiness.json"
    report_path.write_text("{not-json", encoding="utf-8")

    metric = cli.load_ai_session_readiness_metric(report_path)

    assert metric.status == "UNKNOWN"
    assert metric.evidence_status == "malformed"
    assert metric.evidence_usable is False


@pytest.mark.parametrize(
    "mutation",
    [
        lambda payload: payload.update(readiness="HEALTHY"),
        lambda payload: payload.pop("generated_at"),
        lambda payload: payload.update(generated_at="not-a-timestamp"),
        lambda payload: payload.pop("command"),
        lambda payload: payload.pop("domains"),
        lambda payload: payload.update(domains=[]),
        lambda payload: payload.update(warnings=["unstructured"]),
    ],
)
def test_invalid_or_incomplete_readiness_evidence_is_malformed(tmp_path, mutation):
    report_path = tmp_path / "readiness.json"
    payload = readiness_payload("READY")
    mutation(payload)
    write_payload(report_path, payload)

    metric = cli.load_ai_session_readiness_metric(report_path)

    assert metric.status == "UNKNOWN"
    assert metric.evidence_status == "malformed"
    assert metric.evidence_usable is False


def test_logically_inconsistent_readiness_evidence_is_malformed(tmp_path):
    report_path = tmp_path / "readiness.json"
    payload = readiness_payload("READY")
    payload["warnings"] = [{"check_id": "unexpected", "severity": "WARNING"}]
    write_payload(report_path, payload)

    metric = cli.load_ai_session_readiness_metric(report_path)

    assert metric.status == "UNKNOWN"
    assert metric.evidence_status == "malformed"


def test_readiness_counts_domains_timestamp_and_path_are_preserved(tmp_path):
    report_path = tmp_path / "readiness.json"
    payload = readiness_payload("READY WITH WARNINGS")
    payload["warnings"] = [
        {"check_id": "one", "severity": "WARNING"},
        {"check_id": "two", "severity": "WARNING"},
    ]
    write_payload(report_path, payload)

    metric = cli.load_ai_session_readiness_metric(report_path)

    assert metric.error_count == 0
    assert metric.warning_count == 2
    assert metric.domain_count == 3
    assert metric.generated_at == GENERATED_AT
    assert metric.report_path == str(report_path)


def test_engineering_metrics_does_not_recalculate_readiness(tmp_path, monkeypatch):
    report_path = tmp_path / "readiness.json"
    write_payload(report_path, readiness_payload("READY"))

    def fail_if_called(*args, **kwargs):
        raise AssertionError("validator must not be called by Engineering Metrics")

    monkeypatch.setattr(cli.AISessionReadinessValidator, "validate", fail_if_called)

    assert cli.engineering_metrics(report_path).ai_session_readiness.status == "READY"


def test_engineering_metrics_does_not_modify_readiness_report(tmp_path):
    report_path = tmp_path / "readiness.json"
    write_payload(report_path, readiness_payload("READY"))
    original_content = report_path.read_bytes()
    original_mtime = report_path.stat().st_mtime_ns

    cli.engineering_metrics(report_path)

    assert report_path.read_bytes() == original_content
    assert report_path.stat().st_mtime_ns == original_mtime


@pytest.mark.parametrize("state", ["READY", "READY WITH WARNINGS", "NOT READY"])
def test_platform_health_source_preserves_governed_state(tmp_path, state):
    report_path = tmp_path / "readiness.json"
    write_payload(report_path, readiness_payload(state))
    metric = cli.load_ai_session_readiness_metric(report_path)

    health = cli.ai_session_readiness_health_source(metric)

    assert health["state"] == state
    assert health["error_count"] == metric.error_count
    assert health["warning_count"] == metric.warning_count
    assert health["evidence_status"] == "current"
    assert health["last_generated_at"] == GENERATED_AT
    assert health["source_available"] is True
    assert health["source_usable"] is True


def test_platform_health_missing_evidence_is_unknown_not_healthy(tmp_path):
    metric = cli.load_ai_session_readiness_metric(tmp_path / "missing.json")

    health = cli.ai_session_readiness_health_source(metric)

    assert health["state"] == "UNKNOWN"
    assert health["source_available"] is False
    assert health["source_usable"] is False


def test_engineering_metrics_reports_include_structured_and_markdown_readiness(tmp_path, monkeypatch):
    source_path = tmp_path / "source.json"
    write_payload(source_path, readiness_payload("READY WITH WARNINGS"))
    report_root = tmp_path / "reports"
    monkeypatch.setattr(cli, "REPORT_ROOT", report_root)

    cli.write_report("engineering_metrics", cli.engineering_metrics(source_path))

    json_report = json.loads(
        (report_root / "engineering_metrics" / "engineering_metrics_report.json").read_text(encoding="utf-8")
    )
    markdown_report = (
        report_root / "engineering_metrics" / "engineering_metrics_report.md"
    ).read_text(encoding="utf-8")
    assert json_report["ai_session_readiness"]["status"] == "READY WITH WARNINGS"
    assert json_report["ai_session_readiness"]["warning_count"] == 1
    assert json_report["platform_health"]["ai_session_readiness"]["state"] == "READY WITH WARNINGS"
    assert "## AI Session Readiness" in markdown_report
    assert "Overall readiness: READY WITH WARNINGS" in markdown_report
    assert "Source of truth: `./platform-eap ai-session readiness`" in markdown_report


def test_engineering_metrics_cli_remains_successful_with_unknown_evidence(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "REPORT_ROOT", tmp_path / "reports")
    monkeypatch.setattr(cli, "AI_SESSION_READINESS_REPORT", tmp_path / "missing.json")

    result = cli.main(["engineering", "metrics"])
    output = capsys.readouterr().out

    assert result == 0
    assert "# Engineering Metrics" in output
    assert "Status: PASS WITH WARNINGS" in output
    assert "run ./platform-eap ai-session readiness" in output
    assert (tmp_path / "reports" / "engineering_metrics" / "engineering_metrics_report.json").is_file()
