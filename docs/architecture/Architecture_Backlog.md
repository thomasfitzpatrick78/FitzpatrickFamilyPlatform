# Architecture Backlog

**Document Version:** 1.16

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document tracks future architecture topics for the Fitzpatrick Family Platform.

---

## Backlog

| ID | Priority | Topic | Status | Notes |
|----|:--------:|-------|--------|-------|
| AB-001 | High | Registry Driven Infrastructure Foundation | Active | Selected by ADR-006 for Milestone 12. |
| AB-007 | High | Infrastructure operations readiness | Active | PLAT-13.1 documents readiness options and checklists without runtime implementation. |
| AB-008 | High | Platform runtime architecture options | Candidate | Deferred until Infrastructure operations readiness establishes options and gates. |
| AB-009 | High | Platform Digital Twin lifecycle state model | Candidate | Future enhancement proposal for explicit states: Planned -> Delivered -> Powered -> BIOS Verified -> OS Installed -> Network Connected -> SSH Verified -> Docker Ready -> Platform Active. Do not implement lifecycle changes in PLAT-13.3. |
| AB-010 | High | Governed operations and observability | Active | ADR-007 selects governed Prometheus, Node Exporter, cAdvisor, and Grafana target architecture for PLAT-13.6 planning. |
| AB-011 | High | Platform Operations bounded context and canonical evidence architecture | Active | Foundation schema 1.1, the PLAT-14.1A fixture-only slice, migration model v2, and Production Provider Adapter Architecture and Privileged-Access Security Design are published. The constrained proxy is the approved primary direction and OTel/Prometheus is optional supplemental direction. Five `not_applicable` subjects are completed, 16 remain review-required, and provider implementation, privileged access, named-target observation, consumers, activation, and live gates remain blocked. |
| AB-012 | Medium | Secure External and Privileged Provider Integration Standard | Candidate | Evaluate consolidation of provider-independent adapter contracts, fixture-first delivery, privileged-boundary threat modeling, secrets/provenance controls, fail-closed parsing, named-target authorization, and separate recurring-activation gates without duplicating existing privileged-integration, execution, automation, AI-collaboration, or repository governance. No permanent standard is authorized by this candidate. |
| AB-002 | High | Home Automation safety model | Candidate | Needed before device or automation workflows. |
| AB-003 | Medium | AI Services privacy and safety model | Candidate | Required before AI service implementation. |
| AB-004 | Medium | Energy data model | Candidate | Required before energy tracking implementation. |
| AB-005 | Medium | Shared service boundaries | Candidate | Needed before reusable service implementation. |
| AB-006 | Low | Cross-repository engineering extraction criteria | Deferred | Requires evidence from multiple repositories. |

---

## Related Documents

- [Architecture Decision Log](Architecture_Decision_Log.md)
- [Current Architecture State](Current_Architecture_State.md)
- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)
- [Platform Operations Domain Architecture](Platform_Operations_Domain_Architecture.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.16 | Recorded publication of the accepted Production Provider Adapter Architecture and Privileged-Access Security Design and added a bounded future secure-provider standard candidate while retaining all implementation and live gates. |
| 1.15 | Recorded exact five-record migration and corrected historical/current plan lifecycle while retaining review-required migration, provider, activation, and live gates. |
| 1.14 | Recorded deterministic exact-plan approval binding as unpublished and unexecuted while preserving migration, provider, activation, and live gates. |
| 1.13 | Recorded exact-plan approval-in-principle and creation of unpublished, unbound approval evidence while preserving migration, provider, activation, and live gates. |
| 1.12 | Recorded the complete unpublished Registry migration idempotency correction and regenerated pending plan without opening approval, migration, provider, activation, or live gates. |
| 1.11 | Recorded Architecture Gatekeeper acceptance and publication of the PLAT-14.1A fixture-only repository vertical slice while retaining Registry migration, provider, dashboard/API, activation, and live gates. |
| 1.10 | Recorded the complete unpublished PLAT-14.1A repository vertical slice with Registry migration, provider, dashboard, activation, and live gates unchanged. |
| 1.9 | Recorded Architecture Gatekeeper acceptance and publication of the Registry identity implementation with record migration and PLAT-14.1A blocked. |
| 1.8 | Recorded complete unpublished Registry identity schema/validation/migration implementation with record migration and PLAT-14.1A blocked. |
| 1.7 | Recorded PLAT-14.1A and Registry Container Identity Foundation publication while retaining schema, migration, and implementation gates. |
| 1.6 | Recorded PLAT-14.0A publication and PLAT-14.1A specification-alignment decisions while retaining implementation blocking. |
| 1.5 | Added PLAT-14.0A Platform Operations domain architecture and PLAT-14.1A blocking dependency. |
| 1.4 | Added governed operations and observability architecture topic for PLAT-13.6. |
| 1.3 | Added future Platform Digital Twin lifecycle state model proposal from PLAT-13.3 Architecture Review Board decision. |
| 1.2 | Added PLAT-13.1 Infrastructure operations readiness architecture topic. |
| 1.1 | Marked Registry Driven Infrastructure Foundation active for Milestone 12 and deferred runtime architecture until registry foundation exists. |
| 1.0 | Initial Platform architecture backlog. |
