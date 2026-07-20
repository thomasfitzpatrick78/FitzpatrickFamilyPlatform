# Platform Operational Evidence and Health Contract Specification

**Document Version:** 1.2

**Status:** Published Architecture Contract; Implemented: No

**Milestone:** PLAT-14.0A

---

## Purpose

This specification defines the technology-independent contracts and deterministic decision models for Platform Operational Evidence, reconciliation, and Operational Health.

It governs:

- Generic Operational Evidence Envelope v1.0.
- Container Evidence Profile v1.0.
- Reconciliation Contract v1.0.
- Operational Health Assessment Contract v1.0.
- Freshness, completeness, evidence-confidence, assessment-confidence, and initial container-health decision models.
- Provider-adapter, consumer, compatibility, versioning, security, and repository-first acceptance boundaries.

This specification does not implement runtime schemas, models, parsers, validators, adapters, policies, thresholds, providers, dashboards, APIs, or live infrastructure behavior.

---

## Contract Principles

1. Infrastructure Registry declared state remains authoritative.
2. Provider observations are untrusted inputs.
3. Operational Evidence is validated, normalized, provider-independent domain data.
4. One evidence record represents one normalized signal about one operational subject.
5. Reconciliation compares sources without mutating or collapsing them.
6. Health is derived from reconciled evidence and governed rules, never directly from providers or dashboards.
7. Healthy requires positive, current, complete, sufficiently confident proof.
8. Missing, stale, ambiguous, conflicting, incomplete, or unusable mandatory evidence never defaults to Healthy.
9. Confidence is deterministic and categorical; percentages and weighted scores are prohibited.
10. Raw provider payloads remain external supporting artifacts.
11. Contracts and policies are independently versioned and traceable.
12. The container profile is the only approved initial profile; future profiles require separate governance.

---

## Contract Layering and Versions

| Contract | Initial Version | Responsibility |
|----------|-----------------|----------------|
| Generic Operational Evidence Envelope | `1.0` | Stable cross-domain identity, signal, time, provenance, freshness, completeness, confidence, and findings. |
| Container Evidence Profile | `1.0` | Container-specific subject attributes, evidence categories, signals, values, and requirements. |
| Reconciliation Contract | `1.0` | Declared-versus-observed comparison, evidence selection, conflicts, and result. |
| Operational Health Assessment Contract | `1.0` | Deterministic health result, assessment confidence, reasons, findings, and validity. |
| Reconciliation Policy | Independently versioned | Subject mapping, evidence qualification, selection, freshness, and conflict behavior. |
| Health Policy | Independently versioned | Mandatory signals, criteria, precedence, thresholds, findings, and assessment validity. |

An evidence record identifies both `contract_version` and the independently governed `profile_version`. Reconciliation and health records identify their policy versions and all supporting evidence IDs.

---

## Generic Operational Evidence Envelope v1.0

### Identity

| Field | Requirement | Contract |
|-------|-------------|----------|
| `contract_version` | Required | Supported Generic Operational Evidence Envelope major and minor version. Initial value `1.0`. |
| `profile_type` | Required | Bounded profile identifier. Initial approved value `container`. |
| `profile_version` | Required | Independently versioned profile. Initial container value `1.0`. |
| `evidence_id` | Required | Stable unique identifier for this normalized one-signal evidence record. |
| `subject_id` | Required | Platform-owned stable subject identifier. |
| `subject_type` | Required | Bounded subject classification compatible with the selected profile. Initial value `container_service`. |
| `registry_reference` | Required | Repository-relative reference or stable registry identifier resolving to the authoritative declared-state record. |
| `environment` | Required | Governed environment classification; must not be inferred from a provider label without validation. |

`subject_id` is not a Docker container ID, provider label, cAdvisor name, OpenTelemetry resource identifier, Prometheus series identity, or other runtime reference.

For container evidence, the published but unimplemented Registry Container Identity Foundation contract supplies the declared host and governed Compose identity only after separate schema implementation and migration. Missing or invalid declared identity fails closed; an adapter cannot synthesize it from provider observations.

### Evidence Classification

