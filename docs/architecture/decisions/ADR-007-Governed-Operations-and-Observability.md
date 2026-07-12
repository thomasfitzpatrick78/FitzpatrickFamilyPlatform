# ADR-007 - Governed Operations and Observability

**Status:** Approved

**Date Approved:** July 2026

**Category:** Infrastructure Architecture

**Milestone:** Milestone 13

**Baseline:** PLAT-13.6.2 Metrics Foundation live validation recorded

**Implemented:** Partially - Prometheus and Node Exporter active; cAdvisor scrape target active with Docker-container discovery degraded under Docker 29/containerd; Grafana deployed for validation with closeout blocked; alerts, backups, restore validation, and controlled updates remain planned.

---

## Context

The Beelink now hosts the production Pi-hole DNS and blocking service in Docker.

The Platform needs governed operational visibility before additional production services are added. PLAT-13.6.2 has implemented the initial Metrics Foundation. PLAT-13.6.3 prepares Grafana as a repository-provisioned dashboard layer without live deployment. Alerting, backup, restore validation, and update governance remain governed future work.

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

The PLAT-13.6.2 Metrics Foundation portion of the target deployment is implemented and validated. The PLAT-13.6.3 Grafana dashboard package is implementation-ready for Architecture Gatekeeper review. Live Grafana deployment, alerting, backup, restore validation, and controlled update implementation remain future work.

Grafana must be provisioned from repository-managed datasource and dashboard files. Prometheus remains the single governed metrics data source for dashboards; Grafana must not query Node Exporter or cAdvisor directly.

PLAT-13.6.3A implementation finding: Docker 29.6.1 with the containerd-backed image store (`io.containerd.snapshotter.v1`) is the governed Platform runtime baseline. cAdvisor `v0.49.1` is not accepted as sufficient Docker-container observability under that baseline because it remains scrapeable but does not reliably discover Docker containers with stable names or Compose labels. Legacy Docker storage migration, Docker downgrade, disabling the containerd image store, deleting Docker data, or recreating Pi-hole are rejected. Future container metrics must be repository-managed, version-pinned, LAN/internal-only, Prometheus-scraped, and evidence-validated before dashboards claim Docker-container resource visibility.

PLAT-13.6.3B implementation pattern: preserve Docker Engine 29.6.1, preserve Node Exporter, retain cAdvisor as active/degraded, and add an implementation-ready restricted Docker API proxy plus OpenTelemetry Collector Contrib Docker Stats receiver. The Collector exposes only an internal Prometheus-format endpoint, Prometheus remains the single metrics store and Grafana datasource, and Docker daemon Prometheus metrics remain deferred. The replacement is repository-prepared only until live proxy denial proof, OTel metric inventory, Pi-hole identity proof, persistence validation, and reboot validation pass.

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

Prometheus persistent data is stored under `/platform/data/monitoring/prometheus`. Grafana persistent data is planned under `/platform/data/monitoring/grafana` with UID/GID `472:472` and non-global-write permissions.

Configuration is represented in repository-managed templates or specifications before live deployment.

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
| 1.4 | Recorded PLAT-13.6.3B restricted Docker API proxy and OpenTelemetry Docker Stats implementation pattern. |
| 1.3 | Recorded PLAT-13.6.3A Docker 29/containerd cAdvisor compatibility finding and rejected Docker storage migration. |
| 1.2 | Added PLAT-13.6.3 repository-provisioned Grafana dashboard implementation decision without live deployment. |
| 1.1 | Recorded PLAT-13.6.2 Metrics Foundation implementation status while preserving remaining planned observability work. |
| 1.0 | Initial ADR selecting governed Prometheus operations and observability architecture. |
