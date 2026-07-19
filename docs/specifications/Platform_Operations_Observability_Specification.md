# Platform Operations and Observability Specification

**Document Version:** 1.8

**Status:** Planned

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6 - Platform Operations and Observability

---

## Purpose

This specification defines the governed target state for Platform operations and observability, records the verified PLAT-13.6.2 Metrics Foundation deployment, records the PLAT-13.6.3 Operations Dashboard package, records the PLAT-13.6.3A Docker 29/containerd container metrics compatibility correction, records the PLAT-13.6.3B repository-prepared Docker metrics replacement, and aligns the implementation to the technology-neutral Container Metrics capability.

It does not execute live Grafana deployment, backups, alerts, scripts, timers, restore validation, or controlled updates.

---

## Architecture Diagram

```text
Trusted Home Network
  |
  |-- Tom MacBook Admin Workstation
  |
  |-- ASUS Router / DHCP Reservation
  |     |
  |     |-- Beelink / beelink / 192.168.50.127
  |           |
  |           |-- Docker Engine
  |           |     |
  |           |     |-- Pi-hole container (active production)
  |           |     |-- Prometheus (active)
  |           |     |-- Grafana (validation incomplete)
  |           |     |-- cAdvisor (active)
  |           |     |-- Docker API proxy (planned)
  |           |     |-- OTel Docker Stats Collector (planned)
  |           |
  |           |-- Node Exporter (active)
  |           |-- Backup / restore / validation scripts (planned)
  |
  |-- Raspberry Pi Pi-hole rollback host / 192.168.50.67
```

---

## Present Production Baseline

| Area | Present State |
|------|---------------|
| Hostname | `beelink` |
| Operating system | Ubuntu Server 26.04 LTS |
| Architecture | x86_64 |
| Reserved IPv4 | `192.168.50.127` |
| MAC address | `78:55:36:09:D2:45` |
| Administration | SSH with Ed25519 key authentication |
| Docker Engine | Installed, enabled, active after reboot |
| Docker Compose plugin | Installed |
| Docker storage driver | `overlayfs` |
| Docker driver type | `io.containerd.snapshotter.v1` |
| cgroup driver/version | `systemd` / cgroup v2 |
| Platform root | `/platform` |
| Production Pi-hole container | `pihole` |
| Pi-hole Compose path | `/platform/compose/pihole` |
| Pi-hole persistent configuration | `/platform/data/pihole/etc-pihole` |
| Pi-hole admin port | TCP `8080` |
| Pi-hole DNS ports | TCP/UDP `53` on `192.168.50.127` |
| Rollback host | Raspberry Pi at `192.168.50.67`, powered on and unchanged |
| Metrics foundation | Prometheus, Node Exporter, and cAdvisor active and validated under PLAT-13.6.2 |

Proton VPN on the MacBook intentionally uses Proton DNS while connected. That operating mode is not a Pi-hole failure.

---

## Target Components

| Component | Responsibility | State |
|-----------|----------------|-------|
| Prometheus | Metrics collection, retention, target health | Active |
| Node Exporter | Beelink/Linux host metrics | Active |
| cAdvisor | Host/cgroup metrics; Docker-container discovery degraded under Docker 29/containerd | Active degraded |
| Grafana | Governed dashboards and future alert visibility | Deployed for validation; closeout incomplete |
| Docker API proxy | Restricted Docker API boundary for Docker Stats collection | Repository-prepared; not deployed |
| OTel Docker Stats Collector | Docker Stats receiver and internal Prometheus-format endpoint | Repository-prepared; not deployed |
| Pi-hole checks | DNS, admin, health, and customer-facing service validation | Planned |
| Backup scripts | Backup, checksum, report, and retention workflow | Planned |
| Restore validation | Isolated restore proof and reporting | Planned |
| Controlled update workflow | Version, digest, backup, deployment, observation, rollback | Planned |

---

## Container Metrics Capability Abstraction

Container Metrics is the governed capability. Docker is the current implementation context for Milestone 13.

Future implementations may include Podman, containerd, Kubernetes, Incus, or LXC when requirements, architecture, security boundaries, collectors, and live evidence support them.

Governed consumers, including Grafana and future customer-facing applications, consume Container Metrics through Prometheus rather than runtime-specific APIs. Runtime-specific collectors, proxies, receivers, and scrape jobs are replaceable implementation components.

