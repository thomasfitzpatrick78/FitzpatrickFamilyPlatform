# Registry Container Identity Foundation Architecture

**Document Version:** 1.2

**Status:** Published Architecture

**Milestone:** Milestone 14 - PLAT-14.1A prerequisite

**Implementation:** Complete; Published

---

## Purpose

This document defines the architecture options and selected direction for the Registry Container Identity Foundation required by the published PLAT-14.1A Container Operational Health specification.

The capability extends the Infrastructure Registry declared-state contract so container-backed Platform services can be identified, reconciled, and assessed consistently without coupling canonical identity to a runtime engine or telemetry provider.

The original architecture package did not implement the Registry schema, migrate records, change validation or CLI behavior, create health models, access providers, or connect to live infrastructure.

The subsequent authorized implementation package advances the additive Registry schema to `1.1`, implements strict validation and evidence-gated migration tooling, and preserves all 39 current records unchanged. Pre-publication hardening separates the immutable proposal from authorization through a strict exact-plan Architecture Gatekeeper approval artifact and content-hash binding. PLAT-14.1A, providers, health evaluation, activation, and live work remain outside the implementation.

---

## Product and Capability Boundary

### Primary Consumers

- PLAT-14.1A Container Operational Health.
- Future bounded provider adapters.
- Platform Operations reconciliation.
- Operations Analyst.
- Platform Health Dashboard.
- Future Platform APIs.

### Ownership

The Infrastructure Registry owns:

- The existing service record `id` as canonical Platform `subject_id`.
- Declared container participation.
- The governed host relationship.
- The governed Compose identity for the v1 eligible workload.
- Optional host-scoped runtime name and expected image corroboration.
- The declared health-check requirement.
- The applicable Container Operational Health policy-set reference.
- Reviewed inactivity or exclusion declarations.

The foundation does not own runtime discovery, monitoring, evidence collection, provider normalization, reconciliation outcomes, health evaluation, health status, remediation, lifecycle control, Compose deployment, Docker access, orchestration, or activation.

---

## Existing Registry Assessment

### Current Contract

The current Registry has schema ID `infrastructure_registry_v1`, schema version `1.0`, and 39 valid records. It uses flat repository-managed YAML and a deterministic bounded parser. Record IDs are globally unique. `service` and `planned_service` are already the authoritative active and intended service subject types.

Existing useful fields are:

| Existing Field | Current Use | Container Identity Use |
|----------------|-------------|------------------------|
| `id` | Globally unique record identity. | Canonical Platform `subject_id`; unchanged. |
| `record_type` | Distinguishes active and planned services from other assets. | Limits the extension to `service` and `planned_service`. |
| `name` | Human-readable display name. | Display only; never authoritative runtime matching. |
| `lifecycle_status` | `planned`, `active`, `retired`, or `replacement`. | Context only; cannot substitute for container-health participation. |
| `health_status` | Legacy repository-recorded health field. | Not an Operational Health Assessment and not written by PLAT-14.1A. |
| `host_dependencies` | Direct host relationships. | Existing topology relationship; must agree with the selected container host. |
| `service_dependencies` | Service-to-service relationships. | Preserved; not container identity. |
| `monitoring_ready` | General monitoring-readiness indication. | Insufficient for identity or health eligibility. |
| Existing image and Compose-path fields | Free-form operational context on some records. | Migration evidence only; not a normalized identity contract. |

The current parser supports scalar values and flat lists. It does not support nested mappings. Validation permits record-specific descriptive fields, validates required common fields and references, and does not yet enforce a closed container-identity namespace.

### Extension Point

Existing `service` and `planned_service` records are the correct extension point because they already own the stable service subject and host relationships. A physical device, host, provider observation, or runtime container instance must not become a second service identity.

The extension must be optional for legacy and non-container records. Absence of the extension means “not migrated or not assessed,” not “confirmed non-container.” Explicit `not_applicable` is required to record a reviewed non-container conclusion.

### Current Record Assessment

Repository evidence supports this pre-migration classification without changing any record:

| Category | Current Records | Architecture Finding |
|----------|-----------------|----------------------|
| Confirmed active container-backed | `svc-pihole-dns`, `svc-prometheus`, `svc-node-exporter`, `svc-cadvisor`, `svc-grafana` | Container use and governed host are recorded. Exact migration fields still require evidence review. |
| Confirmed planned container-backed | `svc-docker-api-proxy`, `svc-otel-docker-stats` | Repository Compose configuration identifies the planned project and service. They remain planned and inactive. |
| Confirmed non-container or logical service | `svc-docker-engine`, `svc-platform-eap`, `svc-infrastructure-registry-validation`, `svc-controlled-container-updates`, `svc-docker-container-metrics-exporter` | Runtime engine, repository capability, process, or umbrella planning record; not a container-backed assessed subject. |
| Unresolved service | `svc-pihole-raspberry-pi-rollback`, `svc-home-assistant`, `svc-home-automation-hub`, `svc-mqtt-broker`, `svc-ollama-local-ai`, `svc-platform-alerting`, `svc-platform-backup-recovery`, `svc-platform-monitoring-dashboard`, `svc-remote-management` | Repository evidence does not prove the future or current workload form sufficiently for migration. |
| Not applicable record domains | Locations, owners, devices, network devices, and hosts | These remain relationship targets, not container service subjects. |

This assessment is architecture evidence only. It is not a migration and does not establish live state.

---

## Architecture Options

### Option A - Bounded Optional Fields on Service Records

Add a closed, prefixed container identity field set directly to `service` and `planned_service` records. The fields are absent on legacy records and minimal on confirmed non-container records.

**Strengths**

- Preserves one canonical service record and subject ID.
- Fits the current flat YAML parser and record storage layout.
- Reuses existing ownership, location, lifecycle, and dependency relationships.
- Allows an additive schema change and incremental evidence-gated migration.
- Makes cross-record uniqueness and host agreement deterministic.

**Weaknesses**

- Adds optional fields to the general service record contract.
- Requires conditional validation rather than structural separation.
- Needs strict prefix ownership to avoid future field sprawl.

| Criterion | Assessment |
|-----------|------------|
| Commercial architecture alignment | High |
| Future maintainability | High |
| Code quality and rework prevention | High |
| Migration risk | Low to Medium |
| Validation complexity | Medium |
| PLAT-14.0A / PLAT-14.1A compatibility | High |

### Option B - Linked or Embedded Container Identity Profile

Keep the service record authoritative and reference or embed a separate bounded profile.

**Strengths**

- Strong conceptual separation from general service metadata.
- Could support additional workload identity variants later.
- Keeps unrelated service records visually small.

**Weaknesses**

- A linked profile introduces another identifier and reference lifecycle that can drift from the service subject.
- An embedded profile requires nested YAML support absent from the current bounded parser.
- Adds file layout, resolution, versioning, and migration complexity before the repository has multiple profile types requiring reuse.
- Increases the risk that consumers treat the profile as a parallel inventory.

| Criterion | Assessment |
|-----------|------------|
| Commercial architecture alignment | Medium |
| Future maintainability | Medium |
| Code quality and rework prevention | Medium |
| Migration risk | Medium |
| Validation complexity | High |
| PLAT-14.0A / PLAT-14.1A compatibility | Medium to High if the service ID remains authoritative |

### Option C - Independent Container Record Type

Create independent container records linked to services and hosts.

**Strengths**

- Can represent multiple runtime instances explicitly.
- Structurally separates service intent from runtime-instance metadata.

**Weaknesses**

- Blurs declared service identity and ephemeral runtime-instance identity.
- Duplicates lifecycle, ownership, host, and dependency concepts.
- Encourages runtime IDs and provider facts to become declared-state authority.
- Requires a new record type, directory, relationship rules, CLI behavior, and migration model.
- Conflicts with the approved stable service-subject architecture and is premature for deferred replicas.

| Criterion | Assessment |
|-----------|------------|
| Commercial architecture alignment | Low |
| Future maintainability | Low |
| Code quality and rework prevention | Low |
| Migration risk | High |
| Validation complexity | High |
| PLAT-14.0A / PLAT-14.1A compatibility | Low |

---

## Recommendation

Select **Option A: bounded optional container identity fields on existing `service` and `planned_service` records**.

The field set must be closed, prefixed, conditionally validated, and versioned. The Registry record remains the only service subject. The design avoids both a parallel identity profile and a runtime-instance inventory while leaving a future, evidence-driven profile extraction possible if multiple workload identity families later justify it.

The Architecture Gatekeeper approved this selection for publication. Publication is not schema implementation authorization.

---

## Identity Architecture Principles

