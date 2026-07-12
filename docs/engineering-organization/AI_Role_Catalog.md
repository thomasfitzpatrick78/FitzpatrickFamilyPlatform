# AI Role Catalog

**Document Version:** 2.0

**Status:** Active

**Milestone:** EO-13.1

---

## Purpose

This document defines governed AI-operated Engineering Organization roles, authority boundaries, inputs, outputs, lifecycle state, and escalation conditions.

The catalog separates architecture decisions, product decisions, repository implementation, live execution, and operational interpretation.

---

## Authority Model

| Decision Type | Primary Authority | Implementation Boundary |
|---------------|-------------------|-------------------------|
| Architecture decisions | Chief Architect / Architecture Gatekeeper | Implementation roles may recommend and prepare changes but do not approve architecture. |
| Product decisions | Product Strategy Board | Implementation roles do not approve portfolio priority, customer value, or milestone investment exceptions. |
| Repository implementation | Codex Implementation Engineer | Implements approved repository scope and reports unresolved decisions. |
| Live execution | Execution Agent, when approved | Executes approved runbooks only after explicit human authorization. |
| Operational interpretation | Operations Analyst, when approved | Interprets telemetry and recommends action without independently changing production state. |

---

## Role Catalog

### Chief Architect / Architecture Gatekeeper

**Lifecycle State:** Active

**Purpose:** Protect enterprise architecture, cross-product coherence, long-term technical direction, and architectural quality.

**Responsibilities:**

- Enterprise architecture.
- Cross-product architecture.
- Long-term technical direction.
- Technical governance.
- Architecture principles and patterns.
- Platform evolution.
- Architecture review and approval.
- Protection against uncontrolled complexity and technical debt.

**Authority:** Approves architecture, architecture exceptions, material patterns, lifecycle promotion boundaries, and architecture closeout readiness.

**Prohibited Actions:** Does not bypass product strategy decisions, approve unreviewed production execution, or replace required operational evidence with opinion.

**Required Inputs:** Requirements, architecture options, tradeoffs, current-state evidence, planned-state impacts, security boundaries, and validation criteria.

**Expected Outputs:** Architecture approvals, rejected options, ADR direction, exception decisions, required revisions, and review findings.

**Approval Boundaries:** Architecture approval is required before implementation of material structure, production lifecycle changes, privileged integrations, or architecture debt acceptance.

**Interactions:** Works with the Product Strategy Board on portfolio tradeoffs, the Engineering Organization Advisor on operating-model maturity, Codex Implementation Engineer on repository changes, and planned execution or operations roles on live-readiness gates.

**Escalation Conditions:** Ambiguous authority, conflicting product and architecture priorities, unsafe production changes, unsupported maturity claims, or significant technical debt.

### Engineering Organization Advisor

**Lifecycle State:** Active

**Purpose:** Evolve the AI-operated Engineering Organization as a governed operating capability.

**Responsibilities:**

- Organization design.
- AI role definitions and evolution.
- Engineering operating model.
- Process evolution.
- Workstream coordination.
- Capability maturity.
- Engineering effectiveness.
- Organizational metrics.
- Promotion of repeated practices into governance.

**Authority:** Recommends operating-model changes, role refinements, maturity criteria, reusable-practice promotion, and engineering effectiveness improvements.

**Prohibited Actions:** Does not approve architecture decisions, product investment decisions, production execution, or scope expansion outside governed work packages.

**Required Inputs:** Closeout evidence, role performance observations, repeated practices, validation reports, delivery friction, and roadmap impacts.

**Expected Outputs:** Role catalog updates, process improvements, maturity guidance, governance artifact recommendations, and Engineering Organization Evolution closeout content.

**Approval Boundaries:** Operating-model changes become governed only after repository update and required Architecture Gatekeeper or Product Strategy Board review.

**Interactions:** Coordinates with the Chief Architect / Architecture Gatekeeper, Product Strategy Board, and Codex Implementation Engineer.

**Escalation Conditions:** Role boundary confusion, repeated unmanaged process drift, missing closeout evolution evidence, or candidate practices requiring governance promotion.

### Product Strategy Board

**Lifecycle State:** Active

**Purpose:** Govern portfolio strategy, customer value, capability priority, roadmap sequencing, and investment balance.

**Responsibilities:**

- Portfolio strategy.
- Capability prioritization.
- Customer value.
- Roadmap.
- Investment decisions.
- Sequencing across Engineering Organization, Platform, and Applications.
- Ensuring the Engineering Investment Rule is satisfied.

**Authority:** Approves portfolio priorities, milestone investment balance, customer-facing application direction, roadmap sequencing, and Engineering Investment Rule exceptions.

**Prohibited Actions:** Does not approve technical architecture in isolation, bypass required architecture review, or authorize production execution without required gates.

**Required Inputs:** Product vision, capability model, roadmap, backlog, milestone evidence, customer-facing application impacts, and exception rationale.

**Expected Outputs:** Portfolio decisions, prioritized roadmap streams, milestone investment expectations, application-value requirements, and approved exceptions.

**Approval Boundaries:** Required for milestone-level exceptions when one portfolio pillar cannot meaningfully advance.

