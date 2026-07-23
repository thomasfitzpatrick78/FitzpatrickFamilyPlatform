from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
from typing import Mapping, Sequence

from engineering.platform_eap.provider_adapter import ADAPTER_VERSION
from engineering.platform_eap.proxy_foundation import (
    CONFIGURATION_VERSION as PROXY_CONFIGURATION_VERSION,
    CONTRACT_VERSION as PROXY_CONTRACT_VERSION,
    MAX_REQUEST_PAYLOAD_BYTES,
    MAX_RESPONSE_PAYLOAD_BYTES,
    MAX_RESPONSE_RECORDS,
    POLICY_VERSION,
    PROXY_VERSION,
    ProxyEndpointCategory,
    ProxyMethodCategory,
    ProxyPolicyState,
    repository_policy,
)


CONTRACT_VERSION = "1.0"
DEPLOYMENT_CONFIGURATION_VERSION = "privileged-deployment-configuration-v1.0"
DEPLOYMENT_PROFILE_VERSION = "deployment-profile-v1.0"
RUNTIME_CONFIGURATION_VERSION = "runtime-configuration-v1.0"
SECURITY_CONFIGURATION_VERSION = "runtime-security-configuration-v1.0"
RESOURCE_LIMIT_VERSION = "resource-limit-configuration-v1.0"
AUDIT_CONFIGURATION_VERSION = "deployment-audit-configuration-v1.0"
IDENTITY_CONFIGURATION_VERSION = "deployment-identity-configuration-v1.0"
ENDPOINT_POLICY_CONFIGURATION_VERSION = "endpoint-policy-configuration-v1.0"
COMPATIBILITY_VERSION = "deployment-compatibility-v1.0"
BUNDLE_VERSION = "deployment-configuration-bundle-v1.0"
DIGEST_VERSION = "configuration-digest-v1.0"
ACTIVATION_STATUS = "not_activated"
FIXTURE_ROOT = "engineering/tests/fixtures/deployment_configuration"
MAX_CONFIGURATION_BYTES = 131_072


class DeploymentConfigurationDataError(ValueError):
    """Raised when deployment-configuration fixture input is malformed."""


class UnsupportedDeploymentConfigurationVersion(DeploymentConfigurationDataError):
    """Raised when an input contract version is unsupported."""


class FindingSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class DeploymentProfileName(str, Enum):
    REPOSITORY_ONLY = "RepositoryOnly"
    FUTURE_DEVELOPMENT = "FutureDevelopment"
    FUTURE_VALIDATION = "FutureValidation"
    FUTURE_PRODUCTION = "FutureProduction"


class DeploymentAuthenticationMode(str, Enum):
    SERVICE_IDENTITY = "ServiceIdentity"
    FUTURE_MUTUAL_TLS = "FutureMutualTLS"


@dataclass(frozen=True)
class DeploymentFinding:
    severity: FindingSeverity
    code: str
    message: str
    reference: str | None = None


@dataclass(frozen=True)
class DeploymentProfile:
    contract_version: str
    profile_version: str
    name: DeploymentProfileName
    description: str
    deployment_enabled: bool
    execution_enabled: bool


@dataclass(frozen=True)
class DeploymentIdentity:
    contract_version: str
    identity_version: str
    deployment_id: str
    service_identity: str
    identity_scope: str
    deployment_authority: str
    approval_reference: str
    valid_from: str
    valid_until: str
    authentication_mode: DeploymentAuthenticationMode
    future_transport_requirements: tuple[str, ...]
    fixture_only: bool


@dataclass(frozen=True)
class RuntimeSecurityConfiguration:
    contract_version: str
    security_version: str
    non_root_required: bool
    read_only_filesystem_required: bool
    dropped_capabilities: tuple[str, ...]
    seccomp_required: bool
    apparmor_required: bool
    privilege_escalation_allowed: bool
    independent_disablement_required: bool
    credential_loading_allowed: bool
    certificate_loading_allowed: bool


@dataclass(frozen=True)
class ResourceLimitConfiguration:
    contract_version: str
    resource_limit_version: str
    memory_limit_bytes: int
    cpu_limit_millicores: int
    process_limit: int
    concurrency_limit: int
    request_timeout_seconds: int
    shutdown_timeout_seconds: int


