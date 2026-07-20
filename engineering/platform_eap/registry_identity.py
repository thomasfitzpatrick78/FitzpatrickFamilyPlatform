from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass, replace
from datetime import datetime
from enum import Enum
from pathlib import Path, PurePosixPath
from typing import Callable, Mapping, Sequence


SCHEMA_VERSION = "1.1"
CONTRACT_VERSION = "1.0"
MIGRATION_MODEL_VERSION = "registry-container-identity-migration-v1"
EVIDENCE_CATALOG_VERSION = "registry-container-identity-evidence-v1"
ROLLBACK_MODEL_VERSION = "registry-container-identity-rollback-v1"
APPROVAL_MODEL_VERSION = "registry-container-identity-approval-v1"
REGISTRY_MIGRATION_APPROVAL_SCOPE = "registry_record_migration"
REGISTRY_MIGRATION_APPROVAL_AUTHORITY = "Architecture Gatekeeper"

CONTAINER_IDENTITY_FIELDS = {
    "container_identity_contract_version",
    "container_participation",
    "container_host_reference",
    "compose_project",
    "compose_service",
    "governed_runtime_name",
    "health_check_requirement",
    "container_health_policy_reference",
    "expected_image_reference",
    "expected_image_digest",
    "container_identity_evidence",
    "participation_reason",
    "participation_review_reference",
    "participation_review_expires_at",
}
PARTICIPATION_VALUES = {"active", "intentionally_inactive", "excluded", "not_applicable"}
HEALTH_CHECK_VALUES = {"required", "optional", "not_applicable"}
PARTICIPATION_REASON_VALUES = {
    "planned_not_deployed",
    "approved_maintenance_or_shutdown",
    "unsupported_identity_model",
    "identity_unresolved",
    "out_of_scope",
    "logical_or_repository_capability",
    "runtime_engine_not_workload",
    "retired_or_replacement_only",
}
SERVICE_RECORD_TYPES = {"service", "planned_service"}
NOT_APPLICABLE_PROHIBITED_FIELDS = {
    "container_host_reference",
    "compose_project",
    "compose_service",
    "governed_runtime_name",
    "health_check_requirement",
    "container_health_policy_reference",
    "expected_image_reference",
    "expected_image_digest",
    "participation_review_reference",
    "participation_review_expires_at",
}

_COMPOSE_NAME = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,127}$")
_RUNTIME_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
_IMAGE_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/:@-]{0,255}$")
_IMAGE_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_SECRET_LIKE = re.compile(r"(?:password|secret|token|api[_-]?key|docker\.sock|containerd\.sock)\s*[:=]", re.IGNORECASE)


class MigrationClassification(str, Enum):
    CONFIRMED_ACTIVE_CONTAINER_SERVICE = "confirmed_active_container_service"
    CONFIRMED_INTENTIONALLY_INACTIVE_CONTAINER_SERVICE = "confirmed_intentionally_inactive_container_service"
    CONFIRMED_NON_CONTAINER_SERVICE = "confirmed_non_container_service"
    PLANNED_CONTAINER_SERVICE = "planned_container_service"
    UNRESOLVED = "unresolved"
    NOT_APPLICABLE = "not_applicable"


class MigrationAction(str, Enum):
    APPLY = "apply"
    REVIEW_REQUIRED = "review_required"
    NO_CHANGE = "no_change"


class MigrationApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"


