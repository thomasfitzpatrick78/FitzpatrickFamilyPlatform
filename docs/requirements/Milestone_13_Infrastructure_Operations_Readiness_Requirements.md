# Milestone 13 Infrastructure Operations Readiness Requirements

**Document Version:** 1.4

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document defines requirements for PLAT-13.1 Infrastructure Operations Readiness and PLAT-13.3 Beelink Bring-up planning.

---

## Objective

Prepare the Platform for future managed infrastructure operations while preserving the Infrastructure Registry as the source of truth.

---

## Functional Requirements

- Update registry records for known Raspberry Pi Pi-hole facts.
- Represent delivered Beelink, TP-Link 2.5Gb switches, and CyberPower UPS as planned infrastructure until physical setup, installation, and onboarding validation are complete.
- Make unknown or `TBD` fields explicit in registry records.
- Document operations readiness architecture.
- Document remote access architecture options.
- Document local service hosting architecture options.
- Document container hosting standards.
- Document backup and rollback strategy.
- Document Pi-hole migration readiness.
- Document Beelink onboarding readiness.
- Document network modernization readiness.
- Document the Registry-Driven Platform Lifecycle pattern.
- Extend Platform EAP static validation/reporting for explicit unknown field visibility.
- Record delivered Beelink Mini S hardware facts while keeping lifecycle pending onboarding.
- Record delivered TP-Link TL-SG108S-M2 switch facts.
- Record delivered CyberPower CP850PFCLCD UPS facts and avoid CP1000PFCLCD references.
- Document Day 0 / Day 1 Beelink bring-up steps without migrating Pi-hole or changing router DNS.
- Use Ubuntu Server 24.04 LTS as the approved Beelink operating system baseline.
- Document factory Windows as erased during Ubuntu Server installation with no Windows image created.
- Capture registry evidence immediately after BIOS verification, Ubuntu installation, networking completion, and SSH verification.

---

## Non-Functional Requirements

- Registry records remain authoritative.
- Readiness documents derive from or cite registry records where practical.
- Validation remains deterministic and local-file based.
- No runtime discovery, polling, monitoring, dashboards, deployment automation, or remote management shall be implemented.
- No planned service installation shall be bundled into Beelink bring-up planning.
- Docker installation shall remain out of scope for PLAT-13.3 and be deferred to a future workstream.
- Raspberry Pi Pi-hole remained active until the approved migration workstream completed; PLAT-13.6 records it as rollback infrastructure.
- PLAT-13.6.2 records the approved live Metrics Foundation deployment for Prometheus, Node Exporter, and cAdvisor.
- PLAT-13.6 shall not deploy Grafana, backups, alerts, restore validation, update automation, or additional live infrastructure changes without separate approval.
- Finance functionality remains excluded.

---

## Related Documents

- [Milestone 13 Plan](../milestones/Milestone_13/Milestone_13_Infrastructure_Operations_Readiness.md)
- [Infrastructure Operations Readiness Specification](../specifications/Infrastructure_Operations_Readiness_Specification.md)
- [Infrastructure Operations Readiness](../architecture/Infrastructure_Operations_Readiness.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.4 | Recorded completed PLAT-13.6.2 Metrics Foundation while preserving later operations boundaries. |
| 1.3 | Added PLAT-13.6 operations and observability planning requirements and updated Raspberry Pi role to rollback after migration. |
| 1.2 | Applied PLAT-13.3 Architecture Review Board decisions for Ubuntu Server 24.04 LTS, factory Windows erase disposition, checkpoint evidence capture, and Docker deferral. |
| 1.1 | Added PLAT-13.3 delivered hardware and Beelink Day 0 / Day 1 bring-up planning requirements. |
| 1.0 | Initial PLAT-13.1 requirements. |
