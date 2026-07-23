# Production Provider Privileged-Access Security Design and Threat Model

**Document Version:** 1.2

**Status:** Accepted Design; Formal Proxy Security Review Complete; Privileged and Live Access Unauthorized

**Milestone:** PLAT-14.1A named prerequisite

---

## Purpose

This document defines the minimum security architecture, threat model, measurable acceptance criteria, incident response, and future review evidence required before any Production Provider Adapter may access a Docker or other privileged runtime boundary.

The repository foundation implements only strict offline validation, safe fixture paths, bounded payloads, version checks, secret-like-content rejection, deterministic failures, and import-level denial of network/socket/process behavior. It creates no credential, endpoint, proxy, collector, live adapter, deployment, or access authorization.

The formal constrained-proxy review approves this design for publication with binding clarification that authority/request flow and evidence flow are separate, network location alone is not authentication, streaming/upgrade/gRPC-or-equivalent bypass surfaces are denied in the first slice, and repository implementation, privileged deployment, and named-target observation retain distinct gates.

---

## Security Position

Access to the Docker daemon or socket is generally equivalent to substantial host control unless a technically enforced intermediary denies control capabilities. A read-only filesystem mount of the Docker socket does not by itself make Docker API use read-only.

The preferred pattern is:

1. Socket available only to a constrained proxy.
2. Default-deny read categories and methods.
3. No host-published proxy port.
4. Authenticated internal adapter-to-proxy traffic.
5. Adapter has no socket, shell, host mount, privileged mode, or mutation path.
6. One explicit eligible target, signal set, and observation window.
7. Negative proof for every prohibited capability before live observation.

A restricted proxy reduces blast radius but does not eliminate Docker-host compromise risk. Residual risk remains High until the exact configuration and denial behavior are proven at a separately authorized security gate.

---

## Security Zones

| Zone | Trust Level | Assets | Permitted Relationship |
|------|-------------|--------|------------------------|
| Docker host/runtime | Privileged/high impact | Host control, containers, images, volumes, networks, service availability. | Local socket to constrained proxy only. |
| Privileged proxy | High-risk intermediary | Socket authority, endpoint/method policy, request audit. | Bounded authenticated read responses to adapter/collector. |
| Adapter/collector network | Restricted | Named-target authorization, provider responses, normalized observations. | No public ingress; limited provider and output destinations. |
| Canonical evidence boundary | High-integrity/low privilege | Secret-free evidence, failures, provenance, digests. | Write bounded output only; no provider or Registry mutation authority. |
| Consumer boundary | Read-only | Assessments, reasons, confidence, validity. | Read governed outputs; no reverse control path. |

No trust transitively crosses zones. A valid provider response does not become trusted canonical evidence until strict validation; canonical evidence does not authorize health, execution, or remediation by itself.

---

## Proxy Controls

The later security gate must provide the exact current provider-contract mapping. This architecture specifies categories, not endpoint paths.

- Default deny all categories, methods, upgrades, streams, and extensions.
- Allow only the minimum read categories proven necessary for named-target resolution, lifecycle, health-check, restart, and explicitly approved stats.
- Deny every write/control category, including exec, create, start, stop, restart, kill, pause, unpause, remove, rename, update, attach, copy/archive write, build, commit, image mutation/pull where not explicitly approved, volume, network, plugin, secret/config, swarm, service, node, task, session, auth, and system mutation.
- Permit only read methods required by the approved categories; all mutation-capable methods return a deterministic denial.
- Enforce exact target scoping at the proxy when technically possible. When not possible, expose only the narrowest filterable read and enforce exact target validation in the adapter; document residual enumeration risk.
- Bind only to an isolated internal network; no public, Internet, or unrestricted LAN port.
- Require authenticated parties. Crossing a host boundary additionally requires mutually authenticated TLS or an Architecture Gatekeeper-approved equivalent.
- Disable redirects, arbitrary upstream selection, and proxy chaining.
- Apply connection, request, response-size, concurrency, and rate limits.
- Log safe timestamp, correlation ID, authenticated client, category/method result, target scope, response classification, and denial—never credentials or full payloads.
- Pin image/version and configuration digest; prohibit floating tags and silent configuration drift.
- Fail closed on unknown categories, malformed requests, unsupported versions, auth failure, policy-load failure, or audit failure where loss of audit would make operation unsafe.
- Expose a distinct adapter-facing protocol boundary; never forward or share the Docker socket and never relay arbitrary Docker requests.
- Deny streaming, connection upgrade, hijack, attach, logs, events, gRPC or equivalent authorization bypass, and any response that cannot be completely bounded and field-filtered in the first slice.
- Canonically parse methods, paths, query parameters, encodings, targets, and duplicates before authorization; reject alternate-encoding or request-smuggling ambiguity.
- Treat non-root membership in the Docker-socket group as privileged daemon authority rather than a least-privilege substitute.

