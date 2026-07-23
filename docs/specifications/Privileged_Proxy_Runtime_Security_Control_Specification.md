# Privileged Proxy Runtime Security Control Specification

**Document Version:** 1.0

**Status:** Published Future Controls; Controls Not Enforced

**Milestone:** PLAT-14.1A named prerequisite

---

## Purpose

This specification maps the published Deployment Configuration Foundation into future enforceable controls and later proof. A declared manifest is not enforcement evidence. No runtime configuration is created by this document.

## Control Mapping

| Control | Configuration source | Enforcement point | Required validation evidence | Failure behavior and later proof |
|---------|----------------------|-------------------|------------------------------|----------------------------------|
| Non-root UID | Deployment identity/config digest | Container runtime numeric `user` | Process credentials and `/proc` evidence | Required where compatible with the exact approved socket model; incompatible access stops for architecture review rather than falling back to UID 0. |
| Docker socket access authority | Host-specific architecture and deployment approval | Exact socket ownership/access model | Socket owner/group/mode, process groups, daemon configuration, and negative authority-expansion proof | No Docker-group, supplemental root-equivalent group, root fallback, broader permission, host-user/daemon mutation, privileged mode, or capability expansion is implicitly authorized. |
| No privilege escalation | Security config | Runtime `no-new-privileges` | OCI/runtime inspect plus negative test | Deployment blocked if absent. |
| Capabilities | Security config | Drop `ALL`; no add-back initially | Runtime inspect and capability-set test | Any effective/permitted capability blocks deployment. |
| Seccomp | Approved profile digest | Runtime seccomp attachment | Profile digest and denied-syscall tests | Default/unconfined profile blocks deployment. |
| AppArmor | Approved profile digest | Host LSM/runtime profile | Loaded/enforced profile and denial audit | Missing/unconfined profile blocks deployment. |
| Read-only root | Security config | Runtime root filesystem | Write-denial tests outside approved paths | Any unexpected writable path blocks deployment. |
| Writable paths | Exact mount list | Runtime mount namespace | Mount table, flags, size, ownership | Unknown or broader mount blocks startup/deployment. |
| Adapter Unix socket | Identity config | Dedicated runtime directory | Mode/owner/group, `SO_PEERCRED`, signed authorization, exact target/time/scope, and all digest checks | Peer credentials establish local process context only; any identity, authorization, binding, or metadata drift denies requests. |
| Docker socket | Host deployment config | Proxy-only read-only private bind | Mount visibility across all workloads; mode/inode tests | Adapter/sibling visibility or metadata drift blocks. |
| Temporary storage | Resource config | 16 MiB `tmpfs`, `nodev,nosuid,noexec` | Mount flags and exhaustion test | Exhaustion fails request closed. |
| Audit/replay storage | Audit config | Dedicated bounded persistent mount | Durable pre-access nonce verification/commit, restart replay, ambiguity/staleness/corruption/full tests | Any unavailable, ambiguous, corrupt, stale, or unsuccessful replay-state check or append makes the proxy not ready and denies privileged calls. |
| PID limit | Resource config | Runtime `pids_limit: 64` | Runtime inspect and exhaustion test | New work denied; workload unaffected. |
| CPU limit | Resource config | Runtime quota 250 millicores | Runtime inspect and load test | Timeout/fail closed; no limit is deployment blocker. |
| Memory limit | Resource config | Runtime 128 MiB limit | Runtime inspect and oversize/load tests | OOM is failure; restart remains disabled. |
| File descriptors | Resource config | RLIMIT_NOFILE 64 | Process-limit evidence and exhaustion test | New work denied. |
| Concurrency | Proxy config | 4 global, 2 per identity, 1 per authorization | Deterministic saturation tests | `concurrency_exhausted`; no queue growth. |
| Rate | Proxy config | Token bucket 6/minute, burst 2 per identity and target | Clock-controlled rate tests | `rate_limited` before Docker. |
| Request timeout | Resource config | Monotonic 10-second total deadline | Stalled-client/upstream tests | Cancel and fail closed. |
| Docker connect/response timeout | Proxy config | 1-second connect, 3-second response within total | Delayed-socket fixtures/later integration tests | Bounded provider failure, no retry. |
| Request/response limits | Endpoint policy | Frame reader and bounded upstream reader | Boundary plus over-limit tests | Entire message rejected. |
| Restart policy | Runtime config | Runtime restart disabled | Runtime inspect and crash test | Human-reviewed recovery only. |
| Health check | Runtime config | Binary local self-check, no Docker contact | Prove checks config/policy/audit/socket metadata | Not-ready on drift; no automatic restart. |
| Immutable image | Compatibility/config | OCI manifest digest only | Pull/inspect digest, signature, provenance | Tag-only or digest mismatch blocks. |
| Dependency pinning | Source/build contracts | `go.mod`, `go.sum`, toolchain and workflow locks | Clean reproducible build and inventory | Unpinned input blocks artifact acceptance. |
| Environment restrictions | Deployment schema | Closed empty-by-default environment | Runtime inspect, secret-pattern scan | Unknown variable or override blocks startup. |
| Secrets | Identity architecture | No secret mount in first same-host slice; public trust anchor only | Mount/env/file scan | Private key, bearer token, or certificate material blocks. |
| Logging | Audit config | Structured allowlist serializer | Secret and response leakage tests | Unsafe log event rejected; security audit loss disables. |
| Retention | Audit config | Administrator-owned 90-day policy | Rotation, capacity, deletion, and access evidence | Undefined or unbounded retention blocks deployment. |
| Independent shutdown | Deployment/runbook | Adapter-first, socket removal, proxy-second | Timed disablement test without Docker mutation | Failure blocks deployment. |
| Network isolation | Security config | No host network, no network attachment, no TCP sockets | Namespace/runtime inspect and syscall tests | Any IP listener/client capability blocks first slice. |
| Image filesystem | Build architecture | `scratch`, static binary, no shell/package manager | SBOM/image extraction review | Unexpected file/tool blocks acceptance. |

