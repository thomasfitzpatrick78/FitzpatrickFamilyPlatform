from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path, PurePosixPath
from typing import Sequence


MODEL_VERSION = "eo-14.1a-v1"


class GovernedRole(str, Enum):
    EXECUTION_AGENT = "execution_agent"


class FindingSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class ApprovalStatus(str, Enum):
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"


class OutcomeStatus(str, Enum):
    COMPLETED = "completed"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    BLOCKED = "blocked"
    FAILED = "failed"
    NOT_STARTED = "not_started"


class EvidenceType(str, Enum):
    COMMAND_RESULT = "command_result"
    TEST_RESULT = "test_result"
    VALIDATION_REPORT = "validation_report"
    ARTIFACT = "artifact"
    REVIEW_RECORD = "review_record"
    REPOSITORY_STATE = "repository_state"


@dataclass(frozen=True)
class ValidationFinding:
    severity: FindingSeverity
    code: str
    message: str
    path: str | None = None


@dataclass(frozen=True)
class ExecutionPolicy:
    model_version: str = MODEL_VERSION
    supported_roles: tuple[GovernedRole, ...] = (GovernedRole.EXECUTION_AGENT,)
    live_impact_terms: tuple[str, ...] = (
        "activate",
        "deploy",
        "infrastructure",
        "live",
        "production",
        "service restart",
    )


@dataclass(frozen=True)
class Participant:
    participant_id: str


@dataclass(frozen=True)
class EvidenceRequirement:
    requirement_id: str
    evidence_type: EvidenceType
    validation_requirement: str


@dataclass(frozen=True)
class ApprovalRequirement:
    approval_id: str
    human_authority: str
    applies_to: tuple[str, ...]
    required: bool = True


@dataclass(frozen=True)
class GovernedAssignment:
    model_version: str
    assignment_id: str
    title: str
    governed_role: GovernedRole
    authorized_scope: tuple[str, ...]
    permitted_actions: tuple[str, ...]
    prohibited_actions: tuple[str, ...]
    required_validations: tuple[str, ...]
    required_evidence: tuple[EvidenceRequirement, ...]
    human_approval_requirements: tuple[ApprovalRequirement, ...]
    source_references: tuple[str, ...]
    repository_baseline: str | None = None


@dataclass(frozen=True)
class ApprovalRecord:
    approval_id: str
    status: ApprovalStatus
    approved_by: str | None = None
    approved_at: str | None = None


@dataclass(frozen=True)
class ExecutionContext:
    model_version: str
    participant: Participant
    governed_role: GovernedRole
    assignment_id: str
    repository_identity: str
    branch: str
    starting_head: str
    working_tree_state: str
    execution_started_at: str
    approval_state: tuple[ApprovalRecord, ...]


@dataclass(frozen=True)
class ExecutionResult:
    model_version: str
    assignment_id: str
    outcome_status: OutcomeStatus
    summary: str
    actions_performed: tuple[str, ...]
    files_changed: tuple[str, ...]
    validations_executed: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    unresolved_issues: tuple[str, ...]
    deviations_or_escalations: tuple[str, ...]
    completed_at: str


@dataclass(frozen=True)
class EvidenceRecord:
    model_version: str
    evidence_id: str
    evidence_type: EvidenceType
    source_activity: str
    result: str
    timestamp: str
    assignment_id: str
    validation_requirement: str
    artifact_path: str | None = None


@dataclass(frozen=True)
class CompletionPackage:
    model_version: str
    assignment: GovernedAssignment
    participant: Participant
    execution_context: ExecutionContext
    execution_result: ExecutionResult
    validation_findings: tuple[ValidationFinding, ...]
    evidence_inventory: tuple[EvidenceRecord, ...]
    unresolved_decisions: tuple[str, ...]
    recommended_next_approval_gate: str
    commit_occurred: bool
    push_occurred: bool
    activation_occurred: bool
    live_changes_occurred: bool


