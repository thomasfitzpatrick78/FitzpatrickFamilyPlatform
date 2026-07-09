# Network Modernization Readiness Checklist

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This checklist prepares for future network modernization involving delivered TP-Link TL-SG108S-M2 2.5G switches and CyberPower CP850PFCLCD UPS.

PLAT-13.1 and PLAT-13.3 do not install network equipment or change topology.

---

## Registry Evidence

- Delivered switch 1: `net-switch-2-5gbe-1`.
- Delivered switch 2: `net-switch-2-5gbe-2`.
- Delivered UPS: `dev-ups-battery-backup`.
- Current active primary router: `net-asus-mesh-router-primary`.
- Current Pi-hole host: `host-raspberry-pi-pihole`.

---

## Checklist

| Category | Item | Status |
|----------|------|--------|
| Arrival | Confirm TP-Link switches received | Complete - delivered TL-SG108S-M2 |
| Arrival | Confirm CyberPower UPS received | Complete - delivered CP850PFCLCD |
| Inventory | Record exact switch models and port counts | Complete - TL-SG108S-M2, 8 ports each |
| Inventory | Record exact UPS model and protected loads | Partial - CP850PFCLCD recorded; protected loads TBD |
| Topology | Document intended cabling before physical change | TBD |
| Rollback | Document original cabling before physical change | TBD |
| Power | Identify router, Pi-hole, Beelink, and switch UPS coverage | TBD |
| Network | Confirm Pi-hole remains reachable during modernization | TBD |
| Registry | Update lifecycle status only after installation | TBD |
| Validation | Run Platform EAP validation after registry updates | TBD |

---

## Implementation Boundary

This checklist does not approve cabling changes, switch installation, UPS installation, router configuration changes, monitoring, discovery, dashboards, or deployment automation.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Updated delivered switch and UPS facts for PLAT-13.3 while preserving network modernization boundary. |
| 1.0 | Initial network modernization readiness checklist. |
