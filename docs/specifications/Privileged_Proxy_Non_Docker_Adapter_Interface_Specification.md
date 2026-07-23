# Privileged Proxy Non-Docker Adapter Interface Specification

**Document Version:** 1.0

**Status:** Published Architecture Contract; No Runtime Authority

**Contract:** Privileged Proxy Adapter Protocol v1.0

**Milestone:** PLAT-14.1A named prerequisite

---

## Purpose

This specification defines the future adapter-to-proxy protocol. It is intentionally not HTTP and cannot express a Docker path, method, query, header, body, socket, or upstream. It is a repository-only contract and does not create a listener or client.

## Transport

- Linux filesystem Unix-domain `SOCK_STREAM` socket only.
- Four-byte unsigned big-endian length followed by one canonical UTF-8 JSON object.
- One request and one response per connection; the proxy closes after the response.
- Maximum request 16,384 bytes; maximum response 65,536 bytes.
- No compression, streaming, multiplexing, chunking, continuation, upgrade, trailers, file descriptors, or ancillary caller data.
- Adapter read/write deadline and total proxy deadline are bounded by 10 seconds.
- Missing, extra, partial, duplicate, noncanonical, or trailing content fails closed.

Canonical JSON uses UTF-8, lexicographically sorted object keys, compact separators, NFC-normalized strings, integer numbers only, lowercase enum/value forms where this contract specifies them, and no insignificant whitespace. Duplicate keys, floats, exponents, negative zero, byte-order marks, and alternate Unicode forms are rejected before signature or digest verification. The repository-standard SHA-256 content-binding rule is reused; this contract does not create a second digest authority.

## Request Envelope

| Field | Type | Requirement |
|-------|------|-------------|
| `protocol_version` | string | Exact `1.0`. |
| `request_id` | string | 16-64 lowercase hex characters; unique for the attempt. |
| `correlation_id` | string | 16-64 lowercase hex characters shared with adapter evidence/audit. |
| `operation` | enum | One value from the operation table. |
| `requested_at` | RFC 3339 UTC string | Required; within authorization and 30-second skew. |
| `deadline` | RFC 3339 UTC string | Required; no more than 10 seconds after accepted request. |
| `target` | object | Exact governed target fields below. |
| `requested_signals` | array of enum | Closed, operation-compatible, no duplicates. |
| `authorization` | object | Exact signed authorization content and detached signature reference. |
| `policy_digest` | SHA-256 string | Exact approved Proxy Foundation policy digest. |
| `configuration_digest` | SHA-256 string | Exact approved proxy configuration digest. |
| `deployment_bundle_digest` | SHA-256 string | Exact approved deployment bundle digest. |
| `adapter_artifact_digest` | SHA-256 string | Exact approved adapter implementation digest. |
| `proxy_implementation_digest` | SHA-256 string | Exact future accepted proxy artifact digest. |
| `trust_binding_digest` | SHA-256 string | Exact approved binding of trust anchor, signer, service identities, and authorization policy. |

Unknown fields are rejected. A field cannot be `null` unless explicitly allowed; protocol v1 defines no nullable request field.

## Target Object

| Field | Requirement |
|-------|-------------|
| `subject_id` | Exact existing Registry record ID from authorization. |
| `registry_reference` | Safe repository identity reference, not a runtime path. |
| `registry_record_digest` | SHA-256 of exact approved Registry record content. |
| `host_reference` | Exact governed host record ID. |
| `selector_kind` | `compose_identity` or `governed_runtime_name`; selected by authorization. |
| `compose_project` | Required only for `compose_identity`; exact non-wildcard value. |
| `compose_service` | Required only for `compose_identity`; exact non-wildcard value. |
| `governed_runtime_name` | Required only for the separately approved unique-name fallback. |
| `expected_image_reference` | Optional corroboration, never authoritative alone. |
| `expected_image_digest` | Optional corroboration, never authoritative alone. |

