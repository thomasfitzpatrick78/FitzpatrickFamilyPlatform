# Architecture Decision Log

**Document Version:** 1.5

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document is the master index for Fitzpatrick Family Platform Architecture Decision Records.

Individual ADRs are maintained in `docs/architecture/decisions/`.

---

## Decision Lifecycle

```text
Proposed
↓
Approved
↓
Implemented
↓
Baselined
```

---

## Decision Index

| ADR | Title | Category | Status | Implemented | Baseline | Milestone |
|-----|-------|----------|--------|-------------|----------|-----------|
| ADR-001 | Platform Repository Creation | Repository Architecture | Approved | Yes | M11.0 | Milestone 11 |
| ADR-002 | Platform Product Boundary | Product Architecture | Approved | Yes | M11.0 | Milestone 11 |
| ADR-003 | Repository-Managed Governance | Governance Architecture | Approved | Yes | M11.0 | Milestone 11 |
| ADR-004 | Platform Engineering Automation Foundation | Engineering Architecture | Approved | Yes | M11.0 | Milestone 11 |
| ADR-005 | Portfolio Integration and Repository Independence | Portfolio Architecture | Approved | Yes | M11.0 | Milestone 11 |
| ADR-006 | Registry Driven Infrastructure Foundation | Infrastructure Architecture | Approved | No | Pending | Milestone 12 |
| ADR-007 | Governed Operations and Observability | Infrastructure Architecture | Approved | No | Pending | Milestone 13 |
| ADR-008 | AI-Operated Engineering Organization Portfolio Model | Governance Architecture | Approved | No | Pending | EO-13.1 |
| ADR-009 | Evidence Before Operational Health | Product Architecture | Approved | No | Published `c8f9bc3` | PLAT-14.0A |
| ADR-010 | Declared Observed and Reconciled State | Product Architecture | Approved | No | Published `c8f9bc3` | PLAT-14.0A |
| ADR-011 | Generic Operational Evidence Envelope and Versioned Profiles | Product Architecture | Approved | No | Published `c8f9bc3` | PLAT-14.0A |

---

## Decision Categories

### Repository Architecture

- ADR-001 - Platform Repository Creation

### Product Architecture

- ADR-002 - Platform Product Boundary
- ADR-009 - Evidence Before Operational Health
- ADR-010 - Declared Observed and Reconciled State
- ADR-011 - Generic Operational Evidence Envelope and Versioned Profiles

### Governance Architecture

- ADR-003 - Repository-Managed Governance
- ADR-008 - AI-Operated Engineering Organization Portfolio Model

### Engineering Architecture

- ADR-004 - Platform Engineering Automation Foundation

### Portfolio Architecture

- ADR-005 - Portfolio Integration and Repository Independence

### Infrastructure Architecture

- ADR-006 - Registry Driven Infrastructure Foundation
- ADR-007 - Governed Operations and Observability

---

## Future Decisions

Each new ADR shall receive the next sequential repository-local ADR number, be recorded in this index, and be baselined during release closeout.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.5 | Recorded publication baseline `c8f9bc3` for ADR-009 through ADR-011 while retaining Implemented: No. |
| 1.4 | Added ADR-009 through ADR-011 for the PLAT-14.0A Platform Operations domain architecture. |
| 1.3 | Added ADR-008 for the AI-operated Engineering Organization portfolio model. |
| 1.2 | Added ADR-007 for Governed Operations and Observability. |
| 1.1 | Added ADR-006 for Registry Driven Infrastructure Foundation. |
| 1.0 | Initial Platform Architecture Decision Log. |
