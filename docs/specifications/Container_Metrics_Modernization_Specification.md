# Container Metrics Modernization Specification

**Document Version:** 1.0

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

- Requirements, security controls, Pi-hole protections, rollback, cutover checkpoints, and validation are approved.
- cAdvisor retain, reduce, or retire criteria are documented.
- Docker daemon metrics are explicitly evaluated without implicit approval.
- No live infrastructure change is claimed by this specification.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial PLAT-14.1 container metrics modernization specification. |
