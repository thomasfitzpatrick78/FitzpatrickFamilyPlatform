import json
from dataclasses import FrozenInstanceError, replace

import pytest

from engineering.platform_eap import cli
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
    ExecutionPolicy,
    FindingSeverity,
    GovernedAssignment,
    GovernedRole,
    OutcomeStatus,
    Participant,
    ValidationFinding,
    validate_assignment,
    validate_completion_package,
    validate_evidence_record,
    validate_execution_context,
    validate_governed_role,
    validate_participant,
    validate_policy,
)
from engineering.platform_eap.execution_io import (
    assignment_from_dict,
    assignment_to_json,
    completion_from_dict,
    completion_from_json,
    completion_to_dict,
    completion_to_json,
)
from engineering.platform_eap.execution_rendering import render_completion_markdown


HEAD = "c6e982fe1af5e570c407b9c04ed8c489d865e257"
STARTED = "2026-07-19T18:30:00+00:00"
COMPLETED = "2026-07-19T18:45:00+00:00"


def valid_assignment() -> GovernedAssignment:
    return GovernedAssignment(
        model_version=MODEL_VERSION,
        assignment_id="EO-14.1A-TEST",
        title="Governed repository implementation",
        governed_role=GovernedRole.EXECUTION_AGENT,
        authorized_scope=("engineering/platform_eap", "engineering/tests"),
        permitted_actions=("edit governed repository files",),
        prohibited_actions=("push repository changes",),
        required_validations=("engineering-tests",),
        required_evidence=(EvidenceRequirement("EV-REQ-1", EvidenceType.TEST_RESULT, "engineering-tests"),),
        human_approval_requirements=(),
        source_references=("docs/governance/Engineering_Lifecycle.md",),
        repository_baseline=HEAD,
    )


def valid_context(assignment: GovernedAssignment | None = None) -> ExecutionContext:
    assignment = assignment or valid_assignment()
    return ExecutionContext(
        model_version=MODEL_VERSION,
        participant=Participant("participant-test-001"),
        governed_role=assignment.governed_role,
        assignment_id=assignment.assignment_id,
        repository_identity="FitzpatrickFamilyPlatform",
        branch="main",
        starting_head=HEAD,
        working_tree_state="authorized changes present",
        execution_started_at=STARTED,
        approval_state=(),
    )


def valid_evidence(assignment: GovernedAssignment | None = None) -> EvidenceRecord:
    assignment = assignment or valid_assignment()
    return EvidenceRecord(
        model_version=MODEL_VERSION,
        evidence_id="EVIDENCE-1",
        evidence_type=EvidenceType.TEST_RESULT,
        source_activity="python3 -m pytest -p no:cacheprovider engineering/tests",
        result="All engineering tests passed.",
        timestamp=COMPLETED,
        assignment_id=assignment.assignment_id,
        validation_requirement="engineering-tests",
        artifact_path="reports/engineering/repository/repository_report.json",
    )


def valid_result(assignment: GovernedAssignment | None = None) -> ExecutionResult:
    assignment = assignment or valid_assignment()
    return ExecutionResult(
        model_version=MODEL_VERSION,
        assignment_id=assignment.assignment_id,
        outcome_status=OutcomeStatus.COMPLETED,
        summary="Implemented the authorized repository capability.",
        actions_performed=("edit governed repository files",),
        files_changed=("engineering/platform_eap/execution_capability.py",),
        validations_executed=("engineering-tests",),
        evidence_ids=("EVIDENCE-1",),
        unresolved_issues=(),
        deviations_or_escalations=(),
        completed_at=COMPLETED,
    )


def valid_completion() -> CompletionPackage:
    assignment = valid_assignment()
    participant = Participant("participant-test-001")
    context = replace(valid_context(assignment), participant=participant)
    return CompletionPackage(
        model_version=MODEL_VERSION,
        assignment=assignment,
        participant=participant,
        execution_context=context,
        execution_result=valid_result(assignment),
        validation_findings=(ValidationFinding(FindingSeverity.INFO, "tests.pass", "Tests passed."),),
        evidence_inventory=(valid_evidence(assignment),),
        unresolved_decisions=(),
        recommended_next_approval_gate="Architecture Gatekeeper review",
        commit_occurred=False,
        push_occurred=False,
        activation_occurred=False,
        live_changes_occurred=False,
    )


