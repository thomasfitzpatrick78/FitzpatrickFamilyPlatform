# Container Operational Health Specification

**Document Version:** 1.1

**Status:** Published Specification; Implementation Blocked

**Milestone:** PLAT-14.1A

**Lifecycle Stage:** Published; Repository Implementation Not Authorized

---

## Purpose

This specification defines the complete governed repository baseline required before PLAT-14.1A Container Operational Health implementation may be authorized.

Container Operational Health provides deterministic, explainable, repository-owned health assessments for declared container-backed Platform services by reconciling Infrastructure Registry state with canonical Platform Operational Evidence under versioned policies.

This document specifies product behavior, identity, policy, reconciliation, health, output, fixture, consumer, and future-gate contracts. It does not implement models, policy files, parsers, validators, CLI commands, adapters, dashboards, automation, or runtime behavior.

---

## Product and Customer Model

### Primary Customer

The primary customer is the Platform Administrator.

### Downstream Consumers

- Operations Analyst.
- Platform Health Dashboard.
- Future APIs.
- Future governed automation.
- Future household applications requiring Platform-status information.

### Product Promise

The capability answers:

- Which declared subjects were evaluated?
- Which subjects were excluded and why?
- Which evidence was accepted, rejected, stale, incomplete, ambiguous, or conflicting?
- How was runtime identity mapped to Registry identity?
- What reconciliation outcome occurred?
- What health result occurred?
- What assessment confidence was derived?
- Which policies, reason codes, and evidence produced the result?
- When does the assessment expire?

### Measurable Outcomes

- Every assessed subject has a valid Platform `subject_id` and `registry_reference`.
- Every assessment records the Generic Operational Evidence Envelope, Container Evidence Profile, reconciliation-policy, health-policy, and assessment-confidence-policy versions used.
- Every result contains deterministic reason codes and supporting evidence references.
- No `healthy` result is possible unless every mandatory qualifying condition passes.
- Differently shaped provider fixtures representing the same fact normalize to equivalent canonical signals.
- Repeated evaluation with identical inputs and evaluation time produces byte-stable canonical JSON and deterministic Markdown.
- Missing evidence, provider limitations, exclusions, conflicts, stale evidence, and expired assessments remain explicit.
- No provider metric, label, runtime container ID, query, or dashboard expression becomes authoritative health semantics.

### Explicit Non-Ownership

PLAT-14.1A does not own:

- Infrastructure Registry authoring or lifecycle promotion.
- Live telemetry collection.
- Privileged Docker or containerd access.
- Observability transport.
- Dashboard presentation.
- EO-14.1A execution semantics.
- EO-14.4A orchestration semantics.
- Operations Analyst interpretation.
- Remediation or infrastructure mutation.
- Runtime activation.

---

## Ownership Model

| Owner | Responsibility | Boundary |
|-------|----------------|----------|
| Infrastructure Registry | Stable subject identifiers; declared container-backed services; expected participation; host and service relationships; governed container identity attributes. | Does not monitor, normalize evidence, reconcile, or evaluate health. |
| PLAT-14.0A Platform Operations | Generic evidence envelope; Container Evidence Profile; reconciliation and health semantics; freshness, completeness, confidence, provenance, and consumer contracts. | Defines domain contracts, not implementation or provider topology. |
| PLAT-14.1A Core | Container-profile validation; Registry-linked identity resolution; policy validation and application; reconciliation; deterministic health evaluation; JSON objects; Markdown projection; repository fixture validation. | Does not collect live observations or operate providers. |
| Future provider adapters | Provider observation parsing; provider-version support; mapping to canonical signals; normalization findings. | Never calculate authoritative health or mutate Registry state. |
| EO-14.1A | Governed engineering assignment, execution, validation, evidence, and completion contracts. | Does not define Platform Operational Evidence or health. |
| EO-14.4A | Governed workflow orchestration and human-review transition proposals. | Does not execute or calculate health. |
| Operations Analyst | Interprets assessments and recommends actions. | Does not change evidence or recalculate health. |
| Platform Health Dashboard | Renders governed outputs. | Does not calculate authoritative health through queries or presentation logic. |

Production provider adapters are outside the first PLAT-14.1A implementation. The first slice may contain test-scoped fixture translators only.

---

## Infrastructure Registry Container Identity Design

### Authority

The Infrastructure Registry record ID is the Platform-owned stable `subject_id`. PLAT-14.1A must not create a parallel container inventory or derive a stable subject ID from runtime data.

The existing `service` and `planned_service` record types remain authoritative. The published, unimplemented Registry Container Identity Foundation selects a bounded optional `container_*` field set on those records; no independent container record or parallel inventory is permitted. A later separately authorized schema and migration package must implement and validate the contract before PLAT-14.1A can evaluate any subject.

### Proposed Registry-Owned Attributes

| Attribute | Requirement | Contract |
|-----------|-------------|----------|
| `container_identity_contract_version` | Required when the extension is present | Versions the bounded Registry extension. |
| Record `id` | Existing required field | Becomes canonical Platform `subject_id`; no duplicate subject identifier is introduced. |
| `container_participation` | Required | One of `active`, `intentionally_inactive`, `excluded`, or `not_applicable`; replaces an ambiguous boolean. |
| `container_host_reference` | Required for active evaluation | Must resolve to the governed host and agree with Registry host dependencies. |
| `compose_project` | Required when Compose manages the subject | Exact governed Compose project value. |
| `compose_service` | Required when Compose manages the subject | Exact governed Compose service value. |
| `governed_runtime_name` | Optional fallback | Exact runtime name allowed only with host-scoped uniqueness proof. |
| `health_check_requirement` | Required | One of `required`, `optional`, or `not_applicable`. |
| `container_health_policy_reference` | Required for active evaluation | Repository-relative reference to the approved container-health policy set. |
| `expected_image_reference` | Optional | Expected image repository and tag or equivalent identity. |
| `expected_image_digest` | Optional | Immutable expected image identity; corroboration only for runtime matching. |
| `container_identity_evidence` | Required for migrated container-backed subjects | Governed repository evidence supporting the declaration. |
| `participation_reason` and review reference | Required where specified for inactivity or exclusion | Bounded reviewed reason without duplicating personal approval identity. |

