# Metrics Foundation Evidence Template

**Document Version:** 1.0

**Status:** Template

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6.2 - Metrics Foundation

---

## Execution Summary

- Date:
- Executor:
- Beelink hostname:
- Beelink IP:
- Repository commit used:
- Monitoring Compose path:
- Result: PASS / STOP

---

## Image Evidence

| Component | Image Tag | Image ID | Repo Digest |
|-----------|-----------|----------|-------------|
| Prometheus | `prom/prometheus:v2.55.1` |  |  |
| Node Exporter | `prom/node-exporter:v1.8.2` |  |  |
| cAdvisor | `gcr.io/cadvisor/cadvisor:v0.49.1` |  |  |

---

## Preflight Evidence

- Hostname:
- IP address:
- Docker version:
- Compose version:
- Free disk space:
- Pi-hole health:
- Pi-hole container ID before:
- Pi-hole restart count before:
- DNS resolution result:
- Blocking result:
- Admin UI before:
- Port 9090 availability:
- Existing monitoring directories:
- Existing Docker networks:

---

## Deployment Evidence

- Directories created:
- Files transferred:
- Compose render result:
- Image pull result:
- Image IDs and RepoDigests captured:
- Container status:
- Prometheus browser check:
- Prometheus API target status:

---

## Metric Evidence

| Query | Expected Result | Observed Result |
|-------|-----------------|-----------------|
| `up` | series for prometheus, node-exporter, cadvisor |  |
| `node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"}` | host filesystem size for `/` |  |
| `node_boot_time_seconds` | host boot time |  |
| `container_last_seen` | cAdvisor container metric |  |

---

## Pi-hole Non-Regression

- Pi-hole health before:
- Pi-hole container ID before:
- Pi-hole restart count before:
- DNS resolution before:
- Blocking before:
- Admin UI before:
- Pi-hole health after:
- Pi-hole container ID after:
- Pi-hole restart count after:
- DNS resolution after:
- Blocking after:
- Admin UI after:

---

## Persistence and Reboot

- Prometheus data path before recreate:
- Timestamp before Prometheus recreate:
- Query result before Prometheus recreate:
- Prometheus-only recreate result:
- Historical query range after Prometheus recreate:
- Post-reboot SSH:
- Post-reboot monitoring containers:
- Post-reboot Prometheus targets:
- Post-reboot Pi-hole health:
- Post-reboot DNS:

---

## Warnings and Accepted Risks

- Warnings:
- Accepted risks:
- Rollback used: Yes / No

---

## Stop Point

Stop after Metrics Foundation validation.

Do not deploy Grafana, configure alerts, begin backup implementation, perform controlled updates, create a tag, or close Milestone 13.
