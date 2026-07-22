# Operational Excellence Specification

**Document Version:** 1.5

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** PLAT-14.2

---

## Purpose

Define prioritized Milestone 14 operational excellence scope for backup, restore, recovery validation, alerting, runbooks, evidence retention, and service-level recovery.

This specification separates categories so Milestone 14 does not imply all categories will be implemented.

---

## Operational Categories

| Category | Definition | Milestone 14 Priority |
|----------|------------|-----------------------|
| Repository backup | Git repository history and governance artifacts. | Confirm existing git-based protection and document gaps. |
| Configuration backup | Service configuration, compose files, dashboards, scrape config, registry records. | High. |
| Persistent application data backup | Runtime data volumes for services such as Grafana and future applications. | High for active services; candidate for planned services. |
| Host backup | Operating system and host-level recovery. | Candidate pending platform owner decision. |
| Restore testing | Isolated proof that backups can be restored. | High for selected scope. |
| Disaster recovery | Recovery from host loss or major service failure. | Define scenarios; implementation may be deferred. |
| Service-level recovery | Service-specific recovery objectives and runbooks. | High for Pi-hole, Prometheus, Grafana, and registry validation. |
| Authentication recovery | Recovery of Platform-owned authentication boundary, certificates, and access-revocation capability. | High for FFFA-14.2B before real household data. |

---

## Alerting Scope

Initial alerting requirements should cover:

- Pi-hole availability and DNS health.
- Prometheus target availability.
- Host resource risk where validated.
- Backup failure or stale backup evidence.
- Grafana dashboard or data-source failure where validated.
- Authentication boundary health and certificate validity when FFFA-14.2B is approved.

Alert delivery mechanisms require human approval before activation.

Container-health alerts and recovery recommendations must consume validated PLAT-14.1A assessments only after separate dashboard/API and live-evidence gates. Alerting must preserve assessment confidence, reason codes, freshness, and expiration; it must not independently reinterpret provider availability or dashboard no-data as subject failure. The published fixture-only slice does not authorize alert activation.

Under the accepted and published Production Provider Adapter Architecture, provider failures, timeouts, authorization denials, limitations, and coverage loss remain evidence-quality conditions. Operational Excellence may later recommend investigation or disablement from them but cannot treat them as service failure, trigger remediation, or bypass the separately governed provider, consumer, alert, and EO activation gates.

---

## Evidence Retention

Evidence should record:

- Date and time.
- Target service or host.
- Command or validation performed.
- Result.
- Evidence location.
- Data sensitivity note.
- Reviewer.

Secrets, credentials, personal financial data, and runtime-only artifacts must not be committed.

---

## Service Recovery Objectives

Where practical, service-level recovery objectives should define:

- Maximum acceptable outage.
- Minimum backup frequency.
- Restore validation cadence.
- Rollback service or fallback path.
- Required human approval.

If evidence is insufficient, record the objective as a decision required before implementation.

---

## Acceptance Criteria

PLAT-14.2 is ready for review when:

- Backup, restore, recovery, alerting, runbook, evidence, and service recovery categories are separated.
- Prioritized Milestone 14 scope is explicit.
- Implementation deferrals are documented.
- Human approval requirements are clear for alert activation, restore, reboot, rollback, and production changes.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.5 | Added provider-failure and limitation handling while preserving alert, remediation, activation, and live-operation gates. |
| 1.4 | Recorded publication of the PLAT-14.1A fixture assessment proof while preserving alerting, dashboard/API, and live-operation gates. |
| 1.3 | Recorded the complete unpublished PLAT-14.1A fixture assessment proof while preserving alerting, dashboard, and live-operation gates. |
| 1.2 | Added the PLAT-14.1A governed-assessment dependency and preserved separate alert and live-operation approval. |
| 1.1 | Added authentication boundary monitoring, backup, and recovery as Platform operational excellence scope. |
| 1.0 | Initial PLAT-14.2 operational excellence specification. |
