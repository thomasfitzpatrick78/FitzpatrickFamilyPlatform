# Pi-hole Migration Readiness Plan

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This plan defines readiness for a future Pi-hole migration from Raspberry Pi to Beelink.

No migration, repair, upgrade, deployment, cutover, or runtime validation is implemented by PLAT-13.1.

---

## Current State

Registry records identify:

- Pi-hole service: `svc-pihole-dns`.
- Current host: `host-raspberry-pi-pihole`.
- Current device: `dev-raspberry-pi-pihole`.
- Current IP address: `192.168.50.67`.
- Current SSH access: `pi@192.168.50.67`.
- Raspberry Pi OS: Raspbian GNU/Linux 10 / Debian Buster.
- Pi-hole mixed version state: Core `v5.15.5`, Web `v6.0`, FTL `v6.4.1`.

---

## Approved Direction

Migrate Pi-hole to the Beelink using Docker or a VM after Beelink arrives.

The Raspberry Pi should remain intact as rollback after migration.

---

## Readiness Checklist

| Item | Status |
|------|--------|
| Current Pi-hole service record includes version state | Complete |
| Current Raspberry Pi IP and SSH access are recorded | Complete |
| Beelink is represented as planned infrastructure | Complete |
| Target runtime model selected: Docker on host or VM | TBD |
| Beelink OS, IP, hostname, and storage layout recorded | TBD |
| Pi-hole backup/export process selected | TBD |
| DNS cutover plan written | TBD |
| Rollback trigger and steps written | TBD |
| Post-cutover validation criteria written | TBD |

---

## Non-Goals

- Do not force repair or update on the old Raspberry Pi.
- Do not bring up Beelink.
- Do not create Docker or VM deployment artifacts.
- Do not change DNS.
- Do not implement monitoring or dashboards.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Pi-hole migration readiness plan. |
