# AI Session Initialization Standard

**Document Version:** 1.0

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** EO-14.8B

---

## Purpose

This standard defines mandatory AI session initialization checks before planning, architecture, implementation, validation, live work, release, or closeout begins.

---

## Mandatory Checks

| Check | Required Evidence |
|-------|-------------------|
| Repository identity | Repository path and expected repository name. |
| Branch and HEAD | Current branch and current commit. |
| Working-tree state | `git status -sb` and active changed files. |
| Remote synchronization status | Remote tracking state where available. |
| Permanent governance | Applicable permanent governance artifacts reviewed. |
| Current milestone | Active milestone plan and milestone status reviewed. |
| Roadmap, backlog, and Kanban | Product roadmap, product backlog, Engineering Organization roadmap/backlog, and portfolio Kanban reconciled as applicable. |
| Applicable ADRs, specifications, work packages, and continuity briefs | Relevant repository-governed authority artifacts identified. |
| Assigned AI role | Role from AI Role Catalog or approved work package confirmed. |
| Authority and prohibited actions | Allowed actions, prohibited actions, required approvals, and stop conditions confirmed. |
| Parallel workstreams and dependencies | Active parallel workstreams, integration gates, and dependency order reconciled. |
| Current lifecycle stage | Engineering Lifecycle stage and AI Collaboration Lifecycle stage declared. |
| Contradictions | Narrative context compared with repository evidence and any conflict escalated. |
| Readiness result | READY, READY WITH WARNINGS, or NOT READY. |

---

## Reconciliation Statement

Before planning, architecture, implementation, or live work begins, the AI participant must provide a reconciliation statement that identifies:

- the repository and branch;
- the current HEAD;
- the workstream or work package;
- the assigned role;
- the current lifecycle stage;
- active repository changes that must be preserved;
- known dependencies and integration gates;
- prohibited actions;
- readiness outcome.

---

## Readiness Outcomes

| Outcome | Meaning |
|---------|---------|
| READY | Required checks pass and no blocking conflicts exist. |
| READY WITH WARNINGS | Required checks are sufficient to proceed, but warnings or nonblocking gaps must be disclosed. |
| NOT READY | Work must stop until repository state, authority, scope, or governance conflicts are resolved. |

Readiness outcomes must not use a percentage score.

---

## Non-Goals

- Conversation-content scoring.
- AI model evaluation.
- Prompt-quality scoring.
- Validator implementation.
- Platform EAP command implementation.
- Continuity template implementation.

---

## Related Documents

- [AI Collaboration Governance Capability Charter](AI_Collaboration_Governance_Capability_Charter.md)
- [AI Collaboration Lifecycle](AI_Collaboration_Lifecycle.md)
- [AI Session Completion Standard](AI_Session_Completion_Standard.md)
- [AI Session Readiness Validator Specification](AI_Session_Readiness_Validator_Specification.md)
- [Engineering Lifecycle](../../governance/Engineering_Lifecycle.md)
- [AI Role Catalog](../AI_Role_Catalog.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial AI Session Initialization Standard. |