---

## Collector Controls

If OpenTelemetry or another collector is used:

- Run as a dedicated non-root UID/GID with no privileged mode.
- Mount no Docker/containerd socket; use only the constrained proxy.
- Use a read-only root filesystem and explicit writable ephemeral directories.
- Drop all Linux capabilities and set `no-new-privileges`; apply seccomp/AppArmor or equivalent default-deny confinement.
- Mount only reviewed immutable configuration and runtime secret references; no broad host filesystem, home, Docker data, device, or platform-data mounts.
- Apply CPU, memory, process, file-descriptor, queue, batch, and payload limits.
- Restrict egress to the proxy, approved internal transport, and required health/audit sink; deny Internet egress during observation unless separately justified.
- Restrict ingress to an internal scrape/health boundary with no host-published port unless separately approved.
- Pin image source, version, digest, configuration digest, and supported component set.
- Review upstream maturity, vulnerabilities, release notes, and breaking changes before each upgrade.
- Define atomic configuration rollback and image rollback without affecting customer services.
- Allowlist metadata and processors; environment values, command arguments, raw labels, mounts, paths, and secrets are denied.

---

## Adapter Controls

- No shell, subprocess, dynamic command construction, code evaluation, plugin loading, reflection-based providers, or arbitrary URL input.
- Exact provider base boundary from reviewed configuration; no user-controlled scheme/host/port/path construction.
- Strict connect, response, collection, and total timeouts.
- Bounded retries that end inside the authorization window; no infinite retry or recurrence.
- Maximum request/response bytes, records, signals, identity candidates, warnings, limitations, and log events.
- Exact accepted content type, encoding, provider version, JSON shape, value type, unit, timestamp, and unknown-field policy.
- Reject oversized, malformed, future-dated, replayed, unsupported, ambiguous, conflicting, secret-like, path-unsafe, or symlink-unsafe inputs.
- Validate named target before canonical normalization; deny arbitrary enumeration output.
- Emit deterministic failure/limitation results; never convert provider failure into service Unhealthy.
- Never mutate Registry, health status, providers, services, configuration, deployment, or infrastructure.
- Never include credentials or raw provider payloads in canonical evidence.
- Stable output and audit correlation; output file creation, if authorized later, must use a safe bounded path and atomic write.

---

## Secrets

Credentials may be unnecessary when proxy and adapter share a strongly isolated same-host network and the security review proves no unauthorized peer can join it. If authentication requires a credential:

- Store it in an approved runtime secret boundary outside Git and outside canonical evidence.
- Scope it to one proxy/provider, client, target policy, and authorization duration where supported.
- Deliver by a least-exposure mechanism; environment variables are disfavored when they can appear in inspection output.
- Define owner, issuance, rotation, expiry, revocation, emergency revocation, and deletion.
- Exclude it from command lines, process arguments, logs, metrics, traces, exception text, raw-response references, and screenshots.
- Fail closed when missing, expired, revoked, unreadable, or inconsistent.

No placeholder secret, example token, private key, or production credential is created by this architecture package.

Same-host or isolated-network location alone is not authentication. The preferred same-host model is a second non-Docker Unix-domain socket with restrictive ownership/mode and verified peer/service identity. Any IP transport requires mutually authenticated TLS with a dedicated, revocable client identity. A bearer token may supplement but must not replace enforceable channel and service identity.

---

## Named-Target Authorization Control

Authorization binds one eligible Registry subject, exact record hash, host, declared Compose identity or approved unique runtime name, adapter/provider/configuration versions and digests, requested signals, observation mode, time window, output boundary, raw-retention rule, and stop conditions.