These are schema-design requirements only. This package does not modify the active Registry schema or records.

### Pi-hole Migration Expectation

The existing `svc-pihole-dns` record remains the canonical subject. Repository evidence confirms its container-backed role, Beelink host, runtime-name candidate, and Compose path, but does not yet establish its exact Compose project/service keys, approved health-check requirement, or implemented policy reference. Those values require later reviewed evidence and cannot be inferred. Its runtime container ID must never become the subject ID.

Existing records without the new attributes remain valid Infrastructure Registry v1.0 records. They are not eligible for authoritative PLAT-14.1A evaluation until migrated and validated. The migration must be additive, reviewable, and backward compatible with existing Registry consumers.

No health assessment is silently written into Registry `health_status`. A future Registry field may reference a reviewed latest assessment, but the assessment remains a separate artifact and the Registry remains declared-state authority.

---

## Identity Matching Hierarchy

Matching applies in this precedence order:

1. Exact Platform `subject_id` and `registry_reference` resolving to one Registry record.
2. Exact governed subject, host, Compose project, and Compose service tuple.
3. Exact governed runtime name plus host only when uniqueness is proven by policy.
4. Image reference or digest as corroboration only.
5. Runtime container ID as provenance only.
6. Provider labels and resource attributes as adapter inputs only.
7. Fuzzy, suffix, substring, or partial name matching is prohibited for authoritative identity.

Name-only matching cannot produce high-confidence identity. If more than one subject is plausible, the result is `ambiguous`. If no subject is safely resolvable, the adapter returns a normalization finding rather than inventing evidence.

### Identity Scenarios

| Scenario | Deterministic Treatment |
|----------|-------------------------|
| Container recreation changes runtime ID but preserves the exact governed tuple | `matched`; the new runtime ID is provenance. |
| Multiple containers have similar names | `ambiguous`; no authoritative selection. |
| Compose service is renamed without Registry change | Existing subject is `missing`; new observation is `unexpected` or `ambiguous`. |
| Metrics remain after a container is removed | Evidence becomes `stale`; it cannot prove current state. |
| Active declared subject has no qualifying observation | Reconciliation `missing`; health `insufficient_evidence`. |
| Direct complete inventory proves an active subject is absent | Reconciliation `missing` with conclusive-absence reason; health may be `unhealthy`. |
| Observation has no Registry subject | `unexpected`; no canonical assessed subject is created. |
| cAdvisor identity cannot map reliably | Provider finding and `ambiguous` or no evidence record. |

---

## Container Evidence Profile v1.0 Alignment

Declared expectation originates in the Infrastructure Registry. The published `container.lifecycle.expected_state` signal is interpreted only as a Registry-derived projection with declared-state provenance; it is not provider-produced Operational Evidence and is not required when reconciliation consumes Registry state directly.

All successfully normalized evidence is one-signal, Registry-linked, versioned, and governed by the Generic Operational Evidence Envelope v1.0 and Container Evidence Profile v1.0.

### First-Slice Signals

| Signal | Value Contract | Time and Unit | Mandatory for `healthy` | Independent `unhealthy` Proof | Confidence and Reason Treatment |
|--------|----------------|---------------|-------------------------|-------------------------------|---------------------------------|
| `container.lifecycle.observed_state` | `state`: `created`, `running`, `stopped`, `restarting`, `exited`, `missing` | Point observation; no window required; lifecycle freshness policy | Yes; must be current and `running` | `exited` and conclusively established `missing`; `stopped` only when active operation is expected | Missing/stale -> `LIFECYCLE_EVIDENCE_MISSING`; ambiguity -> `IDENTITY_UNRESOLVED`. |
| `container.healthcheck.state` | `state`: `passing`, `failing`, `starting`, `unavailable`, `not_configured` | Point observation; health-check freshness policy | Conditional on Registry requirement | `failing` when required | Required unavailable/not configured cannot prove Healthy. Optional not configured is neutral. |
| `container.restart.count` | Nonnegative `integer` | Lifetime counter only when semantics and collection baseline are explicit; otherwise window required | No in v1 | No in v1 | Advisory; no numeric threshold is active. |
| `container.restart.occurred` | `boolean` | Observation window required | No in v1 | No in v1 | Advisory until restart thresholds are approved. |
| `container.cpu.utilization` | `decimal`, canonical unit `ratio` | Observation window required | No | No in v1 | Advisory; stale evidence receives `RESOURCE_EVIDENCE_STALE`. |
| `container.memory.utilization` | `decimal`, canonical unit `ratio` | Observation window required | No | No in v1 | Advisory. |
| `container.memory.limit` | Nonnegative `integer`, unit `bytes` | Point observation allowed | No | No | Supporting context. |
| `container.memory.pressure` | `state`: `normal`, `elevated`, `critical`, `unknown` | Observation window and resource policy required | No | No in v1 | Current `critical` with at least medium confidence produces `degraded`. |
| `container.telemetry.provider_availability` | `state`: `available`, `unavailable`, `degraded`, `unknown` | Point observation; telemetry freshness policy | No, when another provider supplies qualifying mandatory evidence | Never | Observation quality only; loss does not prove service failure. |
| `container.telemetry.expected_signal_availability` | `state`: `available`, `missing`, `partial`, `unsupported`, `unknown` | Current qualification | Yes for each mandatory signal | Never | Missing mandatory signals -> `MANDATORY_TELEMETRY_PARTIAL` or `TELEMETRY_UNAVAILABLE`. |
| `container.telemetry.identity_resolution` | `state`: `exact`, `weak`, `ambiguous`, `unresolved` | Current identity-policy result | `exact` required | Never | Weak identity is at most medium evidence confidence; ambiguous/unresolved is unusable for health. |
| `container.telemetry.collection_coverage` | `state`: `complete`, `partial`, `none`, `not_assessable` | Current coverage-policy result | Complete coverage of the mandatory set required | Never | Partial mandatory coverage -> insufficient evidence; partial advisory coverage is finding-only in v1. |
| `container.telemetry.provider_limitation` | `state`: `none_known`, `applies`, `unknown` | Provider/version scoped | No active limitation may affect mandatory evidence | Never | Material limitation disqualifies affected evidence and emits `PROVIDER_LIMITATION_APPLIES`. |

Every first-slice signal used in an assessment must carry the exact Registry `subject_id` and `registry_reference`, a timezone-aware observation time, source and provider provenance, envelope/profile versions, freshness, completeness, and evidence confidence. A provider-level observation that cannot be linked exactly to the evaluated subject may be retained as a normalization finding but cannot become qualifying subject evidence.

Signal-specific completeness is:

| Signal | Complete When |
|--------|---------------|
| `container.lifecycle.observed_state` | One allowed state, observation time, exact Registry linkage, and qualifying source provenance are valid. |
| `container.healthcheck.state` | One allowed state, observation time, exact Registry linkage, and the applicable Registry health-check requirement are valid. |
| `container.restart.count` | Nonnegative integer, explicit lifetime/reset semantics, observation time, and exact Registry linkage are valid. |
| `container.restart.occurred` | Boolean value, bounded window start and end, and exact Registry linkage are valid. |
| `container.cpu.utilization` | Finite nonnegative ratio, bounded window, exact Registry linkage, and explicit adapter semantics for host/core normalization are valid. No numeric health threshold is defined in v1. |
| `container.memory.utilization` | Finite nonnegative ratio, bounded window, exact Registry linkage, and explicit adapter semantics for the governing limit are valid. No numeric health threshold is defined in v1. |
| `container.memory.limit` | Nonnegative integer bytes, observation time, and exact Registry linkage are valid; zero must be explicitly documented as unlimited or unknown by the adapter rather than assumed. |
| `container.memory.pressure` | One allowed state, bounded observation window, resource-policy reference, and exact Registry linkage are valid. |
| `container.telemetry.provider_availability` | One allowed state, observation time, provider identity/version, evaluated subject scope, and exact Registry linkage are valid. |
| `container.telemetry.expected_signal_availability` | One allowed state, exact mandatory/advisory signal set, observation time, and exact Registry linkage are valid. |
| `container.telemetry.identity_resolution` | One allowed state, matching-policy reference, considered identifiers, observation time, and exact Registry linkage for `exact` or `weak` are valid; ambiguous/unresolved results remain findings. |
| `container.telemetry.collection_coverage` | One allowed state, expected and observed signal sets, observation time, and exact Registry linkage are valid. |
| `container.telemetry.provider_limitation` | One allowed state, provider/version, affected signal set, limitation reference, observation time, and exact Registry linkage are valid. |

Missing a listed element produces `missing_required_attributes` completeness for that intended use. Additional nonmandatory context may be absent while evidence remains `partial`; `not_assessable` is used when the available record cannot establish which completeness rule applies. Units are `none` for state and boolean signals, `count` for restart count, `ratio` for utilization, and `bytes` for memory limit.

Restart-rate semantics are not part of Container Evidence Profile v1.0. Adding a canonical rate requires separately reviewed profile-version treatment.

Provider metric names, label keys, resource attributes, and dashboard expressions remain outside the canonical signal contract.

---

## Versioned Policy Architecture

### Conceptual Location

Future machine-readable policies belong under:

```text
platform/operations/container-health/policies/
```

This package defines their schemas and initial governed values in documentation only. It does not create runtime policy files.

### Common Policy Header

Every future policy artifact must contain:

| Field | Requirement |
|-------|-------------|
| `policy_id` | Stable bounded identifier. |
| `policy_version` | Semantic version. Initial version `1.0`. |
| `status` | One of `draft`, `active`, `retired`. Assessments may use only `active`. |
| `compatible_contract_versions` | Supported Generic Operational Evidence Envelope versions. Initial value `1.0`. |
| `compatible_profile_versions` | Supported Container Evidence Profile versions. Initial value `1.0`. |
| `purpose` | Bounded policy purpose. |
| `approval_authority` | Architecture Gatekeeper and Platform Administrator. |
| `effective_at` | Timezone-aware activation time after publication. |
| `supersedes` | Prior policy reference or null. |

Unknown fields, unsupported versions, missing references, contradictory rules, negative or nonfinite durations, invalid thresholds, and incompatible contract/profile versions fail closed.

### Policy Artifact Set

| Artifact | Policy ID and Initial Version | Required Content |
|----------|-------------------------------|------------------|
| Policy manifest | `container-policy-set` `1.0` | Exact references to one compatible instance of every required policy; manifest version; approval and effective status. |
| Container reconciliation | `container-reconciliation` `1.0` | Matching precedence, uniqueness rule, selection order, conclusive-absence requirements, conflict behavior, rejected-evidence retention. |
| Lifecycle freshness | `container-lifecycle-freshness` `1.0` | Aging boundary, maximum age, timestamp requirements, future timestamp behavior. |
| Health-check freshness | `container-healthcheck-freshness` `1.0` | Aging boundary, maximum age, requirement interaction. |
| Restart window | `container-restart-window` `1.0` | Evidence semantics; v1 advisory status; no active degradation or failure threshold. |
| Resource pressure | `container-resource-pressure` `1.0` | Advisory treatment; critical memory-pressure degradation rule; no CPU/memory numeric threshold. |
| Telemetry availability | `container-telemetry-availability` `1.0` | Mandatory coverage set, identity resolution, provider limitation, provider-loss treatment. |
| Container health | `container-health` `1.0` | Status precedence, mandatory criteria, reason codes, health-check rules, exclusion treatment. |
| Assessment confidence | `container-assessment-confidence` `1.0` | Minimum confidence, aggregation behavior, caps from conflicts and limitations. |

Policy-specific required fields and initial bounded values are:

| Policy | Required Fields and Initial Values | Validation Rules |
|--------|------------------------------------|------------------|
| Manifest | `manifest_id=container-policy-set`; `manifest_version=1.0`; exact references to reconciliation, lifecycle freshness, health-check freshness, restart window, resource pressure, telemetry availability, health, and assessment-confidence policy `1.0`. | Exactly one reference per required policy; no duplicate IDs; every referenced policy active, compatible, and mutually consistent. |
| Reconciliation | Ordered `match_hierarchy` equal to the seven approved identity steps; `allowed_outcomes` equal to `matched`, `missing`, `unexpected`, `ambiguous`, `conflicting`, `stale`, `not_applicable`; `conclusive_absence_requires` current complete exact-identity population inventory; `retain_considered_evidence=true`. | Fuzzy matching denied; image and runtime ID cannot be primary identity; conflicts cannot be silently selected; unknown outcome denied. |
| Lifecycle freshness | `aging_after_seconds=30`; `maximum_age_seconds=60`; `timestamp_required=true`; `future_timestamp_behavior=invalid`. | Durations are finite positive integers; aging is less than maximum; a timestamp after evaluation time is invalid in v1; stale evidence cannot satisfy Healthy. |
| Health-check freshness | `aging_after_seconds=30`; `maximum_age_seconds=60`; `timestamp_required=true`; `future_timestamp_behavior=invalid`; Registry requirement values `required`, `optional`, `not_applicable`. | Same duration rules as lifecycle; requirement must resolve exactly; missing required check fails closed. |
| Restart window | `mode=advisory`; accepted signals `container.restart.count` and `container.restart.occurred`; `health_thresholds=[]`; reserved code `RESTART_THRESHOLD_EXCEEDED`; bounded-window timestamps required for `occurred`. | Negative count, invalid window, inferred rate, or active threshold is invalid in v1; reserved code cannot be emitted. |
| Resource pressure | `mode=advisory_with_degradation`; CPU and utilization thresholds absent; `critical_memory_pressure_result=degraded`; `minimum_qualifying_confidence=medium`; `unhealthy_rules=[]`. | Nonfinite/invalid units denied; numeric health thresholds denied in v1; only current exact-identity pressure evidence can degrade. |
| Telemetry availability | Mandatory set includes lifecycle observed state plus health-check state when Registry declares it required; identity must be `exact`; mandatory coverage must be `complete`; material provider limitation disqualifies affected evidence. | Provider loss never independently proves Unhealthy; unresolved/ambiguous identity and partial mandatory coverage fail closed. |
| Container health | `evaluation_order` equal to `not_evaluated`, `insufficient_evidence`, `unhealthy`, `degraded`, `healthy`; reason catalog `1.0`; Healthy criteria equal to the mandatory proof in this specification. | Unknown status/reason denied; earlier applicable result wins; Healthy cannot be defaulted or inferred from provider reachability. |
| Assessment confidence | Allowed values `high`, `medium`, `low`, `none`; `healthy_minimum=medium`; no arithmetic scoring; assessment cannot exceed the lowest confidence of mandatory supporting evidence; unresolved critical conflict produces `none`. | Every classification must cite qualifying evidence and policy reasons; unknown value, percentage, score, or untraceable uplift denied. |

The manifest identifies one internally compatible evaluated policy set. Assessments retain the manifest ID/version and every constituent policy ID/version.

### Compatibility and Approval

- An outcome-changing change always creates a new policy version.
- Incompatible meaning, required-field, or precedence changes require a major version.
- Backward-compatible bounded additions require a minor version.
- Editorial changes that cannot change evaluation remain document revisions.
- Architecture Gatekeeper approval is required before a policy becomes `active`.
- Provider adapters and consumers cannot select, modify, or override policies.

---

## Initial Governed Policy Values

These values are proposed for Architecture Gatekeeper approval. They are supported by the repository's existing 15-second Prometheus scrape and prepared OTel collection intervals and 30-second dashboard refresh interval. Live provider validation must confirm or revise them before operational use.

### Mandatory Healthy Evidence

`healthy` requires:

- Registry subject participation `active`.
- Exact Registry-linked identity.
- Current lifecycle evidence equal to `running`.
- Complete coverage of every mandatory signal.
- Evidence confidence of at least `medium` for every mandatory signal.
- Required health check equal to `passing` where Registry policy declares it required.
- No unresolved critical finding or material conflict.
- No provider limitation affecting mandatory evidence.
- Assessment evaluation before `valid_until`.

The minimum is `medium`, not `high`. High evidence confidence requires direct observation under the published contract, while a governed exported or scraped provider path may remain suitable and exact but medium-confidence. Requiring high would couple Healthy to a collection method and undermine the approved transport-independent architecture. Exact identity and complete mandatory coverage remain non-negotiable.

### Provisional Freshness Values

| Evidence or Assessment | Aging Boundary | Maximum Current Age / Validity | Rationale and Review Trigger |
|------------------------|----------------|--------------------------------|------------------------------|
| Lifecycle evidence | 30 seconds | 60 seconds | Two and four expected 15-second collection intervals. Revalidate during first live provider inventory. |
| Health-check evidence | 30 seconds | 60 seconds | Matches lifecycle cadence; revise if runtime health-check cadence is slower and proven. |
| Telemetry-availability evidence | 30 seconds | 60 seconds | Detects loss without treating a single missed collection as failure. Revalidate under live scrape behavior. |
| Advisory resource evidence | 30 seconds | 60 seconds | Same initial collection cadence; no health threshold depends on it in v1. |
| Health assessment | Not applicable | Earliest mandatory-evidence expiry, capped at 60 seconds after `evaluated_at` | Prevents an assessment from outliving its proof. |

Evidence at or below the aging boundary is `current`; evidence above the aging boundary and at or below maximum age is `aging`; evidence above maximum age is `stale`. Missing or invalid timestamps produce `unknown`. Aging evidence may support only a policy that explicitly permits it; v1 Healthy requires `current` mandatory evidence.

`valid_until` is the minimum of each mandatory evidence item's observation time plus its maximum age and `evaluated_at + 60 seconds`.

### Health-Check Requirement

| Registry Value | Meaning | `not_configured` Treatment |
|----------------|---------|----------------------------|
| `required` | A passing runtime health check is mandatory. | `insufficient_evidence` with `REQUIRED_HEALTHCHECK_NOT_CONFIGURED`. |
| `optional` | Health check improves evidence but is not mandatory. | Neutral with `HEALTHCHECK_NOT_REQUIRED`; Healthy remains possible. |
| `not_applicable` | Runtime health check does not apply. | No health-check evidence is required. |

### Restart Policy

Restart evidence is advisory in v1. The system may validate a nonnegative lifetime count with explicit semantics and record whether a restart occurred during a bounded window. It may emit an informational restart finding, but it cannot independently produce `degraded` or `unhealthy` until a later approved policy defines count, rate, window, reset, and intentional-restart behavior.

No canonical health reason code is emitted solely because a valid restart count or occurrence exists in v1; that evidence is retained as advisory support with a bounded informational finding. `RESTART_THRESHOLD_EXCEEDED` is reserved and must not be emitted by policy version `1.0`.

### Resource-Pressure Policy

- CPU and memory utilization are advisory in v1 because no repository evidence supports numeric thresholds.
- Current `container.memory.pressure=critical` with exact identity and at least medium evidence confidence produces `degraded` and `MEMORY_PRESSURE_CRITICAL`.
- `elevated` memory pressure produces an advisory `RESOURCE_PRESSURE_ELEVATED` finding only in v1.
- No resource-pressure signal independently produces `unhealthy` in v1.
- Live validation must establish provider normalization, observation windows, baseline distributions, sustained-duration behavior, and correlation with actual service impairment before numeric thresholds are approved.

### Confidence Application

Confidence belongs to both levels of the architecture. Each evidence record carries one evidence-confidence classification (`high`, `medium`, `low`, or `none`) under the published evidence contract. Each health result carries a separately derived assessment-confidence classification using the same bounded values under `container-assessment-confidence` `1.0`.

Assessment confidence cannot exceed the least-confident mandatory evidence supporting the result. `none` mandatory evidence, unresolved identity, or material conflict normally produces `insufficient_evidence` with assessment confidence `none`. `low` evidence cannot satisfy v1 mandatory Healthy proof. Assessment confidence is derived and traceable; it is not copied from a provider, averaged, scored, or substituted for health status.

---

## Reconciliation Policy v1.0

### Outcomes

| Condition | Outcome |
|-----------|---------|
| Exact declared subject and qualifying current observation agree | `matched` |
| Declared subject has no qualifying current observation | `missing` |
| Observation cannot resolve to a Registry subject | `unexpected` |
| More than one plausible subject exists | `ambiguous` |
| Qualifying current providers disagree materially | `conflicting` |
| Correctly mapped evidence exceeds applicable freshness | `stale` |
| Evidence type does not require declared comparison | `not_applicable` |

No qualifying observation is not proof of absence. It normally produces reconciliation `missing` and health `insufficient_evidence`.

Conclusive absence requires a current, complete, exact-identity inventory observation from a provider approved to establish population absence. It may produce reconciliation `missing` with conclusive-absence reason and health `unhealthy` for an active subject.

The reconciliation record retains all considered, selected, and rejected evidence IDs and bounded rejection reasons. It never mutates Registry or evidence.

---

## Health Decision Table v1.0

Evaluation follows PLAT-14.0A precedence: not evaluated, insufficient evidence, unhealthy, degraded, then healthy.

| Condition | Health Result | Required Reason Code |
|-----------|---------------|----------------------|
| No assessment exists | `not_evaluated` | `NO_EVALUATION` |
| Registry subject is intentionally inactive or excluded | `not_evaluated` | `SUBJECT_NOT_ACTIVE` |
| No current mandatory lifecycle evidence | `insufficient_evidence` | `LIFECYCLE_EVIDENCE_MISSING` |
| Identity is ambiguous or unresolved | `insufficient_evidence` | `IDENTITY_UNRESOLVED` |
| Mandatory evidence confidence is `none` | `insufficient_evidence` | `MANDATORY_EVIDENCE_UNUSABLE` |
| Current lifecycle providers conflict | `insufficient_evidence` | `LIFECYCLE_CONFLICT` |
| Complete mandatory telemetry is unavailable | `insufficient_evidence` | `TELEMETRY_UNAVAILABLE` |
| Material cAdvisor limitation affects the only mandatory lifecycle evidence | `insufficient_evidence` | `PROVIDER_LIMITATION_APPLIES` |
| Active declared subject is conclusively absent | `unhealthy` | `DECLARED_SUBJECT_ABSENT` |
| Container exited unexpectedly | `unhealthy` | `UNEXPECTED_EXIT` |
| Required health check is failing | `unhealthy` | `HEALTHCHECK_FAILED` |
| Required health check is not configured | `insufficient_evidence` | `REQUIRED_HEALTHCHECK_NOT_CONFIGURED` |
| Optional health check is not configured | Neutral | `HEALTHCHECK_NOT_REQUIRED` |
| Mandatory coverage is partial | `insufficient_evidence` | `MANDATORY_TELEMETRY_PARTIAL` |
| Advisory coverage is partial | No status change in v1 | `ADVISORY_TELEMETRY_PARTIAL` |
| Current critical memory-pressure signal qualifies | `degraded` | `MEMORY_PRESSURE_CRITICAL` |
| Elevated advisory pressure qualifies | No status change in v1 | `RESOURCE_PRESSURE_ELEVATED` |
| Advisory resource evidence is stale | No status change | `RESOURCE_EVIDENCE_STALE` |
| Assessment is past `valid_until` | Stored status is noncurrent and cannot be presented as current Healthy | `ASSESSMENT_EXPIRED` |
| Exact running match and every mandatory criterion passes | `healthy` | `ALL_MANDATORY_CRITERIA_PASSED` |

Provider unavailability cannot independently produce `unhealthy`.

---

## Reason-Code Catalog v1.0

| Code | Meaning | Applicable State | Criticality | Treatment | Required Support |
|------|---------|------------------|-------------|-----------|------------------|
| `NO_EVALUATION` | No governed assessment exists. | `not_evaluated` | Informational | Terminal for the absent evaluation | None; consumers must not synthesize a result. |
| `SUBJECT_NOT_ACTIVE` | Registry excludes active evaluation. | `not_evaluated` | Informational | Terminal for this policy evaluation | Registry participation and exclusion reason. |
| `LIFECYCLE_EVIDENCE_MISSING` | No current qualifying lifecycle evidence exists. | `insufficient_evidence` | Blocking | Blocking | Registry subject and considered evidence inventory. |
| `IDENTITY_UNRESOLVED` | Runtime identity cannot resolve exactly. | `insufficient_evidence` | Blocking | Blocking | Mapping candidates and identity findings. |
| `LIFECYCLE_CONFLICT` | Current providers disagree on lifecycle state. | `insufficient_evidence` | Blocking | Blocking | Conflicting evidence IDs. |
| `MANDATORY_EVIDENCE_UNUSABLE` | Mandatory evidence has confidence `none` or is invalid. | `insufficient_evidence` | Blocking | Blocking | Rejected evidence and confidence reasons. |
| `TELEMETRY_UNAVAILABLE` | No provider supplies mandatory current evidence. | `insufficient_evidence` | Blocking | Blocking | Telemetry-availability evidence. |
| `PROVIDER_LIMITATION_APPLIES` | A provider limitation affects mandatory suitability. | `insufficient_evidence` | Blocking | Blocking | Provider/version limitation finding. |
| `DECLARED_SUBJECT_ABSENT` | Complete direct inventory proves an active declared subject absent. | `unhealthy` | Critical | Terminal for evaluation | Exact Registry identity and conclusive inventory evidence. |
| `UNEXPECTED_EXIT` | Current evidence proves unexpected exit. | `unhealthy` | Critical | Terminal for evaluation | Lifecycle evidence and expected active state. |
| `HEALTHCHECK_FAILED` | Required runtime health check is failing. | `unhealthy` | Critical | Terminal for evaluation | Current required health-check evidence. |
| `REQUIRED_HEALTHCHECK_NOT_CONFIGURED` | Required check is absent. | `insufficient_evidence` | Blocking | Blocking | Registry requirement and `not_configured` evidence. |
| `HEALTHCHECK_NOT_REQUIRED` | Optional or inapplicable check is absent. | Any evaluated state | Informational | Informational | Registry requirement. |
| `RESTART_THRESHOLD_EXCEEDED` | Approved restart threshold exceeded. | Reserved | Criticality deferred | Not emitted in v1 | Future policy and bounded-window evidence. |
| `ADVISORY_TELEMETRY_PARTIAL` | Advisory signal coverage is partial. | Any evaluated state | Advisory | Finding-only in v1 | Coverage evidence. |
| `MANDATORY_TELEMETRY_PARTIAL` | Mandatory signal coverage is partial. | `insufficient_evidence` | Blocking | Blocking | Coverage evidence and mandatory set. |
| `RESOURCE_PRESSURE_ELEVATED` | Advisory pressure is elevated. | Any evaluated state | Advisory | Finding-only in v1 | Current resource evidence. |
| `MEMORY_PRESSURE_CRITICAL` | Current memory-pressure state is critical. | `degraded` | Material | Degrading | Current qualified pressure evidence. |
| `RESOURCE_EVIDENCE_STALE` | Resource evidence cannot support a current conclusion. | Any evaluated state | Advisory | Finding-only | Freshness calculation. |
| `ASSESSMENT_EXPIRED` | Assessment is past `valid_until`. | Any stored state, noncurrent | Blocking for current presentation | Consumer-blocking | Assessment timestamps. |
| `ALL_MANDATORY_CRITERIA_PASSED` | Every v1 mandatory criterion passed. | `healthy` | Informational | Terminal for evaluation | Selected evidence and policy trace. |

Provider names belong in provider findings, not canonical health reason codes.

---

## Authoritative Outputs

The first implementation must support exactly four authoritative representations:

1. Operational Evidence JSON.
2. Reconciliation JSON.
3. Operational Health Assessment JSON.
4. Deterministic Markdown projection of a validated assessment.

No separate consumer-summary format is permitted in v1.

### Output Requirements

- Stable model and contract versions.
- Deterministic UTF-8 JSON with sorted keys and stable list ordering where semantic order is not defined.
- Registry `subject_id` and `registry_reference`.
- Contract, profile, manifest, and constituent policy versions.
- Accepted, rejected, selected, and supporting evidence references where applicable.
- Health and assessment confidence.
- Bounded reason codes and findings.
- Freshness calculations, `evaluated_at`, and `valid_until`.
- Repository-fixture scope and explicit `activation_status: not_activated` in fixture evaluation metadata.
- No secrets, raw provider payload, arbitrary metadata, or absolute paths.

The JSON assessment is the authoritative consumer result. Markdown is a projection and cannot add or recalculate health logic.

### Output Persistence

The first implementation should write JSON and Markdown only to standard output or test-controlled streams. Golden expected artifacts may be stored under `engineering/tests/fixtures/container_health/expected/` after implementation authorization. Dynamic fixture execution uses temporary directories and is not committed as operational evidence.

Persistent report publication is deferred. Any later approved file writer must validate before writing, refuse overwrite by default, use a same-directory temporary file, structurally reopen or reparse the completed artifact, atomically replace the destination, and clean temporary output after failure.

---

## Future Read-Only CLI Contract

The bounded future command surface is:

```text
./platform-eap container-health evidence validate <path>
./platform-eap container-health reconcile <input-path>
./platform-eap container-health assess <input-path>
./platform-eap container-health assessment validate <path>
./platform-eap container-health assessment render <path>
```

The CLI is repository-local, deterministic, network-free, provider-free, side-effect-free, and read-only. Input paths must resolve inside the repository and symlink or traversal escape must fail.

| Exit Code | Meaning |
|-----------|---------|
| `0` | Valid input and valid domain result. `not_evaluated`, `insufficient_evidence`, `unhealthy`, `degraded`, and `healthy` are valid results, not process failures. |
| `2` | Malformed input, unknown field, invalid value, unsafe reference, or failed contract validation. |
| `3` | Unsupported or denied contract/profile major version. |
| `4` | Missing, malformed, contradictory, inactive, or incompatible policy set. |

No input field is executed. Rendering writes only to standard output. This package does not implement these commands.

---

## Fixture Adapter Boundary

The future implementation includes one generic governed fixture-observation format and two test-scoped provider fixture shapes that represent the same observations differently.

### Responsibilities

| Boundary | Responsibility |
|----------|----------------|
| Fixture input | Provider-shaped raw observation, timestamps, runtime references, allowed labels, and source-fixture reference. |
| Fixture adapter | Strictly parse one known shape, validate supported values, resolve identity under the governed policy, convert units, and emit evidence or findings. |
| Adapter output | One-signal canonical evidence records or structured normalization findings. |
| Raw fixture | Remains separate from canonical evidence and may contain only synthetic, secret-free test data. |

Required normalization findings include subject mapping failure, ambiguous runtime identity, unsupported signal, malformed value, unsupported unit, missing timestamp, unsafe source reference, unsupported provider version, provider limitation, and secret-like input.

Unknown or unsupported input fails closed. No dynamic discovery, plugin loading, reflection, external dependency, provider access, or universal adapter abstraction is permitted.

Equivalent provider observations must produce equivalent canonical signal name, value, unit, subject identity, and health outcome. Provider provenance remains different and traceable.

Fixture proof does not establish live compatibility, cardinality, provider security, operational timing, or production readiness.

---

## EO-14.1A and EO-14.4A Fixture Integration

One future end-to-end fixture scenario must demonstrate:

1. An EO-14.1A assignment identifies a repository-fixture PLAT-14.1A evaluation.
2. PLAT-14.1A produces valid evidence, reconciliation, and assessment artifacts.
3. An EO-14.1A completion package references those artifacts and required validation evidence.
4. An EO-14.4A automation definition and run consume the published EO assignment and completion contracts.
5. EO-14.4A proposes a human-review transition and renders a handoff.
6. The completion and handoff declare no command, model, provider, lifecycle mutation, activation, or live action.

PLAT-14.1A reuses `GovernedAssignment`, `ApprovalRequirement`, `ApprovalRecord`, `CompletionPackage`, `EvidenceType`, and `ValidationFinding` and the published EO parsers and validators. It does not recreate them.

PLAT outputs expose repository-relative artifact references, stable artifact IDs, validation state, contract/profile/policy versions, and explicit fixture-only scope so EO completion evidence can reference them safely.

The integration proves contract reuse, reference validation, fail-closed handling, and advisory handoff. It does not activate either EO capability or authorize recurring automation.

---

## Repository-First Acceptance Matrix

The future implementation must cover:

### Contracts and Versions

- Valid envelope and Container Profile.
- Unknown fields and malformed values.
- Unsupported contract major version.
- Unsupported profile version.
- Missing, inactive, or incompatible policy set.

### Identity

- Exact match.
- Runtime ID replacement without subject change.
- Similar names.
- Ambiguous mapping.
- Unexpected subject.
- Renamed Compose service.
- Fuzzy matching prohibited.

### Reconciliation

- `matched`, `missing`, `unexpected`, `ambiguous`, `conflicting`, `stale`, and `not_applicable`.
- No observation distinguished from conclusive absence.
- Considered, selected, and rejected evidence preserved.

### Evidence Quality

- `current`, `aging`, `stale`, and `unknown` freshness.
- `complete`, `partial`, `missing_required_attributes`, and `not_assessable` completeness.
- `high`, `medium`, `low`, and `none` evidence confidence.

### Health

- `not_evaluated`, `healthy`, `degraded`, `unhealthy`, and `insufficient_evidence`.
- Inactive and excluded subjects.
- Assessment expiration.

### Lifecycle and Health Check

- Running, missing, stopped intentionally, exited unexpectedly, and restarting.
- Passing, failing, starting, unavailable, required but not configured, and optional but not configured.

### Restart and Resource

- Advisory restart evidence.
- Reserved threshold code not emitted in v1.
- CPU and memory advisory evidence.
- Critical memory-pressure degradation.
- Stale resource evidence.

### Telemetry and Consumer Behavior

- Provider available and unavailable.
- Partial and complete coverage loss.
- Identity unresolved.
- Known cAdvisor limitation.
- No assessment, insufficient evidence, provider failure, required-signal failure, expired assessment, presentation failure, and conclusive unhealthy cases remain distinguishable.

### Provider Independence and Security

- Two differently shaped fixtures normalize to equivalent canonical evidence.
- Provider labels do not leak into canonical signal or subject identity.
- Raw payload excluded.
- Secret-like content, traversal, absolute paths, symlink escape, and unsafe references rejected.

### Outputs and EO Integration

- Stable JSON and Markdown.
- Deterministic ordering.
- Complete policy/version traceability.
- No renderer-owned health logic.
- Valid EO assignment/completion references.
- Invalid references rejected.
- Advisory EO automation handoff with no activation.

### Side Effects

- No network, subprocess, Docker, SSH, infrastructure mutation, persistent runtime state, provider access, or file output beyond explicitly controlled future tests.

Fixture tests prove repository contract, normalization, reconciliation, policy, health, output, and EO-integration behavior only. They do not prove live provider compatibility, privileged proxy denial, metric inventory, timing, cardinality, Grafana rendering, Pi-hole non-regression, production performance, or operational readiness.

---

## Future Gates

| Gate | Authorized Scope | Required Evidence |
|------|------------------|-------------------|
| Core Repository Implementation | Contract models, policy loading, fixture translators, reconciliation, health evaluation, outputs, CLI, and tests. | Full repository acceptance matrix and Architecture Gatekeeper review. |
| Provider-Adapter Implementation | Bounded provider-specific mappings using fixtures only. | Supported versions, normalization equivalence, limitation handling, and no health calculation. |
| Security Review | Restricted Docker API, socket, or other privileged access. | Least privilege, allowlist, denial proof plan, secrets, escape risk, exposure, logging, retention, rollback. |
| Live Observation | Read-only named-target observation. | Approved targets/endpoints, duration, stop conditions, evidence handling, rollback, Pi-hole and household-service non-regression, human approval. |
| Dashboard Integration | Read-only assessment consumption. | Version compatibility, no recalculation, no-data distinctions, expired-assessment behavior, presentation failure handling. |
| Activation | Recurring or EO-coordinated operation. | Validated consumer, operating owner, cadence, disablement, repeated evidence, EO approval, and explicit human approval. |

No later gate is implied by fixture success.

---

## cAdvisor and Dashboard No-Data Requirements

Known cAdvisor limitations produce explicit provider findings, constrain evidence confidence, and prevent ambiguous runtime identity from satisfying Healthy. A healthy cAdvisor scrape target proves provider reachability only. When affected cAdvisor evidence is the only source for mandatory lifecycle identity, the result is `insufficient_evidence`.

Dashboard consumers distinguish:

| Situation | Consumer Treatment |
|-----------|--------------------|
| No assessment exists | Display `not_evaluated`. |
| Assessment reports insufficient evidence | Display `insufficient_evidence` and reasons. |
| Provider unavailable | Display provider-evidence unavailability; do not infer service failure. |
| Required signal unavailable | Display insufficient evidence. |
| Assessment expired | Display noncurrent/expired; never current Healthy. |
| Dashboard query or rendering failed | Display presentation failure without changing the authoritative assessment. |
| Conclusive unhealthy evidence | Display the governed `unhealthy` assessment and reasons. |

Dashboard absence, query failure, or no-data behavior never changes the authoritative assessment.

---

## Implementation Direction and Lifecycle

The approved future direction is a repository vertical slice with bounded fixture adapters:

- Contract and policy validation.
- Registry-linked identity.
- Two provider-shaped fixture normalizations.
- Reconciliation and health evaluation.
- Deterministic JSON and Markdown.
- EO fixture integration.
- No live provider access.

This direction is not implementation authorization. PLAT-14.1A remains blocked until this specification is Architecture Gatekeeper reviewed, published, and followed by a separately authorized repository implementation package.

PLAT-14.0A remains published architecture with `Implemented: No`. EO-14.1A and EO-14.4A remain published and unactivated. Bravo is in Specification Alignment. Charlie remains unstarted and dependent on governed assessments. Provider, security, live-observation, dashboard, activation, and FFFA work remain separate.

---

## Explicit Non-Goals

- Python models, policy loaders, parsers, validators, serializers, or CLI implementation.
- Machine-readable policy artifacts.
- Registry schema or record migration.
- Fixture files used by tests.
- Provider adapters or provider deployment.
- Docker, Prometheus, OpenTelemetry, cAdvisor, Grafana, SSH, network, host, container, or service access.
- APIs, databases, background workers, schedulers, or persistent state.
- Execution Agent or Governed Automation activation.
- Dashboard implementation, remediation, or infrastructure mutation.
- FFFA changes.

---

## Specification Acceptance Criteria

This specification is ready for Architecture Gatekeeper review when:

- Product promise, customer, measurable outcomes, and non-ownership are explicit.
- Registry-owned identity design and matching precedence are deterministic.
- First-slice signals distinguish mandatory from advisory evidence.
- Initial freshness, confidence, health-check, restart, and pressure policies are explicit and disclose live-validation needs.
- Reconciliation distinguishes missing observation from conclusive absence.
- Health precedence and reason codes are bounded and provider-independent.
- Outputs and future CLI are deterministic, read-only, and side-effect-free.
- Fixture adapters prove provider replacement without becoming production adapters.
- EO integration reuses published contracts without activation.
- Future provider, security, observation, dashboard, and activation gates remain separate.
- Portfolio and lifecycle metadata record PLAT-14.0A publication and PLAT-14.1A implementation blocking accurately.
- No implementation or live work is introduced.

---

## Related Documents

- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Infrastructure Registry v1.0 Specification](Infrastructure_Registry_v1.0_Specification.md)
- [Registry Container Identity Foundation Architecture](../architecture/Registry_Container_Identity_Foundation_Architecture.md)
- [Registry Container Identity Foundation Specification](Registry_Container_Identity_Foundation_Specification.md)
- [Container Metrics Modernization Specification](Container_Metrics_Modernization_Specification.md)
- [Platform Operations and Observability Specification](Platform_Operations_Observability_Specification.md)
- [Platform Health Dashboard Specification](Platform_Health_Dashboard_Specification.md)
- [Operations Analyst Specification](../engineering-organization/Operations_Analyst_Specification.md)
- [Execution Capability Usage](../engineering-organization/Execution_Capability_Usage.md)
- [Governed Automation Framework Usage](../engineering-organization/Governed_Automation_Framework_Usage.md)
- [ADR-009 - Evidence Before Operational Health](../architecture/decisions/ADR-009-Evidence-Before-Operational-Health.md)
- [ADR-010 - Declared Observed and Reconciled State](../architecture/decisions/ADR-010-Declared-Observed-and-Reconciled-State.md)
- [ADR-011 - Generic Operational Evidence Envelope and Versioned Profiles](../architecture/decisions/ADR-011-Generic-Operational-Evidence-Envelope-and-Versioned-Profiles.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded publication and aligned the unimplemented Registry Container Identity Foundation dependency, selected service-record field model, and evidence-gated Pi-hole migration boundary. |
| 1.0 | Initial PLAT-14.1A Container Operational Health specification alignment baseline. |
