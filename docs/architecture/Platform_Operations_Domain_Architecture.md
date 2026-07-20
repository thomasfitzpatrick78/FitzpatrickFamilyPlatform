# Platform Operations Domain Architecture

**Document Version:** 1.4

**Status:** Published Architecture; Implemented: No

**Milestone:** PLAT-14.0A

---

## Purpose

This document establishes Platform Operations as the governed bounded context for representing declared operational intent, normalized operational evidence, reconciliation, deterministic operational health, and advisory operational intelligence.

The architecture answers five separate questions:

1. What should exist?
2. What was observed?
3. What does the Platform currently believe is true after reconciliation?
4. What is the resulting operational condition under governed rules?
5. What may downstream operational intelligence infer or recommend?

PLAT-14.0A defines domain architecture and contracts only. It does not implement models, providers, adapters, health evaluation, dashboards, APIs, execution, orchestration, or live infrastructure behavior.

---

## Product and Customer Model

Platform Operations is a Shared Platform product domain that provides trustworthy, explainable operational state to people and governed consumers without binding them to a telemetry technology.

| Customer or Stakeholder | Need | Governed Output |
|-------------------------|------|-----------------|
| Platform Administrator | Determine whether declared Platform services are present and operating with sufficient evidence. | Reconciled state, health assessment, confidence, findings, and supporting references. |
| Operations Analyst | Interpret health, trends, risks, and improvement opportunities without changing authoritative facts. | Versioned evidence and health assessments suitable for advisory analysis. |
| Architecture Gatekeeper | Review whether operational claims are evidence-based, bounded, and safe to promote. | Traceable contracts, policies, reasons, and lifecycle evidence. |
| Platform Health Dashboard and future dashboards | Present governed operational outcomes without inventing health semantics. | Read-only assessment projections with confidence, freshness, and reasons. |
| Future Platform APIs and services | Consume stable operational semantics independent of providers. | Versioned provider-independent contracts. |
| Future household applications | Consume approved Platform operational summaries without coupling to runtime APIs. | Governed downstream views after separate product and architecture approval. |

The bounded context is distinct from the Engineering Organization, the Financial Platform, provider technologies, dashboard presentation, and future household applications.

---

## Bounded Context Scope

Platform Operations owns:

- Platform-owned operational subject identity linked to the Infrastructure Registry.
- The Generic Operational Evidence Envelope and approved domain profiles.
- Normalization boundaries between provider observations and Platform Operational Evidence.
- Reconciliation of declared state and qualifying evidence without source mutation.
- Deterministic Operational Health assessment under governed policies.
- Confidence, freshness, completeness, conflict, and reason semantics.
- Versioned consumer guarantees for operational evidence and health.

Platform Operations does not own:

- Infrastructure Registry declared-state authoring or lifecycle promotion.
- Telemetry-provider runtime behavior.
- Engineering execution contracts.
- Workflow orchestration.
- Dashboard rendering or presentation queries.
- Production authorization or infrastructure control.
- Operations Analyst recommendations or product and architecture decisions.

---

## Subdomains and Progression

```text
Expected
  -> Observed
  -> Reconciled
  -> Evaluated
  -> Interpreted

Declared State
  -> Operational Evidence
  -> Reconciliation
  -> Operational Health
  -> Operational Intelligence
```

| Subdomain | Primary Question | Responsibility | Authoritative Owner |
|-----------|------------------|----------------|---------------------|
| Declared State | What should exist? | Represent intended assets, services, lifecycle, ownership, dependencies, and monitoring readiness. | Infrastructure Registry. |
| Operational Evidence | What was observed? | Validate and normalize provider observations into provider-independent, one-signal evidence records. | Platform Operations contracts; future provider adapters produce conforming records. |
| Reconciliation | What does the Platform currently believe after comparison? | Compare declared state and qualifying evidence while preserving both sources. | Platform Operations reconciliation policy and record. |
| Operational Health | What is the resulting condition? | Apply deterministic policies to reconciled evidence and produce a health status with confidence and reasons. | Platform Operations health policy and assessment. |
| Operational Intelligence | What may be inferred or recommended? | Interpret assessments, trends, risks, and implications without changing evidence or health. | Operations Analyst and separately approved downstream intelligence. |

No downstream subdomain may silently overwrite the output or authority of an upstream subdomain.

---

## Authoritative Sources

