# Network Modernization Readiness Checklist

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This checklist prepares for future network modernization involving planned TP-Link 2.5Gb switches and CyberPower UPS.

PLAT-13.1 does not install network equipment or change topology.

---

## Registry Evidence

- Planned switch 1: `net-switch-2-5gbe-1`.
- Planned switch 2: `net-switch-2-5gbe-2`.
- Planned UPS: `dev-ups-battery-backup`.
- Current active primary router: `net-asus-mesh-router-primary`.
- Current Pi-hole host: `host-raspberry-pi-pihole`.

---

## Checklist

| Category | Item | Status |
|----------|------|--------|
| Arrival | Confirm TP-Link switches received | TBD |
| Arrival | Confirm CyberPower UPS received | TBD |
| Inventory | Record exact switch models and port counts | TBD |
| Inventory | Record exact UPS model and protected loads | TBD |
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
| 1.0 | Initial network modernization readiness checklist. |
