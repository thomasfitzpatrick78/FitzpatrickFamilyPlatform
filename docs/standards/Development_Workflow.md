# Development Workflow

**Document Version:** 1.1

**Status:** Active

**Milestone:** Milestone 11

---

## Purpose

This document defines the governed development workflow for the Platform repository.

---

## Workflow

1. Review product scope.
2. Review requirements.
3. Review architecture and ADRs.
4. Update specifications.
5. Implement approved changes.
6. Run tests.
7. Run Platform EAP validation.
8. Review evidence reports.
9. Commit only after validation passes.
10. Tag releases only when governance authorizes release.

---

## Required Validation

```bash
python3 -m pytest engineering/tests
./platform-eap repository validate
./platform-eap governance validate
./platform-eap release readiness
./platform-eap milestone closeout
./platform-eap engineering metrics
./platform-eap capabilities
```

---

## EO-15.2 Conditional Workflow

An accepted conditional bundle activates each included phase automatically when its predicates pass. One main writer applies exact targets. Read-only specialists may inspect independent lanes. Validation outputs are preclassified, two repair cycles are permitted on exact repairable paths, and evidence is sealed before material review.

Separate Owner acknowledgment is not required between conforming discovery, application, validation, repair, evidence, or cross-repository technical dependencies. Tier 3 actions remain fresh pre-action decisions.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Added EO-15.2 risk-tiered conditional authority and governed subagent adoption. |
| 1.0 | Initial Platform development workflow. |
