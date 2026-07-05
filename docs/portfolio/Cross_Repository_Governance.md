# Cross-Repository Governance

**Document Version:** 1.0

**Status:** Active

**Milestone:** Milestone 11

---

## Purpose

This document defines cross-repository governance for the Platform repository.

---

## Repository Independence

Each portfolio repository owns its own product governance, architecture governance, ADRs, roadmap, milestones, releases, validation, and evidence.

---

## Finance Boundary

Finance remains exclusively in the Fitzpatrick Family Financial Assistant repository.

The Platform repository shall not introduce finance, banking, budgeting, transaction, or investment functionality.

---

## Coordination Rules

Cross-repository coordination is required when:

- A capability may cross product boundaries.
- Shared engineering implementation is proposed.
- A release depends on another repository.
- A portfolio-level governance decision changes repository obligations.

---

## Related Documents

- [Portfolio Integration](Portfolio_Integration.md)
- [Shared Engineering Strategy](Shared_Engineering_Strategy.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Platform cross-repository governance. |
