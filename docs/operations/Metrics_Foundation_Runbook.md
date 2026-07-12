# Metrics Foundation Runbook

**Document Version:** 1.0

**Status:** Approved for user-executed implementation

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6.2 - Metrics Foundation

---

## Purpose

This runbook gives Tom the governed steps to install the first Metrics Foundation on the Beelink production Platform host.

The approved Metrics Foundation includes:

- Prometheus.
- Node Exporter.
- cAdvisor.
- Prometheus persistent storage.
- Local target health validation.
- Docker and host reboot validation.

This runbook stops after the Metrics Foundation is validated. It does not deploy dashboards, alerts, backups, controlled updates, or any unrelated service.

---

## Current State

| Item | Current value |
|------|---------------|
| Host | Beelink Mini S |
| Hostname | `beelink` |
| IP address | `192.168.50.127` |
| MAC address | `78:55:36:09:D2:45` |
| Operating system | Ubuntu Server 26.04 LTS |
| SSH administrator | `tom` |
| Docker | Installed, enabled, and active |
| Existing production service | Pi-hole Docker service |
| Pi-hole Compose path | `/platform/compose/pihole` |
| Pi-hole data path | `/platform/data/pihole/etc-pihole` |
| Pi-hole DNS | TCP/UDP `53` on `192.168.50.127` |
| Pi-hole admin UI | TCP `8080` |
| Rollback host | Raspberry Pi at `192.168.50.67` |

---

## Planned State

| Component | Image | Planned exposure |
|-----------|-------|------------------|
| Prometheus | `prom/prometheus:v2.55.1` | `192.168.50.127:9090` |
| Node Exporter | `prom/node-exporter:v1.8.2` | Internal Docker network only |
| cAdvisor | `gcr.io/cadvisor/cadvisor:v0.49.1` | Internal Docker network only |

Prometheus data is stored at `/platform/data/monitoring/prometheus`.

The monitoring Compose files are stored at `/platform/compose/monitoring`.

---

## Image and Privilege Baseline

Approved images:

| Component | Image tag | Source | Digest status |
|-----------|-----------|--------|---------------|
| Prometheus | `prom/prometheus:v2.55.1` | Official Prometheus Docker Hub image | Captured after live pull |
| Node Exporter | `prom/node-exporter:v1.8.2` | Official Prometheus Docker Hub image | Captured after live pull |
| cAdvisor | `gcr.io/cadvisor/cadvisor:v0.49.1` | cAdvisor project image | Captured after live pull |

Do not replace these with `latest`, rolling, prerelease, `main`, `master`, `edge`, or any other uncontrolled tag.

cAdvisor privilege choices:

| Setting | Value | Why it is required | Read-only | Narrower alternative | Residual risk |
|---------|-------|--------------------|-----------|--------------------|---------------|
| `/` -> `/rootfs` | volume mount | Lets cAdvisor read host filesystem metadata | Yes | Selected host paths only, if later validated | Host metadata visible to cAdvisor |
| `/var/run` -> `/var/run` | volume mount | Lets cAdvisor read runtime metadata | Yes | Selected runtime paths only, if later validated | Runtime metadata visible to cAdvisor |
| `/sys` -> `/sys` | volume mount | Lets cAdvisor read kernel and cgroup metrics | Yes | No narrower approved path yet | Kernel and cgroup metadata visible |
| `/var/lib/docker` -> `/var/lib/docker` | volume mount | Lets cAdvisor read Docker container metadata | Yes | Selected Docker paths only, if later validated | Docker metadata visible |
| `/dev/disk` -> `/dev/disk` | volume mount | Lets cAdvisor read disk label metadata | Yes | Remove later if live metrics remain complete | Disk label metadata visible |
| devices | none | No host device is approved | Not applicable | Already minimized | Some metrics may be unavailable |
| capabilities | `cap_drop: ALL` | No Linux capability is approved for convenience access | Not applicable | Already minimized | Stop if required metrics fail |
| privileged | `false` | Privileged mode is not approved | Not applicable | Already minimized | Some metrics may be unavailable |
| namespace settings | Docker defaults | Host namespaces are not approved | Not applicable | Already minimized | Visibility comes from mounts only |
| user | image default | cAdvisor host-metadata access may require the image default | Not applicable | Fixed non-root user requires future review | In-container access is broader than Prometheus |
| security option | `no-new-privileges:true` | Prevents privilege gain through exec transitions | Not applicable | Already minimized | Does not remove mount visibility |

