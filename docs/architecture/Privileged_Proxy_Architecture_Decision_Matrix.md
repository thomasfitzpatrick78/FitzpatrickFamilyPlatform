# Privileged Proxy Architecture Decision Matrix

**Document Version:** 1.0

**Status:** Architecture Gatekeeper Accepted and Published

**Milestone:** PLAT-14.1A named prerequisite; Bravo workstream

**Evaluation Date:** 2026-07-23

---

## Purpose

This matrix evaluates the first future implementation that may possess the Docker socket. It selects architecture only. It does not authorize implementation, socket access, deployment, credentials, target selection, observation, or activation.

## Scoring

Each criterion is scored from 1 (unacceptable) to 5 (strong). Weighted score equals score multiplied by weight. A candidate is ineligible regardless of total if it cannot prove a non-Docker public interface, default-deny method/path/query/target enforcement, complete response filtering, independent service identity, or deterministic disablement.

| Criterion | Weight | A - Purpose-built minimal proxy | B - General reverse proxy plus policy | C - Existing Docker socket proxy | D - Adapter and proxy one process |
|-----------|-------:|--------------------------------:|----------------------------------------:|----------------------------------:|----------------------------------:|
| Least privilege and socket isolation | 5 | 5 | 3 | 3 | 1 |
| No arbitrary Docker relay | 5 | 5 | 2 | 2 | 1 |
| Method, operation, query, and target enforcement | 5 | 5 | 3 | 3 | 2 |
| Closed response filtering | 5 | 5 | 2 | 2 | 3 |
| Streaming, upgrade, and hijack denial | 4 | 5 | 3 | 3 | 3 |
| Strong adapter service identity | 4 | 5 | 4 | 2 | 1 |
| Audit quality and reason codes | 4 | 5 | 4 | 2 | 3 |
| Runtime isolation and independent disablement | 4 | 5 | 4 | 4 | 1 |
| Testability and denial proof | 4 | 5 | 3 | 3 | 3 |
| Supply-chain attack surface | 4 | 4 | 2 | 3 | 3 |
| Maintainability | 3 | 4 | 3 | 3 | 2 |
| Provider independence | 3 | 5 | 3 | 2 | 1 |
| Deployment Foundation compatibility | 4 | 5 | 3 | 3 | 1 |
| Rollback and disablement | 3 | 5 | 4 | 4 | 1 |
| Operational simplicity | 2 | 4 | 3 | 4 | 4 |
| Avoids adapter responsibility duplication | 3 | 5 | 4 | 3 | 1 |
| **Weighted total (maximum 335)** |  | **325** | **205** | **205** | **116** |
| **Eligibility** |  | **Eligible** | Ineligible | Ineligible | Ineligible |

## Option Analysis

## Evaluated Technology Snapshot

| Candidate | Current primary-source evidence at 2026-07-23 | Security/maintenance implication |
|-----------|------------------------------------------------|----------------------------------|
| Purpose-built Go service | Go `1.26.5` is the current supported security patch; Go supports a major until two newer majors. `golang.org/x/sys` `v0.47.0` was published 2026-06-30 under BSD-3-Clause. | Small, explicitly reviewable dependency set and static build; Platform owns secure implementation and updates. |
| HAProxy policy service | HAProxy `3.4.2` is the current 3.4 LTS patch with stated support through 2031 Q2. | Maintained, but its broad HTTP/TCP routing, configuration, header, upgrade, and transformation capabilities exceed the closed operation boundary. |
| Tecnativa Docker Socket Proxy | `v0.4.2` is the latest release, published 2025-12-16 under Apache-2.0. Its own README describes an Alpine/HAProxy Docker-API proxy configured by endpoint-group environment variables, plain HTTP, Docker-shaped access, and documented API support through `1.51`. | Actively released, but its general Docker relay shape, group-level permissions, TCP/plain-HTTP model, environment configuration, response pass-through, and API-version gap do not satisfy this contract. |

