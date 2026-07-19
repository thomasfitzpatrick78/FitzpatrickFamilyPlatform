from __future__ import annotations

import re
from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path
from typing import Sequence

from engineering.platform_eap.execution_capability import (
    ApprovalRecord,
    ApprovalRequirement,
    ApprovalStatus,
    CompletionPackage,
    EvidenceType,
    FindingSeverity,
    GovernedAssignment,
    ValidationFinding,
    contains_secret_like_content,
    is_safe_repository_path,
    is_valid_timestamp,
    validate_assignment,
    validate_completion_package,
)


MODEL_VERSION = "eo-14.4a-v1"


class AutomationStepType(str, Enum):
    APPROVAL_GATE = "approval_gate"
    EXECUTION_ASSIGNMENT = "execution_assignment"
    EXECUTION_COMPLETION_REVIEW = "execution_completion_review"
    VALIDATION_GATE = "validation_gate"
    EVIDENCE_REVIEW = "evidence_review"
    HUMAN_HANDOFF = "human_handoff"
    TERMINAL_COMPLETION = "terminal_completion"


class AutomationLifecycleState(str, Enum):
    DRAFTED = "drafted"
    READY_FOR_APPROVAL = "ready_for_approval"
    APPROVED = "approved"
    ELIGIBLE = "eligible"
    IN_PROGRESS = "in_progress"
    AWAITING_EVIDENCE = "awaiting_evidence"
    AWAITING_HUMAN_REVIEW = "awaiting_human_review"
    BLOCKED = "blocked"
    FAILED = "failed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class FailurePolicy(str, Enum):
    STOP = "stop"
    BLOCK_PENDING_HUMAN_REVIEW = "block_pending_human_review"
    FAIL_TERMINALLY = "fail_terminally"
    CONTINUE_WITH_WARNING = "continue_with_warning"


class LiveImpact(str, Enum):
    NONE = "none"
    REPOSITORY_ONLY = "repository_only"
    LIVE = "live"


@dataclass(frozen=True)
class OrchestrationStep:
    step_id: str
    title: str
    step_type: AutomationStepType
    prerequisite_step_ids: tuple[str, ...]
    required_approval_ids: tuple[str, ...]
    execution_assignment_reference: str | None
    execution_completion_reference: str | None
    required_evidence_types: tuple[EvidenceType, ...]
    required_validation_outcomes: tuple[str, ...]
    allowed_next_step_ids: tuple[str, ...]
    stop_on_failure: bool
    live_impact: LiveImpact
    human_review_required: bool


@dataclass(frozen=True)
class GovernedAutomationDefinition:
    model_version: str
    automation_id: str
    name: str
    purpose: str
    governing_artifact_references: tuple[str, ...]
    steps: tuple[OrchestrationStep, ...]
    initial_lifecycle_state: AutomationLifecycleState
    allowed_terminal_states: tuple[AutomationLifecycleState, ...]
    human_approval_requirements: tuple[ApprovalRequirement, ...]
    failure_policy: FailurePolicy
    execution_assignment_references: tuple[str, ...]
    required_completion_references: tuple[str, ...]
    required_evidence_references: tuple[str, ...]
    live_impact: LiveImpact
    authorized_repository_scope: tuple[str, ...]


@dataclass(frozen=True)
class AutomationRunContext:
    model_version: str
    definition: GovernedAutomationDefinition
    run_id: str
    repository_identity: str
    branch: str
    starting_head: str
    working_tree_state: str
    run_started_at: str
    current_lifecycle_state: AutomationLifecycleState
    current_step_id: str
    completed_step_ids: tuple[str, ...]
    approval_state: tuple[ApprovalRecord, ...]
    assignments: tuple[GovernedAssignment, ...]
    completions: tuple[CompletionPackage, ...]
    unresolved_issues: tuple[str, ...]
    escalation_state: str
    activation_occurred: bool = False
    live_changes_occurred: bool = False


