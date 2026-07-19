# Governed Automation Framework

**Document Version:** 1.1

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** EO-14.4

**Architecture Alignment Work Package:** EO-14.4A

---

## Purpose

This framework defines how automations are proposed, approved, implemented, operated, reviewed, and retired. EO-14.4A is an orchestration capability: it determines approved automation flow and lifecycle progression without defining execution behavior.

Automation is governed work. It must preserve human approval before production and must produce evidence.

This specification clarifies architecture boundaries only. It does not implement an orchestration runtime, activate automation, or authorize live work.

---

## Execution Capability Alignment

EO-14.4A consumes the published EO-14.1A Execution Capability whenever an approved automation flow reaches an execution step. EO-14.1A remains the authoritative owner of execution semantics.

Automation coordinates execution but does not redefine it:

- EO-14.4A owns orchestration flow, automation lifecycle progression, approval sequencing, and the decision to stop, suspend, resume, or retire an automation under approved governance.
- EO-14.1A owns Participant, Governed Role, assignment, approval, execution context, execution result, validation finding, evidence, and completion-package semantics.
- Execution validation, execution evidence, and completion packages originate from EO-14.1A and are consumed by EO-14.4A as governed orchestration inputs and outcomes.
- EO-14.4A does not create parallel assignment models, execution contexts, evidence records, completion packages, or execution-validation logic.

Any future implementation of EO-14.4A requires a separate approved work package and must reuse the EO-14.1A contracts rather than recreate them.

---

## Automation Catalog

Each automation should be cataloged with:

- Identifier.
- Owner.
- Repository.
- Purpose.
- Lifecycle state.
- Risk classification.
- Required approvals.
- Inputs and outputs.
- Evidence produced.
- Rollback or disablement path.
- Review cadence.

Catalog references to inputs, outputs, and evidence identify the governed EO-14.1A execution artifacts used by an automation flow; they do not define replacement execution schemas.

---

## Lifecycle States

| State | Meaning |
|-------|---------|
| Candidate | Proposed but not approved. |
| Specified | Requirements, risks, and evidence are documented. |
| Approved | Architecture and product gates are complete. |
| Implemented | Repository implementation exists. |
| Operated | Automation is active under approved boundaries. |
| Suspended | Disabled pending review. |
| Retired | Removed or archived with evidence retained. |

---

## Risk Classification

| Risk | Examples | Required Boundary |
|------|----------|-------------------|
| Low | Repository-only reports, read-only validators. | Repository validation and review. |
| Medium | Generated artifacts, scheduled local jobs, notification drafts. | Owner approval and rollback or disablement path. |
| High | Infrastructure commands, backups, restores, credentials, production services. | Architecture Gatekeeper and explicit human production approval. |

---

## Failure Handling

Automations must define:

- Stop conditions.
- Retry policy or no-retry rule.
- Evidence capture on failure.
- Owner notification path.
- Rollback or disablement steps.
- Post-failure review requirement.

Failure handling governs orchestration response. Execution findings, evidence, validation results, and completion state remain EO-14.1A artifacts.

---

## Promotion Rule

Reusable automation may be promoted into governed artifacts only after repeated successful use, evidence review, and Architecture Gatekeeper approval.

---

## Acceptance Criteria

EO-14.4 is ready for review when:

- Catalog fields, ownership, approvals, risk classification, lifecycle state, auditability, failure handling, rollback, and retirement are defined.
- High-risk automation cannot operate without human approval.
- Reusable automation promotion is evidence-based.
- Orchestration consumes EO-14.1A execution contracts without redefining assignment, context, validation, evidence, or completion semantics.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Clarified EO-14.4A as an orchestration capability that consumes the published EO-14.1A Execution Capability without redefining execution semantics or authorizing implementation. |
| 1.0 | Initial Governed Automation Framework. |
