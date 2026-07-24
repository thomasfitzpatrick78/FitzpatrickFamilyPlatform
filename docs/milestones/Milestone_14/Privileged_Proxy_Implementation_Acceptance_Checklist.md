# Privileged Proxy Implementation Acceptance Checklist

**Document Version:** 1.2

**Status:** Published Future Gate; No Implementation Accepted

**Milestone:** PLAT-14.1A named prerequisite

---

## Purpose

This checklist governs a future socket-capable implementation acceptance review. Completion makes an artifact eligible for privileged deployment review only. It does not authorize deployment, a target, observation, consumers, recurrence, or activation.

The transport-free source review tree supplies partial evidence. A checked item below means that exact source-level statement is proven; it does not waive the remaining socket, Docker, runtime, artifact, or Architecture Gatekeeper requirements.

## Architecture and Interface

- [x] Source conforms to ADR-012 and the selected purpose-built minimal design.
- [ ] Proxy and adapter are separate processes, artifacts, identities, and lifecycle units.
- [ ] Adapter has no Docker socket, Docker API, Docker SDK, or arbitrary provider path.
- [ ] Public protocol conforms byte-for-byte to Privileged Proxy Adapter Protocol v1.0.
- [x] Public request contains no Docker URL, path, method, query, header, body, ID, or socket.
- [x] Static route/operation graph proves no arbitrary Docker relay or generic reverse-proxy behavior.
- [x] `System` compatibility operation remains denied unless a separately approved policy revision exists.
- [x] Registry, adapter, PLAT-14.1A, and consumer authority boundaries remain unchanged.

## Policy and Data Enforcement

- [x] Complete published category matrix is implemented from the authoritative policy, not duplicated.
- [x] Unknown and future categories default deny.
- [ ] Exact target, wildcard denial, canonical normalization, duplicate rejection, and query derivation pass.
- [ ] Only fixed read methods and request constructors are reachable.
- [ ] Streaming, upgrade, hijack, tunneling, redirects, retries, and connection reuse are absent or denied.
- [ ] Operation-specific response allowlists are complete for every supported Docker API version.
- [ ] Response size, depth, count, content type, version, and target revalidation pass.
- [ ] Canary secrets, health output, environment, commands, mounts, networks, and raw labels never pass.

## Identity and Authorization

- [ ] Exact Unix socket owner/group/mode and `SO_PEERCRED` verification pass, with evidence that peer credentials establish context but never complete authorization alone.
- [ ] Dedicated numeric service identity and exact socket-access model are documented; no Docker-group, supplemental root-equivalent group, root fallback, broader socket permission, host-user/daemon mutation, privileged mode, or capability expansion is implicit.
- [ ] Authorization signature, approval reference, trust anchor, time window, nonce, one-shot attempt, operation, signal, subject, target, and every policy/configuration/deployment/Registry/adapter/proxy/trust-binding digest pass.
- [ ] Expiry, future time, replay across restart, revocation, wrong client, wrong target, and signer rotation pass.
- [x] No private key, bearer credential, certificate, or secret enters source, image, environment, audit, or repository.

## Runtime Security

- [ ] Non-root, capability drop, no privilege escalation, read-only root, seccomp, AppArmor, and exact writable paths pass.
- [ ] CPU 250m, memory 128 MiB, PIDs 64, FDs 64, concurrency 4/2, rate 6/minute burst 2, and timeouts pass.
- [ ] Image contains only the expected static binary and immutable nonsecret files.
- [ ] No IP network, host network, TCP/UDP listener/client, shell, subprocess, plugin, or dynamic code path exists.
- [ ] Docker socket is visible only to the proxy and cannot be propagated.
- [ ] Socket recreation and permission drift fail closed.
- [ ] Restart policy is disabled and health check does not contact Docker.

## Audit and Failure

- [ ] Every mandatory event, field, reason code, correlation, latency, and digest is correct.
- [x] Credentials, signatures, raw payloads, provider errors, and sensitive metadata never log.
- [ ] Audit/replay durability, ambiguity, staleness, full/corrupt/unavailable behavior, retention, restart recovery, and sequence checks pass with no best-effort fallback.
- [ ] Audit loss before access prevents Docker interaction; loss after access returns failure and disables.
- [ ] Provider failure never becomes service-health evidence.
- [ ] All errors are bounded, deterministic, secret-safe, and fail closed.

