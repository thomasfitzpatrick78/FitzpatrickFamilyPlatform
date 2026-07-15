# Engineering Portfolio Kanban

**Document Version:** 1.1

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** Milestone 14

---

## Purpose

This repository-native Kanban tracks governed Milestone 14 portfolio work across Engineering Organization, Shared Platform, and the Fitzpatrick Family Financial Assistant.

It is a planning artifact. It does not authorize implementation.

---

## Status Values

- Proposed
- Specified
- Approved
- Ready for Implementation
- In Progress
- Validation
- Done
- Deferred

---

## Kanban

| Work Package | Workstream | Repository | Status | Priority | Dependencies | Approval State | Assigned AI Role | Customer Persona | Customer Impact | Platform Impact | EO Impact | Evidence Required | Deferred Items |
|--------------|------------|------------|--------|----------|--------------|----------------|------------------|------------------|-----------------|-----------------|-----------|-------------------|----------------|
| EO-14.1 | Execution Agent | FitzpatrickFamilyPlatform | Specified | High | AI Role Catalog; privileged integration standard | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Safer governed operations | Live-runbook boundary | Defines execution role | Role spec, catalog link, validation results | Activation and credentials |
| EO-14.2 | Operations Analyst | FitzpatrickFamilyPlatform | Specified | Medium | Observability evidence | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Better operational interpretation | Health trend review | Defines analysis role | Role spec, evidence sources | Live operations authority |
| EO-14.3 | Engineering Metrics v2 | FitzpatrickFamilyPlatform | Specified | Medium | EAP reports; maturity model | Engineering Organization Advisor review required | Codex Implementation Engineer | Platform Administrator | Better delivery visibility | Portfolio health evidence | Metrics evolution | Metrics spec and report mapping | Automated longitudinal metrics |
| EO-14.4 | Governed Automation Framework | FitzpatrickFamilyPlatform | Specified | High | Engineering Lifecycle | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Safer automation | Automation lifecycle | Reusable governance | Framework spec | Active scheduled automation |
| PLAT-14.1 | Container Metrics Modernization | FitzpatrickFamilyPlatform | Specified | High | PLAT-13.6.3B; human production approval | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | More accurate operations visibility | Container telemetry modernization | Evidence-first platform execution | Spec, runbook criteria, validation plan | Live deployment |
| PLAT-14.2 | Operational Excellence | FitzpatrickFamilyPlatform | Specified | High | Backup and rollback strategy | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Recovery confidence | Backup, restore, alerts | Operations maturity | Spec, evidence template plan | Full disaster recovery implementation |
| PLAT-14.3 | Platform Health Dashboard | FitzpatrickFamilyPlatform | Specified | Medium | PLAT-14.1; reports | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Executive operational view | Health dashboard model | Metrics/report integration | Spec and source ownership | Unified portal |
| PLAT-14.4 | Platform Authentication Boundary | FitzpatrickFamilyPlatform | Specified | High | FFFA-14.2B; human production approval | Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | Safe household web access | Reverse proxy, identity, HTTPS, LAN controls | Cross-repository security boundary | Auth-boundary spec, package placeholder, direct-access tests | Live deployment and credentials |
| EO-14.5 | Unify Product and Engineering Test Package Namespaces | Cross-repository / FamilyFinanceAssistant | Deferred | Medium | FFFA Architecture Backlog AB-010 | Future Architecture Gatekeeper review required | Codex Implementation Engineer | Platform Administrator | No direct finance defect; lower release-validation friction | Reusable repository test-quality pattern | Tracks duplicate `tests.*` namespace risk across product and engineering suites | FFFA AB-010; evidence that separate `python3 -m pytest tests` and `python3 -m pytest engineering/tests` pass; future single-command acceptance evidence | Nonblocking for FFFA-14.2A; separate suite execution remains current governed workaround |
| EO-14.6 | Standardize Reproducible Python Validation Environments | Cross-repository / FamilyFinanceAssistant | Deferred | Medium | FFFA Architecture Backlog AB-011; governed dependency declarations | Future Architecture Gatekeeper and Engineering Organization Advisor review required | Codex Implementation Engineer | Platform Administrator | No confirmed customer workbook defect; lower false-failure risk | Candidate reusable environment practice across repositories | Tracks reproducible runtime/test/native dependency setup for customer apps and Platform automation | FFFA AB-011; dependency declaration review; evidence that clean local/CI setup supports product tests, engineering tests, and Excel generation | Nonblocking for FFFA-14.2A; copied `.venv` artifacts are unsupported |
| EO-14.7 | Customer Data/Test Environment Isolation | Cross-repository / FamilyFinanceAssistant | Proposed | High | FFFA CUTOVER-001; FFFA Architecture Backlog AB-012 | Architecture Gatekeeper review required | Codex Implementation Engineer | Household Accountant | Prevents customer acceptance evidence contamination | Reusable customer-environment cutover governance | Candidate reusable guard/checklist pattern for customer-facing applications | FFFA customer-path guard tests; Platform Customer Environment Cutover Checklist; sanitized cutover evidence | Future repository validator or EAP check |
| FFFA-14.1 | Transaction Categorization Intelligence | FamilyFinanceAssistant | Specified | High | Existing categorization behavior | Product and architecture review required | Codex Implementation Engineer | Household Accountant | Better data quality and review | None direct | Customer-facing traceability | Specification and acceptance criteria | Implementation |
| FFFA-14.2 | Multi-Channel Financial Presentation | FamilyFinanceAssistant | Specified | High | ADR-087; reporting contract; personas | Product and architecture review required | Codex Implementation Engineer | Household Accountant | Excel-first reporting and web summary | Shared reporting pattern | Portfolio customer-value evidence | ADR, specs, customer acceptance plan | Workbook and web implementation |

---

## Maintenance Rule

Kanban updates must remain repository-native Markdown unless a future approved tool is introduced.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Added EO-14.7 customer data/test environment isolation governance item. |
| 1.1 | Added EO-14.5 and EO-14.6 cross-repository test quality and reproducible Python environment improvement items. |
| 1.0 | Initial Milestone 14 Engineering Portfolio Kanban. |