EO-13.1 creates no live architecture change, no new runtime adapter service, and no deployment authorization.

---

## PLAT-14.0A Platform Operations Domain Boundary

PLAT-14.0A places the existing observability topology inside a broader provider-independent Platform Operations bounded context:

```text
Infrastructure Registry declared state
  -> provider observations from the approved observability topology
  -> normalized Platform Operational Evidence
  -> reconciliation
  -> deterministic Operational Health
  -> advisory Operational Intelligence and read-only presentation
```

ADR-007 remains authoritative for the Prometheus observability stack and the approved restricted proxy plus OpenTelemetry replacement pattern. PLAT-14.0A does not remove or redesign those components. It establishes that Docker, cAdvisor, OpenTelemetry, Prometheus, and Grafana are provider, transport, or presentation concerns and do not own Platform subject identity, normalized evidence semantics, confidence, reconciliation, or authoritative health.

PLAT-14.0A is published at `c8f9bc3446cb1d5c23bf32232203109a7ff067f8` and remains architecture-only. PLAT-14.1A is in Specification Alignment and its implementation remains blocked pending publication of the aligned specification and separate authorization. No provider adapter, configuration, dashboard, or live behavior is implemented by either specification package.

The approved future PLAT-14.1A direction is a repository-only core vertical slice with fixture adapters. The prepared restricted proxy, OpenTelemetry Collector, Prometheus, Docker daemon, cAdvisor, and Grafana artifacts remain subordinate provider, security, transport, live-validation, or presentation work and do not enter the core health contract.

---

## PLAT-13.6.2 Metrics Foundation Implementation Package

PLAT-13.6.2 prepared repository-managed implementation artifacts for the first metrics deployment.

Live execution has since completed and is recorded in [Metrics Foundation Implementation Evidence](../operations/Metrics_Foundation_Implementation_Evidence.md).

Approved components:

- Prometheus `prom/prometheus:v2.55.1`.
- Node Exporter `prom/node-exporter:v1.8.2`.
- cAdvisor `gcr.io/cadvisor/cadvisor:v0.49.1`.

Approved repository paths:

- `platform/compose/monitoring/compose.yaml`.
- `platform/compose/monitoring/.env.example`.
- `platform/compose/monitoring/prometheus/prometheus.yml`.
- `platform/compose/monitoring/README.md`.
- `docs/operations/Metrics_Foundation_Runbook.md`.
- `docs/operations/Metrics_Foundation_Evidence_Template.md`.

Approved live paths:

- `/platform/compose/monitoring`.
- `/platform/data/monitoring/prometheus`.
- `/platform/documentation/operations`.

Implementation decisions:

- Prometheus binds to `192.168.50.127:9090`.
- Node Exporter is exposed only on the `platform-monitoring` Docker network.
- cAdvisor is exposed only on the `platform-monitoring` Docker network.
- cAdvisor is not published on host TCP `8080`, which remains Pi-hole admin.
- Prometheus retention is `15d`.
- Prometheus runs as UID/GID `65534:65534`, and its data directory must use that ownership with non-global-write permissions.
- Docker socket is not mounted into Prometheus.
- cAdvisor uses read-only host metadata mounts, `privileged: false`, `cap_drop: ALL`, and `no-new-privileges:true`.
- Image digests were captured during live evidence after images were pulled.
- The runtime `.env` is created only on the Beelink and is not committed.
- Prometheus targets, host metrics, container metrics, persistence, reboot behavior, and Pi-hole non-regression are verified.
- PLAT-13.6.3A supersedes the container-metric completeness claim: the cAdvisor endpoint is active and scrapeable, but Docker-container discovery is degraded under Docker 29/containerd and must not be used for container-level dashboard claims until corrected.

Explicitly out of scope for PLAT-13.6.2:

- Grafana.
- Alertmanager and notification delivery.
- Backup automation.
- Restore execution.
- Watchtower or unattended updates.
- Pi-hole configuration changes.
- DNS or router changes.
- Raspberry Pi changes.
- Internet exposure.
- Remote monitoring outside the trusted home network.
- Milestone closeout, release tagging, or deployment claims beyond the metrics foundation.

---

## PLAT-13.6.3 Operations Dashboard Implementation Package

PLAT-13.6.3 prepared the repository-managed Grafana dashboard layer. Live validation has begun, but PLAT-13.6.3 closeout is blocked by the PLAT-13.6.3A Docker 29/containerd container metrics compatibility finding.

