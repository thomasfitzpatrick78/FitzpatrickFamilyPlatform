# Docker 29 Container Metrics Compatibility Assessment

**Document Version:** 1.2

**Status:** Architecture Gatekeeper review

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6.3A - Docker 29 Container Metrics Compatibility Correction

---

## Purpose

This assessment records the Docker 29 container metrics compatibility defect found during Operations Dashboard validation and defines the governed stop point before selecting a replacement or supplemental container metrics source.

Container Metrics is the governed capability. Docker is the current implementation context, and the PLAT-13.6.3B proxy plus OTel Docker Stats design is a replaceable implementation component, not a permanent runtime-specific product boundary.

---

## Verified Platform Baseline

| Field | Value |
|-------|-------|
| Hostname | `beelink` |
| IPv4 | `192.168.50.127` |
| Operating system | Ubuntu Server 26.04 LTS |
| Docker Engine | `29.6.1` |
| Docker Compose | `v5.3.1` |
| Docker root | `/var/lib/docker` |
| Storage driver | `overlayfs` |
| Driver type | `io.containerd.snapshotter.v1` |
| cgroup driver | `systemd` |
| cgroup version | `2` |
| Platform root | `/platform` |
| cAdvisor image | `gcr.io/cadvisor/cadvisor:v0.49.1` |

Docker 29 with the containerd-backed image store is the governed Platform baseline. The correction package does not change Docker storage, Docker daemon configuration, Pi-hole, DNS, or router state.

Future Container Metrics implementations may use Podman, containerd, Kubernetes, Incus, or LXC if a later architecture decision approves the runtime, security model, collector, Prometheus integration, and evidence expectations.

---

## Observed Defect

Prometheus can scrape the cAdvisor target, and cAdvisor exposes host and systemd cgroup metrics. However, Docker-container-level series are not reliably created under the current Docker 29/containerd-backed image store.

Observed behavior:

- `up{job="cadvisor"}` is `1`.
- Host and systemd cgroup metrics are present.
- Friendly Docker container names and Compose service labels are not reliable.
- Docker container cgroup ID queries returned no useful Docker-container result.
- Dashboard counts based on broad `container_last_seen` queries reflect host/systemd cgroups rather than actual Docker containers.
- Panels such as CPU by container and Pi-hole container resource use returned `No data` or could not be trusted.

Concise log evidence:

```text
failed to identify the read-write layer ID for container
```

cAdvisor looked for legacy Docker layer paths similar to:

```text
/rootfs/var/lib/docker/image/overlayfs/layerdb/mounts/<container-id>/mount-id
```

Those paths do not exist for the verified Docker 29 `io.containerd.snapshotter.v1` image-store model.

---

## Dashboard Impact

| Dashboard | Impact |
|-----------|--------|
| Docker and Container Dashboard | cAdvisor target health remains meaningful, but Docker-container discovery and friendly container resource panels are not validated. |
| Pi-hole Operations Dashboard | Pi-hole container-specific CPU, memory, and presence panels cannot be trusted until a compatible container metrics source is proven. |
| Metrics Foundation Health Dashboard | cAdvisor scrape health must be shown separately from Docker-container observability completeness. |

No dashboard may claim current access to Pi-hole query totals, blocking percentages, client analytics, domain rankings, DNS probe status, admin-page probe status, or Docker-container resource metrics that are not exported reliably.

---

## Operational Risk

- Operators could misread a healthy cAdvisor scrape target as complete Docker-container observability.
- A broad cgroup count can overstate Docker container count.
- Pi-hole container panels could imply validated resource visibility when the required labels are unavailable.
- Continuing persistence or reboot validation while the Docker dashboard is inaccurate would produce misleading evidence.

Accepted stop point: pause live dashboard validation after recording the compatibility defect. Resume only after repository review and explicit authorization.

---

## Rejected Production Change

Changing Docker storage backend, disabling the containerd image store, downgrading Docker, migrating to legacy overlay2 storage, deleting Docker data, or recreating Pi-hole is rejected.

Rationale:

- Docker 29 and the containerd-backed image store are the current governed Platform baseline.
- Storage migration would introduce production DNS risk.
- Pi-hole is active and healthy and must not be modified to satisfy dashboard convenience.
- A metrics compatibility defect should be solved at the metrics architecture layer, not by weakening the production runtime baseline.

---

## Architecture Options

| Option | Summary | Commercial Architecture Alignment | Maintainability | Quality / Rework Risk | Compatibility State | Decision |
|--------|---------|-----------------------------------|-----------------|-----------------------|--------------------|----------|
| A1 | Docker Engine metrics endpoint plus compatible exporter or collector | High | Medium | Medium | Docker daemon Prometheus metrics are documented; container identity/resource coverage needs live proof | Recommended candidate |
| A2 | Containerd-native metrics or collector | Medium | Medium | Medium | Requires proof that container identity and resource metrics are available without excessive host access | Candidate for investigation |
| A3 | Retain cAdvisor for limited cgroup signals and add separate Docker metadata/metrics source | High | Medium | Low to Medium | Matches current evidence and preserves Prometheus as central source; replacement source needs proof | Recommended architecture pattern |
| B | Keep current cAdvisor limitations and reduce dashboard scope only | Medium | High | High | Verified fallback, but does not meet Docker-container observability objective | Fallback only |
| C | Change Docker storage backend or downgrade Docker | Low | Low | High | Would likely restore legacy cAdvisor assumptions but creates production risk | Rejected |

### Option A1 - Docker Engine Metrics and Compatible Exporter or Collector

