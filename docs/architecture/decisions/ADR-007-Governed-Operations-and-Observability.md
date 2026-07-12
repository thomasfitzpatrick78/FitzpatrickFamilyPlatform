# ADR-007 - Governed Operations and Observability

**Status:** Approved

**Date Approved:** July 2026

**Category:** Infrastructure Architecture

**Milestone:** Milestone 13

**Baseline:** Pending

**Implemented:** No

---

## Context

The Beelink now hosts the production Pi-hole DNS and blocking service in Docker.

The Platform needs governed operational visibility before additional production services are added. The repository must define monitoring, alerting, backup, restore validation, and update governance without deploying those capabilities in this repository-only workstream.

---

## Decision

Select Option A: a governed Prometheus observability stack.

The target architecture uses:

- Prometheus for metrics collection and retention.
- Node Exporter for Beelink/Linux host metrics.
- cAdvisor for Docker and container metrics.
- Grafana for governed dashboards and alerting.
- Pi-hole availability and production-service checks.
- Repository-managed provisioning wherever practical.

Monitoring interfaces must remain restricted to the trusted home network. Internet exposure is not approved.

---

## Alternatives Considered

| Option | Summary | Commercial Architecture Alignment | Maintainability | Quality and Reduced Rework |
|--------|---------|-----------------------------------|-----------------|----------------------------|
| A | Governed Prometheus stack | High | High | High |
| B | Lightweight monitoring stack | Medium | High | Medium |
| C | Native scripts/systemd-only monitoring | Low | Medium | Medium |

Option A was selected because it gives the Platform a reusable operating model that can grow from Pi-hole into Home Assistant, MQTT, Ollama, FFFA, monitoring, and future services.

---

## Selected Architecture

Prometheus scrapes host, Docker, container, and service targets. Grafana reads Prometheus as a provisioned data source and presents governed dashboards. Alert rules are defined in repository-managed configuration where practical. Backup and update workflows produce evidence that can be reviewed through the same operational model.

Target deployment remains future work and is not implemented by this ADR.

---

## Network and Security Boundary

- Monitoring interfaces are limited to the trusted home network.
- No monitoring interface is exposed to the Internet.
- Future remote monitoring requires a separately approved secure-access architecture.
- Grafana credentials must use environment variables or another approved secret mechanism.
- `.env` files containing secrets must not be committed.
- Pi-hole passwords must not appear in repository content.
- Docker socket access must be minimized.
- cAdvisor and exporters receive only required mounts and capabilities.
- Docker group membership remains privileged and limited to trusted administrators.

---

## Persistence Model

Prometheus and Grafana persistent data will be stored under governed Platform paths such as `/platform/data/monitoring/`.

Configuration will be represented in repository-managed templates or specifications before live deployment.

---

## Alerting Model

Initial alerts will cover host availability, Pi-hole DNS availability, Pi-hole container health, repeated restarts, disk pressure, memory pressure, Prometheus target availability, backup failure, overdue backups, restore-validation failure, and monitoring stack availability.

At least one safe alert must be deliberately fired and observed returning to normal during the future implementation milestone.

---

## Backup and Update Relationship

Backups are a prerequisite for controlled production updates.

Container updates must use governed image version and digest policy. Unattended production container updates are prohibited in this milestone.

---

## Operational Ownership

The Family Platform owner is accountable for operational decisions. Tom's MacBook remains the administrative workstation unless a later approved access model changes that boundary.

---

## Consequences

### Positive

- Establishes reusable observability for the Platform.
- Improves Pi-hole reliability, recoverability, and operational visibility.
- Creates a standard for future services.
- Aligns monitoring, backup, restore, alerting, and update evidence.

### Tradeoffs

- Adds operating complexity.
- Requires care around Docker socket and credential handling.
- Requires disciplined repository-managed provisioning to avoid undocumented manual-only configuration.

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Monitoring interfaces exposed too broadly | Keep access on trusted home network only. |
| Secrets committed accidentally | Use placeholders and environment variables only. |
| Docker socket overexposure | Minimize mounts and document privileged access. |
| Alert fatigue | Start with a small reviewed alert set. |
| Backup confidence overstated | Do not call a backup proven until restore validation succeeds. |

---

## Rollback Approach

If monitoring deployment causes instability in a future implementation milestone, stop the monitoring stack, preserve Pi-hole, and remove only monitoring-related containers and bindings. Pi-hole and Raspberry Pi rollback remain independent of monitoring.

---

## Future Evolution

The same observability architecture should support Home Assistant, MQTT, Ollama, FFFA, and future services after each service meets lifecycle, backup, alerting, and registry requirements.

---

## Related Documents

- [Architecture Decision Log](../Architecture_Decision_Log.md)
- [PLAT-13.6 Operations and Observability Specification](../../specifications/Platform_Operations_Observability_Specification.md)
- [Platform Service Lifecycle](../../governance/Service_Lifecycle.md)
- [Production Service Cutover Checklist](../../governance/Production_Service_Cutover_Checklist.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial ADR selecting governed Prometheus operations and observability architecture. |