Approved components:

- Grafana `grafana/grafana:13.1.0`.
- Prometheus datasource provisioned as `Prometheus`.
- Repository-managed dashboard provisioning.
- Four purpose-built dashboards aligned to current Metrics Foundation data.

Approved repository paths:

- `platform/compose/monitoring/compose.yaml`.
- `platform/compose/monitoring/.env.example`.
- `platform/compose/monitoring/grafana/provisioning/datasources/prometheus.yml`.
- `platform/compose/monitoring/grafana/provisioning/dashboards/dashboards.yml`.
- `platform/compose/monitoring/grafana/dashboards/platform-host.json`.
- `platform/compose/monitoring/grafana/dashboards/docker-containers.json`.
- `platform/compose/monitoring/grafana/dashboards/pihole-operations.json`.
- `platform/compose/monitoring/grafana/dashboards/metrics-foundation-health.json`.
- `docs/specifications/Platform_Operations_Dashboard.md`.
- `docs/operations/Operations_Dashboard_Runbook.md`.
- `docs/operations/Operations_Dashboard_Evidence_Template.md`.

Approved implementation decisions:

- Grafana binds to `192.168.50.127:3000`.
- Grafana joins the existing `platform-monitoring` network.
- Grafana reads Prometheus at `http://prometheus:9090`.
- Grafana does not query Node Exporter or cAdvisor directly.
- Grafana data persists at `/platform/data/monitoring/grafana`.
- Grafana runs as UID/GID `472:472`.
- Grafana admin password is supplied only through the Beelink-local `.env` file.
- `.env.example` contains placeholders only.
- Grafana dashboard refresh interval is 30 seconds.
- Grafana digest is captured only after the governed live pull and final closeout evidence remains pending.

Dashboard inventory:

- Platform Host Dashboard.
- Docker and Container Dashboard.
- Pi-hole Operations Dashboard.
- Metrics Foundation Health Dashboard.

Explicitly out of scope for PLAT-13.6.3 closeout before PLAT-13.6.3A review:

- Claiming Grafana persistence or reboot validation complete.
- Claiming Docker-container dashboard accuracy complete.
- Alert rules, notification delivery, backups, restore validation, or automated updates.
- Pi-hole, Prometheus, Node Exporter, cAdvisor, Docker, router, ASUS router, Raspberry Pi, or DNS configuration changes.
- Pi-hole query counts, blocked percentages, domain rankings, client analytics, or other application metrics that are not exported to Prometheus.
- Milestone closeout, release tagging, or production claims for Grafana.

---

## PLAT-13.6.3A Docker 29 Container Metrics Compatibility Correction

Live dashboard validation found that cAdvisor remains scrapeable but does not provide reliable Docker-container identity under Docker Engine `29.6.1` with driver type `io.containerd.snapshotter.v1` and cgroup v2.

Governed finding:

- Docker 29 and the containerd-backed image store remain the approved Platform baseline.
- cAdvisor target up is not equivalent to complete Docker-container observability.
- Docker-container resource dashboards must not count host/systemd cgroups as Docker containers.
- Pi-hole container resource metrics are unavailable pending a compatible container metrics source.
- Persistence and reboot validation for PLAT-13.6.3 remain paused until dashboard accuracy is corrected and reviewed.

Rejected changes:

- Docker storage backend migration.
- Docker downgrade.
- Disabling the containerd image store.
- Legacy overlay2 migration.
- Docker data deletion.
- Pi-hole recreation or modification.

Candidate direction:

- Preserve cAdvisor for limited host/cgroup scrape visibility.
- Add a planned Docker 29/containerd-compatible container metrics source after Architecture Gatekeeper approval and live proof.
- Keep Prometheus as the central governed metrics data source.

## PLAT-13.6.3B Docker Container Metrics Replacement Preparation

PLAT-13.6.3B prepares the approved A3 replacement architecture without live deployment:

- Docker Engine 29.6.1 and the containerd-backed image store remain the governed baseline.
- Node Exporter remains the authoritative host metrics source.
- cAdvisor remains active/degraded and non-authoritative for named Docker-container metrics.
- `tecnativa/docker-socket-proxy:0.4.2` is prepared as the only service with Docker socket access.
- `otel/opentelemetry-collector-contrib:0.156.0` is prepared with the Docker Stats receiver.
- OTel connects to `http://docker-api-proxy:2375` and has no Docker or containerd socket mount.
- OTel exposes an internal Prometheus-format endpoint on `otel-docker-stats:9464`.
- Prometheus remains the single metrics store and Grafana datasource.
- Docker daemon Prometheus metrics remain deferred and disabled.

