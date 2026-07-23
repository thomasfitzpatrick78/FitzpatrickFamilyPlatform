# Privileged Proxy Implementation Architecture

**Document Version:** 1.0

**Status:** Architecture Gatekeeper Approved and Published; No Implementation or Live Authority

**Milestone:** PLAT-14.1A named prerequisite; Bravo workstream

**Architecture Snapshot:** 2026-07-23

---

## Purpose and Boundary

This document defines the exact architecture for the first future constrained proxy that may possess the Docker socket. It is a repository-only architecture and acceptance artifact. It creates no executable service, socket, listener, Docker client, image, dependency, credential, deployment, target, observation, or activation.

The selected implementation is a purpose-built minimal Linux service in Go, separate from the provider adapter. The decision extends the published Proxy and Deployment Configuration foundations; it does not replace their policy, compatibility, digest, or lifecycle authority.

The Architecture Gatekeeper approved this architecture with binding clarifications: review-time versions must be revalidated at implementation acceptance; peer credentials are only local process context; complete signed authorization and every digest remain mandatory; replay state must be durable and fail closed; non-root access may not be achieved through silent authority expansion; reserved compatibility operations remain denied; ADR-012 records architecture acceptance only; and AB-012 remains backlog.

## Governing Invariants

1. The Infrastructure Registry remains declared-identity authority.
2. Named-target authorization grants a bounded attempt; it does not alter Registry state.
3. The provider adapter cannot assign authoritative subject identity or reach Docker.
4. The proxy is the only future Docker-socket holder and cannot calculate canonical health.
5. PLAT-14.1A retains reconciliation and health authority.
6. Consumers remain read-only and provider-independent.
7. Proxy access never implies target authorization.
8. Authorization never implies evidence quality.
9. Evidence never implies health.
10. Health never implies remediation authority.

## Selected Technology

| Item | Decision | Binding rule |
|------|----------|--------------|
| Implementation | Purpose-built minimal proxy | No general reverse-proxy, Docker SDK, plugin, dynamic route, or caller-defined upstream. |
| Language | Go `1.26.5` architecture snapshot | Revalidate and approve the exact supported toolchain, source revision, maintenance, advisories, vulnerabilities, license, and end-of-life state at implementation acceptance. |
| External modules | `golang.org/x/sys` `v0.47.0` only initially | Revalidate and pin exact versions and revisions in `go.mod`/`go.sum`; any drift or additional module requires explicit review. |
| Platforms | Linux `amd64` and `arm64` candidates | Exact host architecture is selected only at deployment review. |
| Binary | Static, `CGO_ENABLED=0`, reproducible-build target | No shell, package manager, dynamic loader, or runtime code loading. |
| Final image | `scratch`, numeric non-root user where compatible with the exact approved socket model | Revalidate the base strategy and pin the OCI image and manifest by digest; no floating tag or silent root/group fallback. |
| Docker access | Direct fixed HTTP/1.1 requests over the local Docker Unix socket | No SDK negotiation or generic HTTP proxying. |
| Adapter transport | Separate filesystem Unix-domain `SOCK_STREAM` socket | No TCP, host port, loopback, HTTP server, gRPC, or network client. |
| Public protocol | Length-prefixed canonical JSON protocol v1 | One request and one response per connection; no streaming or upgrade. |
| Cryptography | Go standard `crypto/ed25519` and `crypto/sha256` | Authorization public key only in proxy configuration; no private key in proxy or repository. |

Go `1.26.5` is the reviewed architecture snapshot, not implementation authorization. At implementation acceptance the exact Go toolchain, `x/sys` and all transitive sources, Docker Engine/API compatibility, container base and image digests, maintenance, security advisories, vulnerabilities, licenses, provenance, signatures, SBOM, and end-of-life status must be revalidated and explicitly bound. The Go vulnerability database and `govulncheck` are required evidence, not substitutes for broader image and dependency scanning.

## Trust Boundaries

