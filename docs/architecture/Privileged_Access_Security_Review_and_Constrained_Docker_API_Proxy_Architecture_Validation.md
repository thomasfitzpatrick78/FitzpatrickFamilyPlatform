# Privileged Access Security Review and Constrained Docker API Proxy Architecture Validation

**Document Version:** 1.3

**Status:** Architecture Gatekeeper Accepted Foundations and Published Implementation Architecture; No Privileged or Live Authority

**Milestone:** PLAT-14.1A named prerequisite; Bravo workstream

**Review Date:** 2026-07-22

---

## Executive Decision

The constrained Docker API proxy is a sound future implementation target only when it is treated as the sole Docker-socket authority, deployed as a separately isolated same-host component, exposed to the adapter through an authenticated non-Docker boundary, and governed by a machine-verifiable default-deny policy.

The Architecture Gatekeeper accepted this review and approved it for publication with the binding clarifications in this document. Publication does not authorize proxy implementation, Docker access, deployment, credentials, an eligible target, named-target observation, recurring operation, or activation.

The **Repository-Only Constrained Docker API Proxy Foundation** gate is implemented and published. The **Repository-Only Privileged Deployment Configuration Foundation** now adds immutable descriptive profiles, exact synthetic service identity, runtime-security and resource prerequisites, audit requirements, proxy/provider/policy compatibility, canonical digests, strict fixtures, and fail-closed validation. These are configuration contracts only: they do not enforce controls, load credentials or certificates, create transport, deploy, select a target, or observe infrastructure. Publication satisfies only repository configuration readiness.

## Repository Evidence

- Published baseline: `77ba80254e697764dec4df5753d42021721fe90c`, `Production Provider Adapter Foundation`.
- Registry schema `1.1` validates 39 records.
- Five exact subjects are published `not_applicable`; the current migration plan is 0 apply, 16 review-required, and 23 no-change.
- No current Registry record is approved as the live named target.
- PLAT-14.1A health and provider foundations are repository-only, fixture-backed, and unactivated.
- No Docker API, Docker socket, proxy, live provider, credential, or privileged implementation exists.

## Architecture Consistency

ADR-007 and ADR-009 through ADR-011, the Platform Operations architecture, Registry identity foundation, Operational Evidence contracts, Container Operational Health specification, provider architecture/contract/foundation, Operational Excellence specification, Platform Health Dashboard specification, and container observability architecture remain compatible.

No architectural contradiction was found. Four clarifications are binding:

1. Authority flow and evidence flow are separate and must not be represented as a single ambiguous chain.
2. Network isolation alone is not authentication; adapter-to-proxy service identity must be technically enforced.
3. Streaming, connection upgrade, gRPC or equivalent bypass, and response-uninspectable categories are denied in the first slice.
4. Repository implementation review, privileged deployment authorization, and named-target observation authorization are distinct gates.

## Validated Authority and Evidence Flows

```text
Authority and request flow:
Registry declaration
        |
        v
Named-target authorization
        |
        v
Provider adapter
        |
        v
Constrained Docker API proxy
        |
        v
Docker Engine

Evidence flow:
Docker Engine observation
        |
        v
Proxy method, target, query, size, and response filtering
        |
        v
Provider adapter strict parsing and normalization
        |
        v
Canonical Operational Evidence
        |
        v
PLAT-14.1A reconciliation and health evaluation
        |
        v
Read-only consumers
```

The authorization never flows from Docker, the proxy, the adapter, evidence, health, or a consumer back into Registry state or infrastructure control.

## Trust-Boundary Assessment

