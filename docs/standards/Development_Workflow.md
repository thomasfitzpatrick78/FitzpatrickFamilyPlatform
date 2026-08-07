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

Validation reports to the terminal by default and does not change tracked report files. Add `--write-report` only when a milestone, release, or accepted Bounded Outcome Envelope explicitly requires a durable snapshot.

---

## Historical EO-15.2 Phase A Conditional Workflow

This workflow remains only for already-bound Phase A packages.

## Bounded-Outcome Workflow for New Work

Read the Authority Index, accepted Bounded Outcome Envelope, and Delivery State. Continue through included implementation, diagnosis, newly justified repair, validation, evidence, commit, publication, fetch, and equality without continuation-only prompts. Stop only for a governed material boundary change, unknown ownership, conflict, or protected information.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Added EO-15.2 risk-tiered conditional authority and governed subagent adoption. |
| 1.0 | Initial Platform development workflow. |
