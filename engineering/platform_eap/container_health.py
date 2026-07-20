from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Mapping, Sequence

from engineering.platform_eap.execution_capability import (
    contains_secret_like_content,
    is_safe_repository_path,
    is_valid_timestamp,
)
from engineering.platform_eap.registry_identity import (
    CONTRACT_VERSION as REGISTRY_IDENTITY_CONTRACT_VERSION,
    validate_container_identity_contract,
)


ENVELOPE_VERSION = "1.0"
PROFILE_VERSION = "1.0"
RECONCILIATION_VERSION = "1.0"
ASSESSMENT_VERSION = "1.0"
BUNDLE_VERSION = "plat-14.1a-fixture-v1"
ACTIVATION_STATUS = "not_activated"
POLICY_MANIFEST_ID = "container-policy-set"
POLICY_MANIFEST_VERSION = "1.0"


class ContainerHealthDataError(ValueError):
    """Raised when untrusted Container Operational Health data is malformed."""


class UnsupportedContractVersion(ContainerHealthDataError):
    """Raised when a contract or profile version is unsupported."""


class PolicyDataError(ContainerHealthDataError):
    """Raised when a policy set is missing, inactive, or incompatible."""


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PolicyDataError(f"Duplicate JSON field is prohibited: {key}.")
        result[key] = value
    return result


class FindingSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class FreshnessStatus(str, Enum):
    CURRENT = "current"
    AGING = "aging"
    STALE = "stale"
    UNKNOWN = "unknown"