| Boundary | Authority and Owner | Trust and Attack Surface | Required Controls | Failure and Audit |
|----------|---------------------|--------------------------|-------------------|-------------------|
| Registry to named-target authorization | Registry is declared-state authority; Architecture Gatekeeper and Platform Administrator approve the bounded use. | High-integrity repository input; risk is stale, incomplete, forged, wildcard, or ineligible identity. | Exact record hash, eligible participation, host and identity tuple, explicit signal/window scope, expiry, no wildcard. | Reject drift or ambiguity before any provider interaction; audit approval identity and digest. |
| Authorization to adapter | Authorization grants one bounded attempt, not infrastructure authority. | Replay, substitution, time-window abuse, output redirection, and unsupported version. | Signed or content-bound approval reference, nonce/correlation, validity window, safe output, version/digest binding. | Fail closed before connection; audit acceptance or deterministic rejection. |
| Adapter to proxy | Adapter is unprivileged and cannot reach Docker directly. | Client spoofing, credential theft, network lateral movement, request smuggling, category bypass. | Enforced service identity, fixed proxy boundary, no arbitrary URL, default-deny methods/categories, payload/time/rate limits. | Deny unknown client/request; correlated client, category, target, and result audit. |
| Proxy to Docker Engine | Proxy is the sole privileged component and Docker-socket authority. Platform Administrator owns deployment. | Root-equivalent daemon authority, parser/proxy compromise, policy drift, socket escape. | Socket visible only to proxy; immutable reviewed policy; no upgrade/stream/bypass; minimal runtime privileges; supply-chain proof. | Fail closed on policy/auth/audit failure; immediate proxy disablement and evidence invalidation. |
| Docker response to proxy | Docker output is untrusted provider data. | Oversize response, secret/topology leakage, malicious strings, excessive enumeration, version drift. | Target/query enforcement, response field allowlist, byte/record/time bounds, content type and API version validation. | Reject or truncate only under explicit contract; never pass unreviewed payload; log safe classification/digest. |
| Proxy response to adapter | Proxy output is constrained but not canonical. | Response spoofing, tampering, replay, partial response, provider limitation. | Authenticated channel, response integrity, correlation, strict schema, timing, coverage, limitation and provenance. | Deterministic provider failure; no service-health conclusion. |
| Adapter to canonical evidence | Adapter translates but does not declare identity or health. | Parser/type confusion, subject injection, secret persistence, false completeness. | Closed contracts, exact versions, no subject assignment, allowlisted fields, provenance and limitation preservation. | No canonical record on invalid input; safe rejection evidence. |
| Evidence to PLAT-14.1A | PLAT owns reconciliation and health. | Spoofed identity, stale/replayed evidence, incomplete mandatory coverage. | Registry-first reconciliation, freshness/confidence policy, deterministic insufficient-evidence treatment. | Reject or downgrade evidence usability; audit reasons and policy versions. |
| PLAT-14.1A to consumers | Consumers are presentation/advisory only. | Recalculated health, hidden limitations, no-data Healthy, reverse control path. | Read-only contract, explicit expired/no-data/provider-failure states, no command surface. | Consumer conformance failure blocks integration; no automation authority. |

## Docker Socket Risk Assessment

Docker Engine control is generally root-equivalent on a rootful daemon. A caller able to use unrestricted Engine API operations can create or execute containers, mount the host filesystem or block devices, alter images, networks and volumes, read sensitive metadata, control Swarm objects, load plugins, and affect host availability. Docker documents that daemon access must be restricted to trusted users and that crafted API parameters can create arbitrary containers with host filesystem access.

A read-only filesystem mount of the Docker socket is **never sufficient protection**. The mount flag constrains filesystem writes to the socket inode; it does not convert authenticated Docker API operations into read-only semantics. The connected client can still submit mutation requests accepted by the daemon. Unix group membership, possession of a client certificate, or a bearer token that grants unrestricted daemon access must therefore be treated like privileged host authority.

Direct socket access by the adapter, collector, dashboard, automation, or consumer remains prohibited.

## Proxy Architecture Decision

The proxy may become the only privileged component if every requirement below is met:

- It is the only component that can open the Docker socket.
- Its Docker-facing boundary is local to the Docker host and never forwarded.
- Its adapter-facing boundary is a distinct protocol endpoint and cannot relay arbitrary Docker requests.
- Policy is default deny across method, category, API version, path class, query/filter shape, target, content type, request size, response size, streaming, and connection upgrade.
- Exact target restriction is enforced before Docker access when possible and verified again on the response.
- Broad enumeration, redirects, proxy chaining, arbitrary upstreams, gRPC or equivalent bypass, HTTP upgrade, hijack, attach, logs, and unbounded streams are denied in the first slice.
- Response filtering uses a closed field allowlist; security decisions do not depend on partial inspection of streaming or oversized responses.
- The process is non-root where technically feasible, runs with all Linux capabilities dropped except a separately justified minimum, uses `no-new-privileges`, a read-only root filesystem, explicit ephemeral storage, seccomp/AppArmor or equivalent confinement, and CPU/memory/PID/file-descriptor limits.
- Docker-socket group access is documented as privileged even when the process UID is non-root.
- Configuration and image are pinned by digest; startup fails on drift, unknown policy, unsupported API version, unavailable audit, or authentication failure.
- Safe audit records are retained under an approved bounded policy and never include raw payloads, credentials, environment values, commands, mounts, or unapproved topology.
- Disablement stops the adapter first and proxy second without restarting or modifying the observed service.

## Endpoint Category Decisions

These are category decisions, not endpoint-path authorization. Exact paths, methods, parameters, and response fields require current official Docker API verification at the later implementation/security gate.

| Category | Decision | Rationale and Binding Constraint |
|----------|----------|----------------------------------|
| Identity discovery | Conditionally allowed | Exact named-target filters only, with bounded result count and response-field allowlist. Unfiltered or wildcard container enumeration is denied. |
| Lifecycle observation | Allowed | Target-specific read needed for canonical lifecycle evidence; no lifecycle mutation method is permitted. |
| Health observation | Allowed | Target-specific read of configured runtime health state is mandatory when Registry policy requires it. |
| Statistics | Conditionally allowed | One-shot, non-streaming, exact-target statistics only with strict byte/time/field limits. Supplemental/advisory unless policy later changes. |
| Restart information | Allowed | Target-specific read of restart count/state is bounded and advisory under policy 1.0. |
| Events | Future | Streaming and broad event visibility create response-inspection, replay, cardinality, and enumeration risks. Requires a separate bounded-stream design. |
| Images | Denied | Container observation may preserve the image reference returned by approved container inspection; image listing, history, export, pull, load, tag, delete, or mutation is unnecessary. |
| Volumes | Denied | Exposes host storage topology and supports destructive or privilege-escalating operations; not required for health. |
| Networks | Denied | Exposes topology and includes mutation/control capability; container response fields outside the allowlist are filtered. |
| Build | Denied | Executes untrusted build inputs and can consume network, filesystem, image, and compute authority. |
| Exec | Denied | Direct code execution and connection hijack are incompatible with observation-only authority. |
| Archive | Denied | Reads or writes container filesystem content and may disclose or change sensitive data. |
| Filesystem | Denied | Filesystem export, copy, diff, mount, and related content operations are outside operational evidence. |
| Secrets | Denied | Secret enumeration or content access is never required for health evidence. |
| Plugins | Denied | Plugin management and inspection expand daemon/host authority and supply-chain attack surface. |
| Swarm | Denied | Secrets, configs, services, nodes, tasks, sessions, and cluster control are outside the named standalone-container scope. |
| System | Conditionally allowed | Only bounded availability and exact API/version compatibility checks may be approved. Broad system information and mutation are denied. |
| Configuration | Denied | Daemon, service, container, secret/config, and runtime configuration reads beyond allowlisted observation fields and all writes are denied. |

## Authentication Recommendation

| Model | Assessment |
|-------|------------|
| Same-host location alone | Rejected as authentication. Location reduces exposure but does not identify the caller. |
| Loopback TCP | Insufficient alone. Namespace and local-compromise boundaries are ambiguous; it still requires authenticated service identity. |
| Token | Not preferred as the sole control. Bearer theft enables replay and creates rotation/logging risk. May only supplement a stronger channel identity. |
| Certificate / mTLS | Required for any IP network boundary. Provides mutual endpoint authentication and auditable client identity but certificates remain root-equivalent if the proxy policy is bypassed. |
| Unix-socket mediation | Preferred same-host transport when a second, non-Docker Unix socket is used with restrictive ownership/mode and peer identity enforcement. The adapter never receives the Docker socket. |
| Service identity | Required at every adapter-to-proxy boundary. Bind authorization to one workload identity, policy, target scope, and time window. |

