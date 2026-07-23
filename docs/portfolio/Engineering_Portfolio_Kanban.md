# Engineering Portfolio Kanban

**Document Version:** 1.28

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** Milestone 14

---

## Purpose

This repository-native Kanban tracks governed Milestone 14 portfolio work across Engineering Organization, Shared Platform, and the Fitzpatrick Family Financial Assistant.

It is a planning artifact. It does not authorize implementation, live deployment, or production operations.

---

## Status Values

- Proposed
- Specified
- Approved
- Ready for Repository Implementation
- In Progress
- Validation
- Done
- Paused
- Deferred
- Blocked
- Architecture Approved

---

## Approved Strategy

Selected execution strategy: Option C - Governed Vertical Slice.

First governed vertical slice: Container Operational Health.

Option C introduces three bounded repository workstreams:

- Alpha - Engineering Organization Controls.
- Bravo - Platform Observability.
- Charlie - Operations Intelligence.

Live infrastructure execution remains unauthorized until separate Architecture Gatekeeper review and explicit human approval.

EO-14.8 and the Architecture Gatekeeper-approved Alpha EO-14.1A and EO-14.4A repository implementations are published; automation remains unactivated.

EO-14.8A through EO-14.8E, the EO-14.8 parent capability, Alpha EO-14.1A and EO-14.4A repository implementations, the bounded Bravo Foundation implementation, and the PLAT-14.1A Option B fixture-only repository implementation are published. Charlie remains unstarted. No automation, role activation, provider access, dashboard/API work, or live work is authorized.

PLAT-14.0A architecture remains published with Implemented: No. The PLAT-14.1A specification, Registry Container Identity Foundation, fixture-only repository slice, provider architecture/security design, repository provider foundation, and formal proxy security review are accepted and published. The constrained proxy is approved only as the future implementation target. Exactly five Registry records declare `not_applicable`; no proxy, privileged deployment, target, credential, access, observation, or activation is authorized.

---

## Kanban

