# Constrained Docker API Proxy Repository Architecture

**Document Version:** 1.1

**Status:** Repository and Deployment Configuration Foundations Implemented; Fixture Only; No Privileged or Live Authority

**Milestone:** PLAT-14.1A; Bravo workstream

## Purpose and Boundary

This document records the implemented repository-only foundation for the future constrained provider boundary accepted by the Privileged Access Security Review. The foundation models security decisions and proves deterministic denial behavior. A separate repository-only deployment configuration foundation now describes profiles, identity, runtime security, resources, audit, compatibility, and exact policy binding. Neither foundation implements a deployed proxy, transport, listener, runtime client, credential, named-target authorization, or infrastructure configuration.

The repository implementation owns immutable contracts, endpoint-category policy, conceptual authentication and authorization contexts, exact synthetic-target validation, bounded request and response validation, deterministic decisions, fixture responses, audit records, and Platform EAP commands. It does not own Registry state, provider normalization, canonical health, deployment, orchestration, governance approval, dashboard rendering, or infrastructure control.

## Repository Flow

```text
Synthetic ProxyRequest
        |
        v
Strict contract and authorization validation
        |
        v
Pure endpoint-category policy decision
        |
        +---- deny, future, invalid, expired, or unauthorized ----> ProxyFailure + ProxyAuditEvent
        |
        v
Governed synthetic fixture response
        |
        v
Bounded ProxyResponse validation
        |
        +---- rejected ----> ProxyFailure + ProxyAuditEvent
        |
        v
Validated fixture-only ProxyResponse + ProxyAuditEvent
```

There is no transport step. The mock reads only governed repository fixtures and cannot contact a runtime.

## Contracts and Versioning

Contract version `1.0` provides immutable models for request, response, decision, policy, configuration, identity, authentication, authorization, target, endpoint category, method category, response metadata, failure, audit event, capability declaration, parameters, records, and mock result. Strict JSON parsing rejects duplicate, missing, unknown, malformed, and unsupported-version fields. Canonical serialization and SHA-256 content binding make policy, configuration, and authorization drift deterministic.

## Endpoint Policy

| Category | Repository policy | First-slice meaning |
|----------|-------------------|---------------------|
| LifecycleObservation, HealthObservation, RestartInformation | Allowed | Synthetic, exact-target, read-only fixture evaluation only. |
| IdentityDiscovery, Statistics | ConditionallyAllowed | Allowed only after the same strict fixture authorization, version, digest, method, and target checks. |
| Events | Future | Reserved; the first slice returns `Future` and exposes no streaming method. |
| Images, Volumes, Networks, Build, Exec, Archive, Filesystem, Secrets, Plugins, Swarm, System, Configuration | Denied | Default-deny classification; no method is exposed. |

Only `ReadOnly` is supported. `BoundedAction`, `Mutating`, and `Streaming` are modeled for closed classification and are unsupported. Policy is expressed by category, never by provider URL or runtime path.

## Authentication and Authorization

`LocalUnixIdentity`, `MutualTLS`, `ServiceIdentity`, `AdministratorAuthorization`, and `NamedTargetAuthorization` exist only as technology-independent contract values. The repository implements no certificates, tokens, cryptography, credential loading, identity store, or authentication service.

Synthetic authorization binds an exact fixture Registry subject reference, subject, policy/configuration/proxy/adapter versions, configuration digest, endpoint categories, signals, observation window, expiry, and synthetic approval reference. Wildcards, missing references, digest drift, unsupported versions, expired windows, live Registry records, and production environments fail closed. This is test authorization, not named-target authorization for infrastructure.

## Configuration and Capability Invariants

- Fixture-only and `not_activated` are mandatory.
- Authentication and exact synthetic targets are mandatory.
- Request bytes, response bytes, parameters, and response records are bounded.
- Networking, runtime access, socket access, and streaming are declared unsupported.
- Policy default is `Denied` and every endpoint category is classified exactly once.
- Response target, versions, timestamps, provenance, limitations, signal scope, order, and size are revalidated before acceptance.

## Separation from Provider and Health Layers

The repository proxy returns constrained synthetic provider-shaped records. It does not produce canonical Operational Evidence or calculate health. The published Production Provider Adapter remains responsible for strict provider translation, and PLAT-14.1A remains responsible for reconciliation, confidence, freshness, and health. Consumers remain read-only and separately gated.

## Remaining Gates

Success at these repository gates does not authorize a socket-capable implementation. The configuration foundation makes a future proposal reviewable but does not enforce runtime controls. Socket-capable implementation, enforced privileged deployment controls, supply-chain evidence, credentials/certificates, exact eligible-subject Registry approval, named-target observation, live provider compatibility, non-regression, consumer integration, recurring operation, and EO activation remain separate Architecture Gatekeeper decisions.

## Related Documents

- [Privileged Access Security Review](Privileged_Access_Security_Review_and_Constrained_Docker_API_Proxy_Architecture_Validation.md)
- [Production Provider Adapter Architecture](Production_Provider_Adapter_Architecture.md)
- [Production Provider Adapter Contract](../specifications/Production_Provider_Adapter_Contract_Specification.md)
- [Repository Usage](Constrained_Docker_API_Proxy_Repository_Usage.md)
- [Implementation Package](../milestones/Milestone_14/Constrained_Docker_API_Proxy_Foundation_Implementation_Package.md)
- [Privileged Deployment Configuration Architecture](Privileged_Deployment_Configuration_Architecture.md)
- [Deployment Configuration Implementation Package](../milestones/Milestone_14/Privileged_Deployment_Configuration_Foundation_Implementation_Package.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded the repository-only deployment configuration layer and exact policy/version binding without socket, network, credential, deployment, target, observation, or activation authority. |
| 1.0 | Recorded the repository-only immutable contracts, category policy, synthetic authentication/authorization, deterministic validation and decisions, fixture mock, static safety boundary, and later blocked gates. |
