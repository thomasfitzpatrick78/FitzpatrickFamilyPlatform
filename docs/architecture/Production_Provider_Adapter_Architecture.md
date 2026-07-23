# Production Provider Adapter Architecture

**Document Version:** 1.4

**Status:** Accepted; Provider, Proxy, and Deployment Configuration Repository Foundations Published; Live Access Unauthorized

**Milestone:** PLAT-14.1A named prerequisite; no standalone work-item identifier assigned

---

## Purpose

This architecture defines how a future production provider adapter may collect bounded container-runtime observations and normalize them into the published Platform Operational Evidence contracts without making Docker, OpenTelemetry, Prometheus, cAdvisor, or any other provider authoritative for Platform identity or health.

The repository-only adapter foundation implements these provider-independent boundaries with strict fixtures, mock clients, deterministic normalization, and failure behavior. The repository-only constrained proxy foundation adds category policy, conceptual identity/authorization, exact synthetic-target validation, bounded responses, and deterministic denial evidence without a transport. The deployment configuration foundation now binds descriptive profiles, identity, runtime security, resources, audit, endpoint policy, compatibility, and canonical digests without deployment capability. None selects or implements a live provider, authorizes privileged access, identifies an eligible live target, activates recurring collection, or changes infrastructure.

---

## Repository Evidence and Constraints

- PLAT-14.1A is published, fixture-only, provider-free, read-only, and unactivated.
- Registry schema `1.1` validates 39 records. Five records are published as `not_applicable`; 16 subjects remain review-required; no current record is eligible for authoritative Container Operational Health evaluation.
- Pi-hole remains unresolved, unmigrated, and unassessed. It is not selected by this architecture.
- Container Evidence Profile `1.0` makes current lifecycle evidence mandatory and runtime health-check evidence mandatory when the Registry declares it required.
- The provisional lifecycle, health-check, telemetry, and advisory-resource aging boundary is 30 seconds and maximum current age is 60 seconds.
- cAdvisor remains scrapeable but has a published Docker 29/containerd identity limitation and cannot independently supply trustworthy named-container identity.
- The repository-prepared proxy and OpenTelemetry topology is not deployed or approved for access. It remains reusable evidence, not implementation authorization.
- Prometheus is an approved metrics transport under ADR-007, not declared-state, evidence, confidence, reconciliation, or health authority.

---

## Product Boundary

Production Provider Adapters collect bounded runtime observations from explicitly authorized sources, normalize them into canonical Platform Operational Evidence, and preserve provider limitations and provenance without owning Registry identity, health policy, health assessment, remediation, or activation.

### Adapter Ownership

- Connect to one explicitly authorized provider boundary.
- Strictly parse and validate one supported provider response contract.
- Extract provider-specific identity inputs without promoting them to declared identity.
- Normalize approved observations into canonical signals.
- Record provider identity, version, adapter version, timing, coverage, completeness inputs, limitations, warnings, and deterministic failures.
- Produce contract-valid evidence or a contract-valid provider failure result.

### Adapter Non-Ownership

- Registry authoring, migration, lifecycle, or canonical `subject_id` creation.
- Reconciliation outcomes or identity repair.
- Evidence-confidence or health-policy authority beyond applying published deterministic rules.
- Healthy, Degraded, Unhealthy, or Insufficient Evidence results.
- Dashboard interpretation, remediation, deployment, execution, orchestration, scheduling, or infrastructure mutation.

The Infrastructure Registry remains declared-identity authority. PLAT-14.1A remains reconciliation and health authority.

---

## Options Assessment

Security posture rates the strength of the constrained design; delivery risk rates implementation uncertainty, where Low is preferable.