- Wildcards and “all containers” are prohibited by default.
- Target discovery outside the governed tuple is prohibited.
- Population enumeration needed to prove conclusive absence is a separate explicit authorization scope and must not be implied by named-target observation.
- Unexpected containers are not returned as arbitrary inventory and cannot create Registry records.
- Authorization cannot be reused after expiry, Registry drift, adapter/provider/configuration drift, or target change.

---

## Raw Payload and Privacy Controls

The default is no full-payload retention. Before parsing, compute a digest only when safe and useful; after parsing, dispose of raw bytes unless the authorization explicitly permits a redacted diagnostic artifact.

Potentially sensitive content includes environment variables, commands, mounts, labels, network details, image registries, paths, hostnames, tokens, credentials, and household topology.

- Canonical output uses allowlisted fields only.
- Redaction occurs before any diagnostic persistence or external logging.
- Diagnostic payloads stay outside Git in an access-controlled runtime store and are deleted after the approved period, normally within 24 hours.
- Repository evidence contains sanitized counts, hashes, limitations, and provenance—not raw runtime content.
- Access and deletion events are audited without reproducing sensitive values.

---

## Threat Model

| Rank | Asset / Threat Source | Attack Path and Impact | Prevention | Detection | Response | Residual Risk |
|------|-----------------------|------------------------|------------|-----------|----------|---------------|
| High | Docker host / compromised adapter or client | Broad daemon API enables container control, mount abuse, credential access, or host takeover. | No direct socket; constrained proxy; default deny; isolated network; auth. | Denied-request logs, configuration digest, host/service integrity checks. | Stop adapter then proxy, revoke credentials, preserve services, investigate. | Medium after proof; High before proof. |
| High | Proxy policy / misconfiguration | Write/control or broad enumeration accidentally exposed. | Reviewed generated policy, closed allowlist, immutable config, no host port. | Automated negative tests for every prohibited category/method; drift monitoring. | Disable proxy, invalidate authorization, correct under new review. | Medium. |
| High | Credentials / theft or replay | Unauthorized provider access or target observation. | Short-lived least-scope secrets, mTLS where required, no Git/log exposure. | Auth failures, client identity audit, replay/correlation checks. | Revoke/rotate, stop observation, review disclosure. | Medium. |
| High | Canonical identity / malicious or spoofed labels | Container labels impersonate an approved subject and manipulate health. | Registry-first exact tuple, labels as observations only, no fuzzy/image-only match. | Conflicting/duplicate identity findings and reconciliation logs. | Reject evidence, invalidate observation, review Registry/runtime state separately. | Medium. |
| High | Provider response / malicious malformed data | Parser exploit, type confusion, secret injection, or health manipulation. | Strict parser, size/depth/count limits, bounded fields, no code execution. | Rejection metrics and deterministic failure audit. | Stop adapter, retain safe digest, patch under implementation gate. | Low to Medium. |
| High | Supply chain / image or dependency tampering | Malicious proxy, collector, or adapter gains privileged reach. | Pinned source/version/digest, minimal dependencies, provenance and vulnerability review. | Digest verification, SBOM/signature where available, vulnerability alerts. | Disable component, revoke access, roll back to reviewed digest. | Medium. |
| High | Automatic remediation escalation | Health or failure output triggers unauthorized control. | No control path; consumer/EO gates; evidence never authorizes action. | Audit confirms no mutation calls; workflow conformance checks. | Suspend consumer/automation and escalate to Gatekeeper. | Low. |
| Medium | Stale or replayed observation | Old Healthy evidence appears current. | Time-aware contract, nonce/correlation, authorization window, 30/60 policy. | Clock/delay metrics, duplicate IDs, replay detection. | Reject, mark provider evidence unusable, investigate clock/transport. | Low to Medium. |
| Medium | Denial of service / oversized payload or cardinality | Memory/CPU exhaustion or delayed freshness. | Byte/record/concurrency/rate/resource limits and timeouts. | Limit/timeout events, resource monitoring, queue depth. | Stop adapter/collector, reduce scope, preserve customer services. | Low to Medium. |
| Medium | Path traversal or symlink attack | Read/write outside approved output or supporting-artifact boundary. | Repository-relative allowlist, resolve-and-contain, symlink rejection, atomic safe output. | Path-rejection audit and repository hygiene checks. | Reject output, stop observation, inspect filesystem boundary. | Low. |
| Medium | Unauthorized target enumeration | Household container inventory or metadata exposed. | Named-target authorization, proxy filtering where possible, no wildcard output. | Request scope logs, unexpected count/coverage findings. | Stop collection, delete unauthorized payload, review exposure. | Medium where provider cannot scope. |
| Medium | Adapter compromise / lateral movement | Network access used to reach other services. | Isolated network, egress allowlist, non-root, read-only FS, no capabilities. | Network-flow audit, unexpected destination alerts. | Stop/recreate adapter, revoke secret, inspect peers. | Low to Medium. |
| Medium | Secret leakage through payloads/logs | Environment, labels, headers, commands, or paths exposed. | Field allowlist, pre-persistence redaction, no full payload/logging. | Secret-pattern scanning and manual evidence review. | Stop, delete/rotate/revoke, incident review. | Medium. |
| Medium | Image/version drift | Provider semantics change and normalization becomes incorrect. | Version pin/support matrix, fail closed on unsupported versions. | Version mismatch and fixture regression failures. | Disable observation, update only through reviewed gate. | Low. |
| Medium | Health-result manipulation | Provider or dashboard asserts Healthy/Unhealthy directly. | Adapter cannot emit health; PLAT policy and signed/traceable artifact chain. | Contract validation and consumer conformance tests. | Reject artifact, suspend consumer, investigate provenance. | Low. |
| Medium | Collector processor/config tampering | Signals, labels, timestamps, or units are silently transformed. | Immutable reviewed config digest and closed processor set. | Config digest verification and normalization equivalence tests. | Roll back config, invalidate affected evidence. | Low to Medium. |
| Medium | Audit/log leakage or loss | Secrets leak or actions become untraceable. | Bounded structured allowlist logs, redaction, retention, fail-safe audit behavior. | Secret scan, missing-sequence/correlation alerts. | Stop unsafe observation, preserve safe evidence, rotate exposed secret. | Low. |
| Low | Clock integrity failure | Incorrect freshness or observation windows. | Synchronized clocks, measured skew, future-time rejection. | Skew and end-to-end delay evidence. | Mark evidence unusable; fix clock outside this gate. | Low. |
| Low | Consumer presentation failure | Missing/expired data shown as Healthy. | Published consumer contract, explicit no-data/expired states. | Dashboard/API conformance tests. | Disable presentation, retain authoritative assessment. | Low. |
| Low | Raw-retention growth | Runtime store exhausts disk or retains sensitive data too long. | Default no retention, byte/time quotas, deletion and rotation. | Quota/age audits. | Delete under approved policy, stop diagnostic retention. | Low. |