@dataclass(frozen=True)
class TransitionRequest:
    requested_lifecycle_state: AutomationLifecycleState
    requested_step_id: str
    resolved_issue_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class EligibilityDecision:
    eligible: bool
    findings: tuple[ValidationFinding, ...]
    unresolved_actions: tuple[str, ...]
    recommended_next_approval_gate: str


@dataclass(frozen=True)
class TransitionDecision:
    allowed: bool
    resulting_lifecycle_state: AutomationLifecycleState | None
    resulting_step_id: str | None
    findings: tuple[ValidationFinding, ...]
    unresolved_actions: tuple[str, ...]
    recommended_next_approval_gate: str


@dataclass(frozen=True)
class AutomationHandoff:
    model_version: str
    automation_id: str
    run_id: str
    current_lifecycle_state: AutomationLifecycleState
    completed_step_ids: tuple[str, ...]
    pending_step_ids: tuple[str, ...]
    assignment_ids: tuple[str, ...]
    completion_assignment_ids: tuple[str, ...]
    evidence_references: tuple[str, ...]
    validation_findings: tuple[ValidationFinding, ...]
    blocking_issues: tuple[str, ...]
    approvals_received: tuple[str, ...]
    approvals_required: tuple[str, ...]
    activation_occurred: bool
    live_changes_occurred: bool
    recommended_next_approval_gate: str


_HEX_HEAD = re.compile(r"^[0-9a-fA-F]{40,64}$")
_EXTERNAL_URL = re.compile(r"\b(?:https?|ftp)://", re.IGNORECASE)
_EXECUTABLE_DIRECTIVE = re.compile(r"(?:^|\s)(?:#!|\$\(|shell_command\s*[:=]|subprocess\.|curl\s+https?://|rm\s+-)", re.IGNORECASE)
_TERMINAL_STATES = {
    AutomationLifecycleState.FAILED,
    AutomationLifecycleState.COMPLETED,
    AutomationLifecycleState.CANCELLED,
}
_ALLOWED_TRANSITIONS = {
    AutomationLifecycleState.DRAFTED: {AutomationLifecycleState.READY_FOR_APPROVAL, AutomationLifecycleState.CANCELLED},
    AutomationLifecycleState.READY_FOR_APPROVAL: {AutomationLifecycleState.APPROVED, AutomationLifecycleState.BLOCKED, AutomationLifecycleState.CANCELLED},
    AutomationLifecycleState.APPROVED: {AutomationLifecycleState.ELIGIBLE, AutomationLifecycleState.BLOCKED, AutomationLifecycleState.CANCELLED},
    AutomationLifecycleState.ELIGIBLE: {AutomationLifecycleState.IN_PROGRESS, AutomationLifecycleState.BLOCKED, AutomationLifecycleState.CANCELLED},
    AutomationLifecycleState.IN_PROGRESS: {AutomationLifecycleState.AWAITING_EVIDENCE, AutomationLifecycleState.AWAITING_HUMAN_REVIEW, AutomationLifecycleState.BLOCKED, AutomationLifecycleState.FAILED},
    AutomationLifecycleState.AWAITING_EVIDENCE: {AutomationLifecycleState.IN_PROGRESS, AutomationLifecycleState.AWAITING_HUMAN_REVIEW, AutomationLifecycleState.BLOCKED, AutomationLifecycleState.FAILED},
    AutomationLifecycleState.AWAITING_HUMAN_REVIEW: {AutomationLifecycleState.IN_PROGRESS, AutomationLifecycleState.COMPLETED, AutomationLifecycleState.BLOCKED, AutomationLifecycleState.FAILED, AutomationLifecycleState.CANCELLED},
    AutomationLifecycleState.BLOCKED: {AutomationLifecycleState.READY_FOR_APPROVAL, AutomationLifecycleState.APPROVED, AutomationLifecycleState.ELIGIBLE, AutomationLifecycleState.IN_PROGRESS, AutomationLifecycleState.FAILED, AutomationLifecycleState.CANCELLED},
}