| Option | Architecture and Privilege | Coverage and Identity | Material Limitations and Failure Modes | Commercial Alignment | Maintainability | Security Posture | Delivery Risk | First-Slice Suitability |
|--------|----------------------------|-----------------------|----------------------------------------|----------------------|-----------------|------------------|---------------|-------------------------|
| A. Constrained Docker Engine API proxy | Only the proxy reaches the Docker socket; a separate adapter uses an internal authenticated, default-deny, read-only boundary. | Best candidate for exact runtime identity, lifecycle, health-check state, restart facts, and bounded stats. | Proxy misconfiguration retains material host risk; API/version compatibility and named-target scoping require proof. | High | Medium | Medium | Medium | **Preferred primary**, subject to security review and denial proof. |
| B. Direct read-only Docker socket | Adapter or collector mounts the Docker socket directly. A read-only filesystem mount does not remove daemon authority. | Broad runtime visibility, but identity quality still depends on strict mapping. | Socket compromise can approach host control; weak isolation, poor per-method audit, excessive enumeration. | Low | Low | Low | High | **Rejected** for the first slice. |
| C. Docker daemon metrics through Prometheus | Docker or an exporter exposes metrics; Prometheus transports observations to a metrics adapter. | Useful engine/resource signals, but lifecycle, health-check, and exact Compose identity coverage are not proven. | Scrape loss, label drift, cardinality, delayed/stale series, and inability to distinguish absence from failure. | Medium | High | Medium | Medium | Supplemental only unless later proof establishes every mandatory signal. |
| D. OpenTelemetry bounded collector pipeline | Hardened collector obtains approved observations through a constrained boundary and exports to an internal transport. | Strong extensibility and resource normalization; Docker Stats coverage of required health-check semantics and exact identity remains unproven. | Processor complexity, alpha or version-dependent components, label transformation, partial pipelines, and transport delay. | High | Medium | High when no socket is mounted | Medium | Preferred **supplemental** resource path; not mandatory v1 authority. |
| E. cAdvisor | Existing internal scrape supplies host/cgroup and some resource observations. | Resource strengths, but published Docker 29/containerd identity is unreliable and runtime health-check semantics are absent. | Healthy scrape can coexist with incomplete container visibility; broad host mounts and misleading cgroup population. | Medium | High | Medium | High for mandatory evidence | Retain only as a bounded supplemental provider. |

### Rejected First-Slice Approaches

- Direct Docker or containerd socket access by the adapter or collector.
- cAdvisor-only health evidence.
- Prometheus scrape health or Docker daemon metrics as proof of service health.
- Multiple mandatory providers whose joint availability is required for Healthy.
- Dynamic provider discovery, plugin loading, or generalized provider orchestration.

---

## Recommended Provider Architecture

The accepted architecture establishes Option A as the preferred primary direction and Option D, transported through Prometheus where useful, as an optional supplemental direction.

```text
Governed named-target authorization
        |
        v
One-shot Production Provider Adapter
        |
        | authenticated bounded read requests
        v
Constrained Docker API Proxy
        |
        | only approved read categories
        v
Docker Engine / named runtime subject
        |
        v
Strict provider response parsing
        |
        v
Production Provider Adapter Contract v1 result
        |
        v
Canonical Operational Evidence JSON
        |
        v
PLAT-14.1A reconciliation and health evaluation
        |
        v
Read-only consumers

Optional supplemental path:
Docker Engine -> constrained proxy -> hardened OTel collector
              -> internal Prometheus transport -> resource-evidence adapter
```

The primary path must supply every mandatory signal needed by the approved target. Supplemental resource signals must not become mandatory for Healthy in v1. If the primary provider cannot supply lifecycle, required health-check state, exact identity inputs, and coverage evidence, the observation fails as insufficient provider evidence; a second mandatory provider is not silently added.

This was initially accepted as an architectural direction without implementation selection. The formal review now selects the constrained proxy as the future repository implementation target, but selects no product, version, configuration, deployment, target, credential, or live authorization.

The formal privileged-access review approves the constrained proxy as the future implementation target only under its binding default-deny category matrix, enforceable service identity, same-host dedicated deployment, non-streaming first slice, supply-chain controls, and separate repository implementation, privileged deployment, and named-target observation gates.

---

## Trust-Boundary Model