| Work Package | Workstream | Repository | Status | Priority | Dependencies | Approval State | Assigned AI Role | Customer Persona | Customer Impact | Platform Impact | EO Impact | Evidence Required | Deferred Items |
|--------------|------------|------------|--------|----------|--------------|----------------|------------------|------------------|-----------------|-----------------|-----------|-------------------|----------------|
| EO-14.1 | Execution Agent | FitzpatrickFamilyPlatform | Specified | High | AI Role Catalog; privileged integration standard | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Safer governed operations | Live-runbook boundary | Defines execution role | Role spec, catalog link, validation results | Activation and credentials |
| EO-14.8 | AI Collaboration Governance | FitzpatrickFamilyPlatform | Done | High | EO-14.8A through EO-14.8E | Complete; Architecture Gatekeeper approved; baseline published | Codex Implementation Engineer | Platform Administrator | Safer AI-assisted delivery | Governed AI participation and readiness visibility | Defines AI collaboration controls | Charter, specifications, operational framework, readiness reports, metrics reports, focused tests | Alpha, Bravo, and Charlie remain separate |
| EO-14.8A | AI Collaboration Governance Capability Charter | FitzpatrickFamilyPlatform | Done | High | Approved architecture charter | Complete | Codex Implementation Engineer | Platform Administrator | Clear AI collaboration constitution | Governance traceability | Capability constitution | Charter artifact | No implementation authority |
| EO-14.8B | AI Collaboration Governance Repository Specification Package | FitzpatrickFamilyPlatform | Done | High | EO-14.8A | Complete | Codex Implementation Engineer | Platform Administrator | Governed AI session readiness | Repository-only specifications | Operationalizes AI collaboration planning | Charter, specification, lifecycle, initialization, completion, continuity brief, Steward, validator specification | None within EO-14.8B |
| EO-14.8C | AI Collaboration Governance Repository Implementation | FitzpatrickFamilyPlatform | Done | High | EO-14.8B Architecture Gatekeeper approval | Complete | Codex Implementation Engineer | Platform Administrator | Governed continuity | Repository controls | Operationalizes approved framework | Framework, templates, operational instances, validation evidence | None within EO-14.8C |
| EO-14.8C.1 | AI Collaboration Governance Repository Framework | FitzpatrickFamilyPlatform | Done | High | EO-14.8B | Complete | Codex Implementation Engineer | Platform Administrator | Reusable governed collaboration | Repository framework and templates | Reusable initialization and continuity structure | Framework and blank templates | None within EO-14.8C.1 |
| EO-14.8C.2 | AI Collaboration Governance Milestone 14 Operationalization | FitzpatrickFamilyPlatform | Done | High | EO-14.8C.1 | Complete | Codex Implementation Engineer | Platform Administrator | Governed Milestone 14 continuity | Operational continuity instances | Initializes bounded workstreams | Four continuity briefs, limited Steward review, validation evidence | Alpha, Bravo, and Charlie implementation |
| EO-14.8D | AI Session Readiness Validator | FitzpatrickFamilyPlatform | Done | Medium | EO-14.8C repository evidence | Complete | Codex Implementation Engineer | Platform Administrator | Governed onboarding readiness | Reusable EAP readiness engine | Repository-evidence readiness validation | Domain results, Markdown and JSON reports, focused tests | Readiness-rule changes remain separate |
| EO-14.8E | Engineering Metrics Integration | FitzpatrickFamilyPlatform | Done | Medium | EO-14.8D governed reports | Complete | Codex Implementation Engineer | Platform Administrator | Visible onboarding readiness | Repository metrics and health-source evidence | Integrates governed readiness without recalculation | Structured and Markdown Engineering Metrics reports, Platform Health source contract, focused tests | Live dashboard deployment remains PLAT work |
| EO-14.1A | Alpha - Engineering Organization Controls | FitzpatrickFamilyPlatform | Done | High | EO-14.8 complete; EO-14.1; approved Option B+ work package | Repository implementation complete and published; Architecture Gatekeeper approved | Codex Implementation Engineer | Platform Administrator | Safer future operations | Execution-contract readiness | Operationalizes Execution Agent boundaries without activation | Immutable models, deterministic validation, JSON and Markdown serialization, bounded CLI, fixtures, focused tests, governed validation evidence | Live Execution Agent activation |
| EO-14.4 | Governed Automation Framework | FitzpatrickFamilyPlatform | Specified | High | Engineering Lifecycle; published EO-14.1A Execution Capability | Architecture aligned; EO-14.4A repository implementation published | Codex Implementation Engineer | Platform Administrator | Safer automation | Automation orchestration lifecycle | Reusable governance aligned to execution contracts | Framework specification with explicit EO-14.1A ownership boundary | Active scheduled automation |
| EO-14.4A | Alpha - Engineering Organization Controls | FitzpatrickFamilyPlatform | Done | High | EO-14.8 complete; EO-14.4; published EO-14.1A | Repository implementation complete and published; Architecture Gatekeeper approved | Codex Implementation Engineer | Platform Administrator | Safer future automation | Orchestration approval and lifecycle controls | Coordinates governed execution without redefining it | Immutable orchestration models, strict IO, deterministic eligibility and transitions, EO-14.1A validation reuse, handoff rendering, bounded CLI, fixtures, and tests | Orchestration persistence, runtime, activation, scheduling, retries, and all automation operation |
| PLAT-14.0A | Architecture Integration / Bravo | FitzpatrickFamilyPlatform | Completed | High | Infrastructure Registry; Platform Digital Twin; PLAT-13.6.3B evidence; Alpha controls | Domain architecture and contracts published at `c8f9bc3`; Implemented: No | Codex Implementation Engineer acting as Architecture Analyst | Platform Administrator | Explainable provider-independent operational health | Platform Operations bounded context and canonical contracts | First downstream product architecture over published controls | Published domain architecture; contract specification; ADR-009 through ADR-011; portfolio and continuity evidence | Implementation, provider adapters, runtime behavior, activation, and live work |
| Registry Container Identity Foundation | Architecture Integration / Registry | FitzpatrickFamilyPlatform | Done; Exact Five-Record Migration Validated | High | Published PLAT-14.1A specification; Infrastructure Registry; Platform Digital Twin; ADR-006; ADR-009 through ADR-011 | Historical plan approved, bound, executed, and completion-validated; exactly five `not_applicable`; rollback ready; 16 remain review-required | Codex Implementation Engineer | Platform Administrator | Stable declared container-service identity | Additive schema `1.1` and deterministic evidence-gated migration capability | Prerequisite for authoritative PLAT-14.1A subjects | Historical/current plan separation, 0/16/23 current plan, exact rollback, completion validation, deterministic no-change, CLI, Digital Twin compatibility, tests | Evidence and approvals for remaining subjects, provider and live work |
| PLAT-14.1 | Container Metrics Modernization | FitzpatrickFamilyPlatform | Specified | High | PLAT-13.6.3B; human production approval | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | More accurate operations visibility | Container telemetry modernization | Evidence-first platform execution | Spec, runbook criteria, validation plan | Live deployment |
| PLAT-14.1A | Bravo - Platform Observability | FitzpatrickFamilyPlatform | Done; Architecture Gatekeeper Accepted / Published / Fixture Only / Unactivated | High | Published PLAT-14.0A; PLAT-14.1A specification; Registry Foundation; provider foundation; EO-14.8; Alpha controls | Fixture-only health/provider foundations and constrained-proxy security review accepted and published; five migrated subjects are `not_applicable`; implementation accepted and published | Chief Architect / Architecture Gatekeeper | Platform Administrator | Deterministic explainable Container Operational Health with a safe path to future named-target evidence | Provider-independent evidence, strict adapters, default-deny privileged boundary, distinct implementation/deployment/observation gates | Governed vertical slice plus reusable secure-provider lifecycle | Trust-boundary validation, endpoint-category matrix, authentication/deployment decision, expanded threat model, pass/fail security gates | Repository-only proxy foundation; then eligible-subject, privileged deployment, named-target observation, consumers, activation, and live work under separate authorization |
| EO-14.2 | Operations Analyst | FitzpatrickFamilyPlatform | Specified | Medium | Observability evidence | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Better operational interpretation | Health trend review | Defines analysis role | Role spec, evidence sources | Live operations authority |
| EO-14.2A | Charlie - Operations Intelligence | FitzpatrickFamilyPlatform | Blocked | High | Published PLAT-14.0A consumer contract; later architecture-aligned PLAT-14.1A evidence; Operations Analyst spec | Implementation not started; final mappings blocked pending PLAT contracts and evidence | Codex Implementation Engineer | Platform Administrator | Evidence-based health interpretation | Container-health interpretation | Operationalizes Operations Analyst | Advisory procedures that consume governed evidence, reconciliation, health, confidence, reasons, and findings without recalculation | Implementation and final mappings before required PLAT gates |
| PLAT-14.3 | Platform Health Dashboard | FitzpatrickFamilyPlatform | Specified | Medium | PLAT-14.1; reports | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Executive operational view | Health dashboard model | Metrics/report integration | Spec and source ownership | Unified portal |
| PLAT-14.3A | Platform Health Dashboard Completion | FitzpatrickFamilyPlatform | Paused | Medium | Published PLAT-14.0A consumer contract; verified architecture-aligned PLAT-14.1A evidence; EO-14.2A; separate PLAT approval | Paused pending PLAT architecture, evidence, and analysis gates | Codex Implementation Engineer | Platform Administrator | Container health summarized accurately | Read-only dashboard consumer completion | Renders governed Platform Operations outputs | Dashboard contract, source mapping, no-data handling, validation evidence | Runtime deployment, independent health calculation, and dashboard claims before evidence proof |
| EO-14.3 | Engineering Metrics v2 | FitzpatrickFamilyPlatform | Specified | Medium | EAP reports; maturity model | Engineering Organization Advisor review required | Codex Implementation Engineer | Platform Administrator | Better delivery visibility | Portfolio health evidence | Metrics evolution | Metrics spec and report mapping | Automated longitudinal metrics |
| EO-14.3A | Charlie - Operations Intelligence | FitzpatrickFamilyPlatform | Blocked | Medium | Published PLAT-14.0A contracts; architecture-aligned PLAT-14.1A evidence; EO-14.2A; PLAT-14.3A | Implementation not started; blocked pending required evidence | Codex Implementation Engineer | Platform Administrator | Transparent milestone evidence | Metrics mapped to governed assessments | Refines Engineering Metrics v2 | Engineering metric mappings; no false precision; contract and policy version traceability | Metrics based on invented telemetry or independent health calculation |
| PLAT-14.2 | Operational Excellence | FitzpatrickFamilyPlatform | Specified | High | PLAT-14.1A; PLAT-14.3A; separate approval | Architecture and human approval required before live work | Codex Implementation Engineer | Platform Administrator | Recovery confidence | Backup, restore, alerts | Operations maturity | Spec, evidence template plan, future architecture approval | Live backup, restore, alerting, production operations |
| PLAT-14.4 | Platform Authentication Boundary | FitzpatrickFamilyPlatform | Deferred | Medium | FFFA-14.2B; future web implementation approval | Future Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Safe household web access when FFFA resumes | Reverse proxy, identity, HTTPS, LAN controls | Cross-repository security boundary | Auth-boundary spec, package placeholder, direct-access tests | Live deployment and credentials |
| EO-14.5 | Unify Product and Engineering Test Package Namespaces | Cross-repository / FamilyFinanceAssistant | Deferred | Medium | FFFA Architecture Backlog AB-010 | Future Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | No direct finance defect; lower release-validation friction | Reusable repository test-quality pattern | Tracks duplicate `tests.*` namespace risk across product and engineering suites | FFFA AB-010; evidence that separate `python3 -m pytest tests` and `python3 -m pytest engineering/tests` pass; future single-command acceptance evidence | Nonblocking for FFFA-14.2A; separate suite execution remains current governed workaround |
| EO-14.6 | Standardize Reproducible Python Validation Environments | Cross-repository / FamilyFinanceAssistant | Deferred | Medium | FFFA Architecture Backlog AB-011; governed dependency declarations | Future Architecture Gatekeeper and Engineering Organization Advisor review required | Codex Implementation Engineer | Platform Administrator | No confirmed customer workbook defect; lower false-failure risk | Candidate reusable environment practice across repositories | Tracks reproducible runtime/test/native dependency setup for customer apps and Platform automation | FFFA AB-011; dependency declaration review; evidence that clean local/CI setup supports product tests, engineering tests, and Excel generation | Nonblocking for FFFA-14.2A; copied `.venv` artifacts are unsupported |
| EO-14.7 | Customer Data/Test Environment Isolation | Cross-repository / FamilyFinanceAssistant | Proposed | High | FFFA CUTOVER-001; FFFA Architecture Backlog AB-012 | Architecture Gatekeeper review required | Codex Implementation Engineer | Household Accountant | Prevents customer acceptance evidence contamination | Reusable customer-environment cutover governance | Candidate reusable guard/checklist pattern for customer-facing applications | FFFA customer-path guard tests; Platform Customer Environment Cutover Checklist; sanitized cutover evidence | Future repository validator or EAP check |
| FFFA-14.1 | Transaction Categorization Intelligence | FamilyFinanceAssistant | Paused | High | Chris customer acceptance; Financial Domain Foundation freeze | Product and architecture review required before any implementation resumes | Codex Implementation Engineer | Household Accountant | Better data quality and review | None direct | Customer-facing traceability | Published FFFA specification and customer acceptance criteria | FFFA implementation |
| FFFA-14.2 | Multi-Channel Financial Presentation | FamilyFinanceAssistant | Paused | High | Chris customer acceptance; Financial Domain Foundation freeze; ADR-087; reporting contract; personas | Product and architecture review required before any implementation resumes | Codex Implementation Engineer | Household Accountant | Excel-first reporting and web summary | Shared reporting pattern | Portfolio customer-value evidence | ADR, specs, customer acceptance plan | Workbook generation and web implementation |

