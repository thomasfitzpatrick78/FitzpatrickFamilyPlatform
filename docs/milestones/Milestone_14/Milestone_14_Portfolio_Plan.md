# Milestone 14 - Operationalizing the AI Engineering Organization

**Document Version:** 2.7

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** Milestone 14

---

## Purpose

This document defines the governed Milestone 14 portfolio plan for the Fitzpatrick Family engineering organization.

Milestone 14 remains governed repository planning and repository implementation until separate approval gates are complete. This plan does not authorize live infrastructure changes, production credentials, deployment, customer application implementation, release tagging, commits, or pushes.

---

## Theme

Operationalizing the AI Engineering Organization.

Milestone 14 intentionally strengthens:

- EO-14.x Engineering Organization.
- PLAT-14.x Shared Platform.
- FFFA-14.x Fitzpatrick Family Financial Assistant.

The Engineering Investment Rule applies at the milestone level. Individual workstreams may be repository-only when the milestone-level evidence still demonstrates Engineering Organization, Shared Platform, and customer-facing application advancement.

---

## Approved Portfolio Architecture

Selected execution strategy: Option C - Governed Vertical Slice.

First governed vertical slice: Container Operational Health.

```text
Container Operational Health
├── AI Collaboration Governance controls
├── Execution Agent operational boundaries
├── Governed Automation Framework controls
├── Platform Operations domain architecture and contracts
├── Container Metrics provider implementation after architecture alignment
├── Operations Analyst interpretation
├── Platform Health Dashboard integration
├── Engineering Metrics v2 evidence
├── Architecture Gatekeeper review
└── Separate future human approval for live infrastructure execution
```

The Fitzpatrick Family Platform owns Engineering Organization operating model, Shared Platform architecture, portfolio coordination, and cross-product engineering governance.

The Fitzpatrick Family Financial Assistant remains the flagship customer-facing application. FFFA customer implementation is paused while Chris performs customer acceptance. The Financial Domain Foundation remains frozen for the rest of Milestone 14 except for separately approved defect fixes.

This repository preserves FFFA as the Milestone 14 customer-value pillar through published FFFA specifications, ADR-087, personas, reporting contracts, and customer acceptance evidence. It does not authorize new FFFA implementation.

EO-14.8 AI Collaboration Governance, the Architecture Gatekeeper-approved EO-14.1A and EO-14.4A repository implementations, and the Bravo Registry Container Identity Foundation repository implementation are published; PLAT-14.1A and Charlie remain unstarted. No automation, Execution Agent activation, or live work is authorized. Future Platform Health dashboard runtime deployment remains PLAT work.

PLAT-14.0A architecture is published at `c8f9bc3446cb1d5c23bf32232203109a7ff067f8`, the PLAT-14.1A Container Operational Health specification is published at `89deeed2480679c9717cb151c3a14fe9414d8b97`, and the Registry Container Identity Foundation architecture/specification and repository implementation are published. Foundation schema `1.1`, strict validation, evidence-gated migration tooling, exact-plan governed approval binding, CLI compatibility, Digital Twin compatibility, and tests are complete. All 39 records remain unchanged; record migration, PLAT implementation, providers, dashboards, and activation remain separately blocked.

---

## Work Package Plan

