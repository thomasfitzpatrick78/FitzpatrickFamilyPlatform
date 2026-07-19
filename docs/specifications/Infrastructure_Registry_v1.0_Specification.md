# Infrastructure Registry v1.0 Specification

**Document Version:** 1.8

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This specification defines Infrastructure Registry v1.0 as the first usable Fitzpatrick Family Platform capability.

---

## Product Capability

Infrastructure Registry v1.0 establishes a Git-native source of truth for household infrastructure assets and Platform services.

The capability is intended to make infrastructure visible, reviewable, version controlled, and ready for future validation, monitoring, dashboards, and automation.

---

## Required Registry Coverage

Infrastructure Registry v1.0 shall support these concepts:

- Physical devices.
- Network devices.
- Hosts.
- Services.
- Planned services.
- Locations.
- Ownership.
- Lifecycle status.
- Health status.
- Dependencies.
- Future monitoring readiness.

---

## Registry Format

Registry records use structured YAML for WS-12.1.

The authoritative registry schema is maintained at `registry/schema/infrastructure_registry_schema.yaml`.

Representative registry records are maintained under `registry/records/`.

The repository shall treat registry records as authoritative. Markdown documentation may be generated or derived from registry records.

---

## Validation Requirements

WS-12.1 implements deterministic Platform EAP registry validation for:

- Required fields.
- Identifier uniqueness.
- Record type consistency.
- Allowed status values.
- Valid dependency references.
- Valid owner and location references.
- Monitoring-readiness fields.
- Finance-scope exclusion.

WS-12.5 elevates registry validation into static Platform Digital Twin integrity validation for:

- Registry ID uniqueness across all records.
- General dependency references.
- Classified topology reference existence.
- Classified topology reference type correctness.
- Active service host reachability.
- Planned service host target validity.
- Orphaned active services.
- Service dependency cycles.

Registry validation is integrated into `./platform-eap repository validate`.

---

## Device Inventory Records

WS-12.2 populates the registry with known Fitzpatrick home infrastructure device records.

Unknown optional details may be recorded as `TBD` until confirmed. Required schema fields remain mandatory and validated.

---

## Service Registry Records

WS-12.3 populates the registry with known active services and planned Platform services.

Service records may depend on host records, device records, network records, or other service records where the approved schema supports dependency references.

Unknown optional service details may be recorded as `TBD` until confirmed.

---

## Network Topology Relationships

WS-12.4 represents topology through optional classified dependency fields in registry records.

Supported classified dependency fields are:

- `network_dependencies`
- `host_dependencies`
- `service_dependencies`
- `power_dependencies`
- `administrative_dependencies`

These fields do not create a separate source of truth. They add relationship semantics to existing registry records and are validated by Platform EAP when present.


## Platform Digital Twin Integrity Validation

WS-12.5 treats registry records as a static Platform Digital Twin and validates the integrity of the represented assets, services, and relationships.

Platform EAP validation remains local-file based and deterministic. It does not execute runtime health checks, network polling, service discovery, monitoring, dashboards, or automation.


## PLAT-14.0A Declared-State Relationship

The Infrastructure Registry remains the authoritative source for Platform declared state, stable subject linkage, ownership, lifecycle, dependencies, and repository-recorded health fields. PLAT-14.0A does not create a parallel inventory and does not allow provider observations, reconciliation, or health evaluation to mutate registry records automatically.

Future Platform Operational Evidence uses a Platform-owned subject identifier linked to a valid registry record. Provider runtime identifiers remain provenance. A PLAT-14.0A Operational Health Assessment is a separate versioned artifact and is not silently written into the registry `health_status` field or treated as lifecycle promotion. Any future mapping or registry update requires separate governed review and evidence.


## Platform Operating Environment

WS-12.6 defines the Platform operating environment baseline from Infrastructure Registry records.

The operating environment documentation covers administration, host placement assumptions, remote management expectations, backup and recovery expectations, update and patching expectations, and service hosting readiness. It does not create a second operating inventory. Registry records remain authoritative.


## Registry CLI

WS-12.7 introduces read-only Infrastructure Registry CLI commands through `./platform-eap registry`.

The CLI supports listing registry records, showing one record by ID, listing services, hosts, and devices, running registry validation, and summarizing topology relationships. All commands are deterministic, local-file based, and read-only.

---

## Non-Goals

Milestone 12 planning does not authorize:

- Runtime monitoring.
- Dashboards.
- Health-check execution.
- Automation execution.
- SQLite-backed CMDB implementation.
- Platform service deployment.
- Finance functionality.

---

## Related Documents

- [ADR-006 - Registry Driven Infrastructure Foundation](../architecture/decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md)
- [Infrastructure Registry Architecture](../architecture/Infrastructure_Registry_Architecture.md)
- [Platform Operating Environment](../architecture/Platform_Operating_Environment.md)
- [Infrastructure Registry CLI](../architecture/Infrastructure_Registry_CLI.md)
- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Milestone 12 Plan](../milestones/Milestone_12/Milestone_12_Infrastructure_Registry_v1.0.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.8 | Added the PLAT-14.0A declared-state, subject-linkage, and no-implicit-mutation boundary. |
| 1.7 | Added WS-12.7 read-only Registry CLI requirements. |
| 1.6 | Added WS-12.6 Platform operating environment baseline requirements. |
| 1.5 | Added WS-12.5 Platform Digital Twin integrity validation requirements. |
| 1.4 | Added WS-12.4 classified dependency fields for network topology relationships. |
| 1.3 | Added WS-12.3 service registry guidance for active and planned Platform services. |
| 1.2 | Added WS-12.2 device inventory guidance for real infrastructure records and `TBD` optional fields. |
| 1.1 | Updated for WS-12.1 implementation of YAML schema, representative records, and Platform EAP registry validation. |
| 1.0 | Initial Infrastructure Registry v1.0 specification. |