def _finding(severity: FindingSeverity, code: str, message: str, path: str | None = None) -> ValidationFinding:
    return ValidationFinding(severity, code, message, path)


def _blank(value: object) -> bool:
    return not isinstance(value, str) or not value.strip()


def _duplicates(values: Sequence[str]) -> set[str]:
    normalized = [value.strip().casefold() for value in values]
    return {value for value in normalized if normalized.count(value) > 1}


def _contains_secret(values: Sequence[str]) -> bool:
    return any(contains_secret_like_content(value) for value in values)


def _has_errors(findings: Sequence[ValidationFinding]) -> bool:
    return any(finding.severity == FindingSeverity.ERROR for finding in findings)


def _cycle_exists(steps: Sequence[OrchestrationStep]) -> bool:
    prerequisites = {step.step_id: set(step.prerequisite_step_ids) for step in steps}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(step_id: str) -> bool:
        if step_id in visiting:
            return True
        if step_id in visited:
            return False
        visiting.add(step_id)
        if any(visit(prerequisite) for prerequisite in prerequisites.get(step_id, ())):
            return True
        visiting.remove(step_id)
        visited.add(step_id)
        return False

    return any(visit(step_id) for step_id in prerequisites)


def validate_automation_definition(
    definition: GovernedAutomationDefinition,
    repository_root: Path | None = None,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    if definition.model_version != MODEL_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "automation.model_version.unsupported", "Automation model version is unsupported.", "model_version"))
    for field_name, value in (("automation_id", definition.automation_id), ("name", definition.name), ("purpose", definition.purpose)):
        if _blank(value):
            findings.append(_finding(FindingSeverity.ERROR, f"automation.{field_name}.required", f"Automation {field_name.replace('_', ' ')} is required.", field_name))
    if not definition.steps:
        findings.append(_finding(FindingSeverity.ERROR, "automation.steps.required", "Automation must define at least one orchestration step.", "steps"))
    if not definition.governing_artifact_references:
        findings.append(_finding(FindingSeverity.ERROR, "automation.artifacts.required", "Automation must reference at least one governing artifact.", "governing_artifact_references"))
    if not definition.authorized_repository_scope:
        findings.append(_finding(FindingSeverity.ERROR, "automation.scope.required", "Automation must define authorized repository scope.", "authorized_repository_scope"))
    step_ids = [step.step_id for step in definition.steps]
    if _duplicates(step_ids):
        findings.append(_finding(FindingSeverity.ERROR, "automation.steps.duplicate", "Automation step identifiers must be unique.", "steps"))
    known_steps = set(step_ids)
    approval_ids = {requirement.approval_id for requirement in definition.human_approval_requirements}
    if len(approval_ids) != len(definition.human_approval_requirements):
        findings.append(_finding(FindingSeverity.ERROR, "automation.approvals.duplicate", "Automation approval identifiers must be unique.", "human_approval_requirements"))
    for field_name, values in (
        ("execution_assignment_references", definition.execution_assignment_references),
        ("required_completion_references", definition.required_completion_references),
        ("required_evidence_references", definition.required_evidence_references),
    ):
        if _duplicates(values) or any(_blank(value) for value in values):
            findings.append(_finding(FindingSeverity.ERROR, f"automation.{field_name}.invalid", "Automation references must be nonblank and unique.", field_name))
    for requirement in definition.human_approval_requirements:
        if _blank(requirement.approval_id) or _blank(requirement.human_authority) or not requirement.applies_to:
            findings.append(_finding(FindingSeverity.ERROR, "automation.approval.incomplete", "Automation human approval requirement is incomplete.", "human_approval_requirements"))
    for step in definition.steps:
        path = f"steps.{step.step_id or '<missing>'}"
        if _blank(step.step_id) or _blank(step.title):
            findings.append(_finding(FindingSeverity.ERROR, "automation.step.identity.required", "Orchestration step identifier and title are required.", path))
        if any(reference not in known_steps for reference in (*step.prerequisite_step_ids, *step.allowed_next_step_ids)):
            findings.append(_finding(FindingSeverity.ERROR, "automation.step.reference.unknown", "Orchestration step references an unknown step.", path))
        if step.step_id in step.prerequisite_step_ids or step.step_id in step.allowed_next_step_ids:
            findings.append(_finding(FindingSeverity.ERROR, "automation.step.reference.self", "Orchestration step cannot reference itself.", path))
        if any(approval_id not in approval_ids for approval_id in step.required_approval_ids):
            findings.append(_finding(FindingSeverity.ERROR, "automation.step.approval.unknown", "Orchestration step references an unknown approval requirement.", path))
        if step.execution_assignment_reference and step.execution_assignment_reference not in definition.execution_assignment_references:
            findings.append(_finding(FindingSeverity.ERROR, "automation.step.assignment.unknown", "Orchestration step references an undeclared EO-14.1A assignment.", path))
        if step.execution_completion_reference and step.execution_completion_reference not in definition.required_completion_references:
            findings.append(_finding(FindingSeverity.ERROR, "automation.step.completion.unknown", "Orchestration step references an undeclared EO-14.1A completion package.", path))
        if step.step_type == AutomationStepType.EXECUTION_ASSIGNMENT and not step.execution_assignment_reference:
            findings.append(_finding(FindingSeverity.ERROR, "automation.step.assignment.required", "Execution-assignment step requires an EO-14.1A assignment reference.", path))
        if step.step_type == AutomationStepType.EXECUTION_COMPLETION_REVIEW and not step.execution_completion_reference:
            findings.append(_finding(FindingSeverity.ERROR, "automation.step.completion.required", "Completion-review step requires an EO-14.1A completion reference.", path))
        if step.live_impact == LiveImpact.LIVE and (not step.human_review_required or not step.required_approval_ids):
            findings.append(_finding(FindingSeverity.ERROR, "automation.step.live.approval_required", "Live-impacting step requires human review and an explicit approval.", path))
    if _cycle_exists(definition.steps):
        findings.append(_finding(FindingSeverity.ERROR, "automation.steps.cyclic", "Automation step prerequisites must be acyclic.", "steps"))
    if definition.initial_lifecycle_state in _TERMINAL_STATES or definition.initial_lifecycle_state == AutomationLifecycleState.BLOCKED:
        findings.append(_finding(FindingSeverity.ERROR, "automation.initial_state.invalid", "Automation initial lifecycle state must be nonterminal and unblocked.", "initial_lifecycle_state"))
    if not definition.allowed_terminal_states or any(state not in _TERMINAL_STATES for state in definition.allowed_terminal_states):
        findings.append(_finding(FindingSeverity.ERROR, "automation.terminal_states.invalid", "Allowed terminal states must contain only completed, failed, or cancelled.", "allowed_terminal_states"))
    if definition.live_impact == LiveImpact.LIVE and not definition.human_approval_requirements:
        findings.append(_finding(FindingSeverity.ERROR, "automation.live.approval_required", "Live-impacting automation requires explicit human approval requirements.", "human_approval_requirements"))
    if definition.failure_policy == FailurePolicy.CONTINUE_WITH_WARNING and definition.live_impact == LiveImpact.LIVE:
        findings.append(_finding(FindingSeverity.ERROR, "automation.failure_policy.live_continue_denied", "Live-impacting automation cannot continue with warning after failure.", "failure_policy"))
    path_values = (*definition.governing_artifact_references, *definition.authorized_repository_scope)
    for value in path_values:
        if not is_safe_repository_path(value):
            findings.append(_finding(FindingSeverity.ERROR, "automation.path.unsafe", "Automation paths must be repository-relative and traversal-free.", value))
    for reference in definition.governing_artifact_references:
        if repository_root is not None and is_safe_repository_path(reference) and not (repository_root / reference).is_file():
            findings.append(_finding(FindingSeverity.ERROR, "automation.artifact.missing", "Governing artifact reference does not identify a repository file.", reference))
    textual = (definition.automation_id, definition.name, definition.purpose, *definition.governing_artifact_references, *definition.required_evidence_references, *(step.title for step in definition.steps))
    if _contains_secret(textual):
        findings.append(_finding(FindingSeverity.ERROR, "automation.content.secret_like", "Automation definition contains secret-like material.", "automation"))
    if any(_EXTERNAL_URL.search(value) for value in textual):
        findings.append(_finding(FindingSeverity.ERROR, "automation.content.external_url", "Automation definition cannot contain external URLs that imply automatic work.", "automation"))
    if any(_EXECUTABLE_DIRECTIVE.search(value) for value in textual):
        findings.append(_finding(FindingSeverity.ERROR, "automation.content.executable", "Automation definition cannot contain executable directives.", "automation"))
    if not _has_errors(findings):
        findings.append(_finding(FindingSeverity.INFO, "automation.definition.valid", "Governed automation definition is valid.", "automation"))
    return findings