class CompletenessStatus(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    MISSING_REQUIRED_ATTRIBUTES = "missing_required_attributes"
    NOT_ASSESSABLE = "not_assessable"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class ReconciliationOutcome(str, Enum):
    MATCHED = "matched"
    MISSING = "missing"
    UNEXPECTED = "unexpected"
    AMBIGUOUS = "ambiguous"
    CONFLICTING = "conflicting"
    STALE = "stale"
    NOT_APPLICABLE = "not_applicable"


class HealthStatus(str, Enum):
    NOT_EVALUATED = "not_evaluated"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    HEALTHY = "healthy"


class ContainerParticipation(str, Enum):
    ACTIVE = "active"
    INTENTIONALLY_INACTIVE = "intentionally_inactive"
    EXCLUDED = "excluded"
    NOT_APPLICABLE = "not_applicable"


class HealthCheckRequirement(str, Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    NOT_APPLICABLE = "not_applicable"


class CollectionMethod(str, Enum):
    DIRECT = "direct"
    SCRAPED = "scraped"
    EXPORTED = "exported"
    INFERRED = "inferred"
    SYNTHETIC = "synthetic"


class IdentityMatchMethod(str, Enum):
    SUBJECT_AND_REGISTRY_REFERENCE = "subject_and_registry_reference"
    HOST_COMPOSE_PROJECT_SERVICE = "host_compose_project_service"
    HOST_UNIQUE_RUNTIME_NAME = "host_unique_runtime_name"


@dataclass(frozen=True)
class DomainFinding:
    severity: FindingSeverity
    code: str
    message: str
    reference: str | None = None


@dataclass(frozen=True)
class DeclaredContainerSubject:
    subject_id: str
    registry_reference: str
    environment: str
    participation: ContainerParticipation
    host_reference: str | None
    compose_project: str | None
    compose_service: str | None
    governed_runtime_name: str | None
    expected_image_reference: str | None
    expected_image_digest: str | None
    health_check_requirement: HealthCheckRequirement
    policy_reference: str
    fixture_only: bool


@dataclass(frozen=True)
class OperationalEvidence:
    contract_version: str
    profile_type: str
    profile_version: str
    evidence_id: str
    subject_id: str
    subject_type: str
    registry_reference: str
    environment: str
    evidence_type: str
    signal_name: str
    value: str | int | float | bool
    value_type: str
    unit: str | None
    observed_at: str
    collected_at: str
    normalized_at: str
    observation_window_start: str | None
    observation_window_end: str | None
    provider_type: str
    provider_id: str
    provider_version: str
    adapter_version: str
    source_reference: str
    runtime_subject_reference: str | None
    identity_match_method: IdentityMatchMethod
    collection_method: CollectionMethod
    freshness_status: FreshnessStatus
    freshness_policy_id: str
    maximum_age_seconds: int
    evaluated_age_seconds: int
    completeness_status: CompletenessStatus
    required_attributes: tuple[str, ...]
    missing_attributes: tuple[str, ...]
    coverage_reference: str | None
    evidence_confidence: Confidence
    confidence_reason_codes: tuple[str, ...]
    finding_codes: tuple[str, ...]
    container_service_reference: str
    host_reference: str
    runtime_name: str | None
    runtime_container_id: str | None
    runtime_engine: str
    orchestrator: str | None


@dataclass(frozen=True)
class NormalizationResult:
    evidence: tuple[OperationalEvidence, ...]
    findings: tuple[DomainFinding, ...]


@dataclass(frozen=True)
class RejectedEvidence:
    evidence_id: str
    reason_code: str


@dataclass(frozen=True)
class ReconciliationRecord:
    reconciliation_id: str
    contract_version: str
    policy_version: str
    policy_manifest_id: str
    policy_manifest_version: str
    subject_id: str
    registry_reference: str
    evidence_ids: tuple[str, ...]
    result: ReconciliationOutcome
    match_method: IdentityMatchMethod | None
    reason_codes: tuple[str, ...]
    reconciled_at: str
    unresolved_conflicts: tuple[str, ...]
    selected_evidence_ids: tuple[str, ...]
    rejected_evidence: tuple[RejectedEvidence, ...]


@dataclass(frozen=True)
class AssessmentEvidenceSummary:
    evidence_id: str
    signal_name: str
    role: str
    freshness_status: FreshnessStatus
    evidence_confidence: Confidence
    observed_at: str
    expires_at: str
    finding_codes: tuple[str, ...]


@dataclass(frozen=True)
class OperationalHealthAssessment:
    assessment_id: str
    contract_version: str
    subject_id: str
    registry_reference: str
    evidence_profile_type: str
    evidence_profile_version: str
    policy_manifest_id: str
    policy_manifest_version: str
    policy_versions: tuple[str, ...]
    health_policy_version: str
    assessment_confidence_policy_version: str
    reconciliation_id: str
    reconciliation_result: ReconciliationOutcome
    evidence_ids: tuple[str, ...]
    evidence_summary: tuple[AssessmentEvidenceSummary, ...]
    health_status: HealthStatus
    assessment_confidence: Confidence
    reason_codes: tuple[str, ...]
    critical_findings: tuple[str, ...]
    noncritical_findings: tuple[str, ...]
    evaluated_at: str
    valid_until: str | None
    fixture_only: bool
    activation_status: str


@dataclass(frozen=True)
class EvaluationBundle:
    bundle_version: str
    fixture_only: bool
    activation_status: str
    evaluated_at: str
    registry_records_root: str
    declared_subject: DeclaredContainerSubject
    evidence: tuple[OperationalEvidence, ...]


@dataclass(frozen=True)
class EvaluationResult:
    evidence: tuple[OperationalEvidence, ...]
    reconciliation: ReconciliationRecord
    assessment: OperationalHealthAssessment
    rendering_profile: str


@dataclass(frozen=True)
class PolicyArtifact:
    policy_id: str
    policy_version: str
    status: str
    compatible_contract_versions: tuple[str, ...]
    compatible_profile_versions: tuple[str, ...]
    purpose: str
    approval_authority: tuple[str, ...]
    effective_at: str
    supersedes: str | None
    rules_json: str
    source_reference: str

    def rules(self) -> dict[str, object]:
        value = json.loads(self.rules_json, object_pairs_hook=_strict_object)
        if not isinstance(value, dict):
            raise PolicyDataError(f"Policy rules are malformed: {self.policy_id}.")
        return value


@dataclass(frozen=True)
class PolicySet:
    manifest_id: str
    manifest_version: str
    status: str
    compatible_contract_versions: tuple[str, ...]
    compatible_profile_versions: tuple[str, ...]
    purpose: str
    approval_authority: tuple[str, ...]
    effective_at: str
    supersedes: str | None
    artifacts: tuple[PolicyArtifact, ...]
    source_reference: str

    def artifact(self, policy_id: str) -> PolicyArtifact:
        matches = [artifact for artifact in self.artifacts if artifact.policy_id == policy_id]
        if len(matches) != 1:
            raise PolicyDataError(f"Policy set must contain exactly one {policy_id} policy.")
        return matches[0]

    def versions(self) -> tuple[str, ...]:
        return tuple(sorted(f"{item.policy_id}:{item.policy_version}" for item in self.artifacts))


POLICY_IDS = (
    "container-assessment-confidence",
    "container-health",
    "container-healthcheck-freshness",
    "container-lifecycle-freshness",
    "container-reconciliation",
    "container-resource-pressure",
    "container-restart-window",
    "container-telemetry-availability",
)
POLICY_LOAD_ORDER = (
    "container-reconciliation",
    "container-lifecycle-freshness",
    "container-healthcheck-freshness",
    "container-restart-window",
    "container-resource-pressure",
    "container-telemetry-availability",
    "container-health",
    "container-assessment-confidence",
)

SIGNAL_CONTRACTS: dict[str, tuple[str, str | None, frozenset[object] | None, bool]] = {
    "container.lifecycle.observed_state": ("state", None, frozenset({"created", "running", "stopped", "restarting", "exited", "missing"}), False),
    "container.healthcheck.state": ("state", None, frozenset({"passing", "failing", "starting", "unavailable", "not_configured"}), False),
    "container.restart.count": ("integer", "count", None, False),
    "container.restart.occurred": ("boolean", None, frozenset({True, False}), True),
    "container.cpu.utilization": ("decimal", "ratio", None, True),
    "container.memory.utilization": ("decimal", "ratio", None, True),
    "container.memory.limit": ("integer", "bytes", None, False),
    "container.memory.pressure": ("state", None, frozenset({"normal", "elevated", "critical", "unknown"}), True),
    "container.telemetry.provider_availability": ("state", None, frozenset({"available", "unavailable", "degraded", "unknown"}), False),
    "container.telemetry.expected_signal_availability": ("state", None, frozenset({"available", "missing", "partial", "unsupported", "unknown"}), False),
    "container.telemetry.identity_resolution": ("state", None, frozenset({"exact", "weak", "ambiguous", "unresolved"}), False),
    "container.telemetry.collection_coverage": ("state", None, frozenset({"complete", "partial", "none", "not_assessable"}), False),
    "container.telemetry.provider_limitation": ("state", None, frozenset({"none_known", "applies", "unknown"}), False),
}

HEALTH_REASON_CODES = frozenset({
    "NO_EVALUATION", "SUBJECT_NOT_ACTIVE", "LIFECYCLE_EVIDENCE_MISSING", "IDENTITY_UNRESOLVED",
    "LIFECYCLE_CONFLICT", "MANDATORY_EVIDENCE_UNUSABLE", "TELEMETRY_UNAVAILABLE",
    "PROVIDER_LIMITATION_APPLIES", "DECLARED_SUBJECT_ABSENT", "UNEXPECTED_EXIT", "HEALTHCHECK_FAILED",
    "REQUIRED_HEALTHCHECK_NOT_CONFIGURED", "HEALTHCHECK_NOT_REQUIRED", "ADVISORY_TELEMETRY_PARTIAL",
    "MANDATORY_TELEMETRY_PARTIAL", "RESOURCE_PRESSURE_ELEVATED", "MEMORY_PRESSURE_CRITICAL",
    "RESOURCE_EVIDENCE_STALE", "ASSESSMENT_EXPIRED", "ALL_MANDATORY_CRITERIA_PASSED",
})
RESERVED_HEALTH_REASON_CODES = frozenset({"RESTART_THRESHOLD_EXCEEDED"})
RECONCILIATION_REASON_CODES = frozenset({
    "EXACT_IDENTITY_MATCH", "UNEXPECTED_SUBJECT", "IDENTITY_UNRESOLVED", "LIFECYCLE_CONFLICT",
    "LIFECYCLE_EVIDENCE_STALE", "LIFECYCLE_EVIDENCE_MISSING", "SUBJECT_NOT_ACTIVE",
})
REJECTION_REASON_CODES = frozenset({
    "UNEXPECTED_SUBJECT", "IDENTITY_UNRESOLVED", "LIFECYCLE_CONFLICT", "LIFECYCLE_EVIDENCE_STALE",
    "NOT_QUALIFYING_CURRENT_LIFECYCLE", "NOT_QUALIFYING_CURRENT_EVIDENCE",
})

POLICY_RULE_FIELDS = {
    "container-reconciliation": {"allowed_outcomes", "conclusive_absence_requires", "fuzzy_matching_allowed", "match_hierarchy", "retain_considered_evidence", "silent_conflict_selection"},
    "container-lifecycle-freshness": {"aging_after_seconds", "future_timestamp_behavior", "healthy_requires", "maximum_age_seconds", "timestamp_required"},
    "container-healthcheck-freshness": {"aging_after_seconds", "future_timestamp_behavior", "healthy_requires", "maximum_age_seconds", "registry_requirement_values", "timestamp_required"},
    "container-restart-window": {"accepted_signals", "health_thresholds", "mode", "occurred_requires_bounded_window", "reserved_reason_code"},
    "container-resource-pressure": {"critical_memory_pressure_result", "minimum_qualifying_confidence", "mode", "numeric_health_thresholds", "unhealthy_rules"},
    "container-telemetry-availability": {"identity_requirement", "mandatory_coverage", "mandatory_signals", "material_provider_limitation_disqualifies_evidence", "provider_loss_proves_unhealthy"},
    "container-health": {"evaluation_order", "healthy_criteria", "healthy_default", "reason_codes"},
    "container-assessment-confidence": {"allowed_values", "arithmetic_scoring", "assessment_cannot_exceed_lowest_mandatory_evidence", "healthy_minimum", "unresolved_critical_conflict_result"},
}


def _parse_time(value: str) -> datetime:
    if not is_valid_timestamp(value):
        raise ContainerHealthDataError(f"Timestamp must be timezone-aware ISO 8601: {value!r}.")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _stable_id(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(encoded).hexdigest()[:20]}"


def _has_errors(findings: Sequence[DomainFinding]) -> bool:
    return any(finding.severity == FindingSeverity.ERROR for finding in findings)


def validate_declared_subject(subject: DeclaredContainerSubject) -> tuple[DomainFinding, ...]:
    findings: list[DomainFinding] = []
    for field_name, value in (
        ("subject_id", subject.subject_id), ("registry_reference", subject.registry_reference),
        ("environment", subject.environment),
        ("policy_reference", subject.policy_reference),
    ):
        if not isinstance(value, str) or not value.strip():
            findings.append(DomainFinding(FindingSeverity.ERROR, f"subject.{field_name}.required", f"Declared subject {field_name} is required."))
    for reference in (subject.registry_reference, subject.policy_reference):
        if not is_safe_repository_path(reference):
            findings.append(DomainFinding(FindingSeverity.ERROR, "subject.reference.unsafe", "Declared subject references must be repository-relative and traversal-free.", reference))
    if not subject.fixture_only:
        findings.append(DomainFinding(FindingSeverity.ERROR, "subject.fixture_scope.required", "The first repository slice accepts fixture-only declared subjects."))
    if subject.environment != "test":
        findings.append(DomainFinding(FindingSeverity.ERROR, "subject.environment.fixture_required", "Repository-slice subjects must use the synthetic test environment."))
    if not subject.registry_reference.startswith("engineering/tests/fixtures/container_health/registry/") or not subject.registry_reference.endswith(".yaml"):
        findings.append(DomainFinding(FindingSeverity.ERROR, "subject.registry_reference.fixture_required", "Repository-slice subjects must reference synthetic Registry fixtures."))
    if subject.host_reference is not None and any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-" for character in subject.host_reference):
        findings.append(DomainFinding(FindingSeverity.ERROR, "subject.host_reference.invalid", "Declared subject host reference must be a governed Registry identifier."))
    if subject.participation == ContainerParticipation.ACTIVE:
        if not subject.host_reference or not subject.compose_project or not subject.compose_service:
            findings.append(DomainFinding(FindingSeverity.ERROR, "subject.compose_identity.required", "Active fixture subjects require exact Compose project and service identity."))
    return tuple(findings)


def declared_subject_from_registry_contract(
    records: Mapping[str, Mapping[str, object]],
    path_by_id: Mapping[str, Path],
    schema: Mapping[str, object],
    repository_root: Path,
    subject_id: str,
    registry_reference: str,
    environment: str,
) -> DeclaredContainerSubject:
    findings = validate_container_identity_contract(records, path_by_id, schema, repository_root)
    errors = [finding for finding in findings if finding.severity == "ERROR"]
    if errors:
        summary = "; ".join(f"{finding.code}: {finding.message}" for finding in errors)
        raise ContainerHealthDataError(f"Registry fixture identity contract is invalid: {summary}")
    record = records.get(subject_id)
    if record is None:
        raise ContainerHealthDataError(f"Registry fixture subject does not exist: {subject_id}.")
    expected_path = path_by_id.get(subject_id)
    if expected_path is None:
        raise ContainerHealthDataError(f"Registry fixture subject path is unavailable: {subject_id}.")
    try:
        actual_reference = str(expected_path.resolve().relative_to(repository_root.resolve()))
    except ValueError as exc:
        raise ContainerHealthDataError("Registry fixture subject path escapes the repository.") from exc
    if registry_reference != actual_reference:
        raise ContainerHealthDataError("Registry fixture reference does not match the validated subject record.")
    if record.get("container_identity_contract_version") != REGISTRY_IDENTITY_CONTRACT_VERSION:
        raise ContainerHealthDataError("Registry fixture uses an unsupported container identity contract.")
    try:
        subject = DeclaredContainerSubject(
            subject_id,
            registry_reference,
            environment,
            ContainerParticipation(str(record["container_participation"])),
            str(record["container_host_reference"]) if record.get("container_host_reference") is not None else None,
            str(record["compose_project"]) if record.get("compose_project") is not None else None,
            str(record["compose_service"]) if record.get("compose_service") is not None else None,
            str(record["governed_runtime_name"]) if record.get("governed_runtime_name") is not None else None,
            str(record["expected_image_reference"]) if record.get("expected_image_reference") is not None else None,
            str(record["expected_image_digest"]) if record.get("expected_image_digest") is not None else None,
            HealthCheckRequirement(str(record["health_check_requirement"])) if record.get("health_check_requirement") is not None else HealthCheckRequirement.NOT_APPLICABLE,
            str(record["container_health_policy_reference"]) if record.get("container_health_policy_reference") is not None else "platform/operations/container-health/policies/container-policy-set-v1.0.json",
            True,
        )
    except (KeyError, ValueError) as exc:
        raise ContainerHealthDataError("Registry fixture cannot be projected into a declared container subject.") from exc
    subject_findings = validate_declared_subject(subject)
    if _has_errors(subject_findings):
        raise ContainerHealthDataError("Validated Registry fixture produced an invalid declared subject projection.")
    return subject


def validate_evidence(evidence: OperationalEvidence) -> tuple[DomainFinding, ...]:
    findings: list[DomainFinding] = []
    for field_name, value in (
        ("evidence_id", evidence.evidence_id), ("subject_id", evidence.subject_id),
        ("registry_reference", evidence.registry_reference), ("environment", evidence.environment),
        ("provider_type", evidence.provider_type), ("provider_id", evidence.provider_id),
        ("provider_version", evidence.provider_version), ("adapter_version", evidence.adapter_version),
        ("source_reference", evidence.source_reference), ("runtime_engine", evidence.runtime_engine),
    ):
        if not isinstance(value, str) or not value.strip():
            findings.append(DomainFinding(FindingSeverity.ERROR, f"evidence.{field_name}.required", f"Evidence {field_name} is required."))
    if evidence.contract_version != ENVELOPE_VERSION:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.contract_version.unsupported", "Unsupported Operational Evidence Envelope version."))
    if evidence.profile_type != "container" or evidence.profile_version != PROFILE_VERSION:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.profile.unsupported", "Unsupported evidence profile or profile version."))
    if evidence.subject_type != "container_service":
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.subject_type.unsupported", "Container evidence requires container_service subject type."))
    contract = SIGNAL_CONTRACTS.get(evidence.signal_name)
    if contract is None:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.signal.unsupported", "Signal is not part of Container Evidence Profile v1.0."))
    else:
        value_type, unit, allowed_values, window_required = contract
        if evidence.evidence_type != _signal_evidence_type(evidence.signal_name):
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.evidence_type.invalid", "Evidence type does not match the canonical signal classification."))
        if evidence.value_type != value_type:
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.value_type.invalid", "Signal value type does not match the profile."))
        if evidence.unit != unit:
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.unit.invalid", "Signal unit does not match the canonical profile unit."))
        if allowed_values is not None and evidence.value not in allowed_values:
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.value.invalid", "Signal value is outside the bounded profile values."))
        if value_type == "integer" and (not isinstance(evidence.value, int) or isinstance(evidence.value, bool) or evidence.value < 0):
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.integer.invalid", "Integer evidence must be a nonnegative integer."))
        if value_type == "decimal" and (not isinstance(evidence.value, (int, float)) or isinstance(evidence.value, bool) or not math.isfinite(float(evidence.value)) or float(evidence.value) < 0):
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.decimal.invalid", "Decimal evidence must be finite and nonnegative."))
        if window_required and (evidence.observation_window_start is None or evidence.observation_window_end is None):
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.window.required", "This signal requires an observation window."))
    for field_name, timestamp in (
        ("observed_at", evidence.observed_at), ("collected_at", evidence.collected_at), ("normalized_at", evidence.normalized_at),
    ):
        if not is_valid_timestamp(timestamp):
            findings.append(DomainFinding(FindingSeverity.ERROR, f"evidence.{field_name}.invalid", f"{field_name} must be timezone-aware."))
    if evidence.observation_window_start is not None and evidence.observation_window_end is not None:
        try:
            if _parse_time(evidence.observation_window_end) < _parse_time(evidence.observation_window_start):
                findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.window.invalid", "Observation window end precedes its start."))
        except ContainerHealthDataError:
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.window.timestamp.invalid", "Observation window timestamps must be timezone-aware."))
    for reference in (evidence.registry_reference, evidence.source_reference, evidence.container_service_reference, evidence.host_reference):
        if not is_safe_repository_path(reference):
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.reference.unsafe", "Evidence references must be repository-relative and traversal-free.", reference))
    if contains_secret_like_content(json.dumps(evidence_to_primitive(evidence), sort_keys=True)):
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.secret_like_content", "Evidence contains secret-like content."))
    if evidence.missing_attributes and evidence.completeness_status == CompletenessStatus.COMPLETE:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.completeness.contradictory", "Complete evidence cannot list missing attributes."))
    if evidence.completeness_status in {CompletenessStatus.PARTIAL, CompletenessStatus.MISSING_REQUIRED_ATTRIBUTES} and not evidence.missing_attributes:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.completeness.contradictory", "Incomplete evidence must identify missing attributes."))
    if evidence.required_attributes != tuple(sorted(set(evidence.required_attributes))) or evidence.missing_attributes != tuple(sorted(set(evidence.missing_attributes))):
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.attributes.order", "Evidence attribute lists must be unique and sorted."))
    if evidence.confidence_reason_codes != tuple(sorted(set(evidence.confidence_reason_codes))) or not evidence.confidence_reason_codes:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.confidence_reasons.invalid", "Evidence confidence reasons must be nonempty, unique, and sorted."))
    if evidence.finding_codes != tuple(sorted(set(evidence.finding_codes))):
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.findings.order", "Evidence finding codes must be unique and sorted."))
    if evidence.freshness_status == FreshnessStatus.STALE and evidence.evidence_confidence != Confidence.NONE:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.confidence.stale", "Stale evidence must have confidence none for current health."))
    if "ambiguous_identity" in evidence.finding_codes and evidence.evidence_confidence != Confidence.NONE:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.confidence.ambiguous", "Ambiguous identity is unusable for authoritative health."))
    if evidence.evaluated_age_seconds < 0 or evidence.maximum_age_seconds < 0:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.age.invalid", "Evidence ages must be nonnegative."))
    try:
        if _parse_time(evidence.collected_at) < _parse_time(evidence.observed_at) or _parse_time(evidence.normalized_at) < _parse_time(evidence.collected_at):
            findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.time_order.invalid", "Evidence observation, collection, and normalization timestamps are out of order."))
    except ContainerHealthDataError:
        pass
    return tuple(findings)


def validate_evidence_for_evaluation(
    evidence: OperationalEvidence,
    evaluated_at: str,
    policy_set: PolicySet,
) -> tuple[DomainFinding, ...]:
    findings = list(validate_evidence(evidence))
    if _has_errors(findings):
        return tuple(findings)
    policy_id = "container-healthcheck-freshness" if evidence.signal_name.startswith("container.healthcheck") else "container-lifecycle-freshness"
    rules = policy_set.artifact(policy_id).rules()
    expected_policy = f"{policy_id}:{policy_set.artifact(policy_id).policy_version}"
    try:
        expected_freshness, expected_age = _freshness(
            evidence.observed_at,
            evaluated_at,
            int(rules["aging_after_seconds"]),
            int(rules["maximum_age_seconds"]),
        )
    except ContainerHealthDataError:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.freshness.invalid", "Evidence freshness cannot be derived under the active policy."))
        return tuple(findings)
    expected_complete = evidence.completeness_status == CompletenessStatus.COMPLETE and not evidence.missing_attributes
    limitation = "known_provider_limitation" in evidence.finding_codes
    runtime_fallback = evidence.identity_match_method == IdentityMatchMethod.HOST_UNIQUE_RUNTIME_NAME
    expected_confidence, _ = _confidence(
        evidence.collection_method,
        expected_freshness,
        expected_complete,
        limitation,
        runtime_fallback,
    )
    if "ambiguous_identity" in evidence.finding_codes:
        expected_confidence = Confidence.NONE
    if (
        evidence.freshness_policy_id != expected_policy
        or evidence.maximum_age_seconds != rules["maximum_age_seconds"]
        or evidence.evaluated_age_seconds != expected_age
        or evidence.freshness_status != expected_freshness
    ):
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.freshness.contradictory", "Evidence freshness fields contradict the active policy and evaluation time."))
    if evidence.evidence_confidence != expected_confidence:
        findings.append(DomainFinding(FindingSeverity.ERROR, "evidence.confidence.contradictory", "Evidence confidence contradicts the governed categorical decision table."))
    return tuple(findings)


def evidence_to_primitive(evidence: OperationalEvidence) -> dict[str, object]:
    return {
        field: (value.value if isinstance(value, Enum) else list(value) if isinstance(value, tuple) else value)
        for field, value in evidence.__dict__.items()
    }


def _freshness(observed_at: str, evaluated_at: str, aging_after: int, maximum_age: int) -> tuple[FreshnessStatus, int]:
    observed = _parse_time(observed_at)
    evaluated = _parse_time(evaluated_at)
    if observed > evaluated:
        raise ContainerHealthDataError("Future-dated fixture observations are invalid under policy v1.0.")
    age = int((evaluated - observed).total_seconds())
    if age <= aging_after:
        return FreshnessStatus.CURRENT, age
    if age <= maximum_age:
        return FreshnessStatus.AGING, age
    return FreshnessStatus.STALE, age


def _confidence(
    method: CollectionMethod,
    freshness: FreshnessStatus,
    complete: bool,
    limitation: bool,
    identity_fallback: bool = False,
) -> tuple[Confidence, tuple[str, ...]]:
    if freshness == FreshnessStatus.STALE or not complete:
        return Confidence.NONE, ("CURRENT_USE_UNQUALIFIED",)
    if limitation:
        return Confidence.LOW, ("KNOWN_PROVIDER_LIMITATION",)
    if freshness == FreshnessStatus.AGING or method == CollectionMethod.INFERRED:
        return Confidence.LOW, ("AGING_OR_INFERRED",)
    if identity_fallback:
        return Confidence.MEDIUM, ("UNIQUE_RUNTIME_NAME_FALLBACK",)
    if method == CollectionMethod.DIRECT:
        return Confidence.HIGH, ("EXACT_CURRENT_COMPLETE_DIRECT",)
    return Confidence.MEDIUM, ("EXACT_CURRENT_COMPLETE_INDIRECT",)


def _signal_evidence_type(signal_name: str) -> str:
    if signal_name.startswith("container.lifecycle"):
        return "lifecycle"
    if signal_name.startswith("container.healthcheck"):
        return "runtime_healthcheck"
    if signal_name.startswith("container.restart"):
        return "restart"
    if signal_name.startswith("container.cpu") or signal_name.startswith("container.memory"):
        return "resource_pressure"
    return "telemetry_availability"


def _fixture_fields(raw: Mapping[str, object]) -> tuple[dict[str, object], list[dict[str, object]]]:
    shape = raw.get("provider_shape")
    if shape == "alpha-v1":
        required = {
            "provider_shape", "fixture_only", "source_reference", "provider_id", "provider_version", "collection_method",
            "observed_at", "collected_at", "host_reference", "compose_project", "compose_service", "runtime_name",
            "runtime_container_id", "runtime_engine", "signals",
        }
        unknown = set(raw) - required - {"known_limitation", "orchestrator", "subject_id", "registry_reference", "image_reference"}
        missing = required - set(raw)
        if missing or unknown:
            raise ContainerHealthDataError(f"alpha fixture fields invalid; missing={sorted(missing)}, unknown={sorted(unknown)}.")
        signals = raw["signals"]
        if not isinstance(signals, list) or any(not isinstance(item, dict) for item in signals):
            raise ContainerHealthDataError("alpha fixture signals must be an array of objects.")
        context = {key: raw[key] for key in required if key != "signals"}
        context["known_limitation"] = raw.get("known_limitation")
        context["orchestrator"] = raw.get("orchestrator")
        context["subject_id"] = raw.get("subject_id")
        context["registry_reference"] = raw.get("registry_reference")
        context["image_reference"] = raw.get("image_reference")
        normalized_signals: list[dict[str, object]] = []
        for item in signals:
            if set(item) - {"signal", "value", "unit", "window_start", "window_end"} or "signal" not in item or "value" not in item:
                raise ContainerHealthDataError("alpha fixture signal contains missing or unknown fields.")
            normalized_signals.append(dict(item))
        return context, normalized_signals
    if shape == "beta-v1":
        required = {"provider_shape", "fixture_only", "source_reference", "provider", "timestamps", "resource", "measurements"}
        missing = required - set(raw)
        unknown = set(raw) - required - {"known_limitation"}
        if missing or unknown:
            raise ContainerHealthDataError(f"beta fixture fields invalid; missing={sorted(missing)}, unknown={sorted(unknown)}.")
        provider, timestamps, resource, measurements = raw["provider"], raw["timestamps"], raw["resource"], raw["measurements"]
        if not all(isinstance(value, dict) for value in (provider, timestamps, resource)) or not isinstance(measurements, list):
            raise ContainerHealthDataError("beta fixture provider, timestamps, resource, or measurements shape is invalid.")
        if set(provider) != {"id", "version", "method"} or set(timestamps) != {"observed", "collected"}:
            raise ContainerHealthDataError("beta fixture provider or timestamps fields are invalid.")
        if set(resource) != {"host", "project", "service", "name", "id", "engine", "orchestrator", "image_reference"}:
            raise ContainerHealthDataError("beta fixture resource fields are invalid.")
        context = {
            "provider_shape": shape, "fixture_only": raw["fixture_only"], "source_reference": raw["source_reference"],
            "provider_id": provider["id"], "provider_version": provider["version"], "collection_method": provider["method"],
            "observed_at": timestamps["observed"], "collected_at": timestamps["collected"], "host_reference": resource["host"],
            "compose_project": resource["project"], "compose_service": resource["service"], "runtime_name": resource["name"],
            "runtime_container_id": resource["id"], "runtime_engine": resource["engine"], "orchestrator": resource["orchestrator"],
            "known_limitation": raw.get("known_limitation"),
            "subject_id": None, "registry_reference": None, "image_reference": resource.get("image_reference"),
        }
        normalized_signals = []
        aliases = {"lifecycle": "container.lifecycle.observed_state", "healthcheck": "container.healthcheck.state", "memory_pressure": "container.memory.pressure"}
        for item in measurements:
            if not isinstance(item, dict) or set(item) - {"kind", "reading", "canonical_unit", "window"} or not {"kind", "reading"} <= set(item):
                raise ContainerHealthDataError("beta fixture measurement contains missing or unknown fields.")
            signal = aliases.get(str(item["kind"]), str(item["kind"]))
            window = item.get("window")
            normalized = {"signal": signal, "value": item["reading"], "unit": item.get("canonical_unit")}
            if window is not None:
                if not isinstance(window, dict) or set(window) != {"start", "end"}:
                    raise ContainerHealthDataError("beta fixture window is invalid.")
                normalized["window_start"] = window["start"]
                normalized["window_end"] = window["end"]
            normalized_signals.append(normalized)
        return context, normalized_signals
    raise UnsupportedContractVersion(f"Unsupported fixture provider shape: {shape!r}.")


def normalize_fixture_observation(
    raw: Mapping[str, object],
    subject: DeclaredContainerSubject,
    evaluated_at: str,
    policy_set: PolicySet,
) -> NormalizationResult:
    if contains_secret_like_content(json.dumps(raw, sort_keys=True)):
        raise ContainerHealthDataError("Fixture contains secret-like content.")
    subject_findings = validate_declared_subject(subject)
    if _has_errors(subject_findings):
        raise ContainerHealthDataError("Declared fixture subject is invalid.")
    context, signals = _fixture_fields(raw)
    if context.get("fixture_only") is not True:
        raise ContainerHealthDataError("Provider observations must explicitly declare fixture_only=true.")
    source_reference = context.get("source_reference")
    if not isinstance(source_reference, str) or not is_safe_repository_path(source_reference) or not source_reference.startswith("engineering/tests/fixtures/container_health/providers/"):
        raise ContainerHealthDataError("Fixture source reference is unsafe or outside the provider-fixture boundary.")
    explicit_identity_present = context.get("subject_id") is not None or context.get("registry_reference") is not None
    explicit_identity_matches = (
        context.get("subject_id") == subject.subject_id
        and context.get("registry_reference") == subject.registry_reference
    )
    tuple_matches = (
        context.get("host_reference") == subject.host_reference
        and context.get("compose_project") == subject.compose_project
        and context.get("compose_service") == subject.compose_service
    )
    runtime_matches = context.get("host_reference") == subject.host_reference and context.get("runtime_name") == subject.governed_runtime_name
    if explicit_identity_present and not explicit_identity_matches:
        return NormalizationResult((), (DomainFinding(FindingSeverity.WARNING, "subject_mapping_failed", "Explicit fixture identity contradicts the declared Registry subject.", source_reference),))
    if explicit_identity_matches:
        match_method = IdentityMatchMethod.SUBJECT_AND_REGISTRY_REFERENCE
    elif tuple_matches:
        match_method = IdentityMatchMethod.HOST_COMPOSE_PROJECT_SERVICE
    elif runtime_matches:
        match_method = IdentityMatchMethod.HOST_UNIQUE_RUNTIME_NAME
    else:
        code = "provider_limitation_applies" if context.get("known_limitation") else "subject_mapping_failed"
        message = "Known provider limitation prevents exact fixture identity resolution." if context.get("known_limitation") else "Fixture observation did not resolve to the declared Registry subject."
        return NormalizationResult((), (DomainFinding(FindingSeverity.WARNING, code, message, source_reference),))
    runtime_fallback = match_method == IdentityMatchMethod.HOST_UNIQUE_RUNTIME_NAME
    if context.get("known_limitation") and runtime_fallback:
        return NormalizationResult((), (DomainFinding(FindingSeverity.WARNING, "provider_limitation_applies", "Known provider limitation prevents exact fixture identity resolution.", source_reference),))
    try:
        method = CollectionMethod(str(context["collection_method"]))
    except ValueError as exc:
        raise ContainerHealthDataError("Fixture collection_method is unsupported.") from exc
    for field_name in ("provider_id", "provider_version", "observed_at", "collected_at", "host_reference", "runtime_engine"):
        if not isinstance(context.get(field_name), str) or not str(context[field_name]).strip():
            raise ContainerHealthDataError(f"Fixture {field_name} must be a nonblank string.")
    observed_at = str(context["observed_at"])
    collected_at = str(context["collected_at"])
    evidence_records: list[OperationalEvidence] = []
    findings: list[DomainFinding] = []
    for index, item in enumerate(signals):
        signal = str(item["signal"])
        contract = SIGNAL_CONTRACTS.get(signal)
        if contract is None:
            findings.append(DomainFinding(FindingSeverity.WARNING, "unsupported_signal", f"Unsupported fixture signal: {signal}.", source_reference))
            continue
        value_type, unit, _, window_required = contract
        if item.get("unit") != unit:
            findings.append(DomainFinding(FindingSeverity.WARNING, "unsupported_unit", f"Unsupported unit for {signal}.", source_reference))
            continue
        complete = not window_required or (item.get("window_start") is not None and item.get("window_end") is not None)
        freshness_policy_id = "container-healthcheck-freshness" if signal.startswith("container.healthcheck") else "container-lifecycle-freshness"
        freshness_rules = policy_set.artifact(freshness_policy_id).rules()
        aging_after = int(freshness_rules["aging_after_seconds"])
        maximum_age = int(freshness_rules["maximum_age_seconds"])
        freshness, age = _freshness(observed_at, evaluated_at, aging_after, maximum_age)
        limitation = bool(context.get("known_limitation"))
        confidence, confidence_reasons = _confidence(method, freshness, complete, limitation, runtime_fallback)
        if subject.expected_image_reference is not None and context.get("image_reference") == subject.expected_image_reference:
            confidence_reasons = tuple(sorted((*confidence_reasons, "IMAGE_IDENTITY_CORROBORATED")))
        finding_codes: list[str] = []
        if limitation:
            finding_codes.append("known_provider_limitation")
        payload = {
            "shape": context["provider_shape"], "provider": context["provider_id"], "source": source_reference,
            "subject": subject.subject_id, "signal": signal, "value": item["value"], "observed_at": observed_at, "index": index,
        }
        evidence = OperationalEvidence(
            ENVELOPE_VERSION, "container", PROFILE_VERSION, _stable_id("evidence", payload), subject.subject_id,
            "container_service", subject.registry_reference, subject.environment, _signal_evidence_type(signal), signal,
            item["value"], value_type, unit, observed_at, collected_at, evaluated_at,
            item.get("window_start") if isinstance(item.get("window_start"), str) else None,
            item.get("window_end") if isinstance(item.get("window_end"), str) else None,
            f"fixture_{str(context['provider_shape']).split('-')[0]}", str(context["provider_id"]), str(context["provider_version"]),
            "plat-14.1a-fixture-adapter-v1", source_reference,
            str(context["runtime_container_id"]) if context.get("runtime_container_id") is not None else None,
            match_method, method, freshness,
            f"{freshness_policy_id}:{policy_set.artifact(freshness_policy_id).policy_version}",
            maximum_age, age, CompletenessStatus.COMPLETE if complete else CompletenessStatus.MISSING_REQUIRED_ATTRIBUTES,
            tuple(sorted(("subject_id", "registry_reference", "observed_at", "source_reference", "host_reference", "runtime_engine"))),
            () if complete else ("observation_window",), None, confidence, confidence_reasons, tuple(sorted(finding_codes)),
            subject.registry_reference, subject.host_reference,
            str(context["runtime_name"]) if context.get("runtime_name") is not None else None,
            str(context["runtime_container_id"]) if context.get("runtime_container_id") is not None else None,
            str(context["runtime_engine"]), str(context["orchestrator"]) if context.get("orchestrator") is not None else None,
        )
        record_findings = validate_evidence(evidence)
        if _has_errors(record_findings):
            findings.extend(record_findings)
        else:
            evidence_records.append(evidence)
    return NormalizationResult(tuple(sorted(evidence_records, key=lambda item: item.evidence_id)), tuple(findings))


def _policy_path(repository_root: Path, reference: str) -> Path:
    if not is_safe_repository_path(reference):
        raise PolicyDataError(f"Unsafe policy reference: {reference}.")
    candidate = (repository_root / reference).resolve()
    root = repository_root.resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file() or candidate.is_symlink():
        raise PolicyDataError(f"Policy reference must identify a regular repository file: {reference}.")
    return candidate


def _policy_header(payload: Mapping[str, object], source_reference: str) -> PolicyArtifact:
    required = {
        "policy_id", "policy_version", "status", "compatible_contract_versions", "compatible_profile_versions",
        "purpose", "approval_authority", "effective_at", "supersedes", "rules",
    }
    missing, unknown = required - set(payload), set(payload) - required
    if missing or unknown:
        raise PolicyDataError(f"Policy fields invalid for {source_reference}; missing={sorted(missing)}, unknown={sorted(unknown)}.")
    if not isinstance(payload["rules"], dict):
        raise PolicyDataError(f"Policy rules must be an object: {source_reference}.")
    arrays = (payload["compatible_contract_versions"], payload["compatible_profile_versions"], payload["approval_authority"])
    if any(not isinstance(value, list) or any(not isinstance(item, str) for item in value) for value in arrays):
        raise PolicyDataError(f"Policy version and authority fields must be string arrays: {source_reference}.")
    return PolicyArtifact(
        str(payload["policy_id"]), str(payload["policy_version"]), str(payload["status"]),
        tuple(payload["compatible_contract_versions"]), tuple(payload["compatible_profile_versions"]), str(payload["purpose"]),
        tuple(payload["approval_authority"]), str(payload["effective_at"]), payload["supersedes"] if isinstance(payload["supersedes"], str) else None,
        json.dumps(payload["rules"], sort_keys=True, separators=(",", ":")), source_reference,
    )


def load_policy_set(repository_root: Path, manifest_reference: str) -> PolicySet:
    manifest_path = _policy_path(repository_root, manifest_reference)
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except (json.JSONDecodeError, OSError, UnicodeError) as exc:
        raise PolicyDataError(f"Unable to parse policy manifest: {exc}.") from exc
    if not isinstance(payload, dict):
        raise PolicyDataError("Policy manifest must be a JSON object.")
    required = {
        "manifest_id", "manifest_version", "status", "compatible_contract_versions", "compatible_profile_versions",
        "purpose", "approval_authority", "effective_at", "supersedes", "policy_references",
    }
    missing, unknown = required - set(payload), set(payload) - required
    if missing or unknown:
        raise PolicyDataError(f"Policy manifest fields invalid; missing={sorted(missing)}, unknown={sorted(unknown)}.")
    references = payload["policy_references"]
    if not isinstance(references, list) or any(not isinstance(value, str) for value in references):
        raise PolicyDataError("Policy manifest references must be an array of repository paths.")
    artifacts = []
    for reference in references:
        path = _policy_path(repository_root, reference)
        try:
            artifact_payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
        except (json.JSONDecodeError, OSError, UnicodeError) as exc:
            raise PolicyDataError(f"Unable to parse policy artifact {reference}: {exc}.") from exc
        if not isinstance(artifact_payload, dict):
            raise PolicyDataError(f"Policy artifact must be an object: {reference}.")
        artifacts.append(_policy_header(artifact_payload, reference))
    policy_set = PolicySet(
        str(payload["manifest_id"]), str(payload["manifest_version"]), str(payload["status"]),
        tuple(payload["compatible_contract_versions"]) if isinstance(payload["compatible_contract_versions"], list) else (),
        tuple(payload["compatible_profile_versions"]) if isinstance(payload["compatible_profile_versions"], list) else (),
        str(payload["purpose"]), tuple(payload["approval_authority"]) if isinstance(payload["approval_authority"], list) else (),
        str(payload["effective_at"]), payload["supersedes"] if isinstance(payload["supersedes"], str) else None,
        tuple(artifacts), manifest_reference,
    )
    validate_policy_set(policy_set)
    return policy_set


def validate_policy_set(policy_set: PolicySet) -> None:
    if policy_set.manifest_id != POLICY_MANIFEST_ID or policy_set.manifest_version != POLICY_MANIFEST_VERSION:
        raise PolicyDataError("Unsupported Container Operational Health policy manifest.")
    if policy_set.status != "active":
        raise PolicyDataError("Assessments may use only an active policy manifest.")
    if policy_set.compatible_contract_versions != (ENVELOPE_VERSION,) or policy_set.compatible_profile_versions != (PROFILE_VERSION,):
        raise PolicyDataError("Policy manifest is incompatible with contract/profile version 1.0.")
    if set(policy_set.approval_authority) != {"Architecture Gatekeeper", "Platform Administrator"}:
        raise PolicyDataError("Policy manifest approval authority is incomplete.")
    if not is_valid_timestamp(policy_set.effective_at):
        raise PolicyDataError("Policy manifest effective_at must be timezone-aware.")
    ids = [artifact.policy_id for artifact in policy_set.artifacts]
    if tuple(ids) != POLICY_LOAD_ORDER or len(ids) != len(set(ids)):
        raise PolicyDataError("Policy manifest must reference exactly one of every required policy.")
    for artifact in policy_set.artifacts:
        if artifact.status != "active" or artifact.policy_version != "1.0":
            raise PolicyDataError(f"Policy must be active at version 1.0: {artifact.policy_id}.")
        if artifact.compatible_contract_versions != (ENVELOPE_VERSION,) or artifact.compatible_profile_versions != (PROFILE_VERSION,):
            raise PolicyDataError(f"Policy is contract/profile incompatible: {artifact.policy_id}.")
        if set(artifact.approval_authority) != {"Architecture Gatekeeper", "Platform Administrator"}:
            raise PolicyDataError(f"Policy approval authority is incomplete: {artifact.policy_id}.")
        if not is_valid_timestamp(artifact.effective_at):
            raise PolicyDataError(f"Policy effective_at must be timezone-aware: {artifact.policy_id}.")
        rule_fields = set(artifact.rules())
        if rule_fields != POLICY_RULE_FIELDS[artifact.policy_id]:
            missing = sorted(POLICY_RULE_FIELDS[artifact.policy_id] - rule_fields)
            unknown = sorted(rule_fields - POLICY_RULE_FIELDS[artifact.policy_id])
            raise PolicyDataError(f"Policy rules are incomplete or unknown for {artifact.policy_id}; missing={missing}, unknown={unknown}.")
    reconciliation = policy_set.artifact("container-reconciliation").rules()
    expected_outcomes = [item.value for item in ReconciliationOutcome]
    if (
        reconciliation.get("allowed_outcomes") != expected_outcomes
        or reconciliation.get("match_hierarchy") != [
            "subject_and_registry_reference", "host_compose_project_service", "host_unique_runtime_name",
            "image_corroboration_only", "runtime_id_provenance_only", "provider_attributes_input_only",
            "fuzzy_matching_prohibited",
        ]
        or reconciliation.get("conclusive_absence_requires") != ["current", "complete", "exact_identity", "population_inventory"]
        or reconciliation.get("fuzzy_matching_allowed") is not False
        or reconciliation.get("retain_considered_evidence") is not True
        or reconciliation.get("silent_conflict_selection") is not False
    ):
        raise PolicyDataError("Reconciliation policy outcomes or fuzzy-match prohibition are invalid.")
    for policy_id in ("container-lifecycle-freshness", "container-healthcheck-freshness"):
        rules = policy_set.artifact(policy_id).rules()
        aging = rules.get("aging_after_seconds")
        maximum = rules.get("maximum_age_seconds")
        if (
            not isinstance(aging, int) or isinstance(aging, bool) or aging <= 0
            or not isinstance(maximum, int) or isinstance(maximum, bool) or maximum <= aging
            or aging != 30 or maximum != 60
            or rules.get("future_timestamp_behavior") != "invalid"
            or rules.get("timestamp_required") is not True
            or rules.get("healthy_requires") != "current"
        ):
            raise PolicyDataError(f"Freshness policy values are invalid: {policy_id}.")
    healthcheck = policy_set.artifact("container-healthcheck-freshness").rules()
    if healthcheck.get("registry_requirement_values") != [item.value for item in HealthCheckRequirement]:
        raise PolicyDataError("Health-check freshness policy Registry requirement values are invalid.")
    restart = policy_set.artifact("container-restart-window").rules()
    if (
        restart.get("mode") != "advisory"
        or restart.get("accepted_signals") != ["container.restart.count", "container.restart.occurred"]
        or restart.get("health_thresholds") != []
        or restart.get("occurred_requires_bounded_window") is not True
        or restart.get("reserved_reason_code") != "RESTART_THRESHOLD_EXCEEDED"
    ):
        raise PolicyDataError("Restart policy v1 must remain advisory without thresholds.")
    resource = policy_set.artifact("container-resource-pressure").rules()
    if (
        resource.get("mode") != "advisory_with_degradation"
        or resource.get("critical_memory_pressure_result") != "degraded"
        or resource.get("minimum_qualifying_confidence") != "medium"
        or resource.get("numeric_health_thresholds") != []
        or resource.get("unhealthy_rules") != []
    ):
        raise PolicyDataError("Resource-pressure policy v1 is invalid.")
    telemetry = policy_set.artifact("container-telemetry-availability").rules()
    if telemetry != {
        "identity_requirement": "exact",
        "mandatory_coverage": "complete",
        "mandatory_signals": ["container.lifecycle.observed_state", "container.healthcheck.state_when_required"],
        "material_provider_limitation_disqualifies_evidence": True,
        "provider_loss_proves_unhealthy": False,
    }:
        raise PolicyDataError("Telemetry-availability policy v1 is invalid.")
    health = policy_set.artifact("container-health").rules()
    if (
        health.get("evaluation_order") != [item.value for item in HealthStatus]
        or health.get("healthy_criteria") != [
            "active_subject", "exact_identity", "current_running_lifecycle", "complete_mandatory_coverage",
            "mandatory_confidence_at_least_medium", "required_healthcheck_passing", "no_critical_conflict",
            "no_material_provider_limitation",
        ]
        or health.get("healthy_default") is not False
        or health.get("reason_codes") != sorted(HEALTH_REASON_CODES)
    ):
        raise PolicyDataError("Container health policy order or reason catalog is invalid.")
    confidence = policy_set.artifact("container-assessment-confidence").rules()
    if confidence != {
        "allowed_values": [item.value for item in Confidence],
        "arithmetic_scoring": False,
        "assessment_cannot_exceed_lowest_mandatory_evidence": True,
        "healthy_minimum": "medium",
        "unresolved_critical_conflict_result": "none",
    }:
        raise PolicyDataError("Assessment-confidence policy is invalid.")


def reconcile(
    subject: DeclaredContainerSubject,
    evidence: Sequence[OperationalEvidence],
    reconciled_at: str,
    policy_set: PolicySet,
) -> ReconciliationRecord:
    subject_findings = validate_declared_subject(subject)
    if _has_errors(subject_findings):
        raise ContainerHealthDataError("Declared subject failed validation.")
    _parse_time(reconciled_at)
    for item in evidence:
        findings = validate_evidence_for_evaluation(item, reconciled_at, policy_set)
        if _has_errors(findings):
            raise ContainerHealthDataError(f"Evidence failed validation: {item.evidence_id}.")
    all_ids = tuple(sorted(item.evidence_id for item in evidence))
    rejected: list[RejectedEvidence] = []
    selected: list[OperationalEvidence] = []
    if subject.participation != ContainerParticipation.ACTIVE:
        outcome, reasons = ReconciliationOutcome.NOT_APPLICABLE, ("SUBJECT_NOT_ACTIVE",)
    else:
        mismatched = [
            item for item in evidence
            if item.subject_id != subject.subject_id
            or item.registry_reference != subject.registry_reference
            or item.container_service_reference != subject.registry_reference
            or item.environment != subject.environment
            or item.host_reference != subject.host_reference
        ]
        for item in mismatched:
            rejected.append(RejectedEvidence(item.evidence_id, "UNEXPECTED_SUBJECT"))
        candidates = [item for item in evidence if item not in mismatched]
        ambiguous = [item for item in candidates if "ambiguous_identity" in item.finding_codes]
        lifecycle = [item for item in candidates if item.signal_name == "container.lifecycle.observed_state"]
        current_lifecycle = [item for item in lifecycle if item.freshness_status == FreshnessStatus.CURRENT and item.evidence_confidence in {Confidence.HIGH, Confidence.MEDIUM}]
        current_values = {str(item.value) for item in current_lifecycle}
        if mismatched and not candidates:
            outcome, reasons = ReconciliationOutcome.UNEXPECTED, ("UNEXPECTED_SUBJECT",)
        elif ambiguous:
            outcome, reasons = ReconciliationOutcome.AMBIGUOUS, ("IDENTITY_UNRESOLVED",)
            rejected.extend(RejectedEvidence(item.evidence_id, "IDENTITY_UNRESOLVED") for item in ambiguous)
        elif len(current_values) > 1:
            outcome, reasons = ReconciliationOutcome.CONFLICTING, ("LIFECYCLE_CONFLICT",)
            rejected.extend(RejectedEvidence(item.evidence_id, "LIFECYCLE_CONFLICT") for item in current_lifecycle)
        elif current_lifecycle:
            outcome, reasons = ReconciliationOutcome.MATCHED, ("EXACT_IDENTITY_MATCH",)
            selected = [item for item in candidates if item.freshness_status == FreshnessStatus.CURRENT and item.evidence_confidence in {Confidence.HIGH, Confidence.MEDIUM}]
            rejected.extend(
                RejectedEvidence(item.evidence_id, "NOT_QUALIFYING_CURRENT_EVIDENCE")
                for item in candidates if item not in selected
            )
        elif lifecycle and all(item.freshness_status == FreshnessStatus.STALE for item in lifecycle):
            outcome, reasons = ReconciliationOutcome.STALE, ("LIFECYCLE_EVIDENCE_STALE",)
            rejected.extend(RejectedEvidence(item.evidence_id, "LIFECYCLE_EVIDENCE_STALE") for item in lifecycle)
        else:
            outcome, reasons = ReconciliationOutcome.MISSING, ("LIFECYCLE_EVIDENCE_MISSING",)
            rejected.extend(RejectedEvidence(item.evidence_id, "NOT_QUALIFYING_CURRENT_LIFECYCLE") for item in candidates)
    payload = {"subject": subject.subject_id, "evidence": all_ids, "outcome": outcome.value, "at": reconciled_at, "policy": policy_set.manifest_version}
    record = ReconciliationRecord(
        _stable_id("reconciliation", payload), RECONCILIATION_VERSION,
        policy_set.artifact("container-reconciliation").policy_version, policy_set.manifest_id, policy_set.manifest_version,
        subject.subject_id, subject.registry_reference, all_ids, outcome,
        next(iter({item.identity_match_method for item in selected}), None)
        if len({item.identity_match_method for item in selected}) <= 1 else None,
        tuple(sorted(reasons)), reconciled_at,
        tuple(sorted(item.reason_code for item in rejected if item.reason_code in {"LIFECYCLE_CONFLICT", "IDENTITY_UNRESOLVED"})),
        tuple(sorted(item.evidence_id for item in selected)), tuple(sorted(rejected, key=lambda item: (item.evidence_id, item.reason_code))),
    )
    if _has_errors(validate_reconciliation(record)):
        raise ContainerHealthDataError("Reconciliation output failed contract validation.")
    return record


def validate_reconciliation(record: ReconciliationRecord) -> tuple[DomainFinding, ...]:
    findings: list[DomainFinding] = []
    if not record.reconciliation_id.strip() or not record.subject_id.strip():
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.identity.required", "Reconciliation and subject identifiers are required."))
    if record.contract_version != RECONCILIATION_VERSION or record.policy_version != "1.0":
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.version.unsupported", "Reconciliation contract or policy version is unsupported."))
    if record.policy_manifest_id != POLICY_MANIFEST_ID or record.policy_manifest_version != POLICY_MANIFEST_VERSION:
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.policy_trace.invalid", "Reconciliation policy manifest trace is invalid."))
    if not is_safe_repository_path(record.registry_reference) or not is_valid_timestamp(record.reconciled_at):
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.reference_or_time.invalid", "Reconciliation Registry reference or timestamp is invalid."))
    if record.evidence_ids != tuple(sorted(set(record.evidence_ids))):
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.evidence.order", "Considered evidence IDs must be unique and sorted."))
    if not set(record.selected_evidence_ids) <= set(record.evidence_ids):
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.selected.invalid", "Selected evidence must be a subset of considered evidence."))
    rejected_ids = {item.evidence_id for item in record.rejected_evidence}
    if not rejected_ids <= set(record.evidence_ids) or rejected_ids.intersection(record.selected_evidence_ids):
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.rejected.invalid", "Rejected evidence must be considered and cannot also be selected."))
    if any(item.reason_code not in REJECTION_REASON_CODES for item in record.rejected_evidence):
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.rejection_reason.unknown", "Reconciliation contains an unknown rejection reason."))
    if not set(record.reason_codes) <= RECONCILIATION_REASON_CODES or record.reason_codes != tuple(sorted(set(record.reason_codes))):
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.reason.invalid", "Reconciliation reasons must be bounded, unique, and sorted."))
    if record.result == ReconciliationOutcome.MATCHED:
        if not record.selected_evidence_ids or record.match_method is None or record.reason_codes != ("EXACT_IDENTITY_MATCH",):
            findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.matched.unproven", "Matched reconciliation lacks selected evidence, match method, or exact-match reason."))
    elif record.match_method is not None:
        findings.append(DomainFinding(FindingSeverity.ERROR, "reconciliation.match_method.contradictory", "Only a matched reconciliation may claim a match method."))
    return tuple(findings)


_CONFIDENCE_ORDER = {Confidence.NONE: 0, Confidence.LOW: 1, Confidence.MEDIUM: 2, Confidence.HIGH: 3}


def _minimum_confidence(items: Sequence[OperationalEvidence]) -> Confidence:
    if not items:
        return Confidence.NONE
    return min((item.evidence_confidence for item in items), key=lambda value: _CONFIDENCE_ORDER[value])


def assess(
    subject: DeclaredContainerSubject,
    evidence: Sequence[OperationalEvidence],
    reconciliation: ReconciliationRecord,
    evaluated_at: str,
    policy_set: PolicySet,
) -> OperationalHealthAssessment:
    evaluated = _parse_time(evaluated_at)
    reconciliation_findings = validate_reconciliation(reconciliation)
    if _has_errors(reconciliation_findings):
        raise ContainerHealthDataError("Reconciliation failed validation before health assessment.")
    if reconciliation.subject_id != subject.subject_id or reconciliation.registry_reference != subject.registry_reference:
        raise ContainerHealthDataError("Reconciliation subject does not match the declared Registry subject.")
    by_signal: dict[str, list[OperationalEvidence]] = {}
    for item in evidence:
        by_signal.setdefault(item.signal_name, []).append(item)
    critical: list[str] = []
    noncritical: list[str] = []
    mandatory: list[OperationalEvidence] = []
    reason_codes: list[str] = []
    status: HealthStatus
    confidence = Confidence.NONE
    if subject.participation != ContainerParticipation.ACTIVE:
        status, reason_codes = HealthStatus.NOT_EVALUATED, ["SUBJECT_NOT_ACTIVE"]
    elif reconciliation.result == ReconciliationOutcome.AMBIGUOUS:
        status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["IDENTITY_UNRESOLVED"], ["Identity is ambiguous or unresolved."]
    elif reconciliation.result == ReconciliationOutcome.CONFLICTING:
        status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["LIFECYCLE_CONFLICT"], ["Current lifecycle evidence conflicts."]
    elif reconciliation.result == ReconciliationOutcome.STALE:
        status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["LIFECYCLE_EVIDENCE_MISSING"], ["Lifecycle evidence is stale."]
    elif reconciliation.result in {ReconciliationOutcome.MISSING, ReconciliationOutcome.UNEXPECTED}:
        status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["LIFECYCLE_EVIDENCE_MISSING"], ["No qualifying current lifecycle evidence exists."]
    elif reconciliation.result == ReconciliationOutcome.NOT_APPLICABLE:
        status, reason_codes = HealthStatus.NOT_EVALUATED, ["SUBJECT_NOT_ACTIVE"]
    else:
        selected_ids = set(reconciliation.selected_evidence_ids)
        selected = [item for item in evidence if item.evidence_id in selected_ids]
        lifecycle = [item for item in selected if item.signal_name == "container.lifecycle.observed_state"]
        if not lifecycle:
            status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["LIFECYCLE_EVIDENCE_MISSING"], ["Mandatory lifecycle evidence is absent."]
        else:
            mandatory.extend(lifecycle)
            lifecycle_state = str(lifecycle[0].value)
            limitations = [item for item in selected if item.signal_name == "container.telemetry.provider_limitation" and item.value == "applies"]
            coverage = [item for item in selected if item.signal_name == "container.telemetry.collection_coverage"]
            expected_availability = [item for item in selected if item.signal_name == "container.telemetry.expected_signal_availability"]
            identity_resolution = [item for item in selected if item.signal_name == "container.telemetry.identity_resolution"]
            if limitations or any("known_provider_limitation" in item.finding_codes for item in lifecycle):
                status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["PROVIDER_LIMITATION_APPLIES"], ["A provider limitation affects mandatory lifecycle evidence."]
            elif any(item.value in {"ambiguous", "unresolved"} for item in identity_resolution):
                status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["IDENTITY_UNRESOLVED"], ["Telemetry identity resolution is ambiguous or unresolved."]
            elif any(item.value in {"partial", "none", "not_assessable"} for item in coverage):
                status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["MANDATORY_TELEMETRY_PARTIAL"], ["Mandatory telemetry coverage is incomplete."]
            elif any(item.value in {"missing", "unsupported", "unknown"} for item in expected_availability):
                status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["TELEMETRY_UNAVAILABLE"], ["A required expected signal is unavailable."]
            elif any(item.value == "partial" for item in expected_availability):
                status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["MANDATORY_TELEMETRY_PARTIAL"], ["Expected mandatory signal availability is partial."]
            elif any(item.evidence_confidence in {Confidence.NONE, Confidence.LOW} for item in lifecycle):
                status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["MANDATORY_EVIDENCE_UNUSABLE"], ["Mandatory lifecycle evidence is below minimum confidence."]
            elif lifecycle_state == "missing" and "conclusive_absence" in lifecycle[0].finding_codes:
                status, reason_codes, critical = HealthStatus.UNHEALTHY, ["DECLARED_SUBJECT_ABSENT"], ["Complete direct inventory proves the active subject absent."]
            elif lifecycle_state == "exited":
                status, reason_codes, critical = HealthStatus.UNHEALTHY, ["UNEXPECTED_EXIT"], ["Current lifecycle evidence proves an unexpected exit."]
            elif lifecycle_state != "running":
                status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["LIFECYCLE_EVIDENCE_MISSING"], [f"Lifecycle state {lifecycle_state} does not prove current operation."]
            else:
                healthchecks = [item for item in selected if item.signal_name == "container.healthcheck.state"]
                if subject.health_check_requirement == HealthCheckRequirement.REQUIRED:
                    if not healthchecks:
                        status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["TELEMETRY_UNAVAILABLE"], ["Required health-check evidence is absent."]
                    else:
                        mandatory.extend(healthchecks)
                        healthcheck_state = str(healthchecks[0].value)
                        if healthchecks[0].evidence_confidence in {Confidence.NONE, Confidence.LOW}:
                            status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["MANDATORY_EVIDENCE_UNUSABLE"], ["Required health-check evidence is unusable."]
                        elif healthcheck_state == "failing":
                            status, reason_codes, critical = HealthStatus.UNHEALTHY, ["HEALTHCHECK_FAILED"], ["Required runtime health check is failing."]
                        elif healthcheck_state == "not_configured":
                            status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["REQUIRED_HEALTHCHECK_NOT_CONFIGURED"], ["Required runtime health check is not configured."]
                        elif healthcheck_state != "passing":
                            status, reason_codes, critical = HealthStatus.INSUFFICIENT_EVIDENCE, ["MANDATORY_EVIDENCE_UNUSABLE"], ["Required health check does not prove passing state."]
                        else:
                            status, reason_codes = HealthStatus.HEALTHY, ["ALL_MANDATORY_CRITERIA_PASSED"]
                else:
                    status, reason_codes = HealthStatus.HEALTHY, ["ALL_MANDATORY_CRITERIA_PASSED"]
                    if not healthchecks or any(item.value == "not_configured" for item in healthchecks):
                        reason_codes.append("HEALTHCHECK_NOT_REQUIRED")
                if status == HealthStatus.HEALTHY:
                    pressure = [item for item in selected if item.signal_name == "container.memory.pressure"]
                    if any(item.value == "critical" and item.evidence_confidence in {Confidence.HIGH, Confidence.MEDIUM} for item in pressure):
                        status, reason_codes = HealthStatus.DEGRADED, ["MEMORY_PRESSURE_CRITICAL"]
                        noncritical.append("Current qualified memory pressure is critical.")
                    elif any(item.value == "elevated" for item in pressure):
                        reason_codes.append("RESOURCE_PRESSURE_ELEVATED")
                        noncritical.append("Current memory pressure is elevated and advisory in policy v1.0.")
        stale_resources = [
            item for item in evidence
            if item.signal_name.startswith(("container.cpu", "container.memory")) and item.freshness_status == FreshnessStatus.STALE
        ]
        if stale_resources:
            reason_codes.append("RESOURCE_EVIDENCE_STALE")
            noncritical.append("Stale resource evidence is retained as advisory and does not affect current health.")
        provider_availability = [
            item for item in evidence
            if item.signal_name == "container.telemetry.provider_availability" and item.value in {"unavailable", "degraded", "unknown"}
        ]
        if provider_availability and status in {HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY}:
            reason_codes.append("ADVISORY_TELEMETRY_PARTIAL")
            noncritical.append("A provider is unavailable or degraded, but other mandatory evidence remains sufficient.")
        restart_evidence = [item for item in evidence if item.signal_name.startswith("container.restart")]
        if restart_evidence:
            noncritical.append("Restart evidence is advisory because policy v1.0 defines no restart threshold.")
        confidence = _minimum_confidence(mandatory) if status not in {HealthStatus.NOT_EVALUATED, HealthStatus.INSUFFICIENT_EVIDENCE} else Confidence.NONE
    valid_until: str | None = None
    if status in {HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY} and mandatory:
        expiries = [_parse_time(item.observed_at) + timedelta(seconds=item.maximum_age_seconds) for item in mandatory]
        valid_until = _utc(min(expiries))
    reason_codes = sorted(set(reason_codes))
    if not set(reason_codes) <= HEALTH_REASON_CODES:
        raise PolicyDataError("Assessment attempted to emit a reason outside catalog v1.0.")
    payload = {"subject": subject.subject_id, "reconciliation": reconciliation.reconciliation_id, "evidence": sorted(item.evidence_id for item in evidence), "status": status.value, "at": evaluated_at}
    mandatory_ids = {item.evidence_id for item in mandatory}
    selected_ids = set(reconciliation.selected_evidence_ids)
    evidence_summary = tuple(
        AssessmentEvidenceSummary(
            item.evidence_id,
            item.signal_name,
            "mandatory" if item.evidence_id in mandatory_ids else
            "advisory" if item.signal_name.startswith(("container.restart", "container.cpu", "container.memory"))
            or item.signal_name == "container.telemetry.provider_availability"
            else "advisory" if item.evidence_id in selected_ids else "constraining",
            item.freshness_status,
            item.evidence_confidence,
            item.observed_at,
            _utc(_parse_time(item.observed_at) + timedelta(seconds=item.maximum_age_seconds)),
            tuple(sorted(item.finding_codes)),
        )
        for item in sorted(evidence, key=lambda value: value.evidence_id)
    )
    return OperationalHealthAssessment(
        _stable_id("assessment", payload), ASSESSMENT_VERSION, subject.subject_id, subject.registry_reference,
        "container", PROFILE_VERSION,
        policy_set.manifest_id, policy_set.manifest_version, policy_set.versions(),
        policy_set.artifact("container-health").policy_version,
        policy_set.artifact("container-assessment-confidence").policy_version,
        reconciliation.reconciliation_id, reconciliation.result, tuple(sorted(item.evidence_id for item in evidence)), evidence_summary,
        status, confidence,
        tuple(reason_codes), tuple(sorted(critical)), tuple(sorted(noncritical)), evaluated_at, valid_until, True, ACTIVATION_STATUS,
    )


def validate_assessment(assessment: OperationalHealthAssessment) -> tuple[DomainFinding, ...]:
    findings: list[DomainFinding] = []
    if not assessment.assessment_id.strip() or not assessment.subject_id.strip() or not assessment.reconciliation_id.strip():
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.identity.required", "Assessment, subject, and reconciliation identifiers are required."))
    if assessment.contract_version != ASSESSMENT_VERSION:
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.contract_version.unsupported", "Unsupported assessment contract version."))
    if assessment.evidence_profile_type != "container" or assessment.evidence_profile_version != PROFILE_VERSION:
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.profile.unsupported", "Assessment evidence profile is unsupported."))
    if (
        assessment.policy_manifest_id != POLICY_MANIFEST_ID
        or assessment.policy_manifest_version != POLICY_MANIFEST_VERSION
        or assessment.health_policy_version != "1.0"
        or assessment.assessment_confidence_policy_version != "1.0"
        or assessment.policy_versions != tuple(f"{policy_id}:1.0" for policy_id in sorted(POLICY_IDS))
    ):
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.policy_trace.invalid", "Assessment policy trace is incomplete or unsupported."))
    if not assessment.fixture_only or assessment.activation_status != ACTIVATION_STATUS:
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.activation.invalid", "Repository-slice assessments must remain fixture-only and not activated."))
    if not is_safe_repository_path(assessment.registry_reference):
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.registry_reference.unsafe", "Assessment Registry reference is unsafe."))
    if not is_valid_timestamp(assessment.evaluated_at) or (assessment.valid_until is not None and not is_valid_timestamp(assessment.valid_until)):
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.timestamp.invalid", "Assessment timestamps must be timezone-aware."))
    if not set(assessment.reason_codes) <= HEALTH_REASON_CODES:
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.reason_code.unknown", "Assessment contains an unknown reason code."))
    if assessment.reason_codes != tuple(sorted(set(assessment.reason_codes))):
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.reason_code.order", "Assessment reason codes must be unique and sorted."))
    if assessment.evidence_ids != tuple(sorted(set(assessment.evidence_ids))):
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.evidence.order", "Assessment evidence references must be unique and sorted."))
    summary_ids = tuple(item.evidence_id for item in assessment.evidence_summary)
    if summary_ids != assessment.evidence_ids or summary_ids != tuple(sorted(summary_ids)):
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.evidence_summary.invalid", "Assessment evidence summary must cover every evidence reference exactly once in stable order."))
    for item in assessment.evidence_summary:
        if item.role not in {"mandatory", "advisory", "constraining"} or not is_valid_timestamp(item.observed_at) or not is_valid_timestamp(item.expires_at):
            findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.evidence_summary.invalid", "Assessment evidence summary contains an invalid role or timestamp."))
            break
    if assessment.health_status == HealthStatus.HEALTHY:
        mandatory = [item for item in assessment.evidence_summary if item.role == "mandatory"]
        if (
            "ALL_MANDATORY_CRITERIA_PASSED" not in assessment.reason_codes
            or assessment.assessment_confidence not in {Confidence.HIGH, Confidence.MEDIUM}
            or assessment.valid_until is None
            or not mandatory
            or any(item.freshness_status != FreshnessStatus.CURRENT for item in mandatory)
        ):
            findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.healthy.unproven", "Healthy lacks mandatory proof, confidence, or validity."))
    if assessment.health_status == HealthStatus.INSUFFICIENT_EVIDENCE and assessment.assessment_confidence != Confidence.NONE:
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.insufficient.confidence", "Insufficient evidence must have assessment confidence none."))
    if assessment.health_status == HealthStatus.NOT_EVALUATED and assessment.valid_until is not None:
        findings.append(DomainFinding(FindingSeverity.ERROR, "assessment.not_evaluated.validity", "Not evaluated cannot claim current validity."))
    return tuple(findings)


def evaluate_bundle(bundle: EvaluationBundle, policy_set: PolicySet) -> EvaluationResult:
    reconciliation = reconcile(bundle.declared_subject, bundle.evidence, bundle.evaluated_at, policy_set)
    assessment = assess(bundle.declared_subject, bundle.evidence, reconciliation, bundle.evaluated_at, policy_set)
    findings = validate_assessment(assessment)
    if _has_errors(findings):
        raise ContainerHealthDataError("Container Operational Health assessment failed validation.")
    return EvaluationResult(bundle.evidence, reconciliation, assessment, "container-health-markdown-v1")


def assessment_presentation_findings(
    assessment: OperationalHealthAssessment, presented_at: str
) -> tuple[DomainFinding, ...]:
    findings = list(validate_assessment(assessment))
    presented = _parse_time(presented_at)
    if assessment.valid_until is not None and presented > _parse_time(assessment.valid_until):
        findings.append(DomainFinding(FindingSeverity.WARNING, "ASSESSMENT_EXPIRED", "Assessment is expired and cannot be presented as current health."))
    return tuple(findings)
