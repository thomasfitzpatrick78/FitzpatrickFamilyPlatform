# Privileged Proxy Source Implementation Notes

**Document Version:** 1.1

**Status:** Published Transport-Free Source; No Runtime Authority

---

## Protocol

`protocol.DecodeRequest` accepts at most 16,384 bytes and requires the bytes themselves to be canonical JSON. It rejects invalid UTF-8, a byte-order mark, duplicate or unknown fields, trailing values, `null`, floats, exponents, negative zero, noncanonical key order, excessive nesting/collections, and strings outside bounded canonical ASCII. Restricting security-relevant identifiers to ASCII makes accepted strings NFC-stable and rejects Unicode confusables rather than normalizing ambiguous values.

Response encoding is deterministic and bounded to 65,536 bytes. Public structs are operation-specific and contain no arbitrary metadata or provider maps.

## Authorization and Digest Binding

The standard library verifies detached base64url Ed25519 signatures. Synthetic private keys are generated only in tests. The signed content binds:

- authorization reference/version, signer, key identifier, algorithm, approval, correlation, nonce, and exact one-shot attempt;
- adapter identity;
- exact subject, host, Registry digest, selector kind, Compose tuple or governed runtime name;
- sorted operation and signal scopes;
- validity window;
- Registry, policy, proxy configuration, deployment bundle, adapter artifact, proxy implementation/source, trust-anchor, and trust-binding digests.

Digest comparisons require the repository-standard lowercase SHA-256 representation and exact constant-time byte equality. No prefix, wildcard, case-folding, missing-binding, or caller-selected trust anchor is accepted.

## Replay Journal

`Journal.CheckAndConsume` is atomic within each implementation. The memory journal uses a mutex and deterministic expiration-plus-retention compaction. The ordinary-file test journal:

- uses an explicit absolute test root and safe basename;
- rejects symlinks, non-regular files, oversized state, noncanonical JSON, unknown fields, invalid checksum, stale/backward time, duplicate bindings, over-capacity state, and residual partial replacement;
- writes a same-directory exclusive `.pending` file, synchronizes it, replaces the state atomically, and synchronizes the directory;
- never silently resets corrupt or unavailable state.

An authorization reference or nonce can appear only once. Expiration does not permit reuse until the configured retention interval has elapsed. This implementation is not production persistence approval.

## Fixed Dispatch and Synthetic Upstream

The dispatcher is a compile-time `switch` over five operations. Each branch calls one typed method on `Observer`. The interface exposes no generic request and cannot represent transport or Docker protocol elements. Unknown and reserved operations deny without invocation.

## Response Projection

`projection.Project` requires the returned synthetic subject and host to match the exact derived target. It accepts exactly one matching operation result, at most one record, a bounded provider-version identifier, and a unique deterministic limitation set. A second result type, unexpected-field marker, target substitution, excessive count, malformed record, or oversized final response rejects the entire response.

## Resource Policy

The repository model binds global concurrency 4, per-identity concurrency 2, six requests per minute with burst 2 per identity/target, total timeout 10 seconds, upstream timeout abstraction 3 seconds, result count 1, shutdown grace 15 seconds, replay retention 24 hours after expiry, and audit retention 90 days. Injected clocks avoid real sleeps. No goroutine server, cgroup, process-limit, host, or runtime enforcement exists.

## Audit and Failure

Audit events are typed canonical records with sequence, timestamp, correlation/request IDs, service/authorization/subject/target references, operation/category, decision/reason, logical latency, limitations, and required policy/configuration/deployment/implementation digests. Event structs have no signature, token, key, raw request/response, environment, command, mount, network, label, or provider-error field.

Failure reason codes are stable and map to nonsecret safe messages. Pre-access audit failure prevents synthetic upstream invocation. Post-access audit failure returns `audit_unavailable` and disables the core. The nonce remains consumed after any later attempt-equivalent failure.

## Modeled Now vs. Later Proof

The source models security ordering and state transitions only. Unix framing, real peer credentials, Docker requests/responses, OS confinement, production durability, image composition, and artifact supply-chain proof must be tested again at their separately authorized gates.

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded Architecture Gatekeeper-approved source publication while preserving all later transport, artifact, and deployment proof. |
| 1.0 | Documented the canonical protocol, authorization, replay, dispatch, projection, resource, audit, and fail-closed source design. |
