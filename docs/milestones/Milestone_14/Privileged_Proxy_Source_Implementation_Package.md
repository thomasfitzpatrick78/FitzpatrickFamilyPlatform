# Privileged Proxy Source Implementation Package

**Document Version:** 1.1

**Status:** Architecture Gatekeeper Approved and Accepted; Published Transport-Free Source

**Milestone:** PLAT-14.1A named prerequisite

---

## Purpose and Boundary

This package records the first purpose-built privileged-proxy Go source foundation. It implements the transport-independent security and policy core against synthetic inputs only.

```text
Transport-free repository source implementation.
No sockets.
No networking.
No Docker.
No deployment.
No production credentials.
No live observation.
```

The package does not produce or accept a binary or image. It does not implement a Unix listener, peer discovery, Docker client, Docker request, deployment configuration enforcement, eligible target, named observation, consumer, dashboard, API, recurrence, or activation.

## Source Layout

| Package | Responsibility |
|---------|----------------|
| `protocol` | Versioned immutable-by-convention models, canonical JSON, bounds, operations, categories, signals, and reason codes |
| `authorization` | Abstract peer checks, Ed25519 verification, one-shot claims, time/scope/selector validation, and exact digest binding |
| `replay` | Atomic check-and-consume interface with memory and ordinary-file test implementations |
| `policy` | Digest-verified compiled adapter for the published Proxy Foundation category matrix |
| `target` | Exact authorized target derivation |
| `upstream` | Five-method typed synthetic observation interface and closed dispatcher |
| `projection` | Operation-specific response allowlists and leakage/target/count rejection |
| `resource` | Injected-clock logical concurrency, rate, burst, timeout, lifetime, and retention policy |
| `audit` | Canonical safe events plus memory and ordinary-file test sinks |
| `core` | Ordered fail-closed `Handle(ctx, peer, requestBytes)` orchestration |
| `safety` | Go AST prohibited-capability validation |

There is no executable `main` package and no transport, Docker-client, network, deployment, shell, or plugin package.

## Core Sequence and Nonce Boundary

The core enforces:

1. request byte bound;
2. strict canonical decode;
3. protocol/operation/signal/target/deadline validation;
4. abstract peer validation;
5. Ed25519 authorization, time, scope, exact selector, and digest validation;
6. published policy evaluation;
7. exact target derivation;
8. successful security-audit precondition;
9. atomic replay check-and-consume;
10. logical admission;
11. closed typed synthetic dispatch;
12. projection and response validation;
13. final canonical audit;
14. canonical response.

The nonce is consumed after the pre-access audit succeeds and before admission or upstream invocation. It remains consumed if capacity, cancellation, synthetic provider, projection, response, or final-audit processing later fails. A retry requires a new authorization and nonce.

## Approved and Denied Operations

The only executable source dispatch entries are:

- `ResolveTargetIdentity`;
- `ObserveLifecycle`;
- `ObserveHealth`;
- `ObserveRestartInformation`;
- `ObserveStatisticsOnce`.

`CheckProviderCompatibility` is represented only as a reserved denied operation because its `System` category remains denied. Unknown and future operations have no fallback. The public model cannot express an HTTP method, URL, route, query, header, body, stream, connection, socket, generic request, or caller-provided handler.

## Existing Authority Reused

- Proxy Foundation policy version `constrained-proxy-policy-v1.0` and its exact category matrix;
- repository-standard `sha256:<lowercase-hex>` content binding;
- published Non-Docker Adapter Interface and reason codes;
- Deployment Configuration digest boundary without enforcement;
- Registry record digest and subject reference without mutation;
- Provider Adapter service identity/artifact boundary without provider access;
- Platform EAP validation and existing repository/governance/report infrastructure.

No competing Registry, policy, evidence, health, deployment, adapter, or lifecycle authority was introduced.

## Acceptance Classification

| Evidence class | Status |
|----------------|--------|
| Source architecture conformance | Satisfied for transport-free scope |
| Canonical protocol models and strict parsing | Satisfied for unframed request/response objects |
| Signed authorization and exact digest binding | Satisfied with synthetic keys |
| Replay abstraction semantics | Satisfied for memory and ordinary-file repository tests |
| Fixed typed dispatch and synthetic upstream | Satisfied |
| Response projection and leakage rejection | Satisfied for synthetic records |
| Logical resource policy and canonical audit | Satisfied at repository abstraction level |
| Static no-network/no-socket/no-Docker/no-shell proof | Satisfied |
| Real socket framing and peer credentials | Not satisfied |
| Real Docker mediation | Not satisfied |
| Production persistence and runtime confinement | Not satisfied |
| Binary/OCI/SBOM/provenance/signature acceptance | Not satisfied |
| Privileged deployment and named-target observation | Not authorized |

The result is a source-foundation review package, not implementation acceptance for privileged deployment.

## Customer-Facing Impact

The source foundation reduces future risk by proving policy, authorization, replay, exact-target, field-projection, resource, audit, and failure behavior before transport exists. A future Platform Administrator can review a smaller bounded authority surface, and a future Operations Analyst can receive deterministic limitations and provider failures. The Platform Health Dashboard and future read-only operational APIs remain consumers of PLAT-14.1A canonical evidence and health contracts only; they never consume proxy-native or Docker-native formats.

No dashboard, API, FFFA, or customer-facing implementation is included.

## Publication Decision

The Architecture Gatekeeper reviewed the exact transport-free source package and recorded `APPROVED AND ACCEPTED`. The source is published for its repository-only transport-free scope. Full implementation acceptance, socket-capable source, artifacts, Docker mediation, privileged deployment, eligible targets, observation, consumers, recurrence, and activation remain separately gated.

## Related Documents

- [Architecture Conformance](../../architecture/Privileged_Proxy_Source_Implementation_Architecture_Conformance.md)
- [Repository Usage](../../guides/Privileged_Proxy_Source_Repository_Usage.md)
- [Source Implementation Notes](../../specifications/Privileged_Proxy_Source_Implementation_Notes.md)
- [Implementation Acceptance Checklist](Privileged_Proxy_Implementation_Acceptance_Checklist.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded Architecture Gatekeeper approval, acceptance, and publication of the transport-free source without opening later implementation or operational gates. |
| 1.0 | Recorded the completed transport-free source foundation and retained every socket, artifact, deployment, observation, consumer, and activation gate. |
