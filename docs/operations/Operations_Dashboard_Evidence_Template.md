# Operations Dashboard Evidence Template

**Document Version:** 1.0

**Status:** Template; PLAT-13.6.3A compatibility correction pending

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6.3 - Operations Dashboard

---

## Execution Summary

| Field | Evidence |
|-------|----------|
| Execution date | TBD |
| Executor | TBD |
| Repository branch | TBD |
| Repository commit | TBD |
| Architecture Gatekeeper approval reference | TBD |
| Beelink hostname | TBD |
| Beelink IP | TBD |
| Grafana endpoint | TBD |
| Result | TBD |
| Architecture Gatekeeper decision | TBD |

---

## Gate Evidence

| Gate | Result | Evidence location or notes |
|------|--------|----------------------------|
| Gate 1 - Repository and host preflight | TBD | TBD |
| Gate 2 - Pi-hole and Prometheus baseline | TBD | TBD |
| Gate 3 - Directory preparation | TBD | TBD |
| Gate 4 - File transfer | TBD | TBD |
| Gate 5 - Runtime `.env` | TBD | Confirm keys only; do not record password. |
| Gate 6 - Compose render | TBD | TBD |
| Gate 7 - Image pull and digest | TBD | TBD |
| Gate 8 - Start Grafana | TBD | TBD |
| Gate 9 - Provisioning validation | TBD | TBD |
| Gate 10 - Dashboard validation | TBD | TBD |
| Gate 11 - Grafana persistence | TBD | TBD |
| Gate 12 - Beelink reboot validation | TBD | TBD |
| Gate 13 - Evidence and stop point | TBD | TBD |

---

## Grafana Image Evidence

| Field | Value |
|-------|-------|
| Image source | `grafana/grafana` |
| Version tag | `13.1.0` |
| Image ID | TBD |
| RepoDigest | TBD |
| Pull command | `docker compose pull grafana` |
| Digest captured after live pull | TBD |

---

## Provisioning Evidence

| Item | Expected | Actual |
|------|----------|--------|
| Datasource name | `Prometheus` | TBD |
| Datasource UID | `prometheus` | TBD |
| Datasource URL | `http://prometheus:9090` | TBD |
| Datasource default | `true` | TBD |
| Dashboard folder | `Platform Operations` | TBD |
| Platform Host Dashboard | Present | TBD |
| Docker and Container Dashboard | Present | TBD |
| Pi-hole Operations Dashboard | Present | TBD |
| Metrics Foundation Health Dashboard | Present | TBD |

---

## Dashboard Validation

| Dashboard | Data appears | No broken panels | Known no-data behavior | Notes |
|-----------|--------------|------------------|------------------------|-------|
| Platform Host Dashboard | TBD | TBD | TBD | TBD |
| Docker and Container Dashboard | TBD | TBD | TBD | TBD |
| Pi-hole Operations Dashboard | TBD | TBD | TBD | TBD |
| Metrics Foundation Health Dashboard | TBD | TBD | TBD | TBD |

---

## Docker 29 Compatibility Evidence

| Field | Evidence |
|-------|----------|
| Docker version | TBD |
| Docker storage driver | TBD |
| Docker DriverStatus driver-type | TBD |
| Docker root | TBD |
| cgroup driver | TBD |
| cgroup version | TBD |
| cAdvisor version | `gcr.io/cadvisor/cadvisor:v0.49.1` |
| cAdvisor target up | TBD |
| cAdvisor compatibility result | TBD |
| Docker container discovery result | TBD |
| Container label availability | TBD |
| Host/systemd cgroup visibility | TBD |
| Dashboard accuracy result | TBD |
| Blocked gate | TBD |
| Accepted stop point | TBD |

Diagnostic queries:

```text
up{job="cadvisor"}
count(container_last_seen)
topk(20, container_last_seen)
count by (name) (container_last_seen{name=~".*(pihole|prometheus|node-exporter|cadvisor|grafana).*"})
```

---

## Pi-hole Non-Regression Evidence

| Check | Before Grafana | After Grafana | After reboot |
|-------|----------------|---------------|--------------|
| Container ID | TBD | TBD | TBD |
| Restart count | TBD | TBD | TBD |
| Health | TBD | TBD | TBD |
| DNS resolution | TBD | TBD | TBD |
| Blocking behavior | TBD | TBD | TBD |
| Admin UI | TBD | TBD | TBD |

---

## Prometheus Non-Regression Evidence

| Check | Before Grafana | After Grafana | After reboot |
|-------|----------------|---------------|--------------|
| Container ID | TBD | TBD | TBD |
| Restart count | TBD | TBD | TBD |
| Target states | TBD | TBD | TBD |
| Host metric query | TBD | TBD | TBD |
| Container metric query | TBD | TBD | TBD |
| Prometheus data path intact | TBD | TBD | TBD |

---

## Persistence Evidence

| Check | Result |
|-------|--------|
| Grafana data path exists at `/platform/data/monitoring/grafana` | TBD |
| Directory ownership is `472:472` | TBD |
| Directory mode is not globally writable | TBD |
| Login survives Grafana container recreation | TBD |
| Datasource survives recreation | TBD |
| Dashboards survive recreation | TBD |
| Approved persistent setting survives recreation | TBD |
| Grafana returns after Beelink reboot | TBD |

---

## Security Evidence

| Control | Evidence |
|---------|----------|
| No real password committed | TBD |
| `.env` exists only on Beelink | TBD |
| `.env` mode is `0600` | TBD |
| Grafana binds only to `192.168.50.127:3000` | TBD |
| No Internet exposure | TBD |
| No Docker socket mounted into Grafana | TBD |
| Grafana does not use host networking | TBD |
| Grafana drops Linux capabilities | TBD |
| Anonymous access disabled | TBD |
| Sign-up disabled | TBD |
| No unattended updates enabled | TBD |

---

## Stop Point Confirmation

Confirm no alerts, notification delivery, backups, restore validation, automated container updates, router changes, Pi-hole changes, Raspberry Pi changes, commit, push, tag, or milestone closeout occurred.

| Confirmation | Result |
|--------------|--------|
| No alerts implemented | TBD |
| No backups implemented | TBD |
| No restore validation executed | TBD |
| No automated updates enabled | TBD |
| No Pi-hole configuration changed | TBD |
| No router DNS changed | TBD |
| No Raspberry Pi changed | TBD |
| No commit, push, or tag made | TBD |

---

## Related Documents

- [Operations Dashboard Runbook](Operations_Dashboard_Runbook.md)
- [Platform Operations Dashboard](../specifications/Platform_Operations_Dashboard.md)
- [Platform Operations and Observability Specification](../specifications/Platform_Operations_Observability_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial PLAT-13.6.3 evidence template. |
