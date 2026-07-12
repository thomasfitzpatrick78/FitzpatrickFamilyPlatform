# Pi-hole Service Objectives

**Document Version:** 1.0

**Status:** Active

**Milestone:** Milestone 13

---

## Purpose

This document defines initial operational objectives for the family DNS and blocking service.

These are pragmatic household operating objectives, not contractual enterprise service-level agreements.

---

## Service Summary

| Field | Value |
|-------|-------|
| Service | Family DNS and blocking |
| Customer-facing users | Household devices and family members |
| Production host | `beelink` |
| Production IP | `192.168.50.127` |
| DNS ports | TCP/UDP `53` |
| Admin port | TCP `8080` |
| Runtime | Docker container `pihole` |
| Compose path | `/platform/compose/pihole` |
| Persistent configuration | `/platform/data/pihole/etc-pihole` |
| Immediate rollback | Raspberry Pi Pi-hole at `192.168.50.67` |
| Special client note | Proton VPN on MacBook intentionally uses Proton DNS while connected |

---

## Initial Objectives

| Objective | Initial Target |
|-----------|----------------|
| Availability | Pi-hole DNS should be available during normal household use, excluding approved maintenance. |
| DNS response validation | Direct DNS queries to `192.168.50.127` should resolve known public domains. |
| Blocking validation | A known blocked domain should be blocked during validation. |
| Container health | Container health should be healthy after restart and during observation. |
| Backup frequency | Daily configuration backup planned, not yet implemented by this repository workstream. |
| Restore objective | Restore validation planned before backup is considered proven. |
| Rollback objective | Raspberry Pi remains powered on and unchanged for immediate DNS rollback. |
| Alert ownership | Family Platform owner, administered from Tom's MacBook. |
| Observation evidence | Health, DNS response, blocked-domain check, dashboard client presence, and notes from representative clients. |

---

## Recovery Objectives

Initial recovery objectives:

- DNS outage should be detected quickly through household symptoms or planned monitoring.
- If Beelink Pi-hole cannot be recovered promptly, rollback to Raspberry Pi DNS should be considered.
- Restore confidence is not established until restore validation is tested.

---

## Evidence Expectations

Capture:

- Date and time of validation.
- Host IP checked.
- Container health result.
- DNS query result.
- Blocklist check result.
- Any client reports.
- Whether Proton VPN was connected on the MacBook during testing.

---

## Non-Goals

This document does not deploy monitoring, backups, alerts, dashboards, update automation, or router changes.

---

## Related Documents

- [PLAT-13.6 Operations and Observability Specification](../specifications/Platform_Operations_Observability_Specification.md)
- [Incident Response Runbooks](Incident_Response_Runbooks.md)
- [Backup and Restore Operations Specification](../architecture/Backup_Restore_Operations_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Pi-hole operational objectives for PLAT-13.6. |