Residual risk: cAdvisor has sensitive host and container visibility. It is not published to the LAN and must remain reachable only by Prometheus on the internal Docker network.

---

## Scope Boundaries

Do not perform any of these actions during this runbook:

- Do not deploy Grafana.
- Do not deploy Alertmanager.
- Do not configure alert notifications.
- Do not create backup automation.
- Do not run restore execution.
- Do not deploy Watchtower or unattended updates.
- Do not change Pi-hole configuration.
- Do not change router DNS.
- Do not change ASUS router settings except viewing existing state if needed.
- Do not change Raspberry Pi configuration.
- Do not expose monitoring to the Internet.
- Do not add remote monitoring outside the trusted home network.
- Do not perform unrelated hardening.
- Do not close the milestone.
- Do not create a release tag.

---

## Gate 1 - Preflight Safety Check

Run these commands from Tom's MacBook:

```bash
ssh tom@192.168.50.127 'hostname && hostname -I && docker --version && docker compose version'
```

Expected result:

- Hostname includes `beelink`.
- IP address includes `192.168.50.127`.
- Docker version prints successfully.
- Docker Compose version prints successfully.

Run:

```bash
ssh tom@192.168.50.127 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
```

Expected result:

- The `pihole` container is running.
- Pi-hole DNS shows TCP/UDP `53`.
- Pi-hole admin uses TCP `8080`.
- No existing Prometheus, Node Exporter, or cAdvisor container is running.

PASS:

- The host identity and Docker baseline match the table above.
- Pi-hole is running.

STOP:

- The Beelink IP is not `192.168.50.127`.
- Docker is unavailable.
- Pi-hole is not running.
- A monitoring stack already exists and was not expected.

---

## Gate 2 - Pi-hole Non-Regression Baseline

Record the current Pi-hole restart count:

```bash
ssh tom@192.168.50.127 'docker inspect -f "{{.RestartCount}}" pihole'
```

Record the current Pi-hole container ID:

```bash
ssh tom@192.168.50.127 'docker inspect -f "{{.Id}}" pihole'
```

Record Pi-hole health:

```bash
ssh tom@192.168.50.127 'docker inspect -f "{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}" pihole'
```

Check DNS from the Beelink:

```bash
ssh tom@192.168.50.127 'dig @192.168.50.127 example.com +short'
```

Check a known blocked domain:

```bash
ssh tom@192.168.50.127 'dig @192.168.50.127 doubleclick.net +short'
```

Check the Pi-hole admin page from the Beelink:

```bash
ssh tom@192.168.50.127 'curl -I --max-time 5 http://192.168.50.127:8080/admin/ | head -n 1'
```

Expected result:

- The restart count prints a number.
- The container ID prints a long identifier.
- The health command prints `healthy` or `running`, depending on the container health configuration.
- The `example.com` lookup returns one or more IP addresses.
- The blocked-domain result should match the existing Pi-hole behavior for the home network.
- The admin-page check returns an HTTP response line.

PASS:

- Pi-hole answers DNS before monitoring is installed.
- Pi-hole admin page is reachable before monitoring is installed.

STOP:

- Pi-hole does not answer DNS.
- The `pihole` container restarted unexpectedly during the check.
- Pi-hole admin page is not reachable.

---

## Gate 3 - Port and Directory Check

Confirm Prometheus port `9090` is not already in use:

```bash
ssh tom@192.168.50.127 'ss -ltnp | grep ":9090 " || true'
```

Expected result:

- No active listener is printed.

Check whether monitoring directories already exist:

```bash
ssh tom@192.168.50.127 'ls -ld /platform/compose/monitoring /platform/data/monitoring/prometheus 2>/dev/null || true'
```

Expected result:

- It is acceptable if the paths do not exist yet.
- If they exist, verify they are from this approved workstream.

PASS:

- Port `9090` is available.
- Existing monitoring paths are absent or expected.

STOP:

- Another service already uses port `9090`.
- Existing monitoring files are present and their source is unknown.

---

## Gate 4 - Prepare Local Evidence File

On Tom's MacBook, copy the evidence template into a dated working file outside the repository:

```bash
cp docs/operations/Metrics_Foundation_Evidence_Template.md /tmp/Metrics_Foundation_Evidence_Working.md
```