def error_codes(findings):
    return {finding.code for finding in findings if finding.severity == FindingSeverity.ERROR}


def test_participant_and_governed_role_are_separate_and_valid():
    participant = Participant("session-123")
    assert not error_codes(validate_participant(participant))
    assert not error_codes(validate_governed_role(GovernedRole.EXECUTION_AGENT))
    assert not hasattr(participant, "governed_role")


def test_policy_supports_only_execution_agent_role():
    assert not error_codes(validate_policy(ExecutionPolicy()))
    invalid = ExecutionPolicy(supported_roles=())
    assert "policy.roles.unsupported" in error_codes(validate_policy(invalid))


def test_participant_requires_stable_identifier():
    assert "participant.identifier.required" in error_codes(validate_participant(Participant("  ")))


def test_unsupported_governed_role_fails_closed():
    assert "role.unsupported" in error_codes(validate_governed_role("administrator"))


def test_valid_assignment_passes():
    assert not error_codes(validate_assignment(valid_assignment()))


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("authorized_scope", (), "assignment.authorized_scope.required"),
        ("permitted_actions", (), "assignment.permitted_actions.required"),
        ("prohibited_actions", (), "assignment.prohibited_actions.required"),
        ("required_validations", (), "assignment.required_validations.required"),
        ("required_evidence", (), "assignment.required_evidence.required"),
        ("source_references", (), "assignment.source_references.required"),
    ],
)
def test_assignment_rejects_missing_required_collections(field, value, code):
    assert code in error_codes(validate_assignment(replace(valid_assignment(), **{field: value})))


def test_assignment_rejects_conflicting_actions():
    assignment = replace(valid_assignment(), prohibited_actions=("EDIT GOVERNED REPOSITORY FILES",))
    assert "assignment.actions.conflict" in error_codes(validate_assignment(assignment))


def test_assignment_rejects_live_action_without_human_approval_requirement():
    assignment = replace(valid_assignment(), permitted_actions=("deploy to live infrastructure",))
    assert "assignment.live_action.approval_required" in error_codes(validate_assignment(assignment))


def test_assignment_accepts_live_action_with_explicit_human_approval_requirement():
    action = "deploy to live infrastructure"
    approval = ApprovalRequirement("APPROVAL-1", "Human Platform Administrator", (action,))
    assignment = replace(valid_assignment(), permitted_actions=(action,), human_approval_requirements=(approval,))
    assert "assignment.live_action.approval_required" not in error_codes(validate_assignment(assignment))


def test_assignment_rejects_evidence_without_known_validation():
    evidence = EvidenceRequirement("EV-2", EvidenceType.ARTIFACT, "unknown-validation")
    assignment = replace(valid_assignment(), required_evidence=(evidence,))
    assert "assignment.evidence.validation.unknown" in error_codes(validate_assignment(assignment))


def test_assignment_rejects_unsafe_and_missing_source_references(tmp_path):
    unsafe = replace(valid_assignment(), source_references=("../secret.txt",))
    assert "assignment.source_reference.unsafe" in error_codes(validate_assignment(unsafe, repository_root=tmp_path))
    assert "assignment.source_reference.missing" in error_codes(validate_assignment(valid_assignment(), repository_root=tmp_path))


def test_assignment_parser_rejects_unknown_executable_directive():
    payload = completion_to_dict(valid_completion())["assignment"]
    payload["shell_command"] = "rm -rf /"
    with pytest.raises(ExecutionDataError, match="unknown or unsafe fields: shell_command"):
        assignment_from_dict(payload)


def test_assignment_parser_rejects_unsupported_role():
    payload = completion_to_dict(valid_completion())["assignment"]
    payload["governed_role"] = "autonomous_administrator"
    with pytest.raises(ExecutionDataError, match="unsupported value"):
        assignment_from_dict(payload)