| Work Package | Workstream | Repository | Purpose | Primary Evidence |
|--------------|------------|------------|---------|------------------|
| EO-14.1 | Execution Agent | FitzpatrickFamilyPlatform | Define governed live-runbook execution role. | Execution Agent specification; role catalog update. |
| EO-14.1A | Execution Agent Operationalization | FitzpatrickFamilyPlatform | Implement execution contracts, activation boundaries, handoffs, and repository-only controls for the first vertical slice. | Repository-side Execution Capability models, validation, JSON and Markdown serialization, bounded CLI, tests, and completion evidence. |
| EO-14.2 | Operations Analyst | FitzpatrickFamilyPlatform | Define governed operational health analysis role. | Operations Analyst specification; role catalog update. |
| EO-14.2A | Operations Analyst Operationalization | FitzpatrickFamilyPlatform | Define Container Operational Health interpretation procedures and evidence states. | Operations Analyst procedures; evidence interpretation model. |
| EO-14.3 | Engineering Metrics v2 | FitzpatrickFamilyPlatform | Define practical evidence-based engineering metrics. | Metrics v2 specification and acceptance criteria. |
| EO-14.3A | Engineering Metrics v2 Refinement | FitzpatrickFamilyPlatform | Map vertical-slice evidence into Engineering Metrics v2 without false precision. | Metric mapping and validation evidence. |
| EO-14.4 | Governed Automation Framework | FitzpatrickFamilyPlatform | Define automation proposal, approval, operation, review, and retirement. | Automation framework specification. |
| EO-14.4A | Governed Automation Framework Operationalization | FitzpatrickFamilyPlatform | Implement repository-side orchestration flow and lifecycle controls while consuming EO-14.1A execution semantics. | Immutable models, strict IO, deterministic validation and transition decisions, EO-14.1A integration, handoff rendering, bounded CLI, fixtures, and tests. |
| EO-14.8 | AI Collaboration Governance | FitzpatrickFamilyPlatform | Govern AI participant initialization, continuity, completion, stewardship, readiness validation, and readiness observability. | Complete; Architecture Gatekeeper approved; Engineering Organization baseline published. |
| EO-14.8A | AI Collaboration Governance Capability Charter | FitzpatrickFamilyPlatform | Approved architectural constitution for AI Collaboration Governance. | Complete. |
| EO-14.8B | AI Collaboration Governance Repository Specification Package | FitzpatrickFamilyPlatform | Specify charter, lifecycle, standards, continuity brief, Steward role, and future readiness validator. | Complete. |
| EO-14.8C | AI Collaboration Governance Repository Implementation | FitzpatrickFamilyPlatform | Implement approved reusable framework and operational artifacts. | Complete through EO-14.8C.1 and EO-14.8C.2. |
| EO-14.8C.1 | AI Collaboration Governance Repository Framework | FitzpatrickFamilyPlatform | Provide the reusable repository framework and blank templates. | Complete. |
| EO-14.8C.2 | AI Collaboration Governance Milestone 14 Operationalization | FitzpatrickFamilyPlatform | Instantiate governed continuity and limited Steward review for active Milestone 14 workstreams. | Complete; Alpha, Bravo, and Charlie ready but not started. |
| EO-14.8D | AI Session Readiness Validator | FitzpatrickFamilyPlatform | Validate repository evidence for governed AI participant onboarding. | Complete. |
| EO-14.8E | Engineering Metrics Integration | FitzpatrickFamilyPlatform | Consume governed readiness evidence in Engineering Metrics and repository-side Platform Health visibility. | Complete. |
| PLAT-14.0A | Platform Operations Domain Architecture | FitzpatrickFamilyPlatform | Establish Platform Operations as the bounded context for Declared State, Operational Evidence, Reconciliation, Operational Health, and Operational Intelligence. | Published architecture and contracts at `c8f9bc3`; Implemented: No. |
| PLAT-14.1 | Container Metrics Modernization | FitzpatrickFamilyPlatform | Carry forward Milestone 13 container metrics architecture into approval-ready requirements. | Container metrics modernization specification. |
| Registry Container Identity Foundation | PLAT-14.1A prerequisite | FitzpatrickFamilyPlatform | Implement the smallest authoritative service-record identity extension, evidence-gated migration, validation, and exact-plan mutation-approval contract. | Architecture Gatekeeper accepted and published; all 39 records unchanged; standalone identifier intentionally deferred; approval artifact and record migration remain separate gates. |
| PLAT-14.1A | Container Operational Health | FitzpatrickFamilyPlatform | Consume validated Registry identity before future evidence, reconciliation, health, output, fixture, and EO integration implementation. | Specification published at `89deeed`; Option B repository vertical slice remains unauthorized and blocked. |
| PLAT-14.2 | Operational Excellence | FitzpatrickFamilyPlatform | Define backup, restore, recovery, alerting, runbook, and evidence scope. | Operational excellence specification. |
| PLAT-14.3 | Platform Health Dashboard | FitzpatrickFamilyPlatform | Define executive operational health view and source-of-truth boundaries. | Platform health dashboard specification. |
| PLAT-14.3A | Platform Health Dashboard Completion | FitzpatrickFamilyPlatform | Complete dashboard source contracts after PLAT-14.1 telemetry contract verification. | Dashboard contract, source mapping, and validation evidence. |
| PLAT-14.4 | Platform Authentication Boundary | FitzpatrickFamilyPlatform | Preserve future local reverse proxy, identity-header trust, LAN-only HTTPS, and authentication operations scope for FFFA-14.2B. | Authentication boundary specification and implementation-package placeholder. |
| FFFA-14.1 | Transaction Categorization Intelligence | FamilyFinanceAssistant | Published customer-facing specification; implementation paused pending customer acceptance. | FFFA specification and acceptance plan. |
| FFFA-14.2 | Family Financial Reporting and Presentation | FamilyFinanceAssistant | Published presentation-independent reporting and dual-channel experience specification; implementation paused pending customer acceptance. | ADR-087, reporting contract, Excel spec, web spec, customer acceptance spec. |

