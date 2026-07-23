from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence

from engineering.platform_eap.container_health import (
    CompletenessStatus,
    Confidence,
    CollectionMethod,
    FreshnessStatus,
    IdentityMatchMethod,
    OperationalEvidence,
    SIGNAL_CONTRACTS,
    validate_evidence,
)
from engineering.platform_eap.execution_capability import (
    contains_secret_like_content,
    is_safe_repository_path,
    is_valid_timestamp,
)


CONTRACT_VERSION = "1.0"
CAPABILITY_VERSION = "1.0"
FIXTURE_CATALOG_VERSION = "1.0"
ADAPTER_VERSION = "repository-provider-adapter-foundation-v1.0"
ACTIVATION_STATUS = "not_activated"
MAX_PAYLOAD_BYTES = 65_536
MAX_SIGNALS = 32
MAX_LIMITATIONS = 16
MAX_WARNINGS = 16
ACCEPTED_CONTENT_TYPES = ("application/json",)
FIXTURE_ROOT = "engineering/tests/fixtures/provider_adapter"


class ProviderAdapterDataError(ValueError):
    """Raised when untrusted provider-adapter data is malformed."""


class UnsupportedProviderContractVersion(ProviderAdapterDataError):
    """Raised when a provider-adapter contract version is unsupported."""


class FindingSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class ObservationMode(str, Enum):
    REPOSITORY_FIXTURE_ONE_SHOT = "repository_fixture_one_shot"
    NAMED_TARGET_ONE_SHOT = "named_target_one_shot"
    NAMED_TARGET_WINDOW = "named_target_window"


class TargetResolution(str, Enum):
    EXACT = "exact"
    ABSENT = "absent"
    CONFLICTING = "conflicting"
    DUPLICATE = "duplicate"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"


