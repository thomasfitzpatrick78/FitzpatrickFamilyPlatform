from __future__ import annotations

import json
from typing import Any, Mapping

from engineering.platform_eap.execution_capability import (
    MODEL_VERSION,
    ApprovalRecord,
    ApprovalRequirement,
    ApprovalStatus,
    CompletionPackage,
    EvidenceRecord,
    EvidenceRequirement,
    EvidenceType,
    ExecutionContext,
    ExecutionDataError,
    ExecutionResult,
    FindingSeverity,
    GovernedAssignment,
    GovernedRole,
    OutcomeStatus,
    Participant,
    ValidationFinding,
)


def _expect_object(value: object, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ExecutionDataError(f"{context} must be a JSON object.")
    return value


def _keys(payload: Mapping[str, Any], required: set[str], optional: set[str], context: str) -> None:
    missing = sorted(required - payload.keys())
    unknown = sorted(payload.keys() - required - optional)
    if missing:
        raise ExecutionDataError(f"{context} is missing required fields: {', '.join(missing)}.")
    if unknown:
        raise ExecutionDataError(f"{context} contains unknown or unsafe fields: {', '.join(unknown)}.")


def _string(value: object, context: str) -> str:
    if not isinstance(value, str):
        raise ExecutionDataError(f"{context} must be a string.")
    return value


def _optional_string(value: object, context: str) -> str | None:
    if value is None:
        return None
    return _string(value, context)


def _boolean(value: object, context: str) -> bool:
    if not isinstance(value, bool):
        raise ExecutionDataError(f"{context} must be a boolean.")
    return value


def _string_tuple(value: object, context: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ExecutionDataError(f"{context} must be an array of strings.")
    return tuple(value)


def _enum(enum_type: type[Enum], value: object, context: str) -> Any:
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ExecutionDataError(f"{context} contains an unsupported value: {value!r}.") from exc


def participant_from_dict(value: object, context: str = "participant") -> Participant:
    payload = _expect_object(value, context)
    _keys(payload, {"participant_id"}, set(), context)
    return Participant(_string(payload["participant_id"], f"{context}.participant_id"))


def evidence_requirement_from_dict(value: object, context: str) -> EvidenceRequirement:
    payload = _expect_object(value, context)
    _keys(payload, {"requirement_id", "evidence_type", "validation_requirement"}, set(), context)
    return EvidenceRequirement(
        _string(payload["requirement_id"], f"{context}.requirement_id"),
        _enum(EvidenceType, payload["evidence_type"], f"{context}.evidence_type"),
        _string(payload["validation_requirement"], f"{context}.validation_requirement"),
    )


def approval_requirement_from_dict(value: object, context: str) -> ApprovalRequirement:
    payload = _expect_object(value, context)
    _keys(payload, {"approval_id", "human_authority", "applies_to", "required"}, set(), context)
    return ApprovalRequirement(
        _string(payload["approval_id"], f"{context}.approval_id"),
        _string(payload["human_authority"], f"{context}.human_authority"),
        _string_tuple(payload["applies_to"], f"{context}.applies_to"),
        _boolean(payload["required"], f"{context}.required"),
    )


def assignment_from_dict(value: object) -> GovernedAssignment:
    payload = _expect_object(value, "assignment")
    required = {
        "model_version", "assignment_id", "title", "governed_role", "authorized_scope",
        "permitted_actions", "prohibited_actions", "required_validations", "required_evidence",
        "human_approval_requirements", "source_references",
    }
    _keys(payload, required, {"repository_baseline"}, "assignment")
    evidence_raw = payload["required_evidence"]
    approvals_raw = payload["human_approval_requirements"]
    if not isinstance(evidence_raw, list) or not isinstance(approvals_raw, list):
        raise ExecutionDataError("assignment evidence and approval requirements must be arrays.")
    return GovernedAssignment(
        model_version=_string(payload["model_version"], "assignment.model_version"),
        assignment_id=_string(payload["assignment_id"], "assignment.assignment_id"),
        title=_string(payload["title"], "assignment.title"),
        governed_role=_enum(GovernedRole, payload["governed_role"], "assignment.governed_role"),
        authorized_scope=_string_tuple(payload["authorized_scope"], "assignment.authorized_scope"),
        permitted_actions=_string_tuple(payload["permitted_actions"], "assignment.permitted_actions"),
        prohibited_actions=_string_tuple(payload["prohibited_actions"], "assignment.prohibited_actions"),
        required_validations=_string_tuple(payload["required_validations"], "assignment.required_validations"),
        required_evidence=tuple(evidence_requirement_from_dict(item, f"assignment.required_evidence[{index}]") for index, item in enumerate(evidence_raw)),
        human_approval_requirements=tuple(approval_requirement_from_dict(item, f"assignment.human_approval_requirements[{index}]") for index, item in enumerate(approvals_raw)),
        source_references=_string_tuple(payload["source_references"], "assignment.source_references"),
        repository_baseline=_optional_string(payload.get("repository_baseline"), "assignment.repository_baseline"),
    )


def approval_record_from_dict(value: object, context: str) -> ApprovalRecord:
    payload = _expect_object(value, context)
    _keys(payload, {"approval_id", "status"}, {"approved_by", "approved_at"}, context)
    return ApprovalRecord(
        _string(payload["approval_id"], f"{context}.approval_id"),
        _enum(ApprovalStatus, payload["status"], f"{context}.status"),
        _optional_string(payload.get("approved_by"), f"{context}.approved_by"),
        _optional_string(payload.get("approved_at"), f"{context}.approved_at"),
    )


def context_from_dict(value: object) -> ExecutionContext:
    payload = _expect_object(value, "execution_context")
    required = {"model_version", "participant", "governed_role", "assignment_id", "repository_identity", "branch", "starting_head", "working_tree_state", "execution_started_at", "approval_state"}
    _keys(payload, required, set(), "execution_context")
    approvals = payload["approval_state"]
    if not isinstance(approvals, list):
        raise ExecutionDataError("execution_context.approval_state must be an array.")
    return ExecutionContext(
        _string(payload["model_version"], "execution_context.model_version"),
        participant_from_dict(payload["participant"], "execution_context.participant"),
        _enum(GovernedRole, payload["governed_role"], "execution_context.governed_role"),
        _string(payload["assignment_id"], "execution_context.assignment_id"),
        _string(payload["repository_identity"], "execution_context.repository_identity"),
        _string(payload["branch"], "execution_context.branch"),
        _string(payload["starting_head"], "execution_context.starting_head"),
        _string(payload["working_tree_state"], "execution_context.working_tree_state"),
        _string(payload["execution_started_at"], "execution_context.execution_started_at"),
        tuple(approval_record_from_dict(item, f"execution_context.approval_state[{index}]") for index, item in enumerate(approvals)),
    )


def result_from_dict(value: object) -> ExecutionResult:
    payload = _expect_object(value, "execution_result")
    required = {"model_version", "assignment_id", "outcome_status", "summary", "actions_performed", "files_changed", "validations_executed", "evidence_ids", "unresolved_issues", "deviations_or_escalations", "completed_at"}
    _keys(payload, required, set(), "execution_result")
    return ExecutionResult(
        _string(payload["model_version"], "execution_result.model_version"),
        _string(payload["assignment_id"], "execution_result.assignment_id"),
        _enum(OutcomeStatus, payload["outcome_status"], "execution_result.outcome_status"),
        _string(payload["summary"], "execution_result.summary"),
        _string_tuple(payload["actions_performed"], "execution_result.actions_performed"),
        _string_tuple(payload["files_changed"], "execution_result.files_changed"),
        _string_tuple(payload["validations_executed"], "execution_result.validations_executed"),
        _string_tuple(payload["evidence_ids"], "execution_result.evidence_ids"),
        _string_tuple(payload["unresolved_issues"], "execution_result.unresolved_issues"),
        _string_tuple(payload["deviations_or_escalations"], "execution_result.deviations_or_escalations"),
        _string(payload["completed_at"], "execution_result.completed_at"),
    )


def evidence_from_dict(value: object, context: str) -> EvidenceRecord:
    payload = _expect_object(value, context)
    required = {"model_version", "evidence_id", "evidence_type", "source_activity", "result", "timestamp", "assignment_id", "validation_requirement"}
    _keys(payload, required, {"artifact_path"}, context)
    return EvidenceRecord(
        _string(payload["model_version"], f"{context}.model_version"),
        _string(payload["evidence_id"], f"{context}.evidence_id"),
        _enum(EvidenceType, payload["evidence_type"], f"{context}.evidence_type"),
        _string(payload["source_activity"], f"{context}.source_activity"),
        _string(payload["result"], f"{context}.result"),
        _string(payload["timestamp"], f"{context}.timestamp"),
        _string(payload["assignment_id"], f"{context}.assignment_id"),
        _string(payload["validation_requirement"], f"{context}.validation_requirement"),
        _optional_string(payload.get("artifact_path"), f"{context}.artifact_path"),
    )


def finding_from_dict(value: object, context: str) -> ValidationFinding:
    payload = _expect_object(value, context)
    _keys(payload, {"severity", "code", "message"}, {"path"}, context)
    return ValidationFinding(
        _enum(FindingSeverity, payload["severity"], f"{context}.severity"),
        _string(payload["code"], f"{context}.code"),
        _string(payload["message"], f"{context}.message"),
        _optional_string(payload.get("path"), f"{context}.path"),
    )


def completion_from_dict(value: object) -> CompletionPackage:
    payload = _expect_object(value, "completion")
    required = {
        "model_version", "assignment", "participant", "execution_context", "execution_result",
        "validation_findings", "evidence_inventory", "unresolved_decisions",
        "recommended_next_approval_gate", "commit_occurred", "push_occurred",
        "activation_occurred", "live_changes_occurred",
    }
    _keys(payload, required, set(), "completion")
    finding_values = payload["validation_findings"]
    evidence_values = payload["evidence_inventory"]
    if not isinstance(finding_values, list) or not isinstance(evidence_values, list):
        raise ExecutionDataError("completion validation findings and evidence inventory must be arrays.")
    return CompletionPackage(
        _string(payload["model_version"], "completion.model_version"),
        assignment_from_dict(payload["assignment"]),
        participant_from_dict(payload["participant"]),
        context_from_dict(payload["execution_context"]),
        result_from_dict(payload["execution_result"]),
        tuple(finding_from_dict(item, f"completion.validation_findings[{index}]") for index, item in enumerate(finding_values)),
        tuple(evidence_from_dict(item, f"completion.evidence_inventory[{index}]") for index, item in enumerate(evidence_values)),
        _string_tuple(payload["unresolved_decisions"], "completion.unresolved_decisions"),
        _string(payload["recommended_next_approval_gate"], "completion.recommended_next_approval_gate"),
        _boolean(payload["commit_occurred"], "completion.commit_occurred"),
        _boolean(payload["push_occurred"], "completion.push_occurred"),
        _boolean(payload["activation_occurred"], "completion.activation_occurred"),
        _boolean(payload["live_changes_occurred"], "completion.live_changes_occurred"),
    )


def assignment_from_json(text: str) -> GovernedAssignment:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ExecutionDataError(f"Assignment JSON is malformed: {exc.msg}.") from exc
    return assignment_from_dict(payload)


def completion_from_json(text: str) -> CompletionPackage:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ExecutionDataError(f"Completion JSON is malformed: {exc.msg}.") from exc
    return completion_from_dict(payload)


def _participant_dict(participant: Participant) -> dict[str, object]:
    return {"participant_id": participant.participant_id}


def assignment_to_dict(assignment: GovernedAssignment) -> dict[str, object]:
    payload: dict[str, object] = {
        "model_version": assignment.model_version,
        "assignment_id": assignment.assignment_id,
        "title": assignment.title,
        "governed_role": assignment.governed_role.value,
        "authorized_scope": list(assignment.authorized_scope),
        "permitted_actions": list(assignment.permitted_actions),
        "prohibited_actions": list(assignment.prohibited_actions),
        "required_validations": list(assignment.required_validations),
        "required_evidence": [
            {
                "requirement_id": requirement.requirement_id,
                "evidence_type": requirement.evidence_type.value,
                "validation_requirement": requirement.validation_requirement,
            }
            for requirement in assignment.required_evidence
        ],
        "human_approval_requirements": [
            {
                "approval_id": requirement.approval_id,
                "human_authority": requirement.human_authority,
                "applies_to": list(requirement.applies_to),
                "required": requirement.required,
            }
            for requirement in assignment.human_approval_requirements
        ],
        "source_references": list(assignment.source_references),
    }
    if assignment.repository_baseline is not None:
        payload["repository_baseline"] = assignment.repository_baseline
    return payload


def _context_dict(context: ExecutionContext) -> dict[str, object]:
    return {
        "model_version": context.model_version,
        "participant": _participant_dict(context.participant),
        "governed_role": context.governed_role.value,
        "assignment_id": context.assignment_id,
        "repository_identity": context.repository_identity,
        "branch": context.branch,
        "starting_head": context.starting_head,
        "working_tree_state": context.working_tree_state,
        "execution_started_at": context.execution_started_at,
        "approval_state": [
            {
                "approval_id": record.approval_id,
                "status": record.status.value,
                **({"approved_by": record.approved_by} if record.approved_by is not None else {}),
                **({"approved_at": record.approved_at} if record.approved_at is not None else {}),
            }
            for record in context.approval_state
        ],
    }


def _result_dict(result: ExecutionResult) -> dict[str, object]:
    return {
        "model_version": result.model_version,
        "assignment_id": result.assignment_id,
        "outcome_status": result.outcome_status.value,
        "summary": result.summary,
        "actions_performed": list(result.actions_performed),
        "files_changed": list(result.files_changed),
        "validations_executed": list(result.validations_executed),
        "evidence_ids": list(result.evidence_ids),
        "unresolved_issues": list(result.unresolved_issues),
        "deviations_or_escalations": list(result.deviations_or_escalations),
        "completed_at": result.completed_at,
    }


def _finding_dict(finding: ValidationFinding) -> dict[str, object]:
    payload: dict[str, object] = {"severity": finding.severity.value, "code": finding.code, "message": finding.message}
    if finding.path is not None:
        payload["path"] = finding.path
    return payload


def _evidence_dict(evidence: EvidenceRecord) -> dict[str, object]:
    payload: dict[str, object] = {
        "model_version": evidence.model_version,
        "evidence_id": evidence.evidence_id,
        "evidence_type": evidence.evidence_type.value,
        "source_activity": evidence.source_activity,
        "result": evidence.result,
        "timestamp": evidence.timestamp,
        "assignment_id": evidence.assignment_id,
        "validation_requirement": evidence.validation_requirement,
    }
    if evidence.artifact_path is not None:
        payload["artifact_path"] = evidence.artifact_path
    return payload


def completion_to_dict(package: CompletionPackage) -> dict[str, object]:
    return {
        "model_version": package.model_version,
        "assignment": assignment_to_dict(package.assignment),
        "participant": _participant_dict(package.participant),
        "execution_context": _context_dict(package.execution_context),
        "execution_result": _result_dict(package.execution_result),
        "validation_findings": [_finding_dict(finding) for finding in package.validation_findings],
        "evidence_inventory": [_evidence_dict(evidence) for evidence in package.evidence_inventory],
        "unresolved_decisions": list(package.unresolved_decisions),
        "recommended_next_approval_gate": package.recommended_next_approval_gate,
        "commit_occurred": package.commit_occurred,
        "push_occurred": package.push_occurred,
        "activation_occurred": package.activation_occurred,
        "live_changes_occurred": package.live_changes_occurred,
    }


def assignment_to_json(assignment: GovernedAssignment) -> str:
    return json.dumps(assignment_to_dict(assignment), indent=2, ensure_ascii=False) + "\n"


def completion_to_json(package: CompletionPackage) -> str:
    return json.dumps(completion_to_dict(package), indent=2, ensure_ascii=False) + "\n"