class ExecutionDataError(ValueError):
    """Raised when untrusted execution-capability data is malformed."""


_HEX_HEAD = re.compile(r"^[0-9a-fA-F]{40,64}$")
_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"\b(?:api[_-]?(?:key|token)|password|secret|token)\s*[:=]", re.IGNORECASE),
    re.compile(r"\b(?:ghp|github_pat|sk-proj)-[A-Za-z0-9_-]{8,}\b"),
)


def _finding(
    severity: FindingSeverity,
    code: str,
    message: str,
    path: str | None = None,
) -> ValidationFinding:
    return ValidationFinding(severity, code, message, path)


def _blank(value: object) -> bool:
    return not isinstance(value, str) or not value.strip()


def is_safe_repository_path(value: str) -> bool:
    if not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and "." not in path.parts


def is_valid_timestamp(value: str) -> bool:
    if _blank(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def contains_secret_like_content(value: str) -> bool:
    return any(pattern.search(value) for pattern in _SECRET_PATTERNS)


def _duplicates(values: Sequence[str]) -> set[str]:
    normalized = [value.strip().casefold() for value in values]
    return {value for value in normalized if normalized.count(value) > 1}


def _contains_live_impact(value: str, policy: ExecutionPolicy) -> bool:
    normalized = value.casefold()
    return any(term.casefold() in normalized for term in policy.live_impact_terms)


def _approval_applies(requirement: ApprovalRequirement, action: str) -> bool:
    action_key = action.strip().casefold()
    return any(value.strip().casefold() in {"*", action_key} for value in requirement.applies_to)


def _approved_for(context: ExecutionContext, assignment: GovernedAssignment, action: str) -> bool:
    approved_ids = {
        record.approval_id
        for record in context.approval_state
        if record.status == ApprovalStatus.APPROVED
    }
    return any(
        requirement.required
        and requirement.approval_id in approved_ids
        and _approval_applies(requirement, action)
        for requirement in assignment.human_approval_requirements
    )


def validate_policy(policy: ExecutionPolicy) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    if policy.model_version != MODEL_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "policy.model_version.unsupported", "Execution policy model version is unsupported.", "policy.model_version"))
    if policy.supported_roles != (GovernedRole.EXECUTION_AGENT,):
        findings.append(_finding(FindingSeverity.ERROR, "policy.roles.unsupported", "EO-14.1A policy must support only the Execution Agent role.", "policy.supported_roles"))
    if not policy.live_impact_terms or any(_blank(term) for term in policy.live_impact_terms):
        findings.append(_finding(FindingSeverity.ERROR, "policy.live_terms.invalid", "Execution policy must define nonblank live-impact terms.", "policy.live_impact_terms"))
    if not findings:
        findings.append(_finding(FindingSeverity.INFO, "policy.valid", "Execution policy is valid.", "policy"))
    return findings


def validate_participant(participant: Participant) -> list[ValidationFinding]:
    if _blank(participant.participant_id):
        return [
            _finding(
                FindingSeverity.ERROR,
                "participant.identifier.required",
                "Participant identifier is required.",
                "participant.participant_id",
            )
        ]
    return [
        _finding(
            FindingSeverity.INFO,
            "participant.valid",
            "Participant is valid.",
            "participant",
        )
    ]


def validate_governed_role(
    role: GovernedRole | object,
    policy: ExecutionPolicy | None = None,
) -> list[ValidationFinding]:
    active_policy = policy or ExecutionPolicy()
    if not isinstance(role, GovernedRole) or role not in active_policy.supported_roles:
        return [
            _finding(
                FindingSeverity.ERROR,
                "role.unsupported",
                "Governed role is missing or unsupported.",
                "governed_role",
            )
        ]
    return [
        _finding(
            FindingSeverity.INFO,
            "role.valid",
            f"Governed role is supported: {role.value}.",
            "governed_role",
        )
    ]