The adapter does not send a Docker container ID, provider URL, Docker label map, filter, query, path, method, or header. The proxy derives the private fixed Docker selector after authorization.

## Operations

| Operation | Category | Authorization | Signals and result |
|-----------|----------|---------------|--------------------|
| `ResolveTargetIdentity` | `IdentityDiscovery` | Conditional; exact target only | Bounded identity projection or absent/ambiguous failure. |
| `ObserveLifecycle` | `LifecycleObservation` | Allowed category plus exact target authorization | `container.lifecycle.observed_state`. |
| `ObserveHealth` | `HealthObservation` | Allowed category and Registry health-check policy | `container.healthcheck.state`; no health log/output. |
| `ObserveRestartInformation` | `RestartInformation` | Allowed category plus exact target authorization | `container.restart.count`, `container.restart.occurred`. |
| `ObserveStatisticsOnce` | `Statistics` | Conditional and signal-specific | Approved CPU/memory/PID-derived fields; one shot only. |
| `CheckProviderCompatibility` | `System` | **Denied under current policy v1.0** | Reserved schema only; cannot execute until policy/configuration approval changes. |

Unknown operations and `Events`, logs, attach, exec, archive, filesystem, images, volumes, networks, build, plugins, Swarm, broad system information, configuration, or any future category return `operation_denied`.

## Authorization Object

The authorization object contains the exact signed content:

| Field | Rule |
|-------|------|
| `authorization_version` | Exact `1.0`. |
| `authorization_reference` | Safe governed reference. |
| `authorization_digest` | SHA-256 of canonical authorization content excluding the detached signature. |
| `signer_identity` | Approved bounded signer identifier. |
| `trust_anchor_digest` | Exact configured Ed25519 public-key digest. |
| `adapter_identity` | Exact permitted service identity and artifact digest; peer credentials alone are insufficient. |
| `allowed_operations` | Closed nonempty operation set. |
| `allowed_signals` | Closed signal set. |
| `subject_id`, `host_reference`, `registry_record_digest` | Exact target binding. |
| `policy_digest`, `configuration_digest`, `deployment_bundle_digest`, `registry_record_digest`, `adapter_artifact_digest`, `proxy_implementation_digest`, `trust_binding_digest` | Exact content binding. |
| `valid_from`, `valid_until` | UTC; validity no longer than 15 minutes. |
| `nonce` | 32-byte cryptographically random value encoded as lowercase hex by the future issuer. |
| `max_attempts` | Exact integer `1`. |
| `signature` | Base64url Ed25519 signature over canonical content; never logged. |

The proxy never accepts an unsigned authorization, a caller-selected trust anchor, a reusable bearer token, or a signature over a digest other than the parsed canonical content.

## Response Envelope

| Field | Requirement |
|-------|-------------|
| `protocol_version` | Exact `1.0`. |
| `request_id` / `correlation_id` | Exact request values. |
| `operation` | Exact accepted operation. |
| `decision` | `allowed`, `denied`, or `failed`. |
| `reason_code` | One stable code from this contract. |
| `proxy_identity` | Approved proxy ID, version, artifact digest, and configuration digest. |
| `target_reference` | Subject and host only; no Docker path or caller-usable provider address. |
| `provider_api_version` | Exact version used, when a provider response was received. |
| `started_at` / `completed_at` | RFC 3339 UTC. |
| `limitations` | Closed list, possibly empty. |
| `result` | Exactly one operation-specific object for `allowed`; absent otherwise. |
| `audit_correlation_id` | Safe reference to mandatory audit records. |

The response contains no raw Docker body, Docker URL/path, raw labels, headers, environment, command, mount, network, health-check output, secret, or arbitrary provider field.

## Operation Results

### Identity

Only the following fields may appear: `resolution` (`exact`, `absent`, `duplicate`, `ambiguous`, `conflicting`), bounded runtime ID digest/reference, bounded runtime name, exact observed Compose project/service/container number states, image reference/digest states, and provider context. At most one exact record is returned.

### Lifecycle

