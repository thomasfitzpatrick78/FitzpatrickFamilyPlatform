# PLAT-15.1A - Repository-Only Socket-Capable Privileged Proxy Source Implementation

**Document Version:** 1.1

**Status:** Authorized for Future Repository Implementation

**Milestone:** Milestone 15

**Priority:** High — Highest-priority Platform implementation package

**Implementation State:** Not Started

**Expected Generated Evidence Baseline:** Permitted

---

## Purpose

This published work package converts the privileged-proxy architecture and transport-free source foundation into the next bounded Platform implementation gate: repository-only socket-capable source with fixture-only Unix-socket integration evidence.

The package applies the Milestone 15 Delivery Leverage criterion by reusing completed architecture, policy, authorization, replay, projection, resource, audit, security-test, and validation foundations. The Product Strategy Board and Architecture Gatekeeper approved and published this exact work-package boundary. Repository implementation may begin only through a separate repository-governed AI Session Initialization.

---

## Portfolio Selection Rationale

Milestone 15 selects work that delivers or unlocks customer value, reduces engineering effort or risk, or measurably increases delivery throughput.

| Delivery-Leverage Question | PLAT-15.1A Contribution |
|----------------------------|--------------------------|
| What delivers software? | Converts the closed privileged-proxy architecture into a bounded source implementation. |
| What unlocks customer value? | Supplies the missing repository source prerequisite for future real Container Operational Health evidence while preserving every operational gate. |
| What reduces engineering risk? | Proves framing, peer identity, fixed Docker request construction, bounded response parsing, durable replay/audit behavior, and prohibited-capability absence before artifact or deployment work. |
| What makes future delivery faster? | Reuses the transport-free core and published acceptance matrix rather than creating a new proxy, provider, policy, lifecycle, or evidence model. |
| What keeps the milestone disciplined? | Stops at repository-only source acceptance and leaves artifacts, deployment, daemon interaction, evidence consumers, and activation separately governed. |

The work directly strengthens the Shared Platform. It strengthens the Engineering Organization by exercising the published EO-15.1 initialization and Transition Review controls through a real Platform package. It unlocks, but does not itself deliver, future customer-facing operational reliability. FFFA acceptance remains a separate High-priority repository-owned outcome and is not changed by this package.

---

## Identifier and Backlog Boundary

`PLAT-15.1A` is the published Milestone 15 work-package identifier subordinate to PLAT-PB-013 and AB-011. It does not create a new Product Backlog capability.

This package advances [PLAT-PB-013](../../product/Product_Backlog.md) and the existing Platform Operations architecture path recorded under AB-011. It does **not** implement, promote, or rename AB-012. AB-012 remains `Candidate - Remain Backlog` until the repository contains the separately approved operational evidence required by the [Architecture Backlog](../../architecture/Architecture_Backlog.md).

---

## Decision Record

| Decision | Required Authority | Current State |
|----------|--------------------|---------------|
| Select repository-only socket-capable proxy source as the highest-priority Platform implementation package | Product Strategy Board | Approved and published |
| Approve the exact source boundary and confirm conformance to the closed transport architecture | Chief Architect / Architecture Gatekeeper | Approved and published |
| Publish this work package as implementation authority | Product Strategy Board and Architecture Gatekeeper | Approved and published |
| Perform repository implementation after publication and a separate AI Session Initialization | Codex Implementation Engineer | Authorized for future repository implementation; not started |

The published repository record satisfies the work-package decisions only. Conversation approval, portfolio planning text, `READY`, or a clean baseline does not authorize implementation, artifact work, deployment, activation, or live work.

---

## Authoritative Inputs

- [Milestone 15 Portfolio Plan](Milestone_15_Portfolio_Plan.md).
- [Milestone 14 Transition Review](../Milestone_14/Milestone_14_Transition_Review.md).
- [Socket-Capable Privileged Proxy Implementation Review Package](../Milestone_14/Socket_Capable_Privileged_Proxy_Implementation_Review_Package.md).
- [Privileged Proxy Source Implementation Package](../Milestone_14/Privileged_Proxy_Source_Implementation_Package.md).
- [Privileged Proxy Implementation Acceptance Checklist](../Milestone_14/Privileged_Proxy_Implementation_Acceptance_Checklist.md).
- [Privileged Proxy Implementation Architecture](../../architecture/Privileged_Proxy_Implementation_Architecture.md).
- [ADR-012 - Purpose-Built Constrained Privileged Proxy](../../architecture/decisions/ADR-012-Purpose-Built-Constrained-Privileged-Proxy.md).
- [Privileged Proxy Threat Model](../../architecture/Privileged_Proxy_Threat_Model.md).
- [Privileged Proxy Non-Docker Adapter Interface Specification](../../specifications/Privileged_Proxy_Non_Docker_Adapter_Interface_Specification.md).
- [Privileged Proxy Runtime Security Control Specification](../../specifications/Privileged_Proxy_Runtime_Security_Control_Specification.md).
- [Privileged Proxy Supply-Chain Security Requirements](../../specifications/Privileged_Proxy_Supply_Chain_Security_Requirements.md).
- [Privileged Proxy Security Test Specification](../../specifications/Privileged_Proxy_Security_Test_Specification.md).
- Published EO-15.1 baseline classification, AI session initialization, completion, continuity, and evidence controls.