| Concept | Authority | Boundary |
|---------|-----------|----------|
| Declared infrastructure and service state | Infrastructure Registry records | Operational evidence may identify mismatch but does not mutate registry records. |
| Provider observation | The identified provider and its supporting artifact | An observation is untrusted provider-originated input, not a Platform fact. |
| Platform Operational Evidence | A record conforming to an approved evidence-envelope and profile version | Providers cannot directly assert canonical confidence or health. |
| Reconciled state | A versioned reconciliation record produced under a governed policy | Reconciliation preserves sources and does not determine health. |
| Operational Health | A versioned health assessment produced under a governed policy | Healthy requires positive proof and is never a default. |
| Operational Intelligence | Reviewed interpretation or recommendation | Intelligence is advisory and cannot change authoritative evidence, health, architecture, lifecycle, or production state. |

---

## Ubiquitous Language

| Term | Definition |
|------|------------|
| Platform Operations | The bounded context that governs operational evidence, reconciliation, health, and downstream interpretation boundaries. |
| Operational Subject | A Platform-owned stable identity for the asset or service being evidenced, linked to an authoritative registry record. |
| Declared State | The expected state represented by the Infrastructure Registry. |
| Observation | Untrusted provider-originated input before Platform validation and normalization. |
| Provider | A technology or source that emits or exposes observations. |
| Provider Adapter | A bounded translator that validates provider observations and returns normalized evidence or structured findings. |
| Operational Evidence | Validated, normalized, provider-independent domain data representing one signal about one operational subject. |
| Evidence Type | The governed semantic category that determines required attributes and intended use. |
| Normalized Signal | A canonical signal name and bounded value whose meaning is independent of the provider's metric or field name. |
| Provenance | Traceability to provider, adapter, collection method, runtime identity, and supporting artifact. |
| Observation Window | The bounded period summarized by evidence when a point-in-time observation is insufficient. |
| Freshness | Policy-derived classification of whether evidence is timely for an intended use. |
| Completeness | Policy-derived classification of whether required evidence attributes and coverage are present. |
| Evidence Confidence | A deterministic classification of an evidence record's suitability based on governed factors. |
| Reconciliation | Deterministic comparison of declared state and qualifying evidence without source mutation. |
| Reconciled State | The recorded result of reconciliation, including selected evidence and unresolved conflicts. |
| Operational Health | A deterministic assessment derived from reconciled evidence and governed health rules. |
| Assessment Confidence | A deterministic classification of the support for a health assessment. |
| Operational Intelligence | Advisory interpretation of assessments, trends, risks, and implications. |
| Supporting Artifact | A repository-safe reference to externalized raw or detailed evidence; it is not embedded in the canonical record. |
| Health Policy | A versioned definition of mandatory criteria, precedence, thresholds, and reason codes for health evaluation. |
| Reconciliation Policy | A versioned definition of identity, selection, conflict, and freshness rules for reconciliation. |
| Container Evidence Profile | The independently versioned container-specific semantics layered over the Generic Operational Evidence Envelope. |

Observation and Operational Evidence are deliberately distinct. An observation becomes Operational Evidence only after validation, subject mapping, normalization, and governed confidence derivation.

---

## Subject Identity

Every canonical evidence record uses a Platform-owned `subject_id` linked by `registry_reference` to the authoritative Infrastructure Registry record.

For container-backed services, the published Registry Container Identity Foundation implementation defines and validates the exact declared host and Compose identity later consumed by reconciliation. No current record has migrated into eligibility. PLAT-14.1A cannot infer or repair missing Registry identity from providers, and no runtime observation may create or mutate the declared subject.

Provider identities are provenance only. Docker container IDs, runtime names, Prometheus labels, cAdvisor names, OpenTelemetry resource identifiers, and future provider identifiers must not become canonical Platform subject identifiers.

Identity ambiguity is explicit evidence. A provider adapter must return a structured finding when it cannot map an observation to one Platform subject. It must not guess, create a parallel inventory, or silently select one of several plausible registry records.

---

## Contract Layering

```text
Provider Observation
  -> Provider Adapter
  -> Generic Operational Evidence Envelope
       + Container Evidence Profile v1
  -> Reconciliation Contract
  -> Operational Health Assessment Contract
  -> Operations Analyst, Dashboard, API, or approved workflow
```

The generic envelope contains stable cross-domain identity, signal, time, provenance, freshness, completeness, confidence, and finding fields. The Container Evidence Profile defines container-specific evidence categories, attributes, normalized signals, and allowed values.

The generic envelope is not a universal plugin framework. Additional profiles require separate governed requirements, architecture review, and approval.

One canonical evidence record represents one normalized signal. Unrelated provider signals are not aggregated into one evidence record.

Raw provider payloads remain external supporting artifacts. The canonical contract contains repository-safe references and bounded findings, not arbitrary provider metadata or extensible raw objects.

---

## Provider Boundary

Docker API, Docker daemon metrics, cAdvisor, OpenTelemetry, Prometheus, and future telemetry technologies are replaceable provider or transport implementations.

A provider adapter may:

- Accept provider-specific observations as untrusted input.
- Validate timestamps, units, values, provenance, and supported provider versions.
- Resolve a runtime reference to a Platform subject under a governed mapping policy.
- Normalize supported observations into approved signals.
- Return structured findings when normalization cannot be completed safely.

A provider adapter may not:

- Create or change Infrastructure Registry records.
- Treat a runtime identifier as canonical subject identity.
- Embed raw provider payloads in canonical evidence.
- Assert evidence confidence directly from a provider claim.
- Return an authoritative health assessment.
- Grant approval, execution, orchestration, or production authority.

Prometheus remains the approved metrics transport and dashboard data source under ADR-007. It is not the authority for Platform Operational Evidence semantics or health rules.

---

## Consumer Boundary

- EO-14.1A owns engineering assignment, execution, validation, evidence, and completion-package semantics. It does not own Platform operational-health semantics.
- EO-14.4A may coordinate approved workflows that reference Platform Operations artifacts. It does not recalculate health or redefine contracts.
- The Operations Analyst may interpret assessments and recommend action. It does not modify evidence or authoritative health outcomes.
- Platform Health and future dashboards render governed outputs. Presentation queries must not become an independent health engine.
- Future APIs expose supported contract versions rather than provider-specific metrics.
- Future automation may act only after separate governance, execution, orchestration, activation, and live-change approval.

Missing dashboard data must never be rendered as Healthy.

---

## Lifecycle and Activation Boundaries

| Work Package or Capability | Lifecycle Position |
|----------------------------|--------------------|
| PLAT-14.0A | Domain architecture and contracts published at `c8f9bc3446cb1d5c23bf32232203109a7ff067f8`; not implemented or operational. |
| PLAT-14.1A | Specification published; Foundation schema/validation/migration framework implementation published; PLAT implementation remains blocked pending separate migration and repository implementation decisions. |
| EO-14.1A | Repository implementation published; Execution Agent unactivated. |
| EO-14.4A | Repository implementation published; automation unactivated. |
| Bravo and Charlie | Implementation unstarted. |
| Live infrastructure | Unauthorized. |

Repository publication of this architecture does not authorize implementation. Repository implementation, Architecture Review, controlled live deployment, evidence, reconciliation, operational validation, and release remain separate Engineering Lifecycle stages.

---

## Security and Trust Boundaries

- Provider observations are untrusted input.
- Raw payloads may contain credentials, tokens, environment variables, command arguments, paths, or sensitive operational metadata and must remain outside canonical records.
- Canonical evidence excludes credentials, tokens, arbitrary metadata, and secret-bearing fields.
- Supporting references must be repository-relative, traversal-free, and free of absolute or secret-bearing paths.
- Timestamps, values, units, enumerations, registry references, and contract versions require validation.
- Providers cannot authoritatively assert confidence, health, approval, or lifecycle state.
- Evidence consumers cannot interpret operational condition as authorization to execute, automate, deploy, or mutate infrastructure.
- Repository fixtures prove contract behavior only, not live compatibility or security.

Privileged telemetry integrations remain governed by the Privileged Infrastructure Integration Standard and require separate live denial proof and human approval.

---

## Repository-First Implementation Strategy

A future PLAT-14.1A repository implementation should begin with immutable contract models, strict parsing, deterministic validation, provider-neutral fixtures, decision-table tests, stable serialization, and read-only rendering. It must not require live Docker, SSH, Prometheus, Grafana, OpenTelemetry, cAdvisor, service activation, or infrastructure mutation to prove the domain architecture.

Repository fixtures are sufficient to prove:

- Contract and version behavior.
- Stable subject identity and registry linkage.
- Provider normalization equivalence.
- Reconciliation outcomes.
- Freshness, completeness, confidence, and health decision tables.
- Consumer handling of insufficient evidence and no-data conditions.

