import ast
import json
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from engineering.platform_eap import cli
from engineering.platform_eap.automation_capability import (
    MODEL_VERSION,
    AutomationLifecycleState,
    AutomationRunContext,
    AutomationStepType,
    FailurePolicy,
    GovernedAutomationDefinition,
    LiveImpact,
    OrchestrationStep,
    TransitionRequest,
    build_automation_handoff,
    evaluate_eligibility,
    evaluate_transition,
    validate_automation_definition,
    validate_automation_run,
)
from engineering.platform_eap.automation_io import (
    AutomationDataError,
    definition_from_dict,
    definition_from_json,
    definition_to_dict,
    definition_to_json,
    run_from_dict,
    run_to_dict,
    run_to_json,
    transition_decision_to_json,
)
from engineering.platform_eap.automation_rendering import render_automation_handoff_markdown
from engineering.platform_eap.execution_capability import (
    MODEL_VERSION as EXECUTION_MODEL_VERSION,
    ApprovalRecord,
    ApprovalRequirement,
    ApprovalStatus,
    CompletionPackage,
    EvidenceRecord,
    EvidenceRequirement,
    EvidenceType,
    ExecutionContext,
    ExecutionResult,
    FindingSeverity,
    GovernedAssignment,
    GovernedRole,
    OutcomeStatus,
    Participant,
    ValidationFinding,
)
from engineering.platform_eap.execution_io import assignment_from_json, completion_from_json


HEAD = "caa089d3afa5e714d4b85d9968c42cd09ab55e1e"
STARTED = "2026-07-19T20:00:00+00:00"
COMPLETED = "2026-07-19T20:15:00+00:00"


def valid_assignment() -> GovernedAssignment:
    return GovernedAssignment(
        EXECUTION_MODEL_VERSION,
        "ASSIGNMENT-1",
        "Validate governed orchestration",
        GovernedRole.EXECUTION_AGENT,
        ("engineering/platform_eap", "engineering/tests"),
        ("validate governed orchestration",),
        ("push repository changes",),
        ("automation-tests",),
        (EvidenceRequirement("EV-REQ", EvidenceType.TEST_RESULT, "automation-tests"),),
        (),
        ("docs/engineering-organization/Governed_Automation_Framework.md",),
        HEAD,
    )


def valid_completion() -> CompletionPackage:
    assignment = valid_assignment()
    participant = Participant("participant-1")
    context = ExecutionContext(
        EXECUTION_MODEL_VERSION,
        participant,
        GovernedRole.EXECUTION_AGENT,
        assignment.assignment_id,
        "FitzpatrickFamilyPlatform",
        "main",
        HEAD,
        "authorized active changes",
        STARTED,
        (),
    )
    evidence = EvidenceRecord(
        EXECUTION_MODEL_VERSION,
        "EVIDENCE-1",
        EvidenceType.TEST_RESULT,
        "python3 -m pytest -p no:cacheprovider engineering/tests",
        "Automation tests passed.",
        COMPLETED,
        assignment.assignment_id,
        "automation-tests",
        "engineering/tests/test_automation_capability.py",
    )
    result = ExecutionResult(
        EXECUTION_MODEL_VERSION,
        assignment.assignment_id,
        OutcomeStatus.COMPLETED,
        "Validated governed orchestration.",
        ("validate governed orchestration",),
        (),
        ("automation-tests",),
        (evidence.evidence_id,),
        (),
        (),
        COMPLETED,
    )
    return CompletionPackage(
        EXECUTION_MODEL_VERSION,
        assignment,
        participant,
        context,
        result,
        (ValidationFinding(FindingSeverity.INFO, "automation-tests.pass", "Automation tests passed."),),
        (evidence,),
        (),
        "Architecture Gatekeeper review",
        False,
        False,
        False,
        False,
    )


def step(
    step_id: str,
    step_type: AutomationStepType,
    prerequisites=(),
    next_steps=(),
    approvals=(),
    assignment=None,
    completion=None,
    evidence=(),
    outcomes=(),
    live_impact=LiveImpact.NONE,
    human_review=False,
) -> OrchestrationStep:
    return OrchestrationStep(step_id, step_id.replace("-", " ").title(), step_type, tuple(prerequisites), tuple(approvals), assignment, completion, tuple(evidence), tuple(outcomes), tuple(next_steps), True, live_impact, human_review)


