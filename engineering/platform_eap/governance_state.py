"""Side-effect-free validation for repository continuity interfaces."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any

from engineering.platform_eap.outcome_envelope import OutcomeFinding


AUTHORITY_INDEX_VERSION = "1.0"
DELIVERY_STATE_VERSION = "1.0"
HEX_40 = re.compile(r"[0-9a-f]{40}")
IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9._-]{2,127}")
ACTIVE_WORKSTREAM_STATUSES = {"Accepted", "Implementing", "Validating", "Publishing", "Blocked"}


def _object(value: Any, path: str, findings: list[OutcomeFinding]) -> dict[str, Any]:
    if not isinstance(value, dict):
        findings.append(OutcomeFinding("invalid_type", "must be an object", path))
        return {}
    return value


def _exact_keys(value: dict[str, Any], required: set[str], path: str, findings: list[OutcomeFinding]) -> None:
    missing = required - set(value)
    unknown = set(value) - required
    if missing:
        findings.append(OutcomeFinding("missing_fields", ", ".join(sorted(missing)), path))
    if unknown:
        findings.append(OutcomeFinding("unknown_fields", ", ".join(sorted(unknown)), path))


def _text(value: Any, path: str, findings: list[OutcomeFinding]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        findings.append(OutcomeFinding("missing_value", "must be a non-empty string", path))
        return None
    return value.strip()


def _path(value: Any, path: str, findings: list[OutcomeFinding]) -> str | None:
    text = _text(value, path, findings)
    if text is None:
        return None
    candidate = PurePosixPath(text)
    if candidate.is_absolute() or ".." in candidate.parts or "\\" in text or text != candidate.as_posix():
        findings.append(OutcomeFinding("invalid_path", "must be a safe repository-relative path", path))
        return None
    return text


def _strings(value: Any, path: str, findings: list[OutcomeFinding]) -> list[str]:
    if not isinstance(value, list):
        findings.append(OutcomeFinding("invalid_type", "must be a list", path))
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        text = _text(item, f"{path}[{index}]", findings)
        if text is not None:
            result.append(text)
    if len(result) != len(set(result)):
        findings.append(OutcomeFinding("duplicate_value", "must not contain duplicates", path))
    return result


def validate_authority_index(value: Any) -> tuple[OutcomeFinding, ...]:
    findings: list[OutcomeFinding] = []
    root = _object(value, "$", findings)
    _exact_keys(root, {"schema_version", "repository", "effective_governance", "active_workstreams", "historical_authority", "repository_overlays", "recovery_order"}, "$", findings)
    if root.get("schema_version") != AUTHORITY_INDEX_VERSION:
        findings.append(OutcomeFinding("unsupported_schema", f"must equal {AUTHORITY_INDEX_VERSION}", "schema_version"))
    _text(root.get("repository"), "repository", findings)
    governance = _object(root.get("effective_governance"), "effective_governance", findings)
    _exact_keys(governance, {"model_id", "schema_major", "status", "standard_path", "effective_from"}, "effective_governance", findings)
    if governance.get("model_id") != "bounded_outcome_v2" or governance.get("schema_major") != 2 or governance.get("status") != "Active":
        findings.append(OutcomeFinding("inactive_or_competing_model", "exactly bounded_outcome_v2 schema major 2 must be Active", "effective_governance"))
    _path(governance.get("standard_path"), "effective_governance.standard_path", findings)
    _text(governance.get("effective_from"), "effective_governance.effective_from", findings)
    workstreams = root.get("active_workstreams")
    if not isinstance(workstreams, list):
        findings.append(OutcomeFinding("invalid_type", "must be a list", "active_workstreams"))
    else:
        ids: list[str] = []
        for index, raw in enumerate(workstreams):
            item_path = f"active_workstreams[{index}]"
            item = _object(raw, item_path, findings)
            _exact_keys(item, {"workstream_id", "status", "outcome_envelope", "delivery_state"}, item_path, findings)
            workstream_id = item.get("workstream_id")
            if not isinstance(workstream_id, str) or not IDENTIFIER.fullmatch(workstream_id):
                findings.append(OutcomeFinding("invalid_identifier", "must be a lowercase governed identifier", f"{item_path}.workstream_id"))
            else:
                ids.append(workstream_id)
            if item.get("status") not in ACTIVE_WORKSTREAM_STATUSES:
                findings.append(OutcomeFinding("invalid_status", "must be an active workstream status", f"{item_path}.status"))
            _path(item.get("outcome_envelope"), f"{item_path}.outcome_envelope", findings)
            _path(item.get("delivery_state"), f"{item_path}.delivery_state", findings)
        if len(ids) != len(set(ids)):
            findings.append(OutcomeFinding("duplicate_value", "workstream ids must be unique", "active_workstreams"))
    history = root.get("historical_authority")
    if not isinstance(history, list):
        findings.append(OutcomeFinding("invalid_type", "must be a list", "historical_authority"))
    else:
        for index, raw in enumerate(history):
            item_path = f"historical_authority[{index}]"
            item = _object(raw, item_path, findings)
            _exact_keys(item, {"path", "disposition", "replacement"}, item_path, findings)
            _path(item.get("path"), f"{item_path}.path", findings)
            if item.get("disposition") not in {"Historical Only", "Superseded"}:
                findings.append(OutcomeFinding("invalid_disposition", "must be Historical Only or Superseded", f"{item_path}.disposition"))
            _path(item.get("replacement"), f"{item_path}.replacement", findings)
    _strings(root.get("repository_overlays"), "repository_overlays", findings)
    recovery = _strings(root.get("recovery_order"), "recovery_order", findings)
    if not recovery or recovery[0] != "AGENTS.md":
        findings.append(OutcomeFinding("invalid_recovery_order", "must begin with AGENTS.md", "recovery_order"))
    return tuple(findings)


def validate_delivery_state(value: Any) -> tuple[OutcomeFinding, ...]:
    findings: list[OutcomeFinding] = []
    root = _object(value, "$", findings)
    _exact_keys(root, {"schema_version", "repository", "updated_at", "outcome", "authority", "baseline", "completed_work", "active_changes", "repair_assessments", "subagent_lanes", "evidence", "blockers", "next_action"}, "$", findings)
    if root.get("schema_version") != DELIVERY_STATE_VERSION:
        findings.append(OutcomeFinding("unsupported_schema", f"must equal {DELIVERY_STATE_VERSION}", "schema_version"))
    _text(root.get("repository"), "repository", findings)
    _text(root.get("updated_at"), "updated_at", findings)
    outcome = _object(root.get("outcome"), "outcome", findings)
    _exact_keys(outcome, {"outcome_id", "status", "envelope_path"}, "outcome", findings)
    if not isinstance(outcome.get("outcome_id"), str) or not IDENTIFIER.fullmatch(outcome["outcome_id"]):
        findings.append(OutcomeFinding("invalid_identifier", "must be a lowercase governed identifier", "outcome.outcome_id"))
    if outcome.get("status") not in ACTIVE_WORKSTREAM_STATUSES | {"Completed"}:
        findings.append(OutcomeFinding("invalid_status", "must be a governed delivery status", "outcome.status"))
    _path(outcome.get("envelope_path"), "outcome.envelope_path", findings)
    authority = _object(root.get("authority"), "authority", findings)
    _exact_keys(authority, {"decision_record", "authority_index"}, "authority", findings)
    _path(authority.get("decision_record"), "authority.decision_record", findings)
    _path(authority.get("authority_index"), "authority.authority_index", findings)
    baseline = _object(root.get("baseline"), "baseline", findings)
    _exact_keys(baseline, {"branch", "head", "tracking_branch", "live_remote_verified"}, "baseline", findings)
    _text(baseline.get("branch"), "baseline.branch", findings)
    if not isinstance(baseline.get("head"), str) or not HEX_40.fullmatch(baseline["head"]):
        findings.append(OutcomeFinding("invalid_baseline", "must be a 40-character lowercase Git object id", "baseline.head"))
    _text(baseline.get("tracking_branch"), "baseline.tracking_branch", findings)
    if type(baseline.get("live_remote_verified")) is not bool:
        findings.append(OutcomeFinding("invalid_type", "must be a boolean", "baseline.live_remote_verified"))
    for field in ("completed_work", "active_changes", "repair_assessments", "subagent_lanes", "evidence", "blockers"):
        _strings(root.get(field), field, findings)
    _text(root.get("next_action"), "next_action", findings)
    return tuple(findings)