No replacement architecture or additional pre-implementation architecture design is requested. Any conflict with these inputs stops the package and returns it to the Architecture Gatekeeper.

---

## Preconditions Before Implementation

Implementation may begin only after all conditions below pass:

1. Product Strategy Board approval of the priority, identifier, and portfolio fit remains recorded and published.
2. Architecture Gatekeeper approval of the exact repository-only source scope remains recorded and published.
3. This work package remains published with implementation status authorized and the governed generated-evidence permission recorded exactly once.
4. A separate Codex Implementation Engineer session completes repository-governed AI Session Initialization against a fetched, synchronized baseline classified `Clean` or qualifying `Expected Generated Evidence` under this exact work package.
5. The published transport review, ADR-012, threat model, interface, security tests, and acceptance checklist remain current and non-conflicting.
6. Exact supported Go and `golang.org/x/sys` versions, source revisions, checksums, maintenance status, advisories, vulnerabilities, and licenses are revalidated before dependency or source changes are accepted.
7. No real Docker, container-runtime, infrastructure, credential, Registry, customer-data, deployment, or live access is required to complete the repository implementation.

Failure or ambiguity in any precondition stops implementation.

---

## Authorized Repository Scope After Approval

After the required approvals and publication, the Codex Implementation Engineer may implement only the following repository scope.

### Adapter-Facing Unix-Socket Boundary

- Linux-only filesystem `AF_UNIX` / `SOCK_STREAM` listener for the published non-Docker adapter protocol.
- Exact absolute-path, ASCII, `sun_path`, directory-chain, absent-path, symlink, owner, group, mode, device, inode, and current-process-only unlink rules.
- Four-byte unsigned big-endian framing, strict request and response limits, one request per connection, mandatory client half-close, EOF-before-processing, response EOF, and exact deadlines.
- Kernel-returned `SO_PEERCRED` numeric UID/GID verification on every accepted connection, with PID retained for bounded audit context only.
- Close-on-exec descriptors, no descriptor passing, no child process, bounded admission, concurrency, file-descriptor use, and deterministic cleanup.

### Fixed Docker Unix-Socket Mediation

- A single-purpose Unix-socket observer implementing only the existing typed `upstream.Observer` responsibilities.
- Immutable configured socket path plus exact pre-connect and post-connect metadata and peer-credential verification.
- One connection for one fixed request, no retry, alternate path, negotiation, discovery, connection reuse, or caller-controlled transport input.
- Byte-exact fixed HTTP/1.1 request constructors for the published container list, inspect, and one-shot statistics routes only.
- Strict bounded response parsing, duplicate and ambiguous framing rejection, version/content-type/size/depth/count enforcement, exact target revalidation, and operation-specific projection.
- Reserved compatibility operations remain compiled denial paths unless a separate approved policy revision changes that authority.

### Durable Repository Adapters and Composition

- Production-grade source adapters for durable replay and audit contracts, exercised only through repository-controlled temporary fixtures.
- Production Provider Adapter source changes are prohibited. Adapter-facing socket tests may use only temporary fake adapter peers expressly defined by the T-01 through T-12 matrix.
- Readiness and failure state necessary to compose the existing transport-free authorization, policy, target, resource, projection, audit, replay, and core orchestration packages.
- A minimal Linux compile target that consumes immutable typed configuration and exposes no deployment, environment override, Docker CLI, live-test, administrative, or general-purpose command surface.
- Necessary changes to the existing privileged-proxy source validator, safety checks, documentation, and evidence summaries so they describe the socket-capable repository source truthfully.

### Tests and Evidence