def validate_assignment(
    assignment: GovernedAssignment,
    policy: ExecutionPolicy | None = None,
    repository_root: Path | None = None,
) -> list[ValidationFinding]:
    active_policy = policy or ExecutionPolicy()
    findings = validate_policy(active_policy)
    if assignment.model_version != active_policy.model_version:
        findings.append(_finding(FindingSeverity.ERROR, "assignment.model_version.unsupported", "Assignment model version is unsupported.", "model_version"))
    for field_name, value in (("assignment_id", assignment.assignment_id), ("title", assignment.title)):
        if _blank(value):
            findings.append(_finding(FindingSeverity.ERROR, f"assignment.{field_name}.required", f"Assignment {field_name.replace('_', ' ')} is required.", field_name))
    findings.extend(validate_governed_role(assignment.governed_role, active_policy))
    required_collections = (
        ("authorized_scope", assignment.authorized_scope),
        ("permitted_actions", assignment.permitted_actions),
        ("prohibited_actions", assignment.prohibited_actions),
        ("required_validations", assignment.required_validations),
        ("required_evidence", assignment.required_evidence),
        ("source_references", assignment.source_references),
    )
    for field_name, values in required_collections:
        if not values:
            findings.append(_finding(FindingSeverity.ERROR, f"assignment.{field_name}.required", f"Assignment {field_name.replace('_', ' ')} must not be empty.", field_name))
    for scope in assignment.authorized_scope:
        if not is_safe_repository_path(scope):
            findings.append(_finding(FindingSeverity.ERROR, "assignment.scope.unsafe", "Authorized scope must be a safe repository-relative path.", scope))
    permitted = {action.strip().casefold() for action in assignment.permitted_actions if action.strip()}
    prohibited = {action.strip().casefold() for action in assignment.prohibited_actions if action.strip()}
    for conflict in sorted(permitted & prohibited):
        findings.append(_finding(FindingSeverity.ERROR, "assignment.actions.conflict", f"Action is both permitted and prohibited: {conflict}.", "permitted_actions"))
    for field_name, values in (
        ("permitted_actions", assignment.permitted_actions),
        ("prohibited_actions", assignment.prohibited_actions),
        ("required_validations", assignment.required_validations),
        ("source_references", assignment.source_references),
    ):
        if any(_blank(value) for value in values):
            findings.append(_finding(FindingSeverity.ERROR, f"assignment.{field_name}.blank", f"Assignment {field_name.replace('_', ' ')} contains a blank value.", field_name))
        if _duplicates(values):
            findings.append(_finding(FindingSeverity.ERROR, f"assignment.{field_name}.duplicate", f"Assignment {field_name.replace('_', ' ')} contains duplicate values.", field_name))
    validation_ids = {value.strip() for value in assignment.required_validations}
    requirement_ids: set[str] = set()
    for requirement in assignment.required_evidence:
        if _blank(requirement.requirement_id):
            findings.append(_finding(FindingSeverity.ERROR, "assignment.evidence.requirement_id.required", "Evidence requirement identifier is required.", "required_evidence"))
        elif requirement.requirement_id in requirement_ids:
            findings.append(_finding(FindingSeverity.ERROR, "assignment.evidence.requirement_id.duplicate", f"Duplicate evidence requirement identifier: {requirement.requirement_id}.", "required_evidence"))
        requirement_ids.add(requirement.requirement_id)
        if not isinstance(requirement.evidence_type, EvidenceType):
            findings.append(_finding(FindingSeverity.ERROR, "assignment.evidence.type.unsupported", "Evidence requirement type is missing or unsupported.", requirement.requirement_id))
        if requirement.validation_requirement not in validation_ids:
            findings.append(_finding(FindingSeverity.ERROR, "assignment.evidence.validation.unknown", f"Evidence requirement references an unknown validation: {requirement.validation_requirement}.", requirement.requirement_id))
    approval_ids: set[str] = set()
    for requirement in assignment.human_approval_requirements:
        if _blank(requirement.approval_id) or _blank(requirement.human_authority) or not requirement.applies_to:
            findings.append(_finding(FindingSeverity.ERROR, "assignment.approval.incomplete", "Human approval requirement is incomplete.", "human_approval_requirements"))
        if requirement.approval_id in approval_ids:
            findings.append(_finding(FindingSeverity.ERROR, "assignment.approval.duplicate", f"Duplicate approval identifier: {requirement.approval_id}.", "human_approval_requirements"))
        approval_ids.add(requirement.approval_id)
    live_actions = [action for action in assignment.permitted_actions if _contains_live_impact(action, active_policy)]
    for action in live_actions:
        if not any(requirement.required and _approval_applies(requirement, action) for requirement in assignment.human_approval_requirements):
            findings.append(_finding(FindingSeverity.ERROR, "assignment.live_action.approval_required", f"Live-impacting action lacks an explicit human approval requirement: {action}.", "human_approval_requirements"))
    for reference in assignment.source_references:
        if not is_safe_repository_path(reference):
            findings.append(_finding(FindingSeverity.ERROR, "assignment.source_reference.unsafe", "Source reference must be a safe repository-relative path.", reference))
        elif repository_root is not None and not (repository_root / reference).is_file():
            findings.append(_finding(FindingSeverity.ERROR, "assignment.source_reference.missing", "Source reference does not identify a repository file.", reference))
    if assignment.repository_baseline is not None and not _HEX_HEAD.fullmatch(assignment.repository_baseline):
        findings.append(_finding(FindingSeverity.ERROR, "assignment.baseline.invalid", "Repository baseline must be a full hexadecimal commit identifier.", "repository_baseline"))
    if not any(finding.severity == FindingSeverity.ERROR for finding in findings):
        findings.append(_finding(FindingSeverity.INFO, "assignment.valid", "Governed assignment is valid.", "assignment"))
    return findings


