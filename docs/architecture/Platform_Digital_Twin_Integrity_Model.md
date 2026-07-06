# Platform Digital Twin Integrity Model

**Document Version:** 1.1

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document defines the static integrity validation model introduced by WS-12.5 for the Fitzpatrick Family Platform Infrastructure Registry.

The Infrastructure Registry is treated as a Platform Digital Twin: a Git-native representation of known and planned infrastructure assets, services, relationships, ownership, lifecycle state, health state, and future monitoring readiness.

---

## Validation Boundary

Platform Digital Twin integrity validation is deterministic and local-file based.

It validates the consistency of registry records stored under `registry/records/`. It does not perform runtime health checks, network polling, service discovery, monitoring, dashboards, automation, or remote management.

---

## Integrity Rules

Platform EAP repository validation checks the following registry integrity rules:

- Registry record IDs must be unique across all YAML records.
- General dependency references must point to existing registry record IDs.
- Classified topology dependency references must point to existing registry record IDs.
- Classified topology dependency fields must contain YAML lists.
- `network_dependencies` must reference network device records.
- `host_dependencies` must reference host records.
- `service_dependencies` must reference service or planned service records.
- `power_dependencies` must reference physical device records.
- `administrative_dependencies` must reference physical device or host records.
- Active services must have a valid host relationship directly or through a service dependency chain.
- Planned services with host relationships must reference planned or active host targets.
- Active services without a valid host path are treated as orphaned services.
- Service dependency chains must not contain circular dependencies.
- Records with explicit `TBD` or unknown markers are reported as static readiness information.

---

## Host Relationship Semantics

A service has a valid host relationship when it directly references a host through `host_dependencies` or indirectly depends on another service that has a valid host relationship.

This supports Platform capabilities such as Infrastructure Registry validation, which may be represented as a service dependency on Platform EAP rather than being directly hosted itself.

---

## Cycle Detection Scope

Cycle detection applies to service dependency chains.

Other topology relationships, such as administrative access or network reachability, may form real-world loops and are therefore validated for reference integrity and type correctness rather than circularity.

## Unknown Field Reporting

Registry records may intentionally use `TBD` or `unknowns` fields for details that are not yet confirmed.

Platform EAP reports these markers as information so architecture review can distinguish known gaps from missing records. These markers do not imply runtime health status and do not trigger discovery, polling, or automation.

---

## Related Documents

- [ADR-006 - Registry Driven Infrastructure Foundation](decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md)
- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)
- [Network Topology Model](Network_Topology_Model.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Infrastructure Operations Readiness](Infrastructure_Operations_Readiness.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Added static unknown and TBD field reporting for PLAT-13.1 readiness. |
| 1.0 | Initial WS-12.5 Platform Digital Twin integrity validation model. |