Preferred model: a dedicated proxy exposes a second Unix-domain socket to the adapter through a narrowly shared runtime boundary, with restrictive UID/GID permissions and verified peer/service identity. If Unix peer identity cannot be proven or any IP transport is used, mutually authenticated TLS with a dedicated short-lived client identity is mandatory. Network membership, loopback, or a token alone is insufficient.

## Deployment Recommendation

| Form | Attack Surface | Maintainability and Audit | Rollback and Complexity | Decision |
|------|----------------|---------------------------|-------------------------|----------|
| Same-host sidecar coupled to adapter | Tight coupling risks shared compromise and lifecycle confusion. | Weak independent ownership and audit. | Simple but rollback may affect both components. | Denied for first slice. |
| Same-host dedicated proxy container plus separate adapter | Keeps socket authority isolated, avoids LAN exposure, and permits distinct identities/policies. | Strong version/config audit and independent disablement. | Moderate complexity; rollback can stop adapter then proxy without touching workload. | **Preferred.** |
| Separate host | Adds network, mTLS, routing, firewall, clock, and remote-daemon exposure. | Stronger host fault separation but higher credential and operations burden. | Complex rollback and incident isolation. | Future only. |
| Shared infrastructure proxy | Cross-target and cross-service blast radius, tenant confusion, and policy aggregation. | Complex audit and change ownership. | High operational risk. | Denied for first slice. |
| Manual administrator execution | Human visibility but risks broad workstation credentials and non-repeatable evidence. | Weak reproducibility unless fully governed. | Useful only for later diagnostics. | Future diagnostic only. |
| Scheduled execution | Recurring privileged reach and automation dependency. | Requires monitoring, ownership, revocation, and repeated evidence. | Separate activation and retirement lifecycle. | Denied until recurring-activation gate. |

## Threat Model Assessment

Likelihood and residual risk assume the proposed controls are correctly implemented and independently verified. Before that proof, proxy/socket compromise and policy drift remain High.

| Threat | Likelihood | Impact | Residual Risk | Required Mitigation |
|--------|------------|--------|---------------|---------------------|
| Proxy compromise | Medium | Critical | Medium | Minimal code/dependencies, confinement, no shell, egress deny, immutable image/config, rapid disablement. |
| Credential or service-identity compromise | Medium | Critical | Medium | Short-lived dedicated identity, mTLS or peer credentials, revocation, replay resistance, policy remains independently restrictive. |
| Policy/configuration drift | Medium | Critical | Low-Medium | Canonical policy artifact, digest binding, startup verification, negative-test matrix, drift alarm, fail closed. |
| Provider spoofing | Low-Medium | High | Low-Medium | Authenticate Docker-facing locality and adapter-facing peer; pin API/version; correlate each request/response. |
| Payload injection or parser attack | Medium | High | Low-Medium | Closed schema/fields, strict types, bounded depth/count/bytes, no dynamic evaluation, fuzz/negative tests. |
| Identity spoofing by labels/names | Medium | High | Medium | Registry-first tuple, exact filters, duplicate/conflict rejection, observed identity never becomes declared identity. |
| Response tampering | Low-Medium | High | Low | Local Unix mediation or mTLS, integrity/correlation, safe digest, strict parsing. |
| Oversized payload or cardinality | Medium | High | Low | Request/response/record limits, exact-target count, one-shot stats, no streams, resource quotas. |
| Resource exhaustion / DoS | Medium | High | Low-Medium | Rate, concurrency, CPU/memory/PID/FD, timeout and circuit limits; proxy failure cannot affect workload. |
| Container escape from proxy | Low | Critical | Medium | Non-root where feasible, no privileged mode, capability drop, seccomp/AppArmor, read-only filesystem, patched runtime. |
| Docker host compromise through daemon authority | Low-Medium | Critical | Medium | Sole socket holder, strict proxy policy, deny all control classes, penetration/negative tests, incident isolation. |
| Log leakage | Medium | High | Low-Medium | Structured allowlist logs, redaction before persistence, no raw body/header/credential, bounded access and retention. |
| Replay | Medium | High | Low | Nonce/correlation, short authorization window, monotonic attempt count, certificate/session binding, timestamp/skew checks. |
| Clock manipulation | Low-Medium | Medium | Low | Authenticated time source, measured skew, future/stale rejection, evidence invalidation. |
| Certificate compromise | Low-Medium | Critical | Medium | Dedicated CA/scope, short validity, protected key, rotation/revocation test, policy prevents unrestricted daemon access. |
| Network compromise | Medium on IP; Low on Unix socket | High | Low-Medium | Prefer Unix socket; otherwise mTLS, no host-published port, firewall/egress allowlist, no redirects. |
| Supply-chain or dependency compromise | Medium | Critical | Medium | Pinned digest, SBOM, provenance/signature verification, vulnerability threshold, approved base image, reproducible review. |
| Proxy image compromise | Low-Medium | Critical | Medium | Trusted build, signature and provenance, minimal image, no package manager/shell where practical, rollback digest. |
| Rate abuse | Medium | High | Low | Per-identity and per-target rate/concurrency limits, one-shot authorization, safe denial audit. |
| Unauthorized enumeration | Medium | High | Medium | Exact target filters, maximum one result, response field allowlist, explicit separate population-scope authorization. |
| Target bypass through encoding/query ambiguity | Medium | Critical | Low-Medium | Canonical parse before policy, reject duplicate/unknown parameters and alternate encodings, method/path/query tests. |
| Streaming/upgrade authorization bypass | Medium | Critical | Low | Deny events/logs/attach/exec/upgrade/gRPC and any response that cannot be completely bounded and filtered. |
| Audit loss or tampering | Low-Medium | High | Low-Medium | Append-only or integrity-protected sink where approved, sequence/correlation checks, fail closed when audit is required. |
| Automatic remediation escalation | Low | Critical | Low | No control endpoint, no reverse consumer path, EO and recurring activation remain separate gates. |