def validate_execution_context(
    context: ExecutionContext,
    assignment: GovernedAssignment,
    policy: ExecutionPolicy | None = None,
) -> list[ValidationFinding]:
    active_policy = policy or ExecutionPolicy()
    findings: list[ValidationFinding] = []
    if context.model_version != active_policy.model_version:
        findings.append(_finding(FindingSeverity.ERROR, "context.model_version.unsupported", "Execution context model version is unsupported.", "execution_context.model_version"))
    findings.extend(validate_participant(context.participant))
    findings.extend(validate_governed_role(context.governed_role, active_policy))
    if context.governed_role != assignment.governed_role:
        findings.append(_finding(FindingSeverity.ERROR, "context.role.mismatch", "Execution context role does not match the assignment role.", "execution_context.governed_role"))
    if context.assignment_id != assignment.assignment_id:
        findings.append(_finding(FindingSeverity.ERROR, "context.assignment.mismatch", "Execution context assignment does not match the governed assignment.", "execution_context.assignment_id"))
    for field_name, value in (
        ("repository_identity", context.repository_identity),
        ("branch", context.branch),
        ("working_tree_state", context.working_tree_state),
    ):
        if _blank(value):
            findings.append(_finding(FindingSeverity.ERROR, f"context.{field_name}.required", f"Execution context {field_name.replace('_', ' ')} is required.", f"execution_context.{field_name}"))
    if not _HEX_HEAD.fullmatch(context.starting_head):
        findings.append(_finding(FindingSeverity.ERROR, "context.starting_head.invalid", "Execution context starting HEAD must be a full hexadecimal commit identifier.", "execution_context.starting_head"))
    if not is_valid_timestamp(context.execution_started_at):
        findings.append(_finding(FindingSeverity.ERROR, "context.started_at.invalid", "Execution start timestamp must be timezone-aware ISO 8601.", "execution_context.execution_started_at"))
    expected_approvals = {requirement.approval_id for requirement in assignment.human_approval_requirements}
    seen_approvals: set[str] = set()
    for record in context.approval_state:
        if record.approval_id not in expected_approvals:
            findings.append(_finding(FindingSeverity.ERROR, "context.approval.unknown", f"Execution context contains an unknown approval: {record.approval_id}.", "execution_context.approval_state"))
        if record.approval_id in seen_approvals:
            findings.append(_finding(FindingSeverity.ERROR, "context.approval.duplicate", f"Execution context contains a duplicate approval: {record.approval_id}.", "execution_context.approval_state"))
        seen_approvals.add(record.approval_id)
        if record.status == ApprovalStatus.APPROVED and (_blank(record.approved_by) or not record.approved_at or not is_valid_timestamp(record.approved_at)):
            findings.append(_finding(FindingSeverity.ERROR, "context.approval.approved_incomplete", f"Approved state requires human authority and timestamp: {record.approval_id}.", "execution_context.approval_state"))
    if assignment.repository_baseline and context.starting_head != assignment.repository_baseline:
        findings.append(_finding(FindingSeverity.WARNING, "context.baseline.mismatch", "Starting repository HEAD does not match the assignment baseline and requires escalation.", "execution_context.starting_head"))
    if not any(finding.severity == FindingSeverity.ERROR for finding in findings):
        findings.append(_finding(FindingSeverity.INFO, "context.valid", "Execution context is valid.", "execution_context"))
    return findings


