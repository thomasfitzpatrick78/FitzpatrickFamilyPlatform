# Platform Monitoring Compose Template

**Status:** Implementation-ready template for PLAT-13.6.2.

This directory contains repository-managed templates for the Metrics Foundation.

It does not mean monitoring has been deployed.

---

## Components

| Component | Image | Purpose |
|-----------|-------|---------|
| Prometheus | `prom/prometheus:v2.55.1` | Metrics collection, local retention, target health |
| Node Exporter | `prom/node-exporter:v1.8.2` | Beelink/Linux host metrics |
| cAdvisor | `gcr.io/cadvisor/cadvisor:v0.49.1` | Docker and container resource metrics |

Image digests are recorded during live Gate 9 evidence capture after images are pulled on the Beelink.

Image sources:

- `prom/prometheus` is the official Prometheus image published by the Prometheus project on Docker Hub.
- `prom/node-exporter` is the official Node Exporter image published by the Prometheus project on Docker Hub.
- `gcr.io/cadvisor/cadvisor` is the cAdvisor image published by the cAdvisor project.

No image uses `latest`, rolling, prerelease, `main`, `master`, `edge`, or another uncontrolled tag.

---

## Network Boundary

- Prometheus binds to `192.168.50.127:9090`.
- Prometheus does not bind to every host interface.
- Node Exporter is exposed only on the internal `platform-monitoring` Docker network.
- cAdvisor is exposed only on the internal `platform-monitoring` Docker network.
- cAdvisor is not published on host TCP `8080`, which belongs to Pi-hole admin.
- No monitoring interface is approved for Internet exposure.

---

## Persistence

Prometheus runtime data is stored at:

```text
/platform/data/monitoring/prometheus
```

Mutable runtime data must not be stored in this Git repository.

The Prometheus container runs as UID/GID `65534:65534`. The live runbook creates `/platform/data/monitoring/prometheus` with that ownership and mode `0750`. The directory must not be globally writable.

---

## Secrets

No secret is required for PLAT-13.6.2 Metrics Foundation.

Copy `.env.example` to `.env` on the Beelink. Do not commit `.env`.

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

## Related Documents

- [Metrics Foundation Runbook](../../../docs/operations/Metrics_Foundation_Runbook.md)
- [Metrics Foundation Evidence Template](../../../docs/operations/Metrics_Foundation_Evidence_Template.md)
- [Platform Operations and Observability Specification](../../../docs/specifications/Platform_Operations_Observability_Specification.md)