## Security Acceptance Criteria

Before implementation authorization, measurable evidence must prove:

1. A complete method/category/path-class/query/target/response policy defaults to deny.
2. Negative tests cover every denied category, all mutation methods, wildcard/empty/duplicate targets, alternate encodings, duplicated parameters, redirects, proxy chaining, upgrade, hijack, streaming, and gRPC or equivalent bypass.
3. Positive tests cover only the approved synthetic identity, lifecycle, health, restart, bounded stats, and version/availability cases.
4. The adapter has no Docker socket, Docker API, arbitrary network, subprocess, shell, credential, or control path.
5. The proxy alone models the socket boundary, but repository tests use no real socket or Docker access.
6. Authentication models fail closed for missing, expired, revoked, wrong-client, wrong-target, replayed, or drifted identity.
7. Response filtering removes all fields outside the canonical allowlist and proves secret/topology-bearing fields cannot pass.
8. Request/response bytes, records, nesting, concurrency, rate, CPU, memory, PIDs, descriptors, and timeouts are explicitly bounded.
9. Non-root, read-only filesystem, capability drop, `no-new-privileges`, seccomp/AppArmor, ingress/egress, and writable-path assertions are machine-verifiable configuration properties.
10. Image digest, source, SBOM, provenance, signature, vulnerability review, supported Docker API range, and configuration digest are required inputs.
11. Audit events are secret-safe, correlated, complete for allow/deny/failure, retention-bounded, and loss behavior is defined.
12. Rollback and disablement are deterministic, independently testable, and do not restart or mutate customer workloads.
13. Configuration, policy, identity, target, and artifact drift invalidate approval.
14. Registry, PLAT health, dashboard, EO, infrastructure, and FFFA mutation paths remain absent.

## Privileged Access Review Gate

Implementation does not pass this gate until an Architecture Gatekeeper review package contains all evidence below.

