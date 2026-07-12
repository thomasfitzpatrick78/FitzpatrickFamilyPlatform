# Platform Operating Environment

**Document Version:** 1.3

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document defines the Fitzpatrick Family Platform operating environment baseline for WS-12.6.

The Infrastructure Registry remains the authoritative source for operating environment records. This document explains how the current registry supports operating readiness; it does not create a second inventory.

---

## Authoritative Source

Operating environment facts are maintained as Git-native registry records under `registry/records/`.

This document may summarize registry state for human review, but any future correction to devices, hosts, services, lifecycle status, health status, ownership, location, or dependencies must be made in registry records first.

---

## Operating Environment Baseline

The current Platform operating environment baseline includes:

| Area | Registry Evidence | Operating Baseline |
|------|-------------------|--------------------|
| Administration | [`dev-toms-macbook-admin`](../../registry/records/devices/toms-macbook-admin.yaml), [`host-toms-macbook-admin`](../../registry/records/hosts/toms-macbook-admin.yaml) | Tom's MacBook is the current administration workstation for repository and household infrastructure work. |
| Production Platform host | [`dev-beelink-mini-pc`](../../registry/records/devices/beelink-mini-pc.yaml), [`host-beelink-mini-pc`](../../registry/records/hosts/beelink-mini-pc.yaml) | Beelink Mini S is active as Platform Node 001, hostname `beelink`, at `192.168.50.127` with Docker Engine and Beelink-hosted Pi-hole. |
| Rollback DNS host | [`dev-raspberry-pi-pihole`](../../registry/records/devices/raspberry-pi-pihole.yaml), [`host-raspberry-pi-pihole`](../../registry/records/hosts/raspberry-pi-pihole.yaml) | Raspberry Pi remains powered on and unchanged at `192.168.50.67` as immediate Pi-hole rollback host. |
| Power continuity | [`dev-ups-battery-backup`](../../registry/records/devices/ups-battery-backup.yaml) | CyberPower CP850PFCLCD UPS is delivered and pending protected-load validation. |
| Active services | [`svc-pihole-dns`](../../registry/records/services/pihole-dns.yaml), [`svc-docker-engine`](../../registry/records/services/docker-engine.yaml), [`svc-prometheus`](../../registry/records/services/prometheus.yaml), [`svc-node-exporter`](../../registry/records/services/node-exporter.yaml), [`svc-cadvisor`](../../registry/records/services/cadvisor.yaml), [`svc-platform-eap`](../../registry/records/services/platform-eap.yaml), [`svc-infrastructure-registry-validation`](../../registry/records/services/infrastructure-registry-validation.yaml) | Current services are represented as registry records with host, service, network, power, and administrative dependencies where known. |
| Planned services | [`svc-home-assistant`](../../registry/records/planned_services/home-assistant.yaml), [`svc-mqtt-broker`](../../registry/records/planned_services/mqtt-broker.yaml), [`svc-ollama-local-ai`](../../registry/records/planned_services/ollama-local-ai.yaml), [`svc-platform-monitoring-dashboard`](../../registry/records/planned_services/platform-monitoring-dashboard.yaml), [`svc-remote-management`](../../registry/records/planned_services/remote-management.yaml) | Planned services are documented for placement readiness but are not deployed by Milestone 12. |

---

## Admin Workstation Model

Tom's MacBook is the current administrative workstation.

The admin workstation model assumes:

- Repository operations are performed from a governed workstation.
- Platform EAP commands execute locally from the repository working tree.
- Administrative access to Platform infrastructure is represented through `administrative_dependencies` in registry records.
- Administrative access does not imply remote management automation.
- The registry must continue to distinguish administrative dependencies from runtime service dependencies.

The current registry records Tom's MacBook as both a physical device and host representation so future tooling can distinguish physical workstation ownership from host-level administrative use.

---

## Host Placement Assumptions

Host placement is governed by registry `host_dependencies` and lifecycle state.

Current assumptions are:

- Pi-hole DNS is hosted on the Beelink host through Docker.
- Raspberry Pi remains the immediate rollback DNS host.
- Platform EAP is repository-managed and currently associated with the Tom MacBook admin host.
- Infrastructure Registry validation depends on Platform EAP rather than being separately hosted.
- Beelink Mini S is the active Platform host for Pi-hole and the active PLAT-13.6.2 Metrics Foundation. Grafana, alerts, backups, restore validation, and controlled updates remain planned.
- `host-home-server` remains a planned logical host concept and should not be treated as deployed runtime infrastructure until registry lifecycle status changes.

