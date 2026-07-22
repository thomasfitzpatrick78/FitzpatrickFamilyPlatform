# Production Provider Adapter Contract Specification

**Document Version:** 1.0

**Status:** Accepted and Published; Contract Only; Implementation and Live Access Unauthorized

**Contract:** Production Provider Adapter Contract v1.0

**Milestone:** PLAT-14.1A named prerequisite

---

## Purpose

This specification defines a strict, provider-independent boundary for a future production provider adapter. It governs adapter identity, named-target authorization input, provider observation results, normalization results, deterministic provider failures, provenance, limitations, compatibility, and security behavior.

It does not define provider endpoint paths, credentials, deployment configuration, a selected target, a production implementation, health evaluation, or live access.

---

## Contract Principles

1. The Registry supplies canonical subject identity and declared target attributes.
2. The authorization input is explicit, bounded, versioned, and non-wildcard.
3. Provider responses are untrusted and must be strictly parsed.
4. An adapter returns canonical evidence records or a deterministic provider failure result.
5. A provider failure is evidence about observation capability, not proof of service failure.
6. Provider identity, labels, runtime IDs, and image identity are observation inputs and provenance only.
7. The adapter never emits an Operational Health status or mutates Registry state.
8. Raw provider payloads are external, minimized, redacted, and represented by a safe digest/reference when retained.
9. Unsupported versions, unknown required semantics, unsafe references, oversize input, ambiguity, and secret-like content fail closed.
10. The same validated input, provider response, and evaluation time produce deterministic output.

---

## Result Types

The top-level result contains exactly one of:

- `observation_result`: a valid bounded provider observation plus zero or more canonical one-signal evidence records; or
- `failure_result`: a deterministic provider failure with no misleading canonical subject-health evidence.

Both result types carry contract version, correlation, adapter identity, authorization reference, target reference, timing, provider provenance, limitations, and safe audit metadata.

---

## Adapter Identity

| Field | Requirement | Contract |
|-------|-------------|----------|
| `contract_version` | Required | Exact supported Production Provider Adapter Contract version; initial value `1.0`. |
| `adapter_id` | Required | Stable governed adapter identifier; not dynamically discovered. |
| `adapter_name` | Required | Human-readable bounded name. |
| `adapter_version` | Required | Immutable build/version identifier. |
| `adapter_artifact_digest` | Required for implementation/live gates | Approved artifact or image SHA-256/digest. |
| `provider_type` | Required | Governed provider category such as constrained Docker API or bounded OTel/Prometheus transport. |
| `provider_api_version` | Required | Exact response contract/version interpreted by the adapter. |
| `supported_provider_versions` | Required | Closed supported-version set or bounded rule. |
| `supported_evidence_contract_versions` | Required | Initial Generic Operational Evidence Envelope value `1.0`. |
| `supported_profile_versions` | Required | Initial Container Evidence Profile value `1.0`. |
| `supported_signal_names` | Required | Closed canonical signal set the adapter may emit. |
| `configuration_digest` | Required for live gates | Digest of reviewed nonsecret adapter configuration. |

Adapter identity does not confer provider access or production authority.

---

## Authorized Target Input

| Field | Requirement | Contract |
|-------|-------------|----------|
| `authorization_reference` | Required | Repository-safe reference to the exact future named-target authorization package. |
| `authorization_digest` | Required | SHA-256 of the reviewed authorization content. |
| `authorization_valid_from` / `authorization_valid_until` | Required | Time-bounded authorization window. |
| `observation_mode` | Required | Initial allowed value `named_target_one_shot`; a bounded `named_target_window` requires explicit authorization. |
| `subject_id` | Required | Existing canonical Registry record ID. |
| `registry_reference` | Required | Safe repository-relative Registry record path. |
| `registry_record_digest` | Required | Exact reviewed declared-state bytes. |
| `host_reference` | Required | Governed Registry host reference. |
| `compose_project` / `compose_service` | Conditional | Exact declared values when Compose manages the subject. |
| `governed_runtime_name` | Conditional | Exact declared fallback only where policy permits and uniqueness is proven. |
| `expected_image_reference` / `expected_image_digest` | Optional | Corroboration only; never sole canonical match. |
| `health_check_requirement` | Required | Registry value `required`, `optional`, or `not_applicable`. |
| `requested_signals` | Required | Nonempty closed subset of the adapter's supported signals. |
| `mandatory_signals` | Required | Exact subset required for this observation and approved policy. |
| `observation_window_start` / `observation_window_end` | Required for window mode | Bounded, timezone-aware, within authorization validity. |
| `provider_boundary_reference` | Required | Exact reviewed proxy/collector/provider configuration reference and digest. |
| `output_reference` | Required | Safe approved runtime or repository-fixture output boundary; live raw payload paths are not repository paths. |

Validation rules:

- Wildcards, arbitrary provider URLs, unbounded target lists, empty targets, fuzzy names, and provider-created subjects are prohibited.
- The subject, host, participation, health-check requirement, and declared identity must agree with the exact Registry record.
- A `not_applicable`, intentionally inactive, excluded, unresolved, invalid, or unapproved Registry subject cannot enter a live active-health observation.
- Requested signals must be approved for the provider/version and must include every mandatory signal.
- Authorization expiry, digest drift, target drift, boundary drift, or unsupported mode fails before connection.

---

## Provider Observation Result

| Field | Requirement | Contract |
|-------|-------------|----------|
| `provider_observation_id` | Required | Deterministic or unique observation identifier scoped to authorization and collection. |
| `correlation_id` | Required | Safe identifier shared across adapter audit events and derived records. |
| `adapter_id` / `adapter_version` | Required | Exact producing adapter. |
| `provider_type` / `provider_id` / `provider_version` | Required | Exact observed provider provenance. |
| `collection_started_at` / `collection_ended_at` | Required | Timezone-aware collection bounds. |
| `observed_at` | Required per observation | Provider-represented time; not silently replaced with collection time. |
| `observation_window_start` / `observation_window_end` | Conditional | Required for windowed signals. |
| `target_resolution_result` | Required | `exact`, `absent`, `conflicting`, `duplicate`, `ambiguous`, or `unresolved`. |
| `observed_identity` | Required | Bounded runtime ID/name, Compose label values, image values, and host/provider context actually observed. |
| `raw_response_digest` | Required when provider bytes were received | SHA-256 of exact received bytes before disposal/redaction. |
| `raw_response_reference` | Optional | Approved access-controlled runtime reference; never an arbitrary or secret-bearing path. |
| `requested_signals` / `returned_signals` | Required | Exact requested and successfully parsed canonical signal sets. |
| `missing_expected_signals` | Required; may be empty | Requested signals not validly returned. |
| `provider_limitations` | Required; may be empty | Closed limitation codes with affected signals and support references. |
| `collection_coverage` | Required | `complete`, `partial`, `none`, or `not_assessable` for the authorized scope. |
| `provider_confidence` | Required | Adapter-derived `high`, `medium`, `low`, or `none` suitability for the observation, never copied from the provider. |
| `provider_confidence_reasons` | Required | Deterministic version/coverage/directness/limitation reasons. |
| `warnings` | Required; may be empty | Closed safe warning codes. |
| `evidence_records` | Required; may be empty | Strict Generic Operational Evidence Envelope `1.0` plus Container Evidence Profile `1.0` records. |

`provider_confidence` is an adapter-contract assessment of source suitability. It is not canonical `evidence_confidence`, assessment confidence, or health. PLAT-14.1A applies the published confidence policy to canonical evidence and may classify it lower.

---

## Observed Identity Contract

The bounded identity object may contain only:

- Runtime container ID.
- Runtime/container name.
- Compose project label.
- Compose service label.
- Compose container-number label when requested.
- Image reference and digest.
- Governed host/provider context.

Each field records `present`, `absent`, `conflicting`, or `unsupported`. Raw label maps, fuzzy-match candidates, environment variables, command arguments, mounts, arbitrary paths, and network configuration are prohibited.

Exact target resolution requires the published PLAT-14.1A matching precedence. Scaled/replicated observations are `duplicate` or `ambiguous` in v1 unless a future profile explicitly governs replica identity.

---

## Canonical Signal Normalization

The adapter may emit only approved Container Evidence Profile signals. Provider metric names, endpoint names, labels, and units do not become canonical semantics.

For each evidence record the adapter must:

- Bind the authorized `subject_id`, `registry_reference`, and governed host.
- Retain provider and runtime identity as provenance.
- Convert values and units under a versioned mapping rule or reject them.
- Record observation, collection, normalization, and window timestamps.
- Derive freshness and completeness only under the referenced published policy.
- Record expected-signal availability, coverage, and limitations.
- Exclude raw payloads, credentials, secret-like data, and arbitrary provider metadata.

The adapter must never emit `container.lifecycle.expected_state`, which remains a Registry-derived declaration.

---

## Deterministic Failure Result

| Field | Requirement | Contract |
|-------|-------------|----------|
| `failure_category` | Required | One bounded category below. |
| `failure_code` | Required | Stable machine-readable code. |
| `safe_message` | Required | Secret-free bounded description. |
| `retryability` | Required | `not_retryable`, `retryable_within_window`, or `new_authorization_required`. |
| `affected_signals` | Required; may be empty | Canonical signals not collected or validated. |
| `provider_available` | Required | `available`, `unavailable`, `degraded`, or `unknown`. |
| `target_resolution_result` | Required when resolution began | Same bounded identity result set. |
| `collection_started_at` / `failed_at` | Required | Timezone-aware failure timing. |
| `provider_limitations` | Required; may be empty | Applicable known limitations. |
| `audit_correlation_id` | Required | Safe log correlation. |