Docker documents a daemon Prometheus metrics endpoint configured through daemon settings such as `metrics-addr`. This provides engine-level visibility, but it is not by itself proven to supply stable container names, Compose service labels, or full container CPU, memory, network, filesystem, and last-seen/state coverage for this Platform.

OpenTelemetry Collector's Docker Stats receiver queries the Docker daemon container stats API and documents CPU, memory, network, and block I/O metrics. It requires Docker API access, defaulting to the Docker socket, and is documented as alpha for metrics. Docker Observer can discover running container endpoints through the Docker API and requires read access to the Docker socket. These are promising but require a security review, version pinning, and live proof before adoption.

Security model:

- Docker daemon metrics endpoint may require Docker daemon configuration and LAN/internal exposure controls.
- Docker API-based collectors require Docker socket or a narrowed proxy.
- A Docker socket proxy is preferred over direct broad socket access if this option proceeds.

### Option A2 - Containerd-Native Metrics or Collector

A containerd-native collector could align with the verified storage model. It must prove stable Docker container identity, cgroup v2 compatibility, Prometheus integration, and bounded host privileges. Any containerd socket access would require explicit Architecture Gatekeeper approval.

### Option A3 - Split cAdvisor and Docker Metadata/Metrics Source

cAdvisor can remain as a limited host/cgroup scrape target while a separate Docker-compatible metrics source supplies container identity and resource metrics. Prometheus remains the central governed data source, and Grafana continues to query only Prometheus.

This option best matches current evidence because it preserves the working cAdvisor scrape target without pretending it satisfies Docker-container observability.

### PLAT-13.6.3B Gatekeeper-Approved A3 Implementation Pattern

The approved repository-first implementation pattern is:

```text
Docker socket
  -> Restricted Docker API proxy
  -> OpenTelemetry Collector Contrib Docker Stats receiver
  -> internal Prometheus-format endpoint
  -> Prometheus
  -> Grafana dashboards
```

Node Exporter continues to feed host metrics directly to Prometheus. cAdvisor remains active but degraded and non-authoritative for named Docker-container metrics until the replacement is live-proven. Docker daemon Prometheus metrics remain a deferred optional gate and are not enabled by this package.

Selected pinned versions:

| Component | Image | Version | Source | Maturity / Support Note | Digest |
|-----------|-------|---------|--------|--------------------------|--------|
| Docker API proxy | `tecnativa/docker-socket-proxy:0.4.2` | `0.4.2` | Official Tecnativa docker-socket-proxy release history | Maintained restricted proxy pattern; requires live denial proof and periodic policy review | Pending governed live pull |
| OpenTelemetry Collector Contrib | `otel/opentelemetry-collector-contrib:0.156.0` | `0.156.0` | Official OpenTelemetry Collector releases | Collector Contrib release; Docker Stats receiver metrics maturity is alpha and requires live proof | Pending governed live pull |

The Docker Stats receiver is expected to expose container CPU, memory, network, and block I/O categories, but exact Prometheus metric names and labels must be inventoried live before dashboard PromQL is accepted.

### Option B - Reduced Dashboard Scope

The repository can keep cAdvisor target health and host/cgroup visibility while removing Docker-container resource claims. This is the immediate correction in PLAT-13.6.3A, but it does not complete the intended container observability objective.

### Option C - Docker Storage Migration or Downgrade

Rejected. This would modify the production runtime baseline and could affect Pi-hole. It is not compatible with the Architecture Gatekeeper decision to preserve Docker 29 and the containerd-backed image store.

---

## Required Future Proof

Before any replacement or supplement becomes active:

- Version must be pinned.
- Image source and digest policy must be governed.
- Network exposure must be LAN/internal-only.
- Docker socket or containerd socket access must be reviewed explicitly.
- Prometheus scrape configuration must be repository-managed.
- Dashboards must use only verified metrics.
- Evidence must prove Docker 29.6.1, cgroup v2, stable container identity, CPU, memory, network, filesystem, and last-seen/state behavior where claimed.
- Pi-hole non-regression must pass.

PLAT-13.6.3B adds repository-managed Compose, OTel, Prometheus, runbook, evidence, registry, dashboard, and test preparation only. It does not deploy the proxy or Collector, enable Docker daemon metrics, retire cAdvisor, or close PLAT-13.6.3.

Grafana and customer-facing applications must consume governed Container Metrics through Prometheus. They must not depend directly on Docker, Podman, containerd, Kubernetes, Incus, LXC, or runtime-specific APIs.

---

## Sources

- [Docker Docs - Collect Docker metrics with Prometheus](https://docs.docker.com/engine/daemon/prometheus/)
- [OpenTelemetry Collector Contrib - Docker Stats Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/dockerstatsreceiver)
- [OpenTelemetry Collector Contrib - Docker Observer Extension](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/observer/dockerobserver)
- [OpenTelemetry Collector Releases](https://github.com/open-telemetry/opentelemetry-collector-releases/releases)
- [Tecnativa docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy)
- [Tecnativa docker-socket-proxy Releases](https://github.com/Tecnativa/docker-socket-proxy/releases)

---

## Related Documents

- [ADR-007 - Governed Operations and Observability](decisions/ADR-007-Governed-Operations-and-Observability.md)
- [Platform Operations Dashboard](../specifications/Platform_Operations_Dashboard.md)
- [Operations Dashboard Runbook](../operations/Operations_Dashboard_Runbook.md)
- [Operations Dashboard Evidence Template](../operations/Operations_Dashboard_Evidence_Template.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Added EO-13.1 technology-neutral Container Metrics abstraction. |
| 1.1 | Recorded PLAT-13.6.3B approved A3 implementation pattern, selected versions, and live-proof gates. |
| 1.0 | Initial Docker 29/containerd cAdvisor compatibility assessment and option review. |