| Field | Requirement | Contract |
|-------|-------------|----------|
| `evidence_type` | Required | Profile-governed semantic evidence category. |
| `signal_name` | Required | Canonical normalized signal name defined by the selected profile. |
| `value` | Required unless the profile explicitly represents absence | Value conforming to `value_type` and the signal's allowed values or range. |
| `value_type` | Required | One of `boolean`, `integer`, `decimal`, `text`, `state`, or `duration`. |
| `unit` | Required when the signal is dimensional; otherwise omitted | Canonical profile-approved unit. Provider-native units must be converted or rejected. |

Provider metric names and label names do not become canonical `signal_name` values without governed profile normalization.

### Time

| Field | Requirement | Contract |
|-------|-------------|----------|
| `observed_at` | Required | Time represented by the provider observation. |
| `collected_at` | Required | Time the observation was collected or retrieved. |
| `normalized_at` | Required | Time the provider adapter completed normalization. |
| `observation_window_start` | Required for windowed or aggregate signals | Inclusive start of the period represented by the value. |
| `observation_window_end` | Required for windowed or aggregate signals | Inclusive end of the represented period; must not precede the start. |

Timestamps are timezone-aware ISO 8601. Serialized repository examples use UTC with `Z`. An observation window may be omitted for point-in-time state or identity evidence. It is required for utilization, restart-occurrence, rate, pressure, or other values whose meaning depends on a period.

### Provenance

| Field | Requirement | Contract |
|-------|-------------|----------|
| `provider_type` | Required | Governed provider category, not a canonical domain semantic. |
| `provider_id` | Required | Stable identifier for the provider instance or configured source. |
| `provider_version` | Required when known; otherwise explicit finding | Provider software, API, or protocol version used to interpret the observation. |
| `adapter_version` | Required | Version of the normalization adapter and mapping rules. |
| `source_reference` | Required | Repository-safe reference to the supporting artifact or governed source location. |
| `runtime_subject_reference` | Conditional | Provider runtime identity retained only as provenance. |
| `collection_method` | Required | One of `direct`, `scraped`, `exported`, `inferred`, or `synthetic`. |

Collection methods mean:

| Method | Meaning |
|--------|---------|
| `direct` | Observation obtained directly from the authoritative runtime interface for that signal. |
| `scraped` | Observation retrieved by scraping a metrics or status endpoint. |
| `exported` | Observation transformed and exposed by an intermediary exporter or collector. |
| `inferred` | Observation derived from other signals under a governed rule. |
| `synthetic` | Observation produced by an intentional test or probe whose synthetic nature is explicit. |

Raw payloads are not embedded. `source_reference` points to a governed supporting artifact when retention is allowed.

### Freshness

| Field | Requirement | Contract |
|-------|-------------|----------|
| `freshness_status` | Required | One of `current`, `aging`, `stale`, or `unknown`. |
| `freshness_policy_id` | Required | Versioned policy used for the intended evidence use. |
| `maximum_age_seconds` | Required when the policy has a maximum age | Nonnegative policy input, not a provider assertion. |
| `evaluated_age_seconds` | Required when age is assessable | Nonnegative age calculated at normalization or governed reevaluation time. |

Stale evidence remains valid historical evidence but cannot satisfy a current-health requirement. `unknown` freshness cannot satisfy mandatory current-health evidence unless a future health policy explicitly permits it for a noncurrent use.

### Completeness

| Field | Requirement | Contract |
|-------|-------------|----------|
| `completeness_status` | Required | One of `complete`, `partial`, `missing_required_attributes`, or `not_assessable`. |
| `required_attributes` | Required | Profile- and evidence-type-derived attributes evaluated for this record. |
| `missing_attributes` | Required; may be empty | Required attributes that were not available or valid. |
| `coverage_reference` | Conditional | Reference to the governed coverage rule or evidence set when completeness depends on a wider inventory. |

Complete does not imply high confidence. Partial evidence may support explicitly noncritical conclusions but cannot satisfy a mandatory criterion unless the health policy says which omitted attributes are nonmandatory. `not_assessable` is never treated as complete.

### Confidence

