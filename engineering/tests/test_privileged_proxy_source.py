import json
import shutil
from pathlib import Path

from engineering.platform_eap import cli
from engineering.platform_eap.privileged_proxy_source import (
    acceptance_summary,
    contract_summary,
    fixture_summary,
    supply_chain_summary,
    validate_source,
)


ROOT = Path(__file__).resolve().parents[2]


def test_privileged_proxy_source_validation_passes():
    assert validate_source(ROOT) == ()


def test_source_contract_is_transport_free_and_closed():
    contract = contract_summary(ROOT)
    assert contract["repository_validation"] == "PASS"
    assert contract["socket_capability"] == "absent"
    assert contract["network_capability"] == "absent"
    assert contract["docker_capability"] == "absent"
    assert contract["privileged_execution"] == "absent"
    assert contract["approved_operations"] == [
        "ResolveTargetIdentity",
        "ObserveHealth",
        "ObserveLifecycle",
        "ObserveRestartInformation",
        "ObserveStatisticsOnce",
    ]


def test_source_fixtures_and_acceptance_remain_repository_only():
    fixtures = fixture_summary(ROOT)
    acceptance = acceptance_summary(ROOT)
    assert fixtures["transport"] == "absent"
    assert fixtures["test_files"]
    assert acceptance["source_foundation"] == "satisfied"
    assert acceptance["socket_behavior"] == "not_satisfied"
    assert acceptance["privileged_deployment"] == "not_authorized"
    assert acceptance["named_target_observation"] == "not_authorized"


def test_supply_chain_evidence_is_honest_about_later_gaps():
    evidence = supply_chain_summary(ROOT)
    assert evidence["go_toolchain"]["version"] == "go1.26.5"
    assert evidence["dependencies"]["external_modules"] == []
    assert evidence["vulnerability_review"]["status"] == "documented_gap"
    assert evidence["provenance"]["slsa_claim"] == "none"
    assert evidence["source_revision"]["publication_commit"] is None


def test_validator_detects_prohibited_import(tmp_path):
    shutil.copytree(ROOT / "engineering/privileged_proxy", tmp_path / "engineering/privileged_proxy")
    fixture_root = tmp_path / "engineering/tests/fixtures/proxy_foundation"
    fixture_root.mkdir(parents=True)
    shutil.copy2(ROOT / "engineering/tests/fixtures/proxy_foundation/proxy-policy.json", fixture_root / "proxy-policy.json")
    shutil.copy2(ROOT / "go.mod", tmp_path / "go.mod")
    shutil.copy2(ROOT / "go.sum", tmp_path / "go.sum")
    unsafe = tmp_path / "engineering/privileged_proxy/core/unsafe.go"
    unsafe.write_text('package core\nimport "net"\n', encoding="utf-8")
    findings = validate_source(tmp_path)
    assert any(finding.code == "source.import.prohibited" and finding.reference.endswith("unsafe.go") for finding in findings)


def test_privileged_proxy_source_cli_commands(capsys):
    for command in (
        ["source", "validate"],
        ["source", "static-safety"],
        ["source", "contract"],
        ["source", "policy"],
        ["source", "fixtures"],
        ["source", "supply-chain"],
        ["source", "acceptance"],
    ):
        assert cli.privileged_proxy_cli(command) == 0
        output = capsys.readouterr().out
        assert output
        if command[1] not in {"validate", "static-safety"}:
            json.loads(output)


def test_privileged_proxy_cli_never_builds_or_executes():
    source = (ROOT / "engineering/platform_eap/privileged_proxy_source.py").read_text(encoding="utf-8")
    assert "subprocess" not in source
