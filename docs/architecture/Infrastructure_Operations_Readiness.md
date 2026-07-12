# Infrastructure Operations Readiness

**Document Version:** 1.3

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
| Current DNS service | `svc-pihole-dns`, `host-beelink-mini-pc`, `svc-docker-engine` | Pi-hole is active in Docker on Beelink at `192.168.50.127`. |
| Raspberry Pi rollback | `svc-pihole-raspberry-pi-rollback`, `host-raspberry-pi-pihole` | Raspberry Pi remains powered on and unchanged at `192.168.50.67` as immediate rollback DNS host. |
| Production Platform host | `dev-beelink-mini-pc`, `host-beelink-mini-pc` | Beelink Mini S is active as Platform Node 001, hostname `beelink`, with Ubuntu Server 26.04 LTS and Docker Engine. |
| Metrics Foundation | `svc-prometheus`, `svc-node-exporter`, `svc-cadvisor` | Prometheus, Node Exporter, and cAdvisor are active after PLAT-13.6.2 live validation. |
| Network modernization | `net-switch-2-5gbe-1`, `net-switch-2-5gbe-2` | Two TP-Link TL-SG108S-M2 8-port 2.5G unmanaged switches are delivered and pending placement/cabling validation. |
| Power continuity | `dev-ups-battery-backup` | CyberPower CP850PFCLCD UPS is delivered and pending protected-load validation. |

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
| Onboarding | Beelink Day 0 / Day 1 bring-up guide | Physical activation, production lifecycle transition, and service deployment |
| Network | Network modernization checklist | Switch installation and topology changes |
| Validation | Static registry reporting improvements | Runtime monitoring or dashboards |

---

## Pi-hole Migration Readiness

Pi-hole migration to Beelink has completed. PLAT-13.6.2 Metrics Foundation has completed. PLAT-13.6 still plans the dashboard, backup, restore, alerting, and update governance needed for the active production service.

Readiness expectations:

- Do not decommission or modify the Raspberry Pi rollback host in PLAT-13.6.
- Preserve the Beelink DHCP reservation as a production prerequisite.
- Do not change production DNS in PLAT-13.6 repository-only planning.
- Preserve governed Metrics Foundation evidence and define backup evidence before future production changes.

---

## Review Gates

Future implementation should not begin until these static gates are complete:

- Registry lifecycle state reflects physical arrival and onboarding status.
- Host operating system, IP address, management path, and storage layout are known.
- Backup and rollback requirements are reviewed.
- Remote access option is selected and approved.
- Container or VM hosting option is selected and approved.
- Validation remains green after registry updates.
- Additional monitoring/dashboard deployment, backup automation, restore validation, and controlled updates require future implementation approval.

---

## Related Documents

- [Remote Access Architecture Options](Remote_Access_Architecture_Options.md)
- [Local Service Hosting Architecture Options](Local_Service_Hosting_Architecture_Options.md)
- [Container Hosting Standards](Container_Hosting_Standards.md)
- [Backup and Rollback Strategy](Backup_and_Rollback_Strategy.md)
- [Registry-Driven Platform Lifecycle](Registry_Driven_Platform_Lifecycle.md)
- [Milestone 13 Plan](../milestones/Milestone_13/Milestone_13_Infrastructure_Operations_Readiness.md)
- [PLAT-13.6 Operations and Observability Specification](../specifications/Platform_Operations_Observability_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.3 | Recorded active PLAT-13.6.2 Metrics Foundation and remaining operations readiness boundaries. |
| 1.2 | Updated baseline for active Beelink-hosted Pi-hole and PLAT-13.6 operations/observability planning. |
| 1.1 | Updated current baseline for delivered Beelink Mini S, TP-Link TL-SG108S-M2 switches, and CyberPower CP850PFCLCD UPS under PLAT-13.3. |
| 1.0 | Initial PLAT-13.1 operations readiness architecture. |
