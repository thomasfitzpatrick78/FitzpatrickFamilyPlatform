# Engineering Workspace Model

**Document Version:** 1.0

**Status:** Active

**Milestone:** EO-13.0

---

## Purpose

This document defines the workspace model for AI-assisted engineering delivery.

---

## Workspace Structure

| Workspace Element | Rule |
|-------------------|------|
| Codex Project | One per repository. |
| Codex Chat | One per approved workstream. |
| Repository Branch | Created only when workflow requires branch isolation. |
| Git Repository | Durable Engineering Memory and governed source of truth. |
| Reports | Generated evidence under `reports/engineering`. |
| Registries | Authoritative structured state when a registry exists. |

---

## Operating Boundaries

- Conversations are working sessions.
- Repository artifacts are durable memory.
- Generated evidence supports review but does not replace human approval.
- Strategic governance remains in the Architecture Review Board and Chief Architect conversation.
- Implementation chats may recommend promotion of practices but cannot make promotion authoritative by themselves.

---

## Related Documents

- [Parallel Workstream Delivery Model](Parallel_Workstream_Delivery_Model.md)
- [Engineering Memory Concept](Engineering_Memory_Concept.md)
- [Permanent Project Operating Model](../governance/Permanent_Project_Operating_Model.md)
- [Repository Principles](../governance/Repository_Principles.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Engineering Workspace Model. |