@dataclass(frozen=True)
class DeploymentAuditConfiguration:
    contract_version: str
    audit_version: str
    logging_policy: str
    audit_policy: str
    required_events: tuple[str, ...]
    destination_reference: str
    secret_redaction_required: bool
    request_payload_logging_allowed: bool
    response_payload_logging_allowed: bool


@dataclass(frozen=True)
class RuntimeConfiguration:
    contract_version: str
    runtime_version: str
    security: RuntimeSecurityConfiguration | None
    resource_limits: ResourceLimitConfiguration | None
    restart_policy: str
    logging_policy: str
    execution_enabled: bool
    runtime_access_enabled: bool
    deployment_enabled: bool


@dataclass(frozen=True)
class ProxyConfiguration:
    contract_version: str
    proxy_version: str
    proxy_configuration_version: str
    proxy_policy_version: str
    maximum_request_payload_bytes: int
    maximum_response_payload_bytes: int
    maximum_response_records: int
    socket_access_enabled: bool
    network_access_enabled: bool
    listener_enabled: bool
    runtime_access_enabled: bool


@dataclass(frozen=True)
class AdapterConfiguration:
    contract_version: str
    adapter_version: str
    provider_contract_version: str
    proxy_contract_version: str
    live_provider_enabled: bool
    named_target_enabled: bool
    fixture_only: bool


@dataclass(frozen=True)
class EndpointCategoryPolicyConfiguration:
    contract_version: str
    endpoint_category: ProxyEndpointCategory
    policy_state: ProxyPolicyState
    allowed_methods: tuple[ProxyMethodCategory, ...]


@dataclass(frozen=True)
class EndpointPolicyConfiguration:
    contract_version: str
    endpoint_policy_version: str
    proxy_policy_version: str
    proxy_policy_digest: str
    category_policy: tuple[EndpointCategoryPolicyConfiguration, ...]
    maximum_request_payload_bytes: int
    maximum_response_payload_bytes: int
    maximum_response_records: int
    allowed_signals: tuple[str, ...]
    denied_categories: tuple[ProxyEndpointCategory, ...]
    future_categories: tuple[ProxyEndpointCategory, ...]


@dataclass(frozen=True)
class DeploymentCompatibility:
    contract_version: str
    compatibility_version: str
    deployment_configuration_version: str
    deployment_profile_version: str
    proxy_contract_version: str
    proxy_version: str
    proxy_configuration_version: str
    proxy_policy_version: str
    provider_contract_version: str
    adapter_version: str
    runtime_configuration_version: str
    security_configuration_version: str
    resource_limit_version: str
    audit_configuration_version: str
    identity_configuration_version: str
    endpoint_policy_configuration_version: str


@dataclass(frozen=True)
class DeploymentConfiguration:
    contract_version: str
    configuration_version: str
    profile: DeploymentProfile
    identity: DeploymentIdentity
    runtime: RuntimeConfiguration
    proxy: ProxyConfiguration
    adapter: AdapterConfiguration
    endpoint_policy: EndpointPolicyConfiguration | None
    audit: DeploymentAuditConfiguration | None
    compatibility: DeploymentCompatibility
    fixture_only: bool
    deployment_enabled: bool
    activation_status: str


@dataclass(frozen=True)
class ConfigurationDigest:
    contract_version: str
    digest_version: str
    algorithm: str
    value: str


@dataclass(frozen=True)
class ConfigurationBundle:
    contract_version: str
    bundle_version: str
    configuration: DeploymentConfiguration
    digest: ConfigurationDigest


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


def configuration_digest(configuration: DeploymentConfiguration) -> ConfigurationDigest:
    return ConfigurationDigest(CONTRACT_VERSION, DIGEST_VERSION, "sha256", canonical_digest(configuration))


def bundle_for(configuration: DeploymentConfiguration) -> ConfigurationBundle:
    return ConfigurationBundle(CONTRACT_VERSION, BUNDLE_VERSION, configuration, configuration_digest(configuration))


def _finding(code: str, message: str, reference: str | None = None) -> DeploymentFinding:
    return DeploymentFinding(FindingSeverity.ERROR, code, message, reference)


