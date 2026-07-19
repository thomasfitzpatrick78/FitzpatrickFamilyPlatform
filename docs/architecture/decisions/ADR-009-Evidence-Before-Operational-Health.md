# ADR-009 - Evidence Before Operational Health

**Status:** Approved

**Date Approved:** July 2026

**Category:** Product Architecture

**Milestone:** PLAT-14.0A

**Baseline:** Pending publication

**Implemented:** No

---

## Context

Milestone 13 proved that a healthy cAdvisor scrape target was not equivalent to complete Docker-container observability. Docker 29 with the containerd-backed image store allowed cAdvisor to remain reachable while stable Docker-container identity and expected resource signals were incomplete.

Dashboard no-data behavior also creates a semantic risk: presentation availability, provider availability, and subject health are different facts. A dashboard or telemetry provider cannot safely infer operational health from its own data presence or absence.

PLAT-14.0A needs a provider-independent rule for how Platform Operational Health becomes authoritative.

---

## Decision

Operational Health shall be derived from validated, normalized Platform Operational Evidence through governed reconciliation and health policies.

Providers, provider adapters, Prometheus queries, dashboards, APIs, and Operations Analyst interpretation shall not directly assert or independently recalculate authoritative Platform Operational Health.

Healthy requires positive proof that every mandatory criterion has current, complete, sufficiently confident evidence. Missing, stale, ambiguous, conflicting, incomplete, or unusable mandatory evidence results in `insufficient_evidence`, not Healthy.

---

## Rationale

- Separates telemetry availability from subject condition.
- Prevents provider limitations from silently becoming health semantics.
- Preserves deterministic, explainable, versioned evaluation.
- Allows providers and presentation technologies to be replaced without redefining health.
- Makes no-data and known cAdvisor limitations explicit rather than optimistic.

---

## Alternatives Considered

### Provider-Owned Health

Allow Docker, cAdvisor, OpenTelemetry, or another provider to supply the authoritative health status.

Rejected because provider health semantics and coverage differ, provider replacement would change domain meaning, and a reachable provider can still provide incomplete subject evidence.

### Dashboard-Owned Health

Use PromQL, dashboard expressions, or panel no-data mappings as the authoritative evaluation layer.

Rejected because presentation logic is difficult to govern as a reusable domain contract and may convert missing data into misleading health claims.

### Operations-Analyst-Owned Health

Allow the Operations Analyst to determine health through interpretation.

Rejected because advisory intelligence must not replace deterministic evidence and health authority.

### Evidence-Before-Health

Normalize observations, reconcile them with declared state, and apply versioned health rules.

Selected because it preserves provider independence, traceability, deterministic behavior, and consumer separation.

---

## Consequences

### Positive

- Health is evidence-based and explainable.
- Missing evidence is represented honestly.
- Provider and dashboard replacement do not redefine authoritative health.
- Consumers share one governed status and reason model.

### Tradeoffs

- Additional contracts and explicit policies are required before PLAT-14.1A implementation.
- Health cannot be claimed until required evidence, reconciliation, and policy versions exist.
- Live provider proof remains necessary after repository implementation.

---

## Compatibility Implications

Existing Infrastructure Registry `health_status`, Prometheus metrics, Grafana panels, and Operations Analyst outputs are not silently reinterpreted as PLAT-14.0A health assessments. Explicit future mappings require approved contract and policy versions.

ADR-007 remains authoritative for the approved Prometheus observability stack and provider topology. ADR-009 governs how evidence becomes authoritative operational health above that topology.

---

## cAdvisor and Dashboard No-Data Relationship

The known cAdvisor Docker 29/containerd limitation demonstrates why a reachable provider cannot directly establish named-container health. Evidence affected by that limitation remains explicit and cannot satisfy mandatory container identity or lifecycle criteria without qualifying proof.

Dashboard no-data is a presentation condition. It may reflect missing or stale evidence, a provider problem, or a query problem; it does not independently prove either Healthy or Unhealthy. Governed evidence and health rules determine the authoritative result.

---

## Implementation and Activation Boundary

This ADR approves architecture direction only. It does not implement health models, policies, evaluators, adapters, dashboards, APIs, or runtime behavior. It does not start PLAT-14.1A, activate EO-14.1A or EO-14.4A, or authorize live infrastructure work.

---

## Related Documents

- [Platform Operations Domain Architecture](../Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](../../specifications/Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Docker 29 Container Metrics Compatibility Assessment](../Docker_29_Container_Metrics_Compatibility_Assessment.md)
- [Platform Health Dashboard Specification](../../specifications/Platform_Health_Dashboard_Specification.md)
- [ADR-007 - Governed Operations and Observability](ADR-007-Governed-Operations-and-Observability.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial evidence-before-operational-health decision. |