---

## Approved Sequence

| Sequence | Work Package | Gate Meaning |
|----------|--------------|--------------|
| 0 | EO-14.8 AI Collaboration Governance | Complete; Architecture Gatekeeper approved and capability baseline published before Alpha, Bravo, or Charlie repository implementation begins. |
| 1 | EO-14.1A Execution Agent Operationalization | Repository implementation published; activation remains separate and unauthorized. |
| 2 | EO-14.4A Governed Automation Framework Operationalization | Repository implementation is published; it consumes EO-14.1A execution validation, evidence, and completion packages and does not authorize automation use. |
| 3 | PLAT-14.0A Platform Operations Domain Architecture | Complete; bounded context, contracts, ADRs, and provider/consumer boundaries published at `c8f9bc3`. |
| 4 | Registry Container Identity Foundation then PLAT-14.1A Container Operational Health | Foundation repository implementation and required exact-plan approval-artifact correction are Architecture Gatekeeper accepted and published with no record migration. Any record migration and PLAT-14.1A Option B repository implementation remain separate decisions. Provider, security, observation, dashboard, and activation remain later gates. |
| 5 | EO-14.2A Operations Analyst Operationalization | Analysis procedures consume governed health assessments and distinguish evidence, health, confidence, and interpretation without recalculation. |
| 6 | PLAT-14.3A Platform Health Dashboard Completion | Dashboard completion follows the verified PLAT-14.0A consumer contract and PLAT-14.1A implementation evidence. |
| 7 | EO-14.3A Engineering Metrics v2 Refinement | Metrics are refined from vertical-slice evidence without unsupported precision. |
| 8 | PLAT-14.2 Operational Excellence | Backup, restore, alerting, and broader operational excellence proceed only through separate architecture and human approval gates. |

This sequence is a governed integration model. It does not authorize live execution.

EO-14.8, the Architecture Gatekeeper-approved Alpha EO-14.1A and EO-14.4A repository implementations, and the bounded Bravo Foundation implementation are published; PLAT-14.1A and Charlie remain unstarted.

---

## Parallel Repository Workstreams

### Alpha - Engineering Organization Controls

**Scope:** EO-14.1A and EO-14.4A.

**Responsibilities:**

- Execution Capability, activation-boundary, and execution-contract design.
- Automation orchestration flow, lifecycle, catalog, approval, failure, rollback, and retirement controls that consume EO-14.1A execution artifacts.
- Repository-only implementation.

**Boundary:** Alpha defines controls before any future live deployment request. It does not activate the Execution Agent for production or authorize automation against live infrastructure.

### Bravo - Platform Observability

**Scope:** Published PLAT-14.0A architecture, PLAT-14.1A specification, and Registry Container Identity Foundation architecture/specification and repository implementation; PLAT-14.1A follows only through separate authorization.

**Responsibilities:**