def _valid_timestamp(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None
    except (TypeError, ValueError):
        return False


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _ordered_unique(values: Sequence[object], allow_empty: bool = False) -> bool:
    rendered = [item.value if isinstance(item, Enum) else str(item) for item in values]
    return (allow_empty or bool(rendered)) and rendered == sorted(set(rendered))


def _digest(value: str) -> bool:
    return len(value) == 71 and value.startswith("sha256:") and all(char in "0123456789abcdef" for char in value[7:])


def deployment_profile(name: DeploymentProfileName) -> DeploymentProfile:
    descriptions = {
        DeploymentProfileName.REPOSITORY_ONLY: "Repository fixture validation only.",
        DeploymentProfileName.FUTURE_DEVELOPMENT: "Descriptive future development deployment requirements.",
        DeploymentProfileName.FUTURE_VALIDATION: "Descriptive future controlled validation requirements.",
        DeploymentProfileName.FUTURE_PRODUCTION: "Descriptive future production requirements.",
    }
    return DeploymentProfile(CONTRACT_VERSION, DEPLOYMENT_PROFILE_VERSION, name, descriptions[name], False, False)


def repository_runtime() -> RuntimeConfiguration:
    security = RuntimeSecurityConfiguration(
        CONTRACT_VERSION,
        SECURITY_CONFIGURATION_VERSION,
        True,
        True,
        ("ALL",),
        True,
        True,
        False,
        True,
        False,
        False,
    )
    limits = ResourceLimitConfiguration(CONTRACT_VERSION, RESOURCE_LIMIT_VERSION, 134_217_728, 250, 64, 4, 10, 15)
    return RuntimeConfiguration(CONTRACT_VERSION, RUNTIME_CONFIGURATION_VERSION, security, limits, "disabled", "structured_secret_safe", False, False, False)


def repository_audit() -> DeploymentAuditConfiguration:
    return DeploymentAuditConfiguration(
        CONTRACT_VERSION,
        AUDIT_CONFIGURATION_VERSION,
        "structured_secret_safe",
        "decision_and_configuration_events",
        tuple(sorted(("configuration_validated", "decision_recorded", "deployment_disabled", "identity_rejected", "policy_rejected"))),
        f"{FIXTURE_ROOT}/deployment-fixtures.json",
        True,
        False,
        False,
    )


def repository_endpoint_policy() -> EndpointPolicyConfiguration:
    policy = repository_policy()
    categories = tuple(
        EndpointCategoryPolicyConfiguration(CONTRACT_VERSION, entry.endpoint_category, entry.state, entry.allowed_methods)
        for entry in policy.entries
    )
    denied = tuple(sorted((entry.endpoint_category for entry in policy.entries if entry.state == ProxyPolicyState.DENIED), key=lambda item: item.value))
    future = tuple(sorted((entry.endpoint_category for entry in policy.entries if entry.state == ProxyPolicyState.FUTURE), key=lambda item: item.value))
    signals = tuple(sorted(("container.cpu.utilization", "container.healthcheck.state", "container.lifecycle.observed_state", "container.restart.count")))
    return EndpointPolicyConfiguration(
        CONTRACT_VERSION,
        ENDPOINT_POLICY_CONFIGURATION_VERSION,
        POLICY_VERSION,
        policy.policy_digest,
        categories,
        MAX_REQUEST_PAYLOAD_BYTES,
        MAX_RESPONSE_PAYLOAD_BYTES,
        MAX_RESPONSE_RECORDS,
        signals,
        denied,
        future,
    )


def repository_compatibility() -> DeploymentCompatibility:
    return DeploymentCompatibility(
        CONTRACT_VERSION,
        COMPATIBILITY_VERSION,
        DEPLOYMENT_CONFIGURATION_VERSION,
        DEPLOYMENT_PROFILE_VERSION,
        PROXY_CONTRACT_VERSION,
        PROXY_VERSION,
        PROXY_CONFIGURATION_VERSION,
        POLICY_VERSION,
        "1.0",
        ADAPTER_VERSION,
        RUNTIME_CONFIGURATION_VERSION,
        SECURITY_CONFIGURATION_VERSION,
        RESOURCE_LIMIT_VERSION,
        AUDIT_CONFIGURATION_VERSION,
        IDENTITY_CONFIGURATION_VERSION,
        ENDPOINT_POLICY_CONFIGURATION_VERSION,
    )


def repository_configuration(profile_name: DeploymentProfileName = DeploymentProfileName.REPOSITORY_ONLY) -> DeploymentConfiguration:
    authentication_mode = DeploymentAuthenticationMode.SERVICE_IDENTITY
    transport_requirements = ("future_authenticated_service_transport", "future_separate_non_runtime_boundary")
    if profile_name == DeploymentProfileName.FUTURE_PRODUCTION:
        authentication_mode = DeploymentAuthenticationMode.FUTURE_MUTUAL_TLS
        transport_requirements = ("future_enforced_service_identity", "future_mutual_authentication", "future_separate_non_runtime_boundary")
    identity = DeploymentIdentity(
        CONTRACT_VERSION,
        IDENTITY_CONFIGURATION_VERSION,
        "fixture-constrained-proxy-deployment",
        "fixture-constrained-proxy-service",
        "synthetic_repository_fixture",
        "Architecture Gatekeeper",
        "FIXTURE-APPROVAL-DEPLOYMENT-001",
        "2026-07-22T11:00:00Z",
        "2026-07-22T13:00:00Z",
        authentication_mode,
        tuple(sorted(transport_requirements)),
        True,
    )
    proxy = ProxyConfiguration(
        CONTRACT_VERSION,
        PROXY_VERSION,
        PROXY_CONFIGURATION_VERSION,
        POLICY_VERSION,
        MAX_REQUEST_PAYLOAD_BYTES,
        MAX_RESPONSE_PAYLOAD_BYTES,
        MAX_RESPONSE_RECORDS,
        False,
        False,
        False,
        False,
    )
    adapter = AdapterConfiguration(CONTRACT_VERSION, ADAPTER_VERSION, "1.0", PROXY_CONTRACT_VERSION, False, False, True)
    return DeploymentConfiguration(
        CONTRACT_VERSION,
        DEPLOYMENT_CONFIGURATION_VERSION,
        deployment_profile(profile_name),
        identity,
        repository_runtime(),
        proxy,
        adapter,
        repository_endpoint_policy(),
        repository_audit(),
        repository_compatibility(),
        True,
        False,
        ACTIVATION_STATUS,
    )


def validate_profile(profile: DeploymentProfile) -> tuple[DeploymentFinding, ...]:
    findings: list[DeploymentFinding] = []
    if profile.contract_version != CONTRACT_VERSION or profile.profile_version != DEPLOYMENT_PROFILE_VERSION:
        findings.append(_finding("profile.version.unsupported", "Deployment profile version is unsupported."))
    if not profile.description:
        findings.append(_finding("profile.description.required", "Deployment profile description is required."))
    if profile.deployment_enabled or profile.execution_enabled:
        findings.append(_finding("profile.execution.prohibited", "Repository deployment profiles cannot enable deployment or execution."))
    return tuple(findings)


def validate_identity(identity: DeploymentIdentity) -> tuple[DeploymentFinding, ...]:
    findings: list[DeploymentFinding] = []
    if identity.contract_version != CONTRACT_VERSION or identity.identity_version != IDENTITY_CONFIGURATION_VERSION:
        findings.append(_finding("identity.version.unsupported", "Deployment identity version is unsupported."))
    for name in ("deployment_id", "service_identity", "identity_scope", "deployment_authority", "approval_reference"):
        value = getattr(identity, name)
        if not value or "*" in value:
            findings.append(_finding(f"identity.{name}.invalid", f"Deployment identity {name} must be exact and non-wildcard."))
    if not identity.approval_reference.startswith("FIXTURE-APPROVAL-"):
        findings.append(_finding("identity.approval.fixture_required", "Repository configuration requires an explicit synthetic approval reference."))
    if not all(_valid_timestamp(value) for value in (identity.valid_from, identity.valid_until)) or (_valid_timestamp(identity.valid_from) and _valid_timestamp(identity.valid_until) and _time(identity.valid_until) < _time(identity.valid_from)):
        findings.append(_finding("identity.window.invalid", "Deployment identity validity window is invalid."))
    if not _ordered_unique(identity.future_transport_requirements):
        findings.append(_finding("identity.transport_requirements.invalid", "Future transport requirements must be nonempty, unique, and sorted."))
    if not identity.fixture_only:
        findings.append(_finding("identity.fixture_scope.required", "Deployment identity must remain synthetic."))
    return tuple(findings)


def validate_security(security: RuntimeSecurityConfiguration | None) -> tuple[DeploymentFinding, ...]:
    if security is None:
        return (_finding("security.required", "Runtime security configuration is required."),)
    findings: list[DeploymentFinding] = []
    if security.contract_version != CONTRACT_VERSION or security.security_version != SECURITY_CONFIGURATION_VERSION:
        findings.append(_finding("security.version.unsupported", "Runtime security configuration version is unsupported."))
    if not security.non_root_required or not security.read_only_filesystem_required or security.dropped_capabilities != ("ALL",):
        findings.append(_finding("security.least_privilege.required", "Non-root, read-only filesystem, and dropping ALL capabilities are required."))
    if not security.seccomp_required or not security.apparmor_required or not security.independent_disablement_required:
        findings.append(_finding("security.controls.required", "Seccomp, AppArmor, and independent disablement requirements are mandatory."))
    if security.privilege_escalation_allowed or security.credential_loading_allowed or security.certificate_loading_allowed:
        findings.append(_finding("security.privileged_loading.prohibited", "Privilege escalation, credential loading, and certificate loading must remain disabled."))
    return tuple(findings)


def validate_resource_limits(limits: ResourceLimitConfiguration | None) -> tuple[DeploymentFinding, ...]:
    if limits is None:
        return (_finding("resources.required", "Resource-limit configuration is required."),)
    findings: list[DeploymentFinding] = []
    if limits.contract_version != CONTRACT_VERSION or limits.resource_limit_version != RESOURCE_LIMIT_VERSION:
        findings.append(_finding("resources.version.unsupported", "Resource-limit configuration version is unsupported."))
    values = (limits.memory_limit_bytes, limits.cpu_limit_millicores, limits.process_limit, limits.concurrency_limit, limits.request_timeout_seconds, limits.shutdown_timeout_seconds)
    if any(value <= 0 for value in values):
        findings.append(_finding("resources.bounds.invalid", "All resource and timeout limits must be positive."))
    if limits.memory_limit_bytes > 536_870_912 or limits.cpu_limit_millicores > 1000 or limits.process_limit > 256 or limits.concurrency_limit > 32 or limits.request_timeout_seconds > 60 or limits.shutdown_timeout_seconds > 60:
        findings.append(_finding("resources.bounds.excessive", "Resource or timeout limits exceed repository safety bounds."))
    return tuple(findings)


def validate_runtime(runtime: RuntimeConfiguration) -> tuple[DeploymentFinding, ...]:
    findings: list[DeploymentFinding] = []
    if runtime.contract_version != CONTRACT_VERSION or runtime.runtime_version != RUNTIME_CONFIGURATION_VERSION:
        findings.append(_finding("runtime.version.unsupported", "Runtime configuration version is unsupported."))
    findings.extend(validate_security(runtime.security))
    findings.extend(validate_resource_limits(runtime.resource_limits))
    if runtime.restart_policy != "disabled" or runtime.logging_policy != "structured_secret_safe":
        findings.append(_finding("runtime.policy.invalid", "Repository restart must be disabled and logging must be structured and secret-safe."))
    if runtime.execution_enabled or runtime.runtime_access_enabled or runtime.deployment_enabled:
        findings.append(_finding("runtime.execution.prohibited", "Runtime execution, access, and deployment must remain disabled."))
    return tuple(findings)


def validate_audit(audit: DeploymentAuditConfiguration | None) -> tuple[DeploymentFinding, ...]:
    if audit is None:
        return (_finding("audit.required", "Deployment audit configuration is required."),)
    findings: list[DeploymentFinding] = []
    if audit.contract_version != CONTRACT_VERSION or audit.audit_version != AUDIT_CONFIGURATION_VERSION:
        findings.append(_finding("audit.version.unsupported", "Deployment audit configuration version is unsupported."))
    if not _ordered_unique(audit.required_events) or not audit.destination_reference.startswith(f"{FIXTURE_ROOT}/"):
        findings.append(_finding("audit.scope.invalid", "Audit events and destination must remain governed repository fixtures."))
    if not audit.secret_redaction_required or audit.request_payload_logging_allowed or audit.response_payload_logging_allowed:
        findings.append(_finding("audit.payload_logging.prohibited", "Secret redaction is required and payload logging is prohibited."))
    return tuple(findings)


def validate_endpoint_policy(policy: EndpointPolicyConfiguration | None) -> tuple[DeploymentFinding, ...]:
    if policy is None:
        return (_finding("endpoint_policy.required", "Endpoint-policy configuration is required."),)
    findings: list[DeploymentFinding] = []
    expected = repository_endpoint_policy()
    if policy.contract_version != CONTRACT_VERSION or policy.endpoint_policy_version != ENDPOINT_POLICY_CONFIGURATION_VERSION or policy.proxy_policy_version != POLICY_VERSION:
        findings.append(_finding("endpoint_policy.version.unsupported", "Endpoint-policy configuration version is unsupported."))
    if policy.proxy_policy_digest != repository_policy().policy_digest or not _digest(policy.proxy_policy_digest):
        findings.append(_finding("endpoint_policy.digest.mismatch", "Endpoint policy does not bind the published proxy policy digest."))
    if policy.category_policy != expected.category_policy or policy.denied_categories != expected.denied_categories or policy.future_categories != expected.future_categories:
        findings.append(_finding("endpoint_policy.matrix.mismatch", "Endpoint category policy does not match the published proxy foundation."))
    if (policy.maximum_request_payload_bytes, policy.maximum_response_payload_bytes, policy.maximum_response_records) != (MAX_REQUEST_PAYLOAD_BYTES, MAX_RESPONSE_PAYLOAD_BYTES, MAX_RESPONSE_RECORDS):
        findings.append(_finding("endpoint_policy.bounds.mismatch", "Endpoint policy bounds do not match the published proxy foundation."))
    if policy.allowed_signals != expected.allowed_signals or not _ordered_unique(policy.allowed_signals):
        findings.append(_finding("endpoint_policy.signals.invalid", "Allowed signals must exactly match the governed nonempty, unique, and sorted signal allowlist."))
    return tuple(findings)


def validate_proxy(proxy: ProxyConfiguration) -> tuple[DeploymentFinding, ...]:
    findings: list[DeploymentFinding] = []
    if (proxy.contract_version, proxy.proxy_version, proxy.proxy_configuration_version, proxy.proxy_policy_version) != (CONTRACT_VERSION, PROXY_VERSION, PROXY_CONFIGURATION_VERSION, POLICY_VERSION):
        findings.append(_finding("proxy.version.incompatible", "Proxy configuration versions are incompatible."))
    if (proxy.maximum_request_payload_bytes, proxy.maximum_response_payload_bytes, proxy.maximum_response_records) != (MAX_REQUEST_PAYLOAD_BYTES, MAX_RESPONSE_PAYLOAD_BYTES, MAX_RESPONSE_RECORDS):
        findings.append(_finding("proxy.bounds.incompatible", "Proxy configuration bounds are incompatible."))
    if proxy.socket_access_enabled or proxy.network_access_enabled or proxy.listener_enabled or proxy.runtime_access_enabled:
        findings.append(_finding("proxy.runtime_capability.prohibited", "Socket, network, listener, and runtime access must remain disabled."))
    return tuple(findings)


def validate_adapter(adapter: AdapterConfiguration) -> tuple[DeploymentFinding, ...]:
    findings: list[DeploymentFinding] = []
    if (adapter.contract_version, adapter.adapter_version, adapter.provider_contract_version, adapter.proxy_contract_version) != (CONTRACT_VERSION, ADAPTER_VERSION, "1.0", PROXY_CONTRACT_VERSION):
        findings.append(_finding("adapter.version.incompatible", "Adapter configuration versions are incompatible."))
    if adapter.live_provider_enabled or adapter.named_target_enabled or not adapter.fixture_only:
        findings.append(_finding("adapter.live_access.prohibited", "Live provider and named-target access must remain disabled and fixture-only."))
    return tuple(findings)


def validate_compatibility(compatibility: DeploymentCompatibility) -> tuple[DeploymentFinding, ...]:
    expected = repository_compatibility()
    if compatibility != expected:
        return (_finding("compatibility.version.incompatible", "Deployment, proxy, provider, policy, runtime, security, resource, audit, identity, or adapter versions are incompatible."),)
    return ()


def validate_configuration(configuration: DeploymentConfiguration) -> tuple[DeploymentFinding, ...]:
    findings: list[DeploymentFinding] = []
    if configuration.contract_version != CONTRACT_VERSION or configuration.configuration_version != DEPLOYMENT_CONFIGURATION_VERSION:
        findings.append(_finding("configuration.version.unsupported", "Deployment configuration version is unsupported."))
    findings.extend(validate_profile(configuration.profile))
    findings.extend(validate_identity(configuration.identity))
    findings.extend(validate_runtime(configuration.runtime))
    findings.extend(validate_proxy(configuration.proxy))
    findings.extend(validate_adapter(configuration.adapter))
    findings.extend(validate_endpoint_policy(configuration.endpoint_policy))
    findings.extend(validate_audit(configuration.audit))
    findings.extend(validate_compatibility(configuration.compatibility))
    expected_authentication = (
        DeploymentAuthenticationMode.FUTURE_MUTUAL_TLS
        if configuration.profile.name == DeploymentProfileName.FUTURE_PRODUCTION
        else DeploymentAuthenticationMode.SERVICE_IDENTITY
    )
    if configuration.identity.authentication_mode != expected_authentication:
        findings.append(_finding("configuration.profile_identity.incompatible", "Deployment profile and descriptive authentication mode are incompatible."))
    if not configuration.fixture_only or configuration.deployment_enabled or configuration.activation_status != ACTIVATION_STATUS:
        findings.append(_finding("configuration.repository_scope.required", "Configuration must remain fixture-only, deployment-disabled, and not activated."))
    return tuple(findings)


def validate_bundle(bundle: ConfigurationBundle) -> tuple[DeploymentFinding, ...]:
    findings: list[DeploymentFinding] = []
    if bundle.contract_version != CONTRACT_VERSION or bundle.bundle_version != BUNDLE_VERSION:
        findings.append(_finding("bundle.version.unsupported", "Configuration bundle version is unsupported."))
    findings.extend(validate_configuration(bundle.configuration))
    expected = configuration_digest(bundle.configuration)
    if bundle.digest != expected or bundle.digest.contract_version != CONTRACT_VERSION or bundle.digest.digest_version != DIGEST_VERSION or bundle.digest.algorithm != "sha256" or not _digest(bundle.digest.value):
        findings.append(_finding("bundle.digest.mismatch", "Configuration bundle digest does not match canonical configuration content."))
    return tuple(findings)


def negotiate_versions(configuration: DeploymentConfiguration) -> Mapping[str, object]:
    findings = validate_compatibility(configuration.compatibility)
    return {
        "contract_version": CONTRACT_VERSION,
        "compatible": not findings,
        "deployment_configuration_version": configuration.configuration_version,
        "proxy_version": configuration.proxy.proxy_version,
        "adapter_version": configuration.adapter.adapter_version,
        "policy_version": configuration.endpoint_policy.proxy_policy_version if configuration.endpoint_policy else None,
        "security_version": configuration.runtime.security.security_version if configuration.runtime.security else None,
        "findings": [primitive(item) for item in findings],
    }


def contract_summary() -> Mapping[str, object]:
    return {
        "contract_version": CONTRACT_VERSION,
        "configuration_version": DEPLOYMENT_CONFIGURATION_VERSION,
        "profiles": [profile.value for profile in DeploymentProfileName],
        "repository_only": True,
        "deployment": "disabled",
        "execution": "disabled",
        "networking": "absent",
        "socket_access": "absent",
        "credential_loading": "prohibited",
        "certificate_loading": "prohibited",
        "named_target_authorization": "not_authorized",
        "activation_status": ACTIVATION_STATUS,
    }
