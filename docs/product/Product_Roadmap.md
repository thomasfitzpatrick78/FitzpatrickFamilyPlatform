# Product Roadmap

**Document Version:** 3.9

**Status:** Active

**Milestone:** Milestone 14

---

## Purpose

This roadmap organizes portfolio direction by milestone horizon without prescribing implementation details.

---

## Current Milestone

### Milestone 14

Focus: operationalize the AI Engineering Organization through the governed Container Operational Health vertical slice while preserving separate architecture and live-execution gates.

Planned outcomes:

- Preserve the completed, Architecture Gatekeeper-approved EO-14.8 AI Collaboration Governance capability as the published Engineering Organization baseline.
- Preserve the published Architecture Gatekeeper-approved EO-14.1A and EO-14.4A repository implementations and keep activation, Bravo, and Charlie behind separate authorization gates.
- Preserve the published fixture-only PLAT-14.1A repository slice and completed five-record `not_applicable` migration while keeping remaining migration, providers, dashboards/APIs, activation, and live work behind separate gates.
- Prepare Engineering Organization controls, Platform observability, and Operations Intelligence through governed repository work packages.
- Retain FFFA customer-value traceability while FFFA implementation remains paused for customer acceptance.
- Keep live Grafana, Prometheus, OpenTelemetry, Docker, Beelink, backup, restore, alerting, and production work behind separate PLAT and human approval gates.

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

The approved Milestone 14 execution strategy is Option C - Governed Vertical Slice. The first governed vertical slice is Container Operational Health.

### EO - Engineering Organization

- EO-14.1 Execution Agent Specification.
- EO-14.1A Execution Agent Operationalization repository implementation is published; role activation remains separate.
- EO-14.2 Operations Analyst Specification.
- EO-14.2A Operations Analyst Operationalization for Container Operational Health evidence interpretation.
- EO-14.3 Engineering Metrics v2.
- EO-14.3A Engineering Metrics v2 Refinement based on verified vertical-slice evidence.
- EO-14.4 Governed Automation Framework.
- EO-14.4A Governed Automation Framework Option B repository implementation is published; automation remains unactivated.
- EO-14.8 AI Collaboration Governance is complete and published as the Engineering Organization baseline.
- EO-14.8A Capability Charter is complete.
- EO-14.8B Repository Specification Package is complete.
- EO-14.8C Repository Implementation is complete through EO-14.8C.1 and EO-14.8C.2.
- EO-14.8D AI Session Readiness Validator is complete.
- EO-14.8E Engineering Metrics Integration is complete.
- EO-14.8 parent capability is complete and Architecture Gatekeeper approved.
- Alpha EO-14.1A and EO-14.4A repository implementations are published.
- The bounded Bravo Foundation and PLAT-14.1A Option B fixture-only repository implementation are published; Charlie remains unstarted. No Execution Agent activation, provider access, dashboard/API work, or live work is authorized.

### PLAT - Shared Platform

- PLAT-14.0A Platform Operations Domain Architecture and canonical contracts are published at `c8f9bc3446cb1d5c23bf32232203109a7ff067f8`; implementation remains absent.
- PLAT-14.1 Container Metrics Modernization.
- Foundation schema `1.1`, strict validation, migration planning/execution/rollback/completion, CLI, and tests are published. Exactly five records are migrated as `not_applicable`; 16 remain review-required. The PLAT-14.1A Option B fixture-only repository vertical slice is Architecture Gatekeeper accepted and published; telemetry-provider, security, observation, dashboard/API, activation, and live work remain later gates.
- PLAT-14.2 Operational Excellence for backup, restore, recovery validation, alerting, runbooks, and evidence retention.
- PLAT-14.3 Platform Health Dashboard.
- PLAT-14.3A Platform Health Dashboard Completion after the verified PLAT-14.1A telemetry contract.
- PLAT-14.4 Platform Authentication Boundary for local reverse proxy authentication, identity-header trust, LAN-only HTTPS, certificate lifecycle, monitoring, backup, recovery, and access revocation; deferred unless future FFFA web implementation approval activates it.

