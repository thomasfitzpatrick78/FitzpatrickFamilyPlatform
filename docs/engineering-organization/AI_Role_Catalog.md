# AI Role Catalog

**Document Version:** 1.0

**Status:** Active

**Milestone:** EO-13.0

---

## Purpose

This document defines governed AI roles for the Engineering Organization.

---

## Role Catalog

| Role | Primary Responsibility | Authority Boundary | Evidence Produced |
|------|------------------------|--------------------|-------------------|
| Codex Delivery Team | Execute approved workstreams inside repository context. | May implement approved scope; does not own strategic governance. | Diffs, validation output, workstream summaries. |
| Architecture Analyst | Analyze repository state, dependencies, and options for architecture review. | Recommends; does not approve architecture. | Architecture notes, tradeoff summaries, impacted artifacts. |
| Validation Operator | Run tests, validators, and evidence collection commands. | Reports results; does not redefine readiness criteria. | Test output, generated reports, failure summaries. |
| Documentation Steward | Create and update governed Markdown artifacts from approved scope. | Maintains repository artifacts; does not invent unapproved strategy. | Documentation diffs, link updates, revision history. |
| Registry Analyst | Inspect authoritative registries and identify gaps. | Reads and proposes registry changes; does not bypass registry governance. | Registry findings and validation evidence. |

---

## Codex Operating Model

- Use one Codex Project per repository.
- Use one Codex chat per approved workstream.
- Each Codex chat returns to architecture review for decisions, exceptions, and promotion of practices into governed artifacts.
- Strategic governance remains outside implementation chats and is handled by the Architecture Review Board and Chief Architect conversation.

---

## Related Documents

- [Human Role Catalog](Human_Role_Catalog.md)
- [Parallel Workstream Delivery Model](Parallel_Workstream_Delivery_Model.md)
- [Engineering Workspace Model](Engineering_Workspace_Model.md)
- [Definition of Done](../governance/Definition_of_Done.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial AI role catalog. |
