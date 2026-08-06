# Cross-Repository Governance

**Document Version:** 1.1

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

## EO-15.2 Cross-Repository Adoption

The Platform owns the canonical shared operating policy. Another repository adopts only an exact published title, semantic version, SHA-256, and acceptance state through its own profile, decision, validation, and publication. Platform approval or success never transfers authority or activates another repository. FFFA retains exclusive Finance, customer-data, workbook, validation-output, and release authority.

---

## Related Documents

- [Portfolio Integration](Portfolio_Integration.md)
- [Shared Engineering Strategy](Shared_Engineering_Strategy.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Added EO-15.2 risk-tiered conditional authority and governed subagent adoption. |
| 1.0 | Initial Platform cross-repository governance. |
