# Product Backlog

**Document Version:** 3.12

**Status:** Active

**Milestone:** Milestone 14

---

## Purpose

This document defines the initial repository-managed Product Backlog for the Fitzpatrick Family Platform.

---

## Status Values

- Candidate
- Planned
- Paused
- Blocked
- Superseded
- Deferred
- Completed

---

## Backlog

| ID | Priority | Capability | Epic | Feature | Candidate Milestone | Status | Dependencies |
|----|:--------:|------------|------|---------|---------------------|--------|--------------|
| PLAT-PB-001 | High | Infrastructure | Repository foundation | Establish governed Platform repository | Milestone 11 | Completed | Approved Milestone 10 repository creation specification |
| PLAT-PB-002 | High | Infrastructure | Engineering foundation | Initialize validation and evidence automation | Milestone 11 | Completed | PLAT-PB-001 |
| PLAT-PB-003 | High | Shared Services | Governance foundation | Establish product, architecture, and engineering governance | Milestone 11 | Completed | PLAT-PB-001 |
| PLAT-PB-004 | High | Infrastructure | Infrastructure Registry | Infrastructure Registry v1.0 | Milestone 12 | Planned | ADR-006; Infrastructure Registry v1.0 Specification |
| PLAT-PB-009 | High | Infrastructure | Operations readiness | Infrastructure Operations Readiness | Milestone 13 | Planned | Infrastructure Registry v1.0 baseline |
| PLAT-PB-011 | High | Infrastructure | Platform node onboarding | Beelink Day 0 / Day 1 Bring-up Plan | Milestone 13 | Planned | PLAT-PB-009; delivered Beelink Mini S |
| PLAT-PB-012 | High | Infrastructure | Operations and observability | Platform Operations and Observability | Milestone 13 | Planned | Active Beelink-hosted Pi-hole; active PLAT-13.6.2 Metrics Foundation; ADR-007 |
| EO-PB-013 | High | Engineering Organization | Governance evolution | Engineering Organization Governance Evolution | Milestone 13 | Planned | EO-13.0 foundation artifacts |
| EO-PB-014 | High | Engineering Organization | Governed live execution | Execution Agent Specification and repository-side Execution Capability | Milestone 14 | Planned | EO-14.1A repository implementation published; live role activation remains planned; AI Role Catalog; privileged infrastructure integration standard |
| EO-PB-015 | High | Engineering Organization | Operations intelligence | Operations Analyst Specification | Milestone 14 | Planned | PLAT observability evidence |
| EO-PB-016 | Medium | Engineering Organization | Engineering metrics | Engineering Metrics v2 | Milestone 14 | Planned | EAP reports; maturity model |
| EO-PB-017 | High | Engineering Organization | Governed automation | Governed Automation Framework orchestration over the published Execution Capability | Milestone 14 | Planned | EO-14.4A repository implementation published; automation activation remains separate |
| EO-PB-018 | Medium | Engineering Organization | Portfolio coordination | Engineering Portfolio Kanban | Milestone 14 | Planned | Milestone 14 portfolio plan |
| EO-PB-019 | Medium | Engineering Organization | Capability maturity | Capability Maturity Assessment | Milestone 14 | Planned | EO-13.1 maturity model |
| EO-PB-020 | Medium | Engineering Organization | Approval model | AI Collaboration and Approval Model | Milestone 14 | Superseded | Superseded by EO-14.8 AI Collaboration Governance |
| EO-PB-021 | High | Engineering Organization | AI collaboration governance | AI Collaboration Governance | Milestone 14 | Completed | EO-14.8A, EO-14.8B, EO-14.8C.1, EO-14.8C.2, EO-14.8D, and EO-14.8E complete; Architecture Gatekeeper approved; baseline published |
| PLAT-PB-017 | High | Infrastructure | Platform Operations | Platform Operations Domain Architecture | Milestone 14 | Completed | Published PLAT-14.0A baseline `c8f9bc3`; ADR-009 through ADR-011 |
| PLAT-PB-013 | High | Infrastructure | Platform Operations | Container Operational Health (Container Metrics Modernization successor) | Milestone 14 | Published Fixture Capability and Provider Foundation | Option B fixture-only health implementation, exact five-record `not_applicable` migration, provider architecture/security design, and repository-only adapter foundation published; no eligible target, live-provider selection, access, consumer, activation, or live authorization |
| PLAT-PB-014 | High | Infrastructure | Operational excellence | Backup, restore, recovery validation, alerting, and runbooks | Milestone 14 | Planned | PLAT-13.6.2; PLAT-13.6.4 requirements |
| PLAT-PB-015 | Medium | Infrastructure | Platform health | Platform Health Dashboard | Milestone 14 | Planned | PLAT-PB-013; repository-generated reports |
| PLAT-PB-016 | High | Shared Services | Authentication boundary | Platform Authentication Boundary for FFFA web access | Milestone 14 | Deferred | FFFA-14.2B; local reverse proxy; human production approval; future FFFA web implementation approval |
| FFFA-PB-001 | High | Customer-Facing Applications | Categorization intelligence | Transaction Categorization Intelligence | Milestone 14 | Paused | Chris customer acceptance; Financial Domain Foundation freeze; existing FFFA categorization behavior and FFFA repository specification |
| FFFA-PB-002 | High | Customer-Facing Applications | Financial reporting | Multi-Channel Financial Presentation | Milestone 14 | Paused | Chris customer acceptance; Financial Domain Foundation freeze; FFFA ADR-087; reporting contract; persona governance |
| PLAT-PB-010 | Medium | Infrastructure | Runtime planning | Define first Platform runtime architecture options | Future | Deferred | PLAT-PB-009 |
| PLAT-PB-005 | Medium | Home Automation | Capability readiness | Assess first home automation vertical slice | Milestone 12 | Candidate | Requirements discovery |
| PLAT-PB-006 | Medium | Energy Management | Capability readiness | Assess first energy management vertical slice | Future | Candidate | Requirements discovery |
| PLAT-PB-007 | Medium | AI Services | Governance | Define AI service safety and privacy requirements | Future | Candidate | Privacy and architecture review |
| PLAT-PB-008 | Medium | Family Intelligence | Evidence model | Define household intelligence evidence model | Future | Candidate | Data governance |