| Boundary | Trust and Authentication | Allowed Direction and Data | Prohibited Data or Action | Failure, Audit, and Validation Owner |
|----------|--------------------------|----------------------------|---------------------------|--------------------------------------|
| Registry to authorization input | High-trust repository declaration plus separately approved authorization reference. | Exact subject, Registry reference, host, governed Compose identity or runtime name, requested signals, time window. | Inferred identity, wildcard target, credentials, provider-discovered subject creation. | Fail closed on missing/invalid declaration. Registry validator and authorization gate own validation. |
| Docker host to privileged proxy | Host-controlled, privileged boundary; socket local to proxy only. | Minimum read categories required for approved target resolution and observations. | Writes, exec, lifecycle control, archive, build, image, volume, network, plugin, secret, swarm, system mutation, or broad unapproved enumeration. | Default deny; method/category audit and denial evidence. Platform Administrator owns deployment; security review validates. |
| Proxy to adapter | Authenticated internal boundary; no public or unrestricted LAN exposure. | Strict response content, bounded size, supported API version, named-target scope. | Socket forwarding, arbitrary URLs, redirects, streaming without bounds, control requests, secrets. | Timeout and deterministic provider failure. Adapter validates response; proxy logs safe request metadata. |
| Optional collector/transport | Lower trust than canonical evidence; replaceable transport. | Approved normalized or near-normalized resource observations with timestamps and provenance. | Health assertions, subject creation, arbitrary labels, environment variables, commands, raw secrets. | Partial/unavailable pipeline becomes provider evidence. Collector validates configuration; adapter validates semantics. |
| Provider adapter to canonical evidence | Adapter is a bounded translator, not authority for declared state or health. | Contract-valid one-signal evidence or structured provider failure; safe digests/references. | Raw payloads, credentials, provider-native arbitrary objects, Registry writes, health status. | Strict parse/normalize or no canonical record. Adapter owns provider-contract validation; PLAT owns canonical validation. |
| Canonical evidence to PLAT-14.1A | High-integrity repository/domain boundary. | Supported evidence/profile versions, exact subject linkage, provenance, time, coverage, limitations. | Unsupported major versions, unbounded extensions, unsafe references, provider health claims. | Reconciliation and health fail closed. PLAT-14.1A owns identity reconciliation and health. |
| PLAT-14.1A to consumers | Read-only governed output. | Assessment status, confidence, reasons, validity, evidence and reconciliation references. | Recalculated health, hidden limitations, no-data Healthy, execution authority. | Consumer renders failure explicitly. Consumer contract owner validates presentation. |

Runtime privilege, transport privilege, provider parsing, canonical evidence authority, health authority, and presentation are independent boundaries. A compromise or failure in one must not silently grant authority in another.

---

## Identity and Reconciliation Boundary

The adapter receives an already authorized Registry subject and records exact observed values for:

- Runtime container ID.
- Container or runtime name.
- Compose project and service labels.
- Image reference or digest when requested.
- Host and provider context.

These values are observation inputs and provenance only. The adapter must not create `subject_id`, fuzzy-match, repair Registry declarations, persist provider labels as Registry truth, use image identity as the sole match, or create records for unexpected containers.

Identity results are exact, absent, conflicting, duplicate, ambiguous, or unresolved. Duplicate or scaled observations produce a bounded unsupported/ambiguous result in v1; scaled-replica modeling remains a future architecture decision. Unexpected containers may be counted only when the named-target authorization explicitly permits bounded population coverage; they do not become Platform subjects.

---

## Evidence Coverage Matrix

Legend: D = directly available candidate; R = derivable; U = unsupported; L = unreliable; V = version-dependent; S = security-sensitive.

| Canonical Signal | A Proxy/API | B Direct Socket | C Daemon/Prometheus | D OTel Pipeline | E cAdvisor |
|------------------|-------------|-----------------|---------------------|-----------------|-------------|
| Lifecycle state | D, V, S | D, V, S | V or U | V | L |
| Runtime health-check state | D, V, S | D, V, S | U | V or U | U |
| Restart count | D, V, S | D, V, S | V | D/V | V |
| Restart occurrence window | R, V | R, V | R/V | R/V | R/L |
| CPU utilization | D/R, V, S | D/R, V, S | V | D/V | D but identity-limited |
| Memory utilization | D/R, V, S | D/R, V, S | V | D/V | D but identity-limited |
| Memory limit | D, V, S | D, V, S | V | D/V | D but identity-limited |
| Memory pressure | R under policy | R under policy | R/V | R/V | R/L |
| Provider availability | D | D | D | D | D |
| Expected-signal availability | R from requested/returned set | R | R | R | R with known limitation |
| Identity resolution inputs | D, V, S | D, V, S | V/L | V | L |
| Collection coverage | R; full-population proof needs explicit authorization | R, over-broad | R/V | R/V | L |
| Provider limitations | D from governed support matrix | D | D | D | D; limitation applies |

