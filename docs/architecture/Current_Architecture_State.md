# Current Architecture State

**Document Version:** 1.3

**Status:** Active

**Milestone:** Milestone 12

---

## Summary

The Platform repository contains governance, product, architecture, standards, validation automation, reports, milestone planning, and registry records for the active Beelink-hosted Pi-hole production service and the active PLAT-13.6.2 Metrics Foundation.

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

Prometheus is active at `192.168.50.127:9090` with 15-day local retention at `/platform/data/monitoring/prometheus`.

Node Exporter and cAdvisor are active on the internal `platform-monitoring` Docker network only.

Grafana has a repository-managed PLAT-13.6.3 implementation-ready package for Architecture Gatekeeper review, including Compose service definition, provisioning files, dashboards, runbook, and evidence template. Grafana is not deployed.

Alerts, backup automation, restore validation, and controlled updates remain planned and are not deployed.

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
| 1.4 | Recorded PLAT-13.6.3 Operations Dashboard repository package as implementation-ready and not deployed. |
| 1.3 | Recorded active PLAT-13.6.2 Metrics Foundation state and remaining planned operations capabilities. |
| 1.2 | Updated current architecture state for active Beelink-hosted Pi-hole and ADR-007 governed observability planning. |
| 1.1 | Added Milestone 12 Registry Driven Infrastructure Foundation architecture state. |
| 1.0 | Initial current architecture state. |