```text
Authority:
Infrastructure Registry
        |
        v
Named-target authorization
        |
        v
Provider adapter
        |
        v
Authenticated non-Docker Unix socket
        |
        v
Constrained privileged proxy
        |
        v
Docker Unix socket
        |
        v
Docker daemon

Evidence:
Docker daemon
        |
        v
Bounded Docker response
        |
        v
Proxy validation and field projection
        |
        v
Non-Docker proxy response
        |
        v
Adapter normalization
        |
        v
Canonical Operational Evidence
        |
        v
PLAT-14.1A reconciliation and health
        |
        v
Read-only consumers
```

| Component | Authority and responsibility | Prohibited responsibility | Failure and audit |
|-----------|------------------------------|---------------------------|-------------------|
| Registry | Canonical declared subject, host, participation, and identity tuple. | Provider access, observation, health inference, or runtime control. | Drift or ambiguity blocks authorization. |
| Authorization package | Exact subject, target, operations, signals, approval, policy/configuration/deployment/Registry/adapter/proxy/trust digests, time window, nonce, and attempt count. | Registry mutation or wildcard/population authority. | Invalid signature, expiry, replay, missing binding, or drift fails before Docker. |
| Adapter | Request bounded proxy operations; normalize constrained results. | Docker socket/API, raw routes, health calculation, subject creation, or remediation. | Emits deterministic provider failure and correlated safe audit. |
| Proxy | Authenticate adapter, validate authorization and digests, enforce operation policy, make fixed Docker requests, project response fields. | Canonical normalization, Registry authority, health, consumers, arbitrary Docker relay, or control methods. | Default deny; security-significant audit is synchronous. |
| Docker daemon | Source of untrusted runtime observations. | Authorization or canonical identity/health authority. | Errors map to bounded non-Docker reason codes. |
| PLAT-14.1A | Reconcile declared and observed identity and calculate health under published policy. | Infrastructure control or provider privilege. | Insufficient evidence remains explicit. |
| Consumers | Present or interpret governed outputs. | Direct provider access, health recalculation, or reverse control. | Contract mismatch blocks integration. |

## Public Protocol Shape

The public adapter boundary is not HTTP and contains no Docker vocabulary. Each connection carries:

1. four-byte unsigned big-endian payload length;
2. one UTF-8 canonical JSON request no larger than 16,384 bytes;
3. one four-byte length and canonical JSON response no larger than 65,536 bytes;
4. orderly close.

The proxy rejects extra frames, partial frames, invalid UTF-8, duplicate keys, unknown keys, noncanonical numbers, control characters, trailing bytes, compression, transfer encoding, and more than one request. Operation-specific response count is one even though the foundation-wide hard ceiling remains 64.

Supported operation names are `ResolveTargetIdentity`, `ObserveLifecycle`, `ObserveHealth`, `ObserveRestartInformation`, and `ObserveStatisticsOnce`. `CheckProviderCompatibility` is reserved but denied by current policy because `System` is denied. It cannot execute until a separately approved policy revision and configuration digest authorize it.

The full request/response contract is defined in the [Non-Docker Adapter Interface Specification](../specifications/Privileged_Proxy_Non_Docker_Adapter_Interface_Specification.md).

## Authentication and Authorization

### Channel Identity

- The proxy creates a second Unix socket in a dedicated runtime directory shared only with the adapter.
- The socket is owned by the proxy UID and a dedicated adapter-client GID with mode `0660`; parent directories are `0750` or stricter.
- On every accepted connection, the proxy obtains `SO_PEERCRED` and requires exact configured UID and primary GID. PID is recorded but is not stable identity by itself.
- Proxy startup and every request revalidate socket type, owner, group, mode, device/inode expectations, and absence of symlink or world access.
- Linux peer credentials establish only the local peer-process context at connection time. They neither prove source-code integrity nor independently authorize a request; restrictive socket metadata, governed service identity, signed one-shot authorization, exact target/time/operation/signal scope, and every required digest must also validate.

### Authorization Envelope

A short-lived detached Ed25519 signature covers canonical JSON containing:

- authorization version and safe reference;
- exact Registry subject and record digest;
- exact host reference and target selector;
- closed operations and signal set;
- policy, proxy configuration, deployment bundle, Registry record, adapter artifact, proxy implementation, trust-anchor, and trust-binding digests;
- `valid_from`, `valid_until`, maximum clock skew, nonce, correlation ID, and `max_attempts: 1`;
- signer identity and trust-anchor digest.