### Mandatory First-Slice Evidence

- Exact authorized target and Registry linkage.
- Current `container.lifecycle.observed_state`.
- Current `container.healthcheck.state` when the Registry requires it.
- Provider availability and supported-version evidence.
- Expected mandatory-signal availability.
- Exact identity-resolution result.
- Complete collection coverage for the authorized mandatory signal set.
- Provider limitation state showing no material limitation affects mandatory evidence.

Restart and resource signals remain advisory under policy version `1.0`.

---

## Multi-Provider Decision

Version 1 uses one primary provider for every mandatory signal and permits one fixed supplemental path for advisory resource signals. Supplemental failure cannot make a service Unhealthy and does not block Healthy when every mandatory primary signal qualifies under policy.

Conflict rules are deterministic:

1. Preserve both observations and their timestamps/provenance.
2. Mandatory primary evidence is evaluated only if the primary provider remains suitable.
3. Supplemental evidence cannot override primary lifecycle or health-check facts.
4. Material disagreement emits `conflicting_evidence`; PLAT reconciliation determines usability.
5. No arithmetic confidence merge or newest-value-wins shortcut is allowed.

---

## Freshness and Cadence Validation

The 30-second aging boundary and 60-second maximum age remain unchanged and provisional. A later named-target gate must record:

- Configured poll/scrape cadence and actual start/end times.
- Provider response duration, retries, and timeout outcomes.
- Transport and normalization delay.
- Host and adapter clock offset and synchronization state.
- Evidence publication delay, PLAT assessment time, and consumer read delay.
- P50, P95, and maximum end-to-end observation-to-assessment age over the approved window.
- Missed and partial collections and their longest consecutive duration.

Policy confirmation requires the maximum credible end-to-end delay plus approved jitter to fit within 60 seconds, and routine delay to fit within 30 seconds. Otherwise the observation gate recommends a separately reviewed policy version change; it does not edit active policy values.

---

## Raw Evidence and Privacy

Default retention is digest/reference only. Full provider payloads are not canonical evidence and are not committed.

- Retain a SHA-256 digest, provider/API version, bounded response classification, and approved runtime-store reference when reproducibility requires it.
- Store a minimal redacted payload only for a separately approved diagnostic need, outside Git, access-controlled, encrypted where supported, and time-limited.
- Remove environment values, commands, mounts, networks, labels outside the allowlist, paths, tokens, credentials, and secret-like values before retention.
- Default runtime retention is no longer than the named observation window plus 24 hours for review; a different duration requires explicit approval.
- Rotation and deletion must be testable and audited without recording deleted secret content.

---

## Logging and Audit

Required safe events are adapter start/version, authorization accepted or rejected, provider connection/denial, target resolved/unresolved/ambiguous, collection completed/partial/timed out, evidence normalized/rejected, limitation recorded, version mismatch, output written, and confirmation that no Registry mutation path was invoked.

Every event includes a correlation ID, safe subject and authorization references, result category, timing, and adapter/provider versions. Logs exclude credentials, raw payloads, environment values, commands, mounts, and arbitrary labels. Adapter correctness cannot depend on Grafana or Prometheus.

---

## Deployment Recommendation

| Form | Privilege and Exposure | Assessment |
|------|------------------------|------------|
| Adapter on Docker host process | Low network latency but weak process isolation and host deployment burden. | Not preferred. |
| Separate same-host adapter container | No socket mount, internal authenticated proxy connection, read-only filesystem, bounded resources, simple disablement. | **Preferred first deployment form**, one-shot and manually triggered. |
| Separate host | Better fault isolation but introduces TLS, credentials, LAN exposure, routing, and clock dependencies. | Defer. |
| Repository CLI from administrator workstation | Explicit invocation but requires a remote privileged transport and risks local credential handling. | Test/diagnostic only after separate design. |
| Scheduled governed automation | Recurring privilege and operational ownership. | Gate 6 only. |

