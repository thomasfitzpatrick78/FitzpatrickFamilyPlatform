# Platform Operations Dashboard

**Document Version:** 1.2

**Status:** Correction pending Architecture Gatekeeper review

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
| Metric dependencies | Node Exporter host metrics, cAdvisor scrape and host/cgroup metrics, Prometheus self-metrics, Prometheus target health, and planned OTel Docker Stats metrics after live inventory. |
| Runtime system of record | Prometheus remains the metrics system of record; Grafana is the visualization layer. |
| Lifecycle state | Deployed for validation; PLAT-13.6.3 closeout blocked. PLAT-13.6.3B Docker metrics replacement is repository-prepared but not live-proven. |
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
  |-- OTel Docker Stats (planned internal endpoint)
  |-- Prometheus self-metrics
```

Grafana must not query Node Exporter, cAdvisor, the Docker API proxy, or OTel directly.

---

## Dashboard Inventory

| Dashboard | File | Purpose | Primary decisions supported |
|-----------|------|---------|-----------------------------|
| Platform Host Dashboard | `platform/compose/monitoring/grafana/dashboards/platform-host.json` | Beelink host availability, capacity, filesystem, disk, network, and scrape health. | Determine whether host health is affecting Pi-hole or monitoring. |
| Docker and Container Dashboard | `platform/compose/monitoring/grafana/dashboards/docker-containers.json` | cAdvisor scrape health, explicit Docker-container discovery limitation, and provisional OTel replacement state. | Determine whether cAdvisor is scrapeable, whether OTel replacement is pending/live, and whether final container panels still require metric inventory. |
| Pi-hole Operations Dashboard | `platform/compose/monitoring/grafana/dashboards/pihole-operations.json` | Infrastructure operations view for Pi-hole without fabricating Pi-hole application analytics; provisional OTel container-panel acceptance criteria. | Check host conditions that affect customer-facing DNS and prepare for Pi-hole container identity proof. |
| Metrics Foundation Health Dashboard | `platform/compose/monitoring/grafana/dashboards/metrics-foundation-health.json` | Prometheus, scrape, target, ingestion, storage, data freshness, cAdvisor capability limitation, and planned OTel target state. | Determine whether dashboard data is fresh and whether cAdvisor target health is being confused with OTel container observability readiness. |

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

PLAT-13.6.3A finding: cAdvisor container-name labels are not reliable under Docker 29.6.1 with the containerd-backed image store. Current dashboards must not use broad cAdvisor cgroup counts as Docker container counts and must not show Pi-hole container resource panels as operational.

PLAT-13.6.3B prepares OTel Docker Stats through a restricted Docker API proxy. Only the `up{job="otel-docker-stats"}` target state is preconfigured as a concrete query. Container resource PromQL remains provisional until live metric inventory proves exact emitted names, labels, Pi-hole identity, and sensitive-metadata exclusion.

Temperature is included only if already exposed by available metrics. PLAT-13.6.3 does not add a new temperature exporter.

---

## Limitations

- Pi-hole query counts, blocked percentages, domain rankings, client analytics, DNS probe results, and admin UI probe results are not available unless future governed Prometheus scraping adds them.
- Docker-container CPU, memory, network, block I/O, and stable last-seen/state metrics are not available from the current cAdvisor deployment under Docker 29/containerd.
- OTel Docker Stats replacement panels must display pre-deployment `No data` honestly until the proxy, Collector, Prometheus scrape, and live metric inventory are validated.
- The Pi-hole Operations Dashboard is an infrastructure operations dashboard, not a Pi-hole application analytics replacement.
- Grafana does not provide alerting, notification delivery, backup assurance, restore validation, or update automation in PLAT-13.6.3.
- Dashboard thresholds are intentionally limited until alerting governance defines severity and escalation rules.
- Grafana image digest is recorded only after a governed live pull.
- PLAT-13.6.3 persistence and reboot validation remain incomplete until Docker-container dashboard accuracy is reviewed.

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
- [Docker 29 Container Metrics Compatibility Assessment](../architecture/Docker_29_Container_Metrics_Compatibility_Assessment.md)
- [Docker Container Metrics Replacement Runbook](../operations/Docker_Container_Metrics_Replacement_Runbook.md)
- [Docker Container Metrics Replacement Evidence Template](../operations/Docker_Container_Metrics_Replacement_Evidence_Template.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Added PLAT-13.6.3B provisional OTel Docker Stats dashboard migration strategy. |
| 1.1 | Added PLAT-13.6.3A Docker 29/containerd cAdvisor compatibility correction and dashboard limitation rules. |
| 1.0 | Initial PLAT-13.6.3 governed dashboard contract and inventory. |