class CoverageStatus(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    NONE = "none"
    NOT_ASSESSABLE = "not_assessable"


class ProviderConfidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class ProviderAvailability(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class Retryability(str, Enum):
    NOT_RETRYABLE = "not_retryable"
    RETRYABLE_WITHIN_WINDOW = "retryable_within_window"
    NEW_AUTHORIZATION_REQUIRED = "new_authorization_required"


class ProviderFailureCategory(str, Enum):
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    PROVIDER_TIMEOUT = "provider_timeout"
    PROVIDER_AUTHENTICATION_FAILURE = "provider_authentication_failure"
    PROVIDER_AUTHORIZATION_FAILURE = "provider_authorization_failure"
    PROVIDER_VERSION_MISMATCH = "provider_version_mismatch"
    MALFORMED_RESPONSE = "malformed_response"
    SIGNAL_UNAVAILABLE = "signal_unavailable"
    CAPABILITY_UNSUPPORTED = "capability_unsupported"
    UNKNOWN_TARGET = "unknown_target"
    AMBIGUOUS_TARGET = "ambiguous_target"
    DUPLICATE_TARGET = "duplicate_target"
    CONFIGURATION_INVALID = "configuration_invalid"
    INTERNAL_ADAPTER_VALIDATION_FAILURE = "internal_adapter_validation_failure"
    PROVIDER_INTERNAL_ERROR = "provider_internal_error"
    RESPONSE_OVERSIZED = "response_oversized"
    CONTENT_TYPE_UNSUPPORTED = "content_type_unsupported"
    PARTIAL_RESPONSE = "partial_response"
    PROVIDER_LIMITATION = "provider_limitation"
    UNSAFE_PAYLOAD = "unsafe_payload"


class MockScenario(str, Enum):
    HEALTHY = "healthy"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    TIMEOUT = "timeout"
    AUTHORIZATION_DENIED = "authorization_denied"
    UNSUPPORTED_PROVIDER_VERSION = "unsupported_provider_version"
    MALFORMED_PAYLOAD = "malformed_payload"
    PARTIAL_RESPONSE = "partial_response"
    MISSING_MANDATORY_SIGNALS = "missing_mandatory_signals"
    CONFLICTING_IDENTITY = "conflicting_identity"
    UNKNOWN_TARGET = "unknown_target"
    DUPLICATE_TARGETS = "duplicate_targets"
    PROVIDER_LIMITATION = "provider_limitation"
    CAPABILITY_MISMATCH = "capability_mismatch"
    LARGE_PAYLOAD_REJECTION = "large_payload_rejection"


@dataclass(frozen=True)
class ProviderFinding:
    severity: FindingSeverity
    code: str
    message: str
    reference: str | None = None


@dataclass(frozen=True)
class ProductionProviderAdapterIdentity:
    contract_version: str
    adapter_id: str
    adapter_name: str
    adapter_version: str
    adapter_artifact_digest: str
    provider_type: str
    provider_api_version: str
    supported_provider_versions: tuple[str, ...]
    supported_evidence_contract_versions: tuple[str, ...]
    supported_profile_versions: tuple[str, ...]
    supported_signal_names: tuple[str, ...]
    configuration_digest: str
    fixture_only: bool
    activation_status: str


@dataclass(frozen=True)
class MandatorySignalSet:
    contract_version: str
    signals: tuple[str, ...]


@dataclass(frozen=True)
class OptionalSignalSet:
    contract_version: str
    signals: tuple[str, ...]


@dataclass(frozen=True)
class AuthorizationContext:
    contract_version: str
    authorization_reference: str
    authorization_digest: str
    authorization_valid_from: str
    authorization_valid_until: str
    observation_mode: ObservationMode
    subject_id: str
    registry_reference: str
    registry_record_digest: str
    host_reference: str
    compose_project: str | None
    compose_service: str | None
    governed_runtime_name: str | None
    expected_image_reference: str | None
    expected_image_digest: str | None
    health_check_requirement: str
    provider_boundary_reference: str
    provider_boundary_digest: str
    output_reference: str
    fixture_only: bool
    activation_status: str


@dataclass(frozen=True)
class ProviderRequest:
    contract_version: str
    request_id: str
    requested_at: str
    adapter_id: str
    authorization_context: AuthorizationContext
    mandatory_signal_set: MandatorySignalSet
    optional_signal_set: OptionalSignalSet

    def requested_signals(self) -> tuple[str, ...]:
        return tuple(sorted((*self.mandatory_signal_set.signals, *self.optional_signal_set.signals)))


@dataclass(frozen=True)
class ProviderCapabilityDeclaration:
    contract_version: str
    capability_version: str
    provider_type: str
    supported_provider_versions: tuple[str, ...]
    supported_adapter_versions: tuple[str, ...]
    supported_evidence_contract_versions: tuple[str, ...]
    supported_profile_versions: tuple[str, ...]
    supported_signals: tuple[str, ...]
    supported_identity_fields: tuple[str, ...]
    supported_observation_modes: tuple[ObservationMode, ...]
    known_limitations: tuple[str, ...]
    fixture_only: bool
    live_access_supported: bool


@dataclass(frozen=True)
class ProviderLimitation:
    limitation_code: str
    affected_signals: tuple[str, ...]
    material: bool
    safe_reference: str


@dataclass(frozen=True)
class ProviderProvenance:
    provider_type: str
    provider_id: str
    provider_version: str
    adapter_id: str
    adapter_version: str
    capability_version: str
    fixture_reference: str
    raw_response_digest: str


@dataclass(frozen=True)
class ProviderCoverage:
    status: CoverageStatus
    requested_signals: tuple[str, ...]
    returned_signals: tuple[str, ...]
    missing_expected_signals: tuple[str, ...]
    unknown_signals: tuple[str, ...]


@dataclass(frozen=True)
class ObservationMetadata:
    provider_observation_id: str
    correlation_id: str
    collection_started_at: str
    collection_ended_at: str
    observed_at: str
    observation_window_start: str | None
    observation_window_end: str | None


@dataclass(frozen=True)
class ObservedIdentity:
    target_resolution_result: TargetResolution
    runtime_container_id: str | None
    runtime_name: str | None
    compose_project: str | None
    compose_service: str | None
    image_reference: str | None
    image_digest: str | None
    host_reference: str | None
    runtime_engine: str
    orchestrator: str | None


@dataclass(frozen=True)
class NormalizedSignal:
    signal_name: str
    value: str | int | float | bool
    value_type: str
    unit: str | None
    observed_at: str
    observation_window_start: str | None
    observation_window_end: str | None
    collection_method: CollectionMethod


@dataclass(frozen=True)
class ProviderResponse:
    contract_version: str
    metadata: ObservationMetadata
    observed_identity: ObservedIdentity
    provenance: ProviderProvenance
    coverage: ProviderCoverage
    limitations: tuple[ProviderLimitation, ...]
    provider_confidence: ProviderConfidence
    provider_confidence_reasons: tuple[str, ...]
    warnings: tuple[str, ...]
    signals: tuple[NormalizedSignal, ...]
    fixture_only: bool
    activation_status: str


@dataclass(frozen=True)
class ProviderFailure:
    contract_version: str
    request_id: str
    failure_category: ProviderFailureCategory
    failure_code: str
    safe_message: str
    retryability: Retryability
    affected_signals: tuple[str, ...]
    provider_available: ProviderAvailability
    target_resolution_result: TargetResolution | None
    collection_started_at: str
    failed_at: str
    limitations: tuple[ProviderLimitation, ...]
    audit_correlation_id: str
    fixture_only: bool
    activation_status: str


@dataclass(frozen=True)
class ProviderResult:
    contract_version: str
    observation_result: ProviderResponse | None
    failure_result: ProviderFailure | None


@dataclass(frozen=True)
class ProviderNormalizationResult:
    contract_version: str
    evidence_records: tuple[OperationalEvidence, ...]
    failure_result: ProviderFailure | None
    limitations: tuple[ProviderLimitation, ...]
    coverage: ProviderCoverage | None
    unknown_signals: tuple[str, ...]
    findings: tuple[ProviderFinding, ...]


def _finding(severity: FindingSeverity, code: str, message: str, reference: str | None = None) -> ProviderFinding:
    return ProviderFinding(severity, code, message, reference)


def _blank(value: object) -> bool:
    return not isinstance(value, str) or not value.strip()


def _ordered(values: Sequence[str]) -> bool:
    return tuple(values) == tuple(sorted(set(values)))


def _digest(value: str) -> bool:
    return value.startswith("sha256:") and len(value) == 71 and all(character in "0123456789abcdef" for character in value[7:])


def _canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _stable_id(prefix: str, value: object) -> str:
    return f"{prefix}-{_canonical_digest(value)[7:23]}"


def _time_order(start: str, end: str) -> bool:
    if not is_valid_timestamp(start) or not is_valid_timestamp(end):
        return False
    from datetime import datetime

    return datetime.fromisoformat(end.replace("Z", "+00:00")) >= datetime.fromisoformat(start.replace("Z", "+00:00"))


def repository_adapter_identity() -> ProductionProviderAdapterIdentity:
    signals = tuple(sorted(SIGNAL_CONTRACTS))
    identity_seed = {
        "adapter_id": "repository-provider-adapter-foundation",
        "adapter_version": ADAPTER_VERSION,
        "contract_version": CONTRACT_VERSION,
        "signals": signals,
    }
    return ProductionProviderAdapterIdentity(
        CONTRACT_VERSION,
        "repository-provider-adapter-foundation",
        "Repository-Only Production Provider Adapter Foundation",
        ADAPTER_VERSION,
        _canonical_digest(identity_seed),
        "repository_mock",
        "repository-fixture-v1",
        ("repository-fixture-v1",),
        ("1.0",),
        ("1.0",),
        signals,
        _canonical_digest({"fixture_only": True, "live_access": False, "networking": False}),
        True,
        ACTIVATION_STATUS,
    )


def repository_capability() -> ProviderCapabilityDeclaration:
    return ProviderCapabilityDeclaration(
        CONTRACT_VERSION,
        CAPABILITY_VERSION,
        "repository_mock",
        ("repository-fixture-v1",),
        (ADAPTER_VERSION,),
        ("1.0",),
        ("1.0",),
        tuple(sorted(SIGNAL_CONTRACTS)),
        tuple(sorted(("compose_project", "compose_service", "host_reference", "image_digest", "image_reference", "runtime_container_id", "runtime_name"))),
        (ObservationMode.REPOSITORY_FIXTURE_ONE_SHOT,),
        tuple(sorted(("repository_fixtures_only", "no_live_provider_access", "no_named_target_authorization"))),
        True,
        False,
    )


def validate_adapter_identity(identity: ProductionProviderAdapterIdentity) -> tuple[ProviderFinding, ...]:
    findings: list[ProviderFinding] = []
    if identity.contract_version != CONTRACT_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "adapter.contract_version.unsupported", "Adapter contract version is unsupported."))
    for field_name in ("adapter_id", "adapter_name", "adapter_version", "provider_type", "provider_api_version"):
        if _blank(getattr(identity, field_name)):
            findings.append(_finding(FindingSeverity.ERROR, f"adapter.{field_name}.required", f"Adapter {field_name} is required."))
    if not _digest(identity.adapter_artifact_digest) or not _digest(identity.configuration_digest):
        findings.append(_finding(FindingSeverity.ERROR, "adapter.digest.invalid", "Adapter artifact and configuration digests must be SHA-256 values."))
    for field_name in ("supported_provider_versions", "supported_evidence_contract_versions", "supported_profile_versions", "supported_signal_names"):
        values = getattr(identity, field_name)
        if not values or not _ordered(values):
            findings.append(_finding(FindingSeverity.ERROR, f"adapter.{field_name}.invalid", f"Adapter {field_name} must be nonempty, unique, and sorted."))
    if not identity.fixture_only or identity.activation_status != ACTIVATION_STATUS:
        findings.append(_finding(FindingSeverity.ERROR, "adapter.repository_scope.required", "Repository adapter identity must remain fixture-only and not activated."))
    return tuple(findings)


