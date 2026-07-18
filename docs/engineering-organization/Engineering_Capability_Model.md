# Engineering Capability Model

**Document Version:** 1.2

**Status:** Active

**Milestone:** EO-13.0

---

## Purpose

This document defines the capability model for the AI-operated Engineering Organization.

---

## Capabilities

| Capability | Description | Current Reference Implementation |
|------------|-------------|----------------------------------|
| Product and Portfolio Governance | Maintain product intent, portfolio priorities, and customer value traceability. | Governed docs under `docs/product`, `docs/portfolio`, and `docs/governance`. |
| Architecture Governance | Preserve architecture-first delivery and durable decision records. | ADRs, Architecture Backlog, and review-ready workstream outputs. |
| AI Roles and Responsibilities | Define active and planned AI roles, authority, prohibited actions, inputs, outputs, and escalation conditions. | AI Role Catalog. |
| Workstream Delivery | Execute scoped repository work through dedicated Codex chats. | One chat per approved workstream. |
| Governed Live Execution | Define future controlled live execution with human approval, runbooks, evidence, rollback, and stop conditions. | Execution Agent remains planned. |
| Operations Intelligence | Interpret telemetry and recommend evidence-based action without production authority. | Operations Analyst remains planned. |
| Validation and Evidence | Demonstrate readiness through deterministic tests and repository reports. | `platform-eap` validators and reports under `reports/engineering`. |
| Capability Maturity | Assess Engineering Organization maturity at milestone closeout or another governed cadence. | Engineering Organization Capability Maturity Model. |
| Registry Authority | Use registries as authoritative state where structured knowledge is required. | Infrastructure Registry under `registry/`. |
| Engineering Memory | Preserve durable knowledge in git-managed artifacts. | Markdown governance docs, ADRs, requirements, specs, reports, and registry records. |
| AI Collaboration Governance | Govern AI participant initialization, continuity, completion, stewardship, readiness validation planning, and collaboration-quality measurement. | EO-14.8B specification package under `docs/engineering-organization/ai-collaboration/`. |
| Practice Promotion | Evaluate repeated practices for promotion into governed artifacts. | Architecture review and documentation updates after evidence exists. |

---

## Capability Maturity

| Level | Meaning |
|-------|---------|
| Emerging | Practice exists in workstreams but is not yet governed. |
| Governed | Practice is documented and has clear ownership. |
| Validated | Practice has deterministic validation or evidence collection. |
| Reusable | Practice is proven across multiple milestones or repositories. |

---

## Related Documents

- [Engineering Organization Roadmap](Engineering_Organization_Roadmap.md)
- [Engineering Organization Backlog](Engineering_Organization_Backlog.md)
- [Engineering Memory Concept](Engineering_Memory_Concept.md)
- [AI Role Catalog](AI_Role_Catalog.md)
- [Engineering Organization Capability Maturity Model](Engineering_Organization_Capability_Maturity_Model.md)
- [Capability Model](../product/Capability_Model.md)
- [AI Collaboration Governance Specification](ai-collaboration/AI_Collaboration_Governance_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Added AI Collaboration Governance capability. |
| 1.1 | Added EO-13.1 role, live execution, operations intelligence, and maturity capabilities. |
| 1.0 | Initial Engineering Organization capability model. |