Required live proof includes proxy denial behavior, emitted metric names, metadata inventory, Pi-hole identity, CPU, memory, network, block I/O, uptime/state where available, sensitive-data exclusion, persistence, reboot behavior, and Pi-hole non-regression.

---

## Target Ports

| Component | Port | Exposure |
|-----------|------|----------|
| Pi-hole DNS | TCP/UDP 53 | Home network production DNS |
| Pi-hole admin | TCP 8080 | Trusted home network only |
| Prometheus | TCP 9090 | Trusted home network only |
| Grafana | TCP 3000 | Trusted home network only; validation endpoint `192.168.50.127:3000` |
| Node Exporter | TCP 9100 | Prometheus internal Docker network only for PLAT-13.6.2 |
| cAdvisor | TCP 8080 internal only | Must avoid Pi-hole admin conflict; no host-published port for PLAT-13.6.2 |
| Docker API proxy | TCP 2375 internal only | Restricted Docker API proxy; no host-published port |
| OTel Docker Stats | TCP 9464 internal only | Prometheus scrape endpoint; no host-published port |

No monitoring interface may be exposed to the Internet.

---

## Target Persistent Paths

These paths describe target and active state. PLAT-13.6.2 has created the monitoring Compose and Prometheus data paths on the Beelink. Grafana, backup, restore, validation, and update paths remain planned.

```text
/platform/compose/monitoring/
  compose.yaml
  .env
  README.md
  prometheus/
    prometheus.yml
    rules/
  grafana/
    provisioning/
      datasources/
      dashboards/
    dashboards/

/platform/data/monitoring/
  prometheus/
  grafana/

/platform/backups/
  pihole/
  monitoring/

/platform/scripts/
  backup/
  restore/
  validation/
  updates/

/platform/documentation/
  operations/
  recovery/
```

`.env` files containing secrets must not be committed. Repository examples must use placeholders only.

---

## Data Flow

1. Node Exporter exposes Beelink host metrics.
2. cAdvisor exposes Docker and container metrics.
3. Pi-hole service checks validate DNS response and container health.
4. Prometheus scrapes metrics and service targets.
5. Prometheus evaluates alert rules.
6. Grafana reads Prometheus through a provisioned data source after PLAT-13.6.3 live deployment is approved and executed.
7. Backup, restore, and update workflows produce evidence reports for review.

---

## Metric Retention

Initial Prometheus retention target:

- 15 days of local metrics retention.
- Retention may be increased only after disk impact is reviewed.
- Metrics retention is not a substitute for backup.

---

## Dashboard Provisioning

Grafana dashboards should be repository-provisioned where practical.

Initial dashboards must cover:

- Beelink host health.
- Docker service health.
- Container health and restarts.
- Pi-hole DNS availability.
- Pi-hole admin availability.
- Backup status.
- Restore validation status.
- Monitoring stack health.

Manual-only dashboard configuration should be avoided unless documented as a temporary exception.

---

## Alert Lifecycle

Each alert must define:

- Severity.
- Trigger condition.
- Duration.
- Recovery condition.
- Owner.
- First-response action.
- Escalation behavior.
- Expected evidence.
- Test method.

Initial alert requirements are documented in [Incident Response Runbooks](../operations/Incident_Response_Runbooks.md).

At least one safe alert must be deliberately fired and observed returning to normal in the future implementation milestone.

---

## Backup and Recovery

Backup scope, exclusions, integrity verification, restore validation, and reporting are governed by [Backup and Restore Operations Specification](../architecture/Backup_Restore_Operations_Specification.md).

A backup is not proven until restore validation succeeds.

---

## Update Lifecycle

Production container updates are governed by [Controlled Container Update Specification](../architecture/Controlled_Container_Update_Specification.md).

Unattended Watchtower-style production updates are prohibited in this milestone.

---

## Access Restrictions and Least Privilege

- Monitoring interfaces stay on the trusted home network.
- Future remote monitoring requires a separate approved architecture.
- Grafana credentials must use environment variables or an approved secret mechanism.
- Pi-hole passwords must not appear in repository content.
- Docker socket access must be minimized.
- Exporters receive only required mounts and capabilities.
- Docker group access is privileged and limited to trusted administrators.