def validate_capability(capability: ProviderCapabilityDeclaration) -> tuple[ProviderFinding, ...]:
    findings: list[ProviderFinding] = []
    if capability.contract_version != CONTRACT_VERSION or capability.capability_version != CAPABILITY_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "capability.version.unsupported", "Provider capability contract or capability version is unsupported."))
    for field_name in (
        "supported_provider_versions",
        "supported_adapter_versions",
        "supported_evidence_contract_versions",
        "supported_profile_versions",
        "supported_signals",
        "supported_identity_fields",
        "known_limitations",
    ):
        values = getattr(capability, field_name)
        if not values or not _ordered(values):
            findings.append(_finding(FindingSeverity.ERROR, f"capability.{field_name}.invalid", f"Capability {field_name} must be nonempty, unique, and sorted."))
    if capability.supported_observation_modes != (ObservationMode.REPOSITORY_FIXTURE_ONE_SHOT,):
        findings.append(_finding(FindingSeverity.ERROR, "capability.observation_mode.live_prohibited", "Repository capability may expose only repository_fixture_one_shot."))
    if not capability.fixture_only or capability.live_access_supported:
        findings.append(_finding(FindingSeverity.ERROR, "capability.live_access.prohibited", "Repository capability must be fixture-only with live access unsupported."))
    if any(signal not in SIGNAL_CONTRACTS for signal in capability.supported_signals):
        findings.append(_finding(FindingSeverity.ERROR, "capability.signal.unsupported", "Capability declares a signal outside the published Container Evidence Profile."))
    return tuple(findings)


