from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

from engineering.platform_eap.cli import main as platform_main
from engineering.platform_eap.governance_state import validate_authority_index, validate_delivery_state
from engineering.platform_eap.outcome_envelope import validate_envelope


ROOT = Path(__file__).resolve().parents[2]
STATE_ROOT = ROOT / "docs" / "engineering-organization" / "ai-collaboration" / "operational" / "milestone-15"


def load(name: str) -> dict[str, object]:
    return json.loads((STATE_ROOT / name).read_text(encoding="utf-8"))


def test_platform_authority_index_has_one_effective_model() -> None:
    index = load("EO_15_2_Authority_Index.json")
    assert validate_authority_index(index) == ()
    assert index["effective_governance"]["model_id"] == "bounded_outcome_v2"
    assert index["effective_governance"]["status"] == "Active"


def test_platform_delivery_state_supports_fresh_task_recovery() -> None:
    state = load("EO_15_2_Delivery_State.json")
    assert validate_delivery_state(state) == ()
    assert state["next_action"]
    assert state["authority"]["authority_index"]


def test_current_bounded_outcome_is_valid() -> None:
    envelope = load("EO_15_2_Bounded_Outcome_Envelope.json")
    assert validate_envelope(envelope, now=datetime(2026, 8, 7, tzinfo=timezone.utc)) == ()


def test_one_isolated_writer_lane_is_allowed_and_overlap_fails() -> None:
    envelope = load("EO_15_2_Bounded_Outcome_Envelope.json")
    envelope["ownership"]["main_writer_active_roots"] = ["docs/governance"]
    envelope["ownership"]["writer_worktrees"] = [{
        "branch": "codex/isolated-writer",
        "excluded_roots": [],
        "integration_owner": "Codex main integrator",
        "owned_roots": ["engineering/platform_eap"],
        "worktree_id": "isolated-writer-worktree",
        "writer_id": "governed-writer",
    }]
    assert validate_envelope(envelope, now=datetime(2026, 8, 7, tzinfo=timezone.utc)) == ()
    conflicting = copy.deepcopy(envelope)
    conflicting["ownership"]["main_writer_active_roots"] = ["engineering"]
    findings = validate_envelope(conflicting, now=datetime(2026, 8, 7, tzinfo=timezone.utc))
    assert any(finding.code == "writer_scope_overlap" for finding in findings)


def test_governance_state_cli_is_side_effect_free(capsys) -> None:
    index_path = "docs/engineering-organization/ai-collaboration/operational/milestone-15/EO_15_2_Authority_Index.json"
    state_path = "docs/engineering-organization/ai-collaboration/operational/milestone-15/EO_15_2_Delivery_State.json"
    assert platform_main(["governance-state", "authority-index", "validate", index_path]) == 0
    assert "Status: PASS" in capsys.readouterr().out
    assert platform_main(["governance-state", "delivery-state", "validate", state_path]) == 0
    assert "Status: PASS" in capsys.readouterr().out
