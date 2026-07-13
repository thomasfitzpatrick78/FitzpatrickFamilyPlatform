# Governed Automation Framework

**Document Version:** 1.0

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** EO-14.4

---

## Purpose

This framework defines how automations are proposed, approved, implemented, operated, reviewed, and retired.

Automation is governed work. It must preserve human approval before production and must produce evidence.

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

---

## Promotion Rule

Reusable automation may be promoted into governed artifacts only after repeated successful use, evidence review, and Architecture Gatekeeper approval.

---

## Acceptance Criteria

EO-14.4 is ready for review when:

- Catalog fields, ownership, approvals, risk classification, lifecycle state, auditability, failure handling, rollback, and retirement are defined.
- High-risk automation cannot operate without human approval.
- Reusable automation promotion is evidence-based.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Governed Automation Framework. |