---

## Measurable Security Acceptance Criteria

Before provider implementation can be considered security-ready:

1. Adapter and collector have no direct Docker/containerd socket and no privileged mode.
2. Only the proxy has the reviewed read-only socket mount; no host-published port exists.
3. Default-deny policy is machine-testable and every prohibited control category/method is denied.
4. The exact approved read categories are documented against current official provider contracts.
5. Named-target/wildcard/unauthorized-target negative tests pass.
6. Authentication, rotation, revocation, and missing-secret failure behavior are proven where credentials are used.
7. No credential, token, key, or secret value exists in Git, evidence, logs, metrics, traces, or command arguments.
8. Non-root UID/GID, read-only root filesystem, all-capability drop, no-new-privileges, confinement profile, resource limits, and egress limits are verified.
9. Strict provider parsing rejects unknown required fields, unsupported versions, invalid content type, malformed data, oversize payloads, excess cardinality, unsafe paths, and secret-like content.
10. Connection/response/total timeouts and bounded retry behavior are deterministic.
11. Provider failures and limitations produce valid failure/telemetry evidence, never service health.
12. Canonical evidence contains complete provenance and no raw provider object.
13. No Registry mutation, health-generation, control, remediation, deployment, or recurring path exists in the adapter.
14. Safe audit events cover start, auth, target, provider, collection, normalization, rejection, limitation, output, and no-mutation confirmation.
15. Disablement and rollback stop adapter first, proxy second, preserve customer services, and revoke access.
16. Fixture and mock-provider security tests pass without network or live provider access.
17. Exact configuration, image, adapter, authorization, and Registry digests are bound before any named-target gate.
18. Architecture Gatekeeper and human Platform Administrator approve the privileged boundary before connection.
19. Streaming, upgrade, hijack, attach, logs, events, gRPC or equivalent bypass, duplicated/ambiguous query parameters, and alternate target encodings are denied by negative tests.
20. Image digest, source, SBOM, provenance/signature evidence, vulnerability disposition, supported Docker API range, and configuration digest are verified before privileged deployment.
21. Repository implementation approval, privileged deployment authorization, and named-target observation authorization are recorded as separate non-transitive decisions.

