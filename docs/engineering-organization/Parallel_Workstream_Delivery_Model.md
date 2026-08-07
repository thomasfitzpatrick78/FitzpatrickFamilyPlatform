# Parallel Workstream Delivery Model

**Document Version:** 1.2

**Status:** Active

**Milestone:** EO-13.0

---

## Purpose

This document defines how parallel AI-assisted workstreams operate inside the Engineering Organization.

---

## Model

Each approved workstream receives one Codex chat in the repository Codex Project. The chat executes scoped work, preserves evidence, and returns for architecture review before decisions are accepted as durable.

```text
Architecture Review Board / Chief Architect
        |
        v
Approved Workstream Scope
        |
        v
Dedicated Codex Chat
        |
        v
Repository Artifacts + Validation Evidence
        |
        v
Architecture Review Return
```

---

## Rules

- One Codex Project is used per repository.
- One Codex chat is used per approved workstream.
- Implementation chats do not own strategic governance.
- Workstream outputs must identify changed artifacts, validation results, risks, and architecture questions.
- Cross-workstream conflicts return to architecture review rather than being resolved independently inside implementation chats.
- Workstream Continuity Briefs, when implemented by approved AI Collaboration Governance work, preserve orientation and handoff context but remain subordinate to permanent governance, approved milestone and architecture artifacts, and approved specifications.

---

## EO-15.2 Main-Task and Specialist Model

This section supersedes the one-chat-per-workstream rule for EO-15.2-governed work.

- Use one main Codex task per approved outcome.
- Keep each workstream or specialist lane inside its own exact authority and scope.
- Use no more than three concurrent specialists. They default to read-only.
- Require the main task to collect and reconcile every result and remain the sole shared-checkout writer.
- Continue automatically inside an accepted Bounded Outcome Envelope until acceptance, a material stop, or a genuine external dependency occurs.
- Serialize shared paths. An envelope may assign at most one writer specialist in a dedicated worktree and branch with non-overlapping owned roots and main-task integration.

---

## Related Documents

- [AI Role Catalog](AI_Role_Catalog.md)
- [Engineering Workspace Model](Engineering_Workspace_Model.md)
- [Organizational Impact Assessment Template](Organizational_Impact_Assessment_Template.md)
- [Development Workflow](../standards/Development_Workflow.md)
- [Workstream Continuity Brief Specification](ai-collaboration/Workstream_Continuity_Brief_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Added EO-15.2 risk-tiered conditional authority and governed subagent adoption. |
| 1.1 | Added future Workstream Continuity Brief relationship for AI Collaboration Governance. |
| 1.0 | Initial parallel workstream delivery model. |
