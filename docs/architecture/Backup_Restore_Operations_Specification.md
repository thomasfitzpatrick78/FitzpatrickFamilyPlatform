# Backup and Restore Operations Specification

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document defines the planned backup and restore model for Platform services.

It does not execute backups or restore tests.

---

## Initial Backup Scope

Pi-hole backups must include:

- `/platform/compose/pihole`
- `/platform/data/pihole/etc-pihole`
- Relevant platform documentation, deployment metadata, and recovery artifacts.

Monitoring backups must include future Prometheus/Grafana configuration and required persistent state after implementation.

---

## Default Exclusions

Large or transient Pi-hole query-history data is excluded by default unless Architecture Review approves a retention need.

Temporary files, cache directories, generated logs, and secrets are excluded unless explicitly approved.

---

## Consistency Strategy

Initial design preference:

1. Use an application export where available.
2. If filesystem backup is required, document whether Pi-hole must be stopped or paused.
3. Avoid interrupting production DNS unless rollback DNS is ready.
4. Capture backup start time, end time, source paths, and result.

---

## Naming and Storage

Backup names should include:

- Service name.
- Environment or host.
- UTC timestamp.
- Backup type.

Example pattern:

```text
pihole-beelink-config-YYYYMMDDTHHMMSSZ.tar.gz
```

Initial storage location:

- `/platform/backups/pihole`
- `/platform/backups/monitoring`

Future evolution should include off-host backup.

---

## Integrity Verification

Each backup must produce a checksum or equivalent integrity record.

The checksum proves the file can be compared later. It does not prove the backup can be restored.

---

## Retention

Initial pragmatic retention:

- Keep 7 daily backups.
- Keep 4 weekly backups.
- Keep 3 monthly backups.

Retention may be reduced if disk usage threatens service reliability.

---

## Restore Validation

A backup is not proven until a restore has been tested.

Restore validation must:

1. Use an isolated path or non-production container.
2. Avoid changing router DNS.
3. Avoid replacing the production Pi-hole until a cutover is approved.
4. Confirm restored configuration can start or be inspected.
5. Produce restore-validation evidence.

---

## Failure Handling

Backup failure must create evidence and an incident review path.

Restore-validation failure must be treated as a higher-priority issue than backup failure because it means recovery confidence is not established.

---

## Related Documents

- [PLAT-13.6 Operations and Observability Specification](../specifications/Platform_Operations_Observability_Specification.md)
- [Incident Response Runbooks](../operations/Incident_Response_Runbooks.md)
- [Production Service Cutover Checklist](../governance/Production_Service_Cutover_Checklist.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial backup and restore planning specification for PLAT-13.6. |