| Field | Requirement | Contract |
|-------|-------------|----------|
| `evidence_confidence` | Required | One of `high`, `medium`, `low`, or `none`. |
| `confidence_reason_codes` | Required | Bounded deterministic factor references explaining the classification. |

Providers do not assert canonical confidence. The adapter or future domain service derives it from governed decision tables.

### Findings, Conflict, and Ambiguity

The smallest explicit finding model is a bounded `finding_codes` list on a successfully normalized record. Required initial codes are:

- `ambiguous_identity`
- `conflicting_evidence`
- `known_provider_limitation`
- `unsupported_normalization`
- `unresolved_provenance`

An adapter that cannot safely emit a canonical evidence record returns a structured normalization finding instead of a partial record. Findings are not arbitrary provider metadata and must not contain secrets or raw payloads.

---

## Container Evidence Profile v1.0

### Subject Attributes

| Field | Requirement | Boundary |
|-------|-------------|----------|
| `container_service_reference` | Required | Stable reference to the declared service or container-service identity in the Infrastructure Registry. |
| `host_reference` | Required for runtime evidence | Registry-linked host on which the runtime subject was observed or expected. |
| `runtime_name` | Conditional provenance | Provider runtime name; not canonical identity. |
| `runtime_container_id` | Conditional provenance | Provider runtime container identifier; prohibited as `subject_id`. |
| `image_reference` | Required for image evidence; optional otherwise | Normalized repository and tag or equivalent reference. |
| `image_digest` | Required only where the evidence type or policy claims immutable image identity | Digest value validated against the applicable format. |
| `orchestrator` | Optional | Bounded runtime coordination context when known. |
| `runtime_engine` | Required for runtime-provider evidence | Bounded runtime engine and version context when applicable. |

Subject attributes supplement the generic envelope. A provider adapter includes only attributes required or permitted for the evidence type.

| Evidence Category | Required Subject Attributes | Optional or Conditional Attributes |
|-------------------|-----------------------------|------------------------------------|
| Lifecycle evidence | `container_service_reference`; `host_reference` and `runtime_engine` for observed runtime state | `runtime_name`, `runtime_container_id`, `image_reference`, `image_digest`, `orchestrator` |
| Runtime health-check evidence | `container_service_reference`, `host_reference`, `runtime_engine` | `runtime_name`, `runtime_container_id`, `orchestrator` |
| Restart evidence | `container_service_reference`, `host_reference`, `runtime_engine` | `runtime_name`, `runtime_container_id`, `orchestrator` |
| Resource-pressure evidence | `container_service_reference`, `host_reference`, `runtime_engine` | `runtime_name`, `runtime_container_id`, `orchestrator`; image fields only when material to provenance |
| Telemetry-availability evidence | `container_service_reference`; provider identity from the generic envelope | Host and runtime attributes when the finding is scoped to one runtime instance |

### Approved Evidence Categories

The initial profile is limited to:

1. Lifecycle evidence.
2. Runtime health-check evidence.
3. Restart evidence.
4. Resource-pressure evidence.
5. Telemetry-availability evidence.

### Lifecycle Evidence

| Canonical Signal | Value Type | Allowed Values or Semantics | Required Profile Attributes |
|------------------|------------|-----------------------------|-----------------------------|
| `container.lifecycle.expected_state` | `state` | `expected`, `intentionally_inactive`, `excluded` | `container_service_reference`; declared-state provenance. |
| `container.lifecycle.observed_state` | `state` | `created`, `running`, `stopped`, `restarting`, `exited`, `missing` | `container_service_reference`, `host_reference`, `runtime_engine`; runtime references when present. |
| `container.image.reference` | `text` | Normalized image reference | `container_service_reference`, `image_reference`. |
| `container.image.digest` | `text` | Validated immutable digest | `container_service_reference`, `image_reference`, `image_digest`. |

`container.lifecycle.expected_state` is a Registry-derived declared-state projection, not provider-produced Operational Evidence. Reconciliation may consume Infrastructure Registry state directly without creating this evidence record. A provider adapter must never emit or override declared expectation.