Fill in evidence as each gate is completed.

Expected result:

- The working evidence file exists locally.
- Evidence is recorded while the procedure is executed, not reconstructed later.

PASS:

- A working evidence file is ready.
- No working evidence file is created inside the Git repository.

STOP:

- The repository checkout is not at the approved PLAT-13.6.2 baseline.

---

## Gate 5 - Create Beelink Directories

Create the monitoring directories on the Beelink:

```bash
ssh tom@192.168.50.127 'sudo mkdir -p /platform/compose/monitoring/prometheus /platform/data/monitoring/prometheus /platform/documentation/operations'
```

Set ownership for the Compose and documentation directories:

```bash
ssh tom@192.168.50.127 'sudo chown -R tom:tom /platform/compose/monitoring /platform/documentation/operations'
```

Set safe ownership and permissions for Prometheus data. The approved Prometheus container runs as UID/GID `65534:65534`.

```bash
ssh tom@192.168.50.127 'sudo chown -R 65534:65534 /platform/data/monitoring/prometheus && sudo chmod 0750 /platform/data/monitoring/prometheus'
```

Validate the directory permissions:

```bash
ssh tom@192.168.50.127 'ls -ldn /platform/data/monitoring/prometheus'
```

Expected result:

- Commands finish without error.
- The numeric owner and group are `65534 65534`.
- The permission mode begins with `drwxr-x---`.

PASS:

- Directories exist and are writable by `tom`.
- Prometheus data directory is owned by UID/GID `65534:65534`.
- Prometheus data directory is not globally writable.

STOP:

- `/platform` is missing.
- Permission changes fail.
- Unexpected files appear under the new monitoring paths.
- The data directory shows mode `777` or any globally writable mode.

---

## Gate 6 - Transfer Repository-Managed Files

From Tom's MacBook, transfer the approved monitoring files:

```bash
rsync -av platform/compose/monitoring/ tom@192.168.50.127:/platform/compose/monitoring/
```

Transfer the runbook and evidence template:

```bash
rsync -av docs/operations/Metrics_Foundation_Runbook.md docs/operations/Metrics_Foundation_Evidence_Template.md tom@192.168.50.127:/platform/documentation/operations/
```

Expected result:

- `compose.yaml`, `.env.example`, `README.md`, and `prometheus/prometheus.yml` are copied.
- No real `.env` file is copied from the repository.

PASS:

- Files are present on the Beelink in `/platform/compose/monitoring`.

STOP:

- `rsync` reports unexpected deletion.
- A real `.env` file appears in the repository.
- Files are copied to the Pi-hole Compose directory by mistake.

---

## Gate 7 - Create Local Runtime Environment File

On the Beelink, create the runtime `.env` from the repository example:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && cp .env.example .env'
```

Confirm the values:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && cat .env'
```

Expected result:

- `MONITORING_BIND_IP=192.168.50.127`.
- `PROMETHEUS_RETENTION=15d`.

PASS:

- The runtime `.env` has only the approved non-secret values.

STOP:

- The bind IP is not `192.168.50.127`.
- The file contains secrets.

---

## Gate 8 - Render Compose Configuration

Validate the Docker Compose configuration without starting anything:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose config'
```

Expected result:

- The configuration renders successfully.
- Prometheus publishes only `192.168.50.127:9090`.
- Node Exporter has no host-published port.
- cAdvisor has no host-published port.
- cAdvisor is not published on host TCP `8080`.
- No monitoring service uses host networking.
- Services use the dedicated `platform-monitoring` Docker network.

PASS:

- Compose renders exactly as expected.

STOP:

- Compose fails to render.
- Prometheus is host-published on `0.0.0.0`.
- Prometheus is host-published on `[::]`.
- Node Exporter or cAdvisor has a LAN-published port.
- Any monitoring service uses host networking.
- Any monitoring service uses TCP/UDP `53`.
- Any image uses `latest`.

---

## Gate 9 - Pull Images and Record Image Evidence

Pull the approved images:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose pull'
```

Record image IDs and digests:

```bash
ssh tom@192.168.50.127 'docker image inspect prom/prometheus:v2.55.1 prom/node-exporter:v1.8.2 gcr.io/cadvisor/cadvisor:v0.49.1 --format "{{.RepoTags}} {{.Id}} {{.RepoDigests}}"'
```

Expected result:

- All three images pull successfully.
- Image IDs are printed.
- Repo digests are printed when available.

PASS:

- Image evidence is recorded in the working evidence file.

STOP:

- Any image fails to pull.
- A different image tag appears.
- Image evidence cannot be recorded.

---

## Gate 10 - Start Metrics Foundation

Start the monitoring stack:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose up -d'
```

Check container status:

```bash
ssh tom@192.168.50.127 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "prometheus|node-exporter|cadvisor|pihole"'
```

Expected result:

- `prometheus` is running.
- `node-exporter` is running.
- `cadvisor` is running.
- `pihole` is still running.
- Only Prometheus publishes `192.168.50.127:9090`.

PASS:

- All three monitoring containers are running.
- Pi-hole remains running.

STOP:

- Pi-hole stops or restarts unexpectedly.
- Prometheus does not start.
- Node Exporter does not start.
- cAdvisor does not start.
- cAdvisor publishes host TCP `8080`.

---

## Gate 11 - Validate Metrics and Persistence

Check Prometheus target health:

```bash
ssh tom@192.168.50.127 'curl -s http://192.168.50.127:9090/api/v1/targets | grep -E "prometheus|node-exporter|cadvisor|\"health\":\"up\""'
```

Check the `up` metric:

```bash
ssh tom@192.168.50.127 'curl -G -s http://192.168.50.127:9090/api/v1/query --data-urlencode "query=up"'
```

Check a host metric:

```bash
ssh tom@192.168.50.127 'curl -G -s http://192.168.50.127:9090/api/v1/query --data-urlencode "query=node_filesystem_size_bytes{mountpoint=\"/\",fstype!=\"rootfs\"}"'
```

Check host boot time:

```bash
ssh tom@192.168.50.127 'curl -G -s http://192.168.50.127:9090/api/v1/query --data-urlencode "query=node_boot_time_seconds"'
```

Check a container metric:

```bash
ssh tom@192.168.50.127 'curl -G -s http://192.168.50.127:9090/api/v1/query --data-urlencode "query=container_last_seen"'
```

Confirm Prometheus data exists:

```bash
ssh tom@192.168.50.127 'sudo du -sh /platform/data/monitoring/prometheus && ls -la /platform/data/monitoring/prometheus | head'
```

Record the current time-series sample before recreating Prometheus:

```bash
ssh tom@192.168.50.127 'date -u +"%Y-%m-%dT%H:%M:%SZ" && curl -G -s http://192.168.50.127:9090/api/v1/query --data-urlencode "query=up{job=\"prometheus\"}"'
```

Recreate only the Prometheus container:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose up -d --force-recreate --no-deps prometheus'
```

After Prometheus is running again, verify that data from before the recreate is still queryable. Replace `START_UNIX` and `END_UNIX` with a short window around the timestamp recorded before recreation.

```bash
ssh tom@192.168.50.127 'curl -G -s http://192.168.50.127:9090/api/v1/query_range --data-urlencode "query=up{job=\"prometheus\"}" --data-urlencode "start=START_UNIX" --data-urlencode "end=END_UNIX" --data-urlencode "step=15s"'
```

Do not run `docker compose down -v`. Do not delete `/platform/data/monitoring/prometheus`. Persistence validation means historical data survives a Prometheus container recreate; it is not the same as checking that the container restarted.

Expected result:

- Prometheus, Node Exporter, and cAdvisor targets are up.
- `up` returns series for the three monitoring jobs.
- `node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"}` returns host filesystem size for `/`.
- `node_boot_time_seconds` returns host boot time.
- `container_last_seen` returns container information.
- Prometheus data files exist under `/platform/data/monitoring/prometheus`.
- The post-recreate range query returns samples from the time before Prometheus was recreated.

PASS:

- All targets are up.
- Metrics are queryable.
- Prometheus data exists outside the Compose directory.
- Historical Prometheus samples remain queryable after only the Prometheus container is recreated.

STOP:

- Any target is down.
- Prometheus cannot query host or container metrics.
- Prometheus data is stored only inside a container.
- Historical samples from before the Prometheus recreate are not queryable.

---

## Gate 12 - Reboot Validation and Stop Point

Reboot the Beelink:

```bash
ssh tom@192.168.50.127 'sudo reboot'
```

Wait two minutes, then confirm SSH is back:

```bash
ssh tom@192.168.50.127 'hostname && uptime'
```

