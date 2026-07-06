# Permanent Project Operating Model

**Document Version:** 1.0

**Status:** Active

**Milestone:** Milestone 11

---

## Purpose

This document defines how the Fitzpatrick Family Platform repository is governed and executed.

It is the highest-level governance artifact in this repository.

---

## Authority

The repository is the authoritative source of truth for Platform product, architecture, engineering, validation, milestone, and release knowledge.

Conversations are working sessions. Approved decisions become durable only when synchronized into this repository.

The AI Engineering Organization is governed as a first-class product. Strategic governance remains outside implementation chats and is handled by the Architecture Review Board and Chief Architect conversation.

---

## Product Boundary

The Platform owns non-finance household capabilities:

- Infrastructure
- Home Automation
- Energy Management
- AI Services
- Shared Services
- Family Intelligence

The Platform does not own finance capabilities. Finance remains exclusively in the Fitzpatrick Family Financial Assistant repository.

---

## Operating Principles

1. Product vision before implementation.
2. Specification before implementation.
3. Architecture decisions documented before architectural implementation.
4. Repository-managed product governance before backlog execution.
5. Evidence-based verification before release.
6. Small independently releasable milestones.
7. Automation before repeated manual process where practical.
8. Portfolio coordination without repository coupling.
9. Engineering executors implement approved work but do not make architecture decisions.
10. No Platform implementation without approved requirements, architecture, and validation criteria.

---

## Engineering Philosophy

- Repository First: durable project knowledge lives in the repository.
- Architecture First: major structure is approved before implementation.
- Product Before Implementation: product value and ownership are established before engineering work begins.
- Evolution Over Redesign: prefer governed evolution over broad replacement.
- Automation Over Repetition: deterministic verification should be automated.
- Trust Evidence Over Assertions: readiness is demonstrated by tests, reports, and repository evidence.

---

## Lifecycle

```text
Vision
↓
Capability
↓
Backlog
↓
Requirements
↓
Architecture
↓
Specification
↓
Implementation
↓
Validation
↓
Evidence
↓
Release
```

---

## Governance Layers

| Layer | Governing Artifact |
|-------|--------------------|
| Engineering Organization Governance | Engineering Organization Foundation artifacts |
| Portfolio Governance | Portfolio Integration and Cross-Repository Governance |
| Project Governance | Permanent Project Operating Model |
| Product Governance | Product Vision, Capability Model, Product Backlog, Product Roadmap, Product Governance |
| Requirements Governance | Requirements documents |
| Architecture Governance | ADRs, Architecture Decision Log, Architecture Backlog |
| Specification Governance | Specifications |
| Delivery Governance | Definition of Done and milestone artifacts |
| Engineering Governance | Standards, validation automation, evidence reports |

---

## Related Documents

- [Engineering Organization Foundation](../engineering-organization/README.md)
- [Repository Principles](Repository_Principles.md)
- [Engineering Lifecycle](Engineering_Lifecycle.md)
- [Definition of Done](Definition_of_Done.md)
- [Product Vision](../product/Product_Vision.md)
- [Architecture Decision Log](../architecture/Architecture_Decision_Log.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Platform operating model. |
| 1.1 | Added Engineering Organization governance layer and authority boundary. |
