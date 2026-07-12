# Infrastructure Registry

**Registry Version:** 1.0

**Milestone:** Milestone 12 - WS-12.1 Infrastructure Registry Foundation

---

## Purpose

This directory contains the Git-native Infrastructure Registry for the Fitzpatrick Family Platform.

The registry is the authoritative source for Platform infrastructure assets and services. Human-readable documentation may be derived from these records.

---

## Scope

Infrastructure Registry v1.0 includes representative records for:

- Physical devices
- Network devices
- Hosts
- Services
- Planned services
- Locations
- Ownership
- Lifecycle status
- Health status
- Dependencies
- Future monitoring readiness

---

## Format

Registry records are YAML files under `registry/records/`.

The schema is documented in `registry/schema/infrastructure_registry_schema.yaml`.

---

## Validation

Registry validation is integrated into Platform EAP repository validation:

```bash
./platform-eap repository validate
```

Validation checks required fields, allowed status values, unique identifiers, owner references, location references, dependency references, monitoring readiness, Platform Digital Twin integrity, and finance-scope exclusion.


---

## WS-12.2 Device Inventory

WS-12.2 adds real Fitzpatrick home infrastructure device records using the approved Infrastructure Registry schema.

Device records include:

- Beelink mini PC.
- Beelink mini PC running the production Pi-hole service.
- Raspberry Pi retained as Pi-hole rollback infrastructure.
- Frontier fiber ONT or modem.
- ASUS mesh router and node devices.
- Two 2.5Gb network switches.
- UPS battery backup.
- Tom's MacBook as an administration workstation.
- Tapo hubs represented as smart-home infrastructure physical devices.

Known facts are recorded directly. Unknown model numbers, serial numbers, management interfaces, port counts, protected loads, operating systems, or quantities are marked `TBD` in optional fields.

`TBD` values do not bypass required registry validation. Required fields, references, lifecycle status, health status, monitoring readiness, and finance-scope exclusions remain validated by Platform EAP.

---

## PLAT-13.3 Delivered Hardware Inventory

PLAT-13.3 records delivered hardware facts for Beelink bring-up planning while preserving pending lifecycle state.

Delivered hardware now recorded in registry:

- Beelink Mini S, Intel N150, 16GB memory, 512GB storage, 12V / 3A input.
- Two TP-Link TL-SG108S-M2 8-port 2.5G unmanaged switches.
- CyberPower CP850PFCLCD UPS, 850VA / 510W.

PLAT-13.6 records that the Beelink has since become the active production Platform host.

Architecture Review Board decisions for PLAT-13.3:

- Ubuntu Server 24.04 LTS is the approved Beelink operating system baseline.
- The factory Windows installation will be erased during Ubuntu Server installation. No Windows image will be created. This node is being commissioned as Platform Node 001 and Windows is not part of the Platform operating model.
- Registry evidence must be captured immediately after BIOS verification, Ubuntu installation, networking completion, and SSH verification.
- Docker installation is out of scope and deferred to a future workstream.

PLAT-13.3 does not migrate Pi-hole, change router DNS, install planned services, implement monitoring, implement remote management, or modernize the network.


---

## PLAT-13.6 Operations and Observability Registry Updates

PLAT-13.6 records the verified production baseline and planned observability capabilities.

Present state now recorded in registry:

- Beelink host `beelink` is active at `192.168.50.127` with MAC `78:55:36:09:D2:45`.
- Ubuntu Server 26.04 LTS is recorded as the verified Beelink operating system.
- Docker Engine is active and enabled on the Beelink.
- Pi-hole DNS is active in Docker on the Beelink.
- Raspberry Pi at `192.168.50.67` remains powered on and unchanged as the immediate rollback DNS host.

Planned capabilities now represented as planned services:

- Prometheus.
- Node Exporter.
- cAdvisor.
- Grafana.
- Platform backup and recovery.
- Platform alerting.
- Controlled container updates.

These records do not deploy monitoring, backups, alerts, restore validation, update automation, packages, containers, or services.

---

## WS-12.3 Service Registry

WS-12.3 adds known and planned Platform service records using the approved Infrastructure Registry schema.

Active service records include:

- Pi-hole DNS service.
- Platform Engineering Automation / `platform-eap` validation capability.
- Infrastructure Registry validation capability.

Planned service records include:

- Home Assistant.
- MQTT broker.
- Ollama local AI service.
- Platform monitoring dashboard.
- Remote management service.

Known host and service dependencies are linked through registry record IDs. Unknown optional details such as version, management URL, host placement, access model, authentication model, and implementation technology are marked `TBD`.

These records do not implement service deployment, monitoring, polling, dashboards, automation, or remote management.

---

## WS-12.5 Platform Validation

WS-12.5 elevates Infrastructure Registry validation into static Platform Digital Twin integrity validation.

Repository validation now verifies unique registry IDs, dependency references, classified topology reference types, active service host reachability, planned service host targets, orphaned active services, and service dependency cycles.

Validation remains deterministic and local-file based. It does not perform runtime health checks, network polling, discovery, monitoring, dashboards, automation, remote management, or registry CLI operations.

---

## WS-12.6 Platform Operating Environment

WS-12.6 documents the Platform operating environment baseline from registry records.

The operating environment guidance covers the admin workstation model, host placement assumptions, remote management expectations, backup and recovery expectations, update and patching expectations, and service hosting readiness.

The registry remains authoritative. The operating environment document summarizes registry state and must not be treated as a separate inventory.


---

## WS-12.7 Registry CLI

WS-12.7 adds read-only Infrastructure Registry CLI commands to inspect the Platform Digital Twin.

Supported commands include:

```bash
./platform-eap registry list
./platform-eap registry show <record-id>
./platform-eap registry services
./platform-eap registry hosts
./platform-eap registry devices
./platform-eap registry validate
./platform-eap registry topology
```

The CLI reads registry records from this directory and does not mutate records or create a second inventory.