The recommended initial form is a one-shot, named-target, read-only adapter container on the same host and isolated network as the proxy. It has no Docker socket, no host filesystem mounts, no host-published port, no recurrence, and no EO activation. This recommendation does not authorize deployment.

---

## Named-Target Live-Observation Gate

A future authorization package must bind:

- One exact eligible Registry subject and Registry record hash.
- One governed host and declared identity tuple.
- Exact adapter build/version/digest and supported contract/profile versions.
- Exact proxy/collector build, configuration digest, provider version, and approved read categories.
- Exact requested signals and explicit observation window.
- Authentication, secret references, network boundary, TLS decision, and safe output location.
- Raw-data handling and deletion time.
- Security review and default-deny/negative-test evidence.
- Manual start, timeout, stop, disable, and rollback procedure.
- Success criteria for identity, mandatory coverage, freshness, limitations, provenance, and non-regression.
- Stop conditions for unexpected enumeration, write capability, target ambiguity, secret exposure, unsupported version, excessive latency, malformed/oversized payload, customer-service regression, or scope drift.

It authorizes neither recurrence nor other containers, dashboards, APIs, EO activation, remediation, or infrastructure mutation.

---

## Future Lifecycle Gates

1. **Repository implementation:** client interfaces, strict parsing, fixture/mock-server normalization, security checks, and no live access.
2. **Privileged-access security review:** exact deployment/proxy/collector configuration, threats, secrets, network and denial proof plan.
3. **Named-target live observation:** one target, one window, no recurrence or mutation.
4. **Provider validation and policy confirmation:** coverage, identity, freshness, limitations, confidence, and policy evidence.
5. **Consumer integration:** read-only Operations Analyst, dashboard, or API consumption without health recalculation.
6. **Recurring activation:** separate EO and operations authorization, owner, cadence, disablement, monitoring, and repeated evidence.

No gate is authorized by this architecture package.

---

## Product Impact

- **Engineering Organization:** reusable privileged-provider gates, repeatable contracts, explicit security evidence, and auditable separation between implementation and activation.
- **Platform:** provider-independent live evidence without weakening Registry identity or Docker-host security.
- **Customer-facing path:** a future Platform Health Dashboard or household operations view can display governed health, freshness, confidence, and limitations without coupling to Docker or treating missing telemetry as Healthy. FFFA dependency awareness remains a future cross-product gate and is not implemented here.

---

## Risks and Open Decisions

| Rank | Decision or Residual Risk | Required Resolution |
|------|---------------------------|---------------------|
| High | A Docker proxy still fronts a host-control boundary; default-deny mistakes may expose mutation or broad enumeration. | Exact configuration, negative tests, attack review, and disablement proof at the security gate. |
| High | No Registry subject is eligible, so target-specific coverage and health-check needs are unknown. | Complete evidence and migration for a non-`not_applicable` subject before live planning. |
| High | Exact provider read categories and subject-scoping behavior are intentionally not fixed here. | Validate current official provider contracts and pin exact allowed requests during implementation/security review. |
| Medium | Docker/collector version evolution may change response semantics, labels, or supported signals. | Support matrix, strict version rejection, fixtures, upgrade review, and rollback. |
| Medium | OpenTelemetry resource coverage and maturity may not satisfy canonical lifecycle or health-check evidence. | Keep supplemental; prove signal inventory before promotion. |
| Medium | Full-population absence proof may require enumeration broader than one named target. | Separate explicit population-scope decision; absence otherwise remains insufficient evidence. |
| Medium | Clock skew and end-to-end delay may invalidate 30/60-second freshness. | Named-target cadence evidence and separate policy review if needed. |
| Low | No standalone work-item number is authorized. | Retain this as a named PLAT-14.1A prerequisite until portfolio authority assigns one. |

No new ADR is created because ADR-007 and ADR-009 through ADR-011 already establish the durable restricted-provider, evidence-first, declared/observed separation, and provider-independent contract principles. A new ADR is warranted only if a later Architecture Gatekeeper decision approves a durable technology/security choice that changes those principles.