- Unit, Linux Unix-socket integration, race, bounded fuzz, saturation, failure-injection, and static prohibited-capability tests.
- Temporary fake adapter and fake Docker Unix-socket peers only; they are test peers and do not modify or replace the Production Provider Adapter.
- Exact T-01 through T-12 evidence from the published Security Test Specification.
- A fail-fast guard that rejects `/var/run/docker.sock`, `/run/docker.sock`, rootless runtime socket paths, non-temporary socket roots, Docker CLI/SDK/daemon access, and any IP networking.
- Source conformance, call-graph, dependency, toolchain, vulnerability, license, test, and completion evidence required for Architecture Gatekeeper source acceptance.
- Bounded planning and continuity updates necessary to record implementation state and the next Architecture Review gate.

The implementation must extend `engineering/privileged_proxy/` and existing Platform EAP validation mechanisms. It may not create a generic IPC, RPC, Unix-transport, HTTP, Docker-client, policy, provider, evidence, lifecycle, or plugin framework.

---

## Explicitly Prohibited Scope

This work package does not authorize:

- any connection to a real Docker, Podman, containerd, or other container daemon;
- access to `/var/run/docker.sock`, `/run/docker.sock`, a rootless runtime socket, or any governed host socket;
- Docker SDK or CLI use, generic HTTP clients/transports, reverse proxying, caller-controlled URLs, IP networking, DNS, TCP, UDP, raw sockets, ports, remote transport, shell, or subprocess execution;
- Docker-socket creation, copying, forwarding, permission/owner/ACL changes, daemon configuration, host user/group changes, supplemental root-equivalent group membership, privilege expansion, or root fallback;
- a persistent binary, release artifact, OCI image/layout/index, registry push, SBOM or provenance release attestation, signing, tag, release, or artifact acceptance;
- deployment configuration application, runtime-control enforcement claims, credentials, certificates, secrets, eligible Registry subjects, Registry mutation, host selection, or infrastructure mutation;
- real provider observation, named targets, canonical operational evidence, health evaluation, dashboards, APIs, consumers, recurrence, scheduling, automation activation, or live work;
- Platform workload remediation or any customer, FFFA, or customer-data change;
- ADR-012 `Implemented: Yes`, AB-012 promotion, architecture reopening, lifecycle redesign, or governance expansion by implication.

Any requirement for prohibited scope stops implementation and requires a separately approved work package or explicit Architecture Gatekeeper decision.

---

## Acceptance Criteria

### Architecture and Reuse

- Source conforms to ADR-012 and every binding clarification in the published Socket-Capable Implementation Review.
- Existing protocol, authorization, policy, target, projection, resource, audit, replay, and core authority is composed rather than duplicated.
- The adapter, proxy, PLAT-14.1A health authority, and consumers remain provider-independent at their published boundaries.
- Docker API compatibility remains owned exclusively inside the single-purpose proxy.
- Static reachability evidence proves that only approved fixed constructors can reach the fake Docker Unix connector.
- No generic transport, routing, HTTP, Docker, plugin, shell, Registry, deployment, scheduler, consumer, or remediation capability is introduced.

### Security and Failure Behavior

- Adapter socket lifecycle, framing, half-close/EOF, deadlines, peer credentials, replacement detection, cleanup ownership, and resource limits pass positive and negative tests.
- Fake Docker socket metadata, peer identity, one-request connection behavior, fixed request bytes, response parsing, target validation, projection, and no-retry behavior pass positive and negative tests.
- Durable replay and audit adapters fail closed on missing, corrupt, stale, full, unavailable, ambiguous, or unsuccessful state and recover only through tested governed behavior.
- Every denial is deterministic, bounded, secret-safe, auditable, and occurs before prohibited provider activity.
- Tests demonstrate no conventional or governed Docker path, Docker daemon/CLI/SDK, non-temporary Unix endpoint, or IP network was touched.

### Verification Evidence

- All T-01 through T-12 repository cases pass without a skipped negative case.
- All T-01 through T-12 cases and every applicable race test execute on supported Linux without host-dependent skips. If supported Linux execution is unavailable, implementation stops rather than weakening or deferring the gate.
- `go test ./...` passes.
- `go test -race ./...` passes on supported Linux.
- Bounded fuzz targets and retained seed corpora pass for framing, canonical JSON, filter encoding, HTTP response, Docker JSON, and projection boundaries.
- `python3 -m pytest -p no:cacheprovider engineering/tests` passes.
- `./platform-eap privileged-proxy source validate` and `source static-safety` pass after being truthfully updated for the approved socket-capable source boundary.
- Repository Validation, Governance Validation, AI Session Readiness, documentation links, architecture links, secret scanning, repository hygiene, and `git diff --check` pass.
- The completion package records the synchronized starting HEAD, exact changed paths, an exact diff or tree digest, Go toolchain, dependency lock/checksums, commands, platform, fixture/corpus identity, timestamps, results, limitations, and confirmation of no prohibited access. Before source publication, it must not fabricate a future commit identifier. A later authorized source-publication commit becomes the canonical source revision only after successful publication and post-publication verification.