def valid_definition() -> GovernedAutomationDefinition:
    return GovernedAutomationDefinition(
        MODEL_VERSION,
        "AUTOMATION-1",
        "Governed execution review",
        "Coordinate approved execution review without executing work.",
        ("docs/engineering-organization/Governed_Automation_Framework.md",),
        (
            step("approval", AutomationStepType.APPROVAL_GATE, next_steps=("assignment",), approvals=("APP-1",), human_review=True),
            step("assignment", AutomationStepType.EXECUTION_ASSIGNMENT, prerequisites=("approval",), next_steps=("completion",), approvals=("APP-1",), assignment="ASSIGNMENT-1"),
            step("completion", AutomationStepType.EXECUTION_COMPLETION_REVIEW, prerequisites=("assignment",), next_steps=("handoff",), completion="ASSIGNMENT-1", evidence=(EvidenceType.TEST_RESULT,), outcomes=("completion.valid",), human_review=True),
            step("handoff", AutomationStepType.HUMAN_HANDOFF, prerequisites=("completion",), next_steps=("terminal",), human_review=True),
            step("terminal", AutomationStepType.TERMINAL_COMPLETION, prerequisites=("handoff",), human_review=True),
        ),
        AutomationLifecycleState.DRAFTED,
        (AutomationLifecycleState.COMPLETED, AutomationLifecycleState.FAILED, AutomationLifecycleState.CANCELLED),
        (ApprovalRequirement("APP-1", "Architecture Gatekeeper", ("approval", "assignment")),),
        FailurePolicy.BLOCK_PENDING_HUMAN_REVIEW,
        ("ASSIGNMENT-1",),
        ("ASSIGNMENT-1",),
        ("EVIDENCE-1",),
        LiveImpact.REPOSITORY_ONLY,
        ("engineering/platform_eap", "engineering/tests"),
    )


def valid_run() -> AutomationRunContext:
    return AutomationRunContext(
        MODEL_VERSION,
        valid_definition(),
        "RUN-1",
        "FitzpatrickFamilyPlatform",
        "main",
        HEAD,
        "authorized active changes",
        STARTED,
        AutomationLifecycleState.IN_PROGRESS,
        "completion",
        ("approval", "assignment"),
        (ApprovalRecord("APP-1", ApprovalStatus.APPROVED, "Architecture Gatekeeper", STARTED),),
        (valid_assignment(),),
        (valid_completion(),),
        (),
        "none",
    )


def error_codes(findings):
    return {finding.code for finding in findings if finding.severity == FindingSeverity.ERROR}


def test_automation_capability_imports_only_public_execution_interfaces():
    source = Path("engineering/platform_eap/automation_capability.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    execution_imports = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module == "engineering.platform_eap.execution_capability"
    ]
    imported_names = {alias.name for node in execution_imports for alias in node.names}
    assert execution_imports
    assert not {name for name in imported_names if name.startswith("_")}
    assert {
        "contains_secret_like_content",
        "is_safe_repository_path",
        "is_valid_timestamp",
    } <= imported_names


def test_definition_and_run_are_immutable_and_valid():
    definition = valid_definition()
    run = valid_run()
    assert not error_codes(validate_automation_definition(definition))
    assert not error_codes(validate_automation_run(run))
    with pytest.raises(FrozenInstanceError):
        definition.name = "changed"
    with pytest.raises(FrozenInstanceError):
        run.branch = "other"


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("automation_id", "", "automation.automation_id.required"),
        ("purpose", "", "automation.purpose.required"),
        ("model_version", "future", "automation.model_version.unsupported"),
        ("allowed_terminal_states", (AutomationLifecycleState.BLOCKED,), "automation.terminal_states.invalid"),
        ("initial_lifecycle_state", AutomationLifecycleState.COMPLETED, "automation.initial_state.invalid"),
        ("authorized_repository_scope", ("../outside",), "automation.path.unsafe"),
    ],
)
def test_definition_rejects_invalid_fields(field, value, code):
    assert code in error_codes(validate_automation_definition(replace(valid_definition(), **{field: value})))


def test_definition_rejects_duplicate_unknown_and_cyclic_steps():
    definition = valid_definition()
    duplicate = replace(definition, steps=(*definition.steps, definition.steps[0]))
    assert "automation.steps.duplicate" in error_codes(validate_automation_definition(duplicate))
    unknown = replace(definition.steps[0], allowed_next_step_ids=("missing",))
    assert "automation.step.reference.unknown" in error_codes(validate_automation_definition(replace(definition, steps=(unknown, *definition.steps[1:]))))
    cyclic_first = replace(definition.steps[0], prerequisite_step_ids=("assignment",))
    assert "automation.steps.cyclic" in error_codes(validate_automation_definition(replace(definition, steps=(cyclic_first, *definition.steps[1:]))))


