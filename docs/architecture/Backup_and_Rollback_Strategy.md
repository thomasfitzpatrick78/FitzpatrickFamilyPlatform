# Backup and Rollback Strategy

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document defines backup and rollback readiness for future managed infrastructure changes.

No backup automation or restore orchestration is implemented by PLAT-13.1.

---

## Strategy

| Layer | Source of Truth | Readiness Expectation |
|-------|-----------------|-----------------------|
| Registry and documentation | Git repository | Commit reviewed registry changes before treating them as authoritative. |
| Raspberry Pi Pi-hole | Current Raspberry Pi at `192.168.50.67` | Keep intact through migration and preserve as rollback. |
| Future Beelink host | Planned Beelink registry records | Establish OS, storage, and backup target before service deployment. |
| Future containers | Future service records and deployment artifacts | Define persistent volume backup and restore before cutover. |
| Network modernization | Network device registry records | Record physical topology and rollback cabling before changes. |

---

## Pi-hole Rollback Position

The Raspberry Pi should remain the rollback path for Pi-hole after migration.

Rollback readiness requires:

- Current Raspberry Pi IP and SSH access recorded.
- Current Pi-hole version state recorded.
- No forced repair or update on the Raspberry Pi before migration.
- DNS cutover steps documented before execution.
- Post-cutover rollback trigger defined before execution.

---

## Future Backup Requirements

Before implementing backup automation, define:

- Backup scope by registry record.
- Backup cadence.
- Retention period.
- Storage target.
- Restore test expectation.
- Owner and review process.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial backup and rollback strategy. |