def validate_evidence_record(
    evidence: EvidenceRecord,
    assignment: GovernedAssignment,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    if evidence.model_version != MODEL_VERSION:
        findings.append(_finding(FindingSeverity.ERROR, "evidence.model_version.unsupported", "Evidence model version is unsupported.", evidence.evidence_id))
    for field_name, value in (
        ("evidence_id", evidence.evidence_id),
        ("source_activity", evidence.source_activity),
        ("result", evidence.result),
        ("assignment_id", evidence.assignment_id),
        ("validation_requirement", evidence.validation_requirement),
    ):
        if _blank(value):
            findings.append(_finding(FindingSeverity.ERROR, f"evidence.{field_name}.required", f"Evidence {field_name.replace('_', ' ')} is required.", evidence.evidence_id or "evidence"))
    if not isinstance(evidence.evidence_type, EvidenceType):
        findings.append(_finding(FindingSeverity.ERROR, "evidence.type.unsupported", "Evidence type is missing or unsupported.", evidence.evidence_id))
    if evidence.assignment_id != assignment.assignment_id:
        findings.append(_finding(FindingSeverity.ERROR, "evidence.assignment.mismatch", "Evidence is not associated with the governed assignment.", evidence.evidence_id))
    if evidence.validation_requirement not in assignment.required_validations:
        findings.append(_finding(FindingSeverity.ERROR, "evidence.validation.unknown", "Evidence is not associated with a required validation.", evidence.evidence_id))
    if not is_valid_timestamp(evidence.timestamp):
        findings.append(_finding(FindingSeverity.ERROR, "evidence.timestamp.invalid", "Evidence timestamp must be timezone-aware ISO 8601.", evidence.evidence_id))
    if any(contains_secret_like_content(value) for value in (evidence.source_activity, evidence.result)):
        findings.append(_finding(FindingSeverity.ERROR, "evidence.content.secret_like", "Evidence contains secret-like material and must not be stored.", evidence.evidence_id))
    if evidence.artifact_path is not None and not is_safe_repository_path(evidence.artifact_path):
        findings.append(_finding(FindingSeverity.ERROR, "evidence.artifact_path.unsafe", "Evidence artifact path must be repository-relative and traversal-free.", evidence.evidence_id))
    if not findings:
        findings.append(_finding(FindingSeverity.INFO, "evidence.valid", "Evidence record is valid.", evidence.evidence_id))
    return findings


def _file_in_scope(path: str, scope: Sequence[str]) -> bool:
    candidate = PurePosixPath(path)
    return any(candidate == PurePosixPath(root) or PurePosixPath(root) in candidate.parents for root in scope)


def validate_execution_result(
    result: ExecutionResult,
    assignment: GovernedAssignment,
    context: ExecutionContext,
    evidence_inventory: Sequence[EvidenceRecord],
    policy: ExecutionPolicy | None = None,
) -> list[ValidationFinding]:
    active_policy = policy or ExecutionPolicy()
    findings: list[ValidationFinding] = []
    if result.model_version != active_policy.model_version:
        findings.append(_finding(FindingSeverity.ERROR, "result.model_version.unsupported", "Execution result model version is unsupported.", "execution_result.model_version"))
    if result.assignment_id != assignment.assignment_id:
        findings.append(_finding(FindingSeverity.ERROR, "result.assignment.mismatch", "Execution result assignment does not match the governed assignment.", "execution_result.assignment_id"))
    if not isinstance(result.outcome_status, OutcomeStatus):
        findings.append(_finding(FindingSeverity.ERROR, "result.outcome.unsupported", "Execution result outcome is unsupported.", "execution_result.outcome_status"))
    if _blank(result.summary):
        findings.append(_finding(FindingSeverity.ERROR, "result.summary.required", "Execution result summary is required.", "execution_result.summary"))
    if not is_valid_timestamp(result.completed_at):
        findings.append(_finding(FindingSeverity.ERROR, "result.completed_at.invalid", "Completion timestamp must be timezone-aware ISO 8601.", "execution_result.completed_at"))
    prohibited = {action.casefold() for action in assignment.prohibited_actions}
    for action in result.actions_performed:
        if action.casefold() in prohibited:
            findings.append(_finding(FindingSeverity.ERROR, "result.action.prohibited", f"Execution result records a prohibited action: {action}.", "execution_result.actions_performed"))
        if _contains_live_impact(action, active_policy) and not _approved_for(context, assignment, action):
            findings.append(_finding(FindingSeverity.ERROR, "result.action.live_unauthorized", f"Live-impacting action lacks approved human authorization: {action}.", "execution_result.actions_performed"))
    for path in result.files_changed:
        if not is_safe_repository_path(path):
            findings.append(_finding(FindingSeverity.ERROR, "result.file.unsafe", "Changed file path must be repository-relative and traversal-free.", path))
        elif not _file_in_scope(path, assignment.authorized_scope):
            findings.append(_finding(FindingSeverity.ERROR, "result.file.out_of_scope", "Changed file falls outside authorized scope.", path))
    required_validations = set(assignment.required_validations)
    executed_validations = set(result.validations_executed)
    if result.outcome_status in {OutcomeStatus.COMPLETED, OutcomeStatus.COMPLETED_WITH_WARNINGS}:
        for validation in sorted(required_validations - executed_validations):
            findings.append(_finding(FindingSeverity.ERROR, "result.validation.missing", f"Completed result is missing required validation: {validation}.", "execution_result.validations_executed"))
    evidence_by_id = {record.evidence_id: record for record in evidence_inventory}
    for evidence_id in result.evidence_ids:
        if evidence_id not in evidence_by_id:
            findings.append(_finding(FindingSeverity.ERROR, "result.evidence.unknown", f"Execution result references missing evidence: {evidence_id}.", "execution_result.evidence_ids"))
    if result.outcome_status in {OutcomeStatus.COMPLETED, OutcomeStatus.COMPLETED_WITH_WARNINGS}:
        for requirement in assignment.required_evidence:
            matching = [
                record
                for record in evidence_inventory
                if record.evidence_id in result.evidence_ids
                and record.evidence_type == requirement.evidence_type
                and record.validation_requirement == requirement.validation_requirement
            ]
            if not matching:
                findings.append(_finding(FindingSeverity.ERROR, "result.evidence.required_missing", f"Completed result is missing mandatory evidence: {requirement.requirement_id}.", "execution_result.evidence_ids"))
    if assignment.repository_baseline and context.starting_head != assignment.repository_baseline and not result.deviations_or_escalations:
        findings.append(_finding(FindingSeverity.ERROR, "result.baseline_mismatch.unescalated", "Starting repository baseline mismatch was not escalated.", "execution_result.deviations_or_escalations"))
    if result.outcome_status == OutcomeStatus.BLOCKED and not (result.unresolved_issues or result.deviations_or_escalations):
        findings.append(_finding(FindingSeverity.ERROR, "result.blocked.reason_required", "Blocked result must identify an unresolved issue or escalation.", "execution_result.unresolved_issues"))
    if not any(finding.severity == FindingSeverity.ERROR for finding in findings):
        findings.append(_finding(FindingSeverity.INFO, "result.valid", "Execution result is valid.", "execution_result"))
    return findings


def validate_completion_package(
    package: CompletionPackage,
    policy: ExecutionPolicy | None = None,
    repository_root: Path | None = None,
) -> list[ValidationFinding]:
    active_policy = policy or ExecutionPolicy()
    findings: list[ValidationFinding] = []
    if package.model_version != active_policy.model_version:
        findings.append(_finding(FindingSeverity.ERROR, "completion.model_version.unsupported", "Completion package model version is unsupported.", "model_version"))
    findings.extend(validate_assignment(package.assignment, active_policy, repository_root))
    findings.extend(validate_participant(package.participant))
    if package.participant != package.execution_context.participant:
        findings.append(_finding(FindingSeverity.ERROR, "completion.participant.mismatch", "Completion participant does not match the execution context participant.", "participant"))
    findings.extend(validate_execution_context(package.execution_context, package.assignment, active_policy))
    evidence_ids: set[str] = set()
    for evidence in package.evidence_inventory:
        if evidence.evidence_id in evidence_ids:
            findings.append(_finding(FindingSeverity.ERROR, "completion.evidence.duplicate", f"Duplicate evidence identifier: {evidence.evidence_id}.", "evidence_inventory"))
        evidence_ids.add(evidence.evidence_id)
        findings.extend(validate_evidence_record(evidence, package.assignment))
    findings.extend(validate_execution_result(package.execution_result, package.assignment, package.execution_context, package.evidence_inventory, active_policy))
    if package.execution_result.outcome_status in {OutcomeStatus.COMPLETED, OutcomeStatus.COMPLETED_WITH_WARNINGS}:
        if any(finding.severity == FindingSeverity.ERROR for finding in package.validation_findings):
            findings.append(_finding(FindingSeverity.ERROR, "completion.claim.contradictory", "Completion is claimed while recorded validation findings contain errors.", "validation_findings"))
    if package.execution_result.outcome_status == OutcomeStatus.BLOCKED and not package.unresolved_decisions:
        findings.append(_finding(FindingSeverity.ERROR, "completion.blocked.unresolved_required", "Blocked completion package must identify unresolved decisions.", "unresolved_decisions"))
    if _blank(package.recommended_next_approval_gate):
        findings.append(_finding(FindingSeverity.ERROR, "completion.next_gate.required", "Recommended next approval gate is required and remains advisory.", "recommended_next_approval_gate"))
    if package.activation_occurred or package.live_changes_occurred:
        live_actions = [action for action in package.execution_result.actions_performed if _contains_live_impact(action, active_policy)]
        if not live_actions or not all(_approved_for(package.execution_context, package.assignment, action) for action in live_actions):
            findings.append(_finding(FindingSeverity.ERROR, "completion.live_claim.unauthorized", "Activation or live-change claim lacks matching authorized execution evidence.", "live_changes_occurred"))
    if not any(finding.severity == FindingSeverity.ERROR for finding in findings):
        findings.append(_finding(FindingSeverity.INFO, "completion.valid", "Completion package is valid and does not authorize its recommended next gate.", "completion"))
    return findings
