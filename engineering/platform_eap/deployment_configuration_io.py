from __future__ import annotations

import json
from enum import Enum
from typing import Any, Mapping

from engineering.platform_eap.deployment_configuration import (
    CONTRACT_VERSION,
    MAX_CONFIGURATION_BYTES,
    AdapterConfiguration,
    ConfigurationBundle,
    ConfigurationDigest,
    DeploymentAuditConfiguration,
    DeploymentAuthenticationMode,
    DeploymentCompatibility,
    DeploymentConfiguration,
    DeploymentConfigurationDataError,
    DeploymentIdentity,
    DeploymentProfile,
    DeploymentProfileName,
    EndpointCategoryPolicyConfiguration,
    EndpointPolicyConfiguration,
    ProxyConfiguration,
    ResourceLimitConfiguration,
    RuntimeConfiguration,
    RuntimeSecurityConfiguration,
    UnsupportedDeploymentConfigurationVersion,
    deterministic_json,
)
from engineering.platform_eap.proxy_foundation import ProxyEndpointCategory, ProxyMethodCategory, ProxyPolicyState


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DeploymentConfigurationDataError(f"Duplicate JSON field is prohibited: {key}.")
        result[key] = value
    return result


def load_json(text: str, context: str = "deployment configuration", maximum_bytes: int = MAX_CONFIGURATION_BYTES) -> object:
    if len(text.encode("utf-8")) > maximum_bytes:
        raise DeploymentConfigurationDataError(f"{context} exceeds the maximum configuration size.")
    try:
        return json.loads(text, object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise DeploymentConfigurationDataError(f"{context} is not valid JSON: {exc.msg}.") from exc


def _object(value: object, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DeploymentConfigurationDataError(f"{context} must be a JSON object.")
    return value


def _keys(payload: Mapping[str, Any], fields: set[str], context: str) -> None:
    missing = sorted(fields - payload.keys())
    unknown = sorted(payload.keys() - fields)
    if missing:
        raise DeploymentConfigurationDataError(f"{context} is missing required fields: {', '.join(missing)}.")
    if unknown:
        raise DeploymentConfigurationDataError(f"{context} contains unknown or unsafe fields: {', '.join(unknown)}.")


def _string(value: object, context: str) -> str:
    if not isinstance(value, str):
        raise DeploymentConfigurationDataError(f"{context} must be a string.")
    return value


def _version(value: object, context: str) -> str:
    version = _string(value, context)
    if version != CONTRACT_VERSION:
        raise UnsupportedDeploymentConfigurationVersion(f"{context} uses unsupported version {version!r}.")
    return version


def _boolean(value: object, context: str) -> bool:
    if not isinstance(value, bool):
        raise DeploymentConfigurationDataError(f"{context} must be a boolean.")
    return value


def _integer(value: object, context: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise DeploymentConfigurationDataError(f"{context} must be an integer.")
    return value


def _array(value: object, context: str) -> list[object]:
    if not isinstance(value, list):
        raise DeploymentConfigurationDataError(f"{context} must be an array.")
    return value


def _strings(value: object, context: str) -> tuple[str, ...]:
    values = _array(value, context)
    if any(not isinstance(item, str) for item in values):
        raise DeploymentConfigurationDataError(f"{context} must contain only strings.")
    return tuple(values)


def _enum(enum_type: type[Enum], value: object, context: str):
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise DeploymentConfigurationDataError(f"{context} contains an unsupported value: {value!r}.") from exc


def profile_from_dict(value: object) -> DeploymentProfile:
    payload = _object(value, "profile")
    fields = {"contract_version", "profile_version", "name", "description", "deployment_enabled", "execution_enabled"}
    _keys(payload, fields, "profile")
    return DeploymentProfile(_version(payload["contract_version"], "profile.contract_version"), _string(payload["profile_version"], "profile.profile_version"), _enum(DeploymentProfileName, payload["name"], "profile.name"), _string(payload["description"], "profile.description"), _boolean(payload["deployment_enabled"], "profile.deployment_enabled"), _boolean(payload["execution_enabled"], "profile.execution_enabled"))


def identity_from_dict(value: object) -> DeploymentIdentity:
    payload = _object(value, "identity")
    fields = {"contract_version", "identity_version", "deployment_id", "service_identity", "identity_scope", "deployment_authority", "approval_reference", "valid_from", "valid_until", "authentication_mode", "future_transport_requirements", "fixture_only"}
    _keys(payload, fields, "identity")
    return DeploymentIdentity(
        _version(payload["contract_version"], "identity.contract_version"),
        _string(payload["identity_version"], "identity.identity_version"),
        _string(payload["deployment_id"], "identity.deployment_id"),
        _string(payload["service_identity"], "identity.service_identity"),
        _string(payload["identity_scope"], "identity.identity_scope"),
        _string(payload["deployment_authority"], "identity.deployment_authority"),
        _string(payload["approval_reference"], "identity.approval_reference"),
        _string(payload["valid_from"], "identity.valid_from"),
        _string(payload["valid_until"], "identity.valid_until"),
        _enum(DeploymentAuthenticationMode, payload["authentication_mode"], "identity.authentication_mode"),
        _strings(payload["future_transport_requirements"], "identity.future_transport_requirements"),
        _boolean(payload["fixture_only"], "identity.fixture_only"),
    )


def security_from_dict(value: object) -> RuntimeSecurityConfiguration:
    payload = _object(value, "security")
    fields = {"contract_version", "security_version", "non_root_required", "read_only_filesystem_required", "dropped_capabilities", "seccomp_required", "apparmor_required", "privilege_escalation_allowed", "independent_disablement_required", "credential_loading_allowed", "certificate_loading_allowed"}
    _keys(payload, fields, "security")
    return RuntimeSecurityConfiguration(
        _version(payload["contract_version"], "security.contract_version"),
        _string(payload["security_version"], "security.security_version"),
        _boolean(payload["non_root_required"], "security.non_root_required"),
        _boolean(payload["read_only_filesystem_required"], "security.read_only_filesystem_required"),
        _strings(payload["dropped_capabilities"], "security.dropped_capabilities"),
        _boolean(payload["seccomp_required"], "security.seccomp_required"),
        _boolean(payload["apparmor_required"], "security.apparmor_required"),
        _boolean(payload["privilege_escalation_allowed"], "security.privilege_escalation_allowed"),
        _boolean(payload["independent_disablement_required"], "security.independent_disablement_required"),
        _boolean(payload["credential_loading_allowed"], "security.credential_loading_allowed"),
        _boolean(payload["certificate_loading_allowed"], "security.certificate_loading_allowed"),
    )


def resources_from_dict(value: object) -> ResourceLimitConfiguration:
    payload = _object(value, "resource_limits")
    fields = {"contract_version", "resource_limit_version", "memory_limit_bytes", "cpu_limit_millicores", "process_limit", "concurrency_limit", "request_timeout_seconds", "shutdown_timeout_seconds"}
    _keys(payload, fields, "resource_limits")
    return ResourceLimitConfiguration(_version(payload["contract_version"], "resource_limits.contract_version"), _string(payload["resource_limit_version"], "resource_limits.resource_limit_version"), *(_integer(payload[name], f"resource_limits.{name}") for name in ("memory_limit_bytes", "cpu_limit_millicores", "process_limit", "concurrency_limit", "request_timeout_seconds", "shutdown_timeout_seconds")))


def runtime_from_dict(value: object) -> RuntimeConfiguration:
    payload = _object(value, "runtime")
    fields = {"contract_version", "runtime_version", "security", "resource_limits", "restart_policy", "logging_policy", "execution_enabled", "runtime_access_enabled", "deployment_enabled"}
    _keys(payload, fields, "runtime")
    security = None if payload["security"] is None else security_from_dict(payload["security"])
    resources = None if payload["resource_limits"] is None else resources_from_dict(payload["resource_limits"])
    return RuntimeConfiguration(_version(payload["contract_version"], "runtime.contract_version"), _string(payload["runtime_version"], "runtime.runtime_version"), security, resources, _string(payload["restart_policy"], "runtime.restart_policy"), _string(payload["logging_policy"], "runtime.logging_policy"), _boolean(payload["execution_enabled"], "runtime.execution_enabled"), _boolean(payload["runtime_access_enabled"], "runtime.runtime_access_enabled"), _boolean(payload["deployment_enabled"], "runtime.deployment_enabled"))


def proxy_from_dict(value: object) -> ProxyConfiguration:
    payload = _object(value, "proxy")
    fields = {"contract_version", "proxy_version", "proxy_configuration_version", "proxy_policy_version", "maximum_request_payload_bytes", "maximum_response_payload_bytes", "maximum_response_records", "socket_access_enabled", "network_access_enabled", "listener_enabled", "runtime_access_enabled"}
    _keys(payload, fields, "proxy")
    return ProxyConfiguration(_version(payload["contract_version"], "proxy.contract_version"), _string(payload["proxy_version"], "proxy.proxy_version"), _string(payload["proxy_configuration_version"], "proxy.proxy_configuration_version"), _string(payload["proxy_policy_version"], "proxy.proxy_policy_version"), _integer(payload["maximum_request_payload_bytes"], "proxy.maximum_request_payload_bytes"), _integer(payload["maximum_response_payload_bytes"], "proxy.maximum_response_payload_bytes"), _integer(payload["maximum_response_records"], "proxy.maximum_response_records"), _boolean(payload["socket_access_enabled"], "proxy.socket_access_enabled"), _boolean(payload["network_access_enabled"], "proxy.network_access_enabled"), _boolean(payload["listener_enabled"], "proxy.listener_enabled"), _boolean(payload["runtime_access_enabled"], "proxy.runtime_access_enabled"))


def adapter_from_dict(value: object) -> AdapterConfiguration:
    payload = _object(value, "adapter")
    fields = {"contract_version", "adapter_version", "provider_contract_version", "proxy_contract_version", "live_provider_enabled", "named_target_enabled", "fixture_only"}
    _keys(payload, fields, "adapter")
    return AdapterConfiguration(_version(payload["contract_version"], "adapter.contract_version"), _string(payload["adapter_version"], "adapter.adapter_version"), _string(payload["provider_contract_version"], "adapter.provider_contract_version"), _string(payload["proxy_contract_version"], "adapter.proxy_contract_version"), _boolean(payload["live_provider_enabled"], "adapter.live_provider_enabled"), _boolean(payload["named_target_enabled"], "adapter.named_target_enabled"), _boolean(payload["fixture_only"], "adapter.fixture_only"))


def category_policy_from_dict(value: object) -> EndpointCategoryPolicyConfiguration:
    payload = _object(value, "category_policy")
    fields = {"contract_version", "endpoint_category", "policy_state", "allowed_methods"}
    _keys(payload, fields, "category_policy")
    methods = tuple(_enum(ProxyMethodCategory, item, "category_policy.allowed_methods") for item in _array(payload["allowed_methods"], "category_policy.allowed_methods"))
    return EndpointCategoryPolicyConfiguration(_version(payload["contract_version"], "category_policy.contract_version"), _enum(ProxyEndpointCategory, payload["endpoint_category"], "category_policy.endpoint_category"), _enum(ProxyPolicyState, payload["policy_state"], "category_policy.policy_state"), methods)


def endpoint_policy_from_dict(value: object) -> EndpointPolicyConfiguration:
    payload = _object(value, "endpoint_policy")
    fields = {"contract_version", "endpoint_policy_version", "proxy_policy_version", "proxy_policy_digest", "category_policy", "maximum_request_payload_bytes", "maximum_response_payload_bytes", "maximum_response_records", "allowed_signals", "denied_categories", "future_categories"}
    _keys(payload, fields, "endpoint_policy")
    categories = tuple(category_policy_from_dict(item) for item in _array(payload["category_policy"], "endpoint_policy.category_policy"))
    denied = tuple(_enum(ProxyEndpointCategory, item, "endpoint_policy.denied_categories") for item in _array(payload["denied_categories"], "endpoint_policy.denied_categories"))
    future = tuple(_enum(ProxyEndpointCategory, item, "endpoint_policy.future_categories") for item in _array(payload["future_categories"], "endpoint_policy.future_categories"))
    return EndpointPolicyConfiguration(_version(payload["contract_version"], "endpoint_policy.contract_version"), _string(payload["endpoint_policy_version"], "endpoint_policy.endpoint_policy_version"), _string(payload["proxy_policy_version"], "endpoint_policy.proxy_policy_version"), _string(payload["proxy_policy_digest"], "endpoint_policy.proxy_policy_digest"), categories, _integer(payload["maximum_request_payload_bytes"], "endpoint_policy.maximum_request_payload_bytes"), _integer(payload["maximum_response_payload_bytes"], "endpoint_policy.maximum_response_payload_bytes"), _integer(payload["maximum_response_records"], "endpoint_policy.maximum_response_records"), _strings(payload["allowed_signals"], "endpoint_policy.allowed_signals"), denied, future)


def audit_from_dict(value: object) -> DeploymentAuditConfiguration:
    payload = _object(value, "audit")
    fields = {"contract_version", "audit_version", "logging_policy", "audit_policy", "required_events", "destination_reference", "secret_redaction_required", "request_payload_logging_allowed", "response_payload_logging_allowed"}
    _keys(payload, fields, "audit")
    return DeploymentAuditConfiguration(_version(payload["contract_version"], "audit.contract_version"), _string(payload["audit_version"], "audit.audit_version"), _string(payload["logging_policy"], "audit.logging_policy"), _string(payload["audit_policy"], "audit.audit_policy"), _strings(payload["required_events"], "audit.required_events"), _string(payload["destination_reference"], "audit.destination_reference"), _boolean(payload["secret_redaction_required"], "audit.secret_redaction_required"), _boolean(payload["request_payload_logging_allowed"], "audit.request_payload_logging_allowed"), _boolean(payload["response_payload_logging_allowed"], "audit.response_payload_logging_allowed"))


def compatibility_from_dict(value: object) -> DeploymentCompatibility:
    payload = _object(value, "compatibility")
    names = ("contract_version", "compatibility_version", "deployment_configuration_version", "deployment_profile_version", "proxy_contract_version", "proxy_version", "proxy_configuration_version", "proxy_policy_version", "provider_contract_version", "adapter_version", "runtime_configuration_version", "security_configuration_version", "resource_limit_version", "audit_configuration_version", "identity_configuration_version", "endpoint_policy_configuration_version")
    _keys(payload, set(names), "compatibility")
    return DeploymentCompatibility(_version(payload["contract_version"], "compatibility.contract_version"), *(_string(payload[name], f"compatibility.{name}") for name in names[1:]))


def configuration_from_dict(value: object) -> DeploymentConfiguration:
    payload = _object(value, "deployment_configuration")
    fields = {"contract_version", "configuration_version", "profile", "identity", "runtime", "proxy", "adapter", "endpoint_policy", "audit", "compatibility", "fixture_only", "deployment_enabled", "activation_status"}
    _keys(payload, fields, "deployment_configuration")
    endpoint_policy = None if payload["endpoint_policy"] is None else endpoint_policy_from_dict(payload["endpoint_policy"])
    audit = None if payload["audit"] is None else audit_from_dict(payload["audit"])
    return DeploymentConfiguration(_version(payload["contract_version"], "deployment_configuration.contract_version"), _string(payload["configuration_version"], "deployment_configuration.configuration_version"), profile_from_dict(payload["profile"]), identity_from_dict(payload["identity"]), runtime_from_dict(payload["runtime"]), proxy_from_dict(payload["proxy"]), adapter_from_dict(payload["adapter"]), endpoint_policy, audit, compatibility_from_dict(payload["compatibility"]), _boolean(payload["fixture_only"], "deployment_configuration.fixture_only"), _boolean(payload["deployment_enabled"], "deployment_configuration.deployment_enabled"), _string(payload["activation_status"], "deployment_configuration.activation_status"))


def digest_from_dict(value: object) -> ConfigurationDigest:
    payload = _object(value, "configuration_digest")
    fields = {"contract_version", "digest_version", "algorithm", "value"}
    _keys(payload, fields, "configuration_digest")
    return ConfigurationDigest(_version(payload["contract_version"], "configuration_digest.contract_version"), _string(payload["digest_version"], "configuration_digest.digest_version"), _string(payload["algorithm"], "configuration_digest.algorithm"), _string(payload["value"], "configuration_digest.value"))


def bundle_from_dict(value: object) -> ConfigurationBundle:
    payload = _object(value, "configuration_bundle")
    fields = {"contract_version", "bundle_version", "configuration", "digest"}
    _keys(payload, fields, "configuration_bundle")
    return ConfigurationBundle(_version(payload["contract_version"], "configuration_bundle.contract_version"), _string(payload["bundle_version"], "configuration_bundle.bundle_version"), configuration_from_dict(payload["configuration"]), digest_from_dict(payload["digest"]))


def bundle_from_json(text: str) -> ConfigurationBundle:
    return bundle_from_dict(load_json(text, "configuration bundle"))


def bundle_to_json(bundle: ConfigurationBundle) -> str:
    return deterministic_json(bundle)


def configuration_to_json(configuration: DeploymentConfiguration) -> str:
    return deterministic_json(configuration)


def contract_summary_to_json(summary: Mapping[str, object]) -> str:
    return deterministic_json(summary)