References: [Go releases](https://go.dev/doc/devel/release), [`x/sys/unix`](https://pkg.go.dev/golang.org/x/sys/unix), [HAProxy supported branches](https://www.haproxy.org/), [Tecnativa source and security model](https://github.com/Tecnativa/docker-socket-proxy), and [Tecnativa releases](https://github.com/Tecnativa/docker-socket-proxy/releases).

### Option A - Purpose-Built Minimal Proxy

Selected. A closed operation dispatcher can make every Docker path, method, query, header, and response field an implementation constant rather than caller input. A separate process preserves the published adapter, proxy, and health authorities. The cost is a security-sensitive codebase that requires rigorous review, fuzzing, supply-chain evidence, and lifecycle ownership.

### Option B - General Reverse Proxy with Strict Policy Layer

HAProxy `3.4.2` LTS is the evaluated maintained reference. Rejected for the first slice. General proxies are designed to relay HTTP and therefore preserve unnecessary parsing, routing, transformation, protocol-upgrade, and configuration surfaces. A policy layer can narrow them, but proving that no alternate route, encoding, header, stream, or upgrade bypass exists is materially harder than proving a closed operation dispatcher.

### Option C - Existing Docker Socket Proxy Product

Tecnativa `docker-socket-proxy` `v0.4.2` is the evaluated maintained reference. Rejected for the first slice. It exposes Docker-shaped HTTP access, configures broad API groups through environment variables, documents plain HTTP within a Docker network, and lists supported Docker API versions only through `1.51`, while the current Docker `29.6.1` reference is API `1.55`. It does not supply the required non-Docker public contract, exact-target authorization/digest binding, operation-specific response projection, or complete reason-coded audit model without material modification. Its documented example also requires privileged container operation for some SELinux/AppArmor contexts, contrary to the selected runtime design.

This decision does not declare existing socket proxies unsafe for all uses. It finds them insufficient for this exact governed contract.

### Option D - Adapter and Privileged Proxy in One Process

Rejected. Combining the canonical-evidence adapter with the socket holder collapses privilege and provider-normalization boundaries, prevents independent disablement, increases compromise impact, and gives provider parsing code unnecessary daemon authority.

### Option E - Other Repository-Evidenced Alternative

No materially different repository-evidenced option satisfies the published constraints. Docker authorization plugins mediate daemon requests after a caller reaches Docker's API and therefore do not replace the required non-Docker adapter boundary or response filtering layer.

## Decision

Recommend **Option A - Purpose-Built Minimal Proxy**, implemented in a future separately authorized package as a small Linux-only Go service with a closed non-Docker operation protocol, a generated fixed Docker-request dispatcher, no Docker SDK, and no general reverse-proxy capability.

## Binding Conditions

- The repository proxy policy remains the only category-policy authority.
- The public boundary contains no Docker URL, path, method, query, header, or request body.
- Exact Docker endpoint details remain private to the privileged implementation.
- `System` remains denied under current policy v1.0. A compatibility operation may be defined but cannot execute until a separately approved policy revision authorizes it.
- Architecture publication does not authorize implementation or any later gate.
- Review-time versions require complete revalidation and explicit binding at implementation acceptance.
- Peer credentials establish local process context only; signed authorization, target/time/scope, durable replay denial, and all digests remain mandatory.
- Non-root socket access cannot be achieved through implicit Docker-group, root, permission, daemon, privilege, or capability expansion.

## Related Documents

- [Privileged Proxy Implementation Architecture](Privileged_Proxy_Implementation_Architecture.md)
- [Privileged Access Security Review](Privileged_Access_Security_Review_and_Constrained_Docker_API_Proxy_Architecture_Validation.md)
- [Constrained Docker API Proxy Architecture](Constrained_Docker_API_Proxy_Architecture.md)
- [ADR-012](decisions/ADR-012-Purpose-Built-Constrained-Privileged-Proxy.md)
