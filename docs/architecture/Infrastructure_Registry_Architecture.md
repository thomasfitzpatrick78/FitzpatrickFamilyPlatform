# Infrastructure Registry Architecture

**Document Version:** 1.3

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document defines the selected Registry Driven Infrastructure Foundation architecture for Milestone 12.

---

## Architecture Summary

Infrastructure Registry v1.0 is a Git-native structured registry for Platform infrastructure assets and services.

The registry is the authoritative source for infrastructure knowledge. Human-readable documentation should be generated, derived, or synchronized from registry records rather than becoming a competing source of truth.

---

## Architectural Principles

- Git-native records are authoritative.
- Structured YAML or JSON records are preferred over prose-only inventory.
- Human-readable documentation remains important, but it should derive from the structured registry model.
- Validation comes before monitoring, dashboards, or automation.
- Registry records must be reviewable through normal repository workflows.
- Finance functionality remains outside Platform scope.

---

## Registry Record Domains

Infrastructure Registry v1.0 shall support planning for these record domains:

| Domain | Purpose |
|--------|---------|
| Physical devices | Represent household devices and equipment. |
| Network devices | Represent routers, switches, access points, and network infrastructure. |
| Hosts | Represent machines or runtime hosts. |
| Services | Represent active Platform or household services. |
| Planned services | Represent intended services before implementation or deployment. |
| Locations | Represent physical or logical locations. |
| Ownership | Represent responsible owner or steward. |
| Lifecycle status | Represent planned, active, retired, or replacement state. |
| Health status | Represent known health state or monitoring readiness. |
| Dependencies | Represent relationships between assets, hosts, and services. |
| Future monitoring readiness | Represent whether an asset or service can later participate in health checks or dashboards. |

---

## Registry Storage Model

Milestone 12 selects repository-managed YAML records for Infrastructure Registry v1.0.

WS-12.1 establishes this initial layout:

```text
registry/
  schema/
    infrastructure_registry_schema.yaml
  records/
    devices/
    hosts/
    locations/
    network_devices/
    owners/
    planned_services/
    services/
```

The schema, naming conventions, representative records, and validation rules are implemented as a small independently releasable foundation.

---

## Validation-First Design

The registry shall be designed so deterministic validation can check:

- Required fields.
- Allowed lifecycle statuses.
- Allowed health statuses.
- Unique identifiers.
- Dependency references.
- Ownership references.
- Location references.
- Monitoring-readiness fields.
- Forbidden finance scope.

WS-12.1 integrates registry validation into Platform EAP repository validation.

---

## Topology Relationship Model

WS-12.4 adds classified dependency metadata to registry records to represent physical, logical, and operational topology relationships without introducing a separate topology source of truth.

Classified dependency fields identify network, host, service, power, and administrative relationships. Platform EAP validates that classified dependency fields are lists and that each reference resolves to an existing registry record.

---

## Future Evolution

The registry may evolve toward:

- Generated Markdown inventory documents.
- Health checks.
- Monitoring integrations.
- Dashboards.
- Dependency impact views.
- Automation readiness gates.
- Platform operating environment reports.

Future evolution requires governed requirements, ADRs when applicable, specifications, validation, and evidence.

Milestone 13 introduces the registry-driven Platform lifecycle pattern:

```text
Authoritative Registry -> Validation -> Automation -> Observability -> AI Reasoning
```

The registry and validation stages must remain authoritative before future automation, observability, or AI reasoning stages are implemented.

---

## Related Documents

- [ADR-006 - Registry Driven Infrastructure Foundation](decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Registry-Driven Platform Lifecycle](Registry_Driven_Platform_Lifecycle.md)
- [Milestone 12 Plan](../milestones/Milestone_12/Milestone_12_Infrastructure_Registry_v1.0.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.3 | Added Milestone 13 registry-driven Platform lifecycle pattern. |
| 1.2 | Added WS-12.4 topology relationship model with classified dependency validation. |
| 1.1 | Updated for WS-12.1 registry structure, YAML records, and Platform EAP validation integration. |
| 1.0 | Initial Infrastructure Registry architecture for Milestone 12. |
