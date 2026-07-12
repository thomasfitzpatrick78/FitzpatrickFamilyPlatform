# Product Backlog

**Document Version:** 1.2

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document defines the initial repository-managed Product Backlog for the Fitzpatrick Family Platform.

---

## Status Values

- Candidate
- Planned
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

Platform Operations and Observability has completed the governed PLAT-13.6.2 Metrics Foundation deployment for Prometheus, Node Exporter, and cAdvisor. PLAT-13.6.3 has prepared the repository-managed Grafana Operations Dashboard package for Architecture Gatekeeper review without live deployment. Backup automation, restore validation, alerting, incident response execution, and controlled update practices remain planned.

---

## Related Documents

- [Capability Model](Capability_Model.md)
- [Product Roadmap](Product_Roadmap.md)
- [Product Governance](Product_Governance.md)
- [Milestone 12 Plan](../milestones/Milestone_12/Milestone_12_Infrastructure_Registry_v1.0.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.6 | Recorded PLAT-13.6.3 Operations Dashboard repository preparation without live deployment. |
| 1.5 | Recorded completed PLAT-13.6.2 Metrics Foundation while preserving later operations work as planned. |
| 1.4 | Added PLAT-PB-012 Platform Operations and Observability backlog item for PLAT-13.6. |
| 1.3 | Added PLAT-PB-011 Beelink Day 0 / Day 1 Bring-up Plan backlog item for PLAT-13.3. |
| 1.2 | Added PLAT-13.1 Infrastructure Operations Readiness backlog item. |
| 1.1 | Added Infrastructure Registry v1.0 as planned Milestone 12 Platform feature and deferred runtime planning. |
| 1.0 | Initial Platform product backlog. |