- Published PLAT-14.0A Platform Operations bounded context and canonical evidence, reconciliation, health, confidence, provider, and consumer contracts.
- Registry Container Identity Foundation option assessment, selected declared-state contract, migration design, validation requirements, and acceptance matrix.
- Additive schema `1.1`, strict conditional validation, deterministic evidence-gated planning/execution/rollback, Registry CLI compatibility, Digital Twin compatibility, and engineering tests without record migration.
- Published PLAT-14.1A Registry identity, versioned policy, first-slice evidence, health, output, fixture, EO integration, and future-gate specification baseline.
- Preserve Infrastructure Registry declared-state authority and Platform-owned subject identity.
- Reframe approved Docker API proxy, OpenTelemetry, Prometheus, Docker daemon, cAdvisor, and Grafana work as future provider or presentation scope.
- Preserve future static validation, runbooks, rollback instructions, and evidence templates without starting PLAT-14.1A.

**Boundary:** Foundation repository implementation is published, but all 39 records remain unchanged. Any record migration and the PLAT-14.1A Option B repository vertical slice remain separately unauthorized. Provider, security, live-observation, dashboard, and activation gates remain separate. Bravo must not deploy or connect to live infrastructure.

### Charlie - Operations Intelligence

**Scope:** EO-14.2A and EO-14.3A.

**Responsibilities:**

- Operations Analyst procedures.
- Evidence interpretation.
- Container-health analysis.
- Engineering metric mappings.
- Unknown, stale, unavailable, and failed signal treatment.

**Boundary:** Charlie may work on analysis structure in parallel but must not invent telemetry names, labels, thresholds, or availability. Final mappings depend on Bravo's verified repository telemetry contract.

---

## Integration Gates

| Gate | Requirement |
|------|-------------|
| AI collaboration controls before Alpha, Bravo, and Charlie | Satisfied by the completed, Architecture Gatekeeper-approved EO-14.8 capability baseline; each later workstream still requires its separately authorized work package. |
| Alpha controls before live request | EO-14.1A defines execution semantics; EO-14.4A defines orchestration flow and lifecycle progression that consume those semantics. Both controls must precede any future live deployment request. |
| Registry identity before PLAT-14.1A implementation | Foundation schema/validation/migration tooling is published, but no record is migrated or eligible. An approved evidence-gated record migration and separate PLAT authorization are required before an active subject can be assessed. |
| Bravo evidence contracts before final Charlie mappings | Bravo must implement and validate the published Platform Operations contracts before final Charlie mappings. |
| Charlie evidence-state discipline | Charlie must distinguish provider observation, normalized evidence, reconciliation, health, confidence, and interpretation and must not recalculate authoritative health. |
| Dashboard follows governed outputs | PLAT-14.3A follows the published Platform Operations consumer contract and later verified PLAT-14.1A evidence; no-data must not become Healthy. |
| Operational Excellence live work remains separate | PLAT-14.2 live backup, restore, and alerting work requires separate architecture and human approval. |
| Architecture review before promotion | Architecture Gatekeeper review is required before lifecycle promotion. |

---

## Dependencies

| Dependency | Applies To | Required Before |
|------------|------------|-----------------|
| Milestone 13 closeout baseline and tag `milestone-13`. | All workstreams. | Milestone 14 implementation authorization. |
| PLAT-14.0A Platform Operations Domain Architecture. | PLAT-14.1A, EO-14.2A, EO-14.3A, PLAT-14.3A. | Canonical evidence, reconciliation, health, confidence, provider, and consumer contract implementation. |
| PLAT-13.6.3B container metrics architecture. | PLAT-14.1A, PLAT-14.3A. | Container telemetry repository package and dashboard source mapping. |
| Privileged Infrastructure Integration Standard. | EO-14.1A, EO-14.4A, PLAT-14.1A, PLAT-14.2. | Any future live infrastructure execution. |
| Alpha controls. | PLAT-14.1A and any future live deployment request. | EO-14.1A execution contracts and EO-14.4A orchestration controls. |
| AI Collaboration Governance. | Alpha, Bravo, Charlie, and future parallel AI workstreams. | Governed initialization, continuity, completion, and handoff readiness. |
| Bravo repository telemetry contract. | EO-14.2A, EO-14.3A, PLAT-14.3A. | Final metric mappings and dashboard completion. |
| FFFA customer acceptance. | FFFA implementation continuation. | Any new FFFA implementation scope. |
| Platform authentication boundary specification. | Future FFFA-14.2B web implementation. | Web implementation with real household financial data. |

---

## Evidence Expectations

Milestone 14 Option C evidence should include:

- Alpha EO-14.1A execution-contract artifacts and EO-14.4A orchestration-control artifacts that consume them without redefining execution semantics.
- AI Collaboration Governance specification package, EO-14.8D readiness reports and tests, and EO-14.8E Engineering Metrics and repository-side Platform Health evidence.
- PLAT-14.0A bounded-context architecture, versioned evidence and health contracts, deterministic decision tables, ADRs, and provider/consumer boundaries.
- Future PLAT-14.1A canonical contract implementation, provider normalization fixtures, static validation, runbooks, and evidence templates after separate authorization; Foundation rollback tooling is published.
- Charlie interpretation model and metric mapping that consumes governed health without inventing telemetry or recalculating authoritative outcomes.
- PLAT-14.3 dashboard source contracts traceable to governed assessments and verified evidence.
- Engineering Metrics v2 refinement based on repository evidence.
- Clear stop conditions and explicit human approval boundaries for any future live work.

---

## Acceptance Criteria

Milestone 14 Option C planning is ready for Architecture Gatekeeper review when:

- Option C - Governed Vertical Slice is recorded as the approved execution strategy.
- Container Operational Health is defined as the first governed vertical slice.
- PLAT-14.0A separates declared state, provider observations, normalized evidence, reconciliation, operational health, and advisory intelligence and is published at `c8f9bc3` with Implemented: No.
- Foundation repository implementation is published with all 39 records unchanged; PLAT-14.1A implementation remains blocked pending separate record migration and PLAT authorization decisions.
- Alpha, Bravo, and Charlie workstreams are defined with boundaries, dependencies, non-goals, and evidence expectations.
- EO-14.8A through EO-14.8E, the EO-14.8 parent capability, EO-14.1A and EO-14.4A repository implementations, and the bounded Bravo Foundation are recorded published while activation and Registry migration remain absent; PLAT-14.1A and Charlie remain unstarted.
- FFFA implementation pause and Financial Domain Foundation freeze are explicit.
- Repository implementation and future controlled live deployment are separated.
- PLAT-14.4 authentication-boundary work remains deferred unless a future dependency explicitly activates it.
- Integration gates preserve Architecture Gatekeeper review and human production approval.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Vertical-slice work is mistaken for live deployment approval. | State repeatedly that repository implementation does not authorize live infrastructure changes. |
| Alpha, Bravo, or Charlie resumes without governed AI collaboration controls. | Pause those workstreams until EO-14.8 controls are approved and implemented sufficiently for governed initialization and continuity. |
| Charlie invents telemetry before Bravo validates the contract. | Require Charlie to use unknown, stale, unavailable, and failed states until Bravo evidence exists. |
| Execution Agent boundaries blur into architecture authority. | Keep Execution Agent activation and execution contracts under Alpha and require Architecture Gatekeeper review. |
| Automation duplicates or bypasses governed execution semantics. | Require EO-14.4A orchestration to consume EO-14.1A assignments, validation, evidence, and completion packages, with human approval preserved before automation use. |
| Dashboard claims overstate container health. | PLAT-14.3A follows the verified PLAT-14.1 telemetry contract. |
| FFFA implementation resumes before customer acceptance. | Record implementation pause and Financial Domain Foundation freeze in milestone planning. |

---

## Non-Goals

- Live Docker API proxy deployment.
- Live OTel Docker Stats Collector deployment.
- Docker daemon changes on a host.
- Grafana production promotion or reboot validation.
- Backup execution.
- Restore execution.
- Alert activation.
- SSH connection or live infrastructure command execution.
- Service lifecycle promotion.
- Customer application feature implementation.
- Workbook generation.
- Responsive web application implementation.
- FFFA repository modification.
- Changes to AI Session Readiness calculation rules.
- Hidden readiness regeneration from the Engineering Metrics command.
- Workstream Continuity Brief template or live brief creation.
- Live Platform Health dashboard deployment or connection.
- Production credentials, public internet exposure, release commit, push, or tag.

---

## Deferred Scope

- PLAT-14.2 live backup, restore, and alerting execution.
- PLAT-14.4 authentication-boundary implementation.
- FFFA implementation pending Chris's customer acceptance review.
- Financial Domain Foundation changes except separately approved defect fixes.
- Remote access or public internet exposure.
- Alpha, Bravo, or Charlie implementation without its separately authorized work package.

