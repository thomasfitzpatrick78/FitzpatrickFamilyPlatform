# Governed Automation Framework Usage

**Document Version:** 1.1

**Status:** Repository Implementation Published; Automation Not Activated

**Milestone:** EO-14.4A

---

## Purpose

The EO-14.4A Option B capability validates declarative automation definitions and governed run records, evaluates eligibility and lifecycle transitions without side effects, and renders advisory human-review handoffs.

Automation coordinates execution; it does not redefine or perform execution. EO-14.1A remains authoritative for assignments, participants, roles, approvals, execution context and results, validation findings, evidence, and completion packages.

## Model and Safety Boundary

The stable model version is `eo-14.4a-v1`. Models are immutable and use bounded step, lifecycle, failure-policy, and live-impact values. Unknown fields and unsafe paths are rejected.

Automation run JSON embeds EO-14.1A assignment and completion objects using the published EO-14.1A parsers. Their validation findings are preserved. Orchestration evidence inventory contains only EO-14.1A evidence identifiers and types.

The capability has no scheduler, timer, retry worker, queue, registry, plugin discovery, model invocation, network access, command execution, persistence layer, or output-file option.

## CLI

Validate a definition:

```text
./platform-eap automation definition validate engineering/tests/fixtures/automation/valid_definition.json
```

Validate a run:

```text
./platform-eap automation run validate engineering/tests/fixtures/automation/valid_run.json
```

Evaluate a proposed transition and print stable JSON:

```text
./platform-eap automation transition evaluate engineering/tests/fixtures/automation/valid_run.json engineering/tests/fixtures/automation/valid_transition.json
```

Render an advisory human-review handoff:

```text
./platform-eap automation handoff render engineering/tests/fixtures/automation/valid_run.json
```

Inputs must resolve to files inside the repository. Symlink escape, traversal, malformed JSON, unknown fields, invalid EO-14.1A packages, and denied transitions produce a nonzero exit. Commands write only to standard output and never advance lifecycle state.

## Lifecycle Decisions

The evaluator rejects unknown transitions, skipped prerequisites or approvals, missing assignment or completion packages, invalid EO-14.1A evidence, baseline mismatch, unresolved blocked state, terminal-state progression, and incomplete completion claims.

An allowed decision is a proposal for human review. It does not authorize or persist the next state.

## Related Documents

- [Governed Automation Framework](Governed_Automation_Framework.md)
- [Execution Capability Usage](Execution_Capability_Usage.md)
- [Execution Agent Specification](Execution_Agent_Specification.md)
- [Engineering Lifecycle](../governance/Engineering_Lifecycle.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded publication of the Architecture Gatekeeper-approved repository implementation without automation activation. |
| 1.0 | Documented the EO-14.4A repository-side orchestration models, EO-14.1A integration, CLI, transition evaluation, handoff rendering, and safety boundaries. |
