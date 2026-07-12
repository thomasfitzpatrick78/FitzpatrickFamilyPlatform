# Product Roadmap

**Document Version:** 1.9

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This roadmap organizes portfolio direction by milestone horizon without prescribing implementation details.

---

## Current Milestone

### Milestone 12

Focus: establish Infrastructure Registry v1.0 as the first usable Platform capability.

Planned outcomes:

- Git-native structured infrastructure registry architecture.
- YAML or JSON registry record model.
- Human-readable documentation derived from registry records.
- Validation-first registry design.
- Workstreams for devices, topology, services, health foundation, and operating environment.
- Future readiness for monitoring, dashboards, and automation.

---

## Near-Term Roadmap

Near-term candidates should build from Infrastructure Registry v1.0:

- Infrastructure operations readiness.
- Remote access architecture selection.
- Local service hosting architecture selection.
- Pi-hole migration readiness.
- Beelink Day 0 / Day 1 bring-up planning for delivered Platform Node 001 hardware.
- Platform operations and observability for active Beelink-hosted Pi-hole service, including completed PLAT-13.6.2 Metrics Foundation, PLAT-13.6.3 Grafana dashboard validation, PLAT-13.6.3A Docker-container metrics correction, PLAT-13.6.3B restricted proxy plus OTel Docker Stats preparation, and planned alerting, backup, restore, and update work.
- Network modernization readiness.
- First Home Automation capability readiness assessment after registry foundation.

---

## Milestone 14 Planning Streams

Milestone 14 planning is coordinated across EO, PLAT, and FFFA streams. These candidates are planned, not approved for implementation by this roadmap.

### EO - Engineering Organization

- EO-14.1 AI Role Catalog Operationalization.
- EO-14.2 Execution Agent Specification.
- EO-14.3 Governed Automation Framework.
- EO-14.4 Operations Analyst / Operations Intelligence.
- EO-14.5 Engineering Organization Metrics.
- EO-14.6 Capability Maturity Assessment.
- EO-14.7 AI Collaboration and Approval Model.

### PLAT - Shared Platform

- Complete governed Container Metrics replacement.
- Platform alerting.
- Backup and recovery.
- Restore validation.
- Controlled updates.
- Observability integration.

### FFFA - Customer-Facing Application

- Identify one approved Fitzpatrick Family Financial Assistant customer-facing capability candidate through existing FFFA backlog and roadmap governance.
- Preserve repository independence and avoid inventing detailed FFFA implementation scope in this repository.
- Use the selected candidate to satisfy Milestone 14 Engineering Investment Rule traceability.

---

## Future Roadmap

Future roadmap candidates include:

- Energy management planning.
- Governed AI services.
- Family intelligence evidence model.
- Cross-domain household dashboards.
- Portfolio-level shared engineering review after multiple repositories provide evidence.

---

## Deferred Initiatives

Deferred initiatives remain in backlog until requirements and architecture are approved:

- Finance functionality.
- Banking integrations.
- Budgeting workflows.
- Transaction workflows.
- Investment tracking.
- Cloud services.
- GitHub Actions.
- Shared package extraction.
- Runtime monitoring until registry validation is established.
- Dashboards until registry records and health status are validated.
- Beelink activation until Day 0 / Day 1 onboarding evidence is reviewed.
- Further Pi-hole production changes until PLAT-13.6 backup, observability, and controlled update requirements are reviewed.
- Deployment automation until registry-driven lifecycle gates are approved.
- Additional monitoring/dashboard live deployment, alerting, backup automation, restore validation, and controlled updates beyond reviewed PLAT-13.6 repository packages until each later PLAT-13.6 work package is approved.

---

## Related Documents

- [Product Backlog](Product_Backlog.md)
- [Capability Model](Capability_Model.md)
- [Architecture Backlog](../architecture/Architecture_Backlog.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Milestone 12 Plan](../milestones/Milestone_12/Milestone_12_Infrastructure_Registry_v1.0.md)
- [Engineering Organization Roadmap](../engineering-organization/Engineering_Organization_Roadmap.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.9 | Added planned Milestone 14 EO, PLAT, and FFFA roadmap streams for Engineering Investment Rule traceability. |
| 1.8 | Added PLAT-13.6.3B governed Docker-container metrics replacement preparation. |
| 1.7 | Added PLAT-13.6.3A Docker-container metrics correction to near-term roadmap. |
| 1.6 | Added PLAT-13.6.3 repository-prepared Operations Dashboard to near-term roadmap. |
| 1.5 | Updated roadmap for completed PLAT-13.6.2 Metrics Foundation and remaining planned operations work. |
| 1.4 | Added PLAT-13.6 operations and observability planning to the near-term roadmap. |
| 1.3 | Added PLAT-13.3 Beelink Day 0 / Day 1 bring-up planning to the near-term roadmap. |
| 1.2 | Added PLAT-13.1 Infrastructure Operations Readiness near-term roadmap items. |
| 1.1 | Added Infrastructure Registry v1.0 as the first Platform feature milestone for Milestone 12. |
| 1.0 | Initial Platform product roadmap. |