Only bounded lifecycle state, running/paused/restarting/dead/OOM indicators, exit code, start and finish timestamps, and observation timestamp may appear. Engine error strings are excluded.

### Health

Only configured-state indicator, health state, failing streak, and observation timestamp may appear. Health check commands, logs, outputs, environment, and raw probe data are excluded.

### Restart

Only restart count, restart-occurrence indicator, bounded restart state, and observation timestamp may appear.

### Statistics

Only the reviewed one-shot CPU totals/deltas, online CPU count, memory usage/limit/cache basis, PID count, read timestamp, cgroup-mode limitation, and calculation-input completeness may appear. Network, block-I/O, raw cgroup maps, per-process data, and streams are excluded.

### Compatibility

Reserved fields are availability and bounded Engine/API compatibility identifiers. The operation remains denied under current policy.

## Reason Codes

| Class | Codes |
|-------|-------|
| Identity/authentication | `identity_missing`, `identity_mismatch`, `identity_revoked`, `authorization_missing`, `authorization_invalid`, `authorization_expired`, `authorization_future`, `authorization_replayed`, `authorization_revoked` |
| Content binding | `policy_digest_mismatch`, `configuration_digest_mismatch`, `deployment_digest_mismatch`, `registry_digest_mismatch`, `adapter_digest_mismatch`, `proxy_digest_mismatch`, `trust_anchor_mismatch`, `trust_binding_digest_mismatch` |
| Request | `request_malformed`, `request_oversized`, `unknown_field`, `duplicate_field`, `protocol_unsupported`, `operation_denied`, `category_denied`, `target_invalid`, `target_mismatch`, `wildcard_denied`, `signal_denied`, `deadline_invalid` |
| Capacity | `rate_limited`, `concurrency_exhausted`, `request_timed_out`, `audit_unavailable` |
| Provider | `provider_unavailable`, `provider_version_unsupported`, `upstream_timed_out`, `upstream_protocol_rejected`, `response_malformed`, `response_oversized`, `response_field_rejected`, `record_limit_exceeded`, `target_absent`, `target_duplicate`, `target_ambiguous`, `target_conflicting` |
| Lifecycle | `proxy_disabled`, `rollback_required`, `internal_fail_closed` |
| Success | `request_completed` |

Every denial/failure returns a nonsecret safe message selected by reason code; provider-supplied error strings never pass through.

## Replay and Idempotency

- Observation operations do not mutate Docker and are semantically read-only.
- An authorization is one-shot, not retry-idempotent. Once its nonce is durably accepted, reuse is denied even when the first provider call fails.
- A retry requires a new request ID and new authorization nonce.
- Duplicate request IDs under the same correlation ID are denied.
- Restart reloads and verifies the durable replay journal before readiness. Unavailable, ambiguous, corrupt, stale beyond policy, or unsuccessful replay-state verification or persistence prevents privileged requests; replay protection is never best effort.

## Failure Rules

- Schema, identity, authorization, policy, digest, rate, and audit failures occur before Docker access.
- Unknown operations always deny and never fall back to raw provider handling.
- Oversized or uninspectable provider responses are wholly rejected; no truncation is represented as success.
- Target mismatch after response parsing invalidates the whole result.
- A failure response is provider-boundary evidence only; it is not service health.

## Acceptance

The contract passes only when canonical test vectors prove byte-stable serialization, strict duplicate/unknown-field rejection, no Docker-shaped public fields, exact operation-to-category mapping, one-shot replay behavior, bounded error handling, and complete response projection.

## Related Documents

- [Privileged Proxy Implementation Architecture](../architecture/Privileged_Proxy_Implementation_Architecture.md)
- [Security Test Specification](Privileged_Proxy_Security_Test_Specification.md)
- [Production Provider Adapter Contract](Production_Provider_Adapter_Contract_Specification.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Published the non-Docker length-prefixed JSON adapter protocol with complete authorization/digest binding and durable fail-closed replay requirements, without transport implementation. |
