# Milestone 13 - Infrastructure Operations Readiness

**Document Version:** 1.2

**Status:** Planned

**Milestone:** Milestone 13

---

## Objective

Prepare the Fitzpatrick Family Platform for managed infrastructure operations while preserving the registry-first Platform Digital Twin architecture established in Milestone 12.

---

## Workstream

| Workstream | Name | Objective |
|------------|------|-----------|
| PLAT-13.1 | Infrastructure Operations Readiness | Define static readiness architecture, options, standards, and checklists for future managed infrastructure operations. |
| PLAT-13.3 | Beelink Bring-up | Define governed Day 0 / Day 1 onboarding instructions for the delivered Beelink Mini S without service migration or production DNS changes. |

---

## Architecture Pattern

Milestone 13 continues the registry-driven Platform lifecycle:

```text
Authoritative Registry -> Validation -> Automation -> Observability -> AI Reasoning
```

PLAT-13.1 and PLAT-13.3 advance the first two stages only. They may prepare future automation and observability, but they do not implement runtime monitoring, polling, discovery, deployment automation, remote management, or dashboards.

---

## Scope

PLAT-13.1 includes:

- Registry completeness improvements for known and planned infrastructure.
- Explicit `TBD` and unknown field handling.
- Operations readiness architecture.
- Remote access architecture options.
- Local service hosting architecture options.
- Container hosting standards.
- Backup and rollback strategy.
- Pi-hole migration readiness plan.
- Beelink onboarding readiness checklist.
- Network modernization readiness checklist.
- Registry-driven Platform lifecycle pattern documentation.
- Static validation and reporting improvements aligned with Platform EAP.

PLAT-13.3 includes:

- Registry updates for delivered Beelink Mini S hardware facts.
- Registry updates for delivered TP-Link TL-SG108S-M2 switches and CyberPower CP850PFCLCD UPS.
- Governed Day 0 / Day 1 Beelink bring-up instructions.
- Ubuntu Server 24.04 LTS operating baseline approval.
- Factory Windows erase disposition with no Windows image created.
- Registry evidence checkpoints after BIOS verification, Ubuntu installation, networking completion, and SSH verification.
- Explicit rollback and no-impact guidance preserving Raspberry Pi Pi-hole service.
- Validation evidence for documentation and registry changes.

---

## Non-Goals

PLAT-13.1 does not implement:

- Beelink bring-up.
- Pi-hole migration execution.
- Runtime monitoring.
- Device polling.
- Network discovery.
- Deployment automation.
- Dashboards.
- Remote management implementation.
- Finance functionality.

PLAT-13.3 does not implement:

- Pi-hole migration.
- Router DNS changes.
- Home Assistant, MQTT, Ollama, monitoring, dashboard, or remote management installation.
- Network modernization.
- Docker installation.
- Beelink active lifecycle transition before physical setup and validation.

---

## Acceptance Criteria

PLAT-13.1 is ready for architecture review when:

- Registry records represent the known Raspberry Pi Pi-hole baseline.
- Beelink, TP-Link switches, and CyberPower UPS are represented as planned infrastructure.
- Unknown and `TBD` fields are explicit in registry records.
- Operations readiness options and checklists are documented.
- Pi-hole migration readiness is documented without forcing repair or upgrade on the Raspberry Pi.
- Platform EAP reports explicit unknown fields during static registry validation.
- Existing repository validation commands have been attempted and results are recorded.

PLAT-13.3 is ready for architecture review when:

- Delivered hardware facts are recorded in registry records.
- The UPS model is recorded as CyberPower CP850PFCLCD, not CP1000PFCLCD.
- The Beelink Day 0 / Day 1 bring-up guide covers physical inspection, safe first power-on, BIOS inspection, OS approach, hostname, static DHCP reservation, SSH setup, admin user approach, Docker readiness, validation, and rollback/no-impact guidance.
- The guide identifies Ubuntu Server 24.04 LTS as the approved operating system and factory Windows as erased with no Windows image created.
- The guide requires registry evidence capture immediately after BIOS verification, Ubuntu installation, networking completion, and SSH verification.
- The Beelink remains `planned` or pending onboarding until physical setup is completed and verified.
- Validation commands have been attempted and results are recorded.

---

## Related Documents

- [Infrastructure Operations Readiness](../../architecture/Infrastructure_Operations_Readiness.md)
- [Remote Access Architecture Options](../../architecture/Remote_Access_Architecture_Options.md)
- [Local Service Hosting Architecture Options](../../architecture/Local_Service_Hosting_Architecture_Options.md)
- [Container Hosting Standards](../../architecture/Container_Hosting_Standards.md)
- [Backup and Rollback Strategy](../../architecture/Backup_and_Rollback_Strategy.md)
- [Registry-Driven Platform Lifecycle](../../architecture/Registry_Driven_Platform_Lifecycle.md)
- [Beelink Day 0 / Day 1 Bring-up Guide](../../architecture/Beelink_Onboarding_Readiness_Checklist.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Applied PLAT-13.3 Architecture Review Board decisions for OS baseline, Windows disposition, registry evidence checkpoints, and Docker deferral. |
| 1.1 | Added PLAT-13.3 Beelink bring-up planning scope and architecture review criteria. |
| 1.0 | Initial PLAT-13.1 Infrastructure Operations Readiness plan. |