The proxy configuration contains only the approved public trust anchor and revocation metadata. The signing key and issuance process remain outside the proxy and Git. Validity may not exceed 15 minutes; accepted clock skew is at most 30 seconds. A durable bounded replay journal verifies and commits the nonce before Docker access. Replayed, expired, future, revoked, wrong-client, wrong-target, drifted, unavailable, ambiguous, corrupt, stale, or unjournalable authorization/replay state fails closed; replay protection is never best effort.

For any future IP transport, mutual TLS with a dedicated short-lived workload certificate becomes mandatory and requires a new architecture decision. Loopback, network membership, or bearer token alone is insufficient.

## Docker Socket Ownership and Mount Model

- Only the proxy container receives the host Docker Unix socket.
- The adapter, PLAT-14.1A, dashboards, APIs, EO services, and consumers never receive it.
- The future bind mount is read-only, nonrecursive where supported, and uses private mount propagation. No sibling workload shares the mount.
- A read-only Docker socket mount is not a sufficient security boundary. Docker operations can mutate the daemon through a read-only-mounted socket.
- Non-root execution is required where compatible with the exact approved host socket-ownership model. No Docker-group membership, supplemental root-equivalent group, root fallback, broader socket permission, host-user mutation, daemon reconfiguration, privileged mode, or capability expansion is preauthorized. If the approved identity cannot reach the socket without broader authority, implementation or deployment stops for architecture review.
- Startup fails if the socket is absent, is not a Unix socket, is a symlink, has unexpected owner/group, or is broader than the approved mode. Metadata is rechecked before each upstream connection and after any connection failure.
- The proxy cannot copy, bind, forward, or expose the Docker socket. It has no child-process, file-copy, general network, plugin, or mount API.
- Socket recreation invalidates readiness until ownership and inode metadata are reverified.
- Disablement stops the adapter, removes the adapter-facing socket, waits up to 15 seconds for in-flight work, then stops the proxy. Rollback selects a previously approved image and configuration digest; it never restarts or mutates observed workloads.

## Docker API Mediation

All Docker-facing values are implementation constants or are derived from already validated authorization fields. The caller can never supply a URL, path, method, query string, header, API version, request body, Docker ID, or upstream socket location.

The first implementation is pinned to one reviewed Docker API version within the exact deployment host's supported range. At this architecture snapshot Docker Engine `29.6.1` documents API `1.55` with minimum `1.40`; the deployment gate must reverify the exact host and current official API reference.

| Public operation | Policy category | Fixed conceptual Docker behavior | Target and query rule | Projected response |
|------------------|-----------------|----------------------------------|-----------------------|--------------------|
| `ResolveTargetIdentity` | `IdentityDiscovery`, conditional | Exact-filter container list, maximum two upstream candidates to detect ambiguity. | Proxy constructs canonical exact Compose label tuple or approved runtime-name filter; caller supplies neither query nor Docker ID. | Zero or one bounded identity result; duplicate/ambiguity is failure. |
| `ObserveLifecycle` | `LifecycleObservation` | Target-specific container inspection. | Docker ID comes only from successful exact resolution; fixed `size=false`. | Running/status/timestamps/exit-state fields needed for lifecycle evidence. |
| `ObserveHealth` | `HealthObservation` | Same target-specific inspection, separately projected. | Health request allowed only when authorization and Registry policy permit. | Health status and failing streak; health log/output is always removed. |
| `ObserveRestartInformation` | `RestartInformation` | Same target-specific inspection, separately projected. | Exact target only. | Restart count and bounded restart state/timestamps. |
| `ObserveStatisticsOnce` | `Statistics`, conditional | One target-specific stats read with fixed nonstreaming parameters. | `stream=false` and one-shot behavior are fixed; no caller query. | CPU/memory/PID fields required by approved mappings; network/block I/O and raw cgroup maps removed. |
| `CheckProviderCompatibility` | `System`, currently denied | Future bounded ping/version request only after policy revision. | No broad system information. | Only availability and API compatibility fields. |