---

## Related Documents

- [AI Role Catalog](../../engineering-organization/AI_Role_Catalog.md)
- [Execution Agent Specification](../../engineering-organization/Execution_Agent_Specification.md)
- [Operations Analyst Specification](../../engineering-organization/Operations_Analyst_Specification.md)
- [Engineering Metrics v2](../../engineering-organization/Engineering_Metrics_v2.md)
- [Governed Automation Framework](../../engineering-organization/Governed_Automation_Framework.md)
- [AI Collaboration Governance Specification](../../engineering-organization/ai-collaboration/AI_Collaboration_Governance_Specification.md)
- [Platform Operations Domain Architecture](../../architecture/Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](../../specifications/Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Container Operational Health Specification](../../specifications/Container_Operational_Health_Specification.md)
- [Container Metrics Modernization Specification](../../specifications/Container_Metrics_Modernization_Specification.md)
- [Operational Excellence Specification](../../specifications/Operational_Excellence_Specification.md)
- [Platform Health Dashboard Specification](../../specifications/Platform_Health_Dashboard_Specification.md)
- [Platform Authentication Boundary Specification](../../specifications/Platform_Authentication_Boundary_Specification.md)
- [Engineering Portfolio Kanban](../../portfolio/Engineering_Portfolio_Kanban.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 2.7 | Recorded Architecture Gatekeeper acceptance and publication of the Registry identity implementation while preserving record-migration, PLAT, provider, dashboard, activation, and live-work gates. |
| 2.6 | Recorded completion of the required exact-plan governed approval-artifact correction pending final Gatekeeper acceptance. |
| 2.5 | Recorded complete unpublished Registry Container Identity Foundation implementation while preserving separate publication, record-migration, PLAT, provider, and live-work gates. |
| 2.4 | Recorded PLAT-14.1A and Registry Container Identity Foundation architecture/specification publication with all implementation gates blocked. |
| 2.3 | Recorded PLAT-14.0A publication and PLAT-14.1A Container Operational Health specification alignment with Option B implementation direction and later gates blocked. |
| 2.2 | Added PLAT-14.0A Platform Operations domain architecture, blocked PLAT-14.1A pending publication and alignment, and synchronized downstream gates. |
| 2.1 | Recorded publication of the Architecture Gatekeeper-approved EO-14.4A repository implementation while preserving separate activation, Bravo, Charlie, and live-work gates. |
| 2.0 | Recorded EO-14.4A Option B repository implementation complete pending Architecture Gatekeeper review, with automation and Execution Agent activation and live work unchanged. |
| 1.9 | Clarified EO-14.4A as orchestration over the published EO-14.1A Execution Capability while preserving separate implementation, activation, and live-work gates. |
| 1.8 | Recorded publication of the Architecture Gatekeeper-approved EO-14.1A repository implementation while preserving activation, EO-14.4A, Bravo, Charlie, FFFA, and live-work gates. |
| 1.7 | Recorded EO-14.1A Option B+ Execution Capability repository implementation pending Architecture Gatekeeper review, with activation, EO-14.4A, Bravo, Charlie, FFFA, and live work unchanged. |
| 1.6 | Closed and published the Architecture Gatekeeper-approved EO-14.8 capability baseline and identified Alpha EO-14.1A and EO-14.4A as next while preserving unstarted workstream boundaries. |
| 1.5 | Recorded EO-14.8E implementation, parent implementation completion pending final review, and repository-only Platform Health boundary. |
| 1.4 | Recorded EO-14.8D implementation for Architecture Gatekeeper review, EO-14.8E blocking, and unchanged Alpha, Bravo, Charlie and live-work boundaries. |
| 1.3 | Recorded EO-14.8C.2 active operationalization and Alpha, Bravo, and Charlie readiness without starting implementation. |
| 1.2 | Added EO-14.8 AI Collaboration Governance specification-package traceability and paused Alpha, Bravo, and Charlie pending governed AI collaboration controls. |
| 1.1 | Replaced initial portfolio execution sequencing with approved Option C governed vertical slice for Container Operational Health. |
| 1.0 | Initial Milestone 14 portfolio plan. |
