# ADR-012 - Purpose-Built Constrained Privileged Proxy

**Status:** Approved

**Date Approved:** July 2026

**Category:** Infrastructure Architecture

**Milestone:** PLAT-14.1A named prerequisite

**Implemented:** No

**Baseline:** Published with the PLAT-14.1A Privileged Proxy Implementation Architecture package

---

## Context

The published Provider Adapter, Privileged Access Security Review, Constrained Proxy, and Deployment Configuration foundations deliberately defer the exact socket-capable implementation. The durable decision now required is whether the socket holder is a purpose-built service, a configurable general proxy, an existing socket-proxy product, or part of the adapter.

The boundary must expose only a provider-independent non-Docker protocol; enforce exact operations, target, method, query, version, size, and response fields; authenticate the adapter workload; bind authorization to exact content digests; and remain independently disableable.

## Decision

The first future socket-capable proxy shall be a **purpose-built minimal Linux service**, separate from the provider adapter.

Its bounded implementation strategy is:

1. Go `1.26.5` at the 2026-07-23 architecture snapshot, updated only to a reviewed supported security patch before implementation.
2. Go standard library plus exactly one initial external module, `golang.org/x/sys` `v0.47.0`, for Linux peer-credential inspection. Every module remains checksum- and lock-pinned.
3. A second filesystem-namespaced Unix-domain stream socket using a versioned, 32-bit big-endian length-prefixed canonical JSON request/response protocol.
4. Verified `SO_PEERCRED` UID/GID/PID as local peer-process context, plus restrictive socket ownership/mode and a short-lived signed authorization envelope. Peer credentials do not independently authorize a request.
5. A closed operation dispatcher that constructs fixed Docker Engine API requests internally. No Docker SDK, reverse-proxy library, caller-controlled URL, generic HTTP handler, plugin system, shell, subprocess, or network transport is permitted.
6. A statically linked `CGO_ENABLED=0` binary in a `scratch` final image, numeric non-root identity where compatible with the exact approved socket-ownership model, immutable digest, signed SBOM and provenance, and the published runtime confinement controls. No Docker-group, root, group-permission, or daemon change is implicitly authorized.

Go is selected because the standard library supplies strict JSON, cryptography, HTTP parsing, bounded concurrency, and Unix-socket primitives in one statically buildable runtime. Avoiding a Docker SDK prevents unused daemon operations and automatic version negotiation from becoming reachable code.

## Consequences

### Positive

- The public interface cannot become an arbitrary Docker relay without a major governed change.
- The Docker request set is enumerable and testable.
- Adapter normalization and health authority remain outside the privileged process.
- A small dependency graph reduces, but does not eliminate, supply-chain exposure.
- A separate process and image support independent disablement and rollback.

### Tradeoffs

- The Platform owns a security-sensitive implementation and patch lifecycle.
- Linux peer credentials require Linux-specific code and later verification under the exact container runtime.
- The service still has root-equivalent Docker authority if compromised.
- Strict response projection must track supported Docker API changes.
- Audit durability and replay protection introduce small bounded writable state.

## Rejected Alternatives

- A general reverse proxy or API gateway retains broad HTTP routing and transformation attack surface.
- Existing Docker socket proxies generally expose Docker-shaped routes or broad endpoint groups and do not provide the required public schema, authorization binding, or field-level response projection.
- Combining adapter and proxy collapses privilege, provider, and normalization boundaries.
- Direct adapter socket access violates the published architecture.

## Version and Review Rule

Go `1.26.5` and `golang.org/x/sys` `v0.47.0` are architecture-snapshot inputs, not perpetual deployment approval. Before implementation acceptance, the Architecture Gatekeeper must revalidate and approve the exact supported toolchain, dependency versions and source revisions, Docker Engine/API range, container base and image digests, maintenance and end-of-life status, security advisories, vulnerabilities, licenses, SBOM, provenance, and signatures. Any drift requires explicit review.

The Go project supports each major release until two newer major releases and issues security fixes on supported branches. The selected source is BSD-3-Clause compatible. Current references:

- [Go release history and support policy](https://go.dev/doc/devel/release)
- [Go license](https://go.dev/LICENSE)
- [Go vulnerability management](https://go.dev/doc/security/vuln/)
- [`golang.org/x/sys/unix` v0.47.0](https://pkg.go.dev/golang.org/x/sys/unix)
- [Linux Unix-domain peer credentials](https://man7.org/linux/man-pages/man7/unix.7.html)

## Implementation and Activation Boundary

This ADR records approval of the architecture decision only. Implementation has not begun; no artifact has been accepted; and no code, dependency retrieval, build, image creation, Docker or socket access, credential, deployment, target approval, observation, consumer, recurring execution, or activation is authorized. Reserved compatibility operations remain denied under the current policy.

## Related Documents

- [Architecture Decision Matrix](../Privileged_Proxy_Architecture_Decision_Matrix.md)
- [Privileged Proxy Implementation Architecture](../Privileged_Proxy_Implementation_Architecture.md)
- [Privileged Proxy Runtime Security Control Specification](../../specifications/Privileged_Proxy_Runtime_Security_Control_Specification.md)
- [Privileged Proxy Supply-Chain Security Requirements](../../specifications/Privileged_Proxy_Supply_Chain_Security_Requirements.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Recorded Architecture Gatekeeper approval of the separate purpose-built minimal Go proxy and authenticated non-Docker Unix-socket boundary, with binding clarification that approval is architecture-only. |