`missing` is emitted only when a governed observation process can conclusively establish absence for the declared subject. Lack of observations alone is not conclusive absence.

### Runtime Health-Check Evidence

| Canonical Signal | Value Type | Allowed Values | Required Profile Attributes |
|------------------|------------|----------------|-----------------------------|
| `container.healthcheck.state` | `state` | `passing`, `failing`, `starting`, `unavailable`, `not_configured` | `container_service_reference`, `host_reference`, `runtime_engine`. |

`not_configured` is a positive fact about configuration, not evidence that the container is healthy. Whether a health check is mandatory is determined by the health policy.

### Restart Evidence

| Canonical Signal | Value Type | Allowed Values or Unit | Window Rule |
|------------------|------------|------------------------|-------------|
| `container.restart.count` | `integer` | Nonnegative count | Window optional only for a lifetime counter with explicit semantics. |
| `container.restart.occurred` | `boolean` | `true` or `false` | Observation window required. |

Restart severity thresholds are versioned health-policy inputs. This profile does not freeze arbitrary counts or durations.

### Resource-Pressure Evidence

| Canonical Signal | Value Type | Canonical Unit | Window Rule |
|------------------|------------|----------------|-------------|
| `container.cpu.utilization` | `decimal` | `ratio` | Observation window required. |
| `container.memory.utilization` | `decimal` | `ratio` | Observation window required. |
| `container.memory.limit` | `integer` | `bytes` | Window optional for a point-in-time configured limit. |
| `container.memory.pressure` | `state` | `normal`, `elevated`, `critical`, `unknown` | Observation window and governed threshold policy required. |

Provider percentages, cores, bytes, or other native forms must be normalized to the canonical unit or rejected with `unsupported_unit`.

### Telemetry-Availability Evidence

| Canonical Signal | Value Type | Allowed Values |
|------------------|------------|----------------|
| `container.telemetry.provider_availability` | `state` | `available`, `unavailable`, `degraded`, `unknown` |
| `container.telemetry.expected_signal_availability` | `state` | `available`, `missing`, `partial`, `unsupported`, `unknown` |
| `container.telemetry.identity_resolution` | `state` | `exact`, `weak`, `ambiguous`, `unresolved` |
| `container.telemetry.collection_coverage` | `state` | `complete`, `partial`, `none`, `not_assessable` |
| `container.telemetry.provider_limitation` | `state` | `none_known`, `applies`, `unknown` |

Telemetry-availability evidence describes the ability to observe. It does not itself prove the container's operating condition.

### Provider Independence

Docker API, Docker daemon metrics, cAdvisor, OpenTelemetry, Prometheus, or future providers may supply observations for these signals through separately implemented adapters. This profile does not define provider-specific schemas, metric names, labels, queries, or configuration.

---

## Reconciliation Contract v1.0

### Record Fields

| Field | Requirement | Contract |
|-------|-------------|----------|
| `reconciliation_id` | Required | Stable unique record identifier. |
| `contract_version` | Required | Reconciliation Contract version. Initial value `1.0`. |
| `policy_version` | Required | Reconciliation policy version applied. |
| `subject_id` | Required | Platform-owned subject identity. |
| `registry_reference` | Required | Authoritative declared-state reference. |
| `evidence_ids` | Required | All evidence considered, including evidence not selected. |
| `result` | Required | One canonical reconciliation outcome. |
| `reason_codes` | Required | Bounded reasons supporting the result. |
| `reconciled_at` | Required | Timezone-aware evaluation timestamp. |
| `unresolved_conflicts` | Required; may be empty | Bounded descriptions or references for unresolved conflicts. |
| `selected_evidence_ids` | Required; may be empty | Evidence that qualified under the policy. |

### Outcomes and Deterministic Behavior

| Condition | Result |
|-----------|--------|
| Declared subject and exact qualifying current observation agree | `matched` |
| Declared subject and no qualifying current evidence | `missing` |
| Observed subject has no declared registry subject | `unexpected` |
| Multiple plausible declared subjects match | `ambiguous` |
| Qualifying providers disagree on a material fact | `conflicting` |
| Correctly mapped evidence falls outside the applicable freshness policy | `stale` |
| Evidence type does not require declared-versus-observed comparison | `not_applicable` |

