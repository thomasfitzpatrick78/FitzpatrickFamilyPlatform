# ADR-010 - Declared Observed and Reconciled State

**Status:** Approved

**Date Approved:** July 2026

**Category:** Product Architecture

**Milestone:** PLAT-14.0A

**Baseline:** Pending publication

**Implemented:** No

---

## Context

The Infrastructure Registry is the authoritative source for declared Platform assets, services, lifecycle state, ownership, dependencies, and monitoring readiness. Telemetry providers observe runtime facts that may be missing, stale, unexpected, ambiguous, conflicting, or inconsistent with declared state.

Collapsing declared and observed facts into one mutable status would allow runtime observations to create a parallel inventory or allow planned state to masquerade as runtime proof. The cAdvisor compatibility finding demonstrated that provider identity and availability can be incomplete even when a configured service and scrape target exist.

---

## Decision

Infrastructure Registry declared state, provider-originated observation, normalized Platform Operational Evidence, and Platform Operations reconciled state shall remain distinct concepts with separate authority.

Reconciliation shall compare declared state and qualifying evidence under a versioned policy, record selected evidence and unresolved conflicts, and produce one of `matched`, `missing`, `unexpected`, `ambiguous`, `conflicting`, `stale`, or `not_applicable`.

Reconciliation shall not mutate Infrastructure Registry records or Operational Evidence and shall not itself determine health.

---

## Rationale

- Preserves the Infrastructure Registry as declared-state authority.
- Prevents observability from creating an uncontrolled parallel inventory.
- Makes drift, unexpected subjects, ambiguity, conflicts, and staleness explicit.
- Retains source facts for review, correction, and future evidence.
- Keeps health evaluation deterministic and separate from state comparison.

---

## Alternatives Considered

### Telemetry as Current-State Authority

Treat the provider's runtime inventory as the authoritative Platform inventory.

Rejected because provider identity may be incomplete or incompatible, provider scope can change, and declared ownership and lifecycle intent would be lost.

### Registry Health Mutation During Collection

Update registry health or lifecycle fields directly whenever observations arrive.

Rejected because collection would silently become infrastructure governance and could overwrite reviewed declared state without reconciliation or approval.

### Read-Time Comparison Only

Let each dashboard or consumer compare declared and observed data independently.

Rejected because different consumers would create incompatible reconciliation and health meanings.

### Explicit Reconciliation Record

Preserve sources and create a separate, versioned comparison result.

Selected because it is traceable, deterministic, reusable, and compatible with repository-first validation.

---

## Consequences

### Positive

- Declared, observed, and believed current state remain explainable.
- Registry drift and provider limitations cannot be hidden by a single status field.
- Consumers share one reconciliation result and reason vocabulary.

### Tradeoffs

- Future implementations must retain evidence and reconciliation references.
- Registry correction and lifecycle promotion remain separate reviewed actions.
- Consumers must handle unexpected, ambiguous, conflicting, and stale outcomes.

---

## Compatibility Implications

Existing registry health values remain declared repository state and are not automatically converted into Operational Health Assessment records. Existing provider labels and Docker container identifiers remain provenance and cannot replace Platform subject identity.

The decision extends the Registry-Driven Platform Lifecycle without changing ADR-006 registry authority or ADR-007 provider topology.

---

## cAdvisor and Dashboard No-Data Relationship

The known cAdvisor Docker 29/containerd limitation produces explicit provider-limitation and identity findings. It cannot support an exact reconciliation for named Docker containers without qualifying corroboration.

Dashboard no-data is a presentation observation. It may indicate missing or stale qualifying evidence but does not directly prove a subject is missing or unhealthy.

---

## Implementation and Activation Boundary

This ADR approves architecture direction only. It does not implement reconciliation models, policies, registry mutation, provider adapters, dashboards, runtime behavior, or live connections. PLAT-14.1A remains blocked pending PLAT-14.0A publication and later alignment.

---

## Related Documents

- [Platform Operations Domain Architecture](../Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](../../specifications/Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Infrastructure Registry v1.0 Specification](../../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Platform Digital Twin Integrity Model](../Platform_Digital_Twin_Integrity_Model.md)
- [ADR-006 - Registry Driven Infrastructure Foundation](ADR-006-Registry-Driven-Infrastructure-Foundation.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial declared, observed, and reconciled-state separation decision. |