### Implementation-Private Fixed Request Table

The following is privileged implementation design, not the public adapter contract. It is a 2026-07-23 Docker API `1.55` snapshot that must be reverified against the exact approved Engine before source implementation:

| Internal constructor | Exact method and path | Exact query/header/body policy | Required/removed response |
|----------------------|-----------------------|--------------------------------|---------------------------|
| `resolveTarget` | `GET /v1.55/containers/json` | Proxy-generated `all=1`, `limit=2`, and canonical `filters` containing only the exact approved Compose project/service tuple or approved exact runtime name. Fixed `Accept: application/json`; no body or caller header. | Read only ID, names, image reference/ID, state/status, and the exact three Compose identity labels. Remove ports, mounts, networks, commands, arbitrary labels, size, and host metadata. |
| `inspectTarget` | `GET /v1.55/containers/{derived-id}/json` | The path ID is obtained only from `resolveTarget`; fixed `size=false`; fixed `Accept`; no body. | Read only `Id`, `Name`, selected `Config.Image`/Compose labels, `Image`, bounded `State` fields, `RestartCount`, and health status/failing streak. Remove args, config/env, full labels, health log, host config, mounts, network settings, paths, secrets, and driver data. |
| `statsOnce` | `GET /v1.55/containers/{derived-id}/stats` | Fixed `stream=false` and `one-shot=true`; fixed `Accept`; no body. | Read only timestamps and reviewed CPU, memory, cache-basis, and PID fields. Remove network, block I/O, raw cgroup maps, names/IDs beyond safe correlation, and unapproved platform fields. |
| `ping` | `HEAD /_ping` | Reserved; no query/body. Current policy denies execution. | If later approved, retain availability and approved API header only. |
| `version` | `GET /v1.55/version` | Reserved; no query/body. Current policy denies execution. | If later approved, retain only Engine version, API version, minimum API version, OS, and architecture needed for compatibility. |

No other Docker method, route, query, header, or response projector may exist in the first implementation. Inspection is invoked separately for each authorized public operation so the public result remains operation-specific even where the same private Docker route is used.

No redirects, automatic API negotiation, retries, chunked response, informational response, compression, streaming content type, upgrade, hijack, or connection reuse is accepted. Upstream headers are not forwarded. Only status, exact content type, declared length, and approved Docker API/version headers are examined.

Docker documents that daemon control should be restricted to trusted users, that crafted API parameters can become host-level authority, and that TLS keys able to reach the daemon must be guarded like root credentials. The design therefore treats proxy compromise as residual Critical impact even after narrowing.

## Policy Enforcement Pipeline

Every request follows the same ordered pipeline:

1. accept no more than four global connections and two per service identity;
2. validate peer credentials and socket metadata;
3. read exactly one bounded frame before deadline;
4. strict-parse and canonicalize the public envelope;
5. verify protocol, operation, target, signal, and time semantics;
6. verify authorization signature, signer status, exact subject and target, validity window, expiry, nonce, approval reference, operation/signal scope, and one-shot attempt;
7. recompute and constant-time compare policy, configuration, bundle, Registry, adapter, proxy implementation, trust-anchor, and trust-binding digests;
8. evaluate the published category matrix, including conditional requirements;
9. synchronously commit authorization acceptance and nonce to audit/replay storage;
10. derive the fixed Docker request from the operation table;
11. connect only to the configured Docker Unix socket;
12. enforce upstream deadline, status, header, body-byte, nesting, and record limits;
13. strict-parse and project only approved response fields;
14. verify returned target identity matches authorization;
15. synchronously audit the decision and return one non-Docker response.

Unknown operations and future categories return `operation_denied`. Duplicate keys/parameters, alternate path encodings, wildcards, method overrides, request bodies, headers, protocol markers, and Docker-shaped strings are rejected during schema validation.

## Resource and Failure Limits