Canonical outcomes are `matched`, `missing`, `unexpected`, `ambiguous`, `conflicting`, `stale`, and `not_applicable`.

Reconciliation preserves registry and evidence facts, records evidence selection, and never mutates either source. It does not itself determine health.

---

## Operational Health Assessment Contract v1.0

### Record Fields

| Field | Requirement | Contract |
|-------|-------------|----------|
| `assessment_id` | Required | Stable unique assessment identifier. |
| `contract_version` | Required | Health Assessment Contract version. Initial value `1.0`. |
| `subject_id` | Required | Platform-owned subject identity. |
| `health_policy_version` | Required | Versioned health policy applied. |
| `reconciliation_id` | Required when reconciliation applies | Source reconciliation record. |
| `evidence_ids` | Required | Evidence supporting or constraining the assessment. |
| `health_status` | Required | One canonical health status. |
| `assessment_confidence` | Required | One of `high`, `medium`, `low`, or `none`. |
| `reason_codes` | Required | Deterministic bounded reasons for the result. |
| `critical_findings` | Required; may be empty | Findings material to required operating criteria. |
| `noncritical_findings` | Required; may be empty | Findings that do not prove critical failure. |
| `evaluated_at` | Required | Timezone-aware assessment time. |
| `valid_until` | Required for current-health claims | Time after which the assessment cannot be treated as current without reevaluation. |

### Canonical Statuses and Precedence

The decision sequence is:

1. If no governed evaluation record exists, status is `not_evaluated`.
2. If evaluation occurred but mandatory evidence is absent, stale, ambiguous, conflicting, incomplete, or has confidence `none`, status is `insufficient_evidence`.
3. If sufficient evidence proves a critical failure, status is `unhealthy`.
4. If sufficient evidence proves operation with a noncritical failure or material risk, status is `degraded`.
5. Only when all mandatory criteria have sufficient current evidence and pass is status `healthy`.

This is a decision sequence, not an ordinal severity scale. `insufficient_evidence` is not healthier or less healthy than `unhealthy`; it means the Platform cannot support the requested conclusion. Healthy is never a default.

---

## Freshness Decision Model

Freshness is policy-driven by subject type, signal, evidence use, and health policy. There is no global threshold.

Each freshness policy defines:

- Policy identifier and version.
- Applicable subject and signal.
- Intended use.
- Maximum age and any aging boundary.
- Whether an observation window is required.
- Evaluation time basis.
- Behavior when timestamps are missing, inconsistent, or future-dated.

Representative policy needs include:

| Evidence | Policy Characteristic |
|----------|-----------------------|
| Container lifecycle | Short maximum age for a current-health conclusion. |
| Resource utilization | Required recent observation window. |
| Image reference or digest | Longer permitted age where runtime identity remains reconciled. |
| Future backup evidence | Cadence based on separately governed backup objectives. |

The examples do not set thresholds. Threshold values require future governed implementation inputs and evidence.

---

## Completeness Decision Model

Completeness is derived from the evidence type, profile version, intended health rule, and coverage policy.

| Classification | Decision Rule |
|----------------|---------------|
| `complete` | Every attribute and coverage item required for the intended use is present and valid. |
| `partial` | Some evidence is usable, but one or more nonuniversally required attributes or coverage elements are absent. |
| `missing_required_attributes` | At least one attribute required for the evidence type or intended health rule is absent or invalid. |
| `not_assessable` | Available facts are insufficient to determine completeness. |

Complete does not imply high confidence. Partial evidence may support a noncritical conclusion only when the health policy identifies the missing elements as nonmandatory for that conclusion. Missing required attributes produce explicit findings. `not_assessable` is never treated as complete.

---

## Evidence Confidence Decision Table

Confidence factors are identity certainty, freshness, completeness, directness, provider suitability, corroboration, known provider limitations, and unresolved conflict.