def validate_authorization(context: AuthorizationContext, requested_at: str) -> tuple[ProviderFinding, ...]:
    findings: list[ProviderFinding] = []
    if context.contract_version != CONTRACT_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "authorization.contract_version.unsupported", "Authorization context version is unsupported."))
    if context.observation_mode != ObservationMode.REPOSITORY_FIXTURE_ONE_SHOT:
        findings.append(_finding(FindingSeverity.ERROR, "authorization.named_target.prohibited", "Repository foundation does not authorize named-target or live observation modes."))
    if not context.fixture_only or context.activation_status != ACTIVATION_STATUS:
        findings.append(_finding(FindingSeverity.ERROR, "authorization.repository_scope.required", "Authorization context must remain a non-activated repository fixture."))
    for field_name in ("authorization_reference", "registry_reference", "host_reference", "provider_boundary_reference", "output_reference"):
        value = getattr(context, field_name)
        if not is_safe_repository_path(value):
            findings.append(_finding(FindingSeverity.ERROR, f"authorization.{field_name}.unsafe", f"Authorization {field_name} must be repository-relative and traversal-free.", value))
    fixture_references = (context.authorization_reference, context.provider_boundary_reference, context.output_reference)
    if any(not reference.startswith(f"{FIXTURE_ROOT}/") for reference in fixture_references):
        findings.append(_finding(FindingSeverity.ERROR, "authorization.fixture_boundary.required", "Authorization, provider boundary, and output references must remain inside provider-adapter fixtures."))
    if not context.registry_reference.startswith("engineering/tests/fixtures/container_health/registry/"):
        findings.append(_finding(FindingSeverity.ERROR, "authorization.registry.fixture_required", "Repository provider requests may reference only synthetic Registry fixtures."))
    for digest in (context.authorization_digest, context.registry_record_digest, context.provider_boundary_digest):
        if not _digest(digest):
            findings.append(_finding(FindingSeverity.ERROR, "authorization.digest.invalid", "Authorization digests must be SHA-256 values."))
    if _blank(context.subject_id) or "*" in context.subject_id or context.subject_id.startswith("svc-pihole"):
        findings.append(_finding(FindingSeverity.ERROR, "authorization.subject.invalid", "Authorization subject must be a bounded synthetic target without wildcards."))
    if context.health_check_requirement not in {"required", "optional", "not_applicable"}:
        findings.append(_finding(FindingSeverity.ERROR, "authorization.health_check_requirement.invalid", "Health-check requirement is unsupported."))
    if not _time_order(context.authorization_valid_from, context.authorization_valid_until) or not is_valid_timestamp(requested_at):
        findings.append(_finding(FindingSeverity.ERROR, "authorization.window.invalid", "Authorization timestamps must form a valid timezone-aware window."))
    else:
        from datetime import datetime

        requested = datetime.fromisoformat(requested_at.replace("Z", "+00:00"))
        valid_from = datetime.fromisoformat(context.authorization_valid_from.replace("Z", "+00:00"))
        valid_until = datetime.fromisoformat(context.authorization_valid_until.replace("Z", "+00:00"))
        if not valid_from <= requested <= valid_until:
            findings.append(_finding(FindingSeverity.ERROR, "authorization.expired", "Provider request is outside the fixture authorization window."))
    if contains_secret_like_content(json.dumps(context_to_primitive(context), sort_keys=True)):
        findings.append(_finding(FindingSeverity.ERROR, "authorization.secret_like_content", "Authorization context contains secret-like content."))
    return tuple(findings)


def validate_request(
    request: ProviderRequest,
    identity: ProductionProviderAdapterIdentity | None = None,
    capability: ProviderCapabilityDeclaration | None = None,
) -> tuple[ProviderFinding, ...]:
    active_identity = identity or repository_adapter_identity()
    active_capability = capability or repository_capability()
    findings = list(validate_adapter_identity(active_identity))
    findings.extend(validate_capability(active_capability))
    findings.extend(validate_authorization(request.authorization_context, request.requested_at))
    if request.contract_version != CONTRACT_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "request.contract_version.unsupported", "Provider request contract version is unsupported."))
    if _blank(request.request_id) or request.adapter_id != active_identity.adapter_id:
        findings.append(_finding(FindingSeverity.ERROR, "request.identity.invalid", "Provider request ID or adapter binding is invalid."))
    if request.mandatory_signal_set.contract_version != CONTRACT_VERSION or request.optional_signal_set.contract_version != CONTRACT_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "request.signal_set.version.unsupported", "Signal-set contract version is unsupported."))
    mandatory = request.mandatory_signal_set.signals
    optional = request.optional_signal_set.signals
    if not mandatory or not _ordered(mandatory) or not _ordered(optional) or set(mandatory).intersection(optional):
        findings.append(_finding(FindingSeverity.ERROR, "request.signal_set.invalid", "Mandatory and optional signals must be sorted, unique, disjoint, and include at least one mandatory signal."))
    requested = request.requested_signals()
    if len(requested) > MAX_SIGNALS or any(signal not in active_capability.supported_signals for signal in requested):
        findings.append(_finding(FindingSeverity.ERROR, "request.signal.unsupported", "Provider request contains excessive or unsupported signals."))
    return tuple(findings)


def validate_limitation(limitation: ProviderLimitation) -> tuple[ProviderFinding, ...]:
    findings: list[ProviderFinding] = []
    if _blank(limitation.limitation_code) or not _ordered(limitation.affected_signals):
        findings.append(_finding(FindingSeverity.ERROR, "limitation.fields.invalid", "Provider limitation code and affected signals must be bounded and deterministic."))
    if any(signal not in SIGNAL_CONTRACTS for signal in limitation.affected_signals):
        findings.append(_finding(FindingSeverity.ERROR, "limitation.signal.unsupported", "Provider limitation references an unsupported canonical signal."))
    if not is_safe_repository_path(limitation.safe_reference):
        findings.append(_finding(FindingSeverity.ERROR, "limitation.reference.unsafe", "Provider limitation reference must be repository-relative and safe."))
    return tuple(findings)


