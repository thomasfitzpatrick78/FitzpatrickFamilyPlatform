# Local Service Hosting Architecture Options

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document records local service hosting options for planned Platform services after Beelink arrival and onboarding.

No service is deployed by PLAT-13.1.

---

## Hosting Options

| Option | Fit | Benefits | Risks / Unknowns |
|--------|-----|----------|------------------|
| Docker on Beelink host OS | Strong candidate for Pi-hole and lightweight services | Simple operations model; good rollback through compose files and volumes | Host OS, storage layout, and backup process TBD |
| VM on Beelink with Docker inside VM | Strong isolation candidate | Clear rollback boundary and snapshot path | Hypervisor choice, resource overhead, and USB/network passthrough TBD |
| Bare-metal service install | Weak candidate | Fewer layers | Harder rollback; more host drift |
| Keep service on Raspberry Pi | Rollback and continuity candidate | Existing Pi-hole service remains intact | Aging OS and mixed Pi-hole version state |

---

## Service Placement Guidance

- Pi-hole migration target is Beelink using Docker or VM after Beelink arrives.
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
| 1.0 | Initial local service hosting architecture options. |
