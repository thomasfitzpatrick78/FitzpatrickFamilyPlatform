# Registry Container Identity Foundation Specification

**Document Version:** 1.3

**Status:** Published Specification and Implementation

**Milestone:** Milestone 14 - PLAT-14.1A prerequisite

**Implementation:** Complete; Published

---

## Purpose

This specification defines the smallest authoritative Infrastructure Registry extension required to provide stable declared identity for container-backed Platform services consumed by PLAT-14.1A Container Operational Health.

The implemented design adds bounded optional fields to existing `service` and `planned_service` records. It does not create a new container record type, linked runtime inventory, provider model, or health-assessment field.

The repository implementation advances the schema to `1.1`, adds strict validation, deterministic migration planning/execution/rollback, an exact-plan governed approval artifact, and compatible CLI commands. It does not migrate any current Registry record or authorize PLAT-14.1A implementation.

---

## Product Contract

The Registry Container Identity Foundation extends the Infrastructure Registry declared-state contract so container-backed Platform services can be identified, reconciled, and assessed consistently without coupling canonical identity to a runtime engine or telemetry provider.

It allows a consumer to determine:

- Which Registry subject represents the service.
- Which governed host is expected.
- Which governed Compose project and service identify the v1 workload.
- Whether the subject participates in current health assessment.
- Whether a runtime health check is required, optional, or not applicable.
- Which Container Operational Health policy set applies.
- Which optional runtime name or image values may corroborate identity.
- Why a subject is intentionally inactive, excluded, or not applicable.

The Registry owns declarations only. Runtime discovery, monitoring, evidence, reconciliation, health, remediation, deployment, orchestration, and activation remain outside this foundation.

---

## Selected Record Model

### Applicable Record Types

The future extension applies only to existing `service` and `planned_service` records.

- Record `id` remains canonical `subject_id`.
- Record path is the authoritative Registry reference.
- Record `name` remains display text only.
- Existing `host_dependencies` and other topology relationships remain authoritative relationships.
- A record may have at most one container identity declaration in contract v1.

Absence of container identity fields preserves legacy validity and means the record is not yet classified for container-health eligibility. It must not be interpreted as confirmed `not_applicable`.

### Implemented Schema Version

The authorized implementation advances `infrastructure_registry_v1` from schema version `1.0` to additive minor version `1.1`.

Existing required common fields and allowed record types remain unchanged. New fields are optional at the general schema level and become conditionally required only when `container_identity_contract_version` is present.

No per-record schema version is required. `container_identity_contract_version` versions the bounded extension, while the repository schema version identifies the overall Registry contract.

---

## Implemented Field Contract v1.0

| Field | Type | Requirement | Contract |
|-------|------|-------------|----------|
| `container_identity_contract_version` | String | Required when any container identity field appears | Exact supported value `1.0`. |
| `container_participation` | String | Required with the extension | One of `active`, `intentionally_inactive`, `excluded`, `not_applicable`. Replaces an ambiguous `container_backed` boolean. |
| `container_host_reference` | Registry ID | Required for `active`; required for inactive/excluded when host is governed | Must resolve to one `host` record and appear in `host_dependencies`. |
| `compose_project` | String | Required for `active` v1 eligibility | Exact governed Compose project. |
| `compose_service` | String | Required for `active` v1 eligibility | Exact governed Compose service. |
| `governed_runtime_name` | String | Optional | Exact host-scoped fallback; lower authority than Compose identity. |
| `health_check_requirement` | String | Required for active and intentionally inactive container-backed subjects | One of `required`, `optional`, `not_applicable`. Registry declares; PLAT-14.1A evaluates evidence. |
| `container_health_policy_reference` | Repository-relative reference | Required for `active` | Resolves to the approved compatible Container Operational Health policy manifest after that implementation exists. No health rules are embedded here. |
| `expected_image_reference` | String | Optional | Normalized repository/name and optional tag; corroboration only. |
| `expected_image_digest` | String | Optional | Valid immutable digest; corroboration and drift evidence only. |
| `container_identity_evidence` | List of repository-relative references | Required for active, intentionally inactive, and excluded migration | Governed evidence supporting the declaration; no live payload or absolute path. |
| `participation_reason` | String | Required for `intentionally_inactive` and `excluded`; optional for `not_applicable` | Bounded reviewed reason. |
| `participation_review_reference` | Repository-relative reference | Required for `excluded`; optional for intentionally inactive | Points to the governed decision/evidence artifact and avoids duplicating approval identities. |
| `participation_review_expires_at` | Timezone-aware timestamp | Optional | Requires reassessment after expiry; does not activate automation. |

### Participation Semantics

| Value | Meaning | PLAT-14.1A Treatment |
|-------|---------|----------------------|
| `active` | Container-backed subject is expected to participate now and has a complete eligible identity contract. | May be evaluated after PLAT implementation authorization. |
| `intentionally_inactive` | Confirmed container-backed subject is deliberately not expected to operate now, including an approved planned-not-deployed case. | `not_evaluated`; reason preserved. |
| `excluded` | Confirmed container-backed subject is outside evaluation because identity, support, policy, or scope is not approved. | `not_evaluated`; reviewed reason required. |
| `not_applicable` | Reviewed conclusion that the service record is not a container-backed assessed subject. | Not a container-health subject. |

Missing extension fields mean legacy or unresolved, never silent eligibility and never implicit `not_applicable`.

### Bounded Reasons

Initial reason values should be limited to:

- `planned_not_deployed`
- `approved_maintenance_or_shutdown`
- `unsupported_identity_model`
- `identity_unresolved`
- `out_of_scope`
- `logical_or_repository_capability`
- `runtime_engine_not_workload`
- `retired_or_replacement_only`

New outcome-changing reasons require a compatible contract revision and review.

---

## Format and Normalization Rules

- `container_host_reference` uses an exact Registry ID and must resolve to `record_type: host`.
- Compose project and service values use lowercase ASCII letters, digits, underscore, period, and hyphen; they begin with a lowercase letter or digit; leading/trailing whitespace is invalid.
- A governed runtime name uses ASCII letters, digits, underscore, period, and hyphen, begins with an alphanumeric character, and is matched case-sensitively exactly as declared.
- Adapters do not trim, case-fold, suffix-match, or otherwise normalize an invalid provider value into a match.
- Image references are syntactically normalized but cannot establish canonical identity.
- Digests require an approved algorithm prefix and valid encoded digest.
- Repository references are relative, cannot contain traversal, cannot be absolute or symlink-escaped, and must resolve inside an approved repository path.
- Timestamps are timezone-aware ISO 8601 values.

The implemented validator publishes bounded accepted regular expressions and length limits in repository code. It tightens syntax without changing identity meaning and does not guess or rewrite existing values.

---

## Conditional Validation Rules

### Active

An `active` record requires:

- `record_type` of `service`.
- Existing lifecycle status `active`.
- Contract version `1.0`.
- One resolving `container_host_reference` also present in `host_dependencies`.
- Compose project and service.
- Bounded health-check requirement.
- Resolving compatible policy reference.
- At least one governed identity-evidence reference.
- A host-scoped unique Compose tuple.

Optional runtime name, if present, must be unique on the host. Image fields remain optional.

### Intentionally Inactive

An `intentionally_inactive` record may be `service` or `planned_service`. It requires a reason, evidence, and all identity fields currently known. A planned container whose host and Compose tuple are governed should declare them; an unresolved critical field prevents future active eligibility but does not require a guessed value.

### Excluded

An `excluded` record requires reason, evidence, and a review reference. It may omit the Compose tuple or host when identity is the reason for exclusion. It is never health eligible.

### Not Applicable

A `not_applicable` record confirms the service is not a container-backed assessed subject. It prohibits host, Compose, runtime-name, health-check, policy, and image identity fields under this extension. A reason may document the conclusion.

---

## Cross-Record Validation

Implemented validation enforces:

- Global uniqueness of existing Registry IDs.
- Container host reference resolves to one host.
- Container host reference agrees with `host_dependencies`.
- `(container_host_reference, compose_project, compose_service)` is unique among active and intentionally inactive declarations where collision would make identity ambiguous.
- `governed_runtime_name` is unique per governed host whenever used for matching.
- Policy reference resolves and supports the declared contract after machine-readable policy implementation is authorized.
- Evidence and review references are safe and resolve.
- Service relationships remain acyclic under existing Digital Twin rules.

The same Compose service name on different governed hosts is permitted because host is part of the identity tuple. The same project/service tuple on one host is prohibited in v1.

---

## Contradiction Rules

Implemented validation rejects:

- Container fields on a record type other than `service` or `planned_service`.
- Active participation without a host, Compose project, Compose service, health-check requirement, compatible policy reference, or evidence.
- Active participation on a non-active service lifecycle.
- `not_applicable` combined with container identity or health-check fields.
- Excluded participation without a reason and review reference.
- Health check `required` when participation is `not_applicable`.
- Container host reference absent from `host_dependencies`.
- Runtime container ID, provider label, cgroup ID, metric label, or provider resource attribute stored as canonical identity.
- Provider-derived health or PLAT assessment status stored in the identity extension.
- Unknown container identity fields or unsupported contract versions.
- Multiple container identity declarations for one service in v1.

---

## Identity Matching Contract

Matching order is fixed:

1. Exact Platform subject ID and valid Registry reference.
2. Exact subject, host, Compose project, and Compose service tuple.
3. Exact governed runtime name plus host only when Registry validation proves uniqueness.
4. Expected image identity as corroboration only.
5. Runtime container ID as evidence provenance only.
6. Provider labels and resource attributes as untrusted adapter inputs only.
7. Fuzzy, suffix, substring, case-folded, or partial matching is prohibited.

### Scenario Treatment

| Scenario | Treatment |
|----------|-----------|
| Runtime ID changes after recreation | Same subject when the governed tuple is unchanged; retain new ID only in evidence provenance. |
| Compose service renamed | Requires reviewed Registry update. Until then, declared subject is missing and observation is unexpected or unresolved. |
| Service moves hosts | Requires reviewed host reference and dependency update; provider observation cannot perform the migration. |
| Similar runtime names | Ambiguous; no authoritative selection. |
| Unmanaged container | Unexpected observation; no Registry record created. |
| Scaled replicas | Deferred. v1 cannot aggregate or create subjects for replicas automatically. |
| Non-Compose workload | Excluded or unresolved pending a separately versioned identity mechanism. |

---

## PLAT-14.1A Consumer Contract

After Architecture Gatekeeper publication, a separately approved evidence-gated record migration, and separate PLAT authorization, PLAT-14.1A may consume:

- Canonical subject ID.
- Registry record reference.
- Container participation.
- Governed host reference.
- Governed Compose identity.
- Optional governed runtime name.
- Health-check requirement.
- Compatible policy-set reference.
- Optional expected image reference and digest.
- Inactivity or exclusion reason and review reference.

PLAT-14.1A must not infer missing declarations, create subjects, change participation, modify Registry records, treat observations as declared state, or override reviewed exclusion decisions.

Missing, invalid, contradictory, unsupported, or unresolved required identity fails closed. The subject is not eligible for authoritative health assessment and receives an explicit Registry-contract finding; no runtime fallback may repair declared state implicitly.

---

## Versioning and Compatibility

- Schema version `1.1` is the implemented additive Registry contract.
- Container identity contract version starts at `1.0`.
- Legacy records without container fields remain valid and ineligible.
- Confirmed non-container records become explicit only through reviewed `not_applicable` migration.
- Outcome-changing meaning, identity precedence, or participation changes require a major container identity contract version.
- Backward-compatible optional corroboration may use a minor version.
- Future required fields cannot invalidate legacy records silently; a migration gate and compatibility period are required.
- Unknown fields and unsupported contract versions fail closed once the extension is present.
- Migration is deterministic and idempotent: identical validated inputs produce the same record patch, and a second application produces no change.

No migration may infer critical values from container names, directory names, image names, provider labels, metric series, or live discovery alone.

---

## Migration Design

The migration framework is implemented as a repository-only capability. It produces reviewed record patches only from an explicitly approved plan; it does not connect to live infrastructure. No current record is migrated by this package.

| Category | Eligible Action | Required Evidence | Default / Review | Rollback |
|----------|-----------------|-------------------|------------------|----------|
| Confirmed active container-backed service | Add complete `active` declaration only when all mandatory values are proven. | Registry host relationship, governed Compose artifact or approved evidence, health-check decision, policy compatibility, reviewed identity evidence. | Ineligible until complete; human approval required. | Revert the migration commit or apply reviewed inverse patch; prior record must validate. |
| Confirmed intentionally inactive container-backed service | Add `intentionally_inactive`, reason, evidence, and known identity. | Declared shutdown/planned status and identity evidence. | Never treated as missing or unhealthy. | Restore prior valid record through Git review. |
| Confirmed non-container service | Add `not_applicable` with optional reason. | Repository purpose and runtime model evidence. | No container-health evaluation. | Restore prior valid record. |
| Planned container-backed service | Add `intentionally_inactive` with `planned_not_deployed` when planned identity is governed. | Repository Compose/configuration and approved plan; no live proof claim. | Remains unactivated and not evaluated. | Restore prior planned record. |
| Unresolved service | Do not add active identity; optionally add reviewed `excluded` only when exclusion is approved. | Human review and explicit unresolved facts. | Remains legacy/ineligible or excluded; never guess. | Remove reviewed extension by inverse patch. |
| Not applicable record domain | No change. | Record type. | Devices, hosts, locations, owners, and network devices remain relationship records. | Not applicable. |

Every migration batch validates before and after, preserves a reviewable diff, identifies its evidence, and proves the second application is a no-op. Mutation requires a canonical plan bound to a separate matching governed approval artifact, explicit confirmation, and rollback metadata.

### Governed Migration Approval Artifact

The migration plan defines what is proposed. A separate repository-local JSON approval artifact defines whether that exact proposal is authorized. Plan approval fields are derived presentation metadata and cannot authorize execution by themselves.

The strict approval artifact contains:

| Field | Requirement |
|-------|-------------|
| `model_version` | Exact supported approval model `registry-container-identity-approval-v1`. |
| `plan_id` | Exact canonical migration plan ID, binding all candidates, actions, proposed fields, record hashes, and evidence hashes. |
| `schema_version` | Exact Registry schema version used by the plan. |
| `migration_model_version` | Exact migration model version used by the plan. |
| `approval_status` | One of `pending`, `approved`, or `rejected`; execution requires `approved`. |
| `approval_scope` | Execution requires exact scope `registry_record_migration`. |
| `approval_timestamp` | Timezone-aware ISO 8601 decision timestamp. |
| `approval_authority` | Exact governed authority `Architecture Gatekeeper`. |
| `approval_authority_reference` | Safe existing repository reference under governed architecture, engineering-organization, governance, or milestone documentation. |
| `decision_notes` | Optional nonblank decision notes. |

The read-only `bind-approval` command verifies the artifact against the canonical plan and binds the artifact path and SHA-256 content hash into a derived plan presentation. Execution reloads the artifact, rejects drift, parses it strictly, rejects unknown fields and unsupported versions, and revalidates plan ID, versions, affirmative scope, timestamp, authority, and review reference. Editing only serialized plan approval fields or referencing an arbitrary existing document cannot authorize mutation.

### Pi-hole Migration Assessment

Repository evidence currently establishes:

- Canonical subject: `svc-pihole-dns`.
- Record type: `service`.
- Active lifecycle and container-backed production role.
- Governed host: `host-beelink-mini-pc`.
- Host relationship: present.
- Governed runtime-name candidate: `pihole`.
- Compose path: `/platform/compose/pihole`.

Repository evidence does not yet establish sufficiently for migration:

- Exact governed Compose project.
- Exact Compose service key.
- Approved Registry health-check requirement.
- Implemented compatible policy-set reference.
- Expected image reference and digest.
- A reviewed migration evidence set under this contract.

The Compose directory name and runtime name cannot be promoted into missing Compose values. Pi-hole therefore appears eligible for a future evidence-gathering migration review but is not yet eligible for an `active` container identity record patch.

### Other Current Records

- `svc-prometheus`, `svc-node-exporter`, `svc-cadvisor`, and `svc-grafana` have repository Compose evidence and are candidates for later active migration review.
- `svc-docker-api-proxy` and `svc-otel-docker-stats` have governed planned Compose definitions and are candidates for intentionally inactive planned declarations, not active status.
- All unresolved services remain unchanged until their workload form is governed.

---

## Implemented Validation Test Matrix

### Schema and Conditional Fields

- Valid legacy service.
- Valid confirmed non-container service.
- Valid active container-backed service.
- Valid intentionally inactive service and planned service.
- Valid excluded subject.
- Missing host, Compose project, Compose service, health-check requirement, policy reference, or evidence.
- Invalid participation and health-check values.
- Invalid or unsafe policy/evidence/review reference.
- Unknown extension field and unsupported version.
- Contradictory participation and field combinations.

### References and Uniqueness

- Valid and missing host reference.
- Host reference inconsistent with `host_dependencies`.
- Duplicate Compose tuple on one host.
- Same Compose service on different hosts.
- Duplicate and unique governed runtime name per host.
- Image identity retained as corroboration only.
- Policy reference resolution after policy implementation exists.

### Identity Behavior

- Runtime ID replacement preserves subject.
- Compose rename and host migration require Registry update.
- Fuzzy and partial matching rejected.
- Provider labels cannot establish canonical identity.
- Unexpected observation cannot create a Registry record.
- Replica input fails closed as unsupported in v1.

### Migration

- Deterministic idempotent migration.
- Eligible confirmed service.
- Planned service remains intentionally inactive.
- Unresolved service remains unresolved.
- No guessed value from path, name, provider label, or image.
- Reviewed inverse patch restores the prior valid record.
- Legacy records remain valid.

### Digital Twin and Regression

- All declared relationships remain valid.
- No runtime-health authority or mutation path is introduced.
- Registry remains static declared state.
- All 39 existing records validate before migration.
- Existing Registry CLI output and read-only behavior remain compatible unless separately approved.
- Repository, governance, and engineering tests remain green.

These tests prove structural integrity, deterministic declared identity, compatibility, migration safety, and fail-closed behavior. They do not prove live container identity, provider compatibility, Docker/Compose state, runtime health, policy operational suitability, dashboard behavior, remediation, or production readiness.

---

## Security and Repository Hygiene

- No credentials, secrets, tokens, socket paths, privileged endpoints, raw provider payloads, environment variables, or command arguments in identity fields.
- No absolute, traversal, symlink-escaped, or external references.
- No runtime-generated ID becomes authoritative Registry state without separate human-governed evidence.
- No automatic discovery or Registry mutation.
- No health-assessment write into Registry records.
- Deterministic, bounded validation messages without sensitive values.
- Human review for unresolved identities, exclusions, and host/Compose changes.
- Separate exact-plan approval evidence for mutation; plan status is never authorization authority by itself.

---

## Acceptance Criteria

This published specification preserves the approved baseline through these acceptance conditions:

- One existing service record remains the only canonical subject.
- Option A is implemented without parallel identity or record migration.
- Schema version `1.1` and extension contract `1.0` are explicit.
- Participation, host, Compose, runtime-name, health-check, policy, image, evidence, and exclusion semantics are bounded.
- Matching precedence is exact and provider-independent.
- Legacy compatibility and fail-closed eligibility are explicit.
- Migration is evidence-gated, idempotent, reversible, and non-live.
- Migration mutation requires a strict content-hash-bound Architecture Gatekeeper approval artifact for the exact canonical plan.
- Pi-hole known and unresolved values are distinguished without inference.
- Validation and engineering test requirements are implemented.
- PLAT-14.1A consumer and non-mutation boundaries are explicit.
- No Registry record, provider, runtime, PLAT-14.1A, or health implementation is introduced.

---

## Related Documents

- [Registry Container Identity Foundation Architecture](../architecture/Registry_Container_Identity_Foundation_Architecture.md)
- [Infrastructure Registry v1.0 Specification](Infrastructure_Registry_v1.0_Specification.md)
- [Infrastructure Registry Architecture](../architecture/Infrastructure_Registry_Architecture.md)
- [Platform Digital Twin Integrity Model](../architecture/Platform_Digital_Twin_Integrity_Model.md)
- [Container Operational Health Specification](Container_Operational_Health_Specification.md)
- [Platform Operational Evidence and Health Contract Specification](Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.3 | Recorded Architecture Gatekeeper acceptance and publication of the completed implementation while retaining separate approval-artifact, record-migration, PLAT, provider, and live-work gates. |
| 1.2 | Bound mutation authorization to a strict separate exact-plan Architecture Gatekeeper approval artifact and content hash before final publication review. |
| 1.1 | Recorded complete unpublished schema 1.1, strict validation, evidence-gated migration, rollback, CLI, and test implementation without migrating records or starting PLAT-14.1A. |
| 1.0 | Published Registry Container Identity Foundation contract, migration design, validation requirements, and future acceptance matrix without implementation authorization. |
