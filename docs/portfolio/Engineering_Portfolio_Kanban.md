# Engineering Portfolio Kanban

**Document Version:** 1.10

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

EO-14.8 and the Architecture Gatekeeper-approved Alpha EO-14.1A repository implementation are published. EO-14.4A is the next separately authorized Alpha package.

EO-14.8A through EO-14.8E, the EO-14.8 parent capability, and Alpha EO-14.1A repository implementation are published. Engineering Metrics consumes the governed readiness report without recalculation. EO-14.4A, Bravo, and Charlie remain unstarted, and no role activation or live work is authorized.

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
| EO-14.4 | Governed Automation Framework | FitzpatrickFamilyPlatform | Specified | High | Engineering Lifecycle | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Safer automation | Automation lifecycle | Reusable governance | Framework spec | Active scheduled automation |
| EO-14.4A | Alpha - Engineering Organization Controls | FitzpatrickFamilyPlatform | Ready for Repository Implementation | High | EO-14.8 complete; EO-14.4; EO-14.1A | Next Engineering Organization work; implementation not started | Codex Implementation Engineer | Platform Administrator | Safer future automation | Automation approval and evidence controls | Operationalizes governed automation | Automation catalog, lifecycle, approval, evidence, failure, rollback, retirement controls | Runtime automation |
| PLAT-14.1 | Container Metrics Modernization | FitzpatrickFamilyPlatform | Specified | High | PLAT-13.6.3B; human production approval | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | More accurate operations visibility | Container telemetry modernization | Evidence-first platform execution | Spec, runbook criteria, validation plan | Live deployment |
| PLAT-14.1A | Bravo - Platform Observability | FitzpatrickFamilyPlatform | Ready for Repository Implementation | High | EO-14.8 complete; Alpha controls; PLAT-14.1; PLAT-13.6.3B | Ready; implementation not started | Codex Implementation Engineer | Platform Administrator | Future container health visibility | Repository telemetry contract | Vertical-slice platform evidence | Restricted Docker API proxy config, OTel config, Prometheus integration, Docker daemon metrics config, Grafana provisioning contracts, static validation, runbooks, rollback, evidence templates | Docker execution, SSH, live Prometheus/Grafana changes |
| EO-14.2 | Operations Analyst | FitzpatrickFamilyPlatform | Specified | Medium | Observability evidence | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Better operational interpretation | Health trend review | Defines analysis role | Role spec, evidence sources | Live operations authority |
| EO-14.2A | Charlie - Operations Intelligence | FitzpatrickFamilyPlatform | Ready for Repository Implementation | High | EO-14.8 complete; Operations Analyst spec; Bravo telemetry contract | Ready; implementation not started | Codex Implementation Engineer | Platform Administrator | Evidence-based health interpretation | Container-health analysis structure | Operationalizes Operations Analyst | Known, unknown, stale, unavailable, failed evidence-state model; analysis procedure | Final mappings before Bravo telemetry contract |
| PLAT-14.3 | Platform Health Dashboard | FitzpatrickFamilyPlatform | Specified | Medium | PLAT-14.1; reports | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Executive operational view | Health dashboard model | Metrics/report integration | Spec and source ownership | Unified portal |
| PLAT-14.3A | Platform Health Dashboard Completion | FitzpatrickFamilyPlatform | Paused | Medium | Verified PLAT-14.1A telemetry contract; EO-14.2A; separate PLAT approval | Paused pending PLAT telemetry and analysis gates | Codex Implementation Engineer | Platform Administrator | Container health summarized accurately | Dashboard source contract completion | Connects platform evidence to analysis | Dashboard contract, source mapping, validation evidence | Runtime deployment and dashboard claims before telemetry proof |
| EO-14.3 | Engineering Metrics v2 | FitzpatrickFamilyPlatform | Specified | Medium | EAP reports; maturity model | Engineering Organization Advisor review required | Codex Implementation Engineer | Platform Administrator | Better delivery visibility | Portfolio health evidence | Metrics evolution | Metrics spec and report mapping | Automated longitudinal metrics |
| EO-14.3A | Charlie - Operations Intelligence | FitzpatrickFamilyPlatform | Ready for Repository Implementation | Medium | EO-14.8 complete; Bravo telemetry contract; EO-14.2A; PLAT-14.3A | Ready; implementation not started | Codex Implementation Engineer | Platform Administrator | Transparent milestone evidence | Metrics mapped to verified evidence | Refines Engineering Metrics v2 | Engineering metric mappings; no false precision; unknown/stale/unavailable signal treatment | Metrics based on invented telemetry |
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
| Alpha before live request | EO-14.1A and EO-14.4A must define execution and automation controls before any future live deployment request. |
| Bravo before final Charlie mappings | PLAT-14.1A must define and validate the repository telemetry contract before final EO-14.2A or EO-14.3A mappings. |
| Charlie evidence-state discipline | EO-14.2A and EO-14.3A must distinguish known, unknown, stale, unavailable, and failed evidence. |
| Dashboard follows telemetry contract | PLAT-14.3A follows the verified PLAT-14.1A telemetry contract. |
| Operational Excellence remains separate | PLAT-14.2 live backup, restore, and alerting work requires separate architecture and human approval. |
| Architecture review before promotion | Architecture Gatekeeper review is required before lifecycle promotion. |

---

## Maintenance Rule

Kanban updates must remain repository-native Markdown unless a future approved tool is introduced.

---

## Revision History

| Version | Description |
|---------|-------------|
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