Fixtures cannot prove live provider compatibility, privileged-proxy denial behavior, cardinality, Pi-hole non-regression, Grafana rendering, operational freshness, or production readiness. Those remain future separately approved live gates.

---

## Relationship to PLAT-14.1A

Existing PLAT-14.1A telemetry scope is preserved and reframed as future provider implementation:

- Restricted Docker API Proxy: privileged provider boundary.
- OpenTelemetry Collector Docker Stats: prospective provider adapter input.
- Prometheus: approved transport and query boundary.
- Docker daemon metrics: optional future provider input.
- cAdvisor: limited provider subject to known compatibility findings.
- Grafana provisioning: presentation implementation that consumes governed outputs and must not define authoritative health.

PLAT-14.1A must implement against the published PLAT-14.0A contracts rather than embed provider-specific identity, metric names, confidence, or health semantics. The PLAT-14.1A Container Operational Health specification defines the aligned policy, identity, output, fixture, and lifecycle baseline; it does not authorize implementation.

---

## Non-Goals

- Production source code, runtime models, parsers, schemas, validators, CLI commands, or report generators.
- Provider adapters or provider-specific schemas.
- Docker, Prometheus, Grafana, OpenTelemetry, cAdvisor, SSH, network, host, or service access.
- Health or reconciliation execution.
- Persistence, databases, APIs, background workers, or model invocation.
- Execution Agent or Governed Automation Framework activation.
- Infrastructure Registry mutation or lifecycle promotion.
- Dashboard implementation or presentation redesign.
- Universal evidence plugins or speculative host, network, backup, certificate, or scheduled-task profiles.
- FFFA changes.
- PLAT-14.1A implementation or Milestone 14 closeout.

---

## Architecture Acceptance Criteria

PLAT-14.0A is ready for Architecture Gatekeeper review when:

- Platform Operations and its five subdomains are defined with authoritative ownership.
- Declared state, observation, operational evidence, reconciliation, health, and intelligence remain distinct.
- Stable subject identity is registry-linked and provider-independent.
- The generic evidence envelope and Container Evidence Profile v1 are independently versioned.
- Health, freshness, completeness, and confidence decisions are deterministic and avoid numeric scoring.
- Healthy requires current, complete, sufficient positive proof.
- Provider adapters and consumers cannot recalculate or assert authoritative health.
- Repository-first fixtures and future live-proof limits are explicit.
- PLAT-14.1A implementation remains blocked pending publication of its aligned specification and later separate repository implementation authorization.
- No implementation, activation, or live infrastructure work is introduced.

---

## Related Documents

- [Platform Operational Evidence and Health Contract Specification](../specifications/Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Container Operational Health Specification](../specifications/Container_Operational_Health_Specification.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Registry Container Identity Foundation Architecture](Registry_Container_Identity_Foundation_Architecture.md)
- [Registry Container Identity Foundation Specification](../specifications/Registry_Container_Identity_Foundation_Specification.md)
- [Platform Digital Twin Integrity Model](Platform_Digital_Twin_Integrity_Model.md)
- [Container Metrics Modernization Specification](../specifications/Container_Metrics_Modernization_Specification.md)
- [Platform Health Dashboard Specification](../specifications/Platform_Health_Dashboard_Specification.md)
- [Operations Analyst Specification](../engineering-organization/Operations_Analyst_Specification.md)
- [ADR-009 - Evidence Before Operational Health](decisions/ADR-009-Evidence-Before-Operational-Health.md)
- [ADR-010 - Declared Observed and Reconciled State](decisions/ADR-010-Declared-Observed-and-Reconciled-State.md)
- [ADR-011 - Generic Operational Evidence Envelope and Versioned Profiles](decisions/ADR-011-Generic-Operational-Evidence-Envelope-and-Versioned-Profiles.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.4 | Recorded publication of the Registry identity schema/validation/migration framework with no eligible migrated subject and PLAT-14.1A still blocked. |
| 1.3 | Recorded complete unpublished Registry identity schema/validation/migration framework with no eligible migrated subject and PLAT-14.1A still blocked. |
| 1.2 | Published the unimplemented Registry Container Identity Foundation prerequisite and no-provider-inference boundary. |
| 1.1 | Recorded PLAT-14.0A publication and the blocked PLAT-14.1A specification-alignment lifecycle. |
| 1.0 | Initial PLAT-14.0A Platform Operations bounded-context and domain architecture. |
