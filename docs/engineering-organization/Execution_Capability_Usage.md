# Execution Capability Usage

**Document Version:** 1.1

**Status:** Repository Implementation Published; Execution Agent Not Activated

**Milestone:** EO-14.1A

---

## Purpose

The EO-14.1A Execution Capability provides repository-side data models, deterministic validation, stable JSON serialization, and Markdown rendering for governed assignments and completion packages.

It makes the approved Option B+ behavioral contract executable and testable. It does not execute work, invoke models, run commands from data, select assignments, activate the Execution Agent, or alter repository or infrastructure state.

---

## Model Boundary

The implementation preserves the approved responsibility flow:

```text
Policy
  -> Assignment
  -> Execution Context
  -> Execution Result
  -> Validation
  -> Evidence
  -> Completion and Handoff
```

`Participant` and `GovernedRole` are separate immutable values. EO-14.1A supports only the bounded `execution_agent` role. Assignments originate outside the capability through approved governance and cannot grant themselves additional authority.

The stable model version is `eo-14.1a-v1`.

---

## CLI

Validate an assignment:

```text
./platform-eap execution assignment validate engineering/tests/fixtures/execution/valid_assignment.json
```

Validate a completion package:

```text
./platform-eap execution completion validate engineering/tests/fixtures/execution/valid_completion.json
```

Render a validated completion package as Markdown on standard output:

```text
./platform-eap execution completion render engineering/tests/fixtures/execution/valid_completion.json
```

The CLI accepts only files whose resolved path remains inside the repository. It does not expose an output-path option and does not overwrite files. Missing files, malformed JSON, unknown fields, unsafe paths, unsupported enum values, and validation errors produce a nonzero exit.

---

## Assignment Contract

A governed assignment records:

- assignment identifier and title;
- the bounded governed role;
- repository-relative authorized scope;
- permitted and prohibited actions;
- required validations and typed evidence requirements;
- explicit human-approval requirements;
- repository-relative governing artifact references;
- an optional full repository baseline commit.

Unknown fields are rejected. Shell-command, executable directive, credential, routing, scheduling, model, and autonomous-work fields are not part of the contract.

---

## Completion Contract

A completion package combines the assignment, participant, execution context, execution result, structured findings, evidence inventory, unresolved decisions, recommended next gate, and explicit commit, push, activation, and live-change declarations.

Validation fails closed when, among other conditions:

- completed work lacks required validation or evidence;
- a changed file falls outside the authorized repository scope;
- a prohibited action is recorded;
- a baseline mismatch lacks an escalation;
- a live-impacting action lacks explicit approved human authorization;
- evidence is unassociated, uses unsafe artifact paths, or contains secret-like material;
- a completed claim conflicts with recorded validation errors;
- a blocked package omits unresolved decisions.

The recommended next approval gate is advisory. Neither validation nor rendering authorizes the next lifecycle step.

---

## Safety Boundary

- Assignment and evidence files are treated as untrusted data.
- JSON parsing uses an explicit allowlist of fields and bounded enum values.
- Repository paths must be relative and traversal-free.
- CLI input paths cannot escape the repository, including through symlinks.
- Evidence has no credential or arbitrary metadata field, and secret-like results fail validation.
- No assignment field is executed.
- Rendering writes only to standard output.
- The capability has no registry, scheduler, router, work queue, persistent participant state, model integration, background process, remote executor, or infrastructure integration.

---

## Related Documents

- [Execution Agent Specification](Execution_Agent_Specification.md)
- [Engineering Lifecycle](../governance/Engineering_Lifecycle.md)
- [Governed Automation Framework](Governed_Automation_Framework.md)
- [AI Session Completion Standard](ai-collaboration/AI_Session_Completion_Standard.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded publication of the Architecture Gatekeeper-approved EO-14.1A repository implementation without activating the Execution Agent. |
| 1.0 | Documented the EO-14.1A repository-side Execution Capability model, CLI, validation, rendering, and safety boundaries. |
