# ADR-011 - Generic Operational Evidence Envelope and Versioned Profiles

**Status:** Approved

**Date Approved:** July 2026

**Category:** Product Architecture

**Milestone:** PLAT-14.0A

**Baseline:** Published at `c8f9bc3446cb1d5c23bf32232203109a7ff067f8`

**Implemented:** No

---

## Context

Platform Operations needs stable evidence semantics across replaceable providers while remaining concrete enough to implement Container Operational Health. A single container-only schema would duplicate cross-domain identity, time, provenance, freshness, completeness, and confidence behavior if later evidence domains are approved. A universal plugin framework would overgeneralize before the Platform has proven a second evidence domain.

The Docker 29/containerd and cAdvisor experience also shows that provider metric names, labels, runtime identities, and support levels are not durable domain contracts.

---

## Decision

Platform Operational Evidence shall use:

1. A stable Generic Operational Evidence Envelope containing cross-domain identity, one-signal classification, time, provenance, freshness, completeness, confidence, and bounded findings.
2. Independently versioned domain profiles, beginning only with Container Evidence Profile v1.0.

One canonical evidence record represents one normalized signal. Provider-specific metric names and runtime identifiers remain normalization inputs or provenance. Raw provider payloads remain external supporting artifacts and are not embedded as arbitrary metadata.

Future profiles require separate governed requirements, architecture review, and approval.

---

## Rationale

- Creates a stable provider-independent contract without a universal framework.
- Reuses only genuinely cross-domain fields.
- Allows container semantics to evolve independently from the envelope.
- Makes provider replacement testable through equivalent canonical signals.
- Prevents raw provider metadata and runtime identity from leaking into the domain model.

---

## Alternatives Considered

### Provider-Specific Canonical Schemas

Define separate canonical Docker, cAdvisor, OpenTelemetry, and Prometheus evidence schemas.

Rejected because consumers would couple to providers and replacement would change authoritative domain semantics.

### Container-Only Monolithic Contract

Put cross-domain and container-specific fields in one versioned contract.

Rejected because stable evidence-envelope behavior could not evolve independently and future approved profiles would duplicate foundational semantics.

### Universal Evidence Plugin Framework

Create extensible payloads and plugin discovery for arbitrary future domains.

Rejected as speculative abstraction that would weaken bounded fields, security review, and profile governance.

### Generic Envelope with One Approved Profile

Create a narrow generic envelope and independently versioned Container Evidence Profile v1.0.

Selected because it balances stability, concrete semantics, security, and future controlled evolution.

---

## Consequences

### Positive

- Consumers can depend on stable cross-domain evidence fields.
- Container semantics remain explicit and independently versioned.
- Provider adapters can be replaced while fixture outputs remain equivalent.
- Raw provider payloads and secret-bearing metadata remain outside canonical contracts.

### Tradeoffs

- Consumers must validate both envelope and profile versions.
- Future profiles require their own governance and cannot rely on arbitrary extension fields.
- Some provider-native detail remains only in supporting artifacts.

---

## Compatibility Implications

Incompatible envelope or profile changes require a major version. Backward-compatible optional fields or bounded extensions use a minor version. Consumers reject unsupported major versions, tolerate omitted optional fields, and reject unknown required semantics.

Prometheus remains the approved dashboard metrics source under ADR-007, but Prometheus metric and label names are not promoted into canonical `signal_name` or `subject_id` values without governed normalization.

---

## cAdvisor and Dashboard No-Data Relationship

The known cAdvisor limitation is represented through bounded provider-limitation, identity, coverage, and confidence findings rather than a cAdvisor-specific canonical schema.

Dashboard no-data remains a consumer condition. It is resolved through evidence qualification and health assessment and cannot create a Healthy result.

---

## Implementation and Activation Boundary

This ADR approves architecture direction only. It does not implement schemas, models, parsers, adapters, provider integrations, migrations, dashboards, APIs, or runtime behavior. It does not authorize future profiles beyond Container Evidence Profile v1.0.

---

## Related Documents

- [Platform Operations Domain Architecture](../Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](../../specifications/Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Docker 29 Container Metrics Compatibility Assessment](../Docker_29_Container_Metrics_Compatibility_Assessment.md)
- [ADR-009 - Evidence Before Operational Health](ADR-009-Evidence-Before-Operational-Health.md)
- [ADR-010 - Declared Observed and Reconciled State](ADR-010-Declared-Observed-and-Reconciled-State.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial generic evidence envelope and independently versioned profile decision. |
