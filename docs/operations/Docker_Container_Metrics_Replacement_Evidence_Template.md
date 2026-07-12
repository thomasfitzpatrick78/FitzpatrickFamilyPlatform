# Docker Container Metrics Replacement Evidence Template

**Document Version:** 1.0

**Status:** Template; no live evidence recorded.

---

## Repository Evidence

- Repository commit:
- Branch:
- Working tree state:
- Package version:
- Reviewer:
- Date:

---

## Host and Docker Baseline

- Hostname:
- IPv4:
- OS:
- Docker Engine:
- Docker Compose:
- Docker root:
- Storage driver:
- Driver type:
- cgroup driver/version:
- Platform root:

---

## Image Evidence

| Service | Image | Image ID | RepoDigest | Source | Result |
|---------|-------|----------|------------|--------|--------|
| Docker API proxy | `tecnativa/docker-socket-proxy:0.4.2` |  | pending live pull | official release |  |
| OTel Collector | `otel/opentelemetry-collector-contrib:0.156.0` |  | pending live pull | official release |  |

---

## Proxy Security Evidence

- Socket mounted only into proxy:
- Socket mount read-only:
- Host-published port absent:
- Allowed capabilities tested:
- Denied capabilities tested:
- POST disabled:
- Mutation denial proof:
- Residual risk accepted:

---

## Collector Evidence

- No direct Docker socket:
- No containerd socket:
- Docker Stats receiver endpoint:
- Collection interval:
- Prometheus exporter endpoint:
- Health extension endpoint:
- Memory limiter:
- External exporters absent:
- Logs/traces pipelines absent:

---

## Metric and Metadata Inventory

- Metric names emitted:
- Labels emitted:
- Resource attributes emitted:
- Container name identity:
- Compose project/service/container number:
- Pi-hole identification:
- CPU:
- Memory:
- Memory limit:
- Network receive/transmit:
- Block I/O:
- Uptime/start time/state:
- Sensitive metadata review:

---

## Prometheus and Dashboard Evidence

- Prometheus config validation:
- Existing targets preserved:
- New target `otel-docker-stats`:
- Dashboard files transferred:
- Docker container count:
- Named container presence:
- Pi-hole CPU/memory/network/block I/O panels:
- No fabricated Pi-hole application analytics:
- No host/systemd cgroup count presented as Docker container count:

---

## Non-Regression Evidence

- Pi-hole DNS resolution:
- Pi-hole blocking:
- Pi-hole admin UI:
- Prometheus historical data:
- Grafana access:
- Node Exporter:
- cAdvisor active/degraded status:
- Persistence/recreation result:
- Reboot result:

---

## Risks and Stop Point

- Residual risks:
- Open questions:
- Architecture Gatekeeper decision:
- Stop before Docker daemon metrics confirmed:
- Stop before cAdvisor retirement confirmed:
- Stop before PLAT-13.6.3 or Milestone 13 closeout confirmed:
