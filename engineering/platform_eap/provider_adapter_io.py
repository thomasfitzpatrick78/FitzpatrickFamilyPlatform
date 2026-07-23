from __future__ import annotations

import json
from enum import Enum
from typing import Any, Mapping

from engineering.platform_eap.container_health import CollectionMethod, OperationalEvidence
from engineering.platform_eap.container_health_io import evidence_from_dict
from engineering.platform_eap.provider_adapter import (
    CONTRACT_VERSION,
    ACTIVATION_STATUS,
    AuthorizationContext,
    CoverageStatus,
    FindingSeverity,
    MandatorySignalSet,
    NormalizedSignal,
    ObservationMetadata,
    ObservationMode,
    ObservedIdentity,
    OptionalSignalSet,
    ProductionProviderAdapterIdentity,
    ProviderAdapterDataError,
    ProviderAvailability,
    ProviderCapabilityDeclaration,
    ProviderConfidence,
    ProviderCoverage,
    ProviderFailure,
    ProviderFailureCategory,
    ProviderFinding,
    ProviderLimitation,
    ProviderNormalizationResult,
    ProviderProvenance,
    ProviderRequest,
    ProviderResponse,
    ProviderResult,
    Retryability,
    TargetResolution,
    UnsupportedProviderContractVersion,
)


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ProviderAdapterDataError(f"Duplicate JSON field is prohibited: {key}.")
        result[key] = value
    return result


