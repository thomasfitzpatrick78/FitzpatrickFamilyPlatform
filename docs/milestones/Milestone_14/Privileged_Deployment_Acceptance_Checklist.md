# Privileged Deployment Acceptance Checklist

**Document Version:** 1.0

**Status:** Published Future Gate; Deployment Unauthorized

**Milestone:** PLAT-14.1A named prerequisite

---

## Purpose

This separate checklist governs a future exact-host privileged deployment decision. Completion does not authorize an eligible target, named-target observation, consumer integration, recurrence, or activation.

## Artifact and Configuration

- [ ] Architecture Gatekeeper-approved implementation artifact and review reference.
- [ ] Exact signed immutable proxy image and manifest digest.
- [ ] Exact adapter artifact digest and compatible protocol/contract versions.
- [ ] Exact approved proxy policy digest and category matrix.
- [ ] Exact proxy configuration and deployment bundle digests.
- [ ] Exact authorization trust-anchor digest and revocation state.
- [ ] Verified SBOM, SLSA provenance, signature, builder identity, source revision, module lock, licenses, and vulnerability disposition.
- [ ] Known-good signed rollback artifact/configuration set.

## Host and Runtime

- [ ] Exact host Registry reference; this is deployment scope, not named-target approval.
- [ ] Exact host OS, kernel, CPU architecture, container runtime, Docker Engine `Version`, API version/range, and socket path.
- [ ] Exact proxy and adapter numeric UID/GID and exact non-root socket-access model.
- [ ] Negative proof that no Docker-group, supplemental root-equivalent group, root fallback, broader socket permission, host-user/daemon mutation, privileged mode, or capability expansion was used.
- [ ] Docker socket owner, group, mode, inode type, recreation behavior, and proxy-only visibility.
- [ ] Exact adapter Unix socket directory owner/group/mode and peer-credential behavior.
- [ ] Non-root, capability, no-new-privileges, seccomp, AppArmor, read-only root, mount, tmpfs, process, CPU, memory, FD, concurrency, rate, and timeout evidence.
- [ ] No host port, host network, TCP/UDP, DNS, egress, sibling socket access, or socket propagation.
- [ ] Restart disabled; local health check cannot contact Docker.

## Audit, Test, and Operations

- [ ] Exact audit destination, access control, capacity, durability, replay journal, 90-day retention, rotation, and fail-closed behavior for unavailable, ambiguous, stale, corrupt, or unsuccessful replay state.
- [ ] Complete positive and negative security suite passes against the exact artifact/configuration in an approved isolated environment.
- [ ] Actual runtime enforcement proof matches each published control; manifest declaration alone is insufficient.
- [ ] Adapter-first/proxy-second independent disablement succeeds without observed-workload mutation.
- [ ] Rollback to the retained known-good digest succeeds and the negative suite reruns.
- [ ] Incident owner, escalation, evidence preservation, revocation, and unsupported-version procedures are approved.
- [ ] Repository validation, governance validation, hygiene, link checks, secret scan, and prohibited-artifact scan pass.
- [ ] Architecture Gatekeeper approves the exact deployment package.
- [ ] Human Platform Administrator affirmatively approves the exact host, artifact, configuration, and time-bounded deployment action.

## Explicit Exclusions

- [ ] No Registry subject is made eligible by deployment approval.
- [ ] No named target, observation window, or Docker-backed provider attempt is authorized.
- [ ] No dashboard, API, Operations Analyst, EO, or FFFA integration is authorized.
- [ ] No recurring execution, monitoring promotion, or activation is authorized.
- [ ] No Docker daemon, workload, Registry, or infrastructure mutation is included in the deployment gate.

## Decision Record

| Exact evidence | Approved value/reference |
|----------------|--------------------------|
| Implementation acceptance | Pending |
| Image digest | Pending |
| Configuration bundle digest | Pending |
| Policy digest | Pending |
| Host/Docker/API | Pending |
| Service identity | Pending |
| Runtime control evidence | Pending |
| Audit/retention evidence | Pending |
| Negative test report | Pending |
| Rollback/disablement report | Pending |
| Architecture Gatekeeper approval | Pending |
| Human Platform Administrator approval | Pending |

All pending values must be replaced with exact reviewed evidence. Blank, wildcard, inferred, or “latest” values fail the gate.

## Related Documents

- [Runtime Security Control Specification](../../specifications/Privileged_Proxy_Runtime_Security_Control_Specification.md)
- [Supply-Chain Security Requirements](../../specifications/Privileged_Proxy_Supply_Chain_Security_Requirements.md)
- [Implementation Acceptance Checklist](Privileged_Proxy_Implementation_Acceptance_Checklist.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Published the future exact-host privileged deployment gate with binding non-root/socket-authority and durable replay requirements while preserving separate target and observation authorization. |
