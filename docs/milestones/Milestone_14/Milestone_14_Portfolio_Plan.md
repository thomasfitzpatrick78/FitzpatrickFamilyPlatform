# Milestone 14 - Operationalizing the AI Engineering Organization

**Document Version:** 1.6

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
├── Container Metrics Modernization repository implementation
├── Operations Analyst interpretation
├── Platform Health Dashboard integration
├── Engineering Metrics v2 evidence
├── Architecture Gatekeeper review
└── Separate future human approval for live infrastructure execution
```

The Fitzpatrick Family Platform owns Engineering Organization operating model, Shared Platform architecture, portfolio coordination, and cross-product engineering governance.

The Fitzpatrick Family Financial Assistant remains the flagship customer-facing application. FFFA customer implementation is paused while Chris performs customer acceptance. The Financial Domain Foundation remains frozen for the rest of Milestone 14 except for separately approved defect fixes.

This repository preserves FFFA as the Milestone 14 customer-value pillar through published FFFA specifications, ADR-087, personas, reporting contracts, and customer acceptance evidence. It does not authorize new FFFA implementation.

EO-14.8 AI Collaboration Governance now governs AI participant initialization, continuity, completion, stewardship, repository readiness validation, and readiness observability. EO-14.8A, EO-14.8B, EO-14.8C.1, EO-14.8C.2, EO-14.8D, EO-14.8E, and the EO-14.8 parent capability are complete. The capability is published as the Engineering Organization baseline following Architecture Gatekeeper approval. The next Engineering Organization work is Alpha through EO-14.1A and EO-14.4A. Alpha, Bravo, and Charlie remain unstarted, and no live work is authorized. Future Platform Health dashboard runtime deployment remains PLAT work.

---

## Work Package Plan

| Work Package | Workstream | Repository | Purpose | Primary Evidence |
|--------------|------------|------------|---------|------------------|
| EO-14.1 | Execution Agent | FitzpatrickFamilyPlatform | Define governed live-runbook execution role. | Execution Agent specification; role catalog update. |
| EO-14.1A | Execution Agent Operationalization | FitzpatrickFamilyPlatform | Define execution contracts, activation boundaries, handoffs, and repository-only controls for the first vertical slice. | Updated planning artifacts; future implementation package. |
| EO-14.2 | Operations Analyst | FitzpatrickFamilyPlatform | Define governed operational health analysis role. | Operations Analyst specification; role catalog update. |
| EO-14.2A | Operations Analyst Operationalization | FitzpatrickFamilyPlatform | Define Container Operational Health interpretation procedures and evidence states. | Operations Analyst procedures; evidence interpretation model. |
| EO-14.3 | Engineering Metrics v2 | FitzpatrickFamilyPlatform | Define practical evidence-based engineering metrics. | Metrics v2 specification and acceptance criteria. |
| EO-14.3A | Engineering Metrics v2 Refinement | FitzpatrickFamilyPlatform | Map vertical-slice evidence into Engineering Metrics v2 without false precision. | Metric mapping and validation evidence. |
| EO-14.4 | Governed Automation Framework | FitzpatrickFamilyPlatform | Define automation proposal, approval, operation, review, and retirement. | Automation framework specification. |
| EO-14.4A | Governed Automation Framework Operationalization | FitzpatrickFamilyPlatform | Define automation catalog, lifecycle, evidence, failure, rollback, and retirement controls for the first vertical slice. | Automation control package. |
| EO-14.8 | AI Collaboration Governance | FitzpatrickFamilyPlatform | Govern AI participant initialization, continuity, completion, stewardship, readiness validation, and readiness observability. | Complete; Architecture Gatekeeper approved; Engineering Organization baseline published. |
| EO-14.8A | AI Collaboration Governance Capability Charter | FitzpatrickFamilyPlatform | Approved architectural constitution for AI Collaboration Governance. | Complete. |
| EO-14.8B | AI Collaboration Governance Repository Specification Package | FitzpatrickFamilyPlatform | Specify charter, lifecycle, standards, continuity brief, Steward role, and future readiness validator. | Complete. |
| EO-14.8C | AI Collaboration Governance Repository Implementation | FitzpatrickFamilyPlatform | Implement approved reusable framework and operational artifacts. | Complete through EO-14.8C.1 and EO-14.8C.2. |
| EO-14.8C.1 | AI Collaboration Governance Repository Framework | FitzpatrickFamilyPlatform | Provide the reusable repository framework and blank templates. | Complete. |
| EO-14.8C.2 | AI Collaboration Governance Milestone 14 Operationalization | FitzpatrickFamilyPlatform | Instantiate governed continuity and limited Steward review for active Milestone 14 workstreams. | Complete; Alpha, Bravo, and Charlie ready but not started. |
| EO-14.8D | AI Session Readiness Validator | FitzpatrickFamilyPlatform | Validate repository evidence for governed AI participant onboarding. | Complete. |
| EO-14.8E | Engineering Metrics Integration | FitzpatrickFamilyPlatform | Consume governed readiness evidence in Engineering Metrics and repository-side Platform Health visibility. | Complete. |
| PLAT-14.1 | Container Metrics Modernization | FitzpatrickFamilyPlatform | Carry forward Milestone 13 container metrics architecture into approval-ready requirements. | Container metrics modernization specification. |
| PLAT-14.1A | Container Metrics Repository Implementation Package | FitzpatrickFamilyPlatform | Prepare restricted Docker API proxy, OTel Collector, Prometheus, Docker daemon metrics, Grafana provisioning, validation, runbooks, rollback, and evidence templates in repository form. | Repository implementation package and static validation evidence. |
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
| 1 | EO-14.1A Execution Agent Operationalization | Execution and handoff controls must be specified before any future live deployment request. |
| 2 | EO-14.4A Governed Automation Framework Operationalization | Automation lifecycle, catalog, approval, evidence, failure, rollback, and retirement controls must be specified before automation use. |
| 3 | PLAT-14.1A Container Metrics Repository Implementation Package | Repository telemetry contract, runbooks, rollback instructions, and evidence templates must be statically validated before live execution is requested. |
| 4 | EO-14.2A Operations Analyst Operationalization | Analysis procedures consume verified evidence and distinguish known, unknown, stale, unavailable, and failed signals. |
| 5 | PLAT-14.3A Platform Health Dashboard Completion | Dashboard completion follows the verified PLAT-14.1 telemetry contract. |
| 6 | EO-14.3A Engineering Metrics v2 Refinement | Metrics are refined from vertical-slice evidence without unsupported precision. |
| 7 | PLAT-14.2 Operational Excellence | Backup, restore, alerting, and broader operational excellence proceed only through separate architecture and human approval gates. |

This sequence is a governed integration model. It does not authorize live execution.

EO-14.8 has completed governed continuity initialization for Alpha, Bravo, and Charlie, passed Architecture Gatekeeper review, and been published as the Engineering Organization baseline. The current lifecycle posture is ready for governed execution. Alpha through EO-14.1A and EO-14.4A is the next Engineering Organization work package. Alpha, Bravo, and Charlie remain unstarted.

---

## Parallel Repository Workstreams

### Alpha - Engineering Organization Controls

**Scope:** EO-14.1A and EO-14.4A.

**Responsibilities:**

- Execution Agent activation and execution-contract design.
- Automation lifecycle, catalog, approval, evidence, failure, rollback, and retirement controls.
- Repository-only implementation.

**Boundary:** Alpha defines controls before any future live deployment request. It does not activate the Execution Agent for production or authorize automation against live infrastructure.

### Bravo - Platform Observability

**Scope:** PLAT-14.1A.

**Responsibilities:**

- Restricted Docker API Proxy repository configuration.
- OpenTelemetry Collector configuration.
- Prometheus integration.
- Docker daemon metrics configuration.
- Grafana provisioning and dashboard source contracts.
- Static validation, runbooks, rollback instructions, and evidence templates.

**Boundary:** Bravo must not deploy or connect to live infrastructure.

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
| Alpha controls before live request | Alpha must define execution and automation controls before any future live deployment request. |
| Bravo telemetry before final Charlie mappings | Bravo must define and validate the repository telemetry contract before final Charlie metric mappings. |
| Charlie evidence-state discipline | Charlie must distinguish known, unknown, stale, unavailable, and failed evidence. |
| Dashboard follows telemetry contract | PLAT-14.3 dashboard completion follows the verified PLAT-14.1 telemetry contract. |
| Operational Excellence live work remains separate | PLAT-14.2 live backup, restore, and alerting work requires separate architecture and human approval. |
| Architecture review before promotion | Architecture Gatekeeper review is required before lifecycle promotion. |

---

## Dependencies

| Dependency | Applies To | Required Before |
|------------|------------|-----------------|
| Milestone 13 closeout baseline and tag `milestone-13`. | All workstreams. | Milestone 14 implementation authorization. |
| PLAT-13.6.3B container metrics architecture. | PLAT-14.1A, PLAT-14.3A. | Container telemetry repository package and dashboard source mapping. |
| Privileged Infrastructure Integration Standard. | EO-14.1A, EO-14.4A, PLAT-14.1A, PLAT-14.2. | Any future live infrastructure execution. |
| Alpha controls. | PLAT-14.1A and any future live deployment request. | Execution, automation, and evidence contracts. |
| AI Collaboration Governance. | Alpha, Bravo, Charlie, and future parallel AI workstreams. | Governed initialization, continuity, completion, and handoff readiness. |
| Bravo repository telemetry contract. | EO-14.2A, EO-14.3A, PLAT-14.3A. | Final metric mappings and dashboard completion. |
| FFFA customer acceptance. | FFFA implementation continuation. | Any new FFFA implementation scope. |
| Platform authentication boundary specification. | Future FFFA-14.2B web implementation. | Web implementation with real household financial data. |

---

## Evidence Expectations

Milestone 14 Option C evidence should include:

- Alpha execution-contract and automation-control artifacts.
- AI Collaboration Governance specification package, EO-14.8D readiness reports and tests, and EO-14.8E Engineering Metrics and repository-side Platform Health evidence.
- Bravo repository telemetry contract, static validation, runbooks, rollback instructions, and evidence templates.
- Charlie evidence-state model and metric mapping that does not invent telemetry.
- PLAT-14.3 dashboard source contracts traceable to verified telemetry.
- Engineering Metrics v2 refinement based on repository evidence.
- Clear stop conditions and explicit human approval boundaries for any future live work.

---

## Acceptance Criteria

Milestone 14 Option C planning is ready for Architecture Gatekeeper review when:

- Option C - Governed Vertical Slice is recorded as the approved execution strategy.
- Container Operational Health is defined as the first governed vertical slice.
- Alpha, Bravo, and Charlie workstreams are defined with boundaries, dependencies, non-goals, and evidence expectations.
- EO-14.8A through EO-14.8E and the EO-14.8 parent capability are recorded complete, with Alpha, Bravo, and Charlie explicitly unstarted.
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
| Automation bypasses human approval. | Governed Automation Framework controls must be operationalized before automation use. |
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
- [Container Metrics Modernization Specification](../../specifications/Container_Metrics_Modernization_Specification.md)
- [Operational Excellence Specification](../../specifications/Operational_Excellence_Specification.md)
- [Platform Health Dashboard Specification](../../specifications/Platform_Health_Dashboard_Specification.md)
- [Platform Authentication Boundary Specification](../../specifications/Platform_Authentication_Boundary_Specification.md)
- [Engineering Portfolio Kanban](../../portfolio/Engineering_Portfolio_Kanban.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.6 | Closed and published the Architecture Gatekeeper-approved EO-14.8 capability baseline and identified Alpha EO-14.1A and EO-14.4A as next while preserving unstarted workstream boundaries. |
| 1.5 | Recorded EO-14.8E implementation, parent implementation completion pending final review, and repository-only Platform Health boundary. |
| 1.4 | Recorded EO-14.8D implementation for Architecture Gatekeeper review, EO-14.8E blocking, and unchanged Alpha, Bravo, Charlie and live-work boundaries. |
| 1.3 | Recorded EO-14.8C.2 active operationalization and Alpha, Bravo, and Charlie readiness without starting implementation. |
| 1.2 | Added EO-14.8 AI Collaboration Governance specification-package traceability and paused Alpha, Bravo, and Charlie pending governed AI collaboration controls. |
| 1.1 | Replaced initial portfolio execution sequencing with approved Option C governed vertical slice for Container Operational Health. |
| 1.0 | Initial Milestone 14 portfolio plan. |
