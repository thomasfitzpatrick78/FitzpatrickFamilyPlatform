# Backup and Rollback Strategy

**Document Version:** 1.1

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document defines backup and rollback readiness for future managed infrastructure changes.

No backup automation or restore orchestration is implemented by PLAT-13.6 repository-only planning.

---

## Strategy

| Layer | Source of Truth | Readiness Expectation |
|-------|-----------------|-----------------------|
| Registry and documentation | Git repository | Commit reviewed registry changes before treating them as authoritative. |
| Beelink-hosted Pi-hole | `svc-pihole-dns` on `host-beelink-mini-pc` | Define backup, restore validation, and controlled update requirements before further production changes. |
| Raspberry Pi Pi-hole rollback | Raspberry Pi at `192.168.50.67` | Keep intact as immediate rollback. |
| Future containers | Future service records and deployment artifacts | Define persistent volume backup and restore before cutover. |
| Network modernization | Network device registry records | Record physical topology and rollback cabling before changes. |

---

## Pi-hole Rollback Position

The Raspberry Pi remains the rollback path for Pi-hole after migration.

Rollback readiness requires:

- Current Raspberry Pi IP and SSH access recorded.
- No decommission or forced repair of Raspberry Pi in PLAT-13.6.
- Beelink Pi-hole backup and restore validation defined before further production changes.
- Rollback trigger and incident response documented.

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
| 1.1 | Updated backup and rollback position for active Beelink-hosted Pi-hole and Raspberry Pi rollback under PLAT-13.6. |
| 1.0 | Initial backup and rollback strategy. |