def test_execution_context_is_valid_and_immutable():
    context = valid_context()
    assert not error_codes(validate_execution_context(context, valid_assignment()))
    with pytest.raises(FrozenInstanceError):
        context.branch = "other"


def test_execution_context_rejects_missing_repository_and_starting_head():
    context = replace(valid_context(), repository_identity="", starting_head="short")
    codes = error_codes(validate_execution_context(context, valid_assignment()))
    assert "context.repository_identity.required" in codes
    assert "context.starting_head.invalid" in codes


def test_execution_context_rejects_invalid_approved_state():
    assignment = replace(
        valid_assignment(),
        human_approval_requirements=(ApprovalRequirement("APP-1", "Human", ("*",)),),
    )
    context = replace(valid_context(assignment), approval_state=(ApprovalRecord("APP-1", ApprovalStatus.APPROVED),))
    assert "context.approval.approved_incomplete" in error_codes(validate_execution_context(context, assignment))


@pytest.mark.parametrize("outcome", list(OutcomeStatus))
def test_each_bounded_outcome_round_trips(outcome):
    package = valid_completion()
    result = replace(package.execution_result, outcome_status=outcome)
    if outcome == OutcomeStatus.BLOCKED:
        result = replace(result, unresolved_issues=("Awaiting review",))
        package = replace(package, unresolved_decisions=("Human decision required",))
    parsed = completion_from_dict(completion_to_dict(replace(package, execution_result=result)))
    assert parsed.execution_result.outcome_status == outcome


def test_completed_result_fails_closed_without_mandatory_evidence():
    package = replace(valid_completion(), evidence_inventory=())
    codes = error_codes(validate_completion_package(package))
    assert "result.evidence.unknown" in codes
    assert "result.evidence.required_missing" in codes


def test_changed_file_outside_authorized_scope_is_rejected():
    package = valid_completion()
    result = replace(package.execution_result, files_changed=("docs/governance/Definition_of_Done.md",))
    assert "result.file.out_of_scope" in error_codes(validate_completion_package(replace(package, execution_result=result)))


def test_prohibited_action_performed_is_rejected():
    package = valid_completion()
    result = replace(package.execution_result, actions_performed=("push repository changes",))
    assert "result.action.prohibited" in error_codes(validate_completion_package(replace(package, execution_result=result)))


def test_baseline_mismatch_requires_escalation():
    package = valid_completion()
    context = replace(package.execution_context, starting_head="a" * 40)
    assert "result.baseline_mismatch.unescalated" in error_codes(validate_completion_package(replace(package, execution_context=context)))


def test_blocked_completion_requires_unresolved_decision():
    package = valid_completion()
    result = replace(package.execution_result, outcome_status=OutcomeStatus.BLOCKED, unresolved_issues=("Blocked",))
    assert "completion.blocked.unresolved_required" in error_codes(validate_completion_package(replace(package, execution_result=result)))


def test_valid_evidence_passes_without_secret_fields():
    evidence = valid_evidence()
    assert not error_codes(validate_evidence_record(evidence, valid_assignment()))
    assert not hasattr(evidence, "credentials")


def test_evidence_requires_assignment_and_validation_associations():
    evidence = replace(valid_evidence(), assignment_id="OTHER", validation_requirement="other")
    codes = error_codes(validate_evidence_record(evidence, valid_assignment()))
    assert "evidence.assignment.mismatch" in codes
    assert "evidence.validation.unknown" in codes


@pytest.mark.parametrize("result", ["password=hunter2", "api_token=abc123", "-----BEGIN PRIVATE KEY-----"])
def test_evidence_rejects_secret_like_results(result):
    evidence = replace(valid_evidence(), result=result)
    assert "evidence.content.secret_like" in error_codes(validate_evidence_record(evidence, valid_assignment()))


def test_evidence_rejects_secret_like_source_activity():
    evidence = replace(valid_evidence(), source_activity="tool --token=abc123")
    assert "evidence.content.secret_like" in error_codes(validate_evidence_record(evidence, valid_assignment()))


