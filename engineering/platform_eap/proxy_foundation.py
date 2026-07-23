from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
from typing import Mapping, Sequence


CONTRACT_VERSION = "1.0"
PROXY_VERSION = "repository-constrained-proxy-v1.0"
POLICY_VERSION = "constrained-proxy-policy-v1.0"
CONFIGURATION_VERSION = "constrained-proxy-configuration-v1.0"
CAPABILITY_VERSION = "constrained-proxy-capability-v1.0"
ADAPTER_VERSION = "repository-provider-adapter-foundation-v1.0"
ACTIVATION_STATUS = "not_activated"
FIXTURE_ROOT = "engineering/tests/fixtures/proxy_foundation"
MAX_REQUEST_PAYLOAD_BYTES = 16_384
MAX_RESPONSE_PAYLOAD_BYTES = 65_536
MAX_RESPONSE_RECORDS = 64
MAX_PARAMETERS = 16


class ProxyDataError(ValueError):
    """Raised when untrusted proxy fixture data is malformed."""


class UnsupportedProxyContractVersion(ProxyDataError):
    """Raised when a proxy contract version is unsupported."""


class FindingSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class ProxyEndpointCategory(str, Enum):
    IDENTITY_DISCOVERY = "IdentityDiscovery"
    LIFECYCLE_OBSERVATION = "LifecycleObservation"
    HEALTH_OBSERVATION = "HealthObservation"
    RESTART_INFORMATION = "RestartInformation"
    STATISTICS = "Statistics"
    EVENTS = "Events"
    IMAGES = "Images"
    VOLUMES = "Volumes"
    NETWORKS = "Networks"
    BUILD = "Build"
    EXEC = "Exec"
    ARCHIVE = "Archive"
    FILESYSTEM = "Filesystem"
    SECRETS = "Secrets"
    PLUGINS = "Plugins"
    SWARM = "Swarm"
    SYSTEM = "System"
    CONFIGURATION = "Configuration"


class ProxyMethodCategory(str, Enum):
    READ_ONLY = "ReadOnly"
    BOUNDED_ACTION = "BoundedAction"
    MUTATING = "Mutating"
    STREAMING = "Streaming"


class ProxyPolicyState(str, Enum):
    ALLOWED = "Allowed"
    CONDITIONALLY_ALLOWED = "ConditionallyAllowed"
    DENIED = "Denied"
    FUTURE = "Future"


class ProxyDecisionStatus(str, Enum):
    ALLOWED = "Allowed"
    DENIED = "Denied"
    FUTURE = "Future"
    UNAUTHORIZED = "Unauthorized"
    UNSUPPORTED_CATEGORY = "UnsupportedCategory"
    UNSUPPORTED_METHOD = "UnsupportedMethod"
    INVALID_TARGET = "InvalidTarget"
    INVALID_POLICY = "InvalidPolicy"
    INVALID_CONFIGURATION = "InvalidConfiguration"
    EXPIRED_AUTHORIZATION = "ExpiredAuthorization"
    PAYLOAD_TOO_LARGE = "PayloadTooLarge"
    RESPONSE_REJECTED = "ResponseRejected"


class ProxyAuthenticationMode(str, Enum):
    LOCAL_UNIX_IDENTITY = "LocalUnixIdentity"
    MUTUAL_TLS = "MutualTLS"
    SERVICE_IDENTITY = "ServiceIdentity"
    ADMINISTRATOR_AUTHORIZATION = "AdministratorAuthorization"
    NAMED_TARGET_AUTHORIZATION = "NamedTargetAuthorization"


@dataclass(frozen=True)
class ProxyFinding:
    severity: FindingSeverity
    code: str
    message: str
    reference: str | None = None


@dataclass(frozen=True)
class ProxyIdentity:
    contract_version: str
    proxy_id: str
    proxy_version: str
    policy_version: str
    configuration_version: str
    fixture_only: bool
    activation_status: str


@dataclass(frozen=True)
class ProxyAuthenticationContext:
    contract_version: str
    mode: ProxyAuthenticationMode
    principal_id: str
    service_identity: str
    authenticated: bool
    fixture_only: bool