---

## Notes

Product Backlog priority does not approve implementation. Each implementation item requires requirements, architecture, specifications, and validation criteria.

Infrastructure Registry v1.0 is the first planned Platform feature milestone and remains non-finance scope.

Infrastructure Operations Readiness prepares future managed infrastructure work without implementing Beelink bring-up, deployment automation, runtime monitoring, dashboards, or finance functionality.

Beelink Day 0 / Day 1 Bring-up planning records delivered hardware facts and onboarding instructions without migrating Pi-hole, changing router DNS, installing planned services, or marking the Beelink active.

Platform Operations and Observability has completed the governed PLAT-13.6.2 Metrics Foundation deployment for Prometheus, Node Exporter, and cAdvisor. PLAT-13.6.3 has deployed Grafana for validation, PLAT-13.6.3A records that Docker-container metrics are blocked by Docker 29/containerd cAdvisor compatibility, and PLAT-13.6.3B prepares the restricted Docker API proxy plus OTel Docker Stats replacement for Architecture Gatekeeper review. Backup automation, restore validation, alerting, incident response execution, and controlled update practices remain planned.

EO-13.1 is a repository-only governance package. It does not close PLAT-13.6 or Milestone 13, and it does not authorize live infrastructure changes.

Milestone 14 backlog candidates are planned, not approved for implementation. The approved execution strategy is Option C - Governed Vertical Slice, with Container Operational Health as the first governed vertical slice.

The first vertical slice coordinates the published EO-14.1A Execution Capability with EO-14.4A orchestration, PLAT-14.0A Platform Operations Domain Architecture, the later architecture-aligned PLAT-14.1A Container Metrics Repository Implementation Package, EO-14.2A Operations Analyst Operationalization, PLAT-14.3A Platform Health Dashboard Completion, EO-14.3A Engineering Metrics v2 Refinement, and later PLAT-14.2 Operational Excellence through separate approval gates. EO-14.4A consumes EO-14.1A execution validation, evidence, and completion packages rather than redefining them.

PLAT-14.0A, the PLAT-14.1A specification, the Foundation, and the Architecture Gatekeeper-accepted PLAT-14.1A Option B fixture-only repository vertical slice are published. Exactly five records are migrated as `not_applicable`; authoritative eligible-subject evaluation, remaining migrations, providers, dashboards/APIs, activation, and live work remain separately blocked.

The provider architecture, Contract v1.0, security design, repository-only provider foundation, and formal proxy security review are accepted and published under PLAT-PB-013. The constrained proxy is approved only as the future implementation target. Only a repository-only proxy foundation may be considered next; privileged implementation, deployment, credentials, named-target observation, consumers, activation, and live work remain blocked. No standalone identifier is assigned because repository evidence does not establish numbering authority.

EO-14.8 AI Collaboration Governance, the Architecture Gatekeeper-approved Alpha EO-14.1A and EO-14.4A repository implementations, the bounded Bravo Foundation implementation, and the Bravo PLAT-14.1A fixture-only repository implementation are published. Charlie remains unstarted. No automation, role activation, provider, dashboard/API, or live work is authorized.

FFFA detail is owned by the FamilyFinanceAssistant repository; this repository records portfolio traceability to FFFA-14.1 and FFFA-14.2 using Existing FFFA backlog and roadmap governance. FFFA implementation is paused while Chris completes customer acceptance, and the Financial Domain Foundation remains frozen for the rest of Milestone 14 except for separately approved defect fixes.

---

## Related Documents