def validate_response(
    response: ProviderResponse,
    request: ProviderRequest,
    capability: ProviderCapabilityDeclaration | None = None,
) -> tuple[ProviderFinding, ...]:
    active_capability = capability or repository_capability()
    findings = list(validate_request(request, capability=active_capability))
    if response.contract_version != CONTRACT_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "response.contract_version.unsupported", "Provider response contract version is unsupported."))
    if not response.fixture_only or response.activation_status != ACTIVATION_STATUS:
        findings.append(_finding(FindingSeverity.ERROR, "response.repository_scope.required", "Provider response must remain fixture-only and not activated."))
    if response.provenance.provider_version not in active_capability.supported_provider_versions:
        findings.append(_finding(FindingSeverity.ERROR, "response.provider_version.unsupported", "Provider response version is not declared by the capability."))
    if response.provenance.adapter_version not in active_capability.supported_adapter_versions:
        findings.append(_finding(FindingSeverity.ERROR, "response.adapter_version.unsupported", "Provider response adapter version is not declared by the capability."))
    if not response.provenance.fixture_reference.startswith(f"{FIXTURE_ROOT}/") or not is_safe_repository_path(response.provenance.fixture_reference):
        findings.append(_finding(FindingSeverity.ERROR, "response.fixture_reference.unsafe", "Provider response fixture reference is outside the governed fixture boundary."))
    if not _digest(response.provenance.raw_response_digest):
        findings.append(_finding(FindingSeverity.ERROR, "response.digest.invalid", "Provider response digest must be SHA-256."))
    metadata = response.metadata
    if not _time_order(metadata.collection_started_at, metadata.collection_ended_at) or not is_valid_timestamp(metadata.observed_at):
        findings.append(_finding(FindingSeverity.ERROR, "response.time.invalid", "Provider response timestamps are invalid or out of order."))
    identity = response.observed_identity
    if identity.target_resolution_result == TargetResolution.EXACT:
        context = request.authorization_context
        exact = (
            identity.host_reference == context.host_reference
            and identity.compose_project == context.compose_project
            and identity.compose_service == context.compose_service
        )
        if not exact:
            findings.append(_finding(FindingSeverity.ERROR, "response.identity.conflicting", "Exact provider identity does not match the authorized synthetic target."))
    coverage = response.coverage
    if not all(_ordered(values) for values in (coverage.requested_signals, coverage.returned_signals, coverage.missing_expected_signals, coverage.unknown_signals)):
        findings.append(_finding(FindingSeverity.ERROR, "response.coverage.order", "Coverage signal sets must be unique and sorted."))
    if coverage.requested_signals != request.requested_signals():
        findings.append(_finding(FindingSeverity.ERROR, "response.coverage.request_mismatch", "Provider coverage does not match the requested signal set."))
    if not set(coverage.returned_signals).issubset(coverage.requested_signals):
        findings.append(_finding(FindingSeverity.ERROR, "response.coverage.unrequested_signal", "Provider coverage contains a signal that was not requested."))
    if not set(coverage.missing_expected_signals).issubset(coverage.requested_signals):
        findings.append(_finding(FindingSeverity.ERROR, "response.coverage.unexpected_missing_signal", "Provider coverage marks an unrequested signal as missing."))
    if set(coverage.returned_signals).intersection(coverage.missing_expected_signals):
        findings.append(_finding(FindingSeverity.ERROR, "response.coverage.contradictory", "Returned and missing signal sets overlap."))
    if len(response.signals) > MAX_SIGNALS or len(response.limitations) > MAX_LIMITATIONS or len(response.warnings) > MAX_WARNINGS:
        findings.append(_finding(FindingSeverity.ERROR, "response.resource_limit.exceeded", "Provider response exceeds a bounded collection limit."))
    signal_names = tuple(sorted(signal.signal_name for signal in response.signals))
    if len(signal_names) != len(set(signal_names)) or signal_names != coverage.returned_signals:
        findings.append(_finding(FindingSeverity.ERROR, "response.signals.invalid", "Provider response signals must be unique and agree with coverage."))
    for signal in response.signals:
        contract = SIGNAL_CONTRACTS.get(signal.signal_name)
        if contract is None:
            findings.append(_finding(FindingSeverity.ERROR, "response.signal.unsupported", "Provider response contains an unsupported canonical signal."))
            continue
        value_type, unit, allowed_values, window_required = contract
        if signal.value_type != value_type or signal.unit != unit or (allowed_values is not None and signal.value not in allowed_values):
            findings.append(_finding(FindingSeverity.ERROR, "response.signal.contract_invalid", f"Provider signal violates the canonical contract: {signal.signal_name}."))
        if value_type == "integer" and (not isinstance(signal.value, int) or isinstance(signal.value, bool)):
            findings.append(_finding(FindingSeverity.ERROR, "response.signal.value_type_invalid", f"Provider signal value must be an integer: {signal.signal_name}."))
        if value_type == "decimal" and (not isinstance(signal.value, (int, float)) or isinstance(signal.value, bool)):
            findings.append(_finding(FindingSeverity.ERROR, "response.signal.value_type_invalid", f"Provider signal value must be numeric: {signal.signal_name}."))
        if value_type == "string" and not isinstance(signal.value, str):
            findings.append(_finding(FindingSeverity.ERROR, "response.signal.value_type_invalid", f"Provider signal value must be a string: {signal.signal_name}."))
        if window_required and (signal.observation_window_start is None or signal.observation_window_end is None):
            findings.append(_finding(FindingSeverity.ERROR, "response.signal.window_required", f"Provider signal requires a bounded observation window: {signal.signal_name}."))
        if signal.observation_window_start is not None and signal.observation_window_end is not None and not _time_order(signal.observation_window_start, signal.observation_window_end):
            findings.append(_finding(FindingSeverity.ERROR, "response.signal.window_invalid", f"Provider signal observation window is invalid: {signal.signal_name}."))
        if not is_valid_timestamp(signal.observed_at):
            findings.append(_finding(FindingSeverity.ERROR, "response.signal.timestamp_invalid", f"Provider signal timestamp is invalid: {signal.signal_name}."))
    for limitation in response.limitations:
        findings.extend(validate_limitation(limitation))
    if not response.provider_confidence_reasons or not _ordered(response.provider_confidence_reasons) or not _ordered(response.warnings):
        findings.append(_finding(FindingSeverity.ERROR, "response.reason_order.invalid", "Provider confidence reasons and warnings must be deterministic."))
    if contains_secret_like_content(json.dumps(response_to_primitive(response), sort_keys=True)):
        findings.append(_finding(FindingSeverity.ERROR, "response.secret_like_content", "Provider response contains secret-like content."))
    return tuple(findings)


