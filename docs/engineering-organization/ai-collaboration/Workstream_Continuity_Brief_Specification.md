# Workstream Continuity Brief Specification

**Document Version:** 1.0

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** EO-14.8B

---

## Purpose

This specification defines a Workstream Continuity Brief as an orientation and traceability artifact for AI-assisted engineering work.

A Workstream Continuity Brief is subordinate to higher authority. It does not replace permanent governance, approved architecture, approved specifications, or milestone artifacts.

EO-14.8B specifies the brief only. It does not create Alpha, Bravo, Charlie, Architecture Integration, or other live continuity briefs.

---

## Authority Hierarchy

When lower authority conflicts with higher authority, higher authority wins:

1. Permanent governance.
2. Approved milestone and architecture artifacts.
3. Approved specification or work package.
4. Active Workstream Continuity Brief.
5. Chat prompt and conversation context.

---

## Required Fields

| Field | Requirement |
|-------|-------------|
| Repository | Repository name and path. |
| Baseline | Branch, HEAD, and relevant baseline state. |
| Status | Draft, Active, Paused, Superseded, or Closed. |
| Active milestone | Milestone name and governing plan. |
| Workstream ID and title | Approved ID and title. |
| Assigned role | AI role and authority source. |
| Objective | Approved objective. |
| Current Engineering Lifecycle stage | Current stage of the work. |
| Authoritative artifacts | Permanent governance, milestone artifacts, specifications, ADRs, and role docs. |
| Completed work and evidence | Completed scope and evidence locations. |
| Active repository changes | Known uncommitted changes to preserve. |
| Parallel workstreams | Related active or paused workstreams. |
| Dependencies and integration gates | Required predecessor gates and coordination points. |
| Unresolved decisions | Decisions requiring governance review. |
| Risks | Known risks, warnings, and limitations. |
| Stop conditions | Conditions requiring halt and escalation. |
| Permitted actions | Actions authorized for the workstream. |
| Prohibited actions | Actions outside scope or authority. |
| Next gate | Next review or lifecycle gate. |
| Last verification date | Date repository state was last verified. |
| Superseded brief reference | Prior brief reference when applicable. |

---

## Lifecycle States

| State | Meaning |
|-------|---------|
| Draft | Prepared but not active. |
| Active | Current continuity artifact for a workstream. |
| Paused | Workstream is paused but continuity is preserved. |
| Superseded | Replaced by a newer continuity brief. |
| Closed | Workstream continuity is no longer active. |

Only one Workstream Continuity Brief may be Active for a workstream.

---

## Non-Goals

- Template implementation.
- Live continuity brief creation.
- Validator implementation.
- Chat transcript preservation.
- Alternate source of authority.
- Capability Registry creation.

---

## Related Documents

- [AI Collaboration Governance Capability Charter](AI_Collaboration_Governance_Capability_Charter.md)
- [AI Collaboration Governance Specification](AI_Collaboration_Governance_Specification.md)
- [AI Collaboration Lifecycle](AI_Collaboration_Lifecycle.md)
- [AI Session Initialization Standard](AI_Session_Initialization_Standard.md)
- [AI Session Completion Standard](AI_Session_Completion_Standard.md)
- [Parallel Workstream Delivery Model](../Parallel_Workstream_Delivery_Model.md)
- [Engineering Workspace Model](../Engineering_Workspace_Model.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Workstream Continuity Brief Specification. |