@dataclass(frozen=True)
class ProxyAuthorizationContext:
    contract_version: str
    authorization_reference: str
    authorization_digest: str
    approval_reference: str
    registry_subject_reference: str
    subject_id: str
    configuration_digest: str
    proxy_version: str
    adapter_version: str
    policy_version: str
    approved_endpoint_categories: tuple[ProxyEndpointCategory, ...]
    approved_signal_set: tuple[str, ...]
    observation_window_start: str
    observation_window_end: str
    expires_at: str
    fixture_only: bool


@dataclass(frozen=True)
class ProxyTarget:
    contract_version: str
    subject_id: str
    registry_subject_reference: str
    host_reference: str
    environment: str
    fixture_only: bool


@dataclass(frozen=True)
class ProxyParameter:
    contract_version: str
    name: str
    value: str


@dataclass(frozen=True)
class ProxyRequest:
    contract_version: str
    request_id: str
    requested_at: str
    endpoint_category: ProxyEndpointCategory
    method_category: ProxyMethodCategory
    target: ProxyTarget
    authentication: ProxyAuthenticationContext
    authorization: ProxyAuthorizationContext
    requested_signals: tuple[str, ...]
    parameters: tuple[ProxyParameter, ...]
    payload_size_bytes: int
    proxy_version: str
    adapter_version: str
    policy_version: str
    configuration_version: str


@dataclass(frozen=True)
class ProxyPolicyEntry:
    contract_version: str
    endpoint_category: ProxyEndpointCategory
    state: ProxyPolicyState
    allowed_methods: tuple[ProxyMethodCategory, ...]


@dataclass(frozen=True)
class ProxyPolicy:
    contract_version: str
    policy_version: str
    policy_digest: str
    entries: tuple[ProxyPolicyEntry, ...]
    default_state: ProxyPolicyState
    fixture_only: bool


@dataclass(frozen=True)
class ProxyConfiguration:
    contract_version: str
    configuration_version: str
    configuration_digest: str
    maximum_request_payload_bytes: int
    maximum_response_payload_bytes: int
    maximum_response_records: int
    require_authentication: bool
    require_exact_target: bool
    allow_streaming: bool
    allow_networking: bool
    allow_runtime_access: bool
    fixture_only: bool
    activation_status: str


@dataclass(frozen=True)
class ProxyCapabilityDeclaration:
    contract_version: str
    capability_version: str
    proxy_version: str
    adapter_version: str
    policy_version: str
    configuration_version: str
    supported_endpoint_categories: tuple[ProxyEndpointCategory, ...]
    supported_method_categories: tuple[ProxyMethodCategory, ...]
    supported_authentication_modes: tuple[ProxyAuthenticationMode, ...]
    fixture_only: bool
    live_access_supported: bool
    networking_supported: bool
    socket_access_supported: bool


@dataclass(frozen=True)
class ProxyDecision:
    contract_version: str
    request_id: str
    decision: ProxyDecisionStatus
    decision_code: str
    safe_message: str
    policy_state: ProxyPolicyState | None
    policy_version: str
    configuration_version: str
    authorization_reference: str | None
    target_subject_id: str | None
    audit_correlation_id: str


@dataclass(frozen=True)
class ProxyResponseMetadata:
    contract_version: str
    request_id: str
    response_id: str
    observed_at: str
    completed_at: str
    target_subject_id: str
    registry_subject_reference: str
    proxy_version: str
    adapter_version: str
    policy_version: str
    configuration_version: str
    provenance_reference: str
    limitation_codes: tuple[str, ...]
    fixture_only: bool


@dataclass(frozen=True)
class ProxyResponseRecord:
    contract_version: str
    signal_name: str
    value: str | int | float | bool
    observed_at: str


@dataclass(frozen=True)
class ProxyResponse:
    contract_version: str
    metadata: ProxyResponseMetadata
    records: tuple[ProxyResponseRecord, ...]
    payload_size_bytes: int