def test_definition_rejects_live_impact_without_approval_and_secret_like_text():
    definition = replace(valid_definition(), live_impact=LiveImpact.LIVE, human_approval_requirements=())
    assert "automation.live.approval_required" in error_codes(validate_automation_definition(definition))
    secret = replace(valid_definition(), purpose="password=hunter2")
    assert "automation.content.secret_like" in error_codes(validate_automation_definition(secret))


@pytest.mark.parametrize(
    ("purpose", "code"),
    [
        ("Trigger https://example.invalid/work", "automation.content.external_url"),
        ("Use shell_command=deploy", "automation.content.executable"),
    ],
)
def test_definition_rejects_external_triggers_and_executable_text(purpose, code):
    assert code in error_codes(validate_automation_definition(replace(valid_definition(), purpose=purpose)))


def test_continue_with_warning_is_denied_for_live_impact():
    definition = replace(valid_definition(), live_impact=LiveImpact.LIVE, failure_policy=FailurePolicy.CONTINUE_WITH_WARNING)
    assert "automation.failure_policy.live_continue_denied" in error_codes(validate_automation_definition(definition))


def test_definition_parser_rejects_unknown_executable_fields_and_dynamic_step_types():
    payload = definition_to_dict(valid_definition())
    payload["shell_command"] = "do work"
    with pytest.raises(AutomationDataError, match="unknown or unsafe fields: shell_command"):
        definition_from_dict(payload)
    payload = definition_to_dict(valid_definition())
    payload["steps"][0]["step_type"] = "plugin_discovered"
    with pytest.raises(AutomationDataError, match="unsupported value"):
        definition_from_dict(payload)


def test_definition_parser_rejects_step_executable_directive():
    payload = definition_to_dict(valid_definition())
    payload["steps"][0]["model_prompt"] = "run this"
    with pytest.raises(AutomationDataError, match="unknown or unsafe fields: model_prompt"):
        definition_from_dict(payload)


def test_definition_json_is_stable_and_round_trips():
    first = definition_to_json(valid_definition())
    assert definition_to_json(definition_from_json(first)) == first


def test_step_requires_declared_assignment_completion_and_live_approval():
    definition = valid_definition()
    assignment_step = replace(definition.steps[1], execution_assignment_reference=None)
    assert "automation.step.assignment.required" in error_codes(validate_automation_definition(replace(definition, steps=(definition.steps[0], assignment_step, *definition.steps[2:]))))
    completion_step = replace(definition.steps[2], execution_completion_reference=None)
    assert "automation.step.completion.required" in error_codes(validate_automation_definition(replace(definition, steps=(*definition.steps[:2], completion_step, *definition.steps[3:]))))
    live_step = replace(definition.steps[0], live_impact=LiveImpact.LIVE, human_review_required=False, required_approval_ids=())
    assert "automation.step.live.approval_required" in error_codes(validate_automation_definition(replace(definition, steps=(live_step, *definition.steps[1:]))))


def test_run_requires_identity_baseline_step_and_approval_state():
    invalid = replace(valid_run(), repository_identity="", starting_head="short", current_step_id="missing")
    codes = error_codes(validate_automation_run(invalid))
    assert {"automation.run.repository_identity.required", "automation.run.starting_head.invalid", "automation.run.current_step.unknown"} <= codes
    approval = ApprovalRecord("APP-1", ApprovalStatus.APPROVED)
    assert "automation.run.approval.approved_incomplete" in error_codes(validate_automation_run(replace(valid_run(), approval_state=(approval,))))
    assert "automation.run.completed_step.approval_missing" in error_codes(validate_automation_run(replace(valid_run(), approval_state=())))


def test_run_reuses_execution_assignment_and_completion_validation():
    assignment = replace(valid_assignment(), assignment_id="")
    codes = error_codes(validate_automation_run(replace(valid_run(), assignments=(assignment,))))
    assert "assignment.assignment_id.required" in codes
    package = valid_completion()
    result = replace(package.execution_result, actions_performed=("push repository changes",))
    codes = error_codes(validate_automation_run(replace(valid_run(), completions=(replace(package, execution_result=result),))))
    assert "result.action.prohibited" in codes