## Allowed Runtime Paths

| Path class | Access | Boundary |
|------------|--------|----------|
| Immutable binary/config/policy/trust anchor | Read-only | Exact digest, root-owned image content. |
| Docker socket | Connect through read-only proxy-only bind | No directory mount or propagation. |
| Adapter boundary directory | Create socket only | Dedicated shared volume; no arbitrary files. |
| Audit/replay directory | Append/update bounded records | `nodev,nosuid,noexec`; no customer or provider payloads. |
| Temporary memory | Bounded scratch only | 16 MiB tmpfs, cleared on stop. |

Every other path is read-only or absent.

## Seccomp and AppArmor Minimums

The approved profiles must be derived from an observed syscall inventory in a nonprivileged test environment and then default deny. They must explicitly deny process execution, namespace creation, mount operations, `ptrace`, kernel module/keyring operations, raw/packet/IP sockets, BPF, perf events, device access, and privilege-changing syscalls. Unix stream socket calls required for the two fixed paths may be permitted. Profile broadening requires a new digest and Architecture Gatekeeper review.

AppArmor must restrict filesystem access to the exact paths above, deny execution except the initial binary, deny network families other than Unix, deny mount, deny signal/ptrace to unrelated processes, and preserve the container runtime's baseline protections.

## Startup Order

1. verify effective identity, capability, filesystem, and mount assumptions;
2. strict-load configuration, policy, compatibility, and public trust anchor;
3. recompute all digests;
4. open and recover audit/replay state;
5. validate Docker-socket metadata without contacting Docker;
6. create and validate the adapter-facing Unix socket;
7. emit durable startup/readiness events;
8. accept bounded adapter requests.

Any failure stops before request acceptance.

## Later Deployment Proof

Repository tests can prove parsers, configuration invariants, fixture decisions, and absence of prohibited imports. Privileged deployment review must separately prove actual UID/GID, effective capabilities, LSM enforcement, seccomp denials, mount namespace, socket visibility, limits under load, audit durability, shutdown, rollback, image identity, and absence of network reachability on the exact host/runtime.

## Related Documents

- [Privileged Deployment Configuration Architecture](../architecture/Privileged_Deployment_Configuration_Architecture.md)
- [Privileged Proxy Implementation Architecture](../architecture/Privileged_Proxy_Implementation_Architecture.md)
- [Privileged Deployment Acceptance Checklist](../milestones/Milestone_14/Privileged_Deployment_Acceptance_Checklist.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Published future enforcement mappings with binding non-root/socket-authority, peer-context, and durable replay-state failure rules without creating runtime configuration. |