class MigrationApprovalDecision(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class RegistryIdentityFinding:
    severity: str
    code: str
    message: str
    path: str | None = None


@dataclass(frozen=True)
class MigrationEvidence:
    reference: str
    assertion: str
    source_sha256: str


@dataclass(frozen=True)
class MigrationCandidate:
    subject_id: str
    record_reference: str
    source_sha256: str
    classification: MigrationClassification
    action: MigrationAction
    proposed_fields: tuple[tuple[str, object], ...]
    evidence: tuple[MigrationEvidence, ...]
    unresolved_fields: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class MigrationPlan:
    model_version: str
    schema_version: str
    plan_id: str
    approval_status: MigrationApprovalStatus
    approval_reference: str | None
    approval_sha256: str | None
    candidates: tuple[MigrationCandidate, ...]


@dataclass(frozen=True)
class MigrationApprovalArtifact:
    model_version: str
    plan_id: str
    schema_version: str
    migration_model_version: str
    approval_status: MigrationApprovalDecision
    approval_scope: str
    approval_timestamp: str
    approval_authority: str
    approval_authority_reference: str
    decision_notes: str | None = None


@dataclass(frozen=True)
class MigrationReport:
    plan_id: str
    approval_status: MigrationApprovalStatus
    candidate_count: int
    apply_count: int
    review_required_count: int
    no_change_count: int
    unresolved_subject_ids: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class MigrationRollbackEntry:
    subject_id: str
    record_reference: str
    original_sha256: str
    migrated_sha256: str
    original_content: str


@dataclass(frozen=True)
class MigrationRollbackMetadata:
    model_version: str
    plan_id: str
    entries: tuple[MigrationRollbackEntry, ...]


@dataclass(frozen=True)
class MigrationResult:
    plan_id: str
    status: str
    dry_run: bool
    evaluated_subject_ids: tuple[str, ...]
    changed_record_references: tuple[str, ...]
    findings: tuple[str, ...]
    rollback_metadata: MigrationRollbackMetadata


class MigrationDataError(ValueError):
    """Raised when migration data is malformed, unsafe, stale, or unauthorized."""


def _finding(severity: str, code: str, message: str, path: str | None = None) -> RegistryIdentityFinding:
    return RegistryIdentityFinding(severity, code, message, path)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _safe_reference(value: object, repository_root: Path, require_exists: bool = True) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts:
        return False
    resolved_root = repository_root.resolve()
    resolved = (repository_root / candidate).resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        return False
    return not require_exists or resolved.is_file()


def _safe_registry_record_reference(value: object, repository_root: Path) -> bool:
    if not _safe_reference(value, repository_root):
        return False
    assert isinstance(value, str)
    parts = PurePosixPath(value).parts
    return len(parts) >= 4 and parts[:2] == ("registry", "records") and parts[-1].endswith(".yaml")


def _safe_approval_reference(value: object, repository_root: Path) -> bool:
    if not _safe_reference(value, repository_root):
        return False
    assert isinstance(value, str)
    parts = PurePosixPath(value).parts
    return len(parts) >= 4 and parts[:2] == ("registry", "migrations") and parts[-1].endswith(".json")


def _safe_governance_reference(value: object, repository_root: Path) -> bool:
    if not _safe_reference(value, repository_root):
        return False
    assert isinstance(value, str)
    parts = PurePosixPath(value).parts
    allowed_prefixes = {
        ("docs", "architecture"),
        ("docs", "engineering-organization"),
        ("docs", "governance"),
        ("docs", "milestones"),
    }
    return len(parts) >= 3 and parts[:2] in allowed_prefixes


def _valid_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def schema_version_from(schema: Mapping[str, object]) -> str:
    value = schema.get("schema_version", "1.0")
    return str(value)


def validate_schema_contract(schema: Mapping[str, object]) -> list[RegistryIdentityFinding]:
    findings: list[RegistryIdentityFinding] = []
    version = schema_version_from(schema)
    if version not in {"1.0", SCHEMA_VERSION}:
        findings.append(_finding("ERROR", "registry.schema.version.unsupported", f"Unsupported Registry schema version: {version}.", "schema_version"))
        return findings
    if version == "1.0":
        return findings
    allowed_fields = schema.get("allowed_fields")
    if not isinstance(allowed_fields, list) or any(not isinstance(item, str) for item in allowed_fields):
        findings.append(_finding("ERROR", "registry.schema.allowed_fields.required", "Registry schema 1.1 must define allowed_fields as a list of strings.", "allowed_fields"))
    elif not CONTAINER_IDENTITY_FIELDS.issubset(set(allowed_fields)):
        missing = sorted(CONTAINER_IDENTITY_FIELDS - set(allowed_fields))
        findings.append(_finding("ERROR", "registry.schema.container_fields.missing", f"Registry schema is missing container identity fields: {', '.join(missing)}.", "allowed_fields"))
    if schema.get("container_identity_contract_versions") != [CONTRACT_VERSION]:
        findings.append(_finding("ERROR", "registry.schema.contract_versions.invalid", "Registry schema must support exactly container identity contract version 1.0.", "container_identity_contract_versions"))
    if set(schema.get("container_participation_values", [])) != PARTICIPATION_VALUES:
        findings.append(_finding("ERROR", "registry.schema.participation_values.invalid", "Registry schema participation values do not match the published contract.", "container_participation_values"))
    if set(schema.get("health_check_requirement_values", [])) != HEALTH_CHECK_VALUES:
        findings.append(_finding("ERROR", "registry.schema.health_check_values.invalid", "Registry schema health-check values do not match the published contract.", "health_check_requirement_values"))
    if set(schema.get("participation_reason_values", [])) != PARTICIPATION_REASON_VALUES:
        findings.append(_finding("ERROR", "registry.schema.participation_reason_values.invalid", "Registry schema participation reasons do not match the published contract.", "participation_reason_values"))
    return findings


def _display_path(path: Path, repository_root: Path) -> str:
    try:
        return str(path.relative_to(repository_root))
    except ValueError:
        return str(path)


def validate_container_identity_contract(
    records: Mapping[str, Mapping[str, object]],
    path_by_id: Mapping[str, Path],
    schema: Mapping[str, object],
    repository_root: Path,
) -> list[RegistryIdentityFinding]:
    findings = validate_schema_contract(schema)
    if schema_version_from(schema) != SCHEMA_VERSION:
        return findings
    allowed_fields_value = schema.get("allowed_fields", [])
    allowed_fields = set(allowed_fields_value) if isinstance(allowed_fields_value, list) else set()
    tuples: dict[tuple[str, str, str], str] = {}
    runtime_names: dict[tuple[str, str], str] = {}

    for subject_id in sorted(records):
        record = records[subject_id]
        path = _display_path(path_by_id.get(subject_id, Path(subject_id)), repository_root)
        unknown = sorted(set(record) - allowed_fields)
        if unknown:
            findings.append(_finding("ERROR", "registry.record.fields.unknown", f"Unknown Registry fields: {', '.join(unknown)}.", path))
        present = CONTAINER_IDENTITY_FIELDS.intersection(record)
        if not present:
            continue
        if record.get("record_type") not in SERVICE_RECORD_TYPES:
            findings.append(_finding("ERROR", "registry.container.record_type.invalid", "Container identity fields are allowed only on service and planned_service records.", path))
        version = record.get("container_identity_contract_version")
        if version != CONTRACT_VERSION:
            findings.append(_finding("ERROR", "registry.container.contract_version.unsupported", "Container identity contract version must be 1.0.", path))
        participation = record.get("container_participation")
        if participation not in PARTICIPATION_VALUES:
            findings.append(_finding("ERROR", "registry.container.participation.invalid", "Container participation is missing or unsupported.", path))
            continue
        for key in sorted(present):
            value = record.get(key)
            if isinstance(value, str) and _SECRET_LIKE.search(value):
                findings.append(_finding("ERROR", "registry.container.value.unsafe", f"Container identity field {key} contains unsafe or secret-like content.", path))

        host = record.get("container_host_reference")
        compose_project = record.get("compose_project")
        compose_service = record.get("compose_service")
        runtime_name = record.get("governed_runtime_name")
        health_requirement = record.get("health_check_requirement")
        policy_reference = record.get("container_health_policy_reference")
        evidence = record.get("container_identity_evidence")

        if host is not None:
            target = records.get(str(host))
            if target is None or target.get("record_type") != "host":
                findings.append(_finding("ERROR", "registry.container.host.invalid", f"Container host reference does not resolve to a host: {host}.", path))
            host_dependencies = record.get("host_dependencies")
            if not isinstance(host_dependencies, list) or host not in host_dependencies:
                findings.append(_finding("ERROR", "registry.container.host.dependency_mismatch", "Container host reference must appear in host_dependencies.", path))
        if compose_project is not None and (not isinstance(compose_project, str) or not _COMPOSE_NAME.fullmatch(compose_project)):
            findings.append(_finding("ERROR", "registry.container.compose_project.invalid", "Compose project must use the governed lowercase format.", path))
        if compose_service is not None and (not isinstance(compose_service, str) or not _COMPOSE_NAME.fullmatch(compose_service)):
            findings.append(_finding("ERROR", "registry.container.compose_service.invalid", "Compose service must use the governed lowercase format.", path))
        if (compose_project is None) != (compose_service is None):
            findings.append(_finding("ERROR", "registry.container.compose.incomplete", "Compose project and service must be declared together.", path))
        if runtime_name is not None and (not isinstance(runtime_name, str) or not _RUNTIME_NAME.fullmatch(runtime_name)):
            findings.append(_finding("ERROR", "registry.container.runtime_name.invalid", "Governed runtime name has an invalid format.", path))
        if health_requirement is not None and health_requirement not in HEALTH_CHECK_VALUES:
            findings.append(_finding("ERROR", "registry.container.health_check.invalid", "Health-check requirement is unsupported.", path))
        if policy_reference is not None and not _safe_reference(policy_reference, repository_root):
            findings.append(_finding("ERROR", "registry.container.policy_reference.invalid", "Container health policy reference must resolve safely inside the repository.", path))
        if evidence is not None:
            if not isinstance(evidence, list) or not evidence or any(not _safe_reference(item, repository_root) for item in evidence):
                findings.append(_finding("ERROR", "registry.container.evidence.invalid", "Container identity evidence must contain safe existing repository references.", path))
        image_reference = record.get("expected_image_reference")
        if image_reference is not None and (not isinstance(image_reference, str) or not _IMAGE_REFERENCE.fullmatch(image_reference)):
            findings.append(_finding("ERROR", "registry.container.image_reference.invalid", "Expected image reference has an invalid format.", path))
        image_digest = record.get("expected_image_digest")
        if image_digest is not None and (not isinstance(image_digest, str) or not _IMAGE_DIGEST.fullmatch(image_digest)):
            findings.append(_finding("ERROR", "registry.container.image_digest.invalid", "Expected image digest must be a lowercase sha256 digest.", path))
        review_reference = record.get("participation_review_reference")
        if review_reference is not None and not _safe_reference(review_reference, repository_root):
            findings.append(_finding("ERROR", "registry.container.review_reference.invalid", "Participation review reference must resolve safely inside the repository.", path))
        review_expiry = record.get("participation_review_expires_at")
        if review_expiry is not None and not _valid_timestamp(review_expiry):
            findings.append(_finding("ERROR", "registry.container.review_expiry.invalid", "Participation review expiration must be a timezone-aware timestamp.", path))
        if review_expiry is not None and review_reference is None:
            findings.append(_finding("ERROR", "registry.container.review_expiry.reference_required", "Participation review expiration requires a governed review reference.", path))
        reason = record.get("participation_reason")
        if reason is not None and reason not in PARTICIPATION_REASON_VALUES:
            findings.append(_finding("ERROR", "registry.container.participation_reason.invalid", "Participation reason is unsupported.", path))

        if participation == "active":
            required = {
                "container_host_reference",
                "compose_project",
                "compose_service",
                "health_check_requirement",
                "container_health_policy_reference",
                "container_identity_evidence",
            }
            missing = sorted(key for key in required if key not in record)
            if missing:
                findings.append(_finding("ERROR", "registry.container.active.required", f"Active container identity is missing required fields: {', '.join(missing)}.", path))
            if record.get("record_type") != "service" or record.get("lifecycle_status") != "active":
                findings.append(_finding("ERROR", "registry.container.active.lifecycle", "Active participation requires an active service record.", path))
        elif participation == "intentionally_inactive":
            required = {"health_check_requirement", "container_identity_evidence", "participation_reason"}
            missing = sorted(key for key in required if key not in record)
            if missing:
                findings.append(_finding("ERROR", "registry.container.inactive.required", f"Intentionally inactive identity is missing required fields: {', '.join(missing)}.", path))
        elif participation == "excluded":
            required = {"container_identity_evidence", "participation_reason", "participation_review_reference"}
            missing = sorted(key for key in required if key not in record)
            if missing:
                findings.append(_finding("ERROR", "registry.container.excluded.required", f"Excluded identity is missing required fields: {', '.join(missing)}.", path))
        elif participation == "not_applicable":
            prohibited = sorted(key for key in NOT_APPLICABLE_PROHIBITED_FIELDS if key in record)
            if prohibited:
                findings.append(_finding("ERROR", "registry.container.not_applicable.contradiction", f"Not-applicable identity contains prohibited fields: {', '.join(prohibited)}.", path))

        if host is not None and compose_project is not None and compose_service is not None and participation in {"active", "intentionally_inactive"}:
            identity_tuple = (str(host), str(compose_project), str(compose_service))
            previous = tuples.get(identity_tuple)
            if previous is not None:
                findings.append(_finding("ERROR", "registry.container.compose.duplicate", f"Compose identity tuple duplicates subject {previous} on the same host.", path))
            else:
                tuples[identity_tuple] = subject_id
        if host is not None and runtime_name is not None:
            runtime_tuple = (str(host), str(runtime_name))
            previous = runtime_names.get(runtime_tuple)
            if previous is not None:
                findings.append(_finding("ERROR", "registry.container.runtime_name.duplicate", f"Governed runtime name duplicates subject {previous} on the same host.", path))
            else:
                runtime_names[runtime_tuple] = subject_id
    return findings


def _expect_keys(payload: Mapping[str, object], required: set[str], optional: set[str], context: str) -> None:
    missing = sorted(required - set(payload))
    unknown = sorted(set(payload) - required - optional)
    if missing:
        raise MigrationDataError(f"{context} is missing required fields: {', '.join(missing)}.")
    if unknown:
        raise MigrationDataError(f"{context} contains unknown fields: {', '.join(unknown)}.")


def _expect_mapping(value: object, context: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise MigrationDataError(f"{context} must be an object.")
    return value


def _expect_string(value: object, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MigrationDataError(f"{context} must be a nonblank string.")
    return value


def _expect_string_tuple(value: object, context: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise MigrationDataError(f"{context} must be an array of nonblank strings.")
    return tuple(value)


def _expected_action(proposed: Mapping[str, object], unresolved: Sequence[str]) -> MigrationAction:
    if unresolved:
        return MigrationAction.REVIEW_REQUIRED
    if proposed:
        return MigrationAction.APPLY
    return MigrationAction.NO_CHANGE


def _validate_classification_proposal(
    classification: MigrationClassification,
    proposed: Mapping[str, object],
    unresolved: Sequence[str],
    context: str,
) -> None:
    participation = proposed.get("container_participation")
    expected_participation = {
        MigrationClassification.CONFIRMED_ACTIVE_CONTAINER_SERVICE: "active",
        MigrationClassification.CONFIRMED_INTENTIONALLY_INACTIVE_CONTAINER_SERVICE: "intentionally_inactive",
        MigrationClassification.CONFIRMED_NON_CONTAINER_SERVICE: "not_applicable",
        MigrationClassification.PLANNED_CONTAINER_SERVICE: "intentionally_inactive",
    }.get(classification)
    if proposed and expected_participation is not None and participation != expected_participation:
        raise MigrationDataError(f"{context} proposal contradicts classification {classification.value}.")
    if classification == MigrationClassification.UNRESOLVED and proposed and participation != "excluded":
        raise MigrationDataError(f"{context} unresolved proposal may only declare a reviewed exclusion.")
    if classification == MigrationClassification.NOT_APPLICABLE and (proposed or unresolved):
        raise MigrationDataError(f"{context} not-applicable record-domain classification must be a resolved no-change candidate.")
    if classification != MigrationClassification.NOT_APPLICABLE and not proposed and not unresolved:
        raise MigrationDataError(f"{context} must contain either a proposal or unresolved findings.")


def _candidate_payload(candidate: MigrationCandidate) -> dict[str, object]:
    return {
        "subject_id": candidate.subject_id,
        "record_reference": candidate.record_reference,
        "source_sha256": candidate.source_sha256,
        "classification": candidate.classification.value,
        "action": candidate.action.value,
        "proposed_fields": {key: value for key, value in candidate.proposed_fields},
        "evidence": [asdict(item) for item in candidate.evidence],
        "unresolved_fields": list(candidate.unresolved_fields),
        "warnings": list(candidate.warnings),
    }


def _plan_content(schema_version: str, candidates: Sequence[MigrationCandidate]) -> dict[str, object]:
    return {
        "model_version": MIGRATION_MODEL_VERSION,
        "schema_version": schema_version,
        "candidates": [_candidate_payload(candidate) for candidate in candidates],
    }


def _plan_id(schema_version: str, candidates: Sequence[MigrationCandidate]) -> str:
    return "sha256:" + _sha256_bytes(_canonical_json(_plan_content(schema_version, candidates)).encode("utf-8"))


def build_migration_plan(
    records: Mapping[str, Mapping[str, object]],
    path_by_id: Mapping[str, Path],
    schema: Mapping[str, object],
    catalog: Mapping[str, object],
    repository_root: Path,
) -> MigrationPlan:
    _expect_keys(catalog, {"model_version", "entries"}, set(), "migration evidence catalog")
    if catalog.get("model_version") != EVIDENCE_CATALOG_VERSION:
        raise MigrationDataError("Migration evidence catalog model version is unsupported.")
    entries = catalog.get("entries")
    if not isinstance(entries, list):
        raise MigrationDataError("Migration evidence catalog entries must be an array.")
    candidates: list[MigrationCandidate] = []
    seen: set[str] = set()
    for index, raw_entry in enumerate(entries):
        entry = _expect_mapping(raw_entry, f"catalog entry {index}")
        _expect_keys(entry, {"subject_id", "classification", "proposed_fields", "evidence", "unresolved_fields", "warnings"}, set(), f"catalog entry {index}")
        subject_id = _expect_string(entry.get("subject_id"), f"catalog entry {index}.subject_id")
        if subject_id in seen:
            raise MigrationDataError(f"Migration evidence catalog contains duplicate subject: {subject_id}.")
        seen.add(subject_id)
        record = records.get(subject_id)
        if record is None or record.get("record_type") not in SERVICE_RECORD_TYPES:
            raise MigrationDataError(f"Migration subject is missing or is not a service: {subject_id}.")
        try:
            classification = MigrationClassification(entry.get("classification"))
        except ValueError as exc:
            raise MigrationDataError(f"Migration classification is unsupported for {subject_id}.") from exc
        proposed = _expect_mapping(entry.get("proposed_fields"), f"catalog entry {index}.proposed_fields")
        unknown_proposals = sorted(set(proposed) - CONTAINER_IDENTITY_FIELDS)
        if unknown_proposals:
            raise MigrationDataError(f"Migration proposal for {subject_id} contains unsupported fields: {', '.join(unknown_proposals)}.")
        evidence_value = entry.get("evidence")
        if not isinstance(evidence_value, list) or not evidence_value:
            raise MigrationDataError(f"Migration candidate {subject_id} requires evidence.")
        evidence: list[MigrationEvidence] = []
        for evidence_index, raw_evidence in enumerate(evidence_value):
            item = _expect_mapping(raw_evidence, f"catalog entry {index}.evidence[{evidence_index}]")
            _expect_keys(item, {"reference", "assertion"}, set(), f"catalog entry {index}.evidence[{evidence_index}]")
            reference = _expect_string(item.get("reference"), "evidence.reference")
            assertion = _expect_string(item.get("assertion"), "evidence.assertion")
            if not _safe_reference(reference, repository_root):
                raise MigrationDataError(f"Migration evidence reference is unsafe or missing: {reference}.")
            evidence.append(MigrationEvidence(reference, assertion, _sha256_bytes((repository_root / reference).read_bytes())))
        unresolved = _expect_string_tuple(entry.get("unresolved_fields"), f"catalog entry {index}.unresolved_fields")
        warnings = _expect_string_tuple(entry.get("warnings"), f"catalog entry {index}.warnings")
        _validate_classification_proposal(classification, proposed, unresolved, f"catalog entry {index}")
        action = _expected_action(proposed, unresolved)
        path = path_by_id.get(subject_id)
        if path is None or not path.is_file():
            raise MigrationDataError(f"Migration record path is missing for {subject_id}.")
        try:
            record_reference = str(path.relative_to(repository_root))
        except ValueError as exc:
            raise MigrationDataError(f"Migration record path is outside the repository for {subject_id}.") from exc
        candidates.append(
            MigrationCandidate(
                subject_id=subject_id,
                record_reference=record_reference,
                source_sha256=_sha256_bytes(path.read_bytes()),
                classification=classification,
                action=action,
                proposed_fields=tuple(sorted(proposed.items())),
                evidence=tuple(evidence),
                unresolved_fields=tuple(sorted(unresolved)),
                warnings=tuple(sorted(warnings)),
            )
        )
    expected_subjects = {subject_id for subject_id, record in records.items() if record.get("record_type") in SERVICE_RECORD_TYPES}
    if seen != expected_subjects:
        missing = sorted(expected_subjects - seen)
        extra = sorted(seen - expected_subjects)
        raise MigrationDataError(f"Migration evidence catalog must cover every service subject; missing={missing}, extra={extra}.")
    for subject_id, record in records.items():
        if record.get("record_type") in SERVICE_RECORD_TYPES:
            continue
        path = path_by_id.get(subject_id)
        if path is None or not path.is_file():
            raise MigrationDataError(f"Migration record path is missing for {subject_id}.")
        try:
            record_reference = str(path.relative_to(repository_root))
        except ValueError as exc:
            raise MigrationDataError(f"Migration record path is outside the repository for {subject_id}.") from exc
        source_sha256 = _sha256_bytes(path.read_bytes())
        candidates.append(
            MigrationCandidate(
                subject_id=subject_id,
                record_reference=record_reference,
                source_sha256=source_sha256,
                classification=MigrationClassification.NOT_APPLICABLE,
                action=MigrationAction.NO_CHANGE,
                proposed_fields=(),
                evidence=(MigrationEvidence(record_reference, "Record type is outside the service-record container identity extension.", source_sha256),),
                unresolved_fields=(),
                warnings=(),
            )
        )
    candidates.sort(key=lambda item: item.subject_id)
    proposed_records = {key: dict(value) for key, value in records.items()}
    for candidate in candidates:
        proposed_records[candidate.subject_id].update(dict(candidate.proposed_fields))
    proposal_findings = validate_container_identity_contract(proposed_records, path_by_id, schema, repository_root)
    errors = [finding for finding in proposal_findings if finding.severity == "ERROR"]
    if errors:
        raise MigrationDataError("Migration catalog produces an invalid Registry contract: " + "; ".join(finding.message for finding in errors))
    candidate_tuple = tuple(candidates)
    return MigrationPlan(
        model_version=MIGRATION_MODEL_VERSION,
        schema_version=schema_version_from(schema),
        plan_id=_plan_id(schema_version_from(schema), candidate_tuple),
        approval_status=MigrationApprovalStatus.PENDING,
        approval_reference=None,
        approval_sha256=None,
        candidates=candidate_tuple,
    )


def migration_approval_to_dict(approval: MigrationApprovalArtifact) -> dict[str, object]:
    payload: dict[str, object] = {
        "model_version": approval.model_version,
        "plan_id": approval.plan_id,
        "schema_version": approval.schema_version,
        "migration_model_version": approval.migration_model_version,
        "approval_status": approval.approval_status.value,
        "approval_scope": approval.approval_scope,
        "approval_timestamp": approval.approval_timestamp,
        "approval_authority": approval.approval_authority,
        "approval_authority_reference": approval.approval_authority_reference,
    }
    if approval.decision_notes is not None:
        payload["decision_notes"] = approval.decision_notes
    return payload


def migration_approval_to_json(approval: MigrationApprovalArtifact) -> str:
    return json.dumps(migration_approval_to_dict(approval), indent=2, sort_keys=True) + "\n"


def migration_approval_from_json(text: str) -> MigrationApprovalArtifact:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise MigrationDataError(f"Migration approval artifact is not valid JSON: {exc}.") from exc
    payload = _expect_mapping(value, "migration approval artifact")
    _expect_keys(
        payload,
        {
            "model_version",
            "plan_id",
            "schema_version",
            "migration_model_version",
            "approval_status",
            "approval_scope",
            "approval_timestamp",
            "approval_authority",
            "approval_authority_reference",
        },
        {"decision_notes"},
        "migration approval artifact",
    )
    if payload.get("model_version") != APPROVAL_MODEL_VERSION:
        raise MigrationDataError("Migration approval artifact model version is unsupported.")
    plan_id = _expect_string(payload.get("plan_id"), "migration approval artifact.plan_id")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", plan_id):
        raise MigrationDataError("Migration approval artifact plan ID must be a sha256 identifier.")
    try:
        approval_status = MigrationApprovalDecision(payload.get("approval_status"))
    except ValueError as exc:
        raise MigrationDataError("Migration approval artifact status is unsupported.") from exc
    decision_notes = payload.get("decision_notes")
    if decision_notes is not None:
        decision_notes = _expect_string(decision_notes, "migration approval artifact.decision_notes")
    return MigrationApprovalArtifact(
        model_version=APPROVAL_MODEL_VERSION,
        plan_id=plan_id,
        schema_version=_expect_string(payload.get("schema_version"), "migration approval artifact.schema_version"),
        migration_model_version=_expect_string(payload.get("migration_model_version"), "migration approval artifact.migration_model_version"),
        approval_status=approval_status,
        approval_scope=_expect_string(payload.get("approval_scope"), "migration approval artifact.approval_scope"),
        approval_timestamp=_expect_string(payload.get("approval_timestamp"), "migration approval artifact.approval_timestamp"),
        approval_authority=_expect_string(payload.get("approval_authority"), "migration approval artifact.approval_authority"),
        approval_authority_reference=_expect_string(
            payload.get("approval_authority_reference"),
            "migration approval artifact.approval_authority_reference",
        ),
        decision_notes=decision_notes,
    )


def _validate_approval_for_plan(
    approval: MigrationApprovalArtifact,
    plan: MigrationPlan,
    repository_root: Path | None = None,
) -> None:
    if approval.plan_id != plan.plan_id:
        raise MigrationDataError("Migration approval artifact does not approve the submitted plan ID.")
    if approval.schema_version != plan.schema_version:
        raise MigrationDataError("Migration approval artifact schema version does not match the submitted plan.")
    if approval.migration_model_version != plan.model_version:
        raise MigrationDataError("Migration approval artifact migration model version does not match the submitted plan.")
    if approval.approval_status != MigrationApprovalDecision.APPROVED:
        raise MigrationDataError("Migration approval artifact does not contain an affirmative approval decision.")
    if approval.approval_scope != REGISTRY_MIGRATION_APPROVAL_SCOPE:
        raise MigrationDataError("Migration approval artifact scope does not permit Registry record migration.")
    if not _valid_timestamp(approval.approval_timestamp):
        raise MigrationDataError("Migration approval artifact timestamp must be timezone-aware ISO 8601.")
    if approval.approval_authority != REGISTRY_MIGRATION_APPROVAL_AUTHORITY:
        raise MigrationDataError("Migration approval artifact authority is not authorized for Registry record migration.")
    if repository_root is not None and not _safe_governance_reference(approval.approval_authority_reference, repository_root):
        raise MigrationDataError("Migration approval authority reference is unsafe or missing from a governed documentation area.")


def bind_migration_approval(plan: MigrationPlan, approval_reference: str, approval_content: bytes) -> MigrationPlan:
    try:
        approval_text = approval_content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationDataError("Migration approval artifact must be UTF-8 JSON.") from exc
    approval = migration_approval_from_json(approval_text)
    _validate_approval_for_plan(approval, plan)
    return replace(
        plan,
        approval_status=MigrationApprovalStatus.APPROVED,
        approval_reference=approval_reference,
        approval_sha256=_sha256_bytes(approval_content),
    )


def migration_plan_to_dict(plan: MigrationPlan) -> dict[str, object]:
    payload = _plan_content(plan.schema_version, plan.candidates)
    payload.update(
        {
            "plan_id": plan.plan_id,
            "approval_status": plan.approval_status.value,
            "approval_reference": plan.approval_reference,
            "approval_sha256": plan.approval_sha256,
        }
    )
    return payload


def migration_plan_to_json(plan: MigrationPlan) -> str:
    return json.dumps(migration_plan_to_dict(plan), indent=2, sort_keys=True) + "\n"


def _candidate_from_payload(value: object, context: str) -> MigrationCandidate:
    payload = _expect_mapping(value, context)
    _expect_keys(payload, {"subject_id", "record_reference", "source_sha256", "classification", "action", "proposed_fields", "evidence", "unresolved_fields", "warnings"}, set(), context)
    try:
        classification = MigrationClassification(payload.get("classification"))
        action = MigrationAction(payload.get("action"))
    except ValueError as exc:
        raise MigrationDataError(f"{context} contains an unsupported classification or action.") from exc
    proposed = _expect_mapping(payload.get("proposed_fields"), f"{context}.proposed_fields")
    if set(proposed) - CONTAINER_IDENTITY_FIELDS:
        raise MigrationDataError(f"{context} contains unsupported proposed fields.")
    evidence_value = payload.get("evidence")
    if not isinstance(evidence_value, list):
        raise MigrationDataError(f"{context}.evidence must be an array.")
    evidence: list[MigrationEvidence] = []
    for index, raw_evidence in enumerate(evidence_value):
        item = _expect_mapping(raw_evidence, f"{context}.evidence[{index}]")
        _expect_keys(item, {"reference", "assertion", "source_sha256"}, set(), f"{context}.evidence[{index}]")
        evidence_sha256 = _expect_string(item.get("source_sha256"), "evidence.source_sha256")
        if not re.fullmatch(r"[0-9a-f]{64}", evidence_sha256):
            raise MigrationDataError(f"{context}.evidence[{index}].source_sha256 must be a lowercase sha256 digest.")
        evidence.append(
            MigrationEvidence(
                _expect_string(item.get("reference"), "evidence.reference"),
                _expect_string(item.get("assertion"), "evidence.assertion"),
                evidence_sha256,
            )
        )
    source_sha256 = _expect_string(payload.get("source_sha256"), f"{context}.source_sha256")
    if not re.fullmatch(r"[0-9a-f]{64}", source_sha256):
        raise MigrationDataError(f"{context}.source_sha256 must be a lowercase sha256 digest.")
    unresolved_fields = tuple(sorted(_expect_string_tuple(payload.get("unresolved_fields"), f"{context}.unresolved_fields")))
    proposed_fields = dict(proposed)
    _validate_classification_proposal(classification, proposed_fields, unresolved_fields, context)
    expected_action = _expected_action(proposed_fields, unresolved_fields)
    if action != expected_action:
        raise MigrationDataError(f"{context} action does not match its proposal and unresolved findings.")
    return MigrationCandidate(
        subject_id=_expect_string(payload.get("subject_id"), f"{context}.subject_id"),
        record_reference=_expect_string(payload.get("record_reference"), f"{context}.record_reference"),
        source_sha256=source_sha256,
        classification=classification,
        action=action,
        proposed_fields=tuple(sorted(proposed_fields.items())),
        evidence=tuple(evidence),
        unresolved_fields=unresolved_fields,
        warnings=tuple(sorted(_expect_string_tuple(payload.get("warnings"), f"{context}.warnings"))),
    )


def migration_plan_from_json(text: str) -> MigrationPlan:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise MigrationDataError(f"Migration plan is not valid JSON: {exc}.") from exc
    payload = _expect_mapping(value, "migration plan")
    _expect_keys(
        payload,
        {"model_version", "schema_version", "plan_id", "approval_status", "approval_reference", "approval_sha256", "candidates"},
        set(),
        "migration plan",
    )
    if payload.get("model_version") != MIGRATION_MODEL_VERSION:
        raise MigrationDataError("Migration plan model version is unsupported.")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise MigrationDataError("Migration plan schema version is unsupported.")
    candidates_value = payload.get("candidates")
    if not isinstance(candidates_value, list):
        raise MigrationDataError("Migration plan candidates must be an array.")
    candidates = tuple(_candidate_from_payload(item, f"migration plan candidate {index}") for index, item in enumerate(candidates_value))
    if tuple(sorted(candidate.subject_id for candidate in candidates)) != tuple(candidate.subject_id for candidate in candidates):
        raise MigrationDataError("Migration plan candidates must use deterministic subject ordering.")
    if len({candidate.subject_id for candidate in candidates}) != len(candidates):
        raise MigrationDataError("Migration plan candidate subject IDs must be unique.")
    expected_plan_id = _plan_id(SCHEMA_VERSION, candidates)
    if payload.get("plan_id") != expected_plan_id:
        raise MigrationDataError("Migration plan ID does not match its canonical content.")
    try:
        approval_status = MigrationApprovalStatus(payload.get("approval_status"))
    except ValueError as exc:
        raise MigrationDataError("Migration plan approval status is unsupported.") from exc
    approval_reference = payload.get("approval_reference")
    if approval_reference is not None and not isinstance(approval_reference, str):
        raise MigrationDataError("Migration plan approval reference must be a string or null.")
    approval_sha256 = payload.get("approval_sha256")
    if approval_sha256 is not None and (not isinstance(approval_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", approval_sha256)):
        raise MigrationDataError("Migration plan approval sha256 must be a lowercase digest or null.")
    if approval_status == MigrationApprovalStatus.PENDING and (approval_reference is not None or approval_sha256 is not None):
        raise MigrationDataError("Pending migration plan cannot contain approval binding metadata.")
    if approval_status == MigrationApprovalStatus.APPROVED and (not approval_reference or not approval_sha256):
        raise MigrationDataError("Approved migration plan requires an approval reference and content hash.")
    return MigrationPlan(
        MIGRATION_MODEL_VERSION,
        SCHEMA_VERSION,
        expected_plan_id,
        approval_status,
        approval_reference,
        approval_sha256,
        candidates,
    )


def build_migration_report(plan: MigrationPlan) -> MigrationReport:
    unresolved = tuple(candidate.subject_id for candidate in plan.candidates if candidate.unresolved_fields)
    warnings = tuple(sorted({warning for candidate in plan.candidates for warning in candidate.warnings}))
    return MigrationReport(
        plan_id=plan.plan_id,
        approval_status=plan.approval_status,
        candidate_count=len(plan.candidates),
        apply_count=sum(candidate.action == MigrationAction.APPLY for candidate in plan.candidates),
        review_required_count=sum(candidate.action == MigrationAction.REVIEW_REQUIRED for candidate in plan.candidates),
        no_change_count=sum(candidate.action == MigrationAction.NO_CHANGE for candidate in plan.candidates),
        unresolved_subject_ids=unresolved,
        warnings=warnings,
    )


def render_migration_review(plan: MigrationPlan) -> str:
    report = build_migration_report(plan)
    lines = [
        "# Registry Container Identity Migration Review",
        "",
        f"Plan ID: `{plan.plan_id}`",
        "",
        f"Approval status: `{plan.approval_status.value}`",
        "",
        f"Candidates: {report.candidate_count}; apply: {report.apply_count}; review required: {report.review_required_count}; no change: {report.no_change_count}.",
        "",
        "| Subject | Classification | Action | Unresolved | Evidence | Warnings |",
        "|---------|----------------|--------|------------|----------|----------|",
    ]
    for candidate in plan.candidates:
        unresolved = ", ".join(candidate.unresolved_fields) if candidate.unresolved_fields else "None"
        evidence = "<br>".join(f"`{item.reference}`" for item in candidate.evidence)
        warnings = "<br>".join(candidate.warnings) if candidate.warnings else "None"
        lines.append(f"| `{candidate.subject_id}` | `{candidate.classification.value}` | `{candidate.action.value}` | {unresolved} | {evidence} | {warnings} |")
    lines.extend(["", "No Registry record is modified by planning or review.", ""])
    return "\n".join(lines)


def _parse_flat_yaml_text(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list: str | None = None
    for line_number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current_list is None:
                raise MigrationDataError(f"Registry record has an orphan list item on line {line_number}.")
            value = stripped[2:].strip()
            items = data.setdefault(current_list, [])
            if not isinstance(items, list):
                raise MigrationDataError(f"Registry record list is invalid on line {line_number}.")
            items.append(value)
            continue
        if ":" not in stripped:
            raise MigrationDataError(f"Registry record syntax is unsupported on line {line_number}.")
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        if key in data:
            raise MigrationDataError(f"Registry record contains duplicate field {key}.")
        value = raw_value.strip()
        current_list = None
        if value == "[]":
            data[key] = []
        elif value == "":
            data[key] = []
            current_list = key
        elif value.lower() == "true":
            data[key] = True
        elif value.lower() == "false":
            data[key] = False
        else:
            data[key] = value
    return data


def _render_field(key: str, value: object) -> list[str]:
    if isinstance(value, bool):
        return [f"{key}: {'true' if value else 'false'}"]
    if isinstance(value, str):
        if not value or "\n" in value or "\r" in value:
            raise MigrationDataError(f"Migration field {key} contains an unsupported string value.")
        return [f"{key}: {value}"]
    if isinstance(value, list):
        if any(not isinstance(item, str) or not item or "\n" in item or "\r" in item for item in value):
            raise MigrationDataError(f"Migration field {key} must contain nonblank single-line strings.")
        return [f"{key}: []"] if not value else [f"{key}:", *(f"  - {item}" for item in value)]
    raise MigrationDataError(f"Migration field {key} has an unsupported value type.")


def _merged_record_text(original: str, proposed_fields: Sequence[tuple[str, object]]) -> str:
    parsed = _parse_flat_yaml_text(original)
    additions: list[str] = []
    for key, value in proposed_fields:
        if key in parsed:
            if parsed[key] != value:
                raise MigrationDataError(f"Registry record already contains conflicting field {key}.")
            continue
        additions.extend(_render_field(key, value))
    if not additions:
        return original
    return original.rstrip("\n") + "\n" + "\n".join(additions) + "\n"


def _atomic_write(path: Path, content: str) -> None:
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def rollback_metadata_to_json(metadata: MigrationRollbackMetadata) -> str:
    return json.dumps(asdict(metadata), indent=2, sort_keys=True) + "\n"


def rollback_metadata_from_json(text: str) -> MigrationRollbackMetadata:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise MigrationDataError(f"Rollback metadata is not valid JSON: {exc}.") from exc
    payload = _expect_mapping(value, "rollback metadata")
    _expect_keys(payload, {"model_version", "plan_id", "entries"}, set(), "rollback metadata")
    if payload.get("model_version") != ROLLBACK_MODEL_VERSION:
        raise MigrationDataError("Rollback metadata model version is unsupported.")
    entries_value = payload.get("entries")
    if not isinstance(entries_value, list):
        raise MigrationDataError("Rollback metadata entries must be an array.")
    entries: list[MigrationRollbackEntry] = []
    for index, raw_entry in enumerate(entries_value):
        entry = _expect_mapping(raw_entry, f"rollback entry {index}")
        _expect_keys(entry, {"subject_id", "record_reference", "original_sha256", "migrated_sha256", "original_content"}, set(), f"rollback entry {index}")
        original_sha256 = _expect_string(entry.get("original_sha256"), "rollback.original_sha256")
        migrated_sha256 = _expect_string(entry.get("migrated_sha256"), "rollback.migrated_sha256")
        if not re.fullmatch(r"[0-9a-f]{64}", original_sha256) or not re.fullmatch(r"[0-9a-f]{64}", migrated_sha256):
            raise MigrationDataError(f"rollback entry {index} contains an invalid sha256 digest.")
        original_content = _expect_string(entry.get("original_content"), "rollback.original_content")
        if _sha256_bytes(original_content.encode("utf-8")) != original_sha256:
            raise MigrationDataError(f"rollback entry {index} original content does not match its sha256 digest.")
        entries.append(MigrationRollbackEntry(
            subject_id=_expect_string(entry.get("subject_id"), "rollback.subject_id"),
            record_reference=_expect_string(entry.get("record_reference"), "rollback.record_reference"),
            original_sha256=original_sha256,
            migrated_sha256=migrated_sha256,
            original_content=original_content,
        ))
    if tuple(sorted(entry.subject_id for entry in entries)) != tuple(entry.subject_id for entry in entries):
        raise MigrationDataError("Rollback metadata entries must use deterministic subject ordering.")
    if len({entry.subject_id for entry in entries}) != len(entries) or len({entry.record_reference for entry in entries}) != len(entries):
        raise MigrationDataError("Rollback metadata entries must have unique subjects and record references.")
    plan_id = _expect_string(payload.get("plan_id"), "rollback.plan_id")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", plan_id):
        raise MigrationDataError("Rollback metadata plan ID must be a sha256 identifier.")
    return MigrationRollbackMetadata(ROLLBACK_MODEL_VERSION, plan_id, tuple(entries))


def _validation_errors(validate: Callable[[], Sequence[object]] | None) -> list[str]:
    if validate is None:
        return []
    return [str(getattr(item, "message", item)) for item in validate() if getattr(item, "severity", None) == "ERROR"]


def execute_migration(
    plan: MigrationPlan,
    repository_root: Path,
    *,
    dry_run: bool,
    confirm: bool = False,
    rollback_output: Path | None = None,
    validate: Callable[[], Sequence[object]] | None = None,
) -> MigrationResult:
    if plan.model_version != MIGRATION_MODEL_VERSION or plan.schema_version != SCHEMA_VERSION:
        raise MigrationDataError("Migration plan version is unsupported.")
    if plan.plan_id != _plan_id(plan.schema_version, plan.candidates):
        raise MigrationDataError("Migration plan canonical ID is invalid.")
    if (
        plan.approval_status != MigrationApprovalStatus.APPROVED
        or not plan.approval_reference
        or not plan.approval_sha256
    ):
        raise MigrationDataError("Migration execution requires a plan bound to an approved migration artifact.")
    if not _safe_approval_reference(plan.approval_reference, repository_root):
        raise MigrationDataError("Migration approval artifact reference is unsafe or missing.")
    approval_content = (repository_root / plan.approval_reference).read_bytes()
    if _sha256_bytes(approval_content) != plan.approval_sha256:
        raise MigrationDataError("Migration approval artifact has drifted from the plan binding.")
    try:
        approval_text = approval_content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationDataError("Migration approval artifact must be UTF-8 JSON.") from exc
    approval = migration_approval_from_json(approval_text)
    _validate_approval_for_plan(approval, plan, repository_root)
    if not dry_run and not confirm:
        raise MigrationDataError("Migration mutation requires explicit confirmation.")
    if not dry_run and rollback_output is None:
        raise MigrationDataError("Migration mutation requires an explicit rollback metadata output path.")

    prepared: list[tuple[Path, str, MigrationRollbackEntry]] = []
    evaluated: list[str] = []
    for candidate in plan.candidates:
        evaluated.append(candidate.subject_id)
        if not candidate.evidence or any(not _safe_reference(item.reference, repository_root) for item in candidate.evidence):
            raise MigrationDataError(f"Migration candidate {candidate.subject_id} lacks safe governed evidence.")
        for item in candidate.evidence:
            if _sha256_bytes((repository_root / item.reference).read_bytes()) != item.source_sha256:
                raise MigrationDataError(f"Migration evidence has drifted for {candidate.subject_id}: {item.reference}.")
        if candidate.action != MigrationAction.APPLY:
            continue
        if not candidate.proposed_fields:
            raise MigrationDataError(f"Migration candidate {candidate.subject_id} has no proposed fields.")
        if candidate.unresolved_fields:
            raise MigrationDataError(f"Migration candidate {candidate.subject_id} has unresolved fields.")
        if not _safe_registry_record_reference(candidate.record_reference, repository_root):
            raise MigrationDataError(f"Migration record reference is unsafe or missing: {candidate.record_reference}.")
        path = repository_root / candidate.record_reference
        original = path.read_text(encoding="utf-8")
        if _parse_flat_yaml_text(original).get("id") != candidate.subject_id:
            raise MigrationDataError(f"Migration record reference does not contain subject {candidate.subject_id}.")
        migrated = _merged_record_text(original, candidate.proposed_fields)
        current_sha = _sha256_bytes(original.encode("utf-8"))
        if migrated == original:
            continue
        if current_sha != candidate.source_sha256:
            raise MigrationDataError(f"Migration plan is stale for {candidate.subject_id}.")
        prepared.append(
            (
                path,
                migrated,
                MigrationRollbackEntry(candidate.subject_id, candidate.record_reference, current_sha, _sha256_bytes(migrated.encode("utf-8")), original),
            )
        )
    metadata = MigrationRollbackMetadata(ROLLBACK_MODEL_VERSION, plan.plan_id, tuple(item[2] for item in prepared))
    if dry_run:
        return MigrationResult(plan.plan_id, "dry_run_complete", True, tuple(evaluated), tuple(item[2].record_reference for item in prepared), (), metadata)
    assert rollback_output is not None
    if rollback_output.exists():
        raise MigrationDataError("Rollback metadata output already exists; refusing overwrite.")
    resolved_root = repository_root.resolve()
    resolved_output = rollback_output.resolve()
    if resolved_output != resolved_root and resolved_root not in resolved_output.parents:
        raise MigrationDataError("Rollback metadata output must remain inside the repository.")

    written: list[MigrationRollbackEntry] = []
    try:
        for path, migrated, entry in prepared:
            _atomic_write(path, migrated)
            written.append(entry)
        errors = _validation_errors(validate)
        if errors:
            raise MigrationDataError("Migrated Registry validation failed: " + "; ".join(errors))
        resolved_output.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write(resolved_output, rollback_metadata_to_json(metadata))
    except Exception:
        for entry in reversed(written):
            _atomic_write(repository_root / entry.record_reference, entry.original_content)
        raise
    status = "applied" if prepared else "no_change"
    return MigrationResult(plan.plan_id, status, False, tuple(evaluated), tuple(entry.record_reference for entry in written), (), metadata)


def rollback_migration(
    metadata: MigrationRollbackMetadata,
    repository_root: Path,
    *,
    confirm: bool,
    validate: Callable[[], Sequence[object]] | None = None,
) -> MigrationResult:
    if metadata.model_version != ROLLBACK_MODEL_VERSION:
        raise MigrationDataError("Rollback metadata version is unsupported.")
    if not confirm:
        raise MigrationDataError("Rollback requires explicit confirmation.")
    prepared: list[tuple[Path, str, MigrationRollbackEntry]] = []
    for entry in metadata.entries:
        if not _safe_registry_record_reference(entry.record_reference, repository_root):
            raise MigrationDataError(f"Rollback record reference is unsafe or missing: {entry.record_reference}.")
        path = repository_root / entry.record_reference
        current = path.read_text(encoding="utf-8")
        if _parse_flat_yaml_text(current).get("id") != entry.subject_id:
            raise MigrationDataError(f"Rollback record reference does not contain subject {entry.subject_id}.")
        if _sha256_bytes(entry.original_content.encode("utf-8")) != entry.original_sha256:
            raise MigrationDataError(f"Rollback original content digest is invalid: {entry.record_reference}.")
        current_sha = _sha256_bytes(current.encode("utf-8"))
        if current_sha == entry.original_sha256:
            continue
        if current_sha != entry.migrated_sha256:
            raise MigrationDataError(f"Rollback target has drifted: {entry.record_reference}.")
        prepared.append((path, current, entry))
    restored: list[tuple[Path, str, MigrationRollbackEntry]] = []
    try:
        for path, current, entry in prepared:
            _atomic_write(path, entry.original_content)
            restored.append((path, current, entry))
        errors = _validation_errors(validate)
        if errors:
            raise MigrationDataError("Rollback validation failed after exact restoration: " + "; ".join(errors))
    except Exception:
        for path, current, _entry in reversed(restored):
            _atomic_write(path, current)
        raise
    return MigrationResult(
        metadata.plan_id,
        "rolled_back" if restored else "no_change",
        False,
        tuple(entry.subject_id for entry in metadata.entries),
        tuple(entry.record_reference for _path, _current, entry in restored),
        (),
        metadata,
    )
