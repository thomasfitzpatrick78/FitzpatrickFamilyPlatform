from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from engineering.platform_eap.cli import main as platform_main
from engineering.platform_eap.conditional_authority import validate_phase_b_outcome_envelope
from engineering.platform_eap.execution_capability import evaluate_bounded_outcome_continuation
from engineering.platform_eap.outcome_envelope import OutcomeDisposition, validate_envelope
from engineering.platform_eap.outcome_envelope_io import (
    OutcomeEnvelopeDataError,
    envelope_sha256,
    load_outcome_envelope,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "engineering" / "tests" / "fixtures" / "outcome_envelope"
NOW = datetime(2026, 8, 6, tzinfo=timezone.utc)


def fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_valid_envelope_passes_and_phase_a_bridge_preserves_phase_b() -> None:
    envelope = fixture("valid_outcome_envelope.json")
    assert validate_envelope(envelope, now=NOW) == ()
    assert validate_phase_b_outcome_envelope(envelope) == ()


def test_material_change_stops_for_owner_but_routine_work_continues() -> None:
    assert validate_envelope(fixture("material_change_stop.json"), now=NOW) == ()
    routine = evaluate_bounded_outcome_continuation(acceptance_complete=False)
    assert routine.disposition == OutcomeDisposition.CONTINUE
    stopped = evaluate_bounded_outcome_continuation(
        acceptance_complete=False,
        material_changes=["security"],
    )
    assert stopped.disposition == OutcomeDisposition.STOP_FOR_OWNER
    assert stopped.material_conditions == ("security",)


def test_two_failures_trigger_internal_reassessment_not_owner_decision() -> None:
    reassess = evaluate_bounded_outcome_continuation(
        acceptance_complete=False,
        same_failure_count=2,
        correction_changed=False,
    )
    assert reassess.disposition == OutcomeDisposition.INTERNAL_REASSESSMENT
    corrected = evaluate_bounded_outcome_continuation(
        acceptance_complete=False,
        same_failure_count=3,
        correction_changed=True,
    )
    assert corrected.disposition == OutcomeDisposition.CONTINUE


def test_scope_expansion_fails_closed() -> None:
    findings = validate_envelope(fixture("invalid_scope_expansion.json"), now=NOW)
    assert any(finding.code == "overlapping_scope" for finding in findings)


def test_protected_publication_requires_bound_checkpoint() -> None:
    envelope = fixture("valid_outcome_envelope.json")
    envelope["tier_3_checkpoints"] = []
    findings = validate_envelope(envelope, now=NOW)
    assert any(finding.code == "missing_tier_3_checkpoint" for finding in findings)


def test_expiry_requires_revalidation_without_erasing_authority() -> None:
    envelope = fixture("valid_outcome_envelope.json")
    envelope["expiry_policy"]["expires_at"] = "2026-08-05T23:59:59Z"
    findings = validate_envelope(envelope, now=NOW)
    assert any(finding.code == "revalidation_required" for finding in findings)


def test_loader_is_confined_and_digest_is_deterministic(tmp_path: Path) -> None:
    target = tmp_path / "envelope.json"
    target.write_text(json.dumps(fixture("valid_outcome_envelope.json")), encoding="utf-8")
    loaded = load_outcome_envelope("envelope.json", tmp_path)
    assert envelope_sha256(loaded) == envelope_sha256(fixture("valid_outcome_envelope.json"))
    with pytest.raises(OutcomeEnvelopeDataError):
        load_outcome_envelope("../envelope.json", tmp_path)


def test_cli_validates_repository_fixture(capsys: pytest.CaptureFixture[str]) -> None:
    relative = "engineering/tests/fixtures/outcome_envelope/valid_outcome_envelope.json"
    assert platform_main(["outcome-envelope", "validate", relative]) == 0
    assert "Status: PASS" in capsys.readouterr().out