def test_run_rejects_out_of_scope_missing_evidence_and_live_claims_via_execution_validation():
    package = valid_completion()
    result = replace(package.execution_result, files_changed=("docs/product/Product_Roadmap.md",), evidence_ids=())
    invalid = replace(package, execution_result=result, evidence_inventory=())
    codes = error_codes(validate_automation_run(replace(valid_run(), completions=(invalid,))))
    assert "result.file.out_of_scope" in codes
    assert "result.evidence.required_missing" in codes
    assert "automation.run.live_state.prohibited" in error_codes(validate_automation_run(replace(valid_run(), live_changes_occurred=True)))


def test_eligibility_accepts_valid_completion_step_and_preserves_execution_findings():
    decision = evaluate_eligibility(valid_run())
    assert decision.eligible
    assert any(finding.code == "completion.valid" for finding in decision.findings)


def test_eligibility_denies_missing_prerequisite_approval_assignment_completion_and_evidence():
    run = valid_run()
    assert "automation.eligibility.prerequisite.missing" in error_codes(evaluate_eligibility(replace(run, completed_step_ids=())).findings)
    assert "automation.eligibility.approval.missing" in error_codes(evaluate_eligibility(replace(run, current_step_id="assignment", approval_state=())).findings)
    assert "automation.eligibility.assignment.missing" in error_codes(evaluate_eligibility(replace(run, current_step_id="assignment", assignments=())).findings)
    assert "automation.eligibility.completion.missing" in error_codes(evaluate_eligibility(replace(run, completions=())).findings)
    package = replace(valid_completion(), evidence_inventory=())
    assert "automation.eligibility.evidence.missing" in error_codes(evaluate_eligibility(replace(run, completions=(package,))).findings)


def test_eligibility_denies_baseline_mismatch_blocked_terminal_and_unresolved():
    run = valid_run()
    assignment = replace(valid_assignment(), repository_baseline="a" * 40)
    assert "automation.eligibility.baseline.mismatch" in error_codes(evaluate_eligibility(replace(run, current_step_id="assignment", assignments=(assignment,))).findings)
    assert "automation.eligibility.blocked" in error_codes(evaluate_eligibility(replace(run, current_lifecycle_state=AutomationLifecycleState.BLOCKED)).findings)
    assert "automation.eligibility.terminal" in error_codes(evaluate_eligibility(replace(run, current_lifecycle_state=AutomationLifecycleState.COMPLETED)).findings)
    assert "automation.eligibility.unresolved" in error_codes(evaluate_eligibility(replace(run, unresolved_issues=("review required",))).findings)


def test_transition_is_deterministic_side_effect_free_and_advisory():
    run = valid_run()
    request = TransitionRequest(AutomationLifecycleState.AWAITING_HUMAN_REVIEW, "completion")
    before = run_to_json(run)
    first = evaluate_transition(run, request)
    second = evaluate_transition(run, request)
    assert first == second
    assert first.allowed
    assert run_to_json(run) == before
    assert "human" in first.recommended_next_approval_gate.lower()
    assert transition_decision_to_json(first) == transition_decision_to_json(second)


def test_transition_denies_unknown_state_skip_terminal_and_unresolved_block():
    run = valid_run()
    denied = evaluate_transition(run, TransitionRequest(AutomationLifecycleState.APPROVED, "completion"))
    assert "automation.transition.state.denied" in error_codes(denied.findings)
    terminal = evaluate_transition(replace(run, current_lifecycle_state=AutomationLifecycleState.COMPLETED), TransitionRequest(AutomationLifecycleState.IN_PROGRESS, "completion"))
    assert "automation.transition.terminal" in error_codes(terminal.findings)
    blocked = replace(run, current_lifecycle_state=AutomationLifecycleState.BLOCKED, unresolved_issues=("ISSUE-1",))
    decision = evaluate_transition(blocked, TransitionRequest(AutomationLifecycleState.IN_PROGRESS, "completion"))
    assert "automation.transition.blocked.unresolved" in error_codes(decision.findings)


def test_blocked_transition_allows_explicit_issue_resolution():
    blocked = replace(valid_run(), current_lifecycle_state=AutomationLifecycleState.BLOCKED, unresolved_issues=("ISSUE-1",))
    decision = evaluate_transition(blocked, TransitionRequest(AutomationLifecycleState.IN_PROGRESS, "completion", ("ISSUE-1",)))
    assert decision.allowed


