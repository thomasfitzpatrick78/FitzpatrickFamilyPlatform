"""Phase B bounded-outcome authority model and side-effect-free validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import PurePosixPath
from typing import Any, Iterable


SCHEMA_VERSION = "2.0"
HEX_40 = re.compile(r"[0-9a-f]{40}")
HEX_64 = re.compile(r"[0-9a-f]{64}")
IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9._-]{2,127}")
MATERIAL_STOP_CONDITIONS = {
    "architecture",
    "public_contract",
    "security",
    "privacy",
    "customer_data_boundary",
    "cost",
    "production_scope",
    "release",
    "destructive_action",
    "required_tools",
    "approved_outcome",
}
ALLOWED_ACTION_CLASSES = {
    "read",
    "implement",
    "diagnose",
    "repair",
    "validate",
    "generate_evidence",
    "stage",
    "commit",
    "publish",
    "fetch_and_prove_equality",
}
PROTECTED_ACTION_CLASSES = {"publish"}
OUTPUT_CLASSES = {
    "no_repository_write",
    "isolated_temporary_output",
    "deterministic_tracked_report",
    "sealed_child_subject",
}
REQUIRED_SANITIZATION = {
    "no_personal_name",
    "no_absolute_checkout_path",
    "no_credential",
    "no_customer_or_protected_value",
    "no_prompt_text",
}


class OutcomeDisposition(str, Enum):
    CONTINUE = "continue"
    INTERNAL_REASSESSMENT = "internal_reassessment"
    STOP_FOR_OWNER = "stop_for_owner"
    COMPLETE = "complete"


@dataclass(frozen=True)
class OutcomeFinding:
    code: str
    message: str
    path: str | None = None


@dataclass(frozen=True)
class ContinuationAssessment:
    disposition: OutcomeDisposition
    reason: str
    material_conditions: tuple[str, ...] = ()


def _mapping(value: Any, path: str, findings: list[OutcomeFinding]) -> dict[str, Any]:
    if not isinstance(value, dict):
        findings.append(OutcomeFinding("invalid_type", "must be an object", path))
        return {}
    return value


def _strings(value: Any, path: str, findings: list[OutcomeFinding], *, required: bool = True) -> list[str]:
    if not isinstance(value, list):
        findings.append(OutcomeFinding("invalid_type", "must be a list", path))
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            findings.append(OutcomeFinding("invalid_value", "must be a non-empty string", f"{path}[{index}]"))
        else:
            result.append(item.strip())
    if required and not result:
        findings.append(OutcomeFinding("missing_value", "must contain at least one item", path))
    if len(result) != len(set(result)):
        findings.append(OutcomeFinding("duplicate_value", "must not contain duplicates", path))
    return result


def _safe_root(value: Any, path: str, findings: list[OutcomeFinding]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        findings.append(OutcomeFinding("invalid_path", "must be a non-empty repository-relative path", path))
        return None
    text = value.strip().rstrip("/") or "."
    candidate = PurePosixPath(text)
    if (
        candidate.is_absolute()
        or text != candidate.as_posix()
        or any(part in {"", ".."} for part in candidate.parts)
        or "\\" in text
        or "\x00" in text
        or any(token in text for token in ("*", "?", "[", "]", "{", "}"))
    ):
        findings.append(OutcomeFinding("invalid_path", "must be an exact safe repository-relative root", path))
        return None
    return text


def _rfc3339(value: Any, path: str, findings: list[OutcomeFinding]) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        findings.append(OutcomeFinding("invalid_timestamp", "must be an RFC3339 UTC timestamp ending in Z", path))
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        findings.append(OutcomeFinding("invalid_timestamp", "must be an RFC3339 UTC timestamp ending in Z", path))
        return None
    return parsed


def _roots_overlap(left: str, right: str) -> bool:
    left_path, right_path = PurePosixPath(left), PurePosixPath(right)
    return left_path == right_path or left_path in right_path.parents or right_path in left_path.parents


def _require_keys(value: dict[str, Any], required: set[str], path: str, findings: list[OutcomeFinding]) -> None:
    missing = required - set(value)
    unknown = set(value) - required
    if missing:
        findings.append(OutcomeFinding("missing_fields", ", ".join(sorted(missing)), path))
    if unknown:
        findings.append(OutcomeFinding("unknown_fields", ", ".join(sorted(unknown)), path))


def validate_envelope(envelope: Any, *, now: datetime | None = None) -> tuple[OutcomeFinding, ...]:
    """Validate an outcome envelope without authenticating its claimed authority."""

    findings: list[OutcomeFinding] = []
    root = _mapping(envelope, "$", findings)
    if not root:
        return tuple(findings)
    top_keys = {
        "schema_version", "envelope_id", "status", "outcome", "authority", "repositories",
        "action_classes", "tier_3_checkpoints", "ownership", "validation", "repair_policy",
        "evidence", "material_stop_conditions", "expiry_policy", "completion",
    }
    _require_keys(root, top_keys, "$", findings)
    if root.get("schema_version") != SCHEMA_VERSION:
        findings.append(OutcomeFinding("unsupported_schema", f"must equal {SCHEMA_VERSION}", "schema_version"))
    envelope_id = root.get("envelope_id")
    if not isinstance(envelope_id, str) or not IDENTIFIER.fullmatch(envelope_id):
        findings.append(OutcomeFinding("invalid_identifier", "must be a lowercase governed identifier", "envelope_id"))
    if root.get("status") != "Accepted":
        findings.append(OutcomeFinding("inactive_envelope", "must equal Accepted before execution", "status"))

    outcome = _mapping(root.get("outcome"), "outcome", findings)
    _require_keys(outcome, {"plain_language_result", "organizational_or_customer_value", "acceptance_criteria"}, "outcome", findings)
    for field in ("plain_language_result", "organizational_or_customer_value"):
        if not isinstance(outcome.get(field), str) or not outcome[field].strip():
            findings.append(OutcomeFinding("missing_value", "must be a non-empty string", f"outcome.{field}"))
    _strings(outcome.get("acceptance_criteria"), "outcome.acceptance_criteria", findings)

    authority = _mapping(root.get("authority"), "authority", findings)
    _require_keys(authority, {"decision_references", "authority_gained", "authority_not_gained"}, "authority", findings)
    decisions = authority.get("decision_references")
    if not isinstance(decisions, list) or not decisions:
        findings.append(OutcomeFinding("missing_value", "must contain at least one decision reference", "authority.decision_references"))
    else:
        for index, raw in enumerate(decisions):
            ref_path = f"authority.decision_references[{index}]"
            ref = _mapping(raw, ref_path, findings)
            _require_keys(ref, {"artifact", "sha256", "decision_date", "approved_effect"}, ref_path, findings)
            if not isinstance(ref.get("artifact"), str) or not ref["artifact"].strip():
                findings.append(OutcomeFinding("missing_value", "must name the decision artifact", f"{ref_path}.artifact"))
            if not isinstance(ref.get("sha256"), str) or not HEX_64.fullmatch(ref["sha256"]):
                findings.append(OutcomeFinding("invalid_digest", "must be 64 lowercase hex characters", f"{ref_path}.sha256"))
            _rfc3339(ref.get("decision_date"), f"{ref_path}.decision_date", findings)
            if not isinstance(ref.get("approved_effect"), str) or not ref["approved_effect"].strip():
                findings.append(OutcomeFinding("missing_value", "must describe the approved effect", f"{ref_path}.approved_effect"))
    _strings(authority.get("authority_gained"), "authority.authority_gained", findings)
    _strings(authority.get("authority_not_gained"), "authority.authority_not_gained", findings)

    repositories = root.get("repositories")
    owned_roots: list[str] = []
    excluded_roots: list[str] = []
    if not isinstance(repositories, list) or not repositories:
        findings.append(OutcomeFinding("missing_value", "must contain at least one repository", "repositories"))
    else:
        repository_names: list[str] = []
        for index, raw in enumerate(repositories):
            repo_path = f"repositories[{index}]"
            repo = _mapping(raw, repo_path, findings)
            _require_keys(repo, {"name", "required_baseline", "branch", "tracking_branch", "live_remote_equality_required", "owned_roots", "excluded_roots"}, repo_path, findings)
            name = repo.get("name")
            if not isinstance(name, str) or not name.strip():
                findings.append(OutcomeFinding("missing_value", "must name the repository", f"{repo_path}.name"))
            else:
                repository_names.append(name.strip())
            baseline = repo.get("required_baseline")
            if not isinstance(baseline, str) or not HEX_40.fullmatch(baseline):
                findings.append(OutcomeFinding("invalid_baseline", "must be a 40-character lowercase Git object id", f"{repo_path}.required_baseline"))
            for field in ("branch", "tracking_branch"):
                value = repo.get(field)
                if not isinstance(value, str) or not value or value.startswith("-") or ".." in value or any(ch.isspace() for ch in value):
                    findings.append(OutcomeFinding("invalid_git_ref", "must be a safe exact Git reference", f"{repo_path}.{field}"))
            if type(repo.get("live_remote_equality_required")) is not bool:
                findings.append(OutcomeFinding("invalid_type", "must be a boolean", f"{repo_path}.live_remote_equality_required"))
            for field, target in (("owned_roots", owned_roots), ("excluded_roots", excluded_roots)):
                raw_roots = repo.get(field)
                if not isinstance(raw_roots, list) or (field == "owned_roots" and not raw_roots):
                    findings.append(OutcomeFinding("missing_value", "must be a non-empty list" if field == "owned_roots" else "must be a list", f"{repo_path}.{field}"))
                    continue
                parsed = [_safe_root(item, f"{repo_path}.{field}[{i}]", findings) for i, item in enumerate(raw_roots)]
                valid = [item for item in parsed if item is not None]
                if len(valid) != len(set(valid)):
                    findings.append(OutcomeFinding("duplicate_value", "must not contain duplicates", f"{repo_path}.{field}"))
                target.extend(valid)
        if len(repository_names) != len(set(repository_names)):
            findings.append(OutcomeFinding("duplicate_value", "repository names must be unique", "repositories"))
    for owned in owned_roots:
        for excluded in excluded_roots:
            if _roots_overlap(owned, excluded):
                findings.append(OutcomeFinding("overlapping_scope", "owned and excluded roots must not overlap", "repositories"))

    action_classes = set(_strings(root.get("action_classes"), "action_classes", findings))
    unknown_actions = action_classes - ALLOWED_ACTION_CLASSES
    if unknown_actions:
        findings.append(OutcomeFinding("unknown_action_class", ", ".join(sorted(unknown_actions)), "action_classes"))

    checkpoints = root.get("tier_3_checkpoints")
    approved_checkpoint_actions: set[str] = set()
    if not isinstance(checkpoints, list):
        findings.append(OutcomeFinding("invalid_type", "must be a list", "tier_3_checkpoints"))
    else:
        checkpoint_ids: list[str] = []
        for index, raw in enumerate(checkpoints):
            checkpoint_path = f"tier_3_checkpoints[{index}]"
            checkpoint = _mapping(raw, checkpoint_path, findings)
            _require_keys(checkpoint, {"checkpoint_id", "action_class", "decision_sha256", "subject", "expires_at"}, checkpoint_path, findings)
            checkpoint_id = checkpoint.get("checkpoint_id")
            if not isinstance(checkpoint_id, str) or not IDENTIFIER.fullmatch(checkpoint_id):
                findings.append(OutcomeFinding("invalid_identifier", "must be a lowercase governed identifier", f"{checkpoint_path}.checkpoint_id"))
            else:
                checkpoint_ids.append(checkpoint_id)
            action = checkpoint.get("action_class")
            if action not in PROTECTED_ACTION_CLASSES:
                findings.append(OutcomeFinding("invalid_checkpoint", "must name a supported Tier 3 action class", f"{checkpoint_path}.action_class"))
            else:
                approved_checkpoint_actions.add(action)
            if not isinstance(checkpoint.get("decision_sha256"), str) or not HEX_64.fullmatch(checkpoint["decision_sha256"]):
                findings.append(OutcomeFinding("invalid_digest", "must be 64 lowercase hex characters", f"{checkpoint_path}.decision_sha256"))
            if not isinstance(checkpoint.get("subject"), str) or not checkpoint["subject"].strip():
                findings.append(OutcomeFinding("missing_value", "must bind the protected subject", f"{checkpoint_path}.subject"))
            _rfc3339(checkpoint.get("expires_at"), f"{checkpoint_path}.expires_at", findings)
        if len(checkpoint_ids) != len(set(checkpoint_ids)):
            findings.append(OutcomeFinding("duplicate_value", "checkpoint ids must be unique", "tier_3_checkpoints"))
    missing_checkpoints = action_classes & PROTECTED_ACTION_CLASSES - approved_checkpoint_actions
    if missing_checkpoints:
        findings.append(OutcomeFinding("missing_tier_3_checkpoint", ", ".join(sorted(missing_checkpoints)), "tier_3_checkpoints"))

    ownership = _mapping(root.get("ownership"), "ownership", findings)
    _require_keys(ownership, {"main_writer", "main_writer_active_roots", "maximum_concurrent_specialists", "specialists_read_only", "writer_worktrees"}, "ownership", findings)
    if not isinstance(ownership.get("main_writer"), str) or not ownership["main_writer"].strip():
        findings.append(OutcomeFinding("missing_value", "must name one accountable writer", "ownership.main_writer"))
    maximum = ownership.get("maximum_concurrent_specialists")
    if not isinstance(maximum, int) or isinstance(maximum, bool) or not 0 <= maximum <= 3:
        findings.append(OutcomeFinding("invalid_value", "must be an integer from 0 to 3", "ownership.maximum_concurrent_specialists"))
    if ownership.get("specialists_read_only") is not True:
        findings.append(OutcomeFinding("unsafe_ownership", "specialists must remain read-only", "ownership.specialists_read_only"))
    main_roots = [
        _safe_root(item, f"ownership.main_writer_active_roots[{index}]", findings)
        for index, item in enumerate(ownership.get("main_writer_active_roots", []))
    ] if isinstance(ownership.get("main_writer_active_roots"), list) else []
    if not isinstance(ownership.get("main_writer_active_roots"), list):
        findings.append(OutcomeFinding("invalid_type", "must be a list", "ownership.main_writer_active_roots"))
    for main_root in (root for root in main_roots if root is not None):
        if not any(
            main_root == repository_root
            or PurePosixPath(repository_root) in PurePosixPath(main_root).parents
            for repository_root in owned_roots
        ):
            findings.append(OutcomeFinding("main_scope_outside_outcome", "main-writer root must be inside an outcome-owned root", "ownership.main_writer_active_roots"))
    writer_worktrees = ownership.get("writer_worktrees")
    if not isinstance(writer_worktrees, list):
        findings.append(OutcomeFinding("invalid_type", "must be a list", "ownership.writer_worktrees"))
        writer_worktrees = []
    if len(writer_worktrees) > 1:
        findings.append(OutcomeFinding("too_many_writer_worktrees", "at most one independent writer worktree is permitted", "ownership.writer_worktrees"))
    for index, raw in enumerate(writer_worktrees):
        writer_path = f"ownership.writer_worktrees[{index}]"
        writer = _mapping(raw, writer_path, findings)
        _require_keys(writer, {"writer_id", "worktree_id", "branch", "owned_roots", "excluded_roots", "integration_owner"}, writer_path, findings)
        for field in ("writer_id", "worktree_id"):
            value = writer.get(field)
            if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
                findings.append(OutcomeFinding("invalid_identifier", "must be a lowercase governed identifier", f"{writer_path}.{field}"))
        branch = writer.get("branch")
        if not isinstance(branch, str) or not branch or branch.startswith("-") or ".." in branch or any(ch.isspace() for ch in branch):
            findings.append(OutcomeFinding("invalid_git_ref", "must be a safe exact Git reference", f"{writer_path}.branch"))
        if writer.get("integration_owner") != ownership.get("main_writer"):
            findings.append(OutcomeFinding("invalid_integration_owner", "must equal the accountable main writer", f"{writer_path}.integration_owner"))
        lane_roots = [
            _safe_root(item, f"{writer_path}.owned_roots[{root_index}]", findings)
            for root_index, item in enumerate(writer.get("owned_roots", []))
        ] if isinstance(writer.get("owned_roots"), list) else []
        lane_exclusions = [
            _safe_root(item, f"{writer_path}.excluded_roots[{root_index}]", findings)
            for root_index, item in enumerate(writer.get("excluded_roots", []))
        ] if isinstance(writer.get("excluded_roots"), list) else []
        if not isinstance(writer.get("owned_roots"), list):
            findings.append(OutcomeFinding("invalid_type", "must be a list", f"{writer_path}.owned_roots"))
        if not isinstance(writer.get("excluded_roots"), list):
            findings.append(OutcomeFinding("invalid_type", "must be a list", f"{writer_path}.excluded_roots"))
        if not lane_roots:
            findings.append(OutcomeFinding("missing_value", "must contain at least one owned root", f"{writer_path}.owned_roots"))
        for lane_root in (root for root in lane_roots if root is not None):
            if not any(
                lane_root == repository_root
                or PurePosixPath(repository_root) in PurePosixPath(lane_root).parents
                for repository_root in owned_roots
            ):
                findings.append(OutcomeFinding("writer_scope_outside_outcome", "writer root must be inside an outcome-owned root", f"{writer_path}.owned_roots"))
            for main_root in (root for root in main_roots if root is not None):
                if _roots_overlap(lane_root, main_root):
                    findings.append(OutcomeFinding("writer_scope_overlap", "writer and active main-writer roots must not overlap", writer_path))
            for excluded_root in (root for root in lane_exclusions if root is not None):
                if _roots_overlap(lane_root, excluded_root):
                    findings.append(OutcomeFinding("writer_scope_overlap", "writer owned and excluded roots must not overlap", writer_path))

    validation = _mapping(root.get("validation"), "validation", findings)
    _require_keys(validation, {"commands", "acceptance_evidence", "fresh_task_recovery_required"}, "validation", findings)
    _strings(validation.get("commands"), "validation.commands", findings)
    _strings(validation.get("acceptance_evidence"), "validation.acceptance_evidence", findings)
    if type(validation.get("fresh_task_recovery_required")) is not bool:
        findings.append(OutcomeFinding("invalid_type", "must be a boolean", "validation.fresh_task_recovery_required"))

    repair = _mapping(root.get("repair_policy"), "repair_policy", findings)
    _require_keys(repair, {"same_failure_reassessment_after", "blind_retry_prohibited", "scope_delta_audit_required", "child_subjects_replay_protected"}, "repair_policy", findings)
    threshold = repair.get("same_failure_reassessment_after")
    if not isinstance(threshold, int) or isinstance(threshold, bool) or threshold < 1:
        findings.append(OutcomeFinding("invalid_value", "must be a positive integer", "repair_policy.same_failure_reassessment_after"))
    for field in ("blind_retry_prohibited", "scope_delta_audit_required", "child_subjects_replay_protected"):
        if repair.get(field) is not True:
            findings.append(OutcomeFinding("unsafe_repair_policy", "must be true", f"repair_policy.{field}"))

    evidence = _mapping(root.get("evidence"), "evidence", findings)
    _require_keys(evidence, {"output_classes", "report_roots", "sanitization"}, "evidence", findings)
    output_classes = set(_strings(evidence.get("output_classes"), "evidence.output_classes", findings))
    if output_classes - OUTPUT_CLASSES:
        findings.append(OutcomeFinding("unknown_output_class", ", ".join(sorted(output_classes - OUTPUT_CLASSES)), "evidence.output_classes"))
    report_roots = [_safe_root(item, f"evidence.report_roots[{i}]", findings) for i, item in enumerate(evidence.get("report_roots", []) if isinstance(evidence.get("report_roots"), list) else [])]
    if not isinstance(evidence.get("report_roots"), list):
        findings.append(OutcomeFinding("invalid_type", "must be a list", "evidence.report_roots"))
    if "deterministic_tracked_report" in output_classes and not any(report_roots):
        findings.append(OutcomeFinding("missing_report_root", "tracked report output requires an approved report root", "evidence.report_roots"))
    sanitization = set(_strings(evidence.get("sanitization"), "evidence.sanitization", findings))
    if REQUIRED_SANITIZATION - sanitization:
        findings.append(OutcomeFinding("missing_sanitization", ", ".join(sorted(REQUIRED_SANITIZATION - sanitization)), "evidence.sanitization"))

    stops = set(_strings(root.get("material_stop_conditions"), "material_stop_conditions", findings))
    if stops != MATERIAL_STOP_CONDITIONS:
        findings.append(OutcomeFinding("invalid_material_stops", "must contain exactly the governed material stop conditions", "material_stop_conditions"))

    expiry = _mapping(root.get("expiry_policy"), "expiry_policy", findings)
    _require_keys(expiry, {"expires_at", "automatic_revalidation", "hard_window_reasons"}, "expiry_policy", findings)
    expires_at = _rfc3339(expiry.get("expires_at"), "expiry_policy.expires_at", findings)
    if expiry.get("automatic_revalidation") is not True:
        findings.append(OutcomeFinding("unsafe_expiry_policy", "must require automatic revalidation", "expiry_policy.automatic_revalidation"))
    _strings(expiry.get("hard_window_reasons"), "expiry_policy.hard_window_reasons", findings, required=False)
    comparison = now or datetime.now(timezone.utc)
    if comparison.tzinfo is None:
        comparison = comparison.replace(tzinfo=timezone.utc)
    if expires_at is not None and expires_at <= comparison:
        findings.append(OutcomeFinding("revalidation_required", "envelope is expired; revalidate material conditions before issuing a child lease", "expiry_policy.expires_at"))

    completion = _mapping(root.get("completion"), "completion", findings)
    _require_keys(completion, {"condition", "publication_evidence_required", "owner_return"}, "completion", findings)
    if not isinstance(completion.get("condition"), str) or not completion["condition"].strip():
        findings.append(OutcomeFinding("missing_value", "must describe the approved completion condition", "completion.condition"))
    if type(completion.get("publication_evidence_required")) is not bool:
        findings.append(OutcomeFinding("invalid_type", "must be a boolean", "completion.publication_evidence_required"))
    if completion.get("owner_return") != "one_plain_language_outcome":
        findings.append(OutcomeFinding("invalid_owner_return", "must equal one_plain_language_outcome", "completion.owner_return"))
    return tuple(findings)


def assess_continuation(
    *,
    acceptance_complete: bool,
    material_changes: Iterable[str] = (),
    same_failure_count: int = 0,
    correction_changed: bool = True,
) -> ContinuationAssessment:
    """Decide whether bounded engineering continues without an Owner prompt."""

    material = tuple(sorted(set(material_changes)))
    unknown = set(material) - MATERIAL_STOP_CONDITIONS
    if unknown:
        return ContinuationAssessment(OutcomeDisposition.STOP_FOR_OWNER, "Unclassified material change requires Owner review.", material)
    if material:
        return ContinuationAssessment(OutcomeDisposition.STOP_FOR_OWNER, "A governed material boundary changed.", material)
    if acceptance_complete:
        return ContinuationAssessment(OutcomeDisposition.COMPLETE, "The approved acceptance criteria are complete.")
    if same_failure_count >= 2:
        if not correction_changed:
            return ContinuationAssessment(OutcomeDisposition.INTERNAL_REASSESSMENT, "Blind retry is prohibited; perform and record a new root-cause assessment.")
        return ContinuationAssessment(OutcomeDisposition.CONTINUE, "A newly justified bounded correction may continue after internal reassessment.")
    return ContinuationAssessment(OutcomeDisposition.CONTINUE, "Continue inside the accepted outcome envelope.")