| Evidence | Pass Condition | Fail Condition |
|----------|----------------|----------------|
| Configuration review | Exact canonical configuration and digest; no unreviewed values or floating references. | Missing, generated-only, mutable, or drifted configuration. |
| Security checklist | Every acceptance criterion mapped to objective evidence. | Assertion without evidence or unresolved critical/high control. |
| Negative testing | Complete denied-category/method/bypass/target matrix passes. | Any write, enumeration, stream, upgrade, bypass, or fail-open result. |
| Authentication | Exact service identity and channel model pass wrong-client, expiry, replay, rotation, and revocation tests. | Location/network/token alone or reusable unrestricted daemon identity. |
| Authorization | Exact category, target, signal, window, and one-shot policy is enforced. | Wildcard, broad list, target substitution, or policy ambiguity. |
| Logging | Secret-safe allow/deny/failure/correlation evidence and retention policy validate. | Raw payload/secret leakage, missing denies, or unsafe audit loss. |
| Rollback | Adapter-first/proxy-second disablement and known-good artifact/config rollback pass without workload mutation. | Requires workload restart, Docker mutation, or unbounded outage. |
| Version and supply chain | Pinned image/config, supported API matrix, SBOM, provenance/signature, vulnerability disposition. | Floating tag, unsupported API, unverifiable image, or unresolved unacceptable vulnerability. |
| Target restriction | Synthetic exact-target and maximum-result proofs pass; population scope remains absent. | Broad enumeration or unexpected target data reaches adapter. |
| Policy compliance | Repository, privileged-integration, provider-contract, evidence, and lifecycle validators pass. | Any contradiction, unsafe exception, or missing approval owner. |
| Repository validation | Full tests and governed validators pass; diff/hygiene/link checks pass. | Error, unexplained warning, prohibited artifact, or code outside authorized scope. |

## Named-Target Observation Gate

This separate gate may be considered only after the privileged boundary is implemented, published, security-reviewed, and deployment-authorized. The approval package must bind:

- One eligible Registry subject, exact record/reference/hash, host, participation state, health-check requirement, Compose identity or approved unique runtime name, and declared image context.
- Exact Docker Engine and API version, proxy image/version/digest, adapter version/digest, contract/profile/policy versions, canonical configuration and policy digests.
- Approved endpoint categories, methods, filters, response fields, mandatory/optional signals, maximum result count, payload/time/rate/resource limits.
- Exact service identity, Unix-socket or mTLS boundary, certificate/secret references if any, validity, rotation and revocation evidence.
- Security-review completion reference, negative-test results, supply-chain evidence, configuration verification, and no-drift proof.
- One explicit observation window, one manual attempt limit, correlation/nonce, safe output location, raw-data prohibition or bounded diagnostic retention/deletion rule.
- Adapter-first/proxy-second stop procedure, rollback plan, incident escalation, workload non-regression checks, and invalidation procedure.
- Success criteria: exact identity, complete mandatory coverage, supported versions, valid provenance, bounded freshness, no material limitation, no unexpected target, no write/control capability, and clean post-observation validation.
- Stop conditions: auth or audit failure, version/config/Registry drift, unexpected enumeration, target ambiguity, write/control availability, secret exposure, resource threshold, clock/freshness failure, workload degradation, or any unapproved data.

Approval authority is the Architecture Gatekeeper with affirmative human Platform Administrator approval for the exact privileged boundary, target, and window. EO roles, provider adapters, automation, dashboards, and consumers cannot approve or expand the observation.

## Governance Recommendation for AB-012

Recommendation: **remain backlog**.

The provider architecture, repository adapter foundation, privileged integration governance, and this security review show a coherent candidate pattern. They do not yet demonstrate repeated successful use across independent provider integrations, privileged deployment safety, named-target evidence, recurring operation, or retirement evidence. Repository governance requires observed, reviewed, evidence-supported repetition before promotion.

Milestone 15 should reevaluate AB-012 after at least the repository-only proxy foundation and one separately approved privileged-boundary evidence cycle, preferably with a second materially different provider integration. This recommendation does not pre-authorize promotion in Milestone 15.

## Revised Lifecycle

The original lifecycle omits explicit artifact/configuration acceptance, eligible-target approval, privileged deployment authorization, and periodic reauthorization. The reviewed lifecycle is:

```text
Repository-only provider and proxy foundations
        |
        v
Implementation architecture and security review
        |
        v
Artifact, supply-chain, configuration, and negative-test acceptance
        |
        v
Eligible Registry subject approval
        |
        v
Privileged deployment authorization and verification
        |
        v
One-shot named-target observation authorization
        |
        v
Observation evidence, non-regression, and provider validation review
        |
        v
Read-only consumer integration
        |
        v
Recurring activation, monitoring, reauthorization, and retirement
```

No later gate is implied by success at an earlier gate. The published repository foundation is deterministic security evidence, not proof of service identity, privileged isolation, provider compatibility, or live denial enforcement.

