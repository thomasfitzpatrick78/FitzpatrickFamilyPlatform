# Metrics Foundation Implementation Evidence

**Document Version:** 1.0

**Status:** Live deployment verified

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6.2 - Metrics Foundation

**Deployment Date:** 2026-07-12

---

## Summary

PLAT-13.6.2 Metrics Foundation has been deployed and validated on the Beelink Platform host.

This evidence records Prometheus, Node Exporter, and cAdvisor only. Grafana, alerts, notifications, backups, restore validation, controlled updates, and Milestone 13 closeout remain out of scope.

---

## Repository Baseline

| Item | Evidence |
|------|----------|
| Branch | `main` |
| Baseline commit | `58a461473756a484a98c14ca6716a5ee92b7bc9e` |
| Commit subject | `PLAT-13.6.2 - Metrics Foundation Implementation Package` |
| Repository state before live execution | Clean and synchronized |

---

## Host Identity

| Item | Evidence |
|------|----------|
| Hostname | `beelink` |
| IPv4 | `192.168.50.127` |
| MAC address | `78:55:36:09:D2:45` |
| Operating system | Ubuntu Server 26.04 LTS |
| Architecture | x86_64 |
| Docker | 29.6.1 |
| Docker Compose | v5.3.1 |
| Platform root | `/platform` |

---

## Deployed Components

| Component | Image | Image ID | Repo digest | Exposure |
|-----------|-------|----------|-------------|----------|
| Prometheus | `prom/prometheus:v2.55.1` | `sha256:2659f4c2ebb718e7695cb9b25ffa7d6be64db013daba13e05c875451cf51b0d3` | `prom/prometheus@sha256:2659f4c2ebb718e7695cb9b25ffa7d6be64db013daba13e05c875451cf51b0d3` | `192.168.50.127:9090` trusted LAN only |
| Node Exporter | `prom/node-exporter:v1.8.2` | `sha256:4032c6d5bfd752342c3e631c2f1de93ba6b86c41db6b167b9a35372c139e7706` | `prom/node-exporter@sha256:4032c6d5bfd752342c3e631c2f1de93ba6b86c41db6b167b9a35372c139e7706` | Internal `platform-monitoring` network only, port `9100` |
| cAdvisor | `gcr.io/cadvisor/cadvisor:v0.49.1` | `sha256:3cde6faf0791ebf7b41d6f8ae7145466fed712ea6f252c935294d2608b1af388` | `gcr.io/cadvisor/cadvisor@sha256:3cde6faf0791ebf7b41d6f8ae7145466fed712ea6f252c935294d2608b1af388` | Internal `platform-monitoring` network only, port `8080` |

---

## Network and Storage

| Item | Evidence |
|------|----------|
| Docker network | `platform-monitoring` |
| Network driver | bridge |
| Host networking | Not used |
| Internet exposure | None |
| Prometheus endpoint | `http://192.168.50.127:9090` |
| Prometheus retention | `15d` |
| Prometheus data path | `/platform/data/monitoring/prometheus` |
| Prometheus runtime user | UID/GID `65534:65534` |
| Prometheus data permissions | `0750` |
| Compose path | `/platform/compose/monitoring` |

---

## Pi-hole Baseline Before Deployment

| Check | Evidence |
|-------|----------|
| Container name | `pihole` |
| Container ID | `6840c56d6d1adcb11a094beb03097967390d8ab0b0068eb3a4ca98db6dc8d80c` |
| Restart count | `0` |
| Health | healthy |
| DNS resolution | PASS |
| Blocking | PASS, `doubleclick.net` returned `0.0.0.0` |
| Admin interface | reachable, HTTP `302` |
| DNS ports | `192.168.50.127` TCP/UDP `53` |
| Admin port | TCP `8080` |

---

## Gate Results