def validate_failure(failure: ProviderFailure) -> tuple[ProviderFinding, ...]:
    findings: list[ProviderFinding] = []
    if failure.contract_version != CONTRACT_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "failure.contract_version.unsupported", "Provider failure contract version is unsupported."))
    if not failure.fixture_only or failure.activation_status != ACTIVATION_STATUS:
        findings.append(_finding(FindingSeverity.ERROR, "failure.repository_scope.required", "Provider failure must remain fixture-only and not activated."))
    for field_name in ("request_id", "failure_code", "safe_message", "audit_correlation_id"):
        if _blank(getattr(failure, field_name)):
            findings.append(_finding(FindingSeverity.ERROR, f"failure.{field_name}.required", f"Provider failure {field_name} is required."))
    if not _ordered(failure.affected_signals) or len(failure.limitations) > MAX_LIMITATIONS:
        findings.append(_finding(FindingSeverity.ERROR, "failure.collections.invalid", "Provider failure collections must be bounded, unique, and sorted."))
    if not _time_order(failure.collection_started_at, failure.failed_at):
        findings.append(_finding(FindingSeverity.ERROR, "failure.time.invalid", "Provider failure timestamps are invalid or out of order."))
    for limitation in failure.limitations:
        findings.extend(validate_limitation(limitation))
    if contains_secret_like_content(json.dumps(failure_to_primitive(failure), sort_keys=True)):
        findings.append(_finding(FindingSeverity.ERROR, "failure.secret_like_content", "Provider failure contains secret-like content."))
    return tuple(findings)


def validate_result(result: ProviderResult) -> tuple[ProviderFinding, ...]:
    findings: list[ProviderFinding] = []
    if result.contract_version != CONTRACT_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "result.contract_version.unsupported", "Provider result contract version is unsupported."))
    if (result.observation_result is None) == (result.failure_result is None):
        findings.append(_finding(FindingSeverity.ERROR, "result.exactly_one.required", "Provider result must contain exactly one observation or failure result."))
    if result.failure_result is not None:
        findings.extend(validate_failure(result.failure_result))
    return tuple(findings)


def _failure(
    request: ProviderRequest,
    category: ProviderFailureCategory,
    code: str,
    message: str,
    availability: ProviderAvailability,
    target_resolution: TargetResolution | None = None,
    retryability: Retryability = Retryability.NOT_RETRYABLE,
    limitations: tuple[ProviderLimitation, ...] = (),
) -> ProviderFailure:
    return ProviderFailure(
        CONTRACT_VERSION,
        request.request_id,
        category,
        code,
        message,
        retryability,
        request.requested_signals(),
        availability,
        target_resolution,
        request.requested_at,
        request.requested_at,
        limitations,
        _stable_id("provider-audit", {"request": request.request_id, "category": category.value, "code": code}),
        True,
        ACTIVATION_STATUS,
    )


def failure_for_scenario(request: ProviderRequest, scenario: MockScenario) -> ProviderFailure:
    mapping = {
        MockScenario.PROVIDER_UNAVAILABLE: (ProviderFailureCategory.PROVIDER_UNAVAILABLE, "PROVIDER_UNAVAILABLE", "Repository mock provider is unavailable.", ProviderAvailability.UNAVAILABLE, None, Retryability.RETRYABLE_WITHIN_WINDOW),
        MockScenario.TIMEOUT: (ProviderFailureCategory.PROVIDER_TIMEOUT, "PROVIDER_TIMEOUT", "Repository mock provider collection timed out.", ProviderAvailability.UNKNOWN, None, Retryability.RETRYABLE_WITHIN_WINDOW),
        MockScenario.AUTHORIZATION_DENIED: (ProviderFailureCategory.PROVIDER_AUTHORIZATION_FAILURE, "AUTHORIZATION_DENIED", "Repository fixture authorization was denied.", ProviderAvailability.UNKNOWN, None, Retryability.NEW_AUTHORIZATION_REQUIRED),
        MockScenario.UNSUPPORTED_PROVIDER_VERSION: (ProviderFailureCategory.PROVIDER_VERSION_MISMATCH, "PROVIDER_VERSION_UNSUPPORTED", "Repository fixture provider version is unsupported.", ProviderAvailability.AVAILABLE, None, Retryability.NOT_RETRYABLE),
        MockScenario.MALFORMED_PAYLOAD: (ProviderFailureCategory.MALFORMED_RESPONSE, "RESPONSE_MALFORMED", "Repository fixture response is malformed.", ProviderAvailability.AVAILABLE, None, Retryability.NOT_RETRYABLE),
        MockScenario.PARTIAL_RESPONSE: (ProviderFailureCategory.PARTIAL_RESPONSE, "PARTIAL_RESPONSE", "Repository fixture response is partial.", ProviderAvailability.DEGRADED, TargetResolution.EXACT, Retryability.NOT_RETRYABLE),
        MockScenario.MISSING_MANDATORY_SIGNALS: (ProviderFailureCategory.SIGNAL_UNAVAILABLE, "MANDATORY_SIGNAL_MISSING", "Repository fixture omitted a mandatory signal.", ProviderAvailability.AVAILABLE, TargetResolution.EXACT, Retryability.NOT_RETRYABLE),
        MockScenario.CONFLICTING_IDENTITY: (ProviderFailureCategory.AMBIGUOUS_TARGET, "IDENTITY_CONFLICT", "Repository fixture identity conflicts with the authorized synthetic target.", ProviderAvailability.AVAILABLE, TargetResolution.CONFLICTING, Retryability.NEW_AUTHORIZATION_REQUIRED),
        MockScenario.UNKNOWN_TARGET: (ProviderFailureCategory.UNKNOWN_TARGET, "TARGET_UNKNOWN", "Repository fixture target is unknown.", ProviderAvailability.AVAILABLE, TargetResolution.ABSENT, Retryability.NEW_AUTHORIZATION_REQUIRED),
        MockScenario.DUPLICATE_TARGETS: (ProviderFailureCategory.DUPLICATE_TARGET, "TARGET_DUPLICATE", "Repository fixture returned duplicate targets.", ProviderAvailability.AVAILABLE, TargetResolution.DUPLICATE, Retryability.NEW_AUTHORIZATION_REQUIRED),
        MockScenario.PROVIDER_LIMITATION: (ProviderFailureCategory.PROVIDER_LIMITATION, "PROVIDER_LIMITATION", "Repository fixture provider limitation affects mandatory evidence.", ProviderAvailability.DEGRADED, TargetResolution.EXACT, Retryability.NOT_RETRYABLE),
        MockScenario.CAPABILITY_MISMATCH: (ProviderFailureCategory.CAPABILITY_UNSUPPORTED, "CAPABILITY_MISMATCH", "Repository fixture capability does not support the request.", ProviderAvailability.AVAILABLE, None, Retryability.NOT_RETRYABLE),
        MockScenario.LARGE_PAYLOAD_REJECTION: (ProviderFailureCategory.RESPONSE_OVERSIZED, "RESPONSE_OVERSIZED", "Repository fixture response exceeds the payload limit.", ProviderAvailability.AVAILABLE, None, Retryability.NOT_RETRYABLE),
    }
    if scenario == MockScenario.HEALTHY:
        raise ProviderAdapterDataError("Healthy mock scenario does not produce a failure.")
    category, code, message, availability, resolution, retryability = mapping[scenario]
    limitations: tuple[ProviderLimitation, ...] = ()
    if scenario == MockScenario.PROVIDER_LIMITATION:
        limitations = (ProviderLimitation("mandatory_identity_limited", request.mandatory_signal_set.signals, True, f"{FIXTURE_ROOT}/provider-capability.json"),)
    return _failure(request, category, code, message, availability, resolution, retryability, limitations)