def validate_automation_run(run: AutomationRunContext, repository_root: Path | None = None) -> list[ValidationFinding]:
    findings = validate_automation_definition(run.definition, repository_root)
    if run.model_version != MODEL_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "automation.run.model_version.unsupported", "Automation run model version is unsupported.", "model_version"))
    for field_name, value in (("run_id", run.run_id), ("repository_identity", run.repository_identity), ("branch", run.branch), ("working_tree_state", run.working_tree_state), ("current_step_id", run.current_step_id), ("escalation_state", run.escalation_state)):
        if _blank(value):
            findings.append(_finding(FindingSeverity.ERROR, f"automation.run.{field_name}.required", f"Automation run {field_name.replace('_', ' ')} is required.", field_name))
    if not _HEX_HEAD.fullmatch(run.starting_head):
        findings.append(_finding(FindingSeverity.ERROR, "automation.run.starting_head.invalid", "Automation run starting HEAD must be a full hexadecimal commit identifier.", "starting_head"))
    if not is_valid_timestamp(run.run_started_at):
        findings.append(_finding(FindingSeverity.ERROR, "automation.run.started_at.invalid", "Automation run start timestamp must be timezone-aware ISO 8601.", "run_started_at"))
    step_ids = {step.step_id for step in run.definition.steps}
    if run.current_step_id not in step_ids:
        findings.append(_finding(FindingSeverity.ERROR, "automation.run.current_step.unknown", "Automation run current step is unknown.", "current_step_id"))
    if any(step_id not in step_ids for step_id in run.completed_step_ids) or _duplicates(run.completed_step_ids):
        findings.append(_finding(FindingSeverity.ERROR, "automation.run.completed_steps.invalid", "Completed step identifiers must be unique and declared by the definition.", "completed_step_ids"))
    expected_approvals = {requirement.approval_id for requirement in run.definition.human_approval_requirements}
    seen_approvals: set[str] = set()
    for record in run.approval_state:
        if record.approval_id not in expected_approvals or record.approval_id in seen_approvals:
            findings.append(_finding(FindingSeverity.ERROR, "automation.run.approval.invalid", "Automation run approval is unknown or duplicated.", record.approval_id))
        seen_approvals.add(record.approval_id)
        if record.status == ApprovalStatus.APPROVED and (_blank(record.approved_by) or not record.approved_at or not is_valid_timestamp(record.approved_at)):
            findings.append(_finding(FindingSeverity.ERROR, "automation.run.approval.approved_incomplete", "Approved automation state requires human authority and timestamp.", record.approval_id))
    approved_ids = {record.approval_id for record in run.approval_state if record.status == ApprovalStatus.APPROVED}
    steps_by_id = {step.step_id: step for step in run.definition.steps}
    for step_id in run.completed_step_ids:
        completed_step = steps_by_id.get(step_id)
        if completed_step and any(approval_id not in approved_ids for approval_id in completed_step.required_approval_ids):
            findings.append(_finding(FindingSeverity.ERROR, "automation.run.completed_step.approval_missing", "Completed step lacks its required human approval.", step_id))
    declared_assignments = set(run.definition.execution_assignment_references)
    assignment_ids: set[str] = set()
    for assignment in run.assignments:
        if assignment.assignment_id in assignment_ids or assignment.assignment_id not in declared_assignments:
            findings.append(_finding(FindingSeverity.ERROR, "automation.run.assignment.invalid", "Automation run assignment is duplicated or undeclared.", assignment.assignment_id))
        assignment_ids.add(assignment.assignment_id)
        findings.extend(validate_assignment(assignment, repository_root=repository_root))
    declared_completions = set(run.definition.required_completion_references)
    completion_ids: set[str] = set()
    for completion in run.completions:
        completion_id = completion.assignment.assignment_id
        if completion_id in completion_ids or completion_id not in declared_completions:
            findings.append(_finding(FindingSeverity.ERROR, "automation.run.completion.invalid", "Automation run completion is duplicated or undeclared.", completion_id))
        completion_ids.add(completion_id)
        findings.extend(validate_completion_package(completion, repository_root=repository_root))
    for step_id in run.completed_step_ids:
        completed_step = steps_by_id.get(step_id)
        if completed_step and completed_step.execution_assignment_reference and completed_step.execution_assignment_reference not in assignment_ids:
            findings.append(_finding(FindingSeverity.ERROR, "automation.run.completed_step.assignment_missing", "Completed step lacks its referenced EO-14.1A assignment.", step_id))
        if completed_step and completed_step.execution_completion_reference and completed_step.execution_completion_reference not in completion_ids:
            findings.append(_finding(FindingSeverity.ERROR, "automation.run.completed_step.completion_missing", "Completed step lacks its referenced EO-14.1A completion package.", step_id))
    terminal_steps = {step.step_id for step in run.definition.steps if step.step_type == AutomationStepType.TERMINAL_COMPLETION}
    if set(run.completed_step_ids) & terminal_steps and run.current_lifecycle_state not in _TERMINAL_STATES:
        findings.append(_finding(FindingSeverity.ERROR, "automation.run.terminal_step.state_mismatch", "Completed terminal step requires a terminal lifecycle state.", "completed_step_ids"))
    if run.activation_occurred or run.live_changes_occurred:
        findings.append(_finding(FindingSeverity.ERROR, "automation.run.live_state.prohibited", "Repository-side orchestration run cannot claim activation or live changes.", "live_changes_occurred"))
    if any(_blank(issue) for issue in run.unresolved_issues) or _contains_secret(run.unresolved_issues):
        findings.append(_finding(FindingSeverity.ERROR, "automation.run.issues.invalid", "Unresolved issues must be nonblank and contain no secret-like material.", "unresolved_issues"))
    if not _has_errors(findings):
        findings.append(_finding(FindingSeverity.INFO, "automation.run.valid", "Automation run context is valid and records no execution authority.", "run"))
    return findings


