# Infrastructure Operations Readiness Specification

**Document Version:** 1.2

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This specification defines PLAT-13.1 Infrastructure Operations Readiness and PLAT-13.3 Beelink Bring-up planning as documentation, registry, and static validation increments.

---

## Capability Boundary

Infrastructure Operations Readiness prepares future managed infrastructure operations. It does not execute operations.

The implementation boundary is:

- Registry updates are allowed.
- Architecture and readiness documents are allowed.
- Static validation and reporting improvements are allowed.
- Governed Day 0 / Day 1 Beelink bring-up instructions are allowed.
- Runtime monitoring, polling, discovery, dashboards, deployment automation, remote management implementation, service installation, Pi-hole migration, router DNS changes, and physical Beelink activation are not allowed.
- Docker installation is not allowed in PLAT-13.3 and shall be performed only in a future approved workstream.

---

## Registry Requirements

Registry records shall:

- Identify Raspberry Pi Pi-hole IP address and SSH access.
- Identify Raspberry Pi OS as Raspbian GNU/Linux 10 / Debian Buster.
- Identify Pi-hole mixed version state.
- Keep Beelink lifecycle status as `planned` until physical setup and onboarding validation are complete.
- Keep TP-Link switches and CyberPower UPS lifecycle status as `planned` until placement, cabling, protected-load, and installation validation are complete.
- Identify delivered Beelink as Beelink Mini S with Intel N150 CPU, 16GB memory, 512GB storage, and 12V / 3A input.
- Identify Ubuntu Server 24.04 LTS as the approved Beelink operating system baseline.
- Identify factory Windows as erased during Ubuntu Server installation with no Windows image created.
- Require registry evidence capture immediately after BIOS verification, Ubuntu installation, networking completion, and SSH verification.
- Identify delivered switches as TP-Link TL-SG108S-M2 8-port 2.5G unmanaged switches.
- Identify delivered UPS as CyberPower CP850PFCLCD, 850VA / 510W.
- Track unknowns explicitly using `TBD` or `unknowns`.

---

## Documentation Requirements

PLAT-13.1 shall provide:

- Operations readiness architecture.
- Remote access options.
- Local service hosting options.
- Container hosting standards.
- Backup and rollback strategy.
- Pi-hole migration readiness plan.
- Beelink Day 0 / Day 1 bring-up guide.
- Network modernization checklist.
- Registry-driven Platform lifecycle pattern.

---

## Validation Requirements

Platform EAP shall continue to validate the Infrastructure Registry through local-file checks.

PLAT-13.1 adds informational reporting for explicit unknown or `TBD` markers. This reporting improves review visibility and does not imply runtime inspection.

---

## Non-Goals

- Beelink bring-up.
- Pi-hole migration.
- Router DNS changes.
- Runtime monitoring.
- Deployment automation.
- Dashboards.
- Remote management implementation.
- Finance functionality.

---

## Related Documents

- [Milestone 13 Requirements](../requirements/Milestone_13_Infrastructure_Operations_Readiness_Requirements.md)
- [Infrastructure Operations Readiness](../architecture/Infrastructure_Operations_Readiness.md)
- [Platform Digital Twin Integrity Model](../architecture/Platform_Digital_Twin_Integrity_Model.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Applied PLAT-13.3 Architecture Review Board operating system, Windows disposition, evidence checkpoint, and Docker deferral decisions. |
| 1.1 | Added PLAT-13.3 delivered hardware registry requirements and Beelink Day 0 / Day 1 planning boundary. |
| 1.0 | Initial PLAT-13.1 specification. |
