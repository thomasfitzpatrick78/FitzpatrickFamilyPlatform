# Platform Operations and Observability Specification

**Document Version:** 1.3

**Status:** Planned

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6 - Platform Operations and Observability

---

## Purpose

This specification defines the governed target state for Platform operations and observability, records the verified PLAT-13.6.2 Metrics Foundation deployment, and records the repository-prepared PLAT-13.6.3 Operations Dashboard package.

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
  |           |     |-- Grafana (planned)
  |           |     |-- cAdvisor (active)
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
| cAdvisor | Docker and container metrics | Active |
| Grafana | Governed dashboards and future alert visibility | Implementation-ready |
| Pi-hole checks | DNS, admin, health, and customer-facing service validation | Planned |
| Backup scripts | Backup, checksum, report, and retention workflow | Planned |
| Restore validation | Isolated restore proof and reporting | Planned |
| Controlled update workflow | Version, digest, backup, deployment, observation, rollback | Planned |

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

PLAT-13.6.3 prepares the repository-managed Grafana dashboard layer without executing live deployment.

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
- Grafana digest is captured only after the governed live pull.

Dashboard inventory:

- Platform Host Dashboard.
- Docker and Container Dashboard.
- Pi-hole Operations Dashboard.
- Metrics Foundation Health Dashboard.

Explicitly out of scope for PLAT-13.6.3 repository preparation:

- Live Grafana deployment before Architecture Gatekeeper approval.
- Alert rules, notification delivery, backups, restore validation, or automated updates.
- Pi-hole, Prometheus, Node Exporter, cAdvisor, Docker, router, ASUS router, Raspberry Pi, or DNS configuration changes.
- Pi-hole query counts, blocked percentages, domain rankings, client analytics, or other application metrics that are not exported to Prometheus.
- Milestone closeout, release tagging, or production claims for Grafana.

---

## Target Ports

| Component | Port | Exposure |
|-----------|------|----------|
| Pi-hole DNS | TCP/UDP 53 | Home network production DNS |
| Pi-hole admin | TCP 8080 | Trusted home network only |
| Prometheus | TCP 9090 | Trusted home network only |
| Grafana | TCP 3000 | Trusted home network only when implemented; planned binding `192.168.50.127:3000` |
| Node Exporter | TCP 9100 | Prometheus internal Docker network only for PLAT-13.6.2 |
| cAdvisor | TCP 8080 internal only | Must avoid Pi-hole admin conflict; no host-published port for PLAT-13.6.2 |

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
| 1.3 | Added PLAT-13.6.3 Operations Dashboard implementation-ready package. |
| 1.2 | Recorded PLAT-13.6.2 live Metrics Foundation validation and active service state. |
| 1.1 | Added PLAT-13.6.2 Metrics Foundation implementation package, scope boundaries, and readiness criteria. |
| 1.0 | Initial PLAT-13.6 operations and observability specification. |