| Level | Deterministic Conditions |
|-------|--------------------------|
| `high` | Exact registry identity; current; complete; direct observation; provider suitable for the signal; no unresolved limitation or conflict. |
| `medium` | Exact identity and current; evidence is indirect or partially complete only for noncritical attributes; provider remains suitable; no critical unresolved conflict. |
| `low` | Identity is weak or ambiguous but retained for explicit nonauthoritative use, evidence is aging, observation is inference-dependent, corroboration is weak, or a known provider limitation affects suitability. Low-confidence evidence cannot satisfy a mandatory critical criterion unless a future policy explicitly and safely allows it. |
| `none` | Evidence is missing, invalid, stale for the intended use, irreconcilably conflicting, unsupported by provider semantics, or lacks resolvable provenance. |

Rules:

- A critical ambiguous identity is treated as unusable for health and therefore `none` for that intended use, even if the historical record retains a lower-confidence classification for analysis.
- Corroboration may resolve a governed uncertainty but cannot override invalid, unsafe, or unsupported evidence.
- Providers do not supply this classification.
- Arithmetic averaging, weighted scores, and confidence percentages are prohibited.

---

## Assessment Confidence Decision Table

Assessment confidence is derived from the mandatory evidence supporting critical health criteria, reconciliation, and policy applicability.

| Level | Deterministic Conditions |
|-------|--------------------------|
| `high` | Every mandatory critical criterion is supported by high-confidence qualifying evidence; reconciliation is exact; no unresolved critical finding exists. |
| `medium` | Every mandatory criterion is supported, none is below medium, and any indirectness or partial completeness affects only noncritical detail. |
| `low` | A governed assessment can be made, but at least one mandatory nonfailure criterion relies on low-confidence evidence or material noncritical uncertainty remains. A policy must explicitly allow the conclusion. |
| `none` | Any mandatory criterion lacks usable evidence, has evidence confidence `none`, or depends on unresolved ambiguous or conflicting reconciliation. The resulting health status is normally `insufficient_evidence`. |

A health assessment cannot have higher confidence than the mandatory evidence supporting its critical health criteria. Nonmandatory evidence does not automatically lower assessment confidence unless the health policy makes it relevant. Confidence is not arithmetically averaged.

---

## Initial Container Health Decision Table

| Condition | Health Status | Required Reason Treatment |
|-----------|---------------|---------------------------|
| No governed evaluation record exists | `not_evaluated` | No assessment exists; consumers must not synthesize one. |
| Evaluation occurs with no current lifecycle evidence | `insufficient_evidence` | Missing mandatory lifecycle evidence. |
| Subject identity is ambiguous or materially conflicting | `insufficient_evidence` | Identity or reconciliation conflict. |
| Only cAdvisor-derived evidence affected by the known Docker 29/containerd identity limitation is available | `insufficient_evidence` | Known provider limitation and insufficient authoritative container identity. |
| Declared active container is conclusively absent through qualifying evidence | `unhealthy` | Critical declared-versus-observed failure. |
| Container exited unexpectedly | `unhealthy` | Critical lifecycle failure. |
| Required runtime health check is failing | `unhealthy` | Critical health-check failure. |
| Restart behavior crosses a governed critical threshold | `unhealthy` | Versioned threshold and window reference required. |
| Restart behavior crosses a governed noncritical risk threshold | `degraded` | Versioned threshold and window reference required. |
| Running container has partial loss of nonmandatory telemetry | `degraded` when operation remains sufficiently proven; otherwise `insufficient_evidence` | Health policy identifies whether the missing signal is mandatory. |
| Running, required health check passing, and all mandatory evidence current, complete, and sufficiently confident | `healthy` | Positive proof for every mandatory criterion. |
| Container is intentionally disabled, inactive, or excluded by declared policy | Excluded from active evaluation or `not_evaluated` | Must not default to `unhealthy` or `healthy`. |

Numeric restart, utilization, pressure, and timing thresholds are future versioned policy inputs. They are not frozen by PLAT-14.0A.

---

## Provider Adapter Contract

A provider adapter accepts provider-specific observations and returns either:

- One or more one-signal Operational Evidence records conforming to supported envelope and profile versions; or
- Structured normalization findings with no unsafe or misleading canonical record.

