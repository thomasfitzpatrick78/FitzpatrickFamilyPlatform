# ADR-008 - AI-Operated Engineering Organization Portfolio Model

**Document Version:** 1.0

**Status:** Approved

**Date:** 2026-07-12

**Milestone:** EO-13.1

**Implemented:** Repository governance prepared; pending Architecture Gatekeeper review and release.

---

## Context

The repository has evolved from Platform-only governance into a broader AI-operated Engineering Organization model. Repeated milestone practices now include repository-first decision records, evidence-first validation, architecture-before-implementation, Codex implementation boundaries, and milestone closeout evidence.

The portfolio needs a durable model that distinguishes:

- Engineering Organization: organizational operating capability, AI roles, governance, lifecycle, and delivery system.
- Shared Platform: reusable technical foundation, infrastructure, services, observability, registry, and Digital Twin.
- Customer-Facing Applications: user-facing products and experiences, led by the Fitzpatrick Family Financial Assistant.

---

## Decision

Adopt the AI-operated Engineering Organization as a first-class governed capability.

Use the three-pillar portfolio model:

```text
AI-Operated Engineering Organization
  -> Engineering Organization
  -> Shared Platform
  -> Customer-Facing Applications
```

The Fitzpatrick Family Platform is the reference implementation of the AI-operated Engineering Organization and the Shared Platform technical foundation.

The Fitzpatrick Family Financial Assistant is the flagship customer-facing application.

Every milestone must measurably strengthen the Engineering Organization, the Shared Platform, and at least one customer-facing application unless a governed exception is approved by the Architecture Gatekeeper and Product Strategy Board.

Every milestone closeout must include Engineering Organization Evolution.

---

## Consequences

- Engineering Organization governance becomes a permanent repository concern.
- Milestone planning, review, closeout, roadmap, backlog, lifecycle, and Definition of Done must trace all three pillars.
- AI roles require governed authority boundaries, prohibited actions, inputs, outputs, approval boundaries, and escalation conditions.
- Repeated successful practices must be evaluated for promotion into governed artifacts.
- Execution Agent and Operations Analyst remain planned roles until future governance activates them.
- Repository-only governance work must not falsely claim direct customer-facing implementation, but milestone-level aggregation must still account for customer-facing application improvement.

---

## Related Documents

- [Engineering Organization Manifesto](../../engineering-organization/Engineering_Organization_Manifesto.md)
- [AI Role Catalog](../../engineering-organization/AI_Role_Catalog.md)
- [Engineering Organization Capability Maturity Model](../../engineering-organization/Engineering_Organization_Capability_Maturity_Model.md)
- [Engineering Principles](../../governance/Engineering_Principles.md)
- [Permanent Project Operating Model](../../governance/Permanent_Project_Operating_Model.md)
- [Definition of Done](../../governance/Definition_of_Done.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial ADR for EO-13.1 AI-operated Engineering Organization portfolio model. |