---

## Integration Gates

| Gate | Requirement |
|------|-------------|
| AI collaboration controls before Alpha, Bravo, and Charlie | Satisfied by the completed, Architecture Gatekeeper-approved EO-14.8 capability baseline; each later workstream still requires its separately authorized work package. |
| Alpha before live request | EO-14.1A defines execution semantics; EO-14.4A defines orchestration flow and lifecycle progression that consume those semantics. Both must precede any future live deployment request. |
| Registry identity before authoritative PLAT-14.1A assessment | Foundation is published; the repository slice uses synthetic identity fixtures only. Approved migration precedes any authoritative current-subject assessment. |
| Bravo before final Charlie mappings | Architecture-aligned PLAT-14.1A must implement and validate the governed contracts before final EO-14.2A or EO-14.3A mappings. |
| Charlie evidence-state discipline | EO-14.2A and EO-14.3A must preserve observation, evidence, reconciliation, health, confidence, and interpretation boundaries. |
| Dashboard follows governed outputs | PLAT-14.3A consumes governed assessments and verified evidence and must not recalculate authoritative health or render no-data as Healthy. |
| Operational Excellence remains separate | PLAT-14.2 live backup, restore, and alerting work requires separate architecture and human approval. |
| Architecture review before promotion | Architecture Gatekeeper review is required before lifecycle promotion. |