Representative normalization findings are:

- `subject_mapping_failed`
- `unsupported_signal`
- `missing_timestamp`
- `ambiguous_runtime_identity`
- `provider_limitation_applies`
- `unsafe_source_reference`
- `malformed_value`
- `unsupported_unit`
- `unsupported_provider_version`

Adapters must be independently testable through repository fixtures. They must not return authoritative health assessments, mutate declared state, grant approval, or hide unsupported input.

---

## Consumer Contract

### EO-14.4A

EO-14.4A may coordinate approved workflows referencing Operational Evidence, reconciliation, or Health Assessment artifact identifiers. It must not recalculate health, redefine Platform Operations contracts, expand authority, or treat an assessment as execution approval.

### Operations Analyst

The Operations Analyst may interpret health, confidence, freshness, trends, risks, and implications. It must preserve source traceability and must not modify evidence, reconciliation, or authoritative health assessments.

### Platform Health Dashboard and Future Dashboards

Dashboards may render health status, assessment confidence, evidence freshness, reason codes, findings, validity, and supporting references. They must not:

- Treat missing data as Healthy.
- Independently calculate authoritative health through PromQL, dashboard expressions, or presentation logic.
- Hide insufficient evidence, stale evidence, conflicts, or known provider limitations.

### Future APIs

Future APIs expose explicitly supported Platform Operations contract versions rather than provider-specific metrics. API consumers reject unsupported major versions and cannot infer approval or production authority from returned evidence.

### Future Automation

Future automation may reference Platform Operations outputs only after separate governance, EO-14.1A execution, EO-14.4A orchestration, activation, and live-change approvals. Evidence and health never self-authorize action.

---

## Compatibility and Versioning

Each contract, profile, reconciliation policy, and health policy is independently versioned.

| Change | Version Intent |
|--------|----------------|
| Incompatible field, meaning, required behavior, or bounded-value change | Major version. |
| Backward-compatible optional field or compatible bounded extension | Minor version. |
| Editorial clarification with no contract-semantic change | Document revision only unless a governed consumer requires a patch identifier. |

Consumers must:

- Reject unsupported major versions.
- Tolerate omitted optional fields.
- Reject unknown required semantics.
- Preserve original contract and policy versions in derived records.
- Never reinterpret provider-specific fields as canonical facts.

Every reconciliation and assessment remains traceable to contract versions, profile version, policy versions, evidence IDs, and evaluation time. PLAT-14.0A does not create a speculative migration framework.

---

## Security and Trust Requirements

- Provider observations are untrusted input.
- Raw payloads remain external and may not be committed when they contain secrets, credentials, tokens, private operational details, or prohibited runtime artifacts.
- Canonical evidence excludes credentials, tokens, environment variables, command arguments, and arbitrary provider metadata.
- `source_reference`, `registry_reference`, and supporting artifact references are repository-relative and traversal-free; absolute paths are prohibited.
- Timestamps, units, bounded states, identifiers, versions, values, and references require deterministic validation.
- Providers cannot assert canonical confidence or health.
- Declared-state linkage must resolve to an allowed Infrastructure Registry subject.
- Consumers cannot infer lifecycle approval, execution authority, or infrastructure-change permission from evidence.
- Repository fixtures are test evidence, not live compatibility evidence.

---

## Representative Trace Examples

### Exact Match and Healthy Assessment

| Stage | Representative Result |
|-------|-----------------------|
| Declared | Registry subject `svc-pihole-dns` is active and expected to run on the governed host. |
| Observed | Provider fixture reports one runtime lifecycle observation and one passing health-check observation. |
| Normalized | Two one-signal evidence records use the registry-linked Platform subject; runtime container ID remains provenance. |
| Reconciled | `matched`, with exact identity and both evidence IDs selected. |
| Evaluated | `healthy` only if the versioned health policy requires those signals and both are current, complete, and sufficiently confident. |
| Interpreted | Operations Analyst may describe current health and remaining nonmandatory telemetry limitations without changing the assessment. |

### Dashboard No-Data