The repeated combination of provider-independent contracts, fixture-first delivery, privileged-boundary threat modeling, named-target authorization, fail-closed parsing, and separate implementation/live/activation gates is broader than the current provider package. Existing governance covers privileged integration safety but does not consolidate the complete adapter lifecycle. Architecture Backlog candidate AB-012 therefore records a future `Secure External and Privileged Provider Integration Standard` evaluation. This publication does not create or promote that standard.

---

## Acceptance Criteria

The published architecture remains conformant when provider options, mandatory coverage, trust boundaries, identity authority, fixed v1 composition, freshness validation, raw-data handling, deployment direction, named-target authorization, later gates, security criteria, risks, and open decisions remain explicit while implementation and live access remain unauthorized.

## Repository Foundation Evidence

The published repository foundation implements the v1 contracts and abstract lifecycle without adding a provider connection. Its default adapter fails deterministically as unavailable, while its only working client reads governed synthetic fixtures. Normalization produces published Operational Evidence but does not reconcile identity, assign a subject, calculate health, or repair Registry state. This satisfies the repository implementation gate only; every provider-specific, privileged, named-target, live, consumer, recurring, and activation gate remains pending.

The published proxy repository foundation models the accepted primary boundary with a machine-readable default-deny category matrix, strict version/digest/target/authorization checks, and a fixture-only mock pipeline. It exposes no endpoint URL, socket, network client, credential, daemon access, deployment artifact, or live mode. This is reusable contract and negative-security evidence only; it does not satisfy the future privileged implementation or deployment gates.

---

## Related Documents

- [Production Provider Adapter Contract Specification](../specifications/Production_Provider_Adapter_Contract_Specification.md)
- [Privileged-Access Security Design and Threat Model](Production_Provider_Privileged_Access_Security_Design.md)
- [Platform Operations Domain Architecture](Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](../specifications/Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Container Operational Health Specification](../specifications/Container_Operational_Health_Specification.md)
- [Container Metrics Modernization Specification](../specifications/Container_Metrics_Modernization_Specification.md)
- [Privileged Infrastructure Integration Standard](../governance/Privileged_Infrastructure_Integration_Standard.md)
- [Docker 29 Container Metrics Compatibility Assessment](Docker_29_Container_Metrics_Compatibility_Assessment.md)
- [Provider Adapter Repository Usage](Production_Provider_Adapter_Repository_Usage.md)
- [Provider Adapter Foundation Implementation Package](../milestones/Milestone_14/Production_Provider_Adapter_Foundation_Implementation_Package.md)
- [Formal Privileged Access Security Review](Privileged_Access_Security_Review_and_Constrained_Docker_API_Proxy_Architecture_Validation.md)
- [Constrained Proxy Repository Architecture](Constrained_Docker_API_Proxy_Architecture.md)
- [Constrained Proxy Repository Usage](Constrained_Docker_API_Proxy_Repository_Usage.md)
- [Privileged Deployment Configuration Architecture](Privileged_Deployment_Configuration_Architecture.md)
- [Deployment Configuration Repository Usage](Deployment_Configuration_Repository_Usage.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.4 | Recorded repository-only deployment configuration contracts, exact compatibility and policy binding, and deterministic digests while preserving every deployment, target, observation, consumer, and activation gate. |
| 1.3 | Recorded publication of the repository-only constrained proxy contracts, policy, fixture mock, and deterministic denial evidence while preserving all privileged, named-target, live, consumer, and activation gates. |
| 1.2 | Recorded formal security validation of the constrained proxy as a future implementation target with binding endpoint, authentication, deployment, supply-chain, and lifecycle gates; no implementation or live authority granted. |
| 1.1 | Recorded the provider-independent repository foundation, strict synthetic fixtures, mock-only normalization, and deterministic failure evidence while retaining all live-provider and privileged gates. |
| 1.0 | Accepted and published production provider option assessment, preferred primary/supplemental direction, trust boundaries, coverage, deployment, privacy, named-target gate, and future lifecycle gates; implementation and live access remain unauthorized. |
