from pathlib import Path
import shutil

from engineering.platform_eap import cli


def remove_generated_caches():
    for path in cli.ROOT.joinpath("engineering").rglob("__pycache__"):
        shutil.rmtree(path)



def test_repository_validation_passes_with_required_structure():
    remove_generated_caches()
    report = cli.repository_validate()
    assert report.status in {"PASS", "PASS WITH WARNINGS"}
    assert not [r for r in report.results if r.severity == "ERROR"]


def test_governance_validation_passes_with_initial_adrs():
    report = cli.governance_validate()
    assert report.status == "PASS"
    messages = [r.message for r in report.results]
    assert "Finance exclusions are governed by product boundary documents" in messages


def test_release_readiness_aggregates_validation():
    remove_generated_caches()
    report = cli.release_readiness()
    assert report.status in {"PASS", "PASS WITH WARNINGS"}
    assert any("Repository validation" in r.message for r in report.results)
    assert any("Governance validation" in r.message for r in report.results)


def test_milestone_closeout_has_required_artifacts():
    remove_generated_caches()
    report = cli.milestone_closeout()
    assert report.status in {"PASS", "PASS WITH WARNINGS"}
    assert not [r for r in report.results if r.severity == "ERROR"]


def test_engineering_metrics_counts_documents_and_adrs():
    report = cli.engineering_metrics()
    assert report.status == "PASS"
    assert any("Markdown documents" in r.message for r in report.results)
    assert any("Architecture decisions" in r.message for r in report.results)


def test_report_writer_creates_markdown_and_json(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "REPORT_ROOT", tmp_path)
    report = cli.engineering_metrics()
    cli.write_report("engineering_metrics", report)
    assert (tmp_path / "engineering_metrics" / "engineering_metrics_report.md").exists()
    assert (tmp_path / "engineering_metrics" / "engineering_metrics_report.json").exists()


def test_cli_capabilities_outputs_registered_capabilities(capsys):
    result = cli.main(["capabilities"])
    output = capsys.readouterr().out
    assert result == 0
    assert "PLAT-EAP-1" in output
    assert "Engineering Metrics" in output


def test_cli_invalid_command_returns_usage(capsys):
    result = cli.main(["unknown"])
    output = capsys.readouterr().out
    assert result == 2
    assert "Usage:" in output
