# Platform Digital Twin Integrity Model

**Document Version:** 1.5

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

PLAT-14.0A preserves this boundary. Platform Operations uses valid registry references as declared-state authority and creates separate evidence, reconciliation, and health records. Runtime observations never mutate the Digital Twin implicitly, and a health assessment never becomes a registry lifecycle promotion.

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

## Future Container Identity Integrity

The published Registry Container Identity Foundation implementation preserves the service record as the Digital Twin subject and uses an optional conditional field set rather than a container-instance record type. Schema-driven validation keeps all 39 legacy records valid, requires exact host and Compose identity before active eligibility, enforces host-scoped uniqueness, and fails closed on unknown or contradictory container states.

Container participation is separate from existing lifecycle and `health_status`. Runtime IDs, provider labels, evidence, reconciliation, and Operational Health Assessments remain outside the Digital Twin declaration and cannot mutate it automatically. The active schema and records are unchanged by the architecture package.

---

## Related Documents

- [ADR-006 - Registry Driven Infrastructure Foundation](decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md)
- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)
- [Network Topology Model](Network_Topology_Model.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Registry Container Identity Foundation Architecture](Registry_Container_Identity_Foundation_Architecture.md)
- [Registry Container Identity Foundation Specification](../specifications/Registry_Container_Identity_Foundation_Specification.md)
- [Infrastructure Operations Readiness](Infrastructure_Operations_Readiness.md)
- [Platform Operations Domain Architecture](Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](../specifications/Platform_Operational_Evidence_and_Health_Contract_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.5 | Recorded publication of the Architecture Gatekeeper-accepted Registry identity implementation with all 39 records unchanged and no runtime authority. |
| 1.4 | Recorded implemented schema 1.1 and Digital Twin-compatible validation with all 39 records unchanged and no runtime authority. |
| 1.3 | Added the future container identity integrity, legacy compatibility, uniqueness, and no-runtime-mutation boundaries. |
| 1.2 | Added the PLAT-14.0A declared-state boundary and separation from evidence, reconciliation, and health. |
| 1.1 | Added static unknown and TBD field reporting for PLAT-13.1 readiness. |
| 1.0 | Initial WS-12.5 Platform Digital Twin integrity validation model. |
