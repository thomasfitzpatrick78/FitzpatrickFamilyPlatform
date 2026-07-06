# Engineering Capability Model

**Document Version:** 1.0

**Status:** Active

**Milestone:** EO-13.0

---

## Purpose

This document defines the capability model for the AI Engineering Organization.

---

## Capabilities

| Capability | Description | Current Reference Implementation |
|------------|-------------|----------------------------------|
| Product and Portfolio Governance | Maintain product intent, portfolio priorities, and customer value traceability. | Governed docs under `docs/product`, `docs/portfolio`, and `docs/governance`. |
| Architecture Governance | Preserve architecture-first delivery and durable decision records. | ADRs, Architecture Backlog, and review-ready workstream outputs. |
| Workstream Delivery | Execute scoped repository work through dedicated Codex chats. | One chat per approved workstream. |
| Validation and Evidence | Demonstrate readiness through deterministic tests and repository reports. | `platform-eap` validators and reports under `reports/engineering`. |
| Registry Authority | Use registries as authoritative state where structured knowledge is required. | Infrastructure Registry under `registry/`. |
| Engineering Memory | Preserve durable knowledge in git-managed artifacts. | Markdown governance docs, ADRs, requirements, specs, reports, and registry records. |
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
- [Capability Model](../product/Capability_Model.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Engineering Organization capability model. |
