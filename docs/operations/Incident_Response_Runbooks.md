# Incident Response Runbooks

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document defines initial incident response runbooks for the Platform.

The commands are future implementation guidance. Do not run commands against live infrastructure unless the incident response action has been approved for that moment.

---

## Severity Model

| Severity | Meaning | Example |
|----------|---------|---------|
| SEV-1 | Household-wide production impact | DNS unavailable for most devices |
| SEV-2 | Major service risk or degraded production | Pi-hole unhealthy but rollback available |
| SEV-3 | Operational issue with workaround | Disk pressure warning |
| SEV-4 | Planning or evidence issue | Missing backup report |

---

## Alert Requirements

| Alert | Severity | Trigger | Duration | Recovery | Owner | First Response | Escalation | Evidence | Test Method |
|-------|----------|---------|----------|----------|-------|----------------|------------|----------|-------------|
| Beelink unavailable | SEV-1 | Host unreachable | 5 minutes | Host reachable | Family Platform owner | Check power, UPS, network | Consider DNS rollback | Ping/SSH notes | Safe planned host reachability test |
| Pi-hole DNS unavailable | SEV-1 | DNS query fails | 2 minutes | DNS query succeeds | Family Platform owner | Test direct DNS | Roll back router DNS if needed | Query output | Deliberate safe query to known domain |
| Pi-hole container unhealthy | SEV-2 | Container health not healthy | 5 minutes | Healthy status | Family Platform owner | Inspect container status | Consider restart/rollback | Container status | Future non-production test |
| Container restarting repeatedly | SEV-2 | Restart count increasing | 5 minutes | Restart count stable | Family Platform owner | Inspect logs | Roll back image | Status/log notes | Future controlled test |
| Disk utilization high | SEV-3 | Disk above threshold | 15 minutes | Below threshold | Family Platform owner | Inspect largest paths | Reduce retention or clean reviewed paths | Disk report | Future threshold test |
| Memory pressure | SEV-3 | Memory pressure sustained | 15 minutes | Memory normal | Family Platform owner | Inspect containers | Stop non-critical planned services | Memory report | Future threshold test |
| Prometheus target unavailable | SEV-3 | Target down | 10 minutes | Target up | Family Platform owner | Check target and network | Fix exporter or config | Target status | Future monitoring test |
| Backup overdue | SEV-3 | No recent backup report | 1 day | Backup completes | Family Platform owner | Check backup workflow | Run reviewed backup | Backup report | Future scheduled test |
| Backup failed | SEV-2 | Backup exits failed | Immediate | Backup succeeds | Family Platform owner | Preserve logs | Avoid update until backup works | Log/report | Future failed backup test |
| Restore validation failed | SEV-2 | Restore test fails | Immediate | Restore validation passes | Family Platform owner | Preserve restore output | Review backup design | Restore report | Future isolated restore test |
| Monitoring stack unavailable | SEV-3 | Prometheus/Grafana unavailable | 15 minutes | Monitoring reachable | Family Platform owner | Check monitoring containers | Keep Pi-hole independent | Monitoring notes | Future safe alert test |

---

## Beelink Unavailable

Symptom: `beelink` or `192.168.50.127` cannot be reached.

Impact: Pi-hole may be unavailable if the host is down.

Severity: SEV-1 if DNS is affected.

First checks:

1. Check whether the UPS and Beelink have power.
2. Check Ethernet connection.
3. Check whether the ASUS router shows the Beelink reservation.
4. From an approved admin workstation, a future safe check may use `ping 192.168.50.127`.

Rollback:

- Consider returning router DNS to Raspberry Pi `192.168.50.67` if Beelink cannot be recovered promptly.

Evidence:

- Time noticed.
- Power state.
- Network state.
- Router client/reservation observation.
- Rollback decision.

Closeout:

- Update registry or runbook if host identity, power, or network assumptions changed.

---

## Docker Unavailable

Symptom: Docker service is not active or containers cannot run.

Impact: Pi-hole container may be stopped.

Severity: SEV-1 if DNS is unavailable; otherwise SEV-2.

First checks:

1. Confirm Beelink is reachable.
2. Future approved command: `systemctl status docker`.
3. Future approved command: `docker ps`.

Rollback:

- Use Raspberry Pi DNS rollback if Pi-hole cannot run on Beelink.

Evidence:

- Docker status.
- Container list.
- Any recent update or reboot.

---

## Pi-hole Container Unhealthy

Symptom: Container `pihole` is unhealthy or stopped.

Impact: DNS or admin UI may be degraded.

Severity: SEV-2, or SEV-1 if DNS fails.

First checks:

1. Future approved command: `docker ps`.
2. Future approved command: `docker inspect pihole`.
3. Check Pi-hole admin page on TCP `8080` from the trusted network.

Rollback:

- Consider Raspberry Pi rollback if DNS is unavailable.

Evidence:

- Container health.
- Recent logs.
- DNS query result.

---

## DNS Unavailable

Symptom: Household clients cannot resolve names.

Impact: Internet use may fail for family devices.

Severity: SEV-1.

First checks:

1. Confirm whether the MacBook is on Proton VPN. Proton VPN uses Proton DNS intentionally.
2. Test a non-VPN client if available.
3. Future approved command: direct query to `192.168.50.127`.

Rollback:

- Change router DNS back to Raspberry Pi only as an approved incident response action.

Evidence:

- Client tested.
- VPN state.
- DNS query output.
- Router DNS setting if inspected.

---

## Disk Pressure

Symptom: Disk utilization exceeds threshold.

Impact: Docker, Pi-hole, backups, or monitoring may fail.

Severity: SEV-3, or SEV-2 if services are failing.

First checks:

1. Future approved command: `df -h`.
2. Future approved command: inspect `/platform/data`, `/platform/backups`, and `/platform/logs`.

Rollback:

- Do not delete data without review. Reduce planned retention only after review.

Evidence:

- Disk report.
- Largest paths.
- Cleanup decision.

---

## Backup Failure

Symptom: Backup report missing or failed.

Impact: Recovery confidence is reduced.

Severity: SEV-2 for failed backup; SEV-3 for overdue backup.

First checks:

1. Check latest backup report.
2. Check available disk.
3. Check permissions.

Rollback:

- Do not perform production update until backup is healthy or explicitly waived by review.

Evidence:

- Backup report.
- Error output.
- Next action.

---

## Restore-Validation Failure

Symptom: Backup exists but isolated restore validation fails.

Impact: Backup cannot be treated as proven.

Severity: SEV-2.

First checks:

1. Preserve restore output.
2. Confirm backup file and checksum.
3. Confirm restore target is isolated.

Rollback:

- Do not replace production with an unvalidated restore.

Evidence:

- Backup identifier.
- Restore command or process.
- Failure point.

---

## Monitoring Unavailable

Symptom: Prometheus or Grafana is unavailable after future implementation.

Impact: Observability is degraded; Pi-hole may still be serving DNS.

Severity: SEV-3 unless production DNS is affected.

First checks:

1. Confirm Pi-hole DNS separately.
2. Check monitoring container status after implementation.
3. Check trusted-network access only.

Rollback:

- Stop monitoring stack if it affects production Pi-hole.

Evidence:

- Monitoring status.
- Pi-hole status.
- Any recent configuration change.

---

## Incorrect DHCP or IP Assignment

Symptom: Beelink address differs from `192.168.50.127`.

Impact: DNS production binding may fail or clients may use the wrong host.

Severity: SEV-1 if DNS is affected; otherwise SEV-2.

First checks:

1. Check ASUS DHCP reservation.
2. Confirm MAC address `78:55:36:09:D2:45`.
3. Confirm no other device has the expected address.

Rollback:

- Restore stable reservation before production promotion or continued operation.
- Consider Raspberry Pi rollback if DNS is affected.

Evidence:

- Router reservation screenshot or note.
- Beelink MAC and IP.
- Client impact.

---

## Closeout Actions

After any incident:

1. Record what happened.
2. Record what fixed it.
3. Record whether rollback was used.
4. Update registry or runbook if the model was wrong.
5. Preserve validation evidence.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial incident response runbooks and alert requirements for PLAT-13.6. |
