# Operations Dashboard Runbook

**Document Version:** 1.0

**Status:** Implementation-ready; not yet executed

**Milestone:** Milestone 13

**Workstream:** PLAT-13.6.3 - Operations Dashboard

---

## Purpose

This runbook gives Tom the governed gates to deploy and validate Grafana as the Platform operations dashboard layer on the Beelink.

Do not run these steps until the Architecture Gatekeeper approves the repository package.

This runbook does not deploy alerts, notification delivery, backups, restore validation, automated updates, Pi-hole changes, router DNS changes, ASUS router changes, Raspberry Pi changes, or Internet exposure.

---

## Approved Target

| Item | Value |
|------|-------|
| Host | `beelink` |
| Host IP | `192.168.50.127` |
| Grafana image | `grafana/grafana:13.1.0` |
| Grafana endpoint | `http://192.168.50.127:3000` |
| Grafana data path | `/platform/data/monitoring/grafana` |
| Grafana UID/GID | `472:472` |
| Monitoring Compose path | `/platform/compose/monitoring` |
| Monitoring network | `platform-monitoring` |
| Data source | Prometheus at `http://prometheus:9090` |
| Refresh interval | 30 seconds |

The Grafana image digest must be recorded only after the live Beelink pull.

---

## Gate 1 - Repository and Host Preflight

From Tom's MacBook, confirm the repository branch and working tree:

```bash
git branch --show-current
git status --short
```

Expected result:

- Branch is the approved implementation branch.
- The working tree contains only reviewed repository changes for PLAT-13.6.2 closeout and PLAT-13.6.3 preparation.

Confirm the Beelink identity:

```bash
ssh tom@192.168.50.127 'hostname && hostname -I && docker --version && docker compose version'
```

Confirm active containers and disk space:

```bash
ssh tom@192.168.50.127 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" && df -h /platform'
```

Confirm monitoring network and Grafana port availability:

```bash
ssh tom@192.168.50.127 'docker network inspect platform-monitoring >/dev/null && ss -ltnp | grep ":3000 " || true'
```

PASS:

- Hostname is `beelink`.
- IP includes `192.168.50.127`.
- Docker and Compose print versions.
- `platform-monitoring` exists.
- TCP 3000 is available.

STOP:

- Host identity is wrong.
- Docker or Compose is unavailable.
- TCP 3000 is already in use.
- The monitoring network is missing unexpectedly.

---

## Gate 2 - Pi-hole and Prometheus Baseline

Record Pi-hole state:

```bash
ssh tom@192.168.50.127 'docker inspect -f "{{.Id}} {{.RestartCount}} {{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}" pihole'
```

Validate DNS, blocking, and admin UI:

```bash
ssh tom@192.168.50.127 'dig @192.168.50.127 example.com +short'
ssh tom@192.168.50.127 'dig @192.168.50.127 doubleclick.net +short'
ssh tom@192.168.50.127 'curl -I --max-time 5 http://192.168.50.127:8080/admin/ | head -n 1'
```

Record Prometheus state:

```bash
ssh tom@192.168.50.127 'docker inspect -f "{{.Id}} {{.RestartCount}} {{.State.Status}}" prometheus'
```

Verify Prometheus targets and one host and container metric:

```bash
ssh tom@192.168.50.127 'curl -s "http://192.168.50.127:9090/api/v1/query?query=up"'
ssh tom@192.168.50.127 'curl -s "http://192.168.50.127:9090/api/v1/query?query=node_load1"'
ssh tom@192.168.50.127 'curl -s "http://192.168.50.127:9090/api/v1/query?query=container_last_seen"'
```

PASS:

- Pi-hole is healthy or running.
- DNS and blocking match the current home-network baseline.
- Pi-hole admin UI returns an HTTP response.
- Prometheus is running and all expected targets are up.
- Host and container metric queries return data.

STOP:

- Pi-hole or Prometheus is already unhealthy.
- Existing targets are down.
- Required baseline metrics are missing.

---

## Gate 3 - Directory Preparation

Create the Grafana data directory and set explicit ownership:

```bash
ssh tom@192.168.50.127 'sudo install -d -o 472 -g 472 -m 0750 /platform/data/monitoring/grafana'
```

PASS:

- `/platform/data/monitoring/grafana` exists.
- Owner is UID/GID `472:472`.
- Mode is not globally writable.

STOP:

- Directory ownership cannot be set.
- A command suggests `chmod 777`.

---

## Gate 4 - File Transfer

Transfer only the approved repository-managed monitoring files to `/platform/compose/monitoring`.

Preserve the existing Beelink `.env` file. Do not overwrite it.

After transfer, verify the inventory:

```bash
ssh tom@192.168.50.127 'find /platform/compose/monitoring/grafana -type f | sort'
```

Expected files:

- Datasource provisioning file.
- Dashboard provisioning file.
- Four dashboard JSON files.

STOP:

- A real `.env` would be overwritten.
- Prometheus files differ unexpectedly.
- Runtime Grafana database files appear in the repository-managed path.

---

## Gate 5 - Runtime .env

On the Beelink, create a dated backup of the existing `/platform/compose/monitoring/.env` before any edit:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && cp -p .env ".env.backup.$(date +%Y%m%d-%H%M%S)"'
```

Extend the existing Beelink-local `/platform/compose/monitoring/.env`; do not replace it blindly.

Retain these existing values:

```text
MONITORING_BIND_IP=192.168.50.127
PROMETHEUS_RETENTION=15d
```

Add only the required Grafana variables from `.env.example`.

Set `GRAFANA_ADMIN_PASSWORD` locally using a strong password stored in Tom's password manager. Do not paste the password into ChatGPT or Codex. Do not echo it into logs.

Use a local editor on the Beelink or another secret-safe edit method. Do not use a command that prints the password.

Set safe permissions:

```bash
ssh tom@192.168.50.127 'chmod 0600 /platform/compose/monitoring/.env && ls -l /platform/compose/monitoring/.env'
```

Confirm non-secret values and secret presence without printing the secret:

```bash
ssh tom@192.168.50.127 'awk -F= '\''$1=="MONITORING_BIND_IP"{print $1"="$2} $1=="PROMETHEUS_RETENTION"{print $1"="$2} $1=="GRAFANA_ADMIN_USER"{print $1"="$2} $1=="GRAFANA_ADMIN_PASSWORD"{print $1"=<set>"}'\'' /platform/compose/monitoring/.env'
```

PASS:

- `.env` exists only on the Beelink.
- File mode is `0600`.
- `MONITORING_BIND_IP=192.168.50.127` remains present.
- `PROMETHEUS_RETENTION=15d` remains present.
- `GRAFANA_ADMIN_PASSWORD` is present.

STOP:

- The existing `.env` backup was not created.
- The existing Prometheus values were removed or changed unintentionally.
- The password appears in terminal history, logs, repository content, or chat.

---

## Gate 6 - Compose Render

Render the Compose configuration:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose config'
```

Verify:

- Grafana image is `grafana/grafana:13.1.0`.
- Grafana publishes only `192.168.50.127:3000`.
- Prometheus binding remains `192.168.50.127:9090`.
- Node Exporter and cAdvisor remain internal-only.
- No DNS, Pi-hole, router, or Raspberry Pi setting appears.
- No secret value is copied into evidence.
- No `network_mode: host` appears.
- The network remains `platform-monitoring`.

STOP:

- Grafana binds to `0.0.0.0`, `[::]`, or an Internet-facing interface.
- Existing Metrics Foundation exposure changes unexpectedly.

---

## Gate 7 - Image Pull and Digest

Pull only Grafana:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose pull grafana'
```

Record image ID and RepoDigest:

```bash
ssh tom@192.168.50.127 'docker image inspect grafana/grafana:13.1.0 --format "{{.Id}} {{join .RepoDigests \" \"}}"'
```

PASS:

- Only the Grafana image is pulled.
- Digest is recorded in evidence.

STOP:

- Other monitoring images are pulled or changed unexpectedly.

---

## Gate 8 - Start Grafana

Start only Grafana:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose up -d grafana'
```

Verify active services:

```bash
ssh tom@192.168.50.127 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
ssh tom@192.168.50.127 'docker logs --tail 80 grafana'
curl -I --max-time 5 http://192.168.50.127:3000/login
```

PASS:

- Grafana starts.
- Pi-hole, Prometheus, Node Exporter, and cAdvisor remain running.
- Grafana login page responds.

STOP:

- Pi-hole or Prometheus restarts unexpectedly.
- Grafana logs show provisioning failure.

---

## Gate 9 - Provisioning Validation