### Lifecycle Result

- Repository implementation stops at Architecture Review with source uncommitted and unpublished unless separately authorized publication procedures apply.
- Architecture Gatekeeper reviews and either accepts or rejects the exact source implementation.
- ADR-012 remains `Implemented: No` through implementation; any later state change requires an explicit Architecture Gatekeeper decision.
- AB-012 remains backlog.
- Source acceptance, if granted, makes the exact source eligible only for a separately authorized artifact-acceptance work package.
- Artifact, deployment, first-daemon-interaction, operational evidence, dashboard/consumer, recurrence, and activation gates remain closed.
- Source acceptance does not satisfy binary, OCI, SBOM, provenance, signature, artifact, deployment, daemon-interaction, observation, consumer, recurrence, or activation acceptance. Artifact-related unchecked items in the implementation acceptance checklist remain deferred.

---

## Required Session Evidence

The later implementation session must create or update repository-native evidence for:

- AI Session Initialization and starting baseline classification;
- exact authority, scope, role, dependencies, and prohibited-action reconciliation;
- source and test changes by path;
- T-01 through T-12 results and any retained bounded corpus identifiers;
- toolchain, dependency, vulnerability, and license review;
- privileged-proxy source validation and static safety;
- repository, governance, readiness, link, hygiene, secret, and whitespace validation;
- no-real-Docker, no-IP-network, no-artifact, no-deployment, no-Registry-mutation, no-customer-data, and no-live-work confirmation;
- completion summary, unresolved risks, synchronized starting HEAD, exact changed paths, exact diff or tree digest, and exact Architecture Gatekeeper next gate. Uncommitted Architecture Review evidence must not claim a future source-publication commit.

Detailed local paths, credentials, host identifiers, Docker state, customer data, and sensitive raw output must not enter Git.

---

## Roles and Authority

| Responsibility | Governed Role |
|----------------|---------------|
| Portfolio priority, milestone sequencing, and customer-value decision | Product Strategy Board |
| Architecture conformance, residual-risk interpretation, source acceptance, and any architecture reopening | Chief Architect / Architecture Gatekeeper |
| Repository implementation, tests, documentation, and evidence within approved scope | Codex Implementation Engineer |
| Engineering Organization delivery-leverage observations | Engineering Organization Advisor |
| Artifact, deployment, host, daemon interaction, production, or live execution | Not authorized by this package; requires later explicit roles and human approval |

The Codex Implementation Engineer must stop on conflicting authority, material ambiguity, architecture drift, an unavailable required negative test, a dependency outside the approved boundary, prohibited access, or scope expansion.

---

## Lifecycle and Publication Gates

```text
Governed Work-Package Publication (Complete)
        |
        v
Separate Codex Implementation Engineer Initialization
        |
        v
Repository-Only Source Implementation and Validation
        |
        v
Architecture Gatekeeper Source Acceptance Review
        |
        v
Separately Authorized Artifact-Acceptance Work Package
```

No later gate is implied by completing an earlier gate.

---

## Success Measures

- One bounded socket-capable source package reaches Architecture Review without real daemon, artifact, deployment, or live access.
- Published architecture and transport-free core are reused without a parallel framework.
- Every required negative test runs and passes; no prohibited capability or access occurs.
- The implementation produces exact source-acceptance evidence with no architecture rework caused by avoidable scope drift.
- Work-package preparation and session initialization use the published EO-15.1 controls, providing observable Delivery Leverage evidence without creating new governance families.

This package makes no unsupported promise about deployment lead time, production throughput, dashboard availability, or customer outcome before the separately governed later gates complete.

---

## Next Gate

Separate repository-governed AI Session Initialization by the Codex Implementation Engineer. That future session must fetch and prove synchronization, reconcile this exact authority, and stop on any conflicting or superseding repository state. Repository implementation remains Not Started.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded Product Strategy Board selection and Architecture Gatekeeper approval and publication of PLAT-15.1A as the highest-priority Platform implementation package, authorized only future repository implementation, permitted governed generated evidence, clarified the adapter-facing and Linux evidence boundaries, and retained every later gate. |
| 1.0 | Proposed the highest-priority Milestone 15 Platform package as repository-only socket-capable privileged-proxy source implementation, preserving AB-012 backlog status and every artifact, deployment, daemon-interaction, consumer, activation, and live-work gate. |
