# Privileged Proxy Implementation Architecture Review Package

**Document Version:** 1.0

**Status:** Architecture Gatekeeper Approved with Binding Clarifications; Published Architecture Package

**Milestone:** PLAT-14.1A named prerequisite; Bravo and Architecture Integration

**Review Date:** 2026-07-23

---

## Architecture Gatekeeper Decision

**APPROVED WITH BINDING CLARIFICATIONS**

The package selects a separate purpose-built minimal Go proxy with a non-Docker authenticated Unix-socket protocol, fixed Docker request dispatcher, exact policy/configuration/authorization digest binding, field-level response projection, enforced runtime-control design, supply-chain gates, formal threat model, complete security-test specification, and separate implementation/deployment acceptance checklists.

This recommendation is for architecture publication only.

| Gate | Recommendation |
|------|----------------|
| Architecture publication | Approved and published by this package |
| Future socket-capable implementation authorization | Not authorized; new exact implementation work package required |
| Privileged deployment authorization | Not authorized; implementation acceptance and exact-host gate required |
| Named-target observation authorization | Not authorized; eligible subject and one-shot approval required |

## Repository Baseline

- Repository: `FitzpatrickFamilyPlatform`, branch `main`.
- Verified starting HEAD, fetched `origin/main`, and live remote `main`: `1fdabb7665beeb0a2db9d9cf6dce5554b80a0ae9`.
- Starting ahead/behind: `0/0`; starting tree: clean.
- Registry schema `1.1`; all 39 records validate; Digital Twin integrity passes.
- Completed migration: five `not_applicable` records; completion/rollback evidence validates.
- Current migration: 0 apply, 16 review-required, 23 no-change.
- PLAT-14.1A, Provider, Proxy, and Deployment Configuration foundations remain repository-only, fixture-backed where applicable, and unactivated.

## Duplication Review

The package reuses:

- Proxy Foundation policy v1.0 as the single category authority.
- Deployment Configuration Foundation versions, digests, limits, identity, runtime, security, audit, and compatibility models.
- Provider Adapter Contract target, authorization, evidence, limitation, and failure boundaries.
- Privileged Access Security Review endpoint-category, same-host, service-identity, nonstreaming, response-filtering, and gate decisions.
- Registry, PLAT-14.1A, provider, health, consumer, and EO authority boundaries.

It does not introduce another policy engine, canonical evidence model, health decision model, deployment executor, provider adapter, Registry identity, governance standard, or live capability.

## Decision Summary

The weighted decision matrix scores the purpose-built option 325/335. General proxies and existing Docker socket proxy products are ineligible because their broad relay/configuration surfaces make the required non-Docker contract and complete response/authorization enforcement materially harder to prove. Combining adapter and proxy is rejected because it collapses privilege and evidence boundaries.

The architecture snapshot selects Go `1.26.5`, standard library plus pinned `golang.org/x/sys` `v0.47.0`, a static `scratch` image, a length-prefixed canonical JSON protocol over a second Unix socket, `SO_PEERCRED` local peer context, governed service identity, and Ed25519-signed one-shot authorization. The proxy uses no Docker SDK or generic reverse proxy.

## Binding Clarifications