def evaluate_eligibility(run: AutomationRunContext, step_id: str | None = None, repository_root: Path | None = None) -> EligibilityDecision:
    findings = validate_automation_run(run, repository_root)
    target_id = step_id or run.current_step_id
    steps = {step.step_id: step for step in run.definition.steps}
    step = steps.get(target_id)
    unresolved: list[str] = []
    if run.current_lifecycle_state in _TERMINAL_STATES:
        findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.terminal", "Automation cannot progress after a terminal state.", "current_lifecycle_state"))
    if run.current_lifecycle_state == AutomationLifecycleState.BLOCKED:
        findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.blocked", "Blocked automation requires explicit resolution or new approval before progression.", "current_lifecycle_state"))
    if run.unresolved_issues:
        findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.unresolved", "Automation has unresolved blocking issues.", "unresolved_issues"))
        unresolved.extend(run.unresolved_issues)
    if step is None:
        findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.step.unknown", "Requested orchestration step is unknown.", target_id))
    else:
        missing_prerequisites = sorted(set(step.prerequisite_step_ids) - set(run.completed_step_ids))
        if missing_prerequisites:
            findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.prerequisite.missing", "Mandatory prerequisite steps are incomplete.", step.step_id))
            unresolved.extend(f"Complete prerequisite: {value}" for value in missing_prerequisites)
        approved_ids = {record.approval_id for record in run.approval_state if record.status == ApprovalStatus.APPROVED}
        missing_approvals = sorted(set(step.required_approval_ids) - approved_ids)
        if missing_approvals:
            findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.approval.missing", "Required human approval is absent.", step.step_id))
            unresolved.extend(f"Obtain approval: {value}" for value in missing_approvals)
        assignments = {assignment.assignment_id: assignment for assignment in run.assignments}
        if step.execution_assignment_reference:
            assignment = assignments.get(step.execution_assignment_reference)
            if assignment is None:
                findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.assignment.missing", "Required EO-14.1A assignment is absent.", step.step_id))
            elif assignment.repository_baseline and assignment.repository_baseline != run.starting_head:
                findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.baseline.mismatch", "EO-14.1A assignment baseline does not match the automation run baseline.", step.step_id))
        completions = {completion.assignment.assignment_id: completion for completion in run.completions}
        if step.execution_completion_reference:
            completion = completions.get(step.execution_completion_reference)
            if completion is None:
                findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.completion.missing", "Required EO-14.1A completion package is absent.", step.step_id))
            else:
                completion_findings = validate_completion_package(completion, repository_root=repository_root)
                evidence_types = {record.evidence_type for record in completion.evidence_inventory}
                if any(evidence_type not in evidence_types for evidence_type in step.required_evidence_types):
                    findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.evidence.missing", "Required EO-14.1A evidence type is absent.", step.step_id))
                evidence_ids = {record.evidence_id for record in completion.evidence_inventory}
                if any(reference not in evidence_ids for reference in run.definition.required_evidence_references):
                    findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.evidence_reference.missing", "Required EO-14.1A evidence reference is absent.", step.step_id))
                finding_codes = {finding.code for finding in completion_findings if finding.severity != FindingSeverity.ERROR}
                if any(code not in finding_codes for code in step.required_validation_outcomes):
                    findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.validation.missing", "Required EO-14.1A validation outcome is absent.", step.step_id))
        if step.live_impact == LiveImpact.LIVE and not step.required_approval_ids:
            findings.append(_finding(FindingSeverity.ERROR, "automation.eligibility.live.denied", "Live-impact progression requires explicit human approval.", step.step_id))
    eligible = not _has_errors(findings)
    gate = "Proceed to human review of the proposed orchestration step" if eligible else "Resolve blocking findings and obtain required human approval"
    return EligibilityDecision(eligible, tuple(findings), tuple(dict.fromkeys(unresolved)), gate)