| Gate | Result | Evidence |
|------|--------|----------|
| Gate 1 - Preflight | PASS | Hostname, IP, Docker, Docker Compose, disk, port `9090`, Docker networks, and repository baseline verified. Disk: 98 GB total, 7.5 GB used, 86 GB available, 9% used. |
| Gate 2 - Pi-hole baseline | PASS | Pi-hole healthy, restart count `0`, container ID recorded, DNS and blocking passed, admin returned HTTP `302`. |
| Gate 3 - Port and path check | PASS | TCP `9090` free; monitoring paths reviewed; Prometheus data path created during implementation. |
| Gate 4 - Evidence preparation | PASS | Working evidence file created outside repository at `/tmp/Metrics_Foundation_Evidence_Working.md`. |
| Gate 5 - Directory and permissions | PASS | Monitoring directories created; Compose/docs owned by `tom:tom`; Prometheus data owned by `65534:65534`, mode `0750`; no globally writable monitoring directory. |
| Gate 6 - Governed file transfer | PASS | Compose, `.env.example`, README, Prometheus config, runbook, and evidence template transferred; no real repository `.env` transferred. |
| Gate 7 - Runtime environment | PASS | Beelink-local `.env` created with `MONITORING_BIND_IP=192.168.50.127` and `PROMETHEUS_RETENTION=15d`; no secrets. |
| Gate 8 - Compose validation | PASS | `docker compose config` passed; exposure, ports, network, persistent mount, no latest tags, and cAdvisor restrictions verified. |
| Gate 9 - Image pull and immutable evidence | PASS | Approved image IDs and repo digests captured. |
| Gate 10 - Runtime start | PASS | `prometheus`, `node-exporter`, `cadvisor`, and `pihole` active; Pi-hole remained healthy. |
| Gate 11 - Metrics and persistence | PASS | All targets up; host/container metrics present; Prometheus persistence survived container recreation. |
| Gate 12 - Reboot validation | PASS | Beelink rebooted, SSH returned, IPv4 unchanged, all containers restarted, Prometheus targets up, Pi-hole non-regression passed. |

---

## Prometheus Target Status

| Target | Status |
|--------|--------|
| `prometheus` | up |
| `node-exporter` | up |
| `cadvisor` | up |

The `up` query returned value `1` for all three jobs.

---

## Metric Evidence

| Metric | Evidence |
|--------|----------|
| `node_filesystem_size_bytes` | Host filesystem `/` reported for `/dev/mapper/ubuntu--vg-ubuntu--lv`, filesystem `ext4`, value `105089261568` bytes. |
| `node_boot_time_seconds` | Returned a valid host boot-time value. |
| `container_last_seen` | Returned host and runtime cgroup data, including `docker.service` and `containerd.service` evidence. |

---

## Persistence Evidence

| Item | Evidence |
|------|----------|
| Initial data size | `492K` |
| Data structures observed | `chunks_head`, `wal`, `queries.active`, `lock` |
| Pre-recreation timestamp | `2026-07-12T19:38:45Z` |
| Pre-recreation sample | Unix time `1783885125.063`, value `1` |
| Recreation command | `docker compose up -d --force-recreate --no-deps prometheus` |
| Persistent data deletion | Not performed |
| `docker compose down -v` | Not performed |
| Historical range query | Values returned from before recreation: `1783885095 -> 1`, `1783885110 -> 1`, `1783885125 -> 1`, `1783885140 -> 1`, `1783885155 -> 1` |
| Result | PASS |

---

## Reboot Evidence

| Check | Evidence |
|-------|----------|
| Beelink reboot | PASS |
| SSH returned | PASS |
| IPv4 after reboot | `192.168.50.127` |
| Containers restarted automatically | `prometheus`, `node-exporter`, `cadvisor`, `pihole` |
| cAdvisor health | healthy |
| Pi-hole health | healthy |
| Prometheus targets | all up |
| DNS after reboot | PASS |
| Blocking after reboot | PASS |
| Pi-hole admin after reboot | reachable, HTTP `302` |

---

## Pi-hole Non-Regression

| Check | Evidence |
|-------|----------|
| Final container ID | `6840c56d6d1adcb11a094beb03097967390d8ab0b0068eb3a4ca98db6dc8d80c` |
| Final restart count | `0` |
| Final health | healthy |
| Container ID unchanged | PASS |
| Restart count unchanged | PASS |
| DNS resolution | PASS |
| Blocking | PASS |
| Admin interface | reachable |
| Result | PASS |

---

## Warnings and Accepted Risks

- cAdvisor has sensitive host and container visibility through approved read-only mounts.
- Node Exporter and cAdvisor remain internal-only on the `platform-monitoring` Docker network.
- Grafana, alerts, backups, restore validation, and controlled updates are not implemented by PLAT-13.6.2.

---

## Stop Point Confirmation

Stop point honored after Metrics Foundation validation.

Do not treat this evidence as approval to deploy Grafana, configure alerts, begin backup implementation, perform controlled updates, create a tag, or close Milestone 13.