def _evidence_type(signal_name: str) -> str:
    if signal_name.startswith("container.lifecycle"):
        return "lifecycle"
    if signal_name.startswith("container.healthcheck"):
        return "runtime_healthcheck"
    if signal_name.startswith("container.restart"):
        return "restart"
    if signal_name.startswith("container.cpu") or signal_name.startswith("container.memory"):
        return "resource_pressure"
    return "telemetry_availability"


def normalize_response(request: ProviderRequest, response: ProviderResponse) -> ProviderNormalizationResult:
    findings = list(validate_response(response, request))
    errors = [finding for finding in findings if finding.severity == FindingSeverity.ERROR]
    if errors:
        failure = _failure(
            request,
            ProviderFailureCategory.INTERNAL_ADAPTER_VALIDATION_FAILURE,
            "RESPONSE_VALIDATION_FAILED",
            "Repository provider response failed strict validation.",
            ProviderAvailability.UNKNOWN,
            response.observed_identity.target_resolution_result,
        )
        return ProviderNormalizationResult(CONTRACT_VERSION, (), failure, response.limitations, response.coverage, response.coverage.unknown_signals, tuple(findings))
    resolution = response.observed_identity.target_resolution_result
    if resolution != TargetResolution.EXACT:
        category = ProviderFailureCategory.UNKNOWN_TARGET if resolution == TargetResolution.ABSENT else ProviderFailureCategory.AMBIGUOUS_TARGET
        failure = _failure(request, category, "TARGET_NOT_EXACT", "Repository provider response did not resolve the synthetic target exactly.", ProviderAvailability.AVAILABLE, resolution)
        return ProviderNormalizationResult(CONTRACT_VERSION, (), failure, response.limitations, response.coverage, response.coverage.unknown_signals, tuple(findings))
    missing_mandatory = tuple(sorted(set(request.mandatory_signal_set.signals).difference(response.coverage.returned_signals)))
    material_limitations = tuple(limitation for limitation in response.limitations if limitation.material and set(limitation.affected_signals).intersection(request.mandatory_signal_set.signals))
    if missing_mandatory or material_limitations:
        category = ProviderFailureCategory.SIGNAL_UNAVAILABLE if missing_mandatory else ProviderFailureCategory.PROVIDER_LIMITATION
        code = "MANDATORY_SIGNAL_MISSING" if missing_mandatory else "MATERIAL_PROVIDER_LIMITATION"
        message = "Repository provider response cannot satisfy the mandatory synthetic signal set."
        failure = _failure(request, category, code, message, ProviderAvailability.DEGRADED, resolution, limitations=material_limitations)
        return ProviderNormalizationResult(CONTRACT_VERSION, (), failure, response.limitations, response.coverage, response.coverage.unknown_signals, tuple(findings))
    identity = response.observed_identity
    context = request.authorization_context
    confidence = {
        ProviderConfidence.HIGH: Confidence.HIGH,
        ProviderConfidence.MEDIUM: Confidence.MEDIUM,
        ProviderConfidence.LOW: Confidence.LOW,
        ProviderConfidence.NONE: Confidence.NONE,
    }[response.provider_confidence]
    limitation_codes = tuple(sorted(limitation.limitation_code for limitation in response.limitations))
    evidence_records: list[OperationalEvidence] = []
    for index, signal in enumerate(response.signals):
        window_required = SIGNAL_CONTRACTS[signal.signal_name][3]
        complete = not window_required or (signal.observation_window_start is not None and signal.observation_window_end is not None)
        required_attributes = tuple(sorted(("host_reference", "observed_at", "provider_provenance", "registry_reference", "source_reference", "subject_id")))
        payload = {
            "request_id": request.request_id,
            "observation_id": response.metadata.provider_observation_id,
            "signal": signal.signal_name,
            "value": signal.value,
            "index": index,
        }
        evidence = OperationalEvidence(
            "1.0",
            "container",
            "1.0",
            _stable_id("evidence", payload),
            context.subject_id,
            "container_service",
            context.registry_reference,
            "test",
            _evidence_type(signal.signal_name),
            signal.signal_name,
            signal.value,
            signal.value_type,
            signal.unit,
            signal.observed_at,
            response.metadata.collection_ended_at,
            response.metadata.collection_ended_at,
            signal.observation_window_start,
            signal.observation_window_end,
            response.provenance.provider_type,
            response.provenance.provider_id,
            response.provenance.provider_version,
            response.provenance.adapter_version,
            response.provenance.fixture_reference,
            identity.runtime_container_id,
            IdentityMatchMethod.SUBJECT_AND_REGISTRY_REFERENCE,
            signal.collection_method,
            FreshnessStatus.CURRENT,
            "container-lifecycle-freshness:1.0" if not signal.signal_name.startswith("container.healthcheck") else "container-healthcheck-freshness:1.0",
            60,
            0,
            CompletenessStatus.COMPLETE if complete else CompletenessStatus.MISSING_REQUIRED_ATTRIBUTES,
            required_attributes,
            () if complete else ("observation_window",),
            response.metadata.provider_observation_id,
            confidence,
            response.provider_confidence_reasons,
            limitation_codes,
            context.registry_reference,
            context.host_reference,
            identity.runtime_name,
            identity.runtime_container_id,
            identity.runtime_engine,
            identity.orchestrator,
        )
        evidence_findings = validate_evidence(evidence)
        findings.extend(
            _finding(FindingSeverity.ERROR if item.severity.value == "ERROR" else FindingSeverity.WARNING, item.code, item.message, item.reference)
            for item in evidence_findings
        )
        if not any(item.severity.value == "ERROR" for item in evidence_findings):
            evidence_records.append(evidence)
    if any(finding.severity == FindingSeverity.ERROR for finding in findings):
        failure = _failure(request, ProviderFailureCategory.INTERNAL_ADAPTER_VALIDATION_FAILURE, "NORMALIZATION_VALIDATION_FAILED", "Canonical evidence failed strict validation.", ProviderAvailability.UNKNOWN, resolution)
        return ProviderNormalizationResult(CONTRACT_VERSION, (), failure, response.limitations, response.coverage, response.coverage.unknown_signals, tuple(findings))
    return ProviderNormalizationResult(
        CONTRACT_VERSION,
        tuple(sorted(evidence_records, key=lambda item: item.evidence_id)),
        None,
        response.limitations,
        response.coverage,
        response.coverage.unknown_signals,
        tuple(findings),
    )