| Stage | Representative Result |
|-------|-----------------------|
| Declared | Registry subject is active and expected. |
| Observed | No qualifying current lifecycle evidence is available. |
| Reconciled | `missing` or `stale`, depending on retained evidence. |
| Evaluated | `insufficient_evidence`, with assessment confidence `none`. |
| Rendered | Dashboard shows insufficient evidence and reasons; it does not show Healthy or infer a provider outage is a container failure. |

---

## Repository-First Acceptance Fixtures

A future implementation must include deterministic fixtures for:

- Exact registry match.
- Declared subject missing.
- Unexpected observed subject.
- Ambiguous identity.
- Conflicting providers.
- Stale evidence.
- Partial evidence.
- Malformed evidence.
- Known cAdvisor limitation.
- High-confidence Docker API lifecycle observation normalized through a fixture.
- Healthy container.
- Degraded container.
- Unhealthy container.
- Insufficient evidence.
- Not evaluated.
- Provider replacement producing the same canonical signal.
- Dashboard no-data represented as insufficient evidence rather than Healthy.

Fixture success does not prove:

- Live Docker compatibility.
- Live Prometheus availability or metric inventory.
- Restricted Docker API security or denial behavior.
- OpenTelemetry compatibility.
- cAdvisor compatibility.
- Metric cardinality or resource behavior.
- Pi-hole non-regression.
- Grafana rendering.
- Operational freshness under live failure.
- Live infrastructure readiness.

Those require separate Architecture Review, explicit human approval, controlled live gates, and operational evidence.

---

## Non-Goals

- Runtime code, schemas, parsers, validators, adapters, evaluation logic, APIs, or storage.
- Provider-specific contracts for Docker, Prometheus, Grafana, OpenTelemetry, or cAdvisor.
- A universal evidence plugin framework.
- Host, network, backup, certificate, or scheduled-task profiles.
- Numeric confidence scores or arbitrary health thresholds.
- Dashboard implementation or live monitoring changes.
- Execution, orchestration, automation, or production activation.
- Infrastructure Registry changes based on observations.

---

## Acceptance Criteria

This specification is ready for Architecture Gatekeeper review when:

- All four contracts have explicit version, ownership, and traceability fields.
- Evidence records are one-signal, provider-independent, and registry-linked.
- The container profile defines bounded initial categories and normalized signals without provider schemas.
- Reconciliation and health remain distinct deterministic steps.
- Freshness, completeness, and confidence have explicit decision models.
- `not_evaluated`, `insufficient_evidence`, `unhealthy`, `degraded`, and `healthy` are unambiguous.
- Provider adapters return evidence or structured findings, never health.
- Consumer restrictions prevent independent recalculation and no-data Healthy claims.
- Compatibility and security behavior are explicit.
- Repository fixture scope and live-proof limitations are disclosed.

---

## Related Documents

- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)
- [Container Operational Health Specification](Container_Operational_Health_Specification.md)
- [Infrastructure Registry v1.0 Specification](Infrastructure_Registry_v1.0_Specification.md)
- [Registry Container Identity Foundation Architecture](../architecture/Registry_Container_Identity_Foundation_Architecture.md)
- [Registry Container Identity Foundation Specification](Registry_Container_Identity_Foundation_Specification.md)
- [Platform Operations and Observability Specification](Platform_Operations_Observability_Specification.md)
- [Container Metrics Modernization Specification](Container_Metrics_Modernization_Specification.md)
- [Platform Health Dashboard Specification](Platform_Health_Dashboard_Specification.md)
- [Operations Analyst Specification](../engineering-organization/Operations_Analyst_Specification.md)
- [Docker 29 Container Metrics Compatibility Assessment](../architecture/Docker_29_Container_Metrics_Compatibility_Assessment.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Added the Registry Container Identity Foundation declared-host/Compose dependency and fail-closed provider boundary without changing contract version 1.0. |
| 1.1 | Clarified Registry-derived lifecycle expectation and linked the PLAT-14.1A specification-alignment baseline without changing contract version 1.0. |
| 1.0 | Initial PLAT-14.0A generic evidence, container profile, reconciliation, health, confidence, provider, consumer, and compatibility contracts. |
