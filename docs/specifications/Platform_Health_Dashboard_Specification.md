# Platform Health Dashboard Specification

**Document Version:** 1.3

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
| Container operational health | Grafana or repository report after PLAT-14.0A publication and architecture-aligned PLAT-14.1A validation | Container views render governed assessments and must wait for normalized evidence and health proof. |
| Monitoring target status | Grafana and repository evidence | Live state in Grafana; validation snapshots in repository reports. |
| Backup status | Repository-generated reports initially | Backup evidence may come from runbooks before live dashboard integration. |
| Registry integrity | Repository-generated reports | Registry validation is repository-first. |
| Digital Twin integrity | Repository-generated reports | Planned versus active state is governed in repository artifacts. |
| Platform risks | Repository-generated reports | Risk interpretation requires reviewed context. |
| Engineering health indicators | Repository-generated reports | Engineering metrics are milestone and governance evidence. |
| AI Session Readiness | Repository-generated Engineering Metrics report sourced from the governed readiness JSON report. | Repository onboarding readiness is not Prometheus telemetry and must retain validator source-of-truth boundaries. |
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

## Platform Operations Consumer Contract

For Container Operational Health, PLAT-14.3A and future dashboards consume the published PLAT-14.0A Operational Health Assessment contract and later verified PLAT-14.1A evidence. Dashboards may render:

- Health status.
- Assessment confidence.
- Freshness and validity.
- Governed reason codes and findings.
- Supporting evidence and reconciliation references.

Dashboards must not:

- Calculate authoritative container health independently through PromQL, dashboard expressions, panel mappings, or presentation logic.
- Treat missing, stale, ambiguous, conflicting, or incomplete data as Healthy.
- Treat provider or scrape-target health as proof of subject health.
- Replace Platform-owned subject identity with provider labels or runtime identifiers.
- Interpret health as permission for execution, automation, lifecycle promotion, or live change.

Dashboard no-data is represented through governed evidence and assessment outcomes, normally `insufficient_evidence` when mandatory current evidence is unavailable. It is not an independent health state.

The PLAT-14.1A consumer mapping must distinguish:

| Condition | Dashboard Treatment |
|-----------|---------------------|
| No assessment exists | Render `not_evaluated`. |
| Assessment reports insufficient evidence | Render `insufficient_evidence` with governed reasons. |
| Provider unavailable | Render telemetry unavailability; do not infer subject failure. |
| Required signal unavailable | Render insufficient evidence. |
| Assessment past `valid_until` | Render expired/noncurrent; never current Healthy. |
| Query or rendering failure | Render presentation failure without changing the assessment. |
| Conclusive unhealthy assessment | Render governed `unhealthy` status and reasons. |

PLAT-14.3A remains downstream of the published PLAT-14.1A specification, separately authorized core implementation, and verified assessment outputs. Dashboard integration, Grafana changes, and live deployment remain separate gates.

---

## AI Session Readiness Repository Source Contract

EO-14.8E adds repository-side Platform Health visibility through the structured Engineering Metrics report. It does not deploy, provision, connect to, or modify Grafana.

| Health Input | Source Field |
|--------------|--------------|
| Current readiness state | `platform_health.ai_session_readiness.state` |
| Error count | `platform_health.ai_session_readiness.error_count` |
| Warning count | `platform_health.ai_session_readiness.warning_count` |
| Evidence condition | `platform_health.ai_session_readiness.evidence_status` |
| Last generated time | `platform_health.ai_session_readiness.last_generated_at` |
| Source availability | `platform_health.ai_session_readiness.source_available` and `source_usable` |
| Source location | `platform_health.ai_session_readiness.source_report_path` |

The transformation preserves `READY`, `READY WITH WARNINGS`, `NOT READY`, and `UNKNOWN`. Missing or malformed evidence must remain `UNKNOWN` and must not be rendered as healthy. `READY WITH WARNINGS` retains its warning count and disclosed conditions; `NOT READY` remains blocking. The source of truth remains `./platform-eap ai-session readiness` and its governed reports.

No time-based staleness threshold is introduced by this contract. A future `stale` evidence condition requires separately governed freshness rules. Runtime Platform Health dashboard deployment remains future PLAT work, not EO-14.8E.

---

## Acceptance Criteria

PLAT-14.3 is ready for review when:

- Grafana versus repository-report ownership is defined.
- Future-scope information is separated from Milestone 14 scope.
- Executive health indicators include evidence and avoid unsupported precision.
- Container-health dashboard work depends on PLAT-14.0A publication, architecture-aligned PLAT-14.1A contract validation, and verified evidence.
- Presentation preserves governed health, confidence, freshness, reasons, and no-data semantics without recalculation.

---

## Related Documents

- [Platform Operations Domain Architecture](../architecture/Platform_Operations_Domain_Architecture.md)
- [Platform Operational Evidence and Health Contract Specification](Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [Container Metrics Modernization Specification](Container_Metrics_Modernization_Specification.md)
- [Container Operational Health Specification](Container_Operational_Health_Specification.md)
- [Operations Analyst Specification](../engineering-organization/Operations_Analyst_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.3 | Added the aligned PLAT-14.1A assessment-expiration, provider-unavailability, and presentation-failure distinctions and preserved the downstream dashboard gate. |
| 1.2 | Added the PLAT-14.0A Platform Operations read-only consumer boundary and authoritative no-data treatment. |
| 1.1 | Added the EO-14.8E repository-side AI Session Readiness health-source contract without live dashboard changes. |
| 1.0 | Initial PLAT-14.3 platform health dashboard specification. |
