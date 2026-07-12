# Privileged Infrastructure Integration Standard

**Document Version:** 1.0

**Status:** Active governance standard

**Applies To:** Repository-managed services that touch privileged host APIs, runtime sockets, infrastructure control planes, or sensitive telemetry boundaries.

---

## Purpose

This standard governs integrations where a useful platform service needs access to a privileged interface such as the Docker socket. The approved pattern is least-privilege, repository-first, evidence-based, and reversible.

---

## Required Pattern

Privileged integrations must use the narrowest practical trust boundary:

1. Prefer a restricted proxy or purpose-built read-only interface over direct socket access.
2. Pin explicit image versions; `latest`, floating aliases, prereleases, and unattended updates are prohibited unless separately approved.
3. Keep privileged endpoints internal to an isolated Docker network unless Architecture Gatekeeper explicitly approves another boundary.
4. Mount sockets read-only where compatible and only into the boundary service that requires them.
5. Deny API capabilities by default and enable only documented minimum read surfaces.
6. Drop Linux capabilities, disable privileged mode, avoid host networking, and avoid device or broad host filesystem mounts.
7. Do not collect secrets, arbitrary environment variables, command arguments, or broad raw metadata.
8. Define resource limits and monitor cardinality or memory pressure.
9. Provide gated implementation, rollback, persistence, reboot, sensitive-data, and non-regression evidence before lifecycle promotion.

---

## Security Review Requirements

Every privileged integration must document:

- The privileged interface and why it is needed.
- The exact service allowed to reach the interface.
- Enabled API groups and the operational reason for each one.
- Denied mutation, management, credential, and broad enumeration surfaces.
- Network exposure and host-published port state.
- Version source, release date where available, support/maturity state, and digest capture plan.
- Metadata allowlist and sensitive-data exclusion review.
- Rollback path that preserves customer-facing services and persistent data.
- Periodic review trigger after upstream releases, Docker upgrades, or observed behavior changes.

A restricted proxy reduces exposure but does not make privileged socket access risk-free.

---

## Lifecycle Requirements

Privileged integrations start as `planned` or `implementation-ready` records in the Infrastructure Registry. They must not be marked active, healthy, monitoring-ready, production, or complete until live evidence proves:

- The intended read behavior works.
- Prohibited mutation or management behavior is denied.
- No unauthorized network exposure exists.
- No secret-bearing metadata is exported.
- Customer-facing service non-regression passes.
- Rollback and recovery steps are documented and tested to the approved gate.

---

## Incident Response

If a privileged integration is suspected of leaking metadata, exposing an API, or enabling unauthorized control:

1. Stop the dependent collector first.
2. Stop the restricted proxy next.
3. Preserve customer-facing services and platform data.
4. Capture logs and configuration evidence without secrets.
5. Revoke the lifecycle promotion until Architecture Gatekeeper review.
6. Do not broaden API access as an emergency shortcut.

---

## Related Documents

- [Service Lifecycle](Service_Lifecycle.md)
- [Production Service Cutover Checklist](Production_Service_Cutover_Checklist.md)
- [Docker Container Metrics Replacement Runbook](../operations/Docker_Container_Metrics_Replacement_Runbook.md)
- [Docker Container Metrics Replacement Evidence Template](../operations/Docker_Container_Metrics_Replacement_Evidence_Template.md)
