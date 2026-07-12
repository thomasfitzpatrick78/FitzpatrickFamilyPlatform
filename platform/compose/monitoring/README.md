# Platform Monitoring Compose Template

**Status:** Active PLAT-13.6.2 Metrics Foundation configuration with PLAT-13.6.3B implementation-ready container metrics replacement.

This directory contains repository-managed configuration for the active Metrics Foundation, the PLAT-13.6.3 Grafana Operations Dashboard package, and the PLAT-13.6.3B restricted Docker API proxy plus OpenTelemetry Docker Stats Collector preparation.

Live deployment evidence is recorded in [Metrics Foundation Implementation Evidence](../../../docs/operations/Metrics_Foundation_Implementation_Evidence.md).

---

## Components

| Component | Image | Purpose |
|-----------|-------|---------|
| Grafana | `grafana/grafana:13.1.0` | Governed dashboards provisioned from repository-managed files; implementation-ready, not yet deployed |
| Prometheus | `prom/prometheus:v2.55.1` | Metrics collection, local retention, target health |
| Node Exporter | `prom/node-exporter:v1.8.2` | Beelink/Linux host metrics |
| cAdvisor | `gcr.io/cadvisor/cadvisor:v0.49.1` | Active/degraded host and cgroup scrape target; not authoritative for named Docker-container metrics under Docker 29/containerd |
| Docker API proxy | `tecnativa/docker-socket-proxy:0.4.2` | Implementation-ready restricted Docker API proxy; not deployed |
| OTel Docker Stats Collector | `otel/opentelemetry-collector-contrib:0.156.0` | Implementation-ready Docker Stats receiver and internal Prometheus endpoint; not deployed |

Image digests were recorded during live Gate 9 evidence capture after images were pulled on the Beelink.

Image sources:

- `grafana/grafana` is the official Grafana Open Source image published by Grafana Labs. Version `13.1.0` is selected as the initial explicit stable tag for PLAT-13.6.3 because the current Grafana documentation identifies v13.1 as the latest documentation line and directs new Docker users to the `grafana/grafana` repository.
- `prom/prometheus` is the official Prometheus image published by the Prometheus project on Docker Hub.
- `prom/node-exporter` is the official Node Exporter image published by the Prometheus project on Docker Hub.
- `gcr.io/cadvisor/cadvisor` is the cAdvisor image published by the cAdvisor project.
- `tecnativa/docker-socket-proxy` is the selected restricted Docker API proxy image from the Tecnativa project.
- `otel/opentelemetry-collector-contrib` is the selected OpenTelemetry Collector Contrib image for the Docker Stats receiver.

No image uses `latest`, rolling, prerelease, `main`, `master`, `edge`, or another uncontrolled tag.

Grafana, Docker API proxy, and OTel Collector digest capture is intentionally deferred until governed live pulls on the Beelink. Future image updates must follow the controlled update workflow; unattended updates are not approved.

---

## Network Boundary

- Grafana is configured to bind to `192.168.50.127:3000` when implemented.
- Prometheus binds to `192.168.50.127:9090`.
- Prometheus does not bind to every host interface.
- Node Exporter is exposed only on the internal `platform-monitoring` Docker network.
- cAdvisor is exposed only on the internal `platform-monitoring` Docker network.
- cAdvisor is not published on host TCP `8080`, which belongs to Pi-hole admin.
- Docker API proxy exposes only internal TCP `2375` on `platform-monitoring`; it has no host-published port.
- OTel Docker Stats exposes only internal TCP `9464` and health TCP `13133` on `platform-monitoring`; it has no host-published port.
- OTel does not mount the Docker socket. Docker socket access is restricted to the proxy with a read-only mount.
- Grafana joins the existing `platform-monitoring` Docker network and reads Prometheus at `http://prometheus:9090`.
- Grafana must not query Node Exporter, cAdvisor, Docker API proxy, or OTel directly.
- No monitoring interface is approved for Internet exposure.

Grafana plugin preinstall and plugin auto-update are disabled through `GF_PLUGINS_PREINSTALL_DISABLED=true` and `GF_PLUGINS_PREINSTALL_AUTO_UPDATE=false`.

cAdvisor is active and scrapeable, but PLAT-13.6.3A records degraded Docker-container discovery under Docker 29.6.1 with the containerd-backed image store. Dashboards must not treat cAdvisor target health as complete Docker-container observability.

PLAT-13.6.3B prepares OTel Docker Stats through a restricted Docker API proxy. The replacement remains implementation-ready only until live proxy denial proof, OTel metric inventory, Pi-hole identity proof, persistence validation, and reboot validation pass.

---

## Persistence

Prometheus runtime data is stored at:

```text
/platform/data/monitoring/prometheus
```

Grafana runtime data is stored at:

```text
/platform/data/monitoring/grafana
```

Mutable runtime data must not be stored in this Git repository.

The Prometheus container runs as UID/GID `65534:65534`. The live runbook creates `/platform/data/monitoring/prometheus` with that ownership and mode `0750`. The directory must not be globally writable.

The Grafana container runs as UID/GID `472:472`. The live runbook creates `/platform/data/monitoring/grafana` with that ownership and mode `0750`. The directory must not be globally writable.

---

## Secrets

Grafana requires an administrator password.

Copy `.env.example` to `.env` on the Beelink. Do not commit `.env`.

Set `GRAFANA_ADMIN_PASSWORD` only in the Beelink-local `.env` file. Store the value in Tom's password manager. Do not paste the password into ChatGPT or Codex and do not record it in evidence.

---

## Grafana Provisioning

PLAT-13.6.3 provisions:

- Prometheus datasource: `grafana/provisioning/datasources/prometheus.yml`.
- Dashboard provider: `grafana/provisioning/dashboards/dashboards.yml`.
- Platform Host Dashboard: `grafana/dashboards/platform-host.json`.
- Docker and Container Dashboard: `grafana/dashboards/docker-containers.json`.
- Pi-hole Operations Dashboard: `grafana/dashboards/pihole-operations.json`.
- Metrics Foundation Health Dashboard: `grafana/dashboards/metrics-foundation-health.json`.

Dashboards refresh every 30 seconds and use the provisioned Prometheus datasource. Manual dashboard edits in the Grafana UI are not authoritative.

Do not place `.gitkeep` files in scanned Grafana provisioning subdirectories. Empty provisioning directories such as `alerting` or `plugins` should be created live only when an approved valid provisioning file is needed.

---

## cAdvisor Privilege Review

| Setting | Value | Required reason | Read-only | Narrower alternative | Residual risk |
|---------|-------|-----------------|-----------|--------------------|---------------|
| `/` -> `/rootfs` | volume mount | Host filesystem metadata for container and filesystem metrics | Yes | Mount only selected paths, but cAdvisor expects host root visibility for complete Docker metrics | Exposes host path names and metadata to cAdvisor |
| `/var/run` -> `/var/run` | volume mount | Runtime metadata used by cAdvisor to inspect containers | Yes | Mount only Docker runtime paths if live validation proves sufficient | Exposes runtime metadata to cAdvisor |
| `/sys` -> `/sys` | volume mount | Kernel, cgroup, CPU, and memory metrics | Yes | No narrower reliable path for cgroup visibility is approved yet | Exposes kernel and cgroup metadata |
| `/var/lib/docker` -> `/var/lib/docker` | volume mount | Docker container metadata and storage metrics | Yes | No narrower Docker storage path is approved yet | Exposes Docker metadata to cAdvisor |
| `/dev/disk` -> `/dev/disk` | volume mount | Disk labels and device metadata for storage metrics | Yes | Remove if live validation proves storage labels are not needed | Exposes disk label metadata |
| devices | none | No host device is approved for this implementation package | Not applicable | Already minimized | Some cAdvisor metrics may be unavailable without devices |
| capabilities | `cap_drop: ALL` | No Linux capability is approved for convenience access | Not applicable | Already minimized | Live validation must stop if required metrics fail |
| privileged | `false` | Privileged container access is not approved | Not applicable | Already minimized | Some cAdvisor metrics may be unavailable without privileged mode |
| namespace settings | Docker defaults | No host namespace sharing is approved | Not applicable | Already minimized | cAdvisor sees only what mounted paths and Docker metadata expose |
| user | image default | The image default is used because cAdvisor host-metadata access may require it | Not applicable | A fixed non-root user can be reviewed after live validation | Container process may run with more in-container file access than Prometheus |
| security option | `no-new-privileges:true` | Prevents privilege gain through exec transitions | Not applicable | Already minimized | Does not remove the host visibility created by mounts |

Residual risk: cAdvisor receives sensitive host visibility. It is not published to the LAN and should remain accessible only through Prometheus on the internal Docker network.

---

## Docker API Proxy and OTel Privilege Review

| Component | Boundary | Required reason | Residual risk |
|-----------|----------|-----------------|---------------|
| Docker API proxy | Read-only `/var/run/docker.sock` mount, internal network only, no host port | Allows Docker Stats receiver read/list/inspect/stat access without mounting the socket into OTel | Docker socket access can still imply host-control risk if proxy policy fails |
| OTel Docker Stats Collector | HTTP access only to `docker-api-proxy:2375`, no direct socket, internal Prometheus endpoint only | Collects Docker container metrics and exports them to Prometheus | Receiver maturity is alpha; exact metrics and labels require live proof |
| Prometheus | Scrapes `otel-docker-stats:9464` internally | Keeps Prometheus as the single metrics store and Grafana datasource | New target must not be treated as healthy before live deployment |

Proxy allowed capability groups are limited to `PING`, `VERSION`, `INFO`, and `CONTAINERS`. Mutation, management, auth, image, network, volume, service, swarm, exec, secret, config, system, task, and POST surfaces are disabled.

---

## Related Documents

- [Metrics Foundation Runbook](../../../docs/operations/Metrics_Foundation_Runbook.md)
- [Metrics Foundation Evidence Template](../../../docs/operations/Metrics_Foundation_Evidence_Template.md)
- [Metrics Foundation Implementation Evidence](../../../docs/operations/Metrics_Foundation_Implementation_Evidence.md)
- [Operations Dashboard Runbook](../../../docs/operations/Operations_Dashboard_Runbook.md)
- [Operations Dashboard Evidence Template](../../../docs/operations/Operations_Dashboard_Evidence_Template.md)
- [Platform Operations Dashboard](../../../docs/specifications/Platform_Operations_Dashboard.md)
- [Docker 29 Container Metrics Compatibility Assessment](../../../docs/architecture/Docker_29_Container_Metrics_Compatibility_Assessment.md)
- [Platform Operations and Observability Specification](../../../docs/specifications/Platform_Operations_Observability_Specification.md)
- [Privileged Infrastructure Integration Standard](../../../docs/governance/Privileged_Infrastructure_Integration_Standard.md)
- [Docker Container Metrics Replacement Runbook](../../../docs/operations/Docker_Container_Metrics_Replacement_Runbook.md)
- [Docker Container Metrics Replacement Evidence Template](../../../docs/operations/Docker_Container_Metrics_Replacement_Evidence_Template.md)