1. `id` is the stable canonical `subject_id`.
2. A record has at most one container identity declaration in contract v1.
3. Container identity fields apply only to `service` and `planned_service`.
4. The v1 eligible identity mechanism is an exact governed Compose project/service tuple on one governed host.
5. Non-Compose workloads are not generalized. They remain explicitly excluded or unresolved until a later version defines sufficient identity.
6. A runtime name is optional, host-scoped, and lower authority than the Compose tuple.
7. Image identity corroborates but never replaces the subject and Compose tuple.
8. Runtime container IDs are evidence provenance only and are never stored as canonical identity.
9. Provider labels and resource attributes are untrusted adapter inputs.
10. Registry records are never created or mutated from runtime observations.

---

## Identity Matching Contract

Authoritative matching uses this order:

1. Exact Platform `subject_id` and valid Registry reference.
2. Exact governed subject, host, Compose project, and Compose service tuple.
3. Exact governed runtime name plus host only when repository validation proves uniqueness.
4. Expected image identity as corroboration only.
5. Runtime container ID as provenance only.
6. Provider labels and resource attributes as adapter inputs only.
7. Fuzzy, suffix, substring, case-folded, or partial matching is prohibited.

An exact match requires byte-equal validated canonical values after syntax validation; adapters do not trim, case-fold, or rewrite identifiers into a match.

### Change Scenarios

| Scenario | Required Treatment |
|----------|--------------------|
| Container recreation changes runtime ID | Same Registry subject when the governed host and Compose tuple remain exact; new runtime ID is provenance. |
| Compose service rename | Governed Registry update and validation are required. Until then, the declared subject is missing and the observation is unexpected or unresolved. |
| Service moves to another host | Review and update the container host reference and topology dependency before treating the new placement as declared state. |
| Similar names | No selection; report ambiguity. |
| Unmanaged observation | Report unexpected/unmapped observation; never create a Registry record. |
| Multiple replicas or scaled service | Deferred in v1. Additional runtime instances cannot become separate authoritative subjects or silently aggregate. |
| More than one profile for one service | Prohibited in v1. A later major contract decision is required. |

Kubernetes, cluster, scheduler, replica-set, and distributed workload identity are outside this architecture.

---

## Security and Trust Boundary

- Registry identity is governed declared state, not trusted runtime truth.
- Provider and runtime inputs are untrusted and outside this package.
- Identity records must not contain credentials, secrets, socket paths, privileged endpoints, environment values, command arguments, or raw provider payloads.
- Repository references must be relative, normalized, and constrained to approved repository locations.
- Weak provider identifiers cannot be promoted into canonical state automatically.
- Unresolved identity and exclusions require human-reviewed repository evidence.
- Registry mutation requires a repository-local approval artifact that identifies the exact canonical plan, approved Registry-migration scope, decision timestamp, Architecture Gatekeeper authority, and governed review reference; executor verification binds its exact content hash.
- No discovery, mutation, remediation, deployment, or health-state write is permitted.

---

## Work-Item Identity

Repository evidence does not establish an approved standalone PLAT or Registry work-item identifier for this prerequisite. The Architecture Gatekeeper approved retaining the descriptive name **Registry Container Identity Foundation** as a named PLAT-14.1A prerequisite. A standalone identifier remains intentionally deferred; this package does not invent one.

---

## Related Documents

- [Registry Container Identity Foundation Specification](../specifications/Registry_Container_Identity_Foundation_Specification.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)
- [Platform Digital Twin Integrity Model](Platform_Digital_Twin_Integrity_Model.md)
- [Platform Operations Domain Architecture](Platform_Operations_Domain_Architecture.md)
- [Container Operational Health Specification](../specifications/Container_Operational_Health_Specification.md)
- [ADR-006 - Registry Driven Infrastructure Foundation](decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md)
- [ADR-009 - Evidence Before Operational Health](decisions/ADR-009-Evidence-Before-Operational-Health.md)
- [ADR-010 - Declared Observed and Reconciled State](decisions/ADR-010-Declared-Observed-and-Reconciled-State.md)
- [ADR-011 - Generic Operational Evidence Envelope and Versioned Profiles](decisions/ADR-011-Generic-Operational-Evidence-Envelope-and-Versioned-Profiles.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Recorded Architecture Gatekeeper acceptance and publication of the schema, validation, migration framework, approval binding, CLI, Digital Twin compatibility, and tests without migrating records or starting PLAT-14.1A. |
| 1.1 | Added the required pre-publication exact-plan governed approval artifact boundary without changing schema, classifications, records, or PLAT scope. |
| 1.0 | Published Option A architecture; later repository implementation completed unpublished without record migration, PLAT-14.1A, provider, or live work. |
