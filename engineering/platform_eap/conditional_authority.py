"""Fail-closed, side-effect-free validation for EO-15.2 conditional bundles."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


TOP_LEVEL_KEYS = {
    "schema_version", "bundle_id", "status", "outcome", "authority",
    "repositories", "tiers", "publication", "ownership", "validation",
    "repair_policy", "evidence", "invalidation_triggers", "expiry",
    "completion_condition",
}
REQUIRED_SECTION_KEYS = {
    "outcome": {"plain_language_result", "organizational_or_customer_value", "acceptance_criteria"},
    "authority": {"decision_references", "authority_gained", "authority_not_gained", "fresh_tier_3_approval", "tier_3_approval_evidence"},
    "tiers": {"tier_0_actions", "tier_1_actions", "tier_2_actions", "tier_3_actions"},
    "publication": {"staging_included", "local_commit_included", "push_included", "draft_pull_request_included", "protected_branch_included", "merge_included", "release_included", "tier_2_recovery"},
    "ownership": {"main_writer", "maximum_concurrent_specialists", "specialists", "worktrees", "branches", "shared_path_leases"},
    "validation": {"commands", "working_directories", "expected_results", "generated_evidence"},
    "repair_policy": {"maximum_cycles_for_same_failure", "repairable_paths", "invariants"},
    "evidence": {"per_phase", "completion", "sanitization"},
}
REPOSITORY_KEYS = {"name", "required_baseline", "branch", "tracking_branch", "live_remote_equality_required", "allowed_paths", "excluded_paths"}
DECISION_REFERENCE_KEYS = {"artifact", "sha256", "decision_date", "approved_effect"}
TIER_3_EVIDENCE_KEYS = {"artifact", "sha256", "decision_date", "expiry", "approved_actions"}
TIER_2_RECOVERY_KEYS = {"action", "subject", "branch", "recovery_method", "evidence", "expiry"}
SPECIALIST_KEYS = {"role", "mode", "lane"}
ALLOWED_SPECIALISTS = {"governed_explorer", "governed_validator", "governed_reviewer"}
PUBLICATION_TIERS = {
    "staging_included": ("tier_1_actions", "stage exact targets"),
    "local_commit_included": ("tier_1_actions", "create local commit"),
    "push_included": ("tier_2_actions", "push named non-protected branch"),
    "draft_pull_request_included": ("tier_2_actions", "create draft pull request"),
    "protected_branch_included": ("tier_3_actions", "publish protected branch"),
    "merge_included": ("tier_3_actions", "merge"),
    "release_included": ("tier_3_actions", "release"),
}
GENERATED_EVIDENCE_CLASSES = {"no repository write", "isolated temporary output", "exact deterministic tracked regeneration"}
REQUIRED_SANITIZATION = {"no personal name", "no absolute checkout path", "no credential", "no customer or protected value", "no prompt text"}
HEX_40 = re.compile(r"[0-9a-f]{40}")
HEX_64 = re.compile(r"[0-9a-f]{64}")
BUNDLE_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,127}")
PLACEHOLDER = re.compile(r"(^|\b)(replace|placeholder|tbd|todo)(\b|_)", re.IGNORECASE)


def _list(value: Any, location: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{location} must be a list")
        return []
    return value


def _nonempty_string(value: Any, location: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or not value.strip() or PLACEHOLDER.search(value):
        errors.append(f"{location} must be a non-placeholder string")
        return False
    return True


def _string_list(value: Any, location: str, errors: list[str], *, required: bool = True) -> list[str]:
    values = _list(value, location, errors)
    if required and not values:
        errors.append(f"{location} must contain at least one item")
    result: list[str] = []
    for index, item in enumerate(values):
        if _nonempty_string(item, f"{location}[{index}]", errors):
            result.append(item.strip())
    if len(result) != len(set(result)):
        errors.append(f"{location} must not contain duplicates")
    return result


def _safe_relative_path(value: Any, location: str, errors: list[str]) -> str | None:
    if not _nonempty_string(value, location, errors):
        return None
    text = value.strip()
    path = PurePosixPath(text)
    if (path.is_absolute() or text != path.as_posix() or any(part in {"", ".", ".."} for part in path.parts)
            or "\\" in text or "\x00" in text or any(token in text for token in ("*", "?", "[", "]", "{" , "}"))):
        errors.append(f"{location} must be an exact safe repository-relative path")
        return None
    return text


def _rfc3339_utc(value: Any, location: str, errors: list[str]) -> bool:
    if not _nonempty_string(value, location, errors):
        return False
    text = value.strip()
    if not text.endswith("Z"):
        errors.append(f"{location} must be an RFC3339 UTC timestamp ending in Z")
        return False
    try:
        datetime.fromisoformat(text[:-1] + "+00:00")
    except ValueError:
        errors.append(f"{location} must be an RFC3339 UTC timestamp ending in Z")
        return False
    return True


def _exact_object(value: Any, keys: set[str], location: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{location} must be an object")
        return {}
    missing = keys - set(value)
    unknown = set(value) - keys
    if missing:
        errors.append(f"{location} missing fields: {', '.join(sorted(missing))}")
    if unknown:
        errors.append(f"{location} unknown fields: {', '.join(sorted(unknown))}")
    return value


def validate_bundle(bundle: Any) -> list[str]:
    """Validate the Tier 0-2 contract; success never authenticates authority."""

    errors: list[str] = []
    if not isinstance(bundle, dict):
        return ["bundle must be an object"]
    missing = TOP_LEVEL_KEYS - set(bundle)
    unknown = set(bundle) - TOP_LEVEL_KEYS
    if missing:
        errors.append(f"missing top-level fields: {', '.join(sorted(missing))}")
    if unknown:
        errors.append(f"unknown top-level fields: {', '.join(sorted(unknown))}")
    if bundle.get("schema_version") != "1.0":
        errors.append("schema_version must equal 1.0")
    bundle_id = bundle.get("bundle_id")
    if not isinstance(bundle_id, str) or not BUNDLE_ID.fullmatch(bundle_id) or PLACEHOLDER.search(bundle_id):
        errors.append("bundle_id must be a non-placeholder lowercase identifier")
    if bundle.get("status") != "Accepted":
        errors.append("status must equal Accepted before execution")

    sections: dict[str, dict[str, Any]] = {}
    for section, required in REQUIRED_SECTION_KEYS.items():
        sections[section] = _exact_object(bundle.get(section), required, section, errors)

    outcome = sections["outcome"]
    _nonempty_string(outcome.get("plain_language_result"), "outcome.plain_language_result", errors)
    _nonempty_string(outcome.get("organizational_or_customer_value"), "outcome.organizational_or_customer_value", errors)
    _string_list(outcome.get("acceptance_criteria"), "outcome.acceptance_criteria", errors)

    authority = sections["authority"]
    decision_references = _list(authority.get("decision_references"), "authority.decision_references", errors)
    if not decision_references:
        errors.append("authority.decision_references must contain at least one exact decision")
    for index, item in enumerate(decision_references):
        ref = _exact_object(item, DECISION_REFERENCE_KEYS, f"authority.decision_references[{index}]", errors)
        for field in ("artifact", "decision_date", "approved_effect"):
            _nonempty_string(ref.get(field), f"authority.decision_references[{index}].{field}", errors)
        if not isinstance(ref.get("sha256"), str) or not HEX_64.fullmatch(ref["sha256"]):
            errors.append(f"authority.decision_references[{index}].sha256 must be 64 lowercase hex characters")
    _string_list(authority.get("authority_gained"), "authority.authority_gained", errors)
    _string_list(authority.get("authority_not_gained"), "authority.authority_not_gained", errors)
    if type(authority.get("fresh_tier_3_approval")) is not bool:
        errors.append("authority.fresh_tier_3_approval must be a boolean")

    repositories = _list(bundle.get("repositories"), "repositories", errors)
    if not repositories:
        errors.append("repositories must contain at least one repository")
    repository_names: list[str] = []
    allowed_all: set[str] = set()
    for index, item in enumerate(repositories):
        location = f"repositories[{index}]"
        repository = _exact_object(item, REPOSITORY_KEYS, location, errors)
        if _nonempty_string(repository.get("name"), f"{location}.name", errors):
            repository_names.append(repository["name"].strip())
        baseline = repository.get("required_baseline")
        if not isinstance(baseline, str) or not HEX_40.fullmatch(baseline):
            errors.append(f"{location}.required_baseline must be 40 lowercase hex characters")
        for field in ("branch", "tracking_branch"):
            if _nonempty_string(repository.get(field), f"{location}.{field}", errors):
                value = repository[field]
                if value.startswith("-") or ".." in value or any(char.isspace() for char in value):
                    errors.append(f"{location}.{field} must be a safe exact Git reference")
        if type(repository.get("live_remote_equality_required")) is not bool:
            errors.append(f"{location}.live_remote_equality_required must be a boolean")
        allowed_raw = _list(repository.get("allowed_paths"), f"{location}.allowed_paths", errors)
        excluded_raw = _list(repository.get("excluded_paths"), f"{location}.excluded_paths", errors)
        if not allowed_raw:
            errors.append(f"{location}.allowed_paths must contain at least one exact path")
        allowed = {path for i, value in enumerate(allowed_raw) if (path := _safe_relative_path(value, f"{location}.allowed_paths[{i}]", errors))}
        excluded = {path for i, value in enumerate(excluded_raw) if (path := _safe_relative_path(value, f"{location}.excluded_paths[{i}]", errors))}
        if len(allowed) != len(allowed_raw):
            errors.append(f"{location}.allowed_paths must contain unique valid paths")
        if len(excluded) != len(excluded_raw):
            errors.append(f"{location}.excluded_paths must contain unique valid paths")
        if allowed & excluded:
            errors.append(f"{location} contains a path in both allowed and excluded lists")
        allowed_all.update(allowed)
    if len(repository_names) != len(set(repository_names)):
        errors.append("repository names must be unique")

    tiers = sections["tiers"]
    actions_by_tier: dict[str, list[str]] = {}
    all_actions: list[str] = []
    for tier in ("tier_0_actions", "tier_1_actions", "tier_2_actions", "tier_3_actions"):
        actions_by_tier[tier] = _string_list(tiers.get(tier), f"tiers.{tier}", errors, required=False)
        all_actions.extend(actions_by_tier[tier])
    if not all_actions:
        errors.append("tiers must contain at least one action")
    if len(all_actions) != len(set(all_actions)):
        errors.append("an action may appear in only one risk tier")

    publication = sections["publication"]
    for field, (tier, action) in PUBLICATION_TIERS.items():
        included = publication.get(field)
        if type(included) is not bool:
            errors.append(f"publication.{field} must be a boolean")
        elif included and action not in actions_by_tier[tier]:
            errors.append(f"publication.{field}=true requires {action!r} in {tier}")
        elif not included and action in actions_by_tier[tier]:
            errors.append(f"{action!r} requires publication.{field}=true")
    recovery_items = _list(publication.get("tier_2_recovery"), "publication.tier_2_recovery", errors)
    for index, item in enumerate(recovery_items):
        recovery = _exact_object(item, TIER_2_RECOVERY_KEYS, f"publication.tier_2_recovery[{index}]", errors)
        for field in ("action", "subject", "branch", "recovery_method", "evidence"):
            _nonempty_string(recovery.get(field), f"publication.tier_2_recovery[{index}].{field}", errors)
        _rfc3339_utc(recovery.get("expiry"), f"publication.tier_2_recovery[{index}].expiry", errors)
        if recovery.get("action") not in actions_by_tier["tier_2_actions"]:
            errors.append(f"publication.tier_2_recovery[{index}].action must name a Tier 2 action")
    if actions_by_tier["tier_2_actions"] and not recovery_items:
        errors.append("Tier 2 actions require exact publication.tier_2_recovery evidence")

    ownership = sections["ownership"]
    _nonempty_string(ownership.get("main_writer"), "ownership.main_writer", errors)
    maximum = ownership.get("maximum_concurrent_specialists")
    if not isinstance(maximum, int) or isinstance(maximum, bool) or not 0 <= maximum <= 3:
        errors.append("ownership.maximum_concurrent_specialists must be an integer from 0 to 3")
    specialists = _list(ownership.get("specialists"), "ownership.specialists", errors)
    if len(specialists) > 3:
        errors.append("no more than three specialists are permitted")
    if isinstance(maximum, int) and not isinstance(maximum, bool) and len(specialists) > maximum:
        errors.append("specialist count exceeds maximum_concurrent_specialists")
    roles: list[str] = []
    for index, item in enumerate(specialists):
        specialist = _exact_object(item, SPECIALIST_KEYS, f"ownership.specialists[{index}]", errors)
        role = specialist.get("role")
        if role not in ALLOWED_SPECIALISTS:
            errors.append(f"ownership.specialists[{index}].role must be a governed specialist name")
        else:
            roles.append(role)
        if specialist.get("mode") != "read-only":
            errors.append(f"ownership.specialists[{index}] must be read-only")
        _nonempty_string(specialist.get("lane"), f"ownership.specialists[{index}].lane", errors)
    if len(roles) != len(set(roles)):
        errors.append("specialist roles must be unique")
    worktrees = _string_list(ownership.get("worktrees"), "ownership.worktrees", errors, required=False)
    branches = _string_list(ownership.get("branches"), "ownership.branches", errors, required=False)
    leases = _string_list(ownership.get("shared_path_leases"), "ownership.shared_path_leases", errors, required=False)
    if actions_by_tier["tier_2_actions"] and (not branches or not leases):
        errors.append("Tier 2 actions require exact branches and shared_path_leases")
    if worktrees and not actions_by_tier["tier_2_actions"]:
        errors.append("worktrees require a Tier 2 action")

    validation = sections["validation"]
    commands = _string_list(validation.get("commands"), "validation.commands", errors)
    directories = _string_list(validation.get("working_directories"), "validation.working_directories", errors)
    results = _string_list(validation.get("expected_results"), "validation.expected_results", errors)
    generated = _string_list(validation.get("generated_evidence"), "validation.generated_evidence", errors)
    if len({len(commands), len(directories), len(results), len(generated)}) != 1:
        errors.append("validation commands, working_directories, expected_results, and generated_evidence must align one-to-one")
    for index, classification in enumerate(generated):
        if classification not in GENERATED_EVIDENCE_CLASSES:
            errors.append(f"validation.generated_evidence[{index}] is not an allowed classification")
    for index, directory in enumerate(directories):
        _safe_relative_path(directory, f"validation.working_directories[{index}]", errors)

    repair = sections["repair_policy"]
    maximum_repairs = repair.get("maximum_cycles_for_same_failure")
    if not isinstance(maximum_repairs, int) or isinstance(maximum_repairs, bool) or not 0 <= maximum_repairs <= 2:
        errors.append("repair_policy.maximum_cycles_for_same_failure must be an integer from 0 to 2")
    repairable_raw = _list(repair.get("repairable_paths"), "repair_policy.repairable_paths", errors)
    repairable = {path for i, value in enumerate(repairable_raw) if (path := _safe_relative_path(value, f"repair_policy.repairable_paths[{i}]", errors))}
    if not repairable.issubset(allowed_all):
        errors.append("repair_policy.repairable_paths must be a subset of repository allowed_paths")
    _string_list(repair.get("invariants"), "repair_policy.invariants", errors)

    tier_3_actions = set(actions_by_tier["tier_3_actions"])
    tier_3_evidence = _list(authority.get("tier_3_approval_evidence"), "authority.tier_3_approval_evidence", errors)
    approved_tier_3_actions: set[str] = set()
    for index, item in enumerate(tier_3_evidence):
        evidence_item = _exact_object(item, TIER_3_EVIDENCE_KEYS, f"authority.tier_3_approval_evidence[{index}]", errors)
        for field in ("artifact", "decision_date"):
            _nonempty_string(evidence_item.get(field), f"authority.tier_3_approval_evidence[{index}].{field}", errors)
        if not isinstance(evidence_item.get("sha256"), str) or not HEX_64.fullmatch(evidence_item["sha256"]):
            errors.append(f"authority.tier_3_approval_evidence[{index}].sha256 must be 64 lowercase hex characters")
        _rfc3339_utc(evidence_item.get("expiry"), f"authority.tier_3_approval_evidence[{index}].expiry", errors)
        approved_tier_3_actions.update(_string_list(evidence_item.get("approved_actions"), f"authority.tier_3_approval_evidence[{index}].approved_actions", errors))
    if tier_3_actions:
        errors.append("Tier 3 is prohibited in the Phase A repository validator and requires separately authenticated initialization")
    elif authority.get("fresh_tier_3_approval") is True or tier_3_evidence:
        errors.append("Tier 3 approval evidence is permitted only when Tier 3 actions are included")

    evidence = sections["evidence"]
    _string_list(evidence.get("per_phase"), "evidence.per_phase", errors)
    _string_list(evidence.get("completion"), "evidence.completion", errors)
    sanitization = set(_string_list(evidence.get("sanitization"), "evidence.sanitization", errors))
    missing_sanitization = REQUIRED_SANITIZATION - sanitization
    if missing_sanitization:
        errors.append(f"evidence.sanitization missing: {', '.join(sorted(missing_sanitization))}")

    invalidation = _string_list(bundle.get("invalidation_triggers"), "invalidation_triggers", errors)
    if len(invalidation) < 8:
        errors.append("invalidation_triggers must define at least eight material triggers")
    _rfc3339_utc(bundle.get("expiry"), "expiry", errors)
    _nonempty_string(bundle.get("completion_condition"), "completion_condition", errors)
    return errors


def load_repository_bundle(path_text: str, repository_root: Path) -> Any:
    candidate = Path(path_text)
    if candidate.is_absolute():
        raise ValueError("bundle path must be repository-relative")
    unresolved = repository_root / candidate
    if unresolved.is_symlink():
        raise ValueError("bundle path must not be a symlink")
    resolved_root = repository_root.resolve()
    resolved = unresolved.resolve(strict=True)
    if resolved_root != resolved and resolved_root not in resolved.parents:
        raise ValueError("bundle path escapes the repository")
    if not resolved.is_file():
        raise ValueError("bundle path must be a regular file")
    return json.loads(resolved.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", help="repository-relative JSON bundle path")
    args = parser.parse_args()
    try:
        errors = validate_bundle(load_repository_bundle(args.bundle, Path.cwd()))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