@dataclass(frozen=True)
class ProxyFailure:
    contract_version: str
    request_id: str
    decision: ProxyDecisionStatus
    failure_code: str
    safe_message: str
    audit_correlation_id: str
    target_subject_id: str | None
    fixture_only: bool


@dataclass(frozen=True)
class ProxyAuditEvent:
    contract_version: str
    audit_correlation_id: str
    request_id: str
    decision: ProxyDecisionStatus
    endpoint_category: ProxyEndpointCategory
    method_category: ProxyMethodCategory
    subject_id: str
    authorization_reference: str
    recorded_at: str
    fixture_only: bool


@dataclass(frozen=True)
class MockProxyResult:
    contract_version: str
    decision: ProxyDecision
    response: ProxyResponse | None
    failure: ProxyFailure | None
    audit_event: ProxyAuditEvent


def primitive(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [primitive(item) for item in value]
    if hasattr(value, "__dataclass_fields__"):
        return {name: primitive(item) for name, item in value.__dict__.items()}
    return value


def canonical_json(value: object) -> str:
    return json.dumps(primitive(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def deterministic_json(value: object) -> str:
    return json.dumps(primitive(value), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def canonical_digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _without_digest(value: object, field_name: str) -> Mapping[str, object]:
    payload = primitive(value)
    assert isinstance(payload, Mapping)
    return {key: item for key, item in payload.items() if key != field_name}


def policy_digest(policy: ProxyPolicy) -> str:
    return canonical_digest(_without_digest(policy, "policy_digest"))


def configuration_digest(configuration: ProxyConfiguration) -> str:
    return canonical_digest(_without_digest(configuration, "configuration_digest"))


def authorization_digest(authorization: ProxyAuthorizationContext) -> str:
    return canonical_digest(_without_digest(authorization, "authorization_digest"))


def _finding(code: str, message: str, reference: str | None = None) -> ProxyFinding:
    return ProxyFinding(FindingSeverity.ERROR, code, message, reference)


def _valid_timestamp(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None
    except (TypeError, ValueError):
        return False


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _ordered_unique(values: Sequence[object]) -> bool:
    rendered = [item.value if isinstance(item, Enum) else str(item) for item in values]
    return bool(rendered) and rendered == sorted(set(rendered))


def _valid_digest(value: str) -> bool:
    return len(value) == 71 and value.startswith("sha256:") and all(char in "0123456789abcdef" for char in value[7:])


def repository_policy() -> ProxyPolicy:
    states = {
        ProxyEndpointCategory.IDENTITY_DISCOVERY: ProxyPolicyState.CONDITIONALLY_ALLOWED,
        ProxyEndpointCategory.LIFECYCLE_OBSERVATION: ProxyPolicyState.ALLOWED,
        ProxyEndpointCategory.HEALTH_OBSERVATION: ProxyPolicyState.ALLOWED,
        ProxyEndpointCategory.RESTART_INFORMATION: ProxyPolicyState.ALLOWED,
        ProxyEndpointCategory.STATISTICS: ProxyPolicyState.CONDITIONALLY_ALLOWED,
        ProxyEndpointCategory.EVENTS: ProxyPolicyState.FUTURE,
    }
    entries = tuple(
        ProxyPolicyEntry(
            CONTRACT_VERSION,
            category,
            states.get(category, ProxyPolicyState.DENIED),
            (ProxyMethodCategory.READ_ONLY,) if states.get(category, ProxyPolicyState.DENIED) in {ProxyPolicyState.ALLOWED, ProxyPolicyState.CONDITIONALLY_ALLOWED} else (),
        )
        for category in ProxyEndpointCategory
    )
    draft = ProxyPolicy(CONTRACT_VERSION, POLICY_VERSION, "", entries, ProxyPolicyState.DENIED, True)
    return replace(draft, policy_digest=policy_digest(draft))


def repository_configuration() -> ProxyConfiguration:
    draft = ProxyConfiguration(
        CONTRACT_VERSION,
        CONFIGURATION_VERSION,
        "",
        MAX_REQUEST_PAYLOAD_BYTES,
        MAX_RESPONSE_PAYLOAD_BYTES,
        MAX_RESPONSE_RECORDS,
        True,
        True,
        False,
        False,
        False,
        True,
        ACTIVATION_STATUS,
    )
    return replace(draft, configuration_digest=configuration_digest(draft))


def repository_identity() -> ProxyIdentity:
    return ProxyIdentity(CONTRACT_VERSION, "repository-constrained-proxy", PROXY_VERSION, POLICY_VERSION, CONFIGURATION_VERSION, True, ACTIVATION_STATUS)


def repository_capability() -> ProxyCapabilityDeclaration:
    return ProxyCapabilityDeclaration(
        CONTRACT_VERSION,
        CAPABILITY_VERSION,
        PROXY_VERSION,
        ADAPTER_VERSION,
        POLICY_VERSION,
        CONFIGURATION_VERSION,
        tuple(ProxyEndpointCategory),
        (ProxyMethodCategory.READ_ONLY,),
        (ProxyAuthenticationMode.SERVICE_IDENTITY,),
        True,
        False,
        False,
        False,
    )


def validate_policy(policy: ProxyPolicy) -> tuple[ProxyFinding, ...]:
    findings: list[ProxyFinding] = []
    if policy.contract_version != CONTRACT_VERSION or policy.policy_version != POLICY_VERSION:
        findings.append(_finding("policy.version.unsupported", "Policy contract or policy version is unsupported."))
    if policy.policy_digest != policy_digest(policy) or not _valid_digest(policy.policy_digest):
        findings.append(_finding("policy.digest.mismatch", "Policy digest does not match canonical policy content."))
    categories = tuple(entry.endpoint_category for entry in policy.entries)
    if set(categories) != set(ProxyEndpointCategory) or len(categories) != len(set(categories)):
        findings.append(_finding("policy.category_matrix.invalid", "Policy must declare each endpoint category exactly once."))
    if policy.default_state != ProxyPolicyState.DENIED:
        findings.append(_finding("policy.default_deny.required", "Policy default state must be Denied."))
    if not policy.fixture_only:
        findings.append(_finding("policy.repository_scope.required", "Policy must remain fixture-only."))
    for entry in policy.entries:
        if entry.contract_version != CONTRACT_VERSION:
            findings.append(_finding("policy.entry.version.unsupported", "Policy entry contract version is unsupported."))
        if entry.state in {ProxyPolicyState.ALLOWED, ProxyPolicyState.CONDITIONALLY_ALLOWED}:
            if entry.allowed_methods != (ProxyMethodCategory.READ_ONLY,):
                findings.append(_finding("policy.method.invalid", "Allowed policy entries must expose only ReadOnly."))
        elif entry.allowed_methods:
            findings.append(_finding("policy.method.prohibited", "Denied and Future policy entries cannot expose methods."))
    return tuple(findings)


def validate_configuration(configuration: ProxyConfiguration) -> tuple[ProxyFinding, ...]:
    findings: list[ProxyFinding] = []
    if configuration.contract_version != CONTRACT_VERSION or configuration.configuration_version != CONFIGURATION_VERSION:
        findings.append(_finding("configuration.version.unsupported", "Configuration contract or version is unsupported."))
    if configuration.configuration_digest != configuration_digest(configuration) or not _valid_digest(configuration.configuration_digest):
        findings.append(_finding("configuration.digest.mismatch", "Configuration digest does not match canonical configuration content."))
    if (configuration.maximum_request_payload_bytes, configuration.maximum_response_payload_bytes, configuration.maximum_response_records) != (
        MAX_REQUEST_PAYLOAD_BYTES,
        MAX_RESPONSE_PAYLOAD_BYTES,
        MAX_RESPONSE_RECORDS,
    ):
        findings.append(_finding("configuration.bounds.invalid", "Repository configuration must use governed request, response, and record bounds."))
    if not configuration.require_authentication or not configuration.require_exact_target:
        findings.append(_finding("configuration.fail_closed.required", "Authentication and exact-target enforcement are required."))
    if configuration.allow_streaming or configuration.allow_networking or configuration.allow_runtime_access:
        findings.append(_finding("configuration.privileged_capability.prohibited", "Streaming, networking, and runtime access must remain disabled."))
    if not configuration.fixture_only or configuration.activation_status != ACTIVATION_STATUS:
        findings.append(_finding("configuration.repository_scope.required", "Configuration must remain fixture-only and not activated."))
    return tuple(findings)


def validate_capability(capability: ProxyCapabilityDeclaration) -> tuple[ProxyFinding, ...]:
    findings: list[ProxyFinding] = []
    expected_versions = (CONTRACT_VERSION, CAPABILITY_VERSION, PROXY_VERSION, ADAPTER_VERSION, POLICY_VERSION, CONFIGURATION_VERSION)
    actual_versions = (capability.contract_version, capability.capability_version, capability.proxy_version, capability.adapter_version, capability.policy_version, capability.configuration_version)
    if actual_versions != expected_versions:
        findings.append(_finding("capability.version.unsupported", "Capability versions do not match the repository foundation."))
    if set(capability.supported_endpoint_categories) != set(ProxyEndpointCategory):
        findings.append(_finding("capability.category.invalid", "Capability must classify every endpoint category."))
    if capability.supported_method_categories != (ProxyMethodCategory.READ_ONLY,):
        findings.append(_finding("capability.method.invalid", "Capability supports only ReadOnly methods."))
    if not capability.fixture_only or capability.live_access_supported or capability.networking_supported or capability.socket_access_supported:
        findings.append(_finding("capability.live_access.prohibited", "Capability must be fixture-only with live, networking, and socket access unsupported."))
    return tuple(findings)


def validate_authentication(context: ProxyAuthenticationContext) -> tuple[ProxyFinding, ...]:
    findings: list[ProxyFinding] = []
    if context.contract_version != CONTRACT_VERSION:
        findings.append(_finding("authentication.version.unsupported", "Authentication contract version is unsupported."))
    if not context.authenticated:
        findings.append(_finding("authentication.required", "Authenticated fixture identity is required."))
    if not context.principal_id or not context.service_identity or "*" in context.principal_id or "*" in context.service_identity:
        findings.append(_finding("authentication.identity.invalid", "Authentication identity must be exact and non-wildcard."))
    if not context.fixture_only:
        findings.append(_finding("authentication.fixture_scope.required", "Authentication context must remain synthetic."))
    return tuple(findings)


def validate_target(target: ProxyTarget) -> tuple[ProxyFinding, ...]:
    findings: list[ProxyFinding] = []
    if target.contract_version != CONTRACT_VERSION:
        findings.append(_finding("target.version.unsupported", "Target contract version is unsupported."))
    if not target.subject_id or "*" in target.subject_id or not target.registry_subject_reference or "*" in target.registry_subject_reference:
        findings.append(_finding("target.exact.required", "Target must have an exact subject and Registry reference."))
    if not target.registry_subject_reference.startswith("engineering/tests/fixtures/container_health/registry/"):
        findings.append(_finding("target.registry_fixture.required", "Repository proxy targets must reference a synthetic Registry fixture."))
    if not target.host_reference or target.environment != "test" or not target.fixture_only:
        findings.append(_finding("target.fixture_scope.required", "Target must remain a synthetic test fixture."))
    return tuple(findings)


def validate_authorization(context: ProxyAuthorizationContext, request: ProxyRequest | None = None) -> tuple[ProxyFinding, ...]:
    findings: list[ProxyFinding] = []
    if context.contract_version != CONTRACT_VERSION:
        findings.append(_finding("authorization.version.unsupported", "Authorization contract version is unsupported."))
    for name in ("authorization_reference", "approval_reference", "registry_subject_reference", "subject_id"):
        value = getattr(context, name)
        if not value or "*" in value:
            findings.append(_finding(f"authorization.{name}.required", f"Authorization {name} must be exact and non-wildcard."))
    if not context.approval_reference.startswith("FIXTURE-APPROVAL-"):
        findings.append(_finding("authorization.approval.fixture_required", "Repository authorization requires an explicit synthetic approval reference."))
    if context.authorization_digest != authorization_digest(context) or not _valid_digest(context.authorization_digest):
        findings.append(_finding("authorization.digest.mismatch", "Authorization digest does not match canonical authorization content."))
    if context.configuration_digest != repository_configuration().configuration_digest:
        findings.append(_finding("authorization.configuration_digest.mismatch", "Authorization configuration digest does not match the repository configuration."))
    if (context.proxy_version, context.adapter_version, context.policy_version) != (PROXY_VERSION, ADAPTER_VERSION, POLICY_VERSION):
        findings.append(_finding("authorization.version.mismatch", "Authorization version binding is unsupported."))
    if not _ordered_unique(context.approved_endpoint_categories) or not _ordered_unique(context.approved_signal_set):
        findings.append(_finding("authorization.scope.invalid", "Approved categories and signals must be nonempty, unique, and sorted."))
    if not all(_valid_timestamp(value) for value in (context.observation_window_start, context.observation_window_end, context.expires_at)):
        findings.append(_finding("authorization.window.invalid", "Authorization window timestamps must be timezone-aware."))
    elif not (_time(context.observation_window_start) <= _time(context.observation_window_end) <= _time(context.expires_at)):
        findings.append(_finding("authorization.window.invalid", "Authorization window and expiration are inconsistent."))
    if not context.fixture_only:
        findings.append(_finding("authorization.fixture_scope.required", "Authorization must remain synthetic and repository-only."))
    if request is not None:
        if context.subject_id != request.target.subject_id or context.registry_subject_reference != request.target.registry_subject_reference:
            findings.append(_finding("authorization.target.mismatch", "Authorization does not bind the exact request target."))
        if request.endpoint_category not in context.approved_endpoint_categories or any(signal not in context.approved_signal_set for signal in request.requested_signals):
            findings.append(_finding("authorization.scope.denied", "Request category or signals exceed the authorization scope."))
        if _valid_timestamp(request.requested_at) and _valid_timestamp(context.expires_at):
            when = _time(request.requested_at)
            if when > _time(context.expires_at):
                findings.append(_finding("authorization.expired", "Authorization expired before the request."))
            if not (_time(context.observation_window_start) <= when <= _time(context.observation_window_end)):
                findings.append(_finding("authorization.observation_window.denied", "Request is outside the approved observation window."))
    return tuple(findings)


def validate_request(request: ProxyRequest) -> tuple[ProxyFinding, ...]:
    findings: list[ProxyFinding] = []
    if request.contract_version != CONTRACT_VERSION:
        findings.append(_finding("request.version.unsupported", "Request contract version is unsupported."))
    if not request.request_id or not _valid_timestamp(request.requested_at):
        findings.append(_finding("request.identity.invalid", "Request identifier and timezone-aware timestamp are required."))
    if request.payload_size_bytes < 0 or request.payload_size_bytes > MAX_REQUEST_PAYLOAD_BYTES:
        findings.append(_finding("request.payload.too_large", "Request payload exceeds the governed maximum."))
    if len(request.parameters) > MAX_PARAMETERS or len({item.name for item in request.parameters}) != len(request.parameters):
        findings.append(_finding("request.parameters.duplicate", "Request parameters must be bounded and have unique names."))
    if tuple(item.name for item in request.parameters) != tuple(sorted(item.name for item in request.parameters)):
        findings.append(_finding("request.parameters.order.invalid", "Request parameters must be deterministically sorted."))
    if not _ordered_unique(request.requested_signals):
        findings.append(_finding("request.signals.invalid", "Requested signals must be nonempty, unique, and sorted."))
    if (request.proxy_version, request.adapter_version, request.policy_version, request.configuration_version) != (PROXY_VERSION, ADAPTER_VERSION, POLICY_VERSION, CONFIGURATION_VERSION):
        findings.append(_finding("request.version_binding.invalid", "Request version binding is unsupported."))
    findings.extend(validate_target(request.target))
    findings.extend(validate_authentication(request.authentication))
    findings.extend(validate_authorization(request.authorization, request))
    return tuple(findings)


def validate_response(response: ProxyResponse, request: ProxyRequest) -> tuple[ProxyFinding, ...]:
    findings: list[ProxyFinding] = []
    if response.contract_version != CONTRACT_VERSION or response.metadata.contract_version != CONTRACT_VERSION:
        findings.append(_finding("response.version.unsupported", "Response contract version is unsupported."))
    if response.payload_size_bytes < 0 or response.payload_size_bytes > MAX_RESPONSE_PAYLOAD_BYTES:
        findings.append(_finding("response.payload.too_large", "Response payload exceeds the governed maximum."))
    if len(response.records) > MAX_RESPONSE_RECORDS:
        findings.append(_finding("response.records.too_many", "Response record count exceeds the governed maximum."))
    metadata = response.metadata
    if metadata.request_id != request.request_id or metadata.target_subject_id != request.target.subject_id or metadata.registry_subject_reference != request.target.registry_subject_reference:
        findings.append(_finding("response.identity.mismatch", "Response does not match the request and exact target identity."))
    if (metadata.proxy_version, metadata.adapter_version, metadata.policy_version, metadata.configuration_version) != (PROXY_VERSION, ADAPTER_VERSION, POLICY_VERSION, CONFIGURATION_VERSION):
        findings.append(_finding("response.version_binding.invalid", "Response version binding is unsupported."))
    if not metadata.provenance_reference.startswith(f"{FIXTURE_ROOT}/") or not metadata.fixture_only:
        findings.append(_finding("response.provenance.invalid", "Response provenance must reference a governed synthetic fixture."))
    if not _ordered_unique(metadata.limitation_codes) and metadata.limitation_codes:
        findings.append(_finding("response.limitations.invalid", "Response limitation codes must be unique and sorted."))
    if not all(_valid_timestamp(value) for value in (metadata.observed_at, metadata.completed_at)) or (_valid_timestamp(metadata.observed_at) and _valid_timestamp(metadata.completed_at) and _time(metadata.completed_at) < _time(metadata.observed_at)):
        findings.append(_finding("response.timestamps.invalid", "Response timestamps must be ordered and timezone-aware."))
    names = tuple(record.signal_name for record in response.records)
    if tuple(sorted(names)) != names or len(names) != len(set(names)) or any(name not in request.requested_signals for name in names):
        findings.append(_finding("response.records.invalid", "Response records must be unique, sorted, and requested."))
    for record in response.records:
        if record.contract_version != CONTRACT_VERSION or not _valid_timestamp(record.observed_at):
            findings.append(_finding("response.record.invalid", "Response record contract or timestamp is invalid."))
    if len(deterministic_json(response).encode("utf-8")) > MAX_RESPONSE_PAYLOAD_BYTES:
        findings.append(_finding("response.serialized_payload.too_large", "Serialized response exceeds the governed maximum."))
    return tuple(findings)


def _decision(request: ProxyRequest, status: ProxyDecisionStatus, code: str, message: str, state: ProxyPolicyState | None) -> ProxyDecision:
    return ProxyDecision(
        CONTRACT_VERSION,
        request.request_id,
        status,
        code,
        message,
        state,
        request.policy_version,
        request.configuration_version,
        request.authorization.authorization_reference if request.authorization else None,
        request.target.subject_id if request.target else None,
        "proxy-audit-" + canonical_digest({"request_id": request.request_id, "status": status.value, "code": code})[7:23],
    )


def evaluate_request(
    request: ProxyRequest,
    policy: ProxyPolicy,
    configuration: ProxyConfiguration,
    capability: ProxyCapabilityDeclaration,
) -> ProxyDecision:
    if validate_configuration(configuration):
        return _decision(request, ProxyDecisionStatus.INVALID_CONFIGURATION, "configuration_invalid", "Repository configuration is invalid.", None)
    if validate_policy(policy):
        return _decision(request, ProxyDecisionStatus.INVALID_POLICY, "policy_invalid", "Repository policy is invalid.", None)
    if validate_capability(capability):
        return _decision(request, ProxyDecisionStatus.INVALID_CONFIGURATION, "capability_invalid", "Repository capability declaration is invalid.", None)
    request_findings = validate_request(request)
    codes = {finding.code for finding in request_findings}
    if "request.payload.too_large" in codes:
        return _decision(request, ProxyDecisionStatus.PAYLOAD_TOO_LARGE, "payload_too_large", "Request payload is too large.", None)
    if "authorization.expired" in codes:
        return _decision(request, ProxyDecisionStatus.EXPIRED_AUTHORIZATION, "authorization_expired", "Authorization has expired.", None)
    if any(code.startswith("target.") or code == "authorization.target.mismatch" for code in codes):
        return _decision(request, ProxyDecisionStatus.INVALID_TARGET, "target_invalid", "Request target is invalid.", None)
    if any(code.startswith("authentication.") or code.startswith("authorization.") for code in codes):
        return _decision(request, ProxyDecisionStatus.UNAUTHORIZED, "authorization_invalid", "Request authorization is invalid.", None)
    if request_findings:
        return _decision(request, ProxyDecisionStatus.DENIED, "request_invalid", "Request validation failed closed.", None)
    if request.authentication.mode not in capability.supported_authentication_modes:
        return _decision(request, ProxyDecisionStatus.UNAUTHORIZED, "authentication_mode_unsupported", "Authentication mode is conceptual but not enabled by the repository capability.", None)
    if request.endpoint_category not in capability.supported_endpoint_categories:
        return _decision(request, ProxyDecisionStatus.UNSUPPORTED_CATEGORY, "category_unsupported", "Endpoint category is unsupported.", None)
    entry = next((item for item in policy.entries if item.endpoint_category == request.endpoint_category), None)
    if entry is None:
        return _decision(request, ProxyDecisionStatus.UNSUPPORTED_CATEGORY, "category_unclassified", "Endpoint category is not classified.", None)
    if entry.state == ProxyPolicyState.FUTURE:
        return _decision(request, ProxyDecisionStatus.FUTURE, "category_future", "Endpoint category is reserved for a future gate.", entry.state)
    if entry.state == ProxyPolicyState.DENIED:
        return _decision(request, ProxyDecisionStatus.DENIED, "category_denied", "Endpoint category is denied by default.", entry.state)
    if request.method_category not in capability.supported_method_categories or request.method_category not in entry.allowed_methods:
        return _decision(request, ProxyDecisionStatus.UNSUPPORTED_METHOD, "method_unsupported", "Method category is not allowed.", entry.state)
    return _decision(request, ProxyDecisionStatus.ALLOWED, "request_allowed", "Synthetic fixture request is allowed.", entry.state)


def decision_to_failure(request: ProxyRequest, decision: ProxyDecision) -> ProxyFailure:
    return ProxyFailure(CONTRACT_VERSION, request.request_id, decision.decision, decision.decision_code, decision.safe_message, decision.audit_correlation_id, request.target.subject_id, True)


def decision_to_audit(request: ProxyRequest, decision: ProxyDecision) -> ProxyAuditEvent:
    return ProxyAuditEvent(
        CONTRACT_VERSION,
        decision.audit_correlation_id,
        request.request_id,
        decision.decision,
        request.endpoint_category,
        request.method_category,
        request.target.subject_id,
        request.authorization.authorization_reference,
        request.requested_at,
        True,
    )


def contract_summary() -> Mapping[str, object]:
    return {
        "contract_version": CONTRACT_VERSION,
        "identity": primitive(repository_identity()),
        "capability": primitive(repository_capability()),
        "repository_only": True,
        "live_access": "absent",
        "networking": "absent",
        "socket_access": "absent",
        "deployment": "not_authorized",
        "privileged_access": "not_authorized",
        "named_target_authorization": "not_authorized",
        "activation_status": ACTIVATION_STATUS,
    }