Initial categories:

- `provider_unavailable`
- `authorization_denied`
- `authorization_expired_or_drifted`
- `target_not_visible`
- `target_ambiguous`
- `provider_version_unsupported`
- `response_malformed`
- `response_oversized`
- `content_type_unsupported`
- `signal_unsupported`
- `collection_timed_out`
- `partial_response`
- `provider_limitation`
- `adapter_internal_validation_failure`
- `unsafe_reference_or_path`
- `secret_like_content_detected`

A failure result may support canonical telemetry-availability evidence only when the contract safely establishes provider availability, requested-signal availability, coverage, or a limitation for the already authorized subject. It must not produce lifecycle or health-check facts that were not observed.

---

## Security and Resource Limits

Each adapter implementation must define and test:

- Connection, response, and total collection timeouts.
- Bounded retry count and backoff that cannot exceed the authorization window.
- Maximum request and response bytes.
- Maximum record, evidence-set, identity-field, warning, limitation, and log-event counts.
- Exact accepted content types and encodings.
- Strict JSON shape and unknown-field behavior.
- Redirect prohibition unless explicitly reviewed.
- Path traversal, absolute path, symlink, control-character, and secret-like content rejection.
- No shell, subprocess, dynamic command, code loading, reflection, plugin discovery, or arbitrary URL construction.
- No automatic Registry write, health write, remediation, deployment, or infrastructure mutation path.

Unknown provider fields are rejected when they affect required semantics. Explicitly allowed ignorable provider fields may be discarded only under a versioned mapping contract and must never pass through to canonical evidence.

---

## Secrets and Authentication

Credentials, if required, are referenced by an approved runtime secret identifier and delivered outside Git. Contract input and output contain only the secret reference classification, never the secret value.

- Least scope and named-boundary access are required.
- Rotation and revocation procedures must exist before live access.
- Missing, expired, revoked, or unreadable credentials fail closed as `authorization_denied` or `provider_unavailable` without logging the credential.
- Authentication headers, certificates, tokens, and secret values are excluded from raw digests only when canonical byte retention is impossible; the handling rule must be explicit and reproducible.

---

## Compatibility and Versioning

- Unsupported contract or provider major versions fail closed.
- Backward-compatible optional contract fields require a minor version.
- Changed field meaning, required behavior, failure category semantics, or authority boundary requires a major version.
- Provider upgrades require fixture refresh, support-matrix review, mapping regression tests, and security review before use.
- Every output preserves adapter, provider, evidence contract, profile, policy, authorization, configuration, and Registry record versions/digests.

The architecture intentionally defers exact Docker endpoint paths and provider field names until an implementation gate verifies current official contracts.

---

## Audit Events

Contract-conformant implementations emit secret-safe events for adapter start/version, authorization accepted/rejected, provider connected/denied, target resolved/unresolved, collection complete/partial/timeout, response rejected, evidence normalized/rejected, limitation recorded, version mismatch, output written, and no Registry mutation attempted.

---

## Acceptance Fixtures for a Future Implementation Gate

Fixture and bounded mock-provider tests must prove:

- Exact named-target success for every mandatory signal.
- Optional and required health-check behavior.
- Equivalent provider shapes normalize to equivalent canonical signals.
- Wrong target, ambiguous target, duplicate target, and unexpected target fail safely.
- Wrong authority, expired authorization, digest drift, and wildcard target fail before connection.
- Unsupported versions, content types, unknown required fields, malformed values, oversize payloads, timeouts, and partial responses produce intended categories.
- Provider failure never produces false service health.
- Raw secrets, commands, environment values, mounts, paths, and arbitrary labels do not enter canonical evidence or logs.
- Repeated identical inputs are byte-stable.
- No network, Docker, provider, Registry, health, deployment, execution, or mutation behavior exists in repository tests.

---

## What Contract Acceptance Proves

Acceptance proves strict repository behavior, deterministic failure semantics, bounded authority, provider-independent normalization, provenance, and safe fixture/mock behavior. It does not prove privileged deployment safety, current provider compatibility, target eligibility, production freshness, Docker-host isolation, Pi-hole non-regression, recurring operation, consumer correctness, or live readiness.

---

## Related Documents

- [Production Provider Adapter Architecture](../architecture/Production_Provider_Adapter_Architecture.md)
- [Privileged-Access Security Design and Threat Model](../architecture/Production_Provider_Privileged_Access_Security_Design.md)
- [Platform Operational Evidence and Health Contract Specification](Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Container Operational Health Specification](Container_Operational_Health_Specification.md)
- [Privileged Infrastructure Integration Standard](../governance/Privileged_Infrastructure_Integration_Standard.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Accepted and published Production Provider Adapter Contract covering adapter identity, named-target input, observation output, deterministic failures, provenance, limitations, compatibility, security, and acceptance fixtures; implementation and live access remain unauthorized. |
