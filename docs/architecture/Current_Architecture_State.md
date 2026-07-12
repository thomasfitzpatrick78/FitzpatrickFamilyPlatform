# Current Architecture State

**Document Version:** 1.2

**Status:** Active

**Milestone:** Milestone 12

---

## Summary

The Platform repository contains governance, product, architecture, standards, validation automation, reports, milestone planning, and registry records for the active Beelink-hosted Pi-hole production service.

Milestone 12 selected the Registry Driven Infrastructure Foundation architecture. Milestone 13 extends that foundation toward governed operations and observability.

---

## Established Architecture

- Repository-managed governance.
- Repository-local ADR framework.
- Product scope excluding finance.
- Independent engineering automation foundation.
- Portfolio integration without shared implementation code.
- Registry Driven Infrastructure Foundation selected for Infrastructure Registry v1.0.
- Git-native YAML or JSON registry records planned as authoritative infrastructure knowledge.
- Validation-first design selected before monitoring, dashboards, or automation.
- Governed operations and observability architecture selected in ADR-007.

---

## Runtime State

Pi-hole is active in Docker on Beelink at `192.168.50.127`.

Prometheus, Grafana, exporters, alerts, backup automation, restore validation, and controlled updates remain planned and are not deployed by PLAT-13.6 repository-only work.

---

## Related Documents

- [Architecture Decision Log](Architecture_Decision_Log.md)
- [Architecture Backlog](Architecture_Backlog.md)
- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)
- [ADR-006 - Registry Driven Infrastructure Foundation](decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md)
- [ADR-007 - Governed Operations and Observability](decisions/ADR-007-Governed-Operations-and-Observability.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Updated current architecture state for active Beelink-hosted Pi-hole and ADR-007 governed observability planning. |
| 1.1 | Added Milestone 12 Registry Driven Infrastructure Foundation architecture state. |
| 1.0 | Initial current architecture state. |