1. Go, `x/sys`, Docker API, container-base, and supply-chain versions are review-time inputs only. Implementation acceptance must revalidate and bind exact supported versions, revisions, digests, maintenance, advisories, vulnerabilities, licenses, provenance, signatures, SBOM, and end-of-life status.
2. `SO_PEERCRED` establishes local peer-process UID/GID/PID context only. Complete authorization also requires the governed service identity, signed one-shot authorization, exact subject and target, nonce, validity window and expiry, approval reference, approved operation/signal scope, and every required policy, configuration, deployment, Registry, adapter, proxy/implementation, trust-anchor, and trust-binding digest.
3. Replay denial is security-critical state. Nonce verification and consumption must be durable; unavailable, ambiguous, corrupt, stale, or unsuccessful replay-state verification or persistence fails closed.
4. Non-root execution is conditional on the exact approved Docker socket-ownership model. Docker-group membership, root fallback, supplemental root-equivalent groups, broader socket permissions, host-user mutation, daemon reconfiguration, privileged mode, or capability expansion are not implicitly authorized; incompatibility stops for architecture review.
5. `System` and all reserved compatibility operations remain denied. Documentation of a potential Docker API call grants no execution, policy, configuration, deployment, or live-test authority.
6. Architecture acceptance does not authorize source implementation, dependency retrieval, compilation, image creation, Docker/socket access, credentials, deployment, target selection, observation, consumers, recurrence, or activation.
7. ADR-012 is approved only as an architecture decision. Implementation has not begun; no artifact, privileged deployment, target, observation, or activation is accepted or authorized.
8. AB-012 remains `Candidate - Remain Backlog`; no promotion to permanent Engineering Organization governance is authorized.

A read-only Docker socket mount is not the security boundary; fixed dispatch, complete authorization, response projection, confinement, fail-closed state, and independent disablement remain mandatory. Declared configuration is not enforcement proof, and a compromised proxy retains Critical Docker-daemon impact.

## ADR Decision

ADR-012 is approved because the purpose-built technology, separate process boundary, non-Docker transport, no-SDK dispatcher, and runtime/supply-chain strategy are durable choices not decided by ADR-007 or ADR-009 through ADR-011. Its `Approved` status follows repository ADR governance and means architecture acceptance only; `Implemented` remains `No`.

## AB-012 Decision

AB-012 remains `Candidate - Remain Backlog`. This architecture adds precise design and acceptance evidence but no implemented privileged boundary, deployment, named-target evidence, recurring operation, independent provider repetition, replacement, or retirement evidence. Promotion remains inappropriate.

## Customer-Facing Impact

The design reduces future Docker coupling for Platform Administrator, Operations Analyst, Platform Health Dashboard, and read-only operational API use cases. Each consumer still depends only on canonical PLAT-14.1A evidence and health contracts. No dashboard, API, or FFFA implementation is included.

## Review Artifacts

- [Architecture](../../architecture/Privileged_Proxy_Implementation_Architecture.md)
- [Decision Matrix](../../architecture/Privileged_Proxy_Architecture_Decision_Matrix.md)
- [ADR-012](../../architecture/decisions/ADR-012-Purpose-Built-Constrained-Privileged-Proxy.md)
- [Threat Model](../../architecture/Privileged_Proxy_Threat_Model.md)
- [Non-Docker Interface](../../specifications/Privileged_Proxy_Non_Docker_Adapter_Interface_Specification.md)
- [Runtime Security Controls](../../specifications/Privileged_Proxy_Runtime_Security_Control_Specification.md)
- [Supply-Chain Requirements](../../specifications/Privileged_Proxy_Supply_Chain_Security_Requirements.md)
- [Security Test Specification](../../specifications/Privileged_Proxy_Security_Test_Specification.md)
- [Implementation Acceptance](Privileged_Proxy_Implementation_Acceptance_Checklist.md)
- [Privileged Deployment Acceptance](Privileged_Deployment_Acceptance_Checklist.md)

## Validation Boundary

The publication package contains documentation and generated governed reports only. It has no executable artifact and therefore no socket, Docker, network, credential, certificate, deployment, Registry, infrastructure, EO activation, dashboard/API, or FFFA capability.

## Next Gate

After publication, the next possible gate is a separately approved **Repository-Only Privileged Proxy Source Implementation** work package for the exact ADR-012 design. Publication itself does not authorize source creation, dependency retrieval, compilation, test binaries, synthetic Docker-server fixtures, OCI images, or socket interaction.

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Published the Architecture Gatekeeper-approved architecture package with all eight binding clarifications and every implementation, deployment, observation, and activation gate preserved. |