| Limit | Initial value | Failure |
|-------|--------------:|---------|
| Request bytes | 16,384 | `request_oversized` before parsing |
| Response bytes | 65,536 | `response_oversized`; no partial response |
| Operation result records | 1 | `target_ambiguous` or `record_limit_exceeded` |
| Global concurrency | 4 | `concurrency_exhausted` |
| Per-identity concurrency | 2 | `concurrency_exhausted` |
| Per-identity and per-target rate | 6 requests/minute, burst 2 | `rate_limited` |
| Total request deadline | 10 seconds | `request_timed_out` |
| Adapter-frame read | 1 second within total | `request_timed_out` |
| Docker connect | 1 second within total | `provider_unavailable` |
| Docker response | 3 seconds within total | `upstream_timed_out` |
| Retries | 0 | Caller needs new authorization when applicable |
| CPU | 250 millicores | Runtime limit; later proof required |
| Memory | 128 MiB | Runtime limit; fail closed/restart disabled |
| PIDs | 64 | Runtime limit |
| File descriptors | 64 | Runtime limit |
| Writable temporary storage | 16 MiB tmpfs | Fail closed if exhausted |
| Shutdown grace | 15 seconds | Force stop proxy after adapter disablement |

Rate and limit changes are configuration changes that require a new configuration digest and approval. Environment variables cannot override governed values.

## Runtime Security

The proxy must run non-root where compatible with the exact approved socket model, with `ALL` Linux capabilities dropped, `no-new-privileges`, a read-only root filesystem, default-deny seccomp, approved AppArmor profile, PID/CPU/memory/FD limits, no host network, no TCP capability, and an immutable image digest. Socket incompatibility must stop for review rather than trigger root, group, permission, daemon, privilege, or capability expansion. Only three paths are writable or mounted:

- the Docker socket, read-only bind, proxy-only;
- the adapter-facing runtime directory, bounded tmpfs or dedicated shared volume;
- a bounded audit/replay volume, `nodev,nosuid,noexec`, proxy append access and administrator retention ownership.

The runtime contains no shell, package manager, CA bundle, DNS configuration, service credentials, private keys, Docker CLI, or dynamic plugin path. A local self-check validates configuration, policy, trust-anchor, audit/replay availability, and socket metadata without contacting Docker.

The complete control-to-enforcement mapping is in the [Runtime Security Control Specification](../specifications/Privileged_Proxy_Runtime_Security_Control_Specification.md).

## Audit and Retention

Security-significant events are canonical JSON records with an event version, RFC 3339 UTC timestamp, monotonic sequence, correlation and request IDs, service identity, target reference, authorization reference, operation/category, decision, reason code, latency, limitation indicators, and exact policy/configuration/bundle/artifact digests.

The proxy never logs credentials, signatures, tokens, certificates, public-key material beyond its digest, raw requests, raw Docker responses, unrestricted headers, environment values, health-check output, commands, mounts, networks, or arbitrary labels.

Startup, configuration/policy load, digest verification, identity/authorization acceptance or rejection, request allow/deny, mismatch, malformed/oversize response, upstream error/timeout, audit failure, disablement, shutdown, and rollback are mandatory events. Security audit and replay-state verification/consumption must be committed before Docker access. If the audit/replay store is unavailable, ambiguous, corrupt, stale beyond policy, full, or cannot durably verify or append, the proxy denies new privileged requests and marks itself not ready. Post-access audit failure returns a provider failure and triggers independent disablement.

Safe security events are retained for 90 days. Replay entries remain through authorization expiry plus 24 hours and are compacted only through an administrator-owned reviewed process. Hash chaining detects accidental gaps but does not eliminate tampering by a fully compromised proxy; external integrity-protected aggregation remains a later activation requirement and residual risk.

## Supply Chain

Future implementation must bind:

- exact repository and source commit;
- reviewed Go patch and toolchain checksum;
- complete `go.mod`/`go.sum`;
- deterministic build inputs and flags;
- `scratch` final image and immutable multi-architecture manifest digest;
- SPDX 3.0 or CycloneDX SBOM covering source, toolchain, modules, and image;
- SLSA v1.2 provenance, minimum Build L2 and target Build L3;
- trusted builder identity and build workflow digest;
- Cosign-compatible image signature and offline-verifiable bundle;
- source, binary, dependency, image, secret, and license scans;
- Go vulnerability database and broader OSV/CVE review;
- documented rollback digest and end-of-life trigger.