def evaluate_transition(run: AutomationRunContext, request: TransitionRequest, repository_root: Path | None = None) -> TransitionDecision:
    findings: list[ValidationFinding] = []
    unresolved: list[str] = []
    if run.current_lifecycle_state in _TERMINAL_STATES:
        findings.append(_finding(FindingSeverity.ERROR, "automation.transition.terminal", "Transition from a terminal lifecycle state is denied.", "current_lifecycle_state"))
    allowed_states = _ALLOWED_TRANSITIONS.get(run.current_lifecycle_state, set())
    if request.requested_lifecycle_state not in allowed_states:
        findings.append(_finding(FindingSeverity.ERROR, "automation.transition.state.denied", "Requested lifecycle transition is not allowed.", "requested_lifecycle_state"))
    if run.current_lifecycle_state == AutomationLifecycleState.BLOCKED:
        unresolved_issue_set = set(run.unresolved_issues)
        if not unresolved_issue_set or not unresolved_issue_set.issubset(set(request.resolved_issue_ids)):
            findings.append(_finding(FindingSeverity.ERROR, "automation.transition.blocked.unresolved", "Blocked-state transition requires explicit resolution of every blocking issue.", "resolved_issue_ids"))
            unresolved.extend(sorted(unresolved_issue_set - set(request.resolved_issue_ids)))
    steps = {step.step_id: step for step in run.definition.steps}
    current_step = steps.get(run.current_step_id)
    if request.requested_step_id not in steps:
        findings.append(_finding(FindingSeverity.ERROR, "automation.transition.step.unknown", "Requested next step is unknown.", "requested_step_id"))
    elif current_step and request.requested_step_id != run.current_step_id and request.requested_step_id not in current_step.allowed_next_step_ids:
        findings.append(_finding(FindingSeverity.ERROR, "automation.transition.step.denied", "Requested next step is not allowed by the current orchestration step.", "requested_step_id"))
    eligibility_run = run
    if run.current_lifecycle_state == AutomationLifecycleState.BLOCKED and not any(
        finding.code == "automation.transition.blocked.unresolved" for finding in findings
    ):
        eligibility_run = replace(
            run,
            current_lifecycle_state=request.requested_lifecycle_state,
            unresolved_issues=tuple(issue for issue in run.unresolved_issues if issue not in request.resolved_issue_ids),
        )
    eligibility = evaluate_eligibility(eligibility_run, request.requested_step_id, repository_root)
    findings.extend(eligibility.findings)
    unresolved.extend(eligibility.unresolved_actions)
    if request.requested_lifecycle_state == AutomationLifecycleState.COMPLETED:
        required_steps = {step.step_id for step in run.definition.steps if step.step_type != AutomationStepType.TERMINAL_COMPLETION}
        completed = set(run.completed_step_ids)
        if current_step:
            completed.add(current_step.step_id)
        if not required_steps.issubset(completed):
            findings.append(_finding(FindingSeverity.ERROR, "automation.transition.completion.incomplete", "Completion is denied until all mandatory orchestration steps are complete.", "completed_step_ids"))
        if AutomationLifecycleState.COMPLETED not in run.definition.allowed_terminal_states:
            findings.append(_finding(FindingSeverity.ERROR, "automation.transition.completion.terminal_denied", "Definition does not allow completed as a terminal state.", "allowed_terminal_states"))
    allowed = not _has_errors(findings)
    gate = eligibility.recommended_next_approval_gate if allowed else "Human review of denied transition and unresolved actions"
    return TransitionDecision(
        allowed,
        request.requested_lifecycle_state if allowed else None,
        request.requested_step_id if allowed else None,
        tuple(findings),
        tuple(dict.fromkeys(unresolved)),
        gate,
    )