Any future service placement change must update the relevant service registry record before documentation summaries are updated.

---

## Remote Management Expectations

Remote management is represented as a planned service, not an implemented capability.

Milestone 12 expectations are:

- Remote management requirements remain registry-visible through `svc-remote-management`.
- Access model, authentication, authorization, and safety controls remain `TBD` until explicitly designed.
- No remote management daemon, agent, VPN, tunnel, or automation is implemented in WS-12.6.
- Future remote management work must preserve repository governance and explicit operator control.

---

## Backup and Recovery Expectations

Backup and recovery expectations for the current baseline are intentionally operational rather than automated:

- The Git repository remains the durable source for Platform documentation, registry records, governance, and engineering evidence.
- Registry changes should be committed through governed repository workflow before being treated as authoritative.
- Device and service recovery expectations are represented through dependencies, lifecycle status, health status, and monitoring readiness fields.
- UPS coverage is represented where known through `power_dependencies`.
- Automated backup execution, restore orchestration, and device image management are deferred.

Future backup automation should derive scope from registry records rather than maintaining a separate backup inventory.

---

## Update and Patching Expectations

Update and patching expectations for WS-12.6 are documentation-only:

- Operating system values may remain `TBD` until confirmed in registry records.
- Patch ownership follows the registry owner model.
- Platform service patch readiness depends on host placement and lifecycle status.
- Updates to planned services are not actionable until those services move beyond planned lifecycle status.
- No patch automation, package management, or remote execution is implemented in Milestone 12.

Future patching workflows should use registry records for host and service targeting.

---

## Service Hosting Readiness

Service hosting readiness is determined from registry state:

| Host | Readiness | Evidence |
|------|-----------|----------|
| Beelink Mini PC Host | Active production Platform host; Ubuntu Server 26.04 LTS, Docker Engine, and Pi-hole production service are recorded. | [`host-beelink-mini-pc`](../../registry/records/hosts/beelink-mini-pc.yaml) |
| Raspberry Pi Pi-hole Host | Immediate rollback DNS host; not the current production DNS host. | [`host-raspberry-pi-pihole`](../../registry/records/hosts/raspberry-pi-pihole.yaml) |
| Tom MacBook Admin Host | Ready for administration and repository-managed Platform EAP execution; not a durable always-on service host. | [`host-toms-macbook-admin`](../../registry/records/hosts/toms-macbook-admin.yaml) |
| Home Server Host | Planned logical host concept; not active operating baseline. | [`host-home-server`](../../registry/records/hosts/home-server.yaml) |

---

## Validation Model

Operating environment readiness is validated indirectly through Platform EAP repository validation:

- Required registry records exist.
- Registry IDs are unique.
- Dependency references resolve to known records.
- Topology references use expected record types.
- Active services have valid host relationships.
- Planned services reference planned or active host targets when host relationships are present.
- Finance functionality remains excluded from Platform scope.

Validation remains static and local-file based.

---

## Non-Goals

WS-12.6 does not implement:

- Runtime health checks.
- Device polling.
- Network discovery.
- Service deployment.
- Remote management implementation.
- Backup automation.
- Dashboards.
- Registry CLI.
- Finance functionality.

---

## Related Documents

- [ADR-006 - Registry Driven Infrastructure Foundation](decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md)
- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)
- [Network Topology Model](Network_Topology_Model.md)
- [Platform Digital Twin Integrity Model](Platform_Digital_Twin_Integrity_Model.md)
- [Infrastructure Operations Readiness](Infrastructure_Operations_Readiness.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Milestone 12 Plan](../milestones/Milestone_12/Milestone_12_Infrastructure_Registry_v1.0.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.4 | Added active PLAT-13.6.2 Metrics Foundation services to the operating baseline. |
| 1.3 | Updated operating baseline for PLAT-13.6 active Beelink, Docker, Pi-hole, and Raspberry Pi rollback state. |
| 1.2 | Updated Beelink and UPS operating baseline for PLAT-13.3 delivered hardware facts. |
| 1.1 | Updated Beelink, UPS, and Pi-hole operating environment summaries for PLAT-13.1 readiness context. |
| 1.0 | Initial WS-12.6 Platform operating environment baseline. |
