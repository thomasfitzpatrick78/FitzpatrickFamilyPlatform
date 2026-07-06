# Infrastructure Operations Readiness

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document defines the PLAT-13.1 operations readiness architecture for moving from a static Infrastructure Registry v1.0 baseline toward managed infrastructure operations.

The Infrastructure Registry remains authoritative. This document summarizes and interprets registry records; it does not create a second inventory.

---

## Current Registry-Derived Baseline

| Area | Registry Evidence | Readiness Position |
|------|-------------------|--------------------|
| Current DNS service | `svc-pihole-dns`, `host-raspberry-pi-pihole`, `dev-raspberry-pi-pihole` | Pi-hole is active on Raspberry Pi at `192.168.50.67`. |
| Raspberry Pi OS | `host-raspberry-pi-pihole` | Raspbian GNU/Linux 10 / Debian Buster is known and recorded. |
| Pi-hole versions | `svc-pihole-dns` | Core `v5.15.5`, Web `v6.0`, and FTL `v6.4.1` are explicitly recorded as a mixed version state. |
| Future Platform host | `dev-beelink-mini-pc`, `host-beelink-mini-pc` | Beelink is planned and not yet available. |
| Network modernization | `net-switch-2-5gbe-1`, `net-switch-2-5gbe-2` | Two TP-Link 2.5Gb switches are planned and pending delivery. |
| Power continuity | `dev-ups-battery-backup` | CyberPower UPS is planned and pending delivery. |

---

## Readiness Principles

- Registry records are updated before readiness documents are revised.
- Unknown values are explicitly marked as `TBD` or described in `unknowns`.
- Active infrastructure is not assumed healthy without evidence.
- Planned infrastructure is not treated as deployed.
- Future automation and observability must derive targets from registry records.
- Raspberry Pi remains intact as rollback after Pi-hole migration.
- Finance functionality remains outside Platform scope.

---

## Operations Readiness Architecture

PLAT-13.1 prepares these future operating capabilities:

| Capability Area | PLAT-13.1 Output | Deferred Implementation |
|-----------------|------------------|-------------------------|
| Access | Remote access options and safety criteria | VPN, tunnel, agent, or remote management service |
| Hosting | Local service hosting options | Beelink OS install, VM creation, container deployment |
| Containers | Container hosting standards | Docker runtime installation and compose deployment |
| Recovery | Backup and rollback strategy | Automated backup jobs and restore orchestration |
| Migration | Pi-hole migration readiness plan | Pi-hole cutover or repair/update on Raspberry Pi |
| Onboarding | Beelink onboarding checklist | Device bring-up |
| Network | Network modernization checklist | Switch installation and topology changes |
| Validation | Static registry reporting improvements | Runtime monitoring or dashboards |

---

## Pi-hole Migration Readiness

The approved direction is to migrate Pi-hole to the Beelink using Docker or a VM after Beelink arrives.

Readiness expectations:

- Do not force repair or update on the old Raspberry Pi.
- Preserve the Raspberry Pi as a known rollback host after migration.
- Capture current Pi-hole version state in registry before migration planning.
- Record the target Beelink host and final runtime model only after architecture review.
- Define rollback criteria before any DNS cutover.

---

## Review Gates

Future implementation should not begin until these static gates are complete:

- Registry lifecycle state reflects physical arrival and onboarding status.
- Host operating system, IP address, management path, and storage layout are known.
- Backup and rollback requirements are reviewed.
- Remote access option is selected and approved.
- Container or VM hosting option is selected and approved.
- Validation remains green after registry updates.

---

## Related Documents

- [Remote Access Architecture Options](Remote_Access_Architecture_Options.md)
- [Local Service Hosting Architecture Options](Local_Service_Hosting_Architecture_Options.md)
- [Container Hosting Standards](Container_Hosting_Standards.md)
- [Backup and Rollback Strategy](Backup_and_Rollback_Strategy.md)
- [Registry-Driven Platform Lifecycle](Registry_Driven_Platform_Lifecycle.md)
- [Milestone 13 Plan](../milestones/Milestone_13/Milestone_13_Infrastructure_Operations_Readiness.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial PLAT-13.1 operations readiness architecture. |
