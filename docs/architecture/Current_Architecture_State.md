# Current Architecture State

**Document Version:** 1.26

**Status:** Active

**Milestone:** Milestone 12

---

## Summary

The Platform repository contains governance, product, architecture, standards, validation automation, reports, milestone planning, and registry records for the active Beelink-hosted Pi-hole production service, the active PLAT-13.6.2 Metrics Foundation, and the PLAT-13.6.3A Operations Dashboard correction package.

Milestone 12 selected the Registry Driven Infrastructure Foundation architecture. Milestone 13 extends that foundation toward governed operations and observability. Milestone 14 published PLAT-14.0A, the PLAT-14.1A specification, the Registry Container Identity Foundation, the Architecture Gatekeeper-accepted PLAT-14.1A Option B fixture-only repository vertical slice, and migration model v2. Exact historical plan `sha256:5addac8821f1a177792240b04c4727e1cc21144c75ab140a1fc8beb93490549f` executed for five approved `not_applicable` subjects with validated rollback and completion evidence. Current plan `sha256:78b3ddcab944e35a5c70bbe991971ab0c939c7c17f7860651a010cecfc24598a` contains 0 apply, 16 review-required, and 23 no-change candidates. Production Provider Adapter Architecture, security design, repository provider foundation, formal security review, transport-incapable proxy foundation, repository-only deployment configuration foundation, the purpose-built privileged-proxy implementation architecture/security acceptance package, and the Architecture Gatekeeper-approved and accepted transport-free standard-library Go source foundation are published. Socket-capable implementation, enforced privileged deployment, credentials/certificates, named-target observation, consumers, activation, and live work remain separately blocked.

---

## Established Architecture

- Repository-managed governance.
- Repository-local ADR framework.
- Product scope excluding finance.
- Independent engineering automation foundation.
- Portfolio integration without shared implementation code.
- Registry Driven Infrastructure Foundation selected for Infrastructure Registry v1.0.
- Git-native YAML or JSON registry records planned as authoritative infrastructure knowledge.
- Validation-first design selected before monitoring, dashboards, or automation.
- Governed operations and observability architecture selected in ADR-007.
- Platform Operations bounded-context direction is published in ADR-009 through ADR-011, with declared state, normalized evidence, reconciliation, deterministic health, and advisory intelligence kept separate; implementation remains absent.
- The Registry Container Identity Foundation published baseline and model v2 remain in force. Five exact `not_applicable` patches are executed and completion-validated; schema `1.1` validates all 39 records, the other 34 are unchanged, and none of the five is container-health eligible.
- The published PLAT-14.1A repository capability implements immutable contracts, strict policy/evidence parsing, synthetic Registry identity, fixture-only normalization, reconciliation, health assessment, deterministic outputs, read-only CLI, and fixture-only EO contract reuse. It remains unactivated and incapable of evaluating an authoritative current Registry subject.
- Migration of the 16 review-required subjects, live production provider access, privileged proxy implementation/deployment, named-target observation, dashboards, activation, and live infrastructure remain blocked.
- Formal security review validates a same-host dedicated constrained Docker API proxy as the future primary implementation target, subject to enforceable service identity, default-deny endpoint policy, non-streaming first-slice behavior, supply-chain proof, and separate implementation/deployment/observation gates. No version, configuration, target, deployment, credential, or access is approved.
- The provider adapter repository foundation implements immutable v1 contracts, strict validation, an abstract lifecycle, synthetic fixtures, deterministic mock clients, canonical normalization, failures, and bounded CLI commands. It has no network, socket, Docker, credential, live-provider, reconciliation, health, or activation path.
- The constrained proxy repository foundation implements immutable request/response/decision/security contracts, a versioned default-deny category policy, conceptual identity and authorization, exact synthetic-target binding, bounded responses, deterministic failures/audit, governed fixtures, and Platform EAP commands. It has no endpoint URL, socket, network, Docker client, credential, deployment, named-target, live observation, or activation path.
- The deployment configuration repository foundation implements immutable descriptive profiles, exact synthetic identity, runtime-security/resource/audit prerequisites, proxy/provider/policy compatibility, canonical bundle digests, strict fixtures, and read-only Platform EAP commands. It does not enforce controls or contain Docker/API/socket/network/listener, credential/certificate, deployment, named-target, observation, or activation capability.
- The approved and published privileged-proxy implementation architecture selects a separate purpose-built minimal Go service, a non-Docker authenticated Unix-socket protocol, a closed fixed Docker-request dispatcher without a Docker SDK, exact digest-bound authorization, durable fail-closed replay state, runtime-control proof, supply-chain gates, a formal threat model, and separate implementation/deployment acceptance checklists. ADR-012 is approved as architecture only and `Implemented: No`; the package contains no executable or privileged capability.
- The published transport-free source implements strict canonical protocol objects, abstract peer context, synthetic-key Ed25519 authorization with exact selector and digest bindings, memory and ordinary-file test replay journals, the published policy adapter, five typed synthetic operations, projection, logical limits, canonical audit, fail-closed core orchestration, Go AST safety, tests, and Platform EAP inspection. It contains no `main` package, listener, socket, networking, Docker/API/SDK/CLI, shell, environment-derived configuration, production credential, binary, image, deployment, Registry mutation, observation, consumer, or activation path. ADR-012 remains `Implemented: No` because repository ADR state is Boolean and the socket-capable architecture is incomplete.
- Pi-hole remains unresolved for privileged eligibility and named-target observation and remains unmigrated in the current Registry migration state; architecture publication changes neither condition.

