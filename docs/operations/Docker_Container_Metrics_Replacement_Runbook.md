# Docker Container Metrics Replacement Runbook

**Document Version:** 1.0

**Status:** Repository-prepared; do not execute without Architecture Gatekeeper approval.

**Scope:** PLAT-13.6.3B restricted Docker API proxy plus OpenTelemetry Docker Stats Collector.

---

## Safety Rules

- Run one command at a time and record evidence after each gate.
- Do not change Docker storage, Docker daemon configuration, Pi-hole, DNS, router, Raspberry Pi, Prometheus data, or Grafana data.
- Do not run `docker compose down -v`, `docker system prune`, broad volume removal, or storage-driver changes.
- Preserve the Beelink-local `.env` file.
- Stop at any unexpected result.

---

## Gate 1 - Repository and Host Preflight

Record branch, commit, working tree, Beelink hostname, IP address, Docker Engine `29.6.1`, Docker Compose `v5.3.1`, Docker root `/var/lib/docker`, storage driver `overlayfs`, driver type `io.containerd.snapshotter.v1`, cgroup version `2`, disk, memory, active containers, and existing `platform-monitoring` network.

Record current cAdvisor evidence: target up, Docker-container discovery degraded, friendly labels not reliable.

---

## Gate 2 - Customer and Platform Baseline

Record Pi-hole container ID, restart count, health, DNS resolution, blocking behavior, admin UI access, Prometheus target state, Grafana endpoint, Node Exporter state, cAdvisor state, and dashboard limitation evidence.

---

## Gate 3 - Evidence Preparation

Create evidence outside the repository. Record the repository commit and changed files. Do not capture secrets, `.env` values, passwords, tokens, or cookie/session data.

---

## Gate 4 - Governed File Transfer

Transfer only approved repository files under `/platform/compose/monitoring`. Preserve `/platform/data/monitoring/prometheus`, `/platform/data/monitoring/grafana`, and the Beelink-local `.env`. Inventory transferred files.

---

## Gate 5 - Compose Rendering

Run `docker compose config --quiet` from `/platform/compose/monitoring`.

Inspect non-secret rendered fields only:

- Docker socket mounted only into `docker-api-proxy`.
- Docker socket mount is read-only.
- `otel-docker-stats` has no Docker or containerd socket.
- `docker-api-proxy` and `otel-docker-stats` have no host-published ports.
- Existing Prometheus, Grafana, Node Exporter, and cAdvisor bindings remain unchanged.
- No service uses host networking or privileged mode.

---

## Gate 6 - Image Pull and Immutable Evidence

Pull only `tecnativa/docker-socket-proxy:0.4.2` and `otel/opentelemetry-collector-contrib:0.156.0`. Record image IDs and `RepoDigests`. Do not pull floating tags and do not restart existing services.

---

## Gate 7 - Start Restricted Proxy Only

Start only `docker-api-proxy`. Confirm it has no host-published port. Validate internal `/_ping`, `/version`, `/info`, and required container read/stat surfaces from the monitoring network.

Validate denied behavior without changing production state. Do not send a mutation request that could alter containers merely to prove denial. If safe denial proof is not possible, stop and escalate.

Verify Pi-hole, Prometheus, Grafana, Node Exporter, and cAdvisor non-regression.

---

## Gate 8 - Start OpenTelemetry Collector Only

Start only `otel-docker-stats`. Inspect logs for proxy connection and receiver errors. Confirm the Collector has no direct socket, no host-published port, and exposes only the internal Prometheus endpoint.

---

## Gate 9 - Metric Inventory

Before dashboard query finalization, inventory actual metric names, labels, and resource attributes from `job="otel-docker-stats"`.

Required proof:

- Docker container count reflects actual Docker containers, not host/systemd cgroups.
- Container names and Compose labels identify Pi-hole.
- CPU, memory, memory limit where available, network receive/transmit, block I/O, uptime/start time or state where available.
- No environment variables, command arguments, secrets, raw metadata, or sensitive host paths appear.

---

## Gate 10 - Prometheus Scrape Integration

Validate Prometheus configuration, reload or restart only Prometheus as governed, and confirm existing historical data and targets remain intact. Confirm `otel-docker-stats` target state separately from cAdvisor.

---

## Gate 11 - Dashboard Query Finalization

Use the live metric inventory to finalize dashboard PromQL. Transfer only corrected dashboard files. Verify each required Docker and Pi-hole container panel. Do not use unsupported metrics, fake zeros, or host/systemd cgroup counts as Docker container counts.

---

## Gate 12 - Proxy Security Proof

Record allowed read API calls and denied mutation/management surfaces for exec, image, volume, network, swarm, service, secret, config, and container mutation operations. Verify no LAN exposure, no direct OTel socket, and no sensitive exported metadata.

---

## Gate 13 - Container Replacement and Persistence Test

Recreate only `docker-api-proxy` and `otel-docker-stats`. Do not delete volumes or platform data. Verify metrics return with stable identities and Pi-hole, Prometheus, Grafana, Node Exporter, and cAdvisor remain unaffected.

---

## Gate 14 - Beelink Reboot Validation

Only after all prior gates pass, reboot Beelink. Verify SSH, Pi-hole, DNS, blocking, Prometheus, Grafana, Node Exporter, cAdvisor, proxy, OTel, the Prometheus OTel target, Docker dashboards, and Pi-hole container panels.

---

## Gate 15 - Mandatory Stop Point

Complete the evidence template and stop before Docker daemon metrics, cAdvisor retirement, alerts, backups, updates, milestone closeout, or tagging.

---

## Rollback

Stop/remove `otel-docker-stats` only. If needed, stop/remove `docker-api-proxy` only. Remove the new Prometheus scrape job only if it causes target or configuration issues. Preserve Pi-hole, Docker Engine, Docker storage, `/platform`, Prometheus data, Grafana data, Node Exporter, cAdvisor, and Raspberry Pi rollback.

After rollback verify DNS, blocking, admin UI, prior Prometheus targets, and Grafana access.