def context_to_primitive(context: AuthorizationContext) -> dict[str, object]:
    return {field: (value.value if isinstance(value, Enum) else value) for field, value in context.__dict__.items()}


def response_to_primitive(response: ProviderResponse) -> dict[str, object]:
    def convert(value: object) -> object:
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, tuple):
            return [convert(item) for item in value]
        if hasattr(value, "__dataclass_fields__"):
            return {field: convert(item) for field, item in value.__dict__.items()}
        return value

    return convert(response)  # type: ignore[return-value]


def failure_to_primitive(failure: ProviderFailure) -> dict[str, object]:
    return response_to_primitive(failure)  # type: ignore[arg-type]


class ProductionProviderAdapter(ABC):
    @abstractmethod
    def initialize(self) -> tuple[ProviderFinding, ...]:
        """Initialize repository-local state without contacting a provider."""

    @abstractmethod
    def validate_configuration(self) -> tuple[ProviderFinding, ...]:
        """Validate immutable repository configuration."""

    @abstractmethod
    def validate_authorization(self, request: ProviderRequest) -> tuple[ProviderFinding, ...]:
        """Validate a fixture-only authorization context."""

    @abstractmethod
    def discover_capabilities(self) -> ProviderCapabilityDeclaration:
        """Return a static repository capability declaration."""

    @abstractmethod
    def collect_observation(self, request: ProviderRequest) -> ProviderResult:
        """Collect only from a deterministic repository fixture client."""

    @abstractmethod
    def normalize(self, request: ProviderRequest, response: ProviderResponse) -> ProviderNormalizationResult:
        """Normalize a strict provider response without health evaluation."""

    @abstractmethod
    def shutdown(self) -> tuple[ProviderFinding, ...]:
        """Release repository-local state without live side effects."""


class UnavailableProviderAdapter(ProductionProviderAdapter):
    def initialize(self) -> tuple[ProviderFinding, ...]:
        return (_finding(FindingSeverity.INFO, "adapter.initialized.repository_only", "Repository-only unavailable adapter initialized without live access."),)

    def validate_configuration(self) -> tuple[ProviderFinding, ...]:
        return tuple((*validate_adapter_identity(repository_adapter_identity()), *validate_capability(repository_capability())))

    def validate_authorization(self, request: ProviderRequest) -> tuple[ProviderFinding, ...]:
        return validate_request(request)

    def discover_capabilities(self) -> ProviderCapabilityDeclaration:
        return repository_capability()

    def collect_observation(self, request: ProviderRequest) -> ProviderResult:
        findings = validate_request(request)
        if any(finding.severity == FindingSeverity.ERROR for finding in findings):
            failure = _failure(request, ProviderFailureCategory.CONFIGURATION_INVALID, "REQUEST_INVALID", "Repository provider request is invalid.", ProviderAvailability.UNKNOWN)
        else:
            failure = _failure(request, ProviderFailureCategory.PROVIDER_UNAVAILABLE, "PROVIDER_NOT_IMPLEMENTED", "No live provider implementation exists in the repository foundation.", ProviderAvailability.UNAVAILABLE)
        return ProviderResult(CONTRACT_VERSION, None, failure)

    def normalize(self, request: ProviderRequest, response: ProviderResponse) -> ProviderNormalizationResult:
        return normalize_response(request, response)

    def shutdown(self) -> tuple[ProviderFinding, ...]:
        return (_finding(FindingSeverity.INFO, "adapter.shutdown.repository_only", "Repository-only unavailable adapter shut down without live access."),)
