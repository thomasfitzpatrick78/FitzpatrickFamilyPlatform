# Architecture Backlog

**Document Version:** 1.3

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document tracks future architecture topics for the Fitzpatrick Family Platform.

---

## Backlog

| ID | Priority | Topic | Status | Notes |
|----|:--------:|-------|--------|-------|
| AB-001 | High | Registry Driven Infrastructure Foundation | Active | Selected by ADR-006 for Milestone 12. |
| AB-007 | High | Infrastructure operations readiness | Active | PLAT-13.1 documents readiness options and checklists without runtime implementation. |
| AB-008 | High | Platform runtime architecture options | Candidate | Deferred until Infrastructure operations readiness establishes options and gates. |
| AB-009 | High | Platform Digital Twin lifecycle state model | Candidate | Future enhancement proposal for explicit states: Planned -> Delivered -> Powered -> BIOS Verified -> OS Installed -> Network Connected -> SSH Verified -> Docker Ready -> Platform Active. Do not implement lifecycle changes in PLAT-13.3. |
| AB-002 | High | Home Automation safety model | Candidate | Needed before device or automation workflows. |
| AB-003 | Medium | AI Services privacy and safety model | Candidate | Required before AI service implementation. |
| AB-004 | Medium | Energy data model | Candidate | Required before energy tracking implementation. |
| AB-005 | Medium | Shared service boundaries | Candidate | Needed before reusable service implementation. |
| AB-006 | Low | Cross-repository engineering extraction criteria | Deferred | Requires evidence from multiple repositories. |

---

## Related Documents

- [Architecture Decision Log](Architecture_Decision_Log.md)
- [Current Architecture State](Current_Architecture_State.md)
- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.3 | Added future Platform Digital Twin lifecycle state model proposal from PLAT-13.3 Architecture Review Board decision. |
| 1.2 | Added PLAT-13.1 Infrastructure operations readiness architecture topic. |
| 1.1 | Marked Registry Driven Infrastructure Foundation active for Milestone 12 and deferred runtime architecture until registry foundation exists. |
| 1.0 | Initial Platform architecture backlog. |