---

## Maintenance Rule

Kanban updates must remain repository-native Markdown unless a future approved tool is introduced.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.28 | Recorded formal constrained-proxy security review and the repository-only proxy foundation as the next gate while preserving the exact PLAT-14.1A fixture-only/unactivated state. |
| 1.27 | Recorded repository-only Production Provider Adapter Foundation publication while preserving the exact PLAT-14.1A fixture-only/unactivated status and all live-provider gates. |
| 1.26 | Recorded publication of the accepted PLAT-14.1A production provider architecture/security package while retaining all implementation, access, consumer, activation, and live gates. |
| 1.25 | Recorded exact five-record Registry migration, rollback/completion evidence, corrected current planner semantics, and unchanged provider, activation, and live-work gates. |
| 1.24 | Recorded deterministic exact-plan approval binding as complete and unpublished with every Registry record and later gate unchanged. |
| 1.23 | Recorded exact-plan approval-in-principle and completion of the unpublished, unbound approval evidence package with Registry and all later gates unchanged. |
| 1.22 | Recorded the complete unpublished Registry migration model-v2 idempotency correction in Validation with all Registry, approval, provider, activation, and live-work gates unchanged. |
| 1.21 | Recorded Architecture Gatekeeper acceptance and publication of the PLAT-14.1A Option B fixture-only repository vertical slice while retaining all record-migration, provider, dashboard/API, activation, and live gates. |
| 1.20 | Recorded the complete unpublished PLAT-14.1A Option B repository vertical slice while retaining all record-migration, provider, dashboard, activation, and live gates. |
| 1.19 | Recorded Architecture Gatekeeper acceptance and publication of the Registry identity implementation while retaining record-migration, PLAT, provider, activation, and live-work gates. |
| 1.18 | Recorded completion of required exact-plan approval-artifact hardening pending final Gatekeeper acceptance. |
| 1.17 | Recorded complete unpublished Registry Container Identity Foundation implementation with all records unchanged and later gates blocked. |
| 1.16 | Recorded PLAT-14.1A and Registry Container Identity Foundation architecture/specification publication without authorizing implementation. |
| 1.15 | Recorded PLAT-14.0A publication and PLAT-14.1A Container Operational Health Specification Alignment with implementation and later gates blocked. |
| 1.14 | Added PLAT-14.0A domain architecture in review preparation and blocked PLAT-14.1A pending publication and architecture alignment. |
| 1.13 | Recorded publication of the Architecture Gatekeeper-approved EO-14.4A repository implementation without activation or live work. |
| 1.12 | Recorded EO-14.4A Option B repository implementation in Validation pending Architecture Gatekeeper review without activation or live work. |
| 1.11 | Recorded the EO-14.4A orchestration-to-execution ownership clarification for Architecture Gatekeeper review without starting implementation or activation. |
| 1.10 | Recorded publication of the Architecture Gatekeeper-approved EO-14.1A repository implementation with activation and later work packages unchanged. |
| 1.9 | Recorded EO-14.1A repository implementation in Validation pending Architecture Gatekeeper review, with EO-14.4A, Bravo, Charlie, activation, and live work unchanged. |
| 1.8 | Recorded EO-14.8 capability completion and baseline publication, with Alpha EO-14.1A and EO-14.4A next and all three workstreams still unstarted. |
| 1.7 | Recorded EO-14.8E implementation, parent final-review state, and unchanged Alpha, Bravo, Charlie and live-operation boundaries. |
| 1.6 | Recorded EO-14.8D implementation-review status, EO-14.8E approval dependency, and unchanged workstream and live-operation boundaries. |
| 1.5 | Recorded EO-14.8C.2 active operationalization and Alpha, Bravo, and Charlie readiness without starting implementation. |
| 1.4 | Added EO-14.8A through EO-14.8E planning statuses and paused Alpha, Bravo, and Charlie pending AI Collaboration Governance controls. |
| 1.3 | Reworked Milestone 14 Kanban for Option C governed vertical slice, Alpha/Bravo/Charlie workstreams, FFFA pause, and integration gates. |
| 1.2 | Added EO-14.7 customer data/test environment isolation governance item. |
| 1.1 | Added EO-14.5 and EO-14.6 cross-repository test quality and reproducible Python environment improvement items. |
| 1.0 | Initial Milestone 14 Engineering Portfolio Kanban. |
