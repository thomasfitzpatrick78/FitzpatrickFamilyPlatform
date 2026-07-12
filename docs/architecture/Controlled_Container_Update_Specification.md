# Controlled Container Update Specification

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document defines the governed production container update model.

It does not pull images, restart containers, or modify live Docker state.

---

## Policy

Production containers must not use ungoverned floating-image behavior.

Each production image update must define:

- Image source.
- Approved version.
- Digest record where practical.
- Release notes review.
- Vulnerability and compatibility review.
- Backup prerequisite.
- Validation plan.
- Observation period.
- Rollback image or prior deployment path.

Unattended Watchtower-style production updates are prohibited in this milestone.

---

## Update Flow

1. Record current image version and digest.
2. Confirm current backup is complete or explicitly waived by review.
3. Review upstream release notes.
4. Review compatibility and known issues.
5. Pull the candidate image in a future implementation workstream.
6. Validate in isolation or canary where practical.
7. Deploy only within approved change scope.
8. Observe service behavior.
9. Roll back to the prior image if validation fails.
10. Update registry and runbook evidence after success.

---

## Pi-hole First Implementation

Pi-hole is the first customer-facing service for controlled update management.

Before a Pi-hole update:

- Raspberry Pi rollback must remain available.
- Beelink DHCP reservation must be verified.
- Pi-hole configuration backup must be current.
- DNS resolution must be validated before and after.
- Blocklist enforcement must be validated before and after.
- Router DNS must not be changed as part of a routine container update.

---

## Evidence

Successful update evidence includes:

- Prior image version and digest.
- New image version and digest.
- Backup identifier.
- Validation commands and results.
- Observation window.
- Rollback decision.
- Registry synchronization.

Failed update evidence includes:

- Failure symptom.
- Time detected.
- Rollback action.
- Recovery validation.
- Follow-up decision.

---

## Related Documents

- [Platform Service Lifecycle](../governance/Service_Lifecycle.md)
- [Production Service Cutover Checklist](../governance/Production_Service_Cutover_Checklist.md)
- [Pi-hole Service Objectives](../operations/Pi-hole_Service_Objectives.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial controlled production container update specification for PLAT-13.6. |
