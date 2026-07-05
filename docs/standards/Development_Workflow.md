# Development Workflow

**Document Version:** 1.0

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

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Platform development workflow. |