def test_transition_denies_completion_until_mandatory_steps_complete():
    run = replace(valid_run(), current_lifecycle_state=AutomationLifecycleState.AWAITING_HUMAN_REVIEW)
    decision = evaluate_transition(run, TransitionRequest(AutomationLifecycleState.COMPLETED, "completion"))
    assert "automation.transition.completion.incomplete" in error_codes(decision.findings)


def test_run_json_reuses_execution_objects_and_rejects_unknown_fields():
    payload = run_to_dict(valid_run())
    assert run_from_dict(payload).assignments[0] == valid_assignment()
    payload["scheduler"] = "cron"
    with pytest.raises(AutomationDataError, match="unknown or unsafe fields: scheduler"):
        run_from_dict(payload)


def test_handoff_references_execution_evidence_and_cannot_self_authorize():
    handoff = build_automation_handoff(valid_run())
    assert handoff.assignment_ids == ("ASSIGNMENT-1",)
    assert handoff.completion_assignment_ids == ("ASSIGNMENT-1",)
    assert handoff.evidence_references == ("EVIDENCE-1:test_result",)
    rendered = render_automation_handoff_markdown(handoff)
    assert rendered == render_automation_handoff_markdown(handoff)
    assert "Activation occurred: no" in rendered
    assert "does not authorize its own next step" in rendered


def test_automation_cli_validates_definition_and_rejects_bad_input(capsys):
    fixture = "engineering/tests/fixtures/automation/valid_definition.json"
    assert cli.main(["automation", "definition", "validate", fixture]) == 0
    assert "Status: PASS" in capsys.readouterr().out
    assert cli.main(["automation", "definition", "validate", "missing.json"]) == 1
    assert "file not found" in capsys.readouterr().out


def test_automation_cli_rejects_path_escape_and_invalid_usage(tmp_path, capsys):
    outside = tmp_path / "definition.json"
    outside.write_text(json.dumps({}), encoding="utf-8")
    assert cli.main(["automation", "definition", "validate", str(outside)]) == 1
    assert "must remain inside the repository" in capsys.readouterr().out
    assert cli.main(["automation", "transition"]) == 2
    assert "Usage: platform-eap automation" in capsys.readouterr().out


def test_automation_cli_validates_run_evaluates_transition_and_renders_handoff(capsys):
    run_path = "engineering/tests/fixtures/automation/valid_run.json"
    transition_path = "engineering/tests/fixtures/automation/valid_transition.json"
    assert cli.main(["automation", "run", "validate", run_path]) == 0
    assert "Status: PASS" in capsys.readouterr().out
    assert cli.main(["automation", "transition", "evaluate", run_path, transition_path]) == 0
    transition_output = capsys.readouterr().out
    assert '"allowed": true' in transition_output
    assert '"resulting_lifecycle_state": "awaiting_human_review"' in transition_output
    assert cli.main(["automation", "handoff", "render", run_path]) == 0
    handoff_output = capsys.readouterr().out
    assert "# Governed Automation Human-Review Handoff" in handoff_output
    assert "Activation occurred: no" in handoff_output


def test_repository_manifest_consumes_published_assignment_and_completion_fixtures():
    manifest_path = Path("engineering/tests/fixtures/automation/end_to_end_execution_manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    definition = definition_from_json(Path(manifest["automation_definition"]).read_text(encoding="utf-8"))
    assignment = assignment_from_json(Path(manifest["execution_assignment"]).read_text(encoding="utf-8"))
    completion = completion_from_json(Path(manifest["execution_completion"]).read_text(encoding="utf-8"))
    run = AutomationRunContext(
        MODEL_VERSION,
        definition,
        "EO-14.4A-FIXTURE-RUN",
        "FitzpatrickFamilyPlatform",
        "main",
        assignment.repository_baseline,
        "authorized fixture state",
        STARTED,
        AutomationLifecycleState.IN_PROGRESS,
        "completion-review",
        ("approval", "assignment"),
        (ApprovalRecord("ARCH-APPROVAL", ApprovalStatus.APPROVED, "Architecture Gatekeeper", STARTED),),
        (assignment,),
        (completion,),
        (),
        "none",
    )
    decision = evaluate_eligibility(run)
    assert decision.eligible
    assert any(finding.code == "completion.valid" for finding in decision.findings)
