# Container Hosting Standards

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document defines static standards for future container-hosted Platform services.

No container runtime, image, compose project, deployment automation, or service is implemented by PLAT-13.1.

---

## Standards

Future container-hosted services should:

- Have a registry service record before deployment.
- Reference a planned or active host through `host_dependencies`.
- Declare network, power, administrative, and service dependencies where known.
- Store persistent data in named volumes or documented host paths.
- Define backup and restore expectations before production use.
- Avoid embedding secrets in repository files.
- Prefer pinned image versions once implementation begins.
- Preserve rollback steps in service-specific migration notes.

---

## Pi-hole Container Readiness

For future Pi-hole migration, define before deployment:

- Docker or VM hosting model.
- Static IP or DNS forwarding design.
- Volume paths for Pi-hole configuration and DNS data.
- Backup export from Raspberry Pi.
- Rollback trigger and rollback DNS target.
- Validation checklist for client DNS behavior.

---

## Deferred Work

Deferred implementation includes Docker installation, compose files, image pulls, service start commands, health probes, scheduled backups, runtime monitoring, and dashboards.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial container hosting standards. |