Check containers after reboot:

```bash
ssh tom@192.168.50.127 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "prometheus|node-exporter|cadvisor|pihole"'
```

Check Prometheus targets again:

```bash
ssh tom@192.168.50.127 'curl -s http://192.168.50.127:9090/api/v1/targets | grep -E "prometheus|node-exporter|cadvisor|\"health\":\"up\""'
```

Check Pi-hole DNS again:

```bash
ssh tom@192.168.50.127 'dig @192.168.50.127 example.com +short'
```

Check Pi-hole blocking again:

```bash
ssh tom@192.168.50.127 'dig @192.168.50.127 doubleclick.net +short'
```

Check the Pi-hole admin page again:

```bash
ssh tom@192.168.50.127 'curl -I --max-time 5 http://192.168.50.127:8080/admin/ | head -n 1'
```

Check Pi-hole health, container ID, and restart count again:

```bash
ssh tom@192.168.50.127 'docker inspect -f "{{.Id}} {{.RestartCount}} {{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}" pihole'
```

Expected result:

- SSH returns after reboot.
- `pihole`, `prometheus`, `node-exporter`, and `cadvisor` are running.
- Prometheus targets are up.
- Pi-hole still answers DNS.
- Pi-hole blocking behavior matches the baseline.
- Pi-hole admin page remains reachable.
- Pi-hole container ID and restart count are reviewed against the baseline.

PASS:

- Metrics Foundation survives Docker and host reboot.
- Pi-hole remains available.
- Pi-hole has no unexpected restart or container replacement.
- Evidence is complete.

STOP:

- The Beelink does not return after reboot.
- Pi-hole is unavailable.
- Monitoring containers do not restart.
- Prometheus targets stay down.
- Pi-hole admin page is unavailable.
- Pi-hole restart count or container ID changed unexpectedly.

This is the required stop point. Do not continue to Grafana, alerts, backups, controlled updates, milestone closeout, or release tagging.

---

## Rollback Procedure

Use rollback only if a STOP condition occurs or Architecture Review requests removal.

Stop monitoring containers:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose down'
```

Confirm Pi-hole is still running:

```bash
ssh tom@192.168.50.127 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep pihole'
```

Confirm DNS still works:

```bash
ssh tom@192.168.50.127 'dig @192.168.50.127 example.com +short'
```

Confirm blocking still works:

```bash
ssh tom@192.168.50.127 'dig @192.168.50.127 doubleclick.net +short'
```

Confirm Pi-hole admin is still reachable:

```bash
ssh tom@192.168.50.127 'curl -I --max-time 5 http://192.168.50.127:8080/admin/ | head -n 1'
```

Confirm SSH and Pi-hole health:

```bash
ssh tom@192.168.50.127 'hostname && docker inspect -f "{{.Id}} {{.RestartCount}} {{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}" pihole'
```

Optional cleanup requires separate Architecture Review approval before it is run:

```bash
ssh tom@192.168.50.127 'sudo rm -rf /platform/compose/monitoring /platform/data/monitoring/prometheus'
```

Do not run optional cleanup during normal rollback. Do not run optional cleanup if evidence preservation is required.

Do not run `docker system prune`. Do not run broad Docker volume deletion. Do not delete `/platform`. Do not uninstall Docker. Rollback affects only the `platform-monitoring` Compose project by default and preserves Prometheus data.

PASS:

- Monitoring is stopped.
- Pi-hole remains running.
- DNS remains available.
- Blocking remains available.
- Pi-hole admin remains reachable.
- SSH remains available.

STOP:

- Pi-hole is affected by rollback.
- DNS fails after monitoring is stopped.

---

## Security Notes

- Prometheus is reachable only at `192.168.50.127:9090` on the trusted home network.
- Node Exporter and cAdvisor are not published to the LAN.
- Prometheus does not mount the Docker socket.
- cAdvisor uses read-only host mounts and is isolated from LAN access.
- The runtime `.env` has no secrets and must not be committed.
- Remote monitoring and Internet exposure require separate approval.

---

## Completion Evidence

After Gate 12, update the evidence file with:

- Repository commit used.
- Image IDs and repo digests.
- Pi-hole before and after restart counts.
- Prometheus target status.
- Metric query outputs.
- Reboot validation result.
- Any warnings or unexpected behavior.

Keep the final evidence available for Architecture Review.