Log in to Grafana through the browser at `http://192.168.50.127:3000`.

Validate:

- Data source `Prometheus` exists.
- `Prometheus` is default.
- Data source URL is `http://prometheus:9090`.
- The four dashboards exist in the `Platform Operations` folder.
- Dashboard panels load without broken-panel errors.
- Pi-hole dashboard does not claim query counts, blocked percentages, domain rankings, or client analytics.

PASS:

- Datasource and dashboards are provisioned from repository-managed files.

STOP:

- Manual-only datasource creation is required.
- Dashboard files do not provision.
- A dashboard fabricates unavailable Pi-hole analytics.

---

## Gate 10 - Dashboard Validation

Validate each dashboard:

- Platform Host Dashboard.
- Docker and Container Dashboard.
- Pi-hole Operations Dashboard.
- Metrics Foundation Health Dashboard.

For each dashboard record:

- Purpose.
- Expected panels.
- Whether data appears.
- Whether `No data` is understandable where metrics are unavailable.
- Whether refresh remains 30 seconds.
- Whether metric names match the current Prometheus scrape.

STOP:

- A panel depends on unsupported metrics without a clear limitation.
- A red or green interpretation implies governed thresholds that do not exist.

---

## Gate 11 - Grafana Persistence

This gate proves Grafana runtime database persistence separately from repository reprovisioning.

Before recreation:

- Log in as the Grafana administrator.
- Confirm the provisioned datasource and dashboards are visible.
- Record one safe database-backed preference or state when practical, such as the signed-in user's selected theme, home dashboard preference, or another harmless account preference.
- Do not create ungoverned dashboard source through the UI.

Recreate only Grafana. Do not delete Grafana data. Do not run `down -v`.

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose stop grafana && docker compose rm -f grafana && docker compose up -d grafana'
```

Verify:

- Administrator login still works with the same locally stored credential.
- The safe database-backed preference or state still exists.
- The provisioned Prometheus datasource still exists.
- The four dashboards still exist.
- Evidence distinguishes the database-backed preference from dashboards and datasource files that are restored by repository provisioning.

STOP:

- Grafana data is lost.
- A command proposes deleting `/platform/data/monitoring/grafana`.

---

## Gate 12 - Beelink Reboot Validation

Reboot only after Gates 1 through 11 pass:

```bash
ssh tom@192.168.50.127 'sudo reboot'
```

After SSH returns, verify:

- Pi-hole DNS, blocking, health, admin UI, container ID, and restart count.
- Prometheus status, restart count, targets, and sample metric queries.
- Node Exporter and cAdvisor scrape health.
- Grafana endpoint and dashboards.
- No unexpected Pi-hole container replacement.

STOP:

- DNS is down.
- Pi-hole restarted unexpectedly.
- Prometheus targets are down.
- Grafana does not return after reboot.

---

## Gate 13 - Evidence and Stop Point

Complete [Operations Dashboard Evidence Template](Operations_Dashboard_Evidence_Template.md).

Stop after evidence capture. Do not add alerts, backups, restore validation, controlled updates, milestone closeout, tag creation, or release claims.

---

## Rollback

If Grafana causes instability:

```bash
ssh tom@192.168.50.127 'cd /platform/compose/monitoring && docker compose stop grafana && docker compose rm -f grafana'
```

Preserve `/platform/data/monitoring/grafana` by default.

Then confirm:

- Pi-hole DNS works.
- Pi-hole blocking works.
- Pi-hole health is healthy or running.
- Pi-hole admin UI is reachable.
- Prometheus targets remain up.
- Prometheus, Node Exporter, and cAdvisor remain preserved.
- Docker and `/platform` remain preserved.
- Raspberry Pi rollback host remains unchanged.
- Node Exporter and cAdvisor remain internal-only.

Do not run `docker system prune`.

Do not delete broad Docker volumes.

Deleting Grafana data requires separate approval.

---

## Related Documents

- [Platform Operations Dashboard](../specifications/Platform_Operations_Dashboard.md)
- [Operations Dashboard Evidence Template](Operations_Dashboard_Evidence_Template.md)
- [Metrics Foundation Runbook](Metrics_Foundation_Runbook.md)
- [ADR-007 - Governed Operations and Observability](../architecture/decisions/ADR-007-Governed-Operations-and-Observability.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial PLAT-13.6.3 live implementation runbook. |