---

## Validation Gates

Before live implementation:

1. Registry records represent present state and planned capabilities.
2. DHCP reservation is verified for the production host.
3. Backup and rollback expectations are documented.
4. Monitoring ports do not conflict with Pi-hole admin port.
5. No secrets are committed.
6. Repository validation passes.
7. Governance validation passes.
8. Registry validation passes.

---

## Rollback

Monitoring rollback must not disturb production Pi-hole.

If monitoring deployment fails in a future workstream, stop monitoring components, preserve Pi-hole, and keep Raspberry Pi rollback available.

---

## Definition of Done

PLAT-13.6 planning baseline is complete when:

- ADR-007 records the approved architecture.
- Service lifecycle and cutover checklist exist.
- Present Beelink, Docker, Pi-hole, and Raspberry Pi rollback facts are recorded.
- Prometheus, Node Exporter, and cAdvisor have governed repository artifacts and live PLAT-13.6.2 evidence.
- Grafana, alerts, backups, restore validation, and controlled updates remain planned but not deployed.
- Tests and EAP validations pass.
- No live infrastructure changes are performed.
- No secrets are committed.

PLAT-13.6.2 Metrics Foundation implementation readiness is complete when:

- The monitoring Compose template is repository-managed.
- Prometheus scrape configuration is repository-managed.
- Registry records preserve planned lifecycle while documenting approved implementation details.
- The live runbook includes preflight, deployment, validation, reboot, rollback, and stop gates.
- Tests verify exposure, image tag, persistence, and scope guardrails.
- No live execution results are claimed by repository artifacts.

PLAT-13.6.2 operational closeout is complete when:

- Prometheus, Node Exporter, and cAdvisor are represented as active registry services.
- Versions, image IDs, and repo digests are recorded.
- Prometheus target validation, persistence validation, reboot validation, and Pi-hole non-regression evidence is governed.
- Later PLAT-13.6 work packages remain planned.
- Tests and EAP validations pass.

---

## Related Documents

- [Platform Operations Dashboard](Platform_Operations_Dashboard.md)
- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Container Operational Health Specification](Container_Operational_Health_Specification.md)
- [Docker 29 Container Metrics Compatibility Assessment](../architecture/Docker_29_Container_Metrics_Compatibility_Assessment.md)
- [Privileged Infrastructure Integration Standard](../governance/Privileged_Infrastructure_Integration_Standard.md)
- [Docker Container Metrics Replacement Runbook](../operations/Docker_Container_Metrics_Replacement_Runbook.md)
- [ADR-007 - Governed Operations and Observability](../architecture/decisions/ADR-007-Governed-Operations-and-Observability.md)
- [Platform Service Lifecycle](../governance/Service_Lifecycle.md)
- [Production Service Cutover Checklist](../governance/Production_Service_Cutover_Checklist.md)
- [Pi-hole Service Objectives](../operations/Pi-hole_Service_Objectives.md)
- [Incident Response Runbooks](../operations/Incident_Response_Runbooks.md)
- [Metrics Foundation Runbook](../operations/Metrics_Foundation_Runbook.md)
- [Metrics Foundation Evidence Template](../operations/Metrics_Foundation_Evidence_Template.md)
- [Metrics Foundation Implementation Evidence](../operations/Metrics_Foundation_Implementation_Evidence.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.8 | Recorded PLAT-14.0A publication and PLAT-14.1A specification alignment while retaining provider topology as subordinate future scope. |
| 1.7 | Added the PLAT-14.0A Platform Operations domain boundary above the existing provider and observability topology. |
| 1.6 | Added EO-13.1 technology-neutral Container Metrics capability abstraction. |
| 1.5 | Added PLAT-13.6.3B restricted Docker API proxy and OTel Docker Stats preparation. |
| 1.4 | Recorded PLAT-13.6.3A Docker 29/containerd container metrics compatibility correction. |
| 1.3 | Added PLAT-13.6.3 Operations Dashboard implementation-ready package. |
| 1.2 | Recorded PLAT-13.6.2 live Metrics Foundation validation and active service state. |
| 1.1 | Added PLAT-13.6.2 Metrics Foundation implementation package, scope boundaries, and readiness criteria. |
| 1.0 | Initial PLAT-13.6 operations and observability specification. |
