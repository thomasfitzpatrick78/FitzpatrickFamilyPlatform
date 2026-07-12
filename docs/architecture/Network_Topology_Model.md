# Network Topology Model

**Document Version:** 1.3

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document explains how WS-12.4 represents the Fitzpatrick home network topology using the Infrastructure Registry as the authoritative source.

---

## Source of Truth

The Infrastructure Registry remains the single source of truth for topology.

Topology is represented through structured YAML registry records under `registry/records/`. This document describes the model; it does not define a separate topology inventory.

---

## Topology Relationship Fields

WS-12.4 adds optional classified dependency fields to registry records:

| Field | Meaning |
|-------|---------|
| `network_dependencies` | Network connectivity, upstream network, or network access dependencies. |
| `host_dependencies` | Host placement or service runtime host dependencies. |
| `service_dependencies` | Service-to-service dependencies. |
| `power_dependencies` | Power continuity or power support dependencies. |
| `administrative_dependencies` | Administrative workstation or operator access dependencies. |

The existing required `dependencies` field remains the general dependency list required by the approved schema. Classified dependency fields provide additional topology semantics and are validated when present.

---

## Represented Topology

The current registry represents the following topology relationships:

```text
Frontier ONT
  -> ASUS Mesh Router Primary
      -> ASUS Mesh Node
      -> TP-Link TL-SG108S-M2 Switch 1
          -> Beelink Mini PC Host
              -> Docker Engine
                  -> Pi-hole DNS Service
                  -> Planned monitoring services
          -> Raspberry Pi Pi-hole Rollback Host
      -> TP-Link TL-SG108S-M2 Switch 2
          -> Family NAS
      -> Tapo Hubs
      -> Tom MacBook Admin Workstation

CyberPower CP850PFCLCD UPS
  -> ASUS Mesh Router Primary
  -> TP-Link TL-SG108S-M2 Switch 1
  -> TP-Link TL-SG108S-M2 Switch 2
  -> Beelink Mini PC
  -> Raspberry Pi Pi-hole Device
  -> Family NAS
```

Power relationships represent planned or known power-support dependencies in registry form. Protected load details remain `TBD` where not yet confirmed.

---

## Validation

Platform EAP repository validation checks classified dependency fields when present:

- Classified dependency fields must be YAML lists.
- Every classified dependency reference must resolve to another registry record ID.
- Classified dependency references must point to the expected record type.
- Active services must have a valid host relationship directly or through a service dependency chain.
- Planned services must reference planned or active host targets when host relationships are present.
- Service dependency chains must not contain circular dependencies.
- Finance-scope exclusions still apply to registry records.

---

## Non-Goals

WS-12.4 does not implement network discovery, live topology generation, monitoring, polling, dashboards, automation, registry CLI, or remote management.

---

## Related Documents

- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Platform Digital Twin Integrity Model](Platform_Digital_Twin_Integrity_Model.md)
- [Milestone 12 Plan](../milestones/Milestone_12/Milestone_12_Infrastructure_Registry_v1.0.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.3 | Updated represented topology for Beelink-hosted Pi-hole, Docker, planned monitoring, and Raspberry Pi rollback under PLAT-13.6. |
| 1.2 | Updated delivered TP-Link switch and CyberPower CP850PFCLCD labels for PLAT-13.3 planning context. |
| 1.1 | Updated validation guidance for WS-12.5 Platform Digital Twin integrity checks. |
| 1.0 | Initial WS-12.4 network topology model. |
