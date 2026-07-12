# Platform Service Lifecycle

**Document Version:** 1.0

**Status:** Active

**Milestone:** Milestone 13

---

## Purpose

This document defines the reusable lifecycle for governed Platform services.

The lifecycle applies to production services such as Pi-hole and future services such as Home Assistant, MQTT, Ollama, monitoring, and family-facing applications.

---

## Lifecycle Stages

| Stage | Required Outcome |
|-------|------------------|
| Design | The service purpose, users, owner, risks, and non-goals are documented. |
| Inventory | Host, ports, paths, dependencies, credentials model, and rollback assets are recorded. |
| Architecture review | The design, network exposure, persistence, backup, rollback, and operations model are approved. |
| Stable network identity | DHCP reservation or equivalent stable identity is created and verified before production promotion. |
| Backup | Configuration and data backup requirements are documented before production cutover. |
| Deployment | Deployment steps are repeatable, reviewed, and scoped to approved changes. |
| Validation | Direct service checks, health checks, and dependency checks pass. |
| Parallel run | The new service can run without disturbing production where practical. |
| Canary | One or more representative clients validate the service before household-wide promotion where practical. |
| Production cutover | Shared dependencies such as router DNS are changed only after rollback is ready. |
| Observation | The service is watched during a defined post-cutover period. |
| Operations | Ownership, incident severity, evidence, and recovery objectives are documented. |
| Controlled update | Version changes follow approved image, backup, validation, observation, and rollback policy. |
| Recovery | Restore and rollback paths are documented and periodically validated. |
| Retirement | Old services are removed only after replacement and rollback requirements are satisfied. |
| Closeout | Registry, runbooks, reports, and evidence are synchronized. |

---

## Required Controls

- A production service must have a documented owner.
- A production service must have stable host identity before promotion.
- A production service must document ports and dependencies.
- A production service must document backup and restore expectations.
- A production service must document rollback validation.
- A production service must define operational telemetry expectations.
- A production service must synchronize registry records before closeout.
- Repository evidence must distinguish planned capabilities from completed live implementation.

---

## Stable Network Identity Rule

Production promotion is blocked until the host address is stable.

For home-network services, this means a DHCP reservation or equivalent stable network identity is created and verified through reboot, lease renewal, or another approved validation method.

The Pi-hole cutover showed that a functioning service can still be unsafe for production if another device can obtain the expected address.

---

## Related Documents

- [Production Service Cutover Checklist](Production_Service_Cutover_Checklist.md)
- [Definition of Done](Definition_of_Done.md)
- [Engineering Lifecycle](Engineering_Lifecycle.md)
- [PLAT-13.6 Operations and Observability Specification](../specifications/Platform_Operations_Observability_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial governed reusable Platform service lifecycle for PLAT-13.6. |
