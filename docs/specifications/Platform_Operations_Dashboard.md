# Platform Operations Dashboard

**Document Version:** 1.0

**Status:** Implementation-ready

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6.3 - Operations Dashboard

---

## Purpose

This document defines the reusable dashboard architecture contract for Platform operations dashboards.

It governs dashboard ownership, purpose, lifecycle, review, evidence, and change control independently from Grafana. Grafana is the initial implementation mechanism, but the contract is intended to apply to later dashboards for Home Assistant, MQTT, Ollama, FFFA runtime services, backup health, alerting health, and future hosts.

---

## Dashboard Contract

| Field | Contract |
|-------|----------|
| Dashboard name | Platform Operations Dashboard |
| Purpose | Provide governed operational visibility for the Beelink-hosted Pi-hole service, the Docker runtime, and the Metrics Foundation. |
| Intended users | Family Platform owner and trusted household technical operators. |
| Service owner | Family Platform owner. |
| Data source | Prometheus only, provisioned in Grafana as `Prometheus` with UID `prometheus`. |
| Refresh interval | 30 seconds. |
| Metric dependencies | Node Exporter host metrics, cAdvisor container metrics, Prometheus self-metrics, and Prometheus target health. |
| Runtime system of record | Prometheus remains the metrics system of record; Grafana is the visualization layer. |
| Lifecycle state | Implementation-ready; not live until deployment evidence is reviewed. |
| Review cadence | Review during each PLAT-13.6 work package, after any Metrics Foundation change, and at least once per milestone while operational dashboards remain active. |
| Change control | Dashboard JSON, datasource provisioning, and dashboard provisioning changes must be reviewed through repository diff before live transfer. Manual UI edits are not authoritative. |
| Evidence requirements | Evidence must show Grafana version and digest, datasource provisioning, dashboard provisioning, HTTP availability, dashboard load behavior, persistence, reboot behavior, and Pi-hole and Prometheus non-regression. |

---

## Implementation Decision

PLAT-13.6.3 selects Option A: Grafana with repository-provisioned dashboards and data sources.

| Option | Summary | Commercial Architecture Alignment | Maintainability | Quality and Reduced Rework | Decision |
|--------|---------|-----------------------------------|-----------------|----------------------------|----------|
| A | Grafana with repository-provisioned dashboards and data sources | High | High | High | Approved |
| B | Grafana with manually imported community dashboards | Medium | Low | Medium | Rejected |
| C | Prometheus UI only | Low | Medium | Low | Rejected |

Rationale: repository-provisioned Grafana provides a repeatable dashboard environment, preserves Prometheus as the single governed metrics data source, and avoids undocumented manual dashboard construction.

---

## Target Architecture

```text
Browser
  |
  v
Grafana
  |
  v
Prometheus
  |-- Node Exporter
  |-- cAdvisor
  |-- Prometheus self-metrics
```

Grafana must not query Node Exporter or cAdvisor directly.

---

## Dashboard Inventory

| Dashboard | File | Purpose | Primary decisions supported |
|-----------|------|---------|-----------------------------|
| Platform Host Dashboard | `platform/compose/monitoring/grafana/dashboards/platform-host.json` | Beelink host availability, capacity, filesystem, disk, network, and scrape health. | Determine whether host health is affecting Pi-hole or monitoring. |
| Docker and Container Dashboard | `platform/compose/monitoring/grafana/dashboards/docker-containers.json` | Container visibility from cAdvisor through Prometheus. | Determine whether runtime or container resource use needs investigation. |
| Pi-hole Operations Dashboard | `platform/compose/monitoring/grafana/dashboards/pihole-operations.json` | Infrastructure operations view for Pi-hole without fabricating Pi-hole application analytics. | Check infrastructure conditions that affect customer-facing DNS and find recovery references. |
| Metrics Foundation Health Dashboard | `platform/compose/monitoring/grafana/dashboards/metrics-foundation-health.json` | Prometheus, scrape, target, ingestion, storage, and data freshness health. | Determine whether dashboard data and Metrics Foundation collection are trustworthy. |

---

## Metric Dependencies

Approved initial metrics include:

- `up`
- `node_boot_time_seconds`
- `node_cpu_seconds_total`
- `node_memory_MemTotal_bytes`
- `node_memory_MemAvailable_bytes`
- `node_filesystem_size_bytes`
- `node_filesystem_avail_bytes`
- `node_load1`
- `node_network_receive_bytes_total`
- `node_network_transmit_bytes_total`
- `node_disk_read_bytes_total`
- `node_disk_written_bytes_total`
- `container_last_seen`
- `container_cpu_usage_seconds_total`
- `container_memory_working_set_bytes`
- `container_network_receive_bytes_total`
- `container_network_transmit_bytes_total`
- `container_fs_usage_bytes`
- `scrape_duration_seconds`
- `scrape_samples_scraped`
- `prometheus_tsdb_head_series`
- `prometheus_tsdb_storage_blocks_bytes`

Container-name labels from cAdvisor must be verified during live validation. Panels that depend on container-name labels must clearly show `No data` when the label is unavailable.

Temperature is included only if already exposed by available metrics. PLAT-13.6.3 does not add a new temperature exporter.

---

## Limitations

- Pi-hole query counts, blocked percentages, domain rankings, client analytics, DNS probe results, and admin UI probe results are not available unless future governed Prometheus scraping adds them.
- The Pi-hole Operations Dashboard is an infrastructure operations dashboard, not a Pi-hole application analytics replacement.
- Grafana does not provide alerting, notification delivery, backup assurance, restore validation, or update automation in PLAT-13.6.3.
- Dashboard thresholds are intentionally limited until alerting governance defines severity and escalation rules.
- Grafana image digest is recorded only after a governed live pull.

---

## Future Alert Relationship

These dashboards are designed to make future alerts understandable, but they do not implement alerts. Future alert work may add alert state panels after PLAT-13.6.5 approves alert rules, notification delivery, deliberate test firing, and evidence requirements.

---

## Future Evolution

Future dashboard contracts should reuse this structure and add only metrics that are actually exported and governed. Candidate future dashboards include:

- Home Assistant operations.
- MQTT broker operations.
- Ollama local AI operations.
- FFFA runtime services.
- Backup health.
- Alerting health.
- Additional Platform hosts.

---

## Related Documents

- [ADR-007 - Governed Operations and Observability](../architecture/decisions/ADR-007-Governed-Operations-and-Observability.md)
- [Platform Operations and Observability Specification](Platform_Operations_Observability_Specification.md)
- [Operations Dashboard Runbook](../operations/Operations_Dashboard_Runbook.md)
- [Operations Dashboard Evidence Template](../operations/Operations_Dashboard_Evidence_Template.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial PLAT-13.6.3 governed dashboard contract and inventory. |
