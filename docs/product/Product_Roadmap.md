# Product Roadmap

**Document Version:** 4.2

**Status:** Active

**Milestone:** Milestone 15

---

## Purpose

This roadmap organizes portfolio direction by milestone horizon without prescribing implementation details.

---

## Current Milestone

### Milestone 15

Focus: increase Engineering Organization throughput through delivery leverage.

Planned outcomes:

- Complete FFFA customer acceptance through FFFA-owned evidence and decision authority.
- Deliver additional Platform implementation only through separately authorized work packages.
- Apply the published EO-15.1 fail-closed baseline and Transition Review mechanisms through authorized future work packages.
- Reuse AI Collaboration, Execution Capability, automation, Platform Operations, Registry, evidence, and validation governance before expanding it.
- Preserve architecture, implementation, artifact, deployment, observation, consumer, activation, release, and live-work gates.
- Retain ADR-012 `Implemented: No`, Capability-First as unpromoted, and AB-012 in backlog until later evidence justifies change.

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

## Milestone 15 Planning Streams

Milestone 15 planning is coordinated across EO, PLAT, and FFFA streams. This roadmap records completed EO-15.1 repository implementation under its separate published work-package authority. The remaining streams are planned, not approved for implementation by this roadmap.

### EO - Engineering Organization

- EO-15.1 Engineering Lifecycle Transition Review Operationalization is Architecture Gatekeeper approved and published.
- The standing generated-evidence policy is authoritative after successful publication and post-publication verification; it does not authorize implementation by itself.
- AI Collaboration Governance, EO-14.1A, and EO-14.4A remain published reusable foundations; activation remains separate.
- Delivery-leverage observations must avoid unsupported precision.
- Existing governance is reused before any expansion proposal.

### PLAT - Shared Platform

- Deliver additional Platform implementation from an existing approved direction.
- Require a separate governed work package before implementation.
- Preserve the PLAT-14.1A source, artifact, deployment, target, observation, consumer, recurrence, and activation gates.
- Keep ADR-012 `Implemented: No` until the applicable implementation and acceptance gates are satisfied.
- Keep live Grafana, Prometheus, OpenTelemetry, Docker, Beelink, backup, restore, alerting, and production work behind separate architecture and human approval.

### FFFA - Customer-Facing Application

- Complete governed customer acceptance in the FamilyFinanceAssistant repository.
- Preserve repository independence and keep customer data and detailed acceptance evidence outside this repository.
- Require the FFFA-owned product and architecture decision before implementation resumes.
- Do not convert technical correctness or Platform portfolio traceability into a customer-readiness claim.

---

## Milestone 14 Closeout Baseline

Milestone 14 completed the governed Container Operational Health vertical slice at its approved repository and architecture boundaries. EO-14.8, EO-14.1A, EO-14.4A, PLAT-14.0A, Registry identity and migration controls, fixture-only PLAT-14.1A, provider/proxy foundations, the transport-free source, and the closed socket-capable implementation review are published. Charlie closed unstarted, FFFA customer acceptance remained incomplete, and every live gate remained separate.

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
- [Milestone 14 Transition Review](../milestones/Milestone_14/Milestone_14_Transition_Review.md)
- [Milestone 15 Portfolio Plan](../milestones/Milestone_15/Milestone_15_Portfolio_Plan.md)
- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)
- [Container Operational Health Specification](../specifications/Container_Operational_Health_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 4.2 | Recorded Architecture Gatekeeper approval and governed publication of EO-15.1 while preserving separate implementation and live-work gates. |
| 4.1 | Recorded completed, unpublished EO-15.1 repository implementation pending Architecture Gatekeeper review. |
| 4.0 | Activated Milestone 15 delivery-leverage direction, EO-15.1 future authority, FFFA customer acceptance, and separately gated Platform implementation while preserving the Milestone 14 closeout baseline. |
| 3.18 | Recorded Architecture Gatekeeper approval and publication of the closed socket-capable transport review while preserving every source and operational gate. |
| 3.17 | Recorded Architecture Gatekeeper approval, acceptance, and publication of the transport-free source while preserving every later implementation and operational gate. |
| 3.16 | Recorded the completed transport-free privileged-proxy source review tree and retained the Architecture Gatekeeper publication hold plus every socket, artifact, deployment, and operational gate. |
| 3.15 | Recorded publication of the approved purpose-built privileged-proxy architecture and acceptance package without authorizing implementation or deployment. |
| 3.14 | Recorded publication of the repository-only privileged deployment configuration foundation while preserving socket-capable implementation, credential, target, observation, consumer, activation, and live gates. |
| 3.13 | Recorded publication of the repository-only constrained proxy foundation while preserving privileged deployment, eligible-target, named-target observation, consumer, activation, and live gates. |
| 3.12 | Recorded the constrained-proxy security review and repository-only proxy foundation as the next recommended gate without authorizing implementation, deployment, credentials, observation, or live work. |
| 3.11 | Recorded publication of the repository-only Production Provider Adapter Foundation while retaining all target, privileged, live, consumer, recurring, and activation gates. |
| 3.10 | Recorded publication of the accepted production provider architecture/security package while preserving implementation, access, consumer, activation, and live-work boundaries. |
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
