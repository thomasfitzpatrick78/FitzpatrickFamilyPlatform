# Architecture Pattern Library

**Document Version:** 1.4

**Status:** Active

**Milestone:** EO-13.0

---

## Purpose

This starter library records proven architecture and delivery patterns that may be reused by the Engineering Organization.

---

## Promotion Criteria

A pattern may be added or promoted when:

- It has been used successfully in at least one governed workstream.
- Its value is supported by validation, review evidence, or repeated delivery experience.
- Its boundary and authority are clear.
- It does not create unnecessary coupling between repositories.

---

## Starter Patterns

| Pattern | Description | Evidence |
|---------|-------------|----------|
| Repository-Managed Governance | Durable governance lives in Markdown and structured repository artifacts. | Milestone 11 governance foundation. |
| Registry as Authority | Structured registries are authoritative for domains requiring consistent state. | Milestone 12 Infrastructure Registry. |
| Evidence-Based Readiness | Readiness is shown through tests, validators, and generated reports. | `platform-eap` validation suite. |
| Outcome Main Task with Bounded Specialists | One Owner-facing main task coordinates an accepted outcome; bounded read-heavy specialist lanes may run in parallel and one same-checkout writer remains accountable. | EO-15.2 governed operating model; effective only upon publication. |
| Architecture Review Return | Implementation chats return for review before decisions become durable. | EO-13.0 delivery model. |

---

## Candidate Pattern Under Evaluation

| Candidate | Current Evidence | Promotion Boundary |
|-----------|------------------|--------------------|
| Capability-First Operationalization | EO-14.8 governance and published, unactivated EO-14.1A execution and EO-14.4A orchestration controls precede PLAT-14.0A Platform Operations product architecture. The published PLAT-14.1A slice supplies first-consumer repository evidence using fixture-only EO contracts. | Not promoted. One fixture-only repository consumer does not prove repeatability, activation safety, or live operational value. A separate Architecture Gatekeeper evidence review and future governed workstream evidence are required before permanent lifecycle governance is considered. |

PLAT-14.0A strengthens the candidate by requiring product-domain architecture before provider implementation. It does not establish sufficient evidence for permanent Engineering Lifecycle governance.

---

## EO-15.2 Outcome-Task and Specialist Pattern

Upon governed publication, the earlier One Chat per Workstream starter pattern is superseded for EO-15.2-governed delivery. Use one Owner-facing main task for the accepted outcome, up to three bounded namespaced specialists for independent read-heavy lanes, and one same-checkout writer. Specialists run only from a parent turn in live read-only permission mode; workspace-write phases are serialized without subagents. Any later independent writer requires a dedicated worktree, branch, owner, path lease, and integration order.

---

## Related Documents

- [Engineering Capability Model](Engineering_Capability_Model.md)
- [Engineering Organization Roadmap](Engineering_Organization_Roadmap.md)
- [Architecture Decision Log](../architecture/Architecture_Decision_Log.md)
- [Shared Engineering Strategy](../portfolio/Shared_Engineering_Strategy.md)
- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.4 | Added EO-15.2 risk-tiered conditional authority and governed subagent adoption. |
| 1.3 | Recorded publication of the first-consumer PLAT-14.1A repository evidence while leaving Capability-First Operationalization unpromoted pending repetition and live evidence. |
| 1.2 | Recorded first-consumer PLAT-14.1A repository evidence while leaving Capability-First Operationalization unpromoted pending review, repetition, and live evidence. |
| 1.1 | Recorded Capability-First Operationalization as an unpromoted candidate informed by PLAT-14.0A. |
| 1.0 | Initial Architecture Pattern Library starter. |
