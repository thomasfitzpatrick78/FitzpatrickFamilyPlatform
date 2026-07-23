# Privileged Deployment Configuration Repository Architecture

**Document Version:** 1.1

**Status:** Repository Foundation Implemented; Configuration Only; No Deployment Authority

**Milestone:** PLAT-14.1A; Bravo workstream

## Purpose and Boundary

This architecture establishes a versioned repository configuration layer for a possible future privileged deployment of the constrained Docker API proxy. It makes the proposed deployment shape reviewable before any infrastructure interaction is authorized.

The foundation owns immutable contracts, strict parsing, deterministic validation, canonical digests, version compatibility, governed fixtures, and read-only Platform EAP inspection. It does not own or implement deployment, execution, Docker or Docker API access, sockets, listeners, networking, credentials, certificates, authentication, named-target authority, Registry mutation, live observation, or infrastructure control.

## Configuration Flow

```text
Governed repository fixture
        |
        v
Strict duplicate/missing/unknown-field parsing
        |
        v
Immutable configuration contracts
        |
        +---- incompatible or unsafe ----> deterministic findings
        |
        v
Proxy/provider/policy/security compatibility
        |
        v
Canonical SHA-256 configuration digest
        |
        v
Repository-only validation evidence
```

There is no apply, deploy, connect, listen, authenticate, observe, or mutate step.

## Contract Model

Contract version `1.0` defines:

- `DeploymentConfiguration` and `ConfigurationBundle` as the complete content-bound configuration package.
- `DeploymentProfile` for `RepositoryOnly`, `FutureDevelopment`, `FutureValidation`, and `FutureProduction`; all profiles keep deployment and execution disabled.
- `DeploymentIdentity` for exact synthetic identity, scope, authority, fixture approval reference, validity window, authentication mode, and future transport requirements.
- `RuntimeConfiguration`, `RuntimeSecurityConfiguration`, and `ResourceLimitConfiguration` for required controls and bounded resources without creating a runtime.
- `DeploymentAuditConfiguration` for required event names, redaction, and fixture-local destination metadata.
- Proxy, adapter, and endpoint-policy configuration contracts bound to the published Proxy and Provider foundations.
- `DeploymentCompatibility` for exact version negotiation across configuration, proxy, provider, adapter, policy, identity, runtime, security, resource, and audit contracts.
- `ConfigurationDigest` for repository-standard canonical SHA-256 content binding.

Every contract is immutable. JSON parsing rejects malformed objects, duplicate fields, missing fields, unknown fields, unsupported contract versions, and oversized input.

## Profiles and Identity

Profiles are descriptive review contexts, not executable environment definitions. `FutureProduction` records conceptual `FutureMutualTLS` requirements so a later gate cannot overlook mutual authentication; it contains no certificate, credential, endpoint, socket, or authentication implementation.

Identity is synthetic and fixture-only. Exact non-wildcard values, an explicit fixture approval reference, and an ordered validity window are required. No profile identifies an Infrastructure Registry record or live target.

## Runtime and Security Controls

The contracts require non-root execution, a read-only filesystem, dropping `ALL` capabilities, seccomp, AppArmor, independent disablement, bounded memory/CPU/process/concurrency/timeouts, disabled restart, structured secret-safe logging, and deterministic audit requirements. Privilege escalation, credential loading, certificate loading, execution, deployment, runtime access, socket access, listener creation, network access, live-provider access, and named-target access are all prohibited by validation.

These values describe prerequisites for a future implementation. They do not enforce operating-system or container-runtime controls and are not evidence that a privileged deployment is safe or active.

## Endpoint Policy Binding

The configuration reproduces the complete published Proxy Foundation category matrix and binds its canonical policy digest, versions, method permissions, request/response bounds, record limit, allowed canonical signals, denied categories, and future categories. Validation rejects drift from the Proxy Foundation rather than creating a second policy authority.

## Compatibility and Digests

Compatibility validation requires exact supported versions for the deployment, profile, proxy, provider, adapter, policy, runtime, security, limits, audit, identity, and endpoint-policy contracts. The version-negotiation result is deterministic and read-only.

The bundle digest covers the full deployment configuration, including policy, runtime, identity, security, limits, audit, proxy, adapter, and compatibility content. It uses canonical JSON plus SHA-256 and supports deterministic equality and mismatch detection. It is integrity evidence, not an approval signature or authorization token.

## Safety Architecture

Static tests prohibit deployment modules from importing or calling socket, Docker SDK, HTTP client, subprocess, shell, SSH, networking, environment-derived runtime behavior, credential loading, or certificate loading capabilities. Fixture paths are repository-owned, bounded, traversal-resistant, and symlink-resistant.

The Platform EAP surface exposes only repository fixture inspection and validation. It has no `live`, `apply`, `deploy`, `activate`, or target-selection command.

## Later Gates

This foundation does not approve a socket-capable implementation. The Architecture Gatekeeper-approved and published purpose-built proxy architecture maps these descriptive values to future enforcement and acceptance evidence but contains no runtime capability. Socket-capable implementation, artifact acceptance, enforced authentication, credentials/certificates, exact eligible Registry subject, deployment, observation, consumer integration, recurrence, and activation remain separate gates.

AB-012 remains a candidate and is not promoted by this repository-only evidence.

## Related Architecture Package

- [Privileged Proxy Implementation Architecture](Privileged_Proxy_Implementation_Architecture.md)
- [Runtime Security Control Specification](../specifications/Privileged_Proxy_Runtime_Security_Control_Specification.md)
- [Privileged Deployment Acceptance Checklist](../milestones/Milestone_14/Privileged_Deployment_Acceptance_Checklist.md)

## Change History

| Version | Change |
|---------|--------|
| 1.1 | Linked the approved and published enforcement and acceptance architecture without changing the repository-only boundary or opening implementation. |
| 1.0 | Established immutable repository-only deployment configuration, identity, runtime security, resource, audit, policy, compatibility, digest, fixture, and CLI boundaries without deployment capability. |