## Tests and Supply Chain

- [ ] Every positive test passes.
- [ ] Every negative test passes with exact reason code and audit evidence.
- [ ] Fuzz corpus covers both protocol boundaries and all parsers/projectors.
- [x] Static prohibited-capability and dependency checks pass.
- [ ] Exact source revision, Go toolchain, `go.mod`, `go.sum`, and build workflow are approved.
- [ ] Review-time Go, `x/sys`, Docker API, container-base, and supply-chain selections are revalidated and rebound to exact supported versions, revisions, digests, maintenance, advisories, vulnerabilities, licenses, provenance, signatures, SBOM, and end-of-life status; all drift has explicit approval.
- [ ] Two isolated builds reproduce the accepted binary and image digests.
- [ ] Immutable image/manifest digest, complete SBOM, SLSA provenance, and signature verify independently.
- [ ] Vulnerability, secret, license, source, binary, and image reviews have no blocking finding.
- [ ] Exact Docker API support matrix and deprecation review are complete.

## Disablement, Rollback, and Repository

- [ ] Adapter-first/proxy-second disablement completes within 15 seconds without workload mutation.
- [ ] Known-good signed rollback set is retained and passes the complete negative suite.
- [ ] Disablement and rollback failure cases remain safely disabled.
- [x] Full repository tests and validators pass.
- [x] Documentation, ADR index, architecture links, lifecycle, portfolio, continuity, and generated reports are synchronized.
- [ ] Repository tree is clean; no credentials, certificate material, prohibited artifact, Registry mutation, infrastructure change, dashboard/API, EO activation, or FFFA change exists.
- [ ] Architecture Gatekeeper explicitly accepts the exact implementation artifact.

## Decision Record

| Gate | State after checklist completion |
|------|----------------------------------|
| Implementation acceptance | May be approved for exact artifact only |
| Privileged deployment authorization | Still required separately |
| Eligible Registry subject | Still required separately |
| Named-target observation | Still required separately |
| Consumer integration | Still required separately |
| Recurring activation | Still required separately |

## Transport-Free Source Evidence

| Evidence | State | Boundary |
|----------|-------|----------|
| Canonical request/response objects | Satisfied | Four-byte Unix-socket framing remains unimplemented |
| Signed authorization and exact digest binding | Satisfied with synthetic keys | Issuance, production trust, revocation operations, and credentials remain unimplemented |
| Replay behavior | Satisfied for memory and ordinary-file repository tests | Production durable store and restart deployment evidence remain unimplemented |
| Fixed dispatcher and projection | Satisfied against typed synthetic upstream | Docker request/response mediation remains unimplemented |
| Logical concurrency/rate/time/retention | Satisfied with injected clocks | OS, container, and deployment enforcement remains unimplemented |
| Unit, seed-fuzz, integration, and static tests | Satisfied for repository source | Socket, host, Docker, image, and deployment tests remain unimplemented |
| Source publication | Architecture Gatekeeper approved, accepted, and published | Transport-free source only; full implementation acceptance remains incomplete |

The checklist remains incomplete and the exact implementation artifact has not been accepted.

## Related Documents

- [Privileged Proxy Implementation Architecture](../../architecture/Privileged_Proxy_Implementation_Architecture.md)
- [Security Test Specification](../../specifications/Privileged_Proxy_Security_Test_Specification.md)
- [Privileged Deployment Acceptance Checklist](Privileged_Deployment_Acceptance_Checklist.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Recorded publication of the Architecture Gatekeeper-approved and accepted transport-free source while retaining 12 satisfied and 39 open or partial implementation-acceptance items. |
| 1.1 | Added checked transport-free source evidence and an explicit partial-evidence matrix without accepting a socket-capable artifact or privileged deployment. |
| 1.0 | Published the future implementation acceptance gate with binding identity, replay, authority, version-revalidation, and reserved-operation requirements, without authorizing implementation or deployment. |
