# Pi-hole Migration Readiness Plan

**Document Version:** 1.1

**Status:** Superseded by PLAT-13.6 production baseline

**Milestone:** Milestone 13

---

## Purpose

This plan defined readiness for the Pi-hole migration from Raspberry Pi to Beelink.

The migration has since completed. PLAT-13.6 records the Beelink-hosted Pi-hole production baseline and preserves the Raspberry Pi as rollback.

---

## Current State

Registry records now identify:

- Pi-hole service: `svc-pihole-dns`.
- Current production host: `host-beelink-mini-pc`.
- Current production IP address: `192.168.50.127`.
- Current runtime: Docker on Beelink.
- Rollback service: `svc-pihole-raspberry-pi-rollback`.
- Rollback host: `host-raspberry-pi-pihole` at `192.168.50.67`.

---

## Approved Direction

Maintain Beelink-hosted Pi-hole as production service and keep Raspberry Pi intact as rollback.

---

## Readiness Checklist

| Item | Status |
|------|--------|
| Current Pi-hole service record includes version state | Complete |
| Current Raspberry Pi IP and SSH access are recorded | Complete |
| Beelink is represented as planned infrastructure | Complete |
| Target runtime model selected: Docker on host | Complete |
| Beelink OS, IP, hostname, and storage layout recorded | Partial - host, IP, OS, runtime, and platform root recorded; storage layout details continue in PLAT-13.6 |
| Pi-hole backup/export process selected | Planned in PLAT-13.6 |
| DNS cutover completed | Complete |
| Rollback trigger and steps written | Planned in PLAT-13.6 incident runbooks |
| Post-cutover validation criteria written | Planned in PLAT-13.6 service objectives |

---

## Non-Goals

- Do not force repair or update on the old Raspberry Pi.
- Do not decommission Raspberry Pi rollback.
- Do not change DNS in PLAT-13.6 repository-only planning.
- Do not deploy monitoring or dashboards in PLAT-13.6 repository-only planning.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Marked migration readiness plan superseded by Beelink-hosted Pi-hole production baseline and PLAT-13.6 operations planning. |
| 1.0 | Initial Pi-hole migration readiness plan. |