### FFFA - Customer-Facing Application

- FFFA-14.1 Transaction Categorization Intelligence.
- FFFA-14.2 Family Financial Reporting and Presentation.
- FFFA implementation is paused while Chris completes customer acceptance.
- The Financial Domain Foundation remains frozen for the rest of Milestone 14 except for separately approved defect fixes.
- Preserve repository independence and avoid inventing detailed FFFA implementation scope in this repository.
- Use FFFA-owned personas, reporting contracts, channel specifications, and customer acceptance evidence to satisfy Milestone 14 Engineering Investment Rule traceability.

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
- [Milestone 14 Portfolio Plan](../milestones/Milestone_14/Milestone_14_Portfolio_Plan.md)
- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)
- [Container Operational Health Specification](../specifications/Container_Operational_Health_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 3.9 | Recorded exact five-record Registry migration and post-migration planner lifecycle correction while preserving provider, consumer, activation, and live-work gates. |
| 3.8 | Recorded Architecture Gatekeeper acceptance and publication of the PLAT-14.1A Option B fixture-only repository vertical slice while preserving all migration, provider, consumer, activation, and live gates. |
| 3.7 | Recorded the complete unpublished PLAT-14.1A Option B repository vertical slice while preserving all publication, migration, provider, activation, and live gates. |
| 3.6 | Recorded Architecture Gatekeeper acceptance and publication of the Registry identity prerequisite while keeping migration, PLAT, provider, and live gates separate. |
| 3.5 | Recorded complete unpublished Registry identity prerequisite implementation while keeping migration, PLAT, provider, and live gates separate. |
| 3.4 | Recorded PLAT-14.1A and Registry Container Identity Foundation architecture/specification publication with implementation blocked. |
| 3.3 | Recorded PLAT-14.0A publication and PLAT-14.1A Container Operational Health specification alignment with implementation and later gates blocked. |
| 3.2 | Added PLAT-14.0A Platform Operations domain architecture and blocked PLAT-14.1A pending publication and alignment. |
| 3.1 | Recorded publication of the Architecture Gatekeeper-approved EO-14.4A repository implementation while preserving activation and live-work gates. |
| 3.0 | Recorded EO-14.4A Option B repository implementation complete pending Architecture Gatekeeper review while preserving activation and live-work gates. |
| 2.9 | Recorded EO-14.4A orchestration alignment with the published EO-14.1A Execution Capability while preserving separate implementation and activation gates. |
| 2.8 | Recorded publication of the Architecture Gatekeeper-approved EO-14.1A repository implementation while preserving separate activation and later work packages. |
| 2.7 | Recorded EO-14.1A repository implementation pending Architecture Gatekeeper review, with EO-14.4A, Bravo, Charlie, activation, and live work unchanged. |
| 2.6 | Recorded the completed and published EO-14.8 baseline, with Alpha EO-14.1A and EO-14.4A next and all three workstreams still unstarted. |
| 2.5 | Corrected active-milestone metadata and framing to Milestone 14 and recorded EO-14.8E implementation-review status. |
| 2.4 | Recorded EO-14.8D implementation-review status, EO-14.8E approval dependency, and unchanged workstream boundaries. |
| 2.3 | Added EO-14.8 AI Collaboration Governance roadmap status and Alpha, Bravo, Charlie pause treatment. |
| 2.2 | Recorded approved Milestone 14 Option C governed vertical slice, Container Operational Health sequencing, FFFA implementation pause, and Financial Domain Foundation freeze. |
| 2.1 | Added Platform-owned authentication boundary roadmap scope for FFFA-14.2B. |
| 2.0 | Aligned Milestone 14 roadmap streams to approved portfolio work packages and FFFA-14 scope. |
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