def build_automation_handoff(run: AutomationRunContext, repository_root: Path | None = None) -> AutomationHandoff:
    findings = tuple(validate_automation_run(run, repository_root))
    all_steps = tuple(step.step_id for step in run.definition.steps)
    completed = set(run.completed_step_ids)
    approvals_received = tuple(record.approval_id for record in run.approval_state if record.status == ApprovalStatus.APPROVED)
    required_approvals = tuple(requirement.approval_id for requirement in run.definition.human_approval_requirements if requirement.required)
    evidence_references = tuple(
        f"{record.evidence_id}:{record.evidence_type.value}"
        for completion in run.completions
        for record in completion.evidence_inventory
    )
    next_gate = "Architecture Gatekeeper or designated human review of the orchestration handoff"
    return AutomationHandoff(
        MODEL_VERSION,
        run.definition.automation_id,
        run.run_id,
        run.current_lifecycle_state,
        tuple(step_id for step_id in all_steps if step_id in completed),
        tuple(step_id for step_id in all_steps if step_id not in completed),
        tuple(assignment.assignment_id for assignment in run.assignments),
        tuple(completion.assignment.assignment_id for completion in run.completions),
        evidence_references,
        findings,
        run.unresolved_issues,
        approvals_received,
        tuple(value for value in required_approvals if value not in approvals_received),
        run.activation_occurred,
        run.live_changes_occurred,
        next_gate,
    )
