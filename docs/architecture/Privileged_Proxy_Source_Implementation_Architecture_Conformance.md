# Privileged Proxy Source Implementation Architecture Conformance

**Document Version:** 1.1

**Status:** Architecture Gatekeeper Approved and Accepted; Published Transport-Free Source

**Milestone:** PLAT-14.1A named prerequisite

---

## Decision

The Architecture Gatekeeper reviewed the exact transport-free Go source foundation and recorded the authoritative decision `APPROVED AND ACCEPTED`. The published source conforms to the [Privileged Proxy Implementation Architecture](Privileged_Proxy_Implementation_Architecture.md) for the repository-only scope authorized by the Repository-Only Privileged Proxy Source Implementation work package.

```text
Transport-free repository source implementation.
No sockets.
No networking.
No Docker.
No deployment.
No production credentials.
No live observation.
```

This decision accepts and publishes the transport-free source only. It does not accept an executable artifact, authorize the later Unix-socket or Docker boundary, or change PLAT-14.1A consumer, target, observation, recurrence, or activation state.

## Conformance Matrix

| Architecture control | Source evidence | Finding |
|----------------------|-----------------|---------|
| Purpose-built minimal Go service | Narrow packages under `engineering/privileged_proxy`; no `main` package | Conforms for source scope |
| Non-Docker public protocol | Strict canonical protocol models contain no method, route, query, header, body, provider address, or socket | Conforms for source scope |
| Peer credentials are context only | `PeerContext` is injected; peer validation is separate from signed authorization | Conforms; real `SO_PEERCRED` remains unimplemented |
| Signed one-shot authorization | Standard-library Ed25519; exact identity, selector, operation, signal, time, nonce, approval, and digest bindings | Conforms with synthetic test keys only |
| Replay denial | In-memory and atomic ordinary-file test journals fail closed on replay, corruption, staleness, capacity, and ambiguous partial replacement | Conforms at repository abstraction level; production durability remains gated |
| Published policy authority | Go policy adapter compiles the exact Proxy Foundation category matrix and verifies its canonical digest | Conforms; no competing policy exists |
| Fixed dispatcher | Five compile-time typed methods; `System` and unknown operations deny | Conforms |
| Exact target | Signed claims bind subject, host, Registry digest, selector kind, and exact selector tuple | Conforms for synthetic inputs |
| Response projection | Operation-specific structs reject extra typed fields, target substitution, excessive records, and oversized output | Conforms for synthetic upstreams |
| Resource policy | Injected-clock concurrency, per-identity concurrency, rate, burst, timeout, lifetime, shutdown, audit, and replay values | Conforms logically; no OS or runtime enforcement exists |
| Audit | Canonical typed events, monotonic test-sink sequence, safe fields, fail-closed precondition | Conforms at repository abstraction level |
| Supply chain | Go 1.26.5 bound by official archive checksum; standard library only; no external modules | Conforms for source review with documented vulnerability/SBOM/provenance gaps before artifact acceptance |
| Static safety | Go AST validator plus Platform EAP repository validator prohibit networking, sockets, Docker/runtime clients, shell, environment-derived configuration, cgo, unsafe, and dynamic loading | Conforms |

## Material-Deviation Review

No material architecture deviation was found. The only architecture-snapshot dependency that would have been needed for real Linux peer credentials, `golang.org/x/sys`, is intentionally absent because real peer inspection is prohibited in this gate. The standard-library-only module narrows supply-chain exposure without changing the future socket-capable architecture decision.

The authorization model strengthens the published contract by representing the architecture-required exact target selector inside signed claims. This closes selector substitution at the transport-free boundary and does not broaden caller authority.

## Boundaries Requiring Later Proof

- Unix-domain framing, listener behavior, socket permissions, inode checks, and real `SO_PEERCRED`;
- Docker Unix-socket client code and exact Engine API request construction;
- supported Docker API and host compatibility;
- production replay and audit durability;
- non-root runtime identity and exact socket-ownership compatibility;
- seccomp, AppArmor, capabilities, cgroups, PIDs, FDs, filesystem, and image confinement;
- reproducible binary and OCI builds, SBOM, provenance, signatures, and vulnerability acceptance;
- eligible Registry subject, privileged deployment, named-target observation, consumers, recurrence, and activation.

## Architecture and Security Review Result

**Decision:** `APPROVED AND ACCEPTED` for transport-free source publication.

| Gate | Readiness |
|------|-----------|
| Source publication | Approved, accepted, and published for the transport-free scope |
| Socket-capable implementation review | Eligible as the next separate gate; not authorized |
| Privileged deployment review | Not ready |
| Named-target observation | Not authorized |

The required Architecture Gatekeeper source-publication decision is satisfied. Publication does not satisfy full implementation acceptance or authorize any later gate.

## Related Documents

- [Source Implementation Package](../milestones/Milestone_14/Privileged_Proxy_Source_Implementation_Package.md)
- [Source Implementation Notes](../specifications/Privileged_Proxy_Source_Implementation_Notes.md)
- [Static Safety and Security-Test Report](../milestones/Milestone_14/Privileged_Proxy_Source_Static_Safety_and_Security_Test_Report.md)
- [Supply-Chain Evidence Report](../milestones/Milestone_14/Privileged_Proxy_Source_Supply_Chain_Evidence_Report.md)
- [ADR-012](decisions/ADR-012-Purpose-Built-Constrained-Privileged-Proxy.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded Architecture Gatekeeper approval, acceptance, and publication of the transport-free source while preserving every socket, Docker, artifact, deployment, and observation gate. |
| 1.0 | Recorded source-scope conformance and the Architecture Gatekeeper publication hold without authorizing sockets, Docker, deployment, or observation. |
