from __future__ import annotations

import json
from enum import Enum
from typing import Any, Mapping

from engineering.platform_eap.proxy_foundation import (
    CONTRACT_VERSION,
    MAX_REQUEST_PAYLOAD_BYTES,
    MAX_RESPONSE_PAYLOAD_BYTES,
    MockProxyResult,
    ProxyAuditEvent,
    ProxyAuthenticationContext,
    ProxyAuthenticationMode,
    ProxyAuthorizationContext,
    ProxyCapabilityDeclaration,
    ProxyConfiguration,
    ProxyDataError,
    ProxyDecision,
    ProxyDecisionStatus,
    ProxyEndpointCategory,
    ProxyFailure,
    ProxyMethodCategory,
    ProxyParameter,
    ProxyPolicy,
    ProxyPolicyEntry,
    ProxyPolicyState,
    ProxyRequest,
    ProxyResponse,
    ProxyResponseMetadata,
    ProxyResponseRecord,
    ProxyTarget,
    UnsupportedProxyContractVersion,
    deterministic_json,
)


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ProxyDataError(f"Duplicate JSON field is prohibited: {key}.")
        result[key] = value
    return result


def load_json(text: str, context: str = "proxy document", maximum_bytes: int | None = None) -> object:
    if maximum_bytes is not None and len(text.encode("utf-8")) > maximum_bytes:
        raise ProxyDataError(f"{context} exceeds the maximum payload size.")
    try:
        return json.loads(text, object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise ProxyDataError(f"{context} is not valid JSON: {exc.msg}.") from exc


def _object(value: object, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ProxyDataError(f"{context} must be a JSON object.")
    return value


def _keys(payload: Mapping[str, Any], fields: set[str], context: str) -> None:
    missing = sorted(fields - payload.keys())
    unknown = sorted(payload.keys() - fields)
    if missing:
        raise ProxyDataError(f"{context} is missing required fields: {', '.join(missing)}.")
    if unknown:
        raise ProxyDataError(f"{context} contains unknown or unsafe fields: {', '.join(unknown)}.")


def _version(value: object, context: str) -> str:
    version = _string(value, context)
    if version != CONTRACT_VERSION:
        raise UnsupportedProxyContractVersion(f"{context} uses unsupported version {version!r}.")
    return version


def _string(value: object, context: str) -> str:
    if not isinstance(value, str):
        raise ProxyDataError(f"{context} must be a string.")
    return value


def _boolean(value: object, context: str) -> bool:
    if not isinstance(value, bool):
        raise ProxyDataError(f"{context} must be a boolean.")
    return value


def _integer(value: object, context: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ProxyDataError(f"{context} must be an integer.")
    return value


def _strings(value: object, context: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ProxyDataError(f"{context} must be an array of strings.")
    return tuple(value)


def _array(value: object, context: str) -> list[object]:
    if not isinstance(value, list):
        raise ProxyDataError(f"{context} must be an array.")
    return value


def _enum(enum_type: type[Enum], value: object, context: str):
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ProxyDataError(f"{context} contains an unsupported value: {value!r}.") from exc


def authentication_from_dict(value: object) -> ProxyAuthenticationContext:
    payload = _object(value, "authentication")
    fields = {"contract_version", "mode", "principal_id", "service_identity", "authenticated", "fixture_only"}
    _keys(payload, fields, "authentication")
    return ProxyAuthenticationContext(
        _version(payload["contract_version"], "authentication.contract_version"),
        _enum(ProxyAuthenticationMode, payload["mode"], "authentication.mode"),
        _string(payload["principal_id"], "authentication.principal_id"),
        _string(payload["service_identity"], "authentication.service_identity"),
        _boolean(payload["authenticated"], "authentication.authenticated"),
        _boolean(payload["fixture_only"], "authentication.fixture_only"),
    )


def authorization_from_dict(value: object) -> ProxyAuthorizationContext:
    payload = _object(value, "authorization")
    fields = {
        "contract_version", "authorization_reference", "authorization_digest", "approval_reference",
        "registry_subject_reference", "subject_id", "configuration_digest", "proxy_version", "adapter_version",
        "policy_version", "approved_endpoint_categories", "approved_signal_set", "observation_window_start",
        "observation_window_end", "expires_at", "fixture_only",
    }
    _keys(payload, fields, "authorization")
    categories = tuple(_enum(ProxyEndpointCategory, item, "authorization.approved_endpoint_categories") for item in _array(payload["approved_endpoint_categories"], "authorization.approved_endpoint_categories"))
    return ProxyAuthorizationContext(
        _version(payload["contract_version"], "authorization.contract_version"),
        _string(payload["authorization_reference"], "authorization.authorization_reference"),
        _string(payload["authorization_digest"], "authorization.authorization_digest"),
        _string(payload["approval_reference"], "authorization.approval_reference"),
        _string(payload["registry_subject_reference"], "authorization.registry_subject_reference"),
        _string(payload["subject_id"], "authorization.subject_id"),
        _string(payload["configuration_digest"], "authorization.configuration_digest"),
        _string(payload["proxy_version"], "authorization.proxy_version"),
        _string(payload["adapter_version"], "authorization.adapter_version"),
        _string(payload["policy_version"], "authorization.policy_version"),
        categories,
        _strings(payload["approved_signal_set"], "authorization.approved_signal_set"),
        _string(payload["observation_window_start"], "authorization.observation_window_start"),
        _string(payload["observation_window_end"], "authorization.observation_window_end"),
        _string(payload["expires_at"], "authorization.expires_at"),
        _boolean(payload["fixture_only"], "authorization.fixture_only"),
    )


def target_from_dict(value: object) -> ProxyTarget:
    payload = _object(value, "target")
    fields = {"contract_version", "subject_id", "registry_subject_reference", "host_reference", "environment", "fixture_only"}
    _keys(payload, fields, "target")
    return ProxyTarget(
        _version(payload["contract_version"], "target.contract_version"),
        _string(payload["subject_id"], "target.subject_id"),
        _string(payload["registry_subject_reference"], "target.registry_subject_reference"),
        _string(payload["host_reference"], "target.host_reference"),
        _string(payload["environment"], "target.environment"),
        _boolean(payload["fixture_only"], "target.fixture_only"),
    )


def parameter_from_dict(value: object) -> ProxyParameter:
    payload = _object(value, "parameter")
    fields = {"contract_version", "name", "value"}
    _keys(payload, fields, "parameter")
    return ProxyParameter(_version(payload["contract_version"], "parameter.contract_version"), _string(payload["name"], "parameter.name"), _string(payload["value"], "parameter.value"))


def request_from_dict(value: object) -> ProxyRequest:
    payload = _object(value, "proxy_request")
    fields = {
        "contract_version", "request_id", "requested_at", "endpoint_category", "method_category", "target",
        "authentication", "authorization", "requested_signals", "parameters", "payload_size_bytes", "proxy_version",
        "adapter_version", "policy_version", "configuration_version",
    }
    _keys(payload, fields, "proxy_request")
    return ProxyRequest(
        _version(payload["contract_version"], "proxy_request.contract_version"),
        _string(payload["request_id"], "proxy_request.request_id"),
        _string(payload["requested_at"], "proxy_request.requested_at"),
        _enum(ProxyEndpointCategory, payload["endpoint_category"], "proxy_request.endpoint_category"),
        _enum(ProxyMethodCategory, payload["method_category"], "proxy_request.method_category"),
        target_from_dict(payload["target"]),
        authentication_from_dict(payload["authentication"]),
        authorization_from_dict(payload["authorization"]),
        _strings(payload["requested_signals"], "proxy_request.requested_signals"),
        tuple(parameter_from_dict(item) for item in _array(payload["parameters"], "proxy_request.parameters")),
        _integer(payload["payload_size_bytes"], "proxy_request.payload_size_bytes"),
        _string(payload["proxy_version"], "proxy_request.proxy_version"),
        _string(payload["adapter_version"], "proxy_request.adapter_version"),
        _string(payload["policy_version"], "proxy_request.policy_version"),
        _string(payload["configuration_version"], "proxy_request.configuration_version"),
    )


def request_from_json(text: str) -> ProxyRequest:
    return request_from_dict(load_json(text, "proxy request", MAX_REQUEST_PAYLOAD_BYTES))


def request_to_json(request: ProxyRequest) -> str:
    return deterministic_json(request)


def policy_entry_from_dict(value: object) -> ProxyPolicyEntry:
    payload = _object(value, "policy_entry")
    fields = {"contract_version", "endpoint_category", "state", "allowed_methods"}
    _keys(payload, fields, "policy_entry")
    methods = tuple(_enum(ProxyMethodCategory, item, "policy_entry.allowed_methods") for item in _array(payload["allowed_methods"], "policy_entry.allowed_methods"))
    return ProxyPolicyEntry(
        _version(payload["contract_version"], "policy_entry.contract_version"),
        _enum(ProxyEndpointCategory, payload["endpoint_category"], "policy_entry.endpoint_category"),
        _enum(ProxyPolicyState, payload["state"], "policy_entry.state"),
        methods,
    )


def policy_from_dict(value: object) -> ProxyPolicy:
    payload = _object(value, "proxy_policy")
    fields = {"contract_version", "policy_version", "policy_digest", "entries", "default_state", "fixture_only"}
    _keys(payload, fields, "proxy_policy")
    return ProxyPolicy(
        _version(payload["contract_version"], "proxy_policy.contract_version"),
        _string(payload["policy_version"], "proxy_policy.policy_version"),
        _string(payload["policy_digest"], "proxy_policy.policy_digest"),
        tuple(policy_entry_from_dict(item) for item in _array(payload["entries"], "proxy_policy.entries")),
        _enum(ProxyPolicyState, payload["default_state"], "proxy_policy.default_state"),
        _boolean(payload["fixture_only"], "proxy_policy.fixture_only"),
    )


def policy_from_json(text: str) -> ProxyPolicy:
    return policy_from_dict(load_json(text, "proxy policy", MAX_RESPONSE_PAYLOAD_BYTES))


def policy_to_json(policy: ProxyPolicy) -> str:
    return deterministic_json(policy)


def configuration_from_dict(value: object) -> ProxyConfiguration:
    payload = _object(value, "proxy_configuration")
    fields = {
        "contract_version", "configuration_version", "configuration_digest", "maximum_request_payload_bytes",
        "maximum_response_payload_bytes", "maximum_response_records", "require_authentication", "require_exact_target",
        "allow_streaming", "allow_networking", "allow_runtime_access", "fixture_only", "activation_status",
    }
    _keys(payload, fields, "proxy_configuration")
    return ProxyConfiguration(
        _version(payload["contract_version"], "proxy_configuration.contract_version"),
        _string(payload["configuration_version"], "proxy_configuration.configuration_version"),
        _string(payload["configuration_digest"], "proxy_configuration.configuration_digest"),
        _integer(payload["maximum_request_payload_bytes"], "proxy_configuration.maximum_request_payload_bytes"),
        _integer(payload["maximum_response_payload_bytes"], "proxy_configuration.maximum_response_payload_bytes"),
        _integer(payload["maximum_response_records"], "proxy_configuration.maximum_response_records"),
        _boolean(payload["require_authentication"], "proxy_configuration.require_authentication"),
        _boolean(payload["require_exact_target"], "proxy_configuration.require_exact_target"),
        _boolean(payload["allow_streaming"], "proxy_configuration.allow_streaming"),
        _boolean(payload["allow_networking"], "proxy_configuration.allow_networking"),
        _boolean(payload["allow_runtime_access"], "proxy_configuration.allow_runtime_access"),
        _boolean(payload["fixture_only"], "proxy_configuration.fixture_only"),
        _string(payload["activation_status"], "proxy_configuration.activation_status"),
    )


def configuration_from_json(text: str) -> ProxyConfiguration:
    return configuration_from_dict(load_json(text, "proxy configuration", MAX_RESPONSE_PAYLOAD_BYTES))


def configuration_to_json(configuration: ProxyConfiguration) -> str:
    return deterministic_json(configuration)


def capability_from_dict(value: object) -> ProxyCapabilityDeclaration:
    payload = _object(value, "proxy_capability")
    fields = {
        "contract_version", "capability_version", "proxy_version", "adapter_version", "policy_version",
        "configuration_version", "supported_endpoint_categories", "supported_method_categories",
        "supported_authentication_modes", "fixture_only", "live_access_supported", "networking_supported", "socket_access_supported",
    }
    _keys(payload, fields, "proxy_capability")
    return ProxyCapabilityDeclaration(
        _version(payload["contract_version"], "proxy_capability.contract_version"),
        _string(payload["capability_version"], "proxy_capability.capability_version"),
        _string(payload["proxy_version"], "proxy_capability.proxy_version"),
        _string(payload["adapter_version"], "proxy_capability.adapter_version"),
        _string(payload["policy_version"], "proxy_capability.policy_version"),
        _string(payload["configuration_version"], "proxy_capability.configuration_version"),
        tuple(_enum(ProxyEndpointCategory, item, "proxy_capability.supported_endpoint_categories") for item in _array(payload["supported_endpoint_categories"], "proxy_capability.supported_endpoint_categories")),
        tuple(_enum(ProxyMethodCategory, item, "proxy_capability.supported_method_categories") for item in _array(payload["supported_method_categories"], "proxy_capability.supported_method_categories")),
        tuple(_enum(ProxyAuthenticationMode, item, "proxy_capability.supported_authentication_modes") for item in _array(payload["supported_authentication_modes"], "proxy_capability.supported_authentication_modes")),
        _boolean(payload["fixture_only"], "proxy_capability.fixture_only"),
        _boolean(payload["live_access_supported"], "proxy_capability.live_access_supported"),
        _boolean(payload["networking_supported"], "proxy_capability.networking_supported"),
        _boolean(payload["socket_access_supported"], "proxy_capability.socket_access_supported"),
    )


def capability_from_json(text: str) -> ProxyCapabilityDeclaration:
    return capability_from_dict(load_json(text, "proxy capability", MAX_RESPONSE_PAYLOAD_BYTES))


def capability_to_json(capability: ProxyCapabilityDeclaration) -> str:
    return deterministic_json(capability)


def response_metadata_from_dict(value: object) -> ProxyResponseMetadata:
    payload = _object(value, "response_metadata")
    fields = {
        "contract_version", "request_id", "response_id", "observed_at", "completed_at", "target_subject_id",
        "registry_subject_reference", "proxy_version", "adapter_version", "policy_version", "configuration_version",
        "provenance_reference", "limitation_codes", "fixture_only",
    }
    _keys(payload, fields, "response_metadata")
    return ProxyResponseMetadata(
        _version(payload["contract_version"], "response_metadata.contract_version"),
        _string(payload["request_id"], "response_metadata.request_id"),
        _string(payload["response_id"], "response_metadata.response_id"),
        _string(payload["observed_at"], "response_metadata.observed_at"),
        _string(payload["completed_at"], "response_metadata.completed_at"),
        _string(payload["target_subject_id"], "response_metadata.target_subject_id"),
        _string(payload["registry_subject_reference"], "response_metadata.registry_subject_reference"),
        _string(payload["proxy_version"], "response_metadata.proxy_version"),
        _string(payload["adapter_version"], "response_metadata.adapter_version"),
        _string(payload["policy_version"], "response_metadata.policy_version"),
        _string(payload["configuration_version"], "response_metadata.configuration_version"),
        _string(payload["provenance_reference"], "response_metadata.provenance_reference"),
        _strings(payload["limitation_codes"], "response_metadata.limitation_codes"),
        _boolean(payload["fixture_only"], "response_metadata.fixture_only"),
    )


def response_record_from_dict(value: object) -> ProxyResponseRecord:
    payload = _object(value, "response_record")
    fields = {"contract_version", "signal_name", "value", "observed_at"}
    _keys(payload, fields, "response_record")
    record_value = payload["value"]
    if not isinstance(record_value, (str, int, float, bool)):
        raise ProxyDataError("response_record.value must be a scalar JSON value.")
    return ProxyResponseRecord(
        _version(payload["contract_version"], "response_record.contract_version"),
        _string(payload["signal_name"], "response_record.signal_name"),
        record_value,
        _string(payload["observed_at"], "response_record.observed_at"),
    )


def response_from_dict(value: object) -> ProxyResponse:
    payload = _object(value, "proxy_response")
    fields = {"contract_version", "metadata", "records", "payload_size_bytes"}
    _keys(payload, fields, "proxy_response")
    return ProxyResponse(
        _version(payload["contract_version"], "proxy_response.contract_version"),
        response_metadata_from_dict(payload["metadata"]),
        tuple(response_record_from_dict(item) for item in _array(payload["records"], "proxy_response.records")),
        _integer(payload["payload_size_bytes"], "proxy_response.payload_size_bytes"),
    )


def response_from_json(text: str) -> ProxyResponse:
    return response_from_dict(load_json(text, "proxy response", MAX_RESPONSE_PAYLOAD_BYTES))


def response_to_json(response: ProxyResponse) -> str:
    return deterministic_json(response)


def decision_to_json(decision: ProxyDecision) -> str:
    return deterministic_json(decision)


def failure_to_json(failure: ProxyFailure) -> str:
    return deterministic_json(failure)


def audit_to_json(event: ProxyAuditEvent) -> str:
    return deterministic_json(event)


def result_to_json(result: MockProxyResult) -> str:
    return deterministic_json(result)


def contract_summary_to_json(summary: Mapping[str, object]) -> str:
    return deterministic_json(summary)