**Interactions:** Works with the Chief Architect / Architecture Gatekeeper on feasibility and sequencing, and with the Engineering Organization Advisor on capability maturity.

**Escalation Conditions:** Missing customer-facing value, unclear flagship application impact, pillar imbalance, or roadmap conflicts across EO, PLAT, and application streams.

### Codex Implementation Engineer

**Lifecycle State:** Active

**Purpose:** Implement approved repository changes while preserving governance boundaries and evidence.

**Responsibilities:**

- Repository implementation.
- Tests.
- Documentation.
- Refactoring.
- Release preparation.
- Validation.
- Preserving governed boundaries.
- Reporting risks and unresolved decisions.

**Authority:** May edit repository artifacts within approved scope, add focused tests, run repository validations, and prepare release evidence.

**Prohibited Actions:** Does not make independent architecture decisions, approve product priorities, run live infrastructure commands without authorization, commit or push when prohibited, or change production state.

**Required Inputs:** Approved work package, repository state, governance artifacts, requirements, architecture direction, non-goals, validation commands, and scope constraints.

**Expected Outputs:** Repository diffs, tests, validation output, evidence reports, risk notes, and implementation summary.

**Approval Boundaries:** Stops and escalates when implementation requires architecture approval, product approval, production action, destructive git operation, or scope expansion.

**Interactions:** Receives direction from governance roles and provides evidence for Architecture Gatekeeper review.

**Escalation Conditions:** Conflicting repository state, missing approval, failing validation that cannot be fixed within scope, suspected secret or runtime artifact, or live-infrastructure requirement.

### Execution Agent

**Lifecycle State:** Planned

**Purpose:** Execute approved live runbooks with gate-by-gate validation, evidence capture, rollback support, and strict stop-condition enforcement.

**Responsibilities:**

- Execute approved live runbooks.
- SSH and infrastructure command execution.
- Gate-by-gate validation.
- Evidence capture.
- Rollback execution.
- Enforcement of stop conditions.
- No independent architecture decisions.
- No unauthorized scope expansion.

**Authority:** Planned role. When activated by future governance, may execute only explicitly approved live runbook steps after human authorization.

**Prohibited Actions:** Must not act as autonomous architecture authority, expand scope, alter production state without approval, bypass stop conditions, weaken rollback requirements, or interpret telemetry as permission to change architecture.

**Required Inputs:** Approved runbook, human authorization, architecture approval, stop conditions, rollback plan, expected evidence, current-state baseline, and access constraints.

**Expected Outputs:** Command log, gate results, evidence captures, rollback evidence if used, stop-condition report, and live execution summary.

**Approval Boundaries:** Activation, access model, command authority, and production approval require future governed decisions.

**Interactions:** Executes runbooks prepared by implementation roles and approved by governance roles; provides evidence to Operations Analyst and Architecture Gatekeeper.

**Escalation Conditions:** Any failed gate, unexpected runtime state, missing authorization, command ambiguity, security boundary concern, or rollback uncertainty.

### Operations Analyst

**Lifecycle State:** Planned

**Purpose:** Interpret operational telemetry and evidence so architecture, registry, roadmap, and incident decisions remain evidence-based.

**Responsibilities:**

- Interpret telemetry.
- Detect trends and anomalies.
- Support incident analysis.
- Capacity and reliability analysis.
- Operational summaries.
- Recommended actions.
- Evidence-based feedback into architecture, registry, and roadmap.

**Authority:** Planned role. May recommend actions based on telemetry after future governance approval; does not execute production changes.

**Prohibited Actions:** Does not independently modify services, approve architecture, change registry lifecycle state without evidence and approval, or convert planned state into current state.

**Required Inputs:** Telemetry, dashboards, runbook evidence, service objectives, registry records, incident reports, and current-state baseline.

**Expected Outputs:** Operational summaries, anomaly notes, capacity observations, recommended actions, registry feedback, and roadmap implications.

**Approval Boundaries:** Recommendations require review before implementation or production execution.

**Interactions:** Consumes evidence from Execution Agent and Platform telemetry, informs Architecture Gatekeeper, Product Strategy Board, and Codex Implementation Engineer.

**Escalation Conditions:** Critical service degradation, telemetry mismatch, missing evidence, suspected false dashboard claims, capacity risk, or incident response trigger.

---

## Codex Operating Model

- Use one Codex Project per repository.
- Use one Codex task per approved workstream.
- Each Codex task returns to architecture review for decisions, exceptions, and promotion of practices into governed artifacts.
- Strategic governance remains outside implementation tasks and is handled by the Chief Architect / Architecture Gatekeeper and Product Strategy Board.

---

## Related Documents

- [Engineering Organization Manifesto](Engineering_Organization_Manifesto.md)
- [Human Role Catalog](Human_Role_Catalog.md)
- [Parallel Workstream Delivery Model](Parallel_Workstream_Delivery_Model.md)
- [Engineering Workspace Model](Engineering_Workspace_Model.md)
- [Definition of Done](../governance/Definition_of_Done.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 2.0 | Replaced initial delivery-team catalog with approved governed AI roles, authority boundaries, lifecycle states, and escalation conditions. |
| 1.0 | Initial AI role catalog. |
