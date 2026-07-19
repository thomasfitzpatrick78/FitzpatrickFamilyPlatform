from __future__ import annotations

import json
from enum import Enum
from typing import Any, Mapping

from engineering.platform_eap.automation_capability import (
    AutomationHandoff,
    AutomationLifecycleState,
    AutomationRunContext,
    AutomationStepType,
    FailurePolicy,
    GovernedAutomationDefinition,
    LiveImpact,
    OrchestrationStep,
    TransitionDecision,
    TransitionRequest,
)
from engineering.platform_eap.execution_capability import ExecutionDataError
from engineering.platform_eap.execution_io import (
    approval_record_from_dict,
    approval_requirement_from_dict,
    assignment_from_dict,
    assignment_to_dict,
    completion_from_dict,
    completion_to_dict,
)


class AutomationDataError(ExecutionDataError):
    """Raised when untrusted orchestration data is malformed."""


def _object(value: object, context: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise AutomationDataError(f"{context} must be a JSON object.")
    return value


def _keys(payload: Mapping[str, Any], required: set[str], optional: set[str], context: str) -> None:
    missing = sorted(required - set(payload))
    unknown = sorted(set(payload) - required - optional)
    if missing:
        raise AutomationDataError(f"{context} is missing required fields: {', '.join(missing)}.")
    if unknown:
        raise AutomationDataError(f"{context} contains unknown or unsafe fields: {', '.join(unknown)}.")


def _string(value: object, context: str) -> str:
    if not isinstance(value, str):
        raise AutomationDataError(f"{context} must be a string.")
    return value


def _optional_string(value: object, context: str) -> str | None:
    if value is None:
        return None
    return _string(value, context)


def _boolean(value: object, context: str) -> bool:
    if not isinstance(value, bool):
        raise AutomationDataError(f"{context} must be a boolean.")
    return value


def _array(value: object, context: str) -> list[object]:
    if not isinstance(value, list):
        raise AutomationDataError(f"{context} must be an array.")
    return value


def _strings(value: object, context: str) -> tuple[str, ...]:
    return tuple(_string(item, f"{context}[{index}]") for index, item in enumerate(_array(value, context)))


def _enum(enum_type: type[Enum], value: object, context: str) -> Any:
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise AutomationDataError(f"{context} contains an unsupported value: {value!r}.") from exc


def step_from_dict(value: object, context: str) -> OrchestrationStep:
    payload = _object(value, context)
    required = {
        "step_id", "title", "step_type", "prerequisite_step_ids", "required_approval_ids",
        "required_evidence_types", "required_validation_outcomes", "allowed_next_step_ids",
        "stop_on_failure", "live_impact", "human_review_required",
    }
    optional = {"execution_assignment_reference", "execution_completion_reference"}
    _keys(payload, required, optional, context)
    from engineering.platform_eap.execution_capability import EvidenceType

    return OrchestrationStep(
        _string(payload["step_id"], f"{context}.step_id"),
        _string(payload["title"], f"{context}.title"),
        _enum(AutomationStepType, payload["step_type"], f"{context}.step_type"),
        _strings(payload["prerequisite_step_ids"], f"{context}.prerequisite_step_ids"),
        _strings(payload["required_approval_ids"], f"{context}.required_approval_ids"),
        _optional_string(payload.get("execution_assignment_reference"), f"{context}.execution_assignment_reference"),
        _optional_string(payload.get("execution_completion_reference"), f"{context}.execution_completion_reference"),
        tuple(_enum(EvidenceType, item, f"{context}.required_evidence_types[{index}]") for index, item in enumerate(_array(payload["required_evidence_types"], f"{context}.required_evidence_types"))),
        _strings(payload["required_validation_outcomes"], f"{context}.required_validation_outcomes"),
        _strings(payload["allowed_next_step_ids"], f"{context}.allowed_next_step_ids"),
        _boolean(payload["stop_on_failure"], f"{context}.stop_on_failure"),
        _enum(LiveImpact, payload["live_impact"], f"{context}.live_impact"),
        _boolean(payload["human_review_required"], f"{context}.human_review_required"),
    )


def definition_from_dict(value: object) -> GovernedAutomationDefinition:
    payload = _object(value, "automation_definition")
    required = {
        "model_version", "automation_id", "name", "purpose", "governing_artifact_references",
        "steps", "initial_lifecycle_state", "allowed_terminal_states", "human_approval_requirements",
        "failure_policy", "execution_assignment_references", "required_completion_references",
        "required_evidence_references", "live_impact", "authorized_repository_scope",
    }
    _keys(payload, required, set(), "automation_definition")
    steps = _array(payload["steps"], "automation_definition.steps")
    approvals = _array(payload["human_approval_requirements"], "automation_definition.human_approval_requirements")
    terminals = _array(payload["allowed_terminal_states"], "automation_definition.allowed_terminal_states")
    return GovernedAutomationDefinition(
        _string(payload["model_version"], "automation_definition.model_version"),
        _string(payload["automation_id"], "automation_definition.automation_id"),
        _string(payload["name"], "automation_definition.name"),
        _string(payload["purpose"], "automation_definition.purpose"),
        _strings(payload["governing_artifact_references"], "automation_definition.governing_artifact_references"),
        tuple(step_from_dict(item, f"automation_definition.steps[{index}]") for index, item in enumerate(steps)),
        _enum(AutomationLifecycleState, payload["initial_lifecycle_state"], "automation_definition.initial_lifecycle_state"),
        tuple(_enum(AutomationLifecycleState, item, f"automation_definition.allowed_terminal_states[{index}]") for index, item in enumerate(terminals)),
        tuple(approval_requirement_from_dict(item, f"automation_definition.human_approval_requirements[{index}]") for index, item in enumerate(approvals)),
        _enum(FailurePolicy, payload["failure_policy"], "automation_definition.failure_policy"),
        _strings(payload["execution_assignment_references"], "automation_definition.execution_assignment_references"),
        _strings(payload["required_completion_references"], "automation_definition.required_completion_references"),
        _strings(payload["required_evidence_references"], "automation_definition.required_evidence_references"),
        _enum(LiveImpact, payload["live_impact"], "automation_definition.live_impact"),
        _strings(payload["authorized_repository_scope"], "automation_definition.authorized_repository_scope"),
    )


def run_from_dict(value: object) -> AutomationRunContext:
    payload = _object(value, "automation_run")
    required = {
        "model_version", "definition", "run_id", "repository_identity", "branch", "starting_head",
        "working_tree_state", "run_started_at", "current_lifecycle_state", "current_step_id",
        "completed_step_ids", "approval_state", "assignments", "completions", "unresolved_issues",
        "escalation_state", "activation_occurred", "live_changes_occurred",
    }
    _keys(payload, required, set(), "automation_run")
    approvals = _array(payload["approval_state"], "automation_run.approval_state")
    assignments = _array(payload["assignments"], "automation_run.assignments")
    completions = _array(payload["completions"], "automation_run.completions")
    return AutomationRunContext(
        _string(payload["model_version"], "automation_run.model_version"),
        definition_from_dict(payload["definition"]),
        _string(payload["run_id"], "automation_run.run_id"),
        _string(payload["repository_identity"], "automation_run.repository_identity"),
        _string(payload["branch"], "automation_run.branch"),
        _string(payload["starting_head"], "automation_run.starting_head"),
        _string(payload["working_tree_state"], "automation_run.working_tree_state"),
        _string(payload["run_started_at"], "automation_run.run_started_at"),
        _enum(AutomationLifecycleState, payload["current_lifecycle_state"], "automation_run.current_lifecycle_state"),
        _string(payload["current_step_id"], "automation_run.current_step_id"),
        _strings(payload["completed_step_ids"], "automation_run.completed_step_ids"),
        tuple(approval_record_from_dict(item, f"automation_run.approval_state[{index}]") for index, item in enumerate(approvals)),
        tuple(assignment_from_dict(item) for item in assignments),
        tuple(completion_from_dict(item) for item in completions),
        _strings(payload["unresolved_issues"], "automation_run.unresolved_issues"),
        _string(payload["escalation_state"], "automation_run.escalation_state"),
        _boolean(payload["activation_occurred"], "automation_run.activation_occurred"),
        _boolean(payload["live_changes_occurred"], "automation_run.live_changes_occurred"),
    )


def transition_from_dict(value: object) -> TransitionRequest:
    payload = _object(value, "transition_request")
    _keys(payload, {"requested_lifecycle_state", "requested_step_id", "resolved_issue_ids"}, set(), "transition_request")
    return TransitionRequest(
        _enum(AutomationLifecycleState, payload["requested_lifecycle_state"], "transition_request.requested_lifecycle_state"),
        _string(payload["requested_step_id"], "transition_request.requested_step_id"),
        _strings(payload["resolved_issue_ids"], "transition_request.resolved_issue_ids"),
    )


def _load(text: str, context: str) -> object:
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise AutomationDataError(f"{context} JSON is malformed: {exc.msg}.") from exc


def definition_from_json(text: str) -> GovernedAutomationDefinition:
    return definition_from_dict(_load(text, "Automation definition"))


def run_from_json(text: str) -> AutomationRunContext:
    return run_from_dict(_load(text, "Automation run"))


def transition_from_json(text: str) -> TransitionRequest:
    return transition_from_dict(_load(text, "Transition request"))


def _approval_requirement_dict(value: object) -> dict[str, object]:
    requirement = value
    return {"approval_id": requirement.approval_id, "human_authority": requirement.human_authority, "applies_to": list(requirement.applies_to), "required": requirement.required}


def _approval_record_dict(record: object) -> dict[str, object]:
    payload: dict[str, object] = {"approval_id": record.approval_id, "status": record.status.value}
    if record.approved_by is not None:
        payload["approved_by"] = record.approved_by
    if record.approved_at is not None:
        payload["approved_at"] = record.approved_at
    return payload


def step_to_dict(step: OrchestrationStep) -> dict[str, object]:
    payload: dict[str, object] = {
        "step_id": step.step_id,
        "title": step.title,
        "step_type": step.step_type.value,
        "prerequisite_step_ids": list(step.prerequisite_step_ids),
        "required_approval_ids": list(step.required_approval_ids),
        "required_evidence_types": [value.value for value in step.required_evidence_types],
        "required_validation_outcomes": list(step.required_validation_outcomes),
        "allowed_next_step_ids": list(step.allowed_next_step_ids),
        "stop_on_failure": step.stop_on_failure,
        "live_impact": step.live_impact.value,
        "human_review_required": step.human_review_required,
    }
    if step.execution_assignment_reference is not None:
        payload["execution_assignment_reference"] = step.execution_assignment_reference
    if step.execution_completion_reference is not None:
        payload["execution_completion_reference"] = step.execution_completion_reference
    return payload


def definition_to_dict(definition: GovernedAutomationDefinition) -> dict[str, object]:
    return {
        "model_version": definition.model_version,
        "automation_id": definition.automation_id,
        "name": definition.name,
        "purpose": definition.purpose,
        "governing_artifact_references": list(definition.governing_artifact_references),
        "steps": [step_to_dict(step) for step in definition.steps],
        "initial_lifecycle_state": definition.initial_lifecycle_state.value,
        "allowed_terminal_states": [state.value for state in definition.allowed_terminal_states],
        "human_approval_requirements": [_approval_requirement_dict(value) for value in definition.human_approval_requirements],
        "failure_policy": definition.failure_policy.value,
        "execution_assignment_references": list(definition.execution_assignment_references),
        "required_completion_references": list(definition.required_completion_references),
        "required_evidence_references": list(definition.required_evidence_references),
        "live_impact": definition.live_impact.value,
        "authorized_repository_scope": list(definition.authorized_repository_scope),
    }


def run_to_dict(run: AutomationRunContext) -> dict[str, object]:
    return {
        "model_version": run.model_version,
        "definition": definition_to_dict(run.definition),
        "run_id": run.run_id,
        "repository_identity": run.repository_identity,
        "branch": run.branch,
        "starting_head": run.starting_head,
        "working_tree_state": run.working_tree_state,
        "run_started_at": run.run_started_at,
        "current_lifecycle_state": run.current_lifecycle_state.value,
        "current_step_id": run.current_step_id,
        "completed_step_ids": list(run.completed_step_ids),
        "approval_state": [_approval_record_dict(record) for record in run.approval_state],
        "assignments": [assignment_to_dict(value) for value in run.assignments],
        "completions": [completion_to_dict(value) for value in run.completions],
        "unresolved_issues": list(run.unresolved_issues),
        "escalation_state": run.escalation_state,
        "activation_occurred": run.activation_occurred,
        "live_changes_occurred": run.live_changes_occurred,
    }


def transition_to_dict(request: TransitionRequest) -> dict[str, object]:
    return {"requested_lifecycle_state": request.requested_lifecycle_state.value, "requested_step_id": request.requested_step_id, "resolved_issue_ids": list(request.resolved_issue_ids)}


def _finding_dict(finding: object) -> dict[str, object]:
    payload: dict[str, object] = {"severity": finding.severity.value, "code": finding.code, "message": finding.message}
    if finding.path is not None:
        payload["path"] = finding.path
    return payload


def transition_decision_to_dict(decision: TransitionDecision) -> dict[str, object]:
    return {
        "allowed": decision.allowed,
        "resulting_lifecycle_state": decision.resulting_lifecycle_state.value if decision.resulting_lifecycle_state else None,
        "resulting_step_id": decision.resulting_step_id,
        "findings": [_finding_dict(value) for value in decision.findings],
        "unresolved_actions": list(decision.unresolved_actions),
        "recommended_next_approval_gate": decision.recommended_next_approval_gate,
    }


def handoff_to_dict(handoff: AutomationHandoff) -> dict[str, object]:
    return {
        "model_version": handoff.model_version,
        "automation_id": handoff.automation_id,
        "run_id": handoff.run_id,
        "current_lifecycle_state": handoff.current_lifecycle_state.value,
        "completed_step_ids": list(handoff.completed_step_ids),
        "pending_step_ids": list(handoff.pending_step_ids),
        "assignment_ids": list(handoff.assignment_ids),
        "completion_assignment_ids": list(handoff.completion_assignment_ids),
        "evidence_references": list(handoff.evidence_references),
        "validation_findings": [_finding_dict(value) for value in handoff.validation_findings],
        "blocking_issues": list(handoff.blocking_issues),
        "approvals_received": list(handoff.approvals_received),
        "approvals_required": list(handoff.approvals_required),
        "activation_occurred": handoff.activation_occurred,
        "live_changes_occurred": handoff.live_changes_occurred,
        "recommended_next_approval_gate": handoff.recommended_next_approval_gate,
    }


def _json(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def definition_to_json(value: GovernedAutomationDefinition) -> str:
    return _json(definition_to_dict(value))


def run_to_json(value: AutomationRunContext) -> str:
    return _json(run_to_dict(value))


def transition_to_json(value: TransitionRequest) -> str:
    return _json(transition_to_dict(value))


def transition_decision_to_json(value: TransitionDecision) -> str:
    return _json(transition_decision_to_dict(value))


def handoff_to_json(value: AutomationHandoff) -> str:
    return _json(handoff_to_dict(value))