Floating tags, unknown source, unpinned modules, absent SBOM, absent or unverifiable provenance/signature, unsupported Go/Docker versions, unresolved applicable Critical vulnerability, or unauthorized builder blocks privileged deployment.

## Disablement and Rollback

Disablement is independent from Docker and the observed workload:

1. reject new adapter requests;
2. stop the adapter;
3. remove or unmount only the adapter-facing Unix socket;
4. drain for at most 15 seconds;
5. stop the proxy;
6. preserve safe audit evidence;
7. revoke outstanding authorizations;
8. if rollback is approved, restore the last known-good proxy image, policy, configuration, and trust-anchor digests;
9. rerun the full negative suite before any later access.

No step restarts, stops, modifies, or redeploys the observed service. A disablement or rollback procedure that requires a Docker mutation fails acceptance.

## Lifecycle State

| Capability | State after architecture publication |
|------------|--------------------------------------|
| Provider Foundation | Published; repository-only |
| Security Review | Published |
| Proxy Foundation | Published; repository-only |
| Deployment Configuration Foundation | Published; repository-only |
| Privileged Proxy Implementation Architecture | Proposed for publication |
| Socket-capable implementation | Not authorized |
| Privileged deployment | Not authorized |
| Eligible Registry subject | Not approved |
| Named-target observation | Not authorized |
| Consumer integration | Not authorized |
| Recurring activation | Not authorized |

## Customer-Facing Impact

This architecture enables a future Platform Administrator to approve and disable a narrowly bounded provider, an Operations Analyst to receive explicit provider limitations and failures, the Platform Health Dashboard to consume canonical PLAT-14.1A outputs without Docker coupling, and future read-only operational APIs to remain provider-independent. It does not implement any consumer, dashboard, API, or FFFA change.

## External References

- [Go release history and support policy](https://go.dev/doc/devel/release)
- [Go license](https://go.dev/LICENSE)
- [Go vulnerability management](https://go.dev/doc/security/vuln/)
- [`golang.org/x/sys/unix`](https://pkg.go.dev/golang.org/x/sys/unix)
- [Linux Unix-domain peer credentials](https://man7.org/linux/man-pages/man7/unix.7.html)
- [Docker Engine security](https://docs.docker.com/engine/security/)
- [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/)
- [Docker Engine API and versioning](https://docs.docker.com/reference/api/engine/)
- [Docker Engine API version history](https://docs.docker.com/reference/api/engine/version-history/)
- [SLSA v1.2](https://slsa.dev/spec/v1.2/)
- [Sigstore image signature verification](https://docs.sigstore.dev/cosign/verifying/verify/)
- [SPDX specifications](https://spdx.dev/use/specifications/)

## Related Repository Documents

- [Architecture Decision Matrix](Privileged_Proxy_Architecture_Decision_Matrix.md)
- [ADR-012](decisions/ADR-012-Purpose-Built-Constrained-Privileged-Proxy.md)
- [Privileged Proxy Threat Model](Privileged_Proxy_Threat_Model.md)
- [Non-Docker Adapter Interface Specification](../specifications/Privileged_Proxy_Non_Docker_Adapter_Interface_Specification.md)
- [Runtime Security Control Specification](../specifications/Privileged_Proxy_Runtime_Security_Control_Specification.md)
- [Supply-Chain Security Requirements](../specifications/Privileged_Proxy_Supply_Chain_Security_Requirements.md)
- [Security Test Specification](../specifications/Privileged_Proxy_Security_Test_Specification.md)
- [Implementation Acceptance Checklist](../milestones/Milestone_14/Privileged_Proxy_Implementation_Acceptance_Checklist.md)
- [Privileged Deployment Acceptance Checklist](../milestones/Milestone_14/Privileged_Deployment_Acceptance_Checklist.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Published the Architecture Gatekeeper-approved purpose-built minimal proxy architecture with binding version, identity, replay, socket-authority, compatibility, ADR, and backlog clarifications and no implementation or live authority. |