def test_evidence_rejects_unsafe_artifact_reference():
    evidence = replace(valid_evidence(), artifact_path="../../credentials")
    assert "evidence.artifact_path.unsafe" in error_codes(validate_evidence_record(evidence, valid_assignment()))


def test_valid_completion_package_passes():
    assert not error_codes(validate_completion_package(valid_completion()))


def test_completion_claim_with_recorded_error_is_rejected():
    package = replace(
        valid_completion(),
        validation_findings=(ValidationFinding(FindingSeverity.ERROR, "test.failed", "A test failed."),),
    )
    assert "completion.claim.contradictory" in error_codes(validate_completion_package(package))


def test_completion_json_is_stable_and_round_trips():
    package = valid_completion()
    first = completion_to_json(package)
    second = completion_to_json(completion_from_json(first))
    assert first == second
    assert first.index('"model_version"') < first.index('"assignment"') < first.index('"participant"')


def test_assignment_json_is_stable():
    assignment = valid_assignment()
    assert assignment_to_json(assignment) == assignment_to_json(assignment)


def test_markdown_render_is_stable_and_preserves_advisory_gate_boundary():
    package = valid_completion()
    rendered = render_completion_markdown(package)
    assert rendered == render_completion_markdown(package)
    assert "Commit occurred: no" in rendered
    assert "Activation occurred: no" in rendered
    assert "does not authorize the next lifecycle step" in rendered


def test_completion_parser_rejects_self_authorization_field():
    payload = completion_to_dict(valid_completion())
    payload["next_gate_authorized"] = True
    with pytest.raises(ExecutionDataError, match="unknown or unsafe fields: next_gate_authorized"):
        completion_from_dict(payload)


def prepare_cli_root(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "ROOT", tmp_path)
    source = tmp_path / "docs/governance/Engineering_Lifecycle.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Lifecycle\n", encoding="utf-8")


def test_execution_cli_validates_assignment(tmp_path, monkeypatch, capsys):
    prepare_cli_root(tmp_path, monkeypatch)
    path = tmp_path / "assignment.json"
    path.write_text(assignment_to_json(valid_assignment()), encoding="utf-8")
    assert cli.main(["execution", "assignment", "validate", "assignment.json"]) == 0
    assert "Status: PASS" in capsys.readouterr().out


def test_execution_cli_validates_and_renders_completion(tmp_path, monkeypatch, capsys):
    prepare_cli_root(tmp_path, monkeypatch)
    path = tmp_path / "completion.json"
    path.write_text(completion_to_json(valid_completion()), encoding="utf-8")
    assert cli.main(["execution", "completion", "validate", "completion.json"]) == 0
    assert "Status: PASS" in capsys.readouterr().out
    assert cli.main(["execution", "completion", "render", "completion.json"]) == 0
    assert "# Governed Execution Completion Package" in capsys.readouterr().out


def test_execution_cli_missing_and_malformed_inputs_fail_safely(tmp_path, monkeypatch, capsys):
    prepare_cli_root(tmp_path, monkeypatch)
    assert cli.main(["execution", "assignment", "validate", "missing.json"]) == 1
    assert "file not found" in capsys.readouterr().out
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{not-json", encoding="utf-8")
    assert cli.main(["execution", "assignment", "validate", "malformed.json"]) == 1
    assert "malformed" in capsys.readouterr().out


def test_execution_cli_rejects_input_outside_repository(tmp_path, monkeypatch, capsys):
    repository = tmp_path / "repository"
    repository.mkdir()
    prepare_cli_root(repository, monkeypatch)
    outside = tmp_path / "outside.json"
    outside.write_text(json.dumps({}), encoding="utf-8")
    assert cli.main(["execution", "assignment", "validate", str(outside)]) == 1
    assert "must remain inside the repository" in capsys.readouterr().out


def test_execution_cli_invalid_usage_returns_two(capsys):
    assert cli.main(["execution", "completion"]) == 2
    assert "Usage: platform-eap execution" in capsys.readouterr().out