- [Capability Model](Capability_Model.md)
- [Product Roadmap](Product_Roadmap.md)
- [Product Governance](Product_Governance.md)
- [Milestone 12 Plan](../milestones/Milestone_12/Milestone_12_Infrastructure_Registry_v1.0.md)
- [Engineering Organization Manifesto](../engineering-organization/Engineering_Organization_Manifesto.md)
- [Milestone 14 Portfolio Plan](../milestones/Milestone_14/Milestone_14_Portfolio_Plan.md)
- [Engineering Portfolio Kanban](../portfolio/Engineering_Portfolio_Kanban.md)
- [AI Collaboration Governance Specification](../engineering-organization/ai-collaboration/AI_Collaboration_Governance_Specification.md)
- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 3.12 | Recorded formal proxy security review and the repository-only constrained-proxy foundation as the next possible gate without authorizing privileged or live work. |
| 3.11 | Recorded publication of the repository-only provider foundation under PLAT-PB-013 without inventing a work-item identifier or authorizing a live provider. |
| 3.10 | Recorded publication of the accepted Production Provider Adapter Architecture and security prerequisite under PLAT-PB-013 without inventing a work-item identifier or authorizing implementation. |
| 3.9 | Recorded exact five-record Registry migration and current-plan lifecycle correction while retaining eligible-subject, provider, dashboard/API, activation, and live gates. |
| 3.8 | Recorded Architecture Gatekeeper acceptance and publication of the PLAT-14.1A Option B fixture-only repository vertical slice while retaining Registry migration, provider, dashboard/API, activation, and live gates. |
| 3.7 | Recorded the complete unpublished PLAT-14.1A Option B repository vertical slice while retaining Registry migration, publication, provider, dashboard, activation, and live gates. |
| 3.6 | Recorded Architecture Gatekeeper acceptance and publication of the Registry identity prerequisite without record migration, standalone identifier, or PLAT-14.1A authorization. |
| 3.5 | Recorded complete unpublished Registry identity prerequisite implementation without record migration, standalone identifier, or PLAT-14.1A authorization. |
| 3.4 | Recorded PLAT-14.1A and unimplemented Registry Container Identity Foundation publication without adding a standalone work-item identifier. |
| 3.3 | Marked PLAT-14.0A published and reframed PLAT-PB-013 as implementation-blocked Container Operational Health specification alignment. |
| 3.2 | Added PLAT-14.0A Platform Operations domain architecture and blocked PLAT-14.1A pending publication and alignment. |
| 3.1 | Recorded publication of the Architecture Gatekeeper-approved EO-14.4A repository implementation while retaining planned activation and later gates. |
| 3.0 | Recorded EO-14.4A Option B repository implementation complete pending Architecture Gatekeeper review while retaining planned activation and later gates. |
| 2.9 | Recorded EO-14.4A orchestration alignment with the published EO-14.1A Execution Capability while retaining planned status and separate implementation and activation gates. |
| 2.8 | Recorded publication of the Architecture Gatekeeper-approved EO-14.1A repository implementation while retaining the planned live-role state and later gates. |
| 2.7 | Recorded EO-14.1A repository implementation pending Architecture Gatekeeper review while retaining the planned live-role state and unchanged EO-14.4A, Bravo, Charlie, and live-work gates. |
| 2.6 | Recorded EO-14.8 completion and baseline publication, with Alpha EO-14.1A and EO-14.4A next and all three workstreams still unstarted. |
| 2.5 | Corrected active-milestone metadata to Milestone 14 and recorded EO-14.8E implementation and parent final-review state. |
| 2.4 | Recorded EO-14.8D implementation-review status, EO-14.8E approval dependency, and unchanged workstream boundaries. |
| 2.3 | Added EO-14.8 AI Collaboration Governance backlog item, superseded earlier AI Collaboration and Approval Model candidate, and recorded Alpha, Bravo, Charlie pause treatment. |
| 2.2 | Recorded approved Milestone 14 Option C governed vertical slice, Container Operational Health sequencing, FFFA implementation pause, Financial Domain Foundation freeze, and deferred authentication-boundary dependency. |
| 2.1 | Added Platform-owned authentication boundary backlog item for FFFA-14.2B. |
| 2.0 | Aligned Milestone 14 backlog with approved EO-14, PLAT-14, and FFFA-14 portfolio work packages. |
| 1.9 | Added EO-13.1 and planned Milestone 14 EO, PLAT, and FFFA backlog candidates. |
| 1.8 | Added PLAT-13.6.3B Docker container metrics replacement preparation. |
| 1.7 | Added PLAT-13.6.3A Docker 29/containerd container metrics compatibility correction. |
| 1.6 | Recorded PLAT-13.6.3 Operations Dashboard repository preparation without live deployment. |
| 1.5 | Recorded completed PLAT-13.6.2 Metrics Foundation while preserving later operations work as planned. |
| 1.4 | Added PLAT-PB-012 Platform Operations and Observability backlog item for PLAT-13.6. |
| 1.3 | Added PLAT-PB-011 Beelink Day 0 / Day 1 Bring-up Plan backlog item for PLAT-13.3. |
| 1.2 | Added PLAT-13.1 Infrastructure Operations Readiness backlog item. |
| 1.1 | Added Infrastructure Registry v1.0 as planned Milestone 12 Platform feature and deferred runtime planning. |
| 1.0 | Initial Platform product backlog. |
