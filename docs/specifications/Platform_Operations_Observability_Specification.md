# Platform Operations and Observability Specification

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6 - Platform Operations and Observability

---

## Purpose

This specification defines the governed target state for Platform operations and observability.

It does not deploy monitoring, backups, alerts, scripts, containers, packages, timers, dashboards, or services.

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
  |           |     |-- Prometheus (planned)
  |           |     |-- Grafana (planned)
  |           |     |-- cAdvisor (planned)
  |           |
  |           |-- Node Exporter (planned)
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

Proton VPN on the MacBook intentionally uses Proton DNS while connected. That operating mode is not a Pi-hole failure.

---

## Target Components

| Component | Responsibility | State |
|-----------|----------------|-------|
| Prometheus | Metrics collection, retention, target health, alert rule evaluation | Planned |
| Node Exporter | Beelink/Linux host metrics | Planned |
| cAdvisor | Docker and container metrics | Planned |
| Grafana | Governed dashboards and alert visibility | Planned |
| Pi-hole checks | DNS, admin, health, and customer-facing service validation | Planned |
| Backup scripts | Backup, checksum, report, and retention workflow | Planned |
| Restore validation | Isolated restore proof and reporting | Planned |
| Controlled update workflow | Version, digest, backup, deployment, observation, rollback | Planned |

---

## Target Ports

| Component | Port | Exposure |
|-----------|------|----------|
| Pi-hole DNS | TCP/UDP 53 | Home network production DNS |
| Pi-hole admin | TCP 8080 | Trusted home network only |
| Prometheus | TCP 9090 | Trusted home network only when implemented |
| Grafana | TCP 3000 | Trusted home network only when implemented |
| Node Exporter | TCP 9100 | Prometheus/home network only when implemented |
| cAdvisor | TCP 8080 or assigned alternative | Must avoid Pi-hole admin conflict; trusted home network only |

No monitoring interface may be exposed to the Internet.

---

## Target Persistent Paths

These paths describe target state. This repository workstream does not create files on the Beelink.

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
6. Grafana reads Prometheus through a provisioned data source.
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

PLAT-13.6 repository-only planning is complete when:

- ADR-007 records the approved architecture.
- Service lifecycle and cutover checklist exist.
- Present Beelink, Docker, Pi-hole, and Raspberry Pi rollback facts are recorded.
- Prometheus, Node Exporter, cAdvisor, Grafana, alerts, backups, restore validation, and controlled updates are planned but not deployed.
- Tests and EAP validations pass.
- No live infrastructure changes are performed.
- No secrets are committed.

---

## Related Documents

- [ADR-007 - Governed Operations and Observability](../architecture/decisions/ADR-007-Governed-Operations-and-Observability.md)
- [Platform Service Lifecycle](../governance/Service_Lifecycle.md)
- [Production Service Cutover Checklist](../governance/Production_Service_Cutover_Checklist.md)
- [Pi-hole Service Objectives](../operations/Pi-hole_Service_Objectives.md)
- [Incident Response Runbooks](../operations/Incident_Response_Runbooks.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial PLAT-13.6 operations and observability specification. |