def load_json(text: str, context: str = "provider adapter document", maximum_bytes: int | None = None) -> object:
    encoded = text.encode("utf-8")
    if maximum_bytes is not None and len(encoded) > maximum_bytes:
        raise ProviderAdapterDataError(f"{context} exceeds the maximum payload size.")
    try:
        return json.loads(text, object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise ProviderAdapterDataError(f"{context} is not valid JSON: {exc.msg}.") from exc


def _object(value: object, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ProviderAdapterDataError(f"{context} must be a JSON object.")
    return value


def _keys(payload: Mapping[str, Any], required: set[str], optional: set[str], context: str) -> None:
    missing = sorted(required - payload.keys())
    unknown = sorted(payload.keys() - required - optional)
    if missing:
        raise ProviderAdapterDataError(f"{context} is missing required fields: {', '.join(missing)}.")
    if unknown:
        raise ProviderAdapterDataError(f"{context} contains unknown or unsafe fields: {', '.join(unknown)}.")


def _string(value: object, context: str) -> str:
    if not isinstance(value, str):
        raise ProviderAdapterDataError(f"{context} must be a string.")
    return value


def _optional_string(value: object, context: str) -> str | None:
    return None if value is None else _string(value, context)


def _boolean(value: object, context: str) -> bool:
    if not isinstance(value, bool):
        raise ProviderAdapterDataError(f"{context} must be a boolean.")
    return value


def _strings(value: object, context: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ProviderAdapterDataError(f"{context} must be an array of strings.")
    return tuple(value)


def _enum(enum_type: type[Enum], value: object, context: str):
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ProviderAdapterDataError(f"{context} contains an unsupported value: {value!r}.") from exc


def _version(value: object, context: str) -> str:
    version = _string(value, context)
    if version != CONTRACT_VERSION:
        raise UnsupportedProviderContractVersion(f"{context} uses unsupported version {version!r}.")
    return version


def _model_to_primitive(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [_model_to_primitive(item) for item in value]
    if hasattr(value, "__dataclass_fields__"):
        return {field: _model_to_primitive(item) for field, item in value.__dict__.items()}
    return value


def _to_json(value: object) -> str:
    return json.dumps(_model_to_primitive(value), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def adapter_identity_from_dict(value: object) -> ProductionProviderAdapterIdentity:
    payload = _object(value, "adapter_identity")
    fields = {
        "contract_version", "adapter_id", "adapter_name", "adapter_version", "adapter_artifact_digest",
        "provider_type", "provider_api_version", "supported_provider_versions",
        "supported_evidence_contract_versions", "supported_profile_versions", "supported_signal_names",
        "configuration_digest", "fixture_only", "activation_status",
    }
    _keys(payload, fields, set(), "adapter_identity")
    return ProductionProviderAdapterIdentity(
        _version(payload["contract_version"], "adapter_identity.contract_version"),
        _string(payload["adapter_id"], "adapter_identity.adapter_id"),
        _string(payload["adapter_name"], "adapter_identity.adapter_name"),
        _string(payload["adapter_version"], "adapter_identity.adapter_version"),
        _string(payload["adapter_artifact_digest"], "adapter_identity.adapter_artifact_digest"),
        _string(payload["provider_type"], "adapter_identity.provider_type"),
        _string(payload["provider_api_version"], "adapter_identity.provider_api_version"),
        _strings(payload["supported_provider_versions"], "adapter_identity.supported_provider_versions"),
        _strings(payload["supported_evidence_contract_versions"], "adapter_identity.supported_evidence_contract_versions"),
        _strings(payload["supported_profile_versions"], "adapter_identity.supported_profile_versions"),
        _strings(payload["supported_signal_names"], "adapter_identity.supported_signal_names"),
        _string(payload["configuration_digest"], "adapter_identity.configuration_digest"),
        _boolean(payload["fixture_only"], "adapter_identity.fixture_only"),
        _string(payload["activation_status"], "adapter_identity.activation_status"),
    )


def mandatory_signal_set_from_dict(value: object) -> MandatorySignalSet:
    payload = _object(value, "mandatory_signal_set")
    _keys(payload, {"contract_version", "signals"}, set(), "mandatory_signal_set")
    return MandatorySignalSet(_version(payload["contract_version"], "mandatory_signal_set.contract_version"), _strings(payload["signals"], "mandatory_signal_set.signals"))


def optional_signal_set_from_dict(value: object) -> OptionalSignalSet:
    payload = _object(value, "optional_signal_set")
    _keys(payload, {"contract_version", "signals"}, set(), "optional_signal_set")
    return OptionalSignalSet(_version(payload["contract_version"], "optional_signal_set.contract_version"), _strings(payload["signals"], "optional_signal_set.signals"))


def authorization_context_from_dict(value: object) -> AuthorizationContext:
    payload = _object(value, "authorization_context")
    fields = {
        "contract_version", "authorization_reference", "authorization_digest", "authorization_valid_from",
        "authorization_valid_until", "observation_mode", "subject_id", "registry_reference",
        "registry_record_digest", "host_reference", "compose_project", "compose_service",
        "governed_runtime_name", "expected_image_reference", "expected_image_digest",
        "health_check_requirement", "provider_boundary_reference", "provider_boundary_digest",
        "output_reference", "fixture_only", "activation_status",
    }
    _keys(payload, fields, set(), "authorization_context")
    return AuthorizationContext(
        _version(payload["contract_version"], "authorization_context.contract_version"),
        _string(payload["authorization_reference"], "authorization_context.authorization_reference"),
        _string(payload["authorization_digest"], "authorization_context.authorization_digest"),
        _string(payload["authorization_valid_from"], "authorization_context.authorization_valid_from"),
        _string(payload["authorization_valid_until"], "authorization_context.authorization_valid_until"),
        _enum(ObservationMode, payload["observation_mode"], "authorization_context.observation_mode"),
        _string(payload["subject_id"], "authorization_context.subject_id"),
        _string(payload["registry_reference"], "authorization_context.registry_reference"),
        _string(payload["registry_record_digest"], "authorization_context.registry_record_digest"),
        _string(payload["host_reference"], "authorization_context.host_reference"),
        _optional_string(payload["compose_project"], "authorization_context.compose_project"),
        _optional_string(payload["compose_service"], "authorization_context.compose_service"),
        _optional_string(payload["governed_runtime_name"], "authorization_context.governed_runtime_name"),
        _optional_string(payload["expected_image_reference"], "authorization_context.expected_image_reference"),
        _optional_string(payload["expected_image_digest"], "authorization_context.expected_image_digest"),
        _string(payload["health_check_requirement"], "authorization_context.health_check_requirement"),
        _string(payload["provider_boundary_reference"], "authorization_context.provider_boundary_reference"),
        _string(payload["provider_boundary_digest"], "authorization_context.provider_boundary_digest"),
        _string(payload["output_reference"], "authorization_context.output_reference"),
        _boolean(payload["fixture_only"], "authorization_context.fixture_only"),
        _string(payload["activation_status"], "authorization_context.activation_status"),
    )


def provider_request_from_dict(value: object) -> ProviderRequest:
    payload = _object(value, "provider_request")
    fields = {"contract_version", "request_id", "requested_at", "adapter_id", "authorization_context", "mandatory_signal_set", "optional_signal_set"}
    _keys(payload, fields, set(), "provider_request")
    return ProviderRequest(
        _version(payload["contract_version"], "provider_request.contract_version"),
        _string(payload["request_id"], "provider_request.request_id"),
        _string(payload["requested_at"], "provider_request.requested_at"),
        _string(payload["adapter_id"], "provider_request.adapter_id"),
        authorization_context_from_dict(payload["authorization_context"]),
        mandatory_signal_set_from_dict(payload["mandatory_signal_set"]),
        optional_signal_set_from_dict(payload["optional_signal_set"]),
    )


def provider_request_from_json(text: str) -> ProviderRequest:
    return provider_request_from_dict(load_json(text, "provider request"))


def provider_request_to_json(request: ProviderRequest) -> str:
    return _to_json(request)


def capability_from_dict(value: object) -> ProviderCapabilityDeclaration:
    payload = _object(value, "provider_capability")
    fields = {
        "contract_version", "capability_version", "provider_type", "supported_provider_versions",
        "supported_adapter_versions", "supported_evidence_contract_versions", "supported_profile_versions",
        "supported_signals", "supported_identity_fields", "supported_observation_modes", "known_limitations",
        "fixture_only", "live_access_supported",
    }
    _keys(payload, fields, set(), "provider_capability")
    modes = payload["supported_observation_modes"]
    if not isinstance(modes, list):
        raise ProviderAdapterDataError("provider_capability.supported_observation_modes must be an array.")
    return ProviderCapabilityDeclaration(
        _version(payload["contract_version"], "provider_capability.contract_version"),
        _string(payload["capability_version"], "provider_capability.capability_version"),
        _string(payload["provider_type"], "provider_capability.provider_type"),
        _strings(payload["supported_provider_versions"], "provider_capability.supported_provider_versions"),
        _strings(payload["supported_adapter_versions"], "provider_capability.supported_adapter_versions"),
        _strings(payload["supported_evidence_contract_versions"], "provider_capability.supported_evidence_contract_versions"),
        _strings(payload["supported_profile_versions"], "provider_capability.supported_profile_versions"),
        _strings(payload["supported_signals"], "provider_capability.supported_signals"),
        _strings(payload["supported_identity_fields"], "provider_capability.supported_identity_fields"),
        tuple(_enum(ObservationMode, item, "provider_capability.supported_observation_modes") for item in modes),
        _strings(payload["known_limitations"], "provider_capability.known_limitations"),
        _boolean(payload["fixture_only"], "provider_capability.fixture_only"),
        _boolean(payload["live_access_supported"], "provider_capability.live_access_supported"),
    )


def capability_from_json(text: str) -> ProviderCapabilityDeclaration:
    return capability_from_dict(load_json(text, "provider capability"))


def capability_to_json(capability: ProviderCapabilityDeclaration) -> str:
    return _to_json(capability)


def adapter_identity_to_json(identity: ProductionProviderAdapterIdentity) -> str:
    return _to_json(identity)


def limitation_from_dict(value: object, context: str = "provider_limitation") -> ProviderLimitation:
    payload = _object(value, context)
    _keys(payload, {"limitation_code", "affected_signals", "material", "safe_reference"}, set(), context)
    return ProviderLimitation(
        _string(payload["limitation_code"], f"{context}.limitation_code"),
        _strings(payload["affected_signals"], f"{context}.affected_signals"),
        _boolean(payload["material"], f"{context}.material"),
        _string(payload["safe_reference"], f"{context}.safe_reference"),
    )


def provenance_from_dict(value: object) -> ProviderProvenance:
    payload = _object(value, "provider_provenance")
    fields = {"provider_type", "provider_id", "provider_version", "adapter_id", "adapter_version", "capability_version", "fixture_reference", "raw_response_digest"}
    _keys(payload, fields, set(), "provider_provenance")
    return ProviderProvenance(
        _string(payload["provider_type"], "provider_provenance.provider_type"),
        _string(payload["provider_id"], "provider_provenance.provider_id"),
        _string(payload["provider_version"], "provider_provenance.provider_version"),
        _string(payload["adapter_id"], "provider_provenance.adapter_id"),
        _string(payload["adapter_version"], "provider_provenance.adapter_version"),
        _string(payload["capability_version"], "provider_provenance.capability_version"),
        _string(payload["fixture_reference"], "provider_provenance.fixture_reference"),
        _string(payload["raw_response_digest"], "provider_provenance.raw_response_digest"),
    )


def coverage_from_dict(value: object) -> ProviderCoverage:
    payload = _object(value, "provider_coverage")
    fields = {"status", "requested_signals", "returned_signals", "missing_expected_signals", "unknown_signals"}
    _keys(payload, fields, set(), "provider_coverage")
    return ProviderCoverage(
        _enum(CoverageStatus, payload["status"], "provider_coverage.status"),
        _strings(payload["requested_signals"], "provider_coverage.requested_signals"),
        _strings(payload["returned_signals"], "provider_coverage.returned_signals"),
        _strings(payload["missing_expected_signals"], "provider_coverage.missing_expected_signals"),
        _strings(payload["unknown_signals"], "provider_coverage.unknown_signals"),
    )


def observation_metadata_from_dict(value: object) -> ObservationMetadata:
    payload = _object(value, "observation_metadata")
    fields = {"provider_observation_id", "correlation_id", "collection_started_at", "collection_ended_at", "observed_at", "observation_window_start", "observation_window_end"}
    _keys(payload, fields, set(), "observation_metadata")
    return ObservationMetadata(
        _string(payload["provider_observation_id"], "observation_metadata.provider_observation_id"),
        _string(payload["correlation_id"], "observation_metadata.correlation_id"),
        _string(payload["collection_started_at"], "observation_metadata.collection_started_at"),
        _string(payload["collection_ended_at"], "observation_metadata.collection_ended_at"),
        _string(payload["observed_at"], "observation_metadata.observed_at"),
        _optional_string(payload["observation_window_start"], "observation_metadata.observation_window_start"),
        _optional_string(payload["observation_window_end"], "observation_metadata.observation_window_end"),
    )


def observed_identity_from_dict(value: object) -> ObservedIdentity:
    payload = _object(value, "observed_identity")
    fields = {"target_resolution_result", "runtime_container_id", "runtime_name", "compose_project", "compose_service", "image_reference", "image_digest", "host_reference", "runtime_engine", "orchestrator"}
    _keys(payload, fields, set(), "observed_identity")
    return ObservedIdentity(
        _enum(TargetResolution, payload["target_resolution_result"], "observed_identity.target_resolution_result"),
        _optional_string(payload["runtime_container_id"], "observed_identity.runtime_container_id"),
        _optional_string(payload["runtime_name"], "observed_identity.runtime_name"),
        _optional_string(payload["compose_project"], "observed_identity.compose_project"),
        _optional_string(payload["compose_service"], "observed_identity.compose_service"),
        _optional_string(payload["image_reference"], "observed_identity.image_reference"),
        _optional_string(payload["image_digest"], "observed_identity.image_digest"),
        _optional_string(payload["host_reference"], "observed_identity.host_reference"),
        _string(payload["runtime_engine"], "observed_identity.runtime_engine"),
        _optional_string(payload["orchestrator"], "observed_identity.orchestrator"),
    )


def normalized_signal_from_dict(value: object, context: str = "normalized_signal") -> NormalizedSignal:
    payload = _object(value, context)
    fields = {"signal_name", "value", "value_type", "unit", "observed_at", "observation_window_start", "observation_window_end", "collection_method"}
    _keys(payload, fields, set(), context)
    scalar = payload["value"]
    if not isinstance(scalar, (str, int, float, bool)):
        raise ProviderAdapterDataError(f"{context}.value must be a scalar JSON value.")
    return NormalizedSignal(
        _string(payload["signal_name"], f"{context}.signal_name"),
        scalar,
        _string(payload["value_type"], f"{context}.value_type"),
        _optional_string(payload["unit"], f"{context}.unit"),
        _string(payload["observed_at"], f"{context}.observed_at"),
        _optional_string(payload["observation_window_start"], f"{context}.observation_window_start"),
        _optional_string(payload["observation_window_end"], f"{context}.observation_window_end"),
        _enum(CollectionMethod, payload["collection_method"], f"{context}.collection_method"),
    )


def provider_response_from_dict(value: object) -> ProviderResponse:
    payload = _object(value, "provider_response")
    fields = {"contract_version", "metadata", "observed_identity", "provenance", "coverage", "limitations", "provider_confidence", "provider_confidence_reasons", "warnings", "signals", "fixture_only", "activation_status"}
    _keys(payload, fields, set(), "provider_response")
    limitations = payload["limitations"]
    signals = payload["signals"]
    if not isinstance(limitations, list) or not isinstance(signals, list):
        raise ProviderAdapterDataError("provider_response limitations and signals must be arrays.")
    return ProviderResponse(
        _version(payload["contract_version"], "provider_response.contract_version"),
        observation_metadata_from_dict(payload["metadata"]),
        observed_identity_from_dict(payload["observed_identity"]),
        provenance_from_dict(payload["provenance"]),
        coverage_from_dict(payload["coverage"]),
        tuple(limitation_from_dict(item, f"provider_response.limitations[{index}]") for index, item in enumerate(limitations)),
        _enum(ProviderConfidence, payload["provider_confidence"], "provider_response.provider_confidence"),
        _strings(payload["provider_confidence_reasons"], "provider_response.provider_confidence_reasons"),
        _strings(payload["warnings"], "provider_response.warnings"),
        tuple(normalized_signal_from_dict(item, f"provider_response.signals[{index}]") for index, item in enumerate(signals)),
        _boolean(payload["fixture_only"], "provider_response.fixture_only"),
        _string(payload["activation_status"], "provider_response.activation_status"),
    )


def provider_response_from_json(text: str) -> ProviderResponse:
    return provider_response_from_dict(load_json(text, "provider response"))


def provider_response_to_json(response: ProviderResponse) -> str:
    return _to_json(response)


def provider_failure_from_dict(value: object) -> ProviderFailure:
    payload = _object(value, "provider_failure")
    fields = {"contract_version", "request_id", "failure_category", "failure_code", "safe_message", "retryability", "affected_signals", "provider_available", "target_resolution_result", "collection_started_at", "failed_at", "limitations", "audit_correlation_id", "fixture_only", "activation_status"}
    _keys(payload, fields, set(), "provider_failure")
    limitations = payload["limitations"]
    if not isinstance(limitations, list):
        raise ProviderAdapterDataError("provider_failure.limitations must be an array.")
    resolution = payload["target_resolution_result"]
    return ProviderFailure(
        _version(payload["contract_version"], "provider_failure.contract_version"),
        _string(payload["request_id"], "provider_failure.request_id"),
        _enum(ProviderFailureCategory, payload["failure_category"], "provider_failure.failure_category"),
        _string(payload["failure_code"], "provider_failure.failure_code"),
        _string(payload["safe_message"], "provider_failure.safe_message"),
        _enum(Retryability, payload["retryability"], "provider_failure.retryability"),
        _strings(payload["affected_signals"], "provider_failure.affected_signals"),
        _enum(ProviderAvailability, payload["provider_available"], "provider_failure.provider_available"),
        None if resolution is None else _enum(TargetResolution, resolution, "provider_failure.target_resolution_result"),
        _string(payload["collection_started_at"], "provider_failure.collection_started_at"),
        _string(payload["failed_at"], "provider_failure.failed_at"),
        tuple(limitation_from_dict(item, f"provider_failure.limitations[{index}]") for index, item in enumerate(limitations)),
        _string(payload["audit_correlation_id"], "provider_failure.audit_correlation_id"),
        _boolean(payload["fixture_only"], "provider_failure.fixture_only"),
        _string(payload["activation_status"], "provider_failure.activation_status"),
    )


def provider_failure_from_json(text: str) -> ProviderFailure:
    return provider_failure_from_dict(load_json(text, "provider failure"))


def provider_failure_to_json(failure: ProviderFailure) -> str:
    return _to_json(failure)


def provider_result_from_dict(value: object) -> ProviderResult:
    payload = _object(value, "provider_result")
    _keys(payload, {"contract_version", "observation_result", "failure_result"}, set(), "provider_result")
    return ProviderResult(
        _version(payload["contract_version"], "provider_result.contract_version"),
        None if payload["observation_result"] is None else provider_response_from_dict(payload["observation_result"]),
        None if payload["failure_result"] is None else provider_failure_from_dict(payload["failure_result"]),
    )


def provider_result_from_json(text: str) -> ProviderResult:
    return provider_result_from_dict(load_json(text, "provider result"))


def provider_result_to_json(result: ProviderResult) -> str:
    return _to_json(result)


def provider_normalization_result_from_dict(value: object) -> ProviderNormalizationResult:
    payload = _object(value, "normalization_result")
    fields = {"contract_version", "evidence_records", "failure_result", "limitations", "coverage", "unknown_signals", "findings"}
    _keys(payload, fields, set(), "normalization_result")
    evidence = payload["evidence_records"]
    limitations = payload["limitations"]
    findings = payload["findings"]
    if not isinstance(evidence, list) or not isinstance(limitations, list) or not isinstance(findings, list):
        raise ProviderAdapterDataError("normalization_result evidence, limitations, and findings must be arrays.")
    parsed_findings: list[ProviderFinding] = []
    for index, value in enumerate(findings):
        item = _object(value, f"normalization_result.findings[{index}]")
        _keys(item, {"severity", "code", "message", "reference"}, set(), f"normalization_result.findings[{index}]")
        parsed_findings.append(
            ProviderFinding(
                _enum(FindingSeverity, item["severity"], f"normalization_result.findings[{index}].severity"),
                _string(item["code"], f"normalization_result.findings[{index}].code"),
                _string(item["message"], f"normalization_result.findings[{index}].message"),
                _optional_string(item["reference"], f"normalization_result.findings[{index}].reference"),
            )
        )
    return ProviderNormalizationResult(
        _version(payload["contract_version"], "normalization_result.contract_version"),
        tuple(evidence_from_dict(item, f"normalization_result.evidence_records[{index}]") for index, item in enumerate(evidence)),
        None if payload["failure_result"] is None else provider_failure_from_dict(payload["failure_result"]),
        tuple(limitation_from_dict(item, f"normalization_result.limitations[{index}]") for index, item in enumerate(limitations)),
        None if payload["coverage"] is None else coverage_from_dict(payload["coverage"]),
        _strings(payload["unknown_signals"], "normalization_result.unknown_signals"),
        tuple(parsed_findings),
    )


def provider_normalization_result_from_json(text: str) -> ProviderNormalizationResult:
    return provider_normalization_result_from_dict(load_json(text, "normalization result"))


def provider_normalization_result_to_json(result: ProviderNormalizationResult) -> str:
    return _to_json(result)


def operational_evidence_to_json(evidence: OperationalEvidence) -> str:
    return _to_json(evidence)


def contract_summary_to_json(identity: ProductionProviderAdapterIdentity, capability: ProviderCapabilityDeclaration) -> str:
    payload = {
        "contract_version": CONTRACT_VERSION,
        "activation_status": ACTIVATION_STATUS,
        "adapter_identity": _model_to_primitive(identity),
        "capability_declaration": _model_to_primitive(capability),
        "result_types": ["observation_result", "failure_result"],
        "health_status_authority": "prohibited",
        "live_provider_mode": "absent",
    }
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
