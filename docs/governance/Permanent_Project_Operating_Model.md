# Permanent Project Operating Model

**Document Version:** 1.2

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

The AI-operated Engineering Organization is governed as a first-class operating capability. Strategic governance remains outside implementation tasks and is handled by the Chief Architect / Architecture Gatekeeper, Engineering Organization Advisor, and Product Strategy Board.

The governed portfolio has three pillars:

1. Engineering Organization.
2. Shared Platform.
3. Customer-Facing Applications.

The Fitzpatrick Family Platform is the reference implementation of the AI-operated Engineering Organization. The Fitzpatrick Family Financial Assistant is the flagship customer-facing application.

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
11. Every milestone measurably strengthens the Engineering Organization, Shared Platform, and at least one customer-facing application unless a governed exception is approved.
12. Repeated successful practices are evaluated for promotion into governed artifacts.
13. Production changes require explicit human authorization until a separately governed approval model is established.

---

## Engineering Philosophy

- Repository First: durable project knowledge lives in the repository.
- Architecture First: major structure is approved before implementation.
- Product Before Implementation: product value and ownership are established before engineering work begins.
- Evolution Over Redesign: prefer governed evolution over broad replacement.
- Automation Over Repetition: deterministic verification should be automated.
- Trust Evidence Over Assertions: readiness is demonstrated by tests, reports, and repository evidence.
- Governed Automation: automation executes approved architecture and runbooks without independently expanding scope.
- Continuous Organizational Improvement: the Engineering Organization improves through measured capability evolution.

---

## Engineering Investment Rule

Every milestone must measurably strengthen:

1. The Engineering Organization.
2. The Shared Platform.
3. At least one customer-facing application.

This rule applies at the milestone level, not to every individual workstream.

Milestone requirements must identify expected outcomes for all three pillars. Workstream planning must identify the owner and evidence for each pillar. Milestone review evaluates all three pillars, and closeout records evidence for all three.

A milestone cannot be considered fully complete if one pillar has no meaningful advancement unless a formally approved exception exists.

### Exception Process

An exception requires:

- explicit Architecture Gatekeeper approval;
- explicit Product Strategy Board approval;
- documented rationale;
- documented compensating plan;
- visible disclosure in milestone closeout.

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
Registry and Digital Twin Reconciliation
↓
Operational Validation
↓
Release
↓
Milestone Closeout
↓
Engineering Organization Evolution
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
- [Engineering Principles](Engineering_Principles.md)
- [Engineering Lifecycle](Engineering_Lifecycle.md)
- [Definition of Done](Definition_of_Done.md)
- [Product Vision](../product/Product_Vision.md)
- [Architecture Decision Log](../architecture/Architecture_Decision_Log.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Added EO-13.1 three-pillar portfolio model, Engineering Investment Rule, and Engineering Organization Evolution lifecycle requirement. |
| 1.1 | Added Engineering Organization governance layer and authority boundary. |
| 1.0 | Initial Platform operating model. |