---

## Runtime State

Pi-hole is active in Docker on Beelink at `192.168.50.127`.

Prometheus is active at `192.168.50.127:9090` with 15-day local retention at `/platform/data/monitoring/prometheus`.

Node Exporter and cAdvisor are active on the internal `platform-monitoring` Docker network only.

PLAT-13.6.3A records a Docker 29/containerd compatibility defect: cAdvisor is scrapeable, but Docker-container discovery is degraded because friendly Docker container names and Compose labels are not reliable under the current Docker 29.6.1 `io.containerd.snapshotter.v1` image-store model.

PLAT-13.6.3B prepares the approved replacement architecture in the repository: a restricted Docker API proxy, an OpenTelemetry Collector Contrib Docker Stats receiver, and an internal Prometheus scrape target. These services are not deployed, active, healthy, or validated. Exact OTel metric names, Pi-hole identity, proxy denial proof, persistence, and reboot behavior require live evidence before dashboard closeout.

Grafana has been deployed for validation, but PLAT-13.6.3 closeout remains incomplete. Live dashboard validation is paused pending Architecture Gatekeeper review of the container metrics correction.

Alerts, backup automation, restore validation, and controlled updates remain planned and are not deployed.

---

## Related Documents

- [Architecture Decision Log](Architecture_Decision_Log.md)
- [Architecture Backlog](Architecture_Backlog.md)
- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)
- [ADR-006 - Registry Driven Infrastructure Foundation](decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md)
- [ADR-007 - Governed Operations and Observability](decisions/ADR-007-Governed-Operations-and-Observability.md)
- [Platform Operations Domain Architecture](Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](../specifications/Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Container Operational Health Specification](../specifications/Container_Operational_Health_Specification.md)
- [Registry Container Identity Foundation Architecture](Registry_Container_Identity_Foundation_Architecture.md)
- [Registry Container Identity Foundation Specification](../specifications/Registry_Container_Identity_Foundation_Specification.md)
- [ADR-009 - Evidence Before Operational Health](decisions/ADR-009-Evidence-Before-Operational-Health.md)
- [ADR-010 - Declared Observed and Reconciled State](decisions/ADR-010-Declared-Observed-and-Reconciled-State.md)
- [ADR-011 - Generic Operational Evidence Envelope and Versioned Profiles](decisions/ADR-011-Generic-Operational-Evidence-Envelope-and-Versioned-Profiles.md)
- [Docker 29 Container Metrics Compatibility Assessment](Docker_29_Container_Metrics_Compatibility_Assessment.md)
- [Privileged Infrastructure Integration Standard](../governance/Privileged_Infrastructure_Integration_Standard.md)
- [Docker Container Metrics Replacement Runbook](../operations/Docker_Container_Metrics_Replacement_Runbook.md)
- [Production Provider Adapter Architecture](Production_Provider_Adapter_Architecture.md)
- [Production Provider Adapter Contract Specification](../specifications/Production_Provider_Adapter_Contract_Specification.md)
- [Privileged-Access Security Design and Threat Model](Production_Provider_Privileged_Access_Security_Design.md)
- [Provider Adapter Repository Usage](Production_Provider_Adapter_Repository_Usage.md)
- [Provider Adapter Foundation Implementation Package](../milestones/Milestone_14/Production_Provider_Adapter_Foundation_Implementation_Package.md)
- [Formal Privileged Access Security Review](Privileged_Access_Security_Review_and_Constrained_Docker_API_Proxy_Architecture_Validation.md)
- [Constrained Proxy Repository Architecture](Constrained_Docker_API_Proxy_Architecture.md)
- [Constrained Proxy Repository Usage](Constrained_Docker_API_Proxy_Repository_Usage.md)
- [Privileged Proxy Implementation Architecture](Privileged_Proxy_Implementation_Architecture.md)
- [Privileged Proxy Architecture Review Package](../milestones/Milestone_14/Privileged_Proxy_Implementation_Architecture_Review_Package.md)
- [ADR-012 - Purpose-Built Constrained Privileged Proxy](decisions/ADR-012-Purpose-Built-Constrained-Privileged-Proxy.md)
- [Privileged Proxy Source Architecture Conformance](Privileged_Proxy_Source_Implementation_Architecture_Conformance.md)
- [Privileged Proxy Source Implementation Package](../milestones/Milestone_14/Privileged_Proxy_Source_Implementation_Package.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.26 | Recorded Architecture Gatekeeper approval, acceptance, and publication of the transport-free source while preserving all socket, artifact, deployment, and operational gates. |
| 1.25 | Recorded the completed uncommitted transport-free privileged-proxy source review tree and retained the Architecture Gatekeeper publication hold plus every socket, artifact, deployment, and operational gate. |
| 1.24 | Recorded Architecture Gatekeeper approval and publication of the privileged-proxy implementation architecture/security acceptance package, with no implementation or live gate opened. |
| 1.23 | Recorded publication of the repository-only privileged deployment configuration foundation while preserving all socket-capable implementation, enforcement, credential, target, observation, consumer, activation, and live gates. |
| 1.22 | Recorded publication of the repository-only constrained proxy contracts, policy, fixtures, deterministic mock, safety validation, and CLI while retaining all privileged, target, observation, consumer, activation, and live gates. |
| 1.21 | Recorded formal security validation of the constrained proxy as a future implementation target while preserving separate repository implementation, privileged deployment, named-target, consumer, activation, and live gates. |
| 1.20 | Recorded publication of the repository-only provider adapter foundation while preserving live-provider, privileged-access, named-target, consumer, activation, and infrastructure gates. |
| 1.19 | Recorded publication of the accepted production provider architecture/security direction while preserving provider implementation, privileged access, observation, consumer, activation, and live gates. |
| 1.18 | Recorded exact five-record migration, rollback/completion evidence, post-migration current-plan semantics, and unchanged provider, activation, and live state. |
| 1.17 | Recorded deterministic exact-plan approval binding as unpublished and unexecuted with all Registry, provider, activation, and live state unchanged. |
| 1.16 | Recorded exact-plan approval-in-principle and creation of unpublished, unbound approval evidence with all Registry, provider, activation, and live state unchanged. |
| 1.15 | Recorded the complete unpublished Registry migration model-v2 idempotency correction while preserving all approval, record, provider, dashboard/API, activation, and live-work gates. |
| 1.14 | Recorded Architecture Gatekeeper acceptance and publication of the PLAT-14.1A fixture-only repository slice while preserving Registry, provider, dashboard/API, activation, and live-work gates. |
| 1.13 | Recorded the complete unpublished PLAT-14.1A fixture-only repository vertical slice while preserving Registry, provider, dashboard, activation, and live-work gates. |
| 1.12 | Recorded Architecture Gatekeeper acceptance and publication of the Registry identity implementation with all records and later gates unchanged. |
| 1.11 | Recorded completed pre-publication exact-plan approval-artifact hardening with all records and later gates unchanged. |
| 1.10 | Recorded complete unpublished Registry identity schema/validation/migration framework with all 39 records unchanged and PLAT blocked. |
| 1.9 | Recorded PLAT-14.1A and Registry Container Identity Foundation architecture/specification publication without implementation. |
| 1.8 | Recorded PLAT-14.0A publication and PLAT-14.1A Container Operational Health specification alignment with implementation blocked. |
| 1.7 | Added PLAT-14.0A Platform Operations domain architecture and the blocked PLAT-14.1A dependency state. |
| 1.6 | Recorded PLAT-13.6.3B repository-prepared Docker API proxy and OpenTelemetry Docker Stats replacement architecture. |
| 1.5 | Recorded PLAT-13.6.3A Docker 29/containerd cAdvisor compatibility defect and paused dashboard validation. |
| 1.4 | Recorded PLAT-13.6.3 Operations Dashboard repository package as implementation-ready and not deployed. |
| 1.3 | Recorded active PLAT-13.6.2 Metrics Foundation state and remaining planned operations capabilities. |
| 1.2 | Updated current architecture state for active Beelink-hosted Pi-hole and ADR-007 governed observability planning. |
| 1.1 | Added Milestone 12 Registry Driven Infrastructure Foundation architecture state. |
| 1.0 | Initial current architecture state. |
