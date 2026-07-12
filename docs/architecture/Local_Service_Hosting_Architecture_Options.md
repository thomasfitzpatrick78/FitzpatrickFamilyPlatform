# Local Service Hosting Architecture Options

**Document Version:** 1.1

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document records local service hosting options for Platform services after Beelink onboarding.

Pi-hole is now deployed on Beelink using Docker. Monitoring, dashboards, backup automation, and additional services remain planned until approved implementation.

---

## Hosting Options

| Option | Fit | Benefits | Risks / Unknowns |
|--------|-----|----------|------------------|
| Docker on Beelink host OS | Selected for Pi-hole and strong candidate for lightweight services | Simple operations model; good rollback through compose files and volumes | Backup, restore validation, monitoring, and update governance must mature. |
| VM on Beelink with Docker inside VM | Strong isolation candidate | Clear rollback boundary and snapshot path | Hypervisor choice, resource overhead, and USB/network passthrough TBD |
| Bare-metal service install | Weak candidate | Fewer layers | Harder rollback; more host drift |
| Keep service on Raspberry Pi | Rollback and continuity candidate | Existing Pi-hole service remains intact | Aging OS and mixed Pi-hole version state |

---

## Service Placement Guidance

- Pi-hole production service is hosted on Beelink using Docker.
- Raspberry Pi should remain intact as rollback after migration.
- Planned services should remain `planned_service` records until deployed.
- Host placement must be reflected in `host_dependencies` before implementation.
- Service deployment automation is out of scope for PLAT-13.1.

---

## Decision Inputs

Before selecting Docker-on-host or VM-hosting, record:

- Beelink hardware model.
- Host operating system.
- IP address and hostname.
- Storage layout.
- Backup target.
- Recovery path.
- Remote access model.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Updated hosting options for Beelink-hosted Docker Pi-hole production baseline and PLAT-13.6 planning. |
| 1.0 | Initial local service hosting architecture options. |
