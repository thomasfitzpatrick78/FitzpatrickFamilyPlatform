# Container Metrics Modernization Specification

**Document Version:** 1.3

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** PLAT-14.1

---

## Purpose

Define the Milestone 14 requirements and approval boundaries for modernizing container metrics after the Milestone 13 Docker 29 and cAdvisor compatibility findings.

This specification does not authorize live deployment.

---

## Scope

- Restricted Docker API proxy.
- OpenTelemetry Collector.
- Docker Stats receiver.
- Prometheus integration.
- Container metrics dashboard.
- Safe cAdvisor transition.
- Docker daemon metrics evaluation.
- Grafana persistence validation.
- Final dashboard validation.
- Final reboot validation.

This telemetry-oriented scope is retained as subordinate future provider, security, observability-transport, live-validation, and presentation work. It is not the PLAT-14.1A core product definition.

---

## PLAT-14.1A Container Operational Health Alignment

PLAT-14.1A is Container Operational Health: deterministic, explainable, repository-owned health assessments for declared container-backed Platform services using Registry state, canonical evidence, reconciliation, and versioned policies.

The future core repository implementation is a provider-independent vertical slice containing contract and policy validation, Registry-linked identity resolution, fixture-only normalization proofs, reconciliation, health evaluation, deterministic JSON and Markdown, tests, and fixture-based EO contract integration. It remains blocked pending Architecture Gatekeeper review and publication of the aligned specification and separate implementation authorization.

The retained provider work is classified as follows:

| Existing Work | Future Classification |
|---------------|-----------------------|
| Restricted Docker API proxy | Privileged-access and security gate; not core health implementation. |
| OpenTelemetry Docker Stats Collector | Future provider-adapter implementation and live metric inventory. |
| Prometheus | Observability transport and metrics store. |
| Docker daemon metrics | Deferred provider candidate. |
| cAdvisor | Limited provider whose known identity limitation constrains evidence confidence. |
| Grafana provisioning and PromQL | Presentation and dashboard-integration scope. |
| Live metric inventory, persistence, reboot, and Pi-hole proof | Future controlled live-observation validation. |

No provider owns canonical subject identity, policy, reconciliation, confidence, or health. No retained provider artifact is deleted or treated as implementation authorization.

---

## Current-State Evidence Requirements

Before implementation, evidence must confirm:

- Active Docker version and runtime mode.
- Current cAdvisor metric availability and limitations.
- Prometheus target state.
- Grafana dashboard provisioning state.
- Pi-hole production health before any monitoring change.
- Registry state for active and planned services.
- Rollback service state for Raspberry Pi Pi-hole.

---

## Architecture Boundaries

- PLAT-14.0A Platform Operations Domain Architecture is published at `c8f9bc3446cb1d5c23bf32232203109a7ff067f8` and remains architecture-only with `Implemented: No`.
- The PLAT-14.1A specification and Registry Container Identity Foundation architecture/specification are published; repository implementation remains blocked pending separate Registry schema/migration and PLAT authorization.
- Infrastructure Registry remains authoritative for declared state and canonical Platform subject linkage.
- Docker API, Docker daemon metrics, cAdvisor, OpenTelemetry, Prometheus, and future telemetry sources are provider or transport implementations, not owners of canonical evidence or health semantics.
- Provider observations must be normalized into the approved Generic Operational Evidence Envelope and Container Evidence Profile before authoritative reconciliation or health evaluation.
- Provider adapters must return normalized evidence or structured findings and must not return authoritative health assessments.
- Grafana and future dashboards render governed outputs and must not independently calculate authoritative health or treat no-data as Healthy.
- Docker API access must pass through a restricted proxy.
- OTel Collector must consume only approved metric endpoints.
- Prometheus scrape configuration must be repository-managed.
- Grafana dashboards must not claim accurate container visibility until metric evidence proves it.
- Docker daemon metrics remain evaluation-only until separately approved.
- cAdvisor remains active until explicit retain, reduce, or retire criteria are satisfied.

---

## Security Controls

- No unauthenticated broad Docker socket exposure.
- No privileged container metrics component without Architecture Gatekeeper approval.
- No public internet exposure.
- No credentials committed to the repository.
- Network access limited to approved local monitoring paths.
- Denial proof required for restricted Docker API proxy behavior.

---

## Pi-hole Protection

- Pi-hole service health must be captured before and after each live gate.
- DNS resolution must not depend on metrics modernization.
- Router DNS and Pi-hole configuration changes are out of scope.
- Raspberry Pi rollback service must remain available until separately retired.

---

## Rollback

Rollback must restore:

- Prior Prometheus scrape configuration.
- Prior Grafana dashboard provisioning.
- Prior running metric containers or service definitions.
- No-impact Pi-hole service state.

Rollback evidence must be captured if used.

---

## Cutover Checkpoints

| Checkpoint | Required Evidence |
|------------|-------------------|
| Preflight | Current-state baseline, approvals, rollback readiness. |
| Proxy validation | Allowed and denied Docker API behavior. |
| OTel validation | Docker Stats receiver metrics visible without service regression. |
| Prometheus validation | Target up state and expected metric inventory. |
| Dashboard validation | Panels match validated metrics and avoid unsupported claims. |
| Persistence validation | Grafana state survives approved restart. |
| Reboot validation | Only after explicit human approval. |

---

## cAdvisor Decision Criteria

| Decision | Criteria |
|----------|----------|
| Retain | Host or non-container metrics remain useful and no conflict exists. |
| Reduce | Some panels or scrapes are obsolete but service remains useful during transition. |
| Retire | Replacement metrics satisfy required coverage, dashboards are migrated, rollback is approved, and no dependent evidence remains. |

---

## Acceptance Criteria

PLAT-14.1 is ready for implementation review when:

- PLAT-14.0A remains published and its lifecycle metadata is synchronized.
- The PLAT-14.1A Container Operational Health specification, Registry identity design, policies, reason codes, outputs, fixtures, and future gates are Architecture Gatekeeper approved and published.
- A separately authorized PLAT-14.1A repository implementation package selects the approved provider-independent vertical slice without deleting telemetry-provider work.
- Requirements, security controls, Pi-hole protections, rollback, cutover checkpoints, and validation are approved.
- cAdvisor retain, reduce, or retire criteria are documented.
- Docker daemon metrics are explicitly evaluated without implicit approval.
- No live infrastructure change is claimed by this specification.

---

## Related Documents

- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Container Operational Health Specification](Container_Operational_Health_Specification.md)
- [Docker 29 Container Metrics Compatibility Assessment](../architecture/Docker_29_Container_Metrics_Compatibility_Assessment.md)
- [Privileged Infrastructure Integration Standard](../governance/Privileged_Infrastructure_Integration_Standard.md)
- [Platform Health Dashboard Specification](Platform_Health_Dashboard_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.3 | Recorded PLAT-14.1A and Registry Container Identity Foundation publication without authorizing provider or runtime work. |
| 1.2 | Reclassified existing telemetry work as subordinate future provider, security, transport, live-validation, and presentation scope beneath PLAT-14.1A Container Operational Health. |
| 1.1 | Added PLAT-14.0A dependency and separated canonical Platform Operations contracts from provider and presentation implementation. |
| 1.0 | Initial PLAT-14.1 container metrics modernization specification. |
