from __future__ import annotations

import json
from enum import Enum
from typing import Any, Mapping

from engineering.platform_eap.container_health import (
    ACTIVATION_STATUS,
    ASSESSMENT_VERSION,
    AssessmentEvidenceSummary,
    BUNDLE_VERSION,
    CompletenessStatus,
    Confidence,
    ContainerHealthDataError,
    ContainerParticipation,
    CollectionMethod,
    DeclaredContainerSubject,
    EvaluationBundle,
    FreshnessStatus,
    HealthCheckRequirement,
    HealthStatus,
    IdentityMatchMethod,
    OperationalEvidence,
    OperationalHealthAssessment,
    ReconciliationOutcome,
    ReconciliationRecord,
    RejectedEvidence,
    UnsupportedContractVersion,
)


def _object(value: object, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ContainerHealthDataError(f"{context} must be a JSON object.")
    return value


def _keys(payload: Mapping[str, Any], required: set[str], optional: set[str], context: str) -> None:
    missing = sorted(required - payload.keys())
    unknown = sorted(payload.keys() - required - optional)
    if missing:
        raise ContainerHealthDataError(f"{context} is missing required fields: {', '.join(missing)}.")
    if unknown:
        raise ContainerHealthDataError(f"{context} contains unknown or unsafe fields: {', '.join(unknown)}.")


def _string(value: object, context: str) -> str:
    if not isinstance(value, str):
        raise ContainerHealthDataError(f"{context} must be a string.")
    return value


def _optional_string(value: object, context: str) -> str | None:
    if value is None:
        return None
    return _string(value, context)


def _integer(value: object, context: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ContainerHealthDataError(f"{context} must be an integer.")
    return value


def _boolean(value: object, context: str) -> bool:
    if not isinstance(value, bool):
        raise ContainerHealthDataError(f"{context} must be a boolean.")
    return value


def _strings(value: object, context: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ContainerHealthDataError(f"{context} must be an array of strings.")
    return tuple(value)


def _enum(enum_type: type[Enum], value: object, context: str):
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ContainerHealthDataError(f"{context} contains an unsupported value: {value!r}.") from exc


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ContainerHealthDataError(f"Duplicate JSON field is prohibited: {key}.")
        result[key] = value
    return result


def _load(text: str, context: str) -> object:
    try:
        return json.loads(text, object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise ContainerHealthDataError(f"{context} is not valid JSON: {exc.msg}.") from exc


def declared_subject_from_dict(value: object, context: str = "declared_subject") -> DeclaredContainerSubject:
    payload = _object(value, context)
    required = {
        "subject_id", "registry_reference", "environment", "participation", "host_reference", "compose_project",
        "compose_service", "governed_runtime_name", "expected_image_reference", "expected_image_digest", "health_check_requirement", "policy_reference", "fixture_only",
    }
    _keys(payload, required, set(), context)
    return DeclaredContainerSubject(
        _string(payload["subject_id"], f"{context}.subject_id"),
        _string(payload["registry_reference"], f"{context}.registry_reference"),
        _string(payload["environment"], f"{context}.environment"),
        _enum(ContainerParticipation, payload["participation"], f"{context}.participation"),
        _optional_string(payload["host_reference"], f"{context}.host_reference"),
        _optional_string(payload["compose_project"], f"{context}.compose_project"),
        _optional_string(payload["compose_service"], f"{context}.compose_service"),
        _optional_string(payload["governed_runtime_name"], f"{context}.governed_runtime_name"),
        _optional_string(payload["expected_image_reference"], f"{context}.expected_image_reference"),
        _optional_string(payload["expected_image_digest"], f"{context}.expected_image_digest"),
        _enum(HealthCheckRequirement, payload["health_check_requirement"], f"{context}.health_check_requirement"),
        _string(payload["policy_reference"], f"{context}.policy_reference"),
        _boolean(payload["fixture_only"], f"{context}.fixture_only"),
    )


def declared_subject_to_dict(subject: DeclaredContainerSubject) -> dict[str, object]:
    return {
        "subject_id": subject.subject_id,
        "registry_reference": subject.registry_reference,
        "environment": subject.environment,
        "participation": subject.participation.value,
        "host_reference": subject.host_reference,
        "compose_project": subject.compose_project,
        "compose_service": subject.compose_service,
        "governed_runtime_name": subject.governed_runtime_name,
        "expected_image_reference": subject.expected_image_reference,
        "expected_image_digest": subject.expected_image_digest,
        "health_check_requirement": subject.health_check_requirement.value,
        "policy_reference": subject.policy_reference,
        "fixture_only": subject.fixture_only,
    }


_EVIDENCE_FIELDS = {
    "contract_version", "profile_type", "profile_version", "evidence_id", "subject_id", "subject_type",
    "registry_reference", "environment", "evidence_type", "signal_name", "value", "value_type", "unit",
    "observed_at", "collected_at", "normalized_at", "observation_window_start", "observation_window_end",
    "provider_type", "provider_id", "provider_version", "adapter_version", "source_reference",
    "runtime_subject_reference", "identity_match_method", "collection_method", "freshness_status", "freshness_policy_id",
    "maximum_age_seconds", "evaluated_age_seconds", "completeness_status", "required_attributes",
    "missing_attributes", "coverage_reference", "evidence_confidence", "confidence_reason_codes", "finding_codes",
    "container_service_reference", "host_reference", "runtime_name", "runtime_container_id", "runtime_engine", "orchestrator",
}


def evidence_from_dict(value: object, context: str = "evidence") -> OperationalEvidence:
    payload = _object(value, context)
    _keys(payload, _EVIDENCE_FIELDS, set(), context)
    contract_version = _string(payload["contract_version"], f"{context}.contract_version")
    profile_version = _string(payload["profile_version"], f"{context}.profile_version")
    if not contract_version.startswith("1.") or not profile_version.startswith("1."):
        raise UnsupportedContractVersion(f"{context} uses an unsupported contract/profile major version.")
    raw_value = payload["value"]
    if not isinstance(raw_value, (str, int, float, bool)):
        raise ContainerHealthDataError(f"{context}.value must be a scalar JSON value.")
    return OperationalEvidence(
        contract_version, _string(payload["profile_type"], f"{context}.profile_type"), profile_version,
        _string(payload["evidence_id"], f"{context}.evidence_id"), _string(payload["subject_id"], f"{context}.subject_id"),
        _string(payload["subject_type"], f"{context}.subject_type"),
        _string(payload["registry_reference"], f"{context}.registry_reference"), _string(payload["environment"], f"{context}.environment"),
        _string(payload["evidence_type"], f"{context}.evidence_type"), _string(payload["signal_name"], f"{context}.signal_name"),
        raw_value, _string(payload["value_type"], f"{context}.value_type"), _optional_string(payload["unit"], f"{context}.unit"),
        _string(payload["observed_at"], f"{context}.observed_at"), _string(payload["collected_at"], f"{context}.collected_at"),
        _string(payload["normalized_at"], f"{context}.normalized_at"),
        _optional_string(payload["observation_window_start"], f"{context}.observation_window_start"),
        _optional_string(payload["observation_window_end"], f"{context}.observation_window_end"),
        _string(payload["provider_type"], f"{context}.provider_type"), _string(payload["provider_id"], f"{context}.provider_id"),
        _string(payload["provider_version"], f"{context}.provider_version"), _string(payload["adapter_version"], f"{context}.adapter_version"),
        _string(payload["source_reference"], f"{context}.source_reference"),
        _optional_string(payload["runtime_subject_reference"], f"{context}.runtime_subject_reference"),
        _enum(IdentityMatchMethod, payload["identity_match_method"], f"{context}.identity_match_method"),
        _enum(CollectionMethod, payload["collection_method"], f"{context}.collection_method"),
        _enum(FreshnessStatus, payload["freshness_status"], f"{context}.freshness_status"),
        _string(payload["freshness_policy_id"], f"{context}.freshness_policy_id"),
        _integer(payload["maximum_age_seconds"], f"{context}.maximum_age_seconds"),
        _integer(payload["evaluated_age_seconds"], f"{context}.evaluated_age_seconds"),
        _enum(CompletenessStatus, payload["completeness_status"], f"{context}.completeness_status"),
        _strings(payload["required_attributes"], f"{context}.required_attributes"),
        _strings(payload["missing_attributes"], f"{context}.missing_attributes"),
        _optional_string(payload["coverage_reference"], f"{context}.coverage_reference"),
        _enum(Confidence, payload["evidence_confidence"], f"{context}.evidence_confidence"),
        _strings(payload["confidence_reason_codes"], f"{context}.confidence_reason_codes"),
        _strings(payload["finding_codes"], f"{context}.finding_codes"),
        _string(payload["container_service_reference"], f"{context}.container_service_reference"),
        _string(payload["host_reference"], f"{context}.host_reference"),
        _optional_string(payload["runtime_name"], f"{context}.runtime_name"),
        _optional_string(payload["runtime_container_id"], f"{context}.runtime_container_id"),
        _string(payload["runtime_engine"], f"{context}.runtime_engine"),
        _optional_string(payload["orchestrator"], f"{context}.orchestrator"),
    )


def evidence_to_dict(evidence: OperationalEvidence) -> dict[str, object]:
    payload: dict[str, object] = {}
    for field, value in evidence.__dict__.items():
        if isinstance(value, Enum):
            payload[field] = value.value
        elif isinstance(value, tuple):
            payload[field] = list(value)
        else:
            payload[field] = value
    return payload


def evidence_from_json(text: str) -> OperationalEvidence:
    return evidence_from_dict(_load(text, "Operational Evidence"))


def evidence_to_json(evidence: OperationalEvidence) -> str:
    return json.dumps(evidence_to_dict(evidence), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def bundle_from_dict(value: object) -> EvaluationBundle:
    payload = _object(value, "evaluation_bundle")
    required = {"bundle_version", "fixture_only", "activation_status", "evaluated_at", "registry_records_root", "declared_subject", "evidence"}
    _keys(payload, required, set(), "evaluation_bundle")
    version = _string(payload["bundle_version"], "evaluation_bundle.bundle_version")
    if version != BUNDLE_VERSION:
        raise UnsupportedContractVersion(f"Unsupported evaluation bundle version: {version}.")
    evidence_values = payload["evidence"]
    if not isinstance(evidence_values, list):
        raise ContainerHealthDataError("evaluation_bundle.evidence must be an array.")
    return EvaluationBundle(
        version,
        _boolean(payload["fixture_only"], "evaluation_bundle.fixture_only"),
        _string(payload["activation_status"], "evaluation_bundle.activation_status"),
        _string(payload["evaluated_at"], "evaluation_bundle.evaluated_at"),
        _string(payload["registry_records_root"], "evaluation_bundle.registry_records_root"),
        declared_subject_from_dict(payload["declared_subject"]),
        tuple(evidence_from_dict(item, f"evaluation_bundle.evidence[{index}]") for index, item in enumerate(evidence_values)),
    )


def bundle_from_json(text: str) -> EvaluationBundle:
    bundle = bundle_from_dict(_load(text, "evaluation bundle"))
    if not bundle.fixture_only or bundle.activation_status != ACTIVATION_STATUS:
        raise ContainerHealthDataError("Evaluation bundle must remain fixture-only and not activated.")
    return bundle


def reconciliation_to_dict(record: ReconciliationRecord) -> dict[str, object]:
    return {
        "reconciliation_id": record.reconciliation_id,
        "contract_version": record.contract_version,
        "policy_version": record.policy_version,
        "policy_manifest_id": record.policy_manifest_id,
        "policy_manifest_version": record.policy_manifest_version,
        "subject_id": record.subject_id,
        "registry_reference": record.registry_reference,
        "evidence_ids": list(record.evidence_ids),
        "result": record.result.value,
        "match_method": record.match_method.value if record.match_method is not None else None,
        "reason_codes": list(record.reason_codes),
        "reconciled_at": record.reconciled_at,
        "unresolved_conflicts": list(record.unresolved_conflicts),
        "selected_evidence_ids": list(record.selected_evidence_ids),
        "rejected_evidence": [
            {"evidence_id": item.evidence_id, "reason_code": item.reason_code} for item in record.rejected_evidence
        ],
    }


def reconciliation_to_json(record: ReconciliationRecord) -> str:
    return json.dumps(reconciliation_to_dict(record), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def reconciliation_from_dict(value: object) -> ReconciliationRecord:
    payload = _object(value, "reconciliation")
    required = {
        "reconciliation_id", "contract_version", "policy_version", "policy_manifest_id", "policy_manifest_version",
        "subject_id", "registry_reference", "evidence_ids", "result", "match_method", "reason_codes", "reconciled_at",
        "unresolved_conflicts", "selected_evidence_ids", "rejected_evidence",
    }
    _keys(payload, required, set(), "reconciliation")
    rejected_raw = payload["rejected_evidence"]
    if not isinstance(rejected_raw, list):
        raise ContainerHealthDataError("reconciliation.rejected_evidence must be an array.")
    rejected = []
    for index, item in enumerate(rejected_raw):
        item_payload = _object(item, f"reconciliation.rejected_evidence[{index}]")
        _keys(item_payload, {"evidence_id", "reason_code"}, set(), f"reconciliation.rejected_evidence[{index}]")
        rejected.append(RejectedEvidence(_string(item_payload["evidence_id"], "evidence_id"), _string(item_payload["reason_code"], "reason_code")))
    return ReconciliationRecord(
        _string(payload["reconciliation_id"], "reconciliation.reconciliation_id"),
        _string(payload["contract_version"], "reconciliation.contract_version"),
        _string(payload["policy_version"], "reconciliation.policy_version"),
        _string(payload["policy_manifest_id"], "reconciliation.policy_manifest_id"),
        _string(payload["policy_manifest_version"], "reconciliation.policy_manifest_version"),
        _string(payload["subject_id"], "reconciliation.subject_id"),
        _string(payload["registry_reference"], "reconciliation.registry_reference"),
        _strings(payload["evidence_ids"], "reconciliation.evidence_ids"),
        _enum(ReconciliationOutcome, payload["result"], "reconciliation.result"),
        _enum(IdentityMatchMethod, payload["match_method"], "reconciliation.match_method") if payload["match_method"] is not None else None,
        _strings(payload["reason_codes"], "reconciliation.reason_codes"),
        _string(payload["reconciled_at"], "reconciliation.reconciled_at"),
        _strings(payload["unresolved_conflicts"], "reconciliation.unresolved_conflicts"),
        _strings(payload["selected_evidence_ids"], "reconciliation.selected_evidence_ids"),
        tuple(rejected),
    )


def reconciliation_from_json(text: str) -> ReconciliationRecord:
    return reconciliation_from_dict(_load(text, "Container Reconciliation Record"))


def assessment_to_dict(assessment: OperationalHealthAssessment) -> dict[str, object]:
    return {
        "assessment_id": assessment.assessment_id,
        "contract_version": assessment.contract_version,
        "subject_id": assessment.subject_id,
        "registry_reference": assessment.registry_reference,
        "evidence_profile_type": assessment.evidence_profile_type,
        "evidence_profile_version": assessment.evidence_profile_version,
        "policy_manifest_id": assessment.policy_manifest_id,
        "policy_manifest_version": assessment.policy_manifest_version,
        "policy_versions": list(assessment.policy_versions),
        "health_policy_version": assessment.health_policy_version,
        "assessment_confidence_policy_version": assessment.assessment_confidence_policy_version,
        "reconciliation_id": assessment.reconciliation_id,
        "reconciliation_result": assessment.reconciliation_result.value,
        "evidence_ids": list(assessment.evidence_ids),
        "evidence_summary": [
            {
                "evidence_id": item.evidence_id,
                "signal_name": item.signal_name,
                "role": item.role,
                "freshness_status": item.freshness_status.value,
                "evidence_confidence": item.evidence_confidence.value,
                "observed_at": item.observed_at,
                "expires_at": item.expires_at,
                "finding_codes": list(item.finding_codes),
            }
            for item in assessment.evidence_summary
        ],
        "health_status": assessment.health_status.value,
        "assessment_confidence": assessment.assessment_confidence.value,
        "reason_codes": list(assessment.reason_codes),
        "critical_findings": list(assessment.critical_findings),
        "noncritical_findings": list(assessment.noncritical_findings),
        "evaluated_at": assessment.evaluated_at,
        "valid_until": assessment.valid_until,
        "fixture_only": assessment.fixture_only,
        "activation_status": assessment.activation_status,
    }


def assessment_from_dict(value: object) -> OperationalHealthAssessment:
    payload = _object(value, "assessment")
    required = {
        "assessment_id", "contract_version", "subject_id", "registry_reference", "evidence_profile_type", "evidence_profile_version", "policy_manifest_id",
        "policy_manifest_version", "policy_versions", "health_policy_version", "assessment_confidence_policy_version",
        "reconciliation_id", "reconciliation_result", "evidence_ids", "evidence_summary", "health_status", "assessment_confidence", "reason_codes",
        "critical_findings", "noncritical_findings", "evaluated_at", "valid_until", "fixture_only", "activation_status",
    }
    _keys(payload, required, set(), "assessment")
    version = _string(payload["contract_version"], "assessment.contract_version")
    if not version.startswith("1."):
        raise UnsupportedContractVersion("Unsupported Operational Health Assessment major version.")
    summary_raw = payload["evidence_summary"]
    if not isinstance(summary_raw, list):
        raise ContainerHealthDataError("assessment.evidence_summary must be an array.")
    summary: list[AssessmentEvidenceSummary] = []
    for index, value in enumerate(summary_raw):
        item = _object(value, f"assessment.evidence_summary[{index}]")
        _keys(
            item,
            {"evidence_id", "signal_name", "role", "freshness_status", "evidence_confidence", "observed_at", "expires_at", "finding_codes"},
            set(),
            f"assessment.evidence_summary[{index}]",
        )
        summary.append(AssessmentEvidenceSummary(
            _string(item["evidence_id"], "evidence_summary.evidence_id"),
            _string(item["signal_name"], "evidence_summary.signal_name"),
            _string(item["role"], "evidence_summary.role"),
            _enum(FreshnessStatus, item["freshness_status"], "evidence_summary.freshness_status"),
            _enum(Confidence, item["evidence_confidence"], "evidence_summary.evidence_confidence"),
            _string(item["observed_at"], "evidence_summary.observed_at"),
            _string(item["expires_at"], "evidence_summary.expires_at"),
            _strings(item["finding_codes"], "evidence_summary.finding_codes"),
        ))
    return OperationalHealthAssessment(
        _string(payload["assessment_id"], "assessment.assessment_id"), version,
        _string(payload["subject_id"], "assessment.subject_id"),
        _string(payload["registry_reference"], "assessment.registry_reference"),
        _string(payload["evidence_profile_type"], "assessment.evidence_profile_type"),
        _string(payload["evidence_profile_version"], "assessment.evidence_profile_version"),
        _string(payload["policy_manifest_id"], "assessment.policy_manifest_id"),
        _string(payload["policy_manifest_version"], "assessment.policy_manifest_version"),
        _strings(payload["policy_versions"], "assessment.policy_versions"),
        _string(payload["health_policy_version"], "assessment.health_policy_version"),
        _string(payload["assessment_confidence_policy_version"], "assessment.assessment_confidence_policy_version"),
        _string(payload["reconciliation_id"], "assessment.reconciliation_id"),
        _enum(ReconciliationOutcome, payload["reconciliation_result"], "assessment.reconciliation_result"),
        _strings(payload["evidence_ids"], "assessment.evidence_ids"),
        tuple(summary),
        _enum(HealthStatus, payload["health_status"], "assessment.health_status"),
        _enum(Confidence, payload["assessment_confidence"], "assessment.assessment_confidence"),
        _strings(payload["reason_codes"], "assessment.reason_codes"),
        _strings(payload["critical_findings"], "assessment.critical_findings"),
        _strings(payload["noncritical_findings"], "assessment.noncritical_findings"),
        _string(payload["evaluated_at"], "assessment.evaluated_at"),
        _optional_string(payload["valid_until"], "assessment.valid_until"),
        _boolean(payload["fixture_only"], "assessment.fixture_only"),
        _string(payload["activation_status"], "assessment.activation_status"),
    )


def assessment_from_json(text: str) -> OperationalHealthAssessment:
    return assessment_from_dict(_load(text, "Operational Health Assessment"))


def assessment_to_json(assessment: OperationalHealthAssessment) -> str:
    return json.dumps(assessment_to_dict(assessment), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