Security acceptance proves the reviewed configuration and repository behavior meet the bounded design. It does not prove absence of all upstream vulnerabilities, live provider compatibility, target eligibility, customer-service non-regression, recurring safety, or operational readiness.

---

## Named-Target Security Review Evidence

The future security gate must include:

- Data-flow and deployment diagram.
- Exact image/artifact versions, digests, provenance, support/maturity, and vulnerability review.
- Exact proxy read policy and complete negative-test matrix.
- Network bindings, membership, firewall/segmentation, authentication, and TLS decision.
- Socket, filesystem, capability, seccomp/AppArmor, UID/GID, resource, ingress, and egress inventory.
- Secret issuance/rotation/revocation evidence or proof no secret is required.
- Target authorization and enumeration bounds.
- Payload size, content, redaction, retention, deletion, and audit configuration.
- Timeout, retry, failure, disablement, rollback, and incident-response tests.
- Proof that customer-facing services, Registry, PLAT health, and infrastructure cannot be mutated through the observation path.

---

## Disablement and Incident Response

1. Stop the adapter or collector.
2. Stop or isolate the proxy if compromise, policy error, secret leakage, or unexpected capability is suspected.
3. Revoke credentials and authorization.
4. Preserve customer-facing services; do not restart, recreate, or modify the observed workload as a monitoring response.
5. Retain safe configuration digests, bounded logs, response hashes, timestamps, and findings; do not retain leaked secret values.
6. Delete unauthorized raw payloads under incident evidence rules.
7. Invalidate derived evidence and assessments for the affected window.
8. Require Architecture Gatekeeper review before re-enabling access.

## Repository Security Evidence

The repository implementation accepts only synthetic fixture data from a fixed governed directory, rejects symlinks, traversal, oversized input, malformed JSON, duplicate and unknown fields, unsupported future versions, unsafe authorization references, secret-like content, capability mismatches, and invalid or duplicate identity. Static tests prohibit network, socket, subprocess, shell, and random imports in the adapter modules. These controls prove the offline boundary only and do not reduce the residual risk of a future privileged provider.

---

## Related Documents

- [Production Provider Adapter Architecture](Production_Provider_Adapter_Architecture.md)
- [Production Provider Adapter Contract Specification](../specifications/Production_Provider_Adapter_Contract_Specification.md)
- [Privileged Infrastructure Integration Standard](../governance/Privileged_Infrastructure_Integration_Standard.md)
- [Container Operational Health Specification](../specifications/Container_Operational_Health_Specification.md)
- [Docker 29 Container Metrics Compatibility Assessment](Docker_29_Container_Metrics_Compatibility_Assessment.md)
- [Provider Adapter Repository Usage](Production_Provider_Adapter_Repository_Usage.md)
- [Formal Privileged Access Security Review](Privileged_Access_Security_Review_and_Constrained_Docker_API_Proxy_Architecture_Validation.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Incorporated the formal proxy security review: distinct authority/evidence flows, enforceable service identity, first-slice stream/upgrade/bypass denial, supply-chain proof, and separate implementation/deployment/observation gates. |
| 1.1 | Recorded bounded repository security validation and deterministic fixture/mock isolation without credentials, endpoints, proxy configuration, privileged access, or live observation. |
| 1.0 | Accepted and published privileged-access security design, trust zones, proxy/collector/adapter/secret controls, threat model, acceptance criteria, and incident response; privileged and live access remain unauthorized. |