## Architecture Decision

**Approved and published.**

The constrained proxy remains approved as the future privileged implementation target under the controls and gates in this review. The repository-only foundation is published, fixture-backed, unactivated, and transport-incapable. A socket-capable implementation, privileged deployment, and named-target observation remain distinct future gates and are not authorized by the repository foundation.

## Proposed Implementation Architecture Follow-On

A complete proposed follow-on package now selects a purpose-built minimal Go proxy, authenticated non-Docker Unix-socket protocol, closed fixed Docker dispatcher without a Docker SDK, digest-bound one-shot authorization, runtime enforcement mapping, supply-chain requirements, implementation-specific threat model, security test matrix, and separate implementation/deployment acceptance checklists.

The follow-on package is Architecture Gatekeeper approved and published. It resolves the architecture questions identified here but does not implement or authorize a socket-capable artifact. Implementation authorization, artifact acceptance, privileged deployment, eligible-subject approval, named-target observation, consumer integration, and recurring activation remain distinct gates.

## Authoritative External References

- [Docker Engine security and daemon attack surface](https://docs.docker.com/engine/security/)
- [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/)
- [Docker access authorization plugin behavior and limitations](https://docs.docker.com/engine/extend/plugins_authorization/)
- [Docker Engine API and versioning](https://docs.docker.com/reference/api/engine/)
- [Docker Engine API version history](https://docs.docker.com/reference/api/engine/version-history/)
- [Docker rootless mode](https://docs.docker.com/engine/security/rootless/)
- [Docker AppArmor guidance](https://docs.docker.com/engine/security/apparmor/)
- [Docker SBOM attestations](https://docs.docker.com/build/metadata/attestations/sbom/)

## Related Repository Documents

- [Production Provider Adapter Architecture](Production_Provider_Adapter_Architecture.md)
- [Production Provider Privileged-Access Security Design](Production_Provider_Privileged_Access_Security_Design.md)
- [Production Provider Adapter Contract](../specifications/Production_Provider_Adapter_Contract_Specification.md)
- [Production Provider Adapter Foundation Implementation Package](../milestones/Milestone_14/Production_Provider_Adapter_Foundation_Implementation_Package.md)
- [Constrained Proxy Repository Architecture](Constrained_Docker_API_Proxy_Architecture.md)
- [Constrained Proxy Repository Usage](Constrained_Docker_API_Proxy_Repository_Usage.md)
- [Constrained Proxy Foundation Implementation Package](../milestones/Milestone_14/Constrained_Docker_API_Proxy_Foundation_Implementation_Package.md)
- [Privileged Deployment Configuration Architecture](Privileged_Deployment_Configuration_Architecture.md)
- [Deployment Configuration Repository Usage](Deployment_Configuration_Repository_Usage.md)
- [Deployment Configuration Implementation Package](../milestones/Milestone_14/Privileged_Deployment_Configuration_Foundation_Implementation_Package.md)
- [Privileged Proxy Implementation Architecture](Privileged_Proxy_Implementation_Architecture.md)
- [Privileged Proxy Architecture Review Package](../milestones/Milestone_14/Privileged_Proxy_Implementation_Architecture_Review_Package.md)
- [Privileged Infrastructure Integration Standard](../governance/Privileged_Infrastructure_Integration_Standard.md)
- [Container Operational Health Specification](../specifications/Container_Operational_Health_Specification.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.3 | Recorded approval and publication of the purpose-built implementation architecture/security acceptance follow-on without opening any privileged or live gate. |
| 1.2 | Recorded the repository-only deployment configuration foundation as reviewable, content-bound prerequisite evidence without runtime enforcement, credentials, deployment, target, observation, or live authority. |
| 1.1 | Recorded publication of the repository-only proxy foundation as deterministic fixture/security evidence while retaining separate socket-capable implementation, privileged deployment, named-target observation, consumer, and activation gates. |
| 1.0 | Completed the formal constrained Docker API proxy architecture/security review, endpoint-category decisions, authentication/deployment recommendations, expanded threat model, pass/fail gates, AB-012 recommendation, and revised lifecycle without implementation or live authority. |
