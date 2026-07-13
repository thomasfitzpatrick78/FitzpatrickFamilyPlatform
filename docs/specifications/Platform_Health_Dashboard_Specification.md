# Platform Health Dashboard Specification

**Document Version:** 1.0

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** PLAT-14.3

---

## Purpose

Define a governed executive operational view for Platform health across hosts, services, containers, monitoring, backup status, registry integrity, Digital Twin integrity, Platform risks, and engineering health indicators.

---

## Information Placement

| Information | Primary Home | Rationale |
|-------------|--------------|-----------|
| Host and service time-series health | Grafana | Operational telemetry belongs in dashboards when metric sources are validated. |
| Container metrics | Grafana after PLAT-14.1 validation | Container panels must wait for modernized metrics proof. |
| Monitoring target status | Grafana and repository evidence | Live state in Grafana; validation snapshots in repository reports. |
| Backup status | Repository-generated reports initially | Backup evidence may come from runbooks before live dashboard integration. |
| Registry integrity | Repository-generated reports | Registry validation is repository-first. |
| Digital Twin integrity | Repository-generated reports | Planned versus active state is governed in repository artifacts. |
| Platform risks | Repository-generated reports | Risk interpretation requires reviewed context. |
| Engineering health indicators | Repository-generated reports | Engineering metrics are milestone and governance evidence. |
| Executive summary | Combined dashboard or report index | Final channel depends on validated sources and user need. |

---

## Future Scope

- Unified executive web portal.
- Automated backup evidence ingestion.
- Longitudinal engineering metrics warehouse.
- Cross-repository dashboard federation.
- Customer-facing household health views.

---

## Requirements

- Dashboard claims must be traceable to validated sources.
- Repository-generated reports must distinguish current state from planned state.
- Risk indicators must include owner, evidence, and next review point.
- Executive view must be readable without requiring terminal access.
- No public internet exposure is approved in the initial release.
- No secrets or personal financial data may appear in dashboards or reports.

---

## Acceptance Criteria

PLAT-14.3 is ready for review when:

- Grafana versus repository-report ownership is defined.
- Future-scope information is separated from Milestone 14 scope.
- Executive health indicators include evidence and avoid unsupported precision.
- Container-health dashboard work depends on PLAT-14.1 metric validation.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial PLAT-14.3 platform health dashboard specification. |
