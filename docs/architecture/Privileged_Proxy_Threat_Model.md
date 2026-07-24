# Privileged Proxy Threat Model

**Document Version:** 1.1

**Status:** Architecture Gatekeeper Approved and Published v1.1; No Runtime Authority

**Milestone:** PLAT-14.1A named prerequisite

---

## Scope

This threat model covers the future purpose-built socket holder, its adapter boundary, Docker boundary, configuration, authorization, audit, build artifact, disablement, and rollback. It does not claim that repository architecture eliminates runtime risk.

Risk is stated after the accepted architecture controls. Before implementation and independent proof, privileged proxy compromise remains Critical impact and High uncertainty.

## Assets and Trust Assumptions

Protected assets are Docker daemon authority, host integrity, target identity, authorization intent, provider data minimization, policy/configuration integrity, service identity, audit evidence, build identity, availability, and independent disablement.

The model assumes a correctly functioning Linux kernel/container runtime, controlled host administrator, approved Registry and authorization artifacts, protected signing authority, and verified build platform. Each assumption requires later evidence; none is inferred from repository fixtures.

## Threat Register

| Threat | Actor and attack path | Preventive control | Detective control | Recovery control | Residual risk | Later evidence |
|--------|-----------------------|--------------------|-------------------|------------------|---------------|----------------|
| Malicious/compromised adapter | Authorized local client sends crafted, repeated, or broadened requests. | Non-Docker closed schema, peer UID/GID, signed one-shot authorization, exact operation/target/digests, rate/concurrency limits. | Identity/request denial audit and nonce journal. | Revoke identity/authorizations; adapter-first disablement. | Medium | Fuzz, wrong-client, replay, saturation tests. |
| Malicious local process | Connects to shared Unix socket or substitutes filesystem object. | Dedicated directory, `0660`, exact `SO_PEERCRED`, symlink/inode/mode checks, namespace isolation. | Identity rejection and socket-drift events. | Remove socket, rotate service identity, restart only after review. | Low-Medium | Exact-host UID/GID and namespace tests. |
| Compromised proxy | Uses its Docker authority outside policy. | Minimal code/dependencies, no SDK/general proxy, LSM/seccomp, no shell/network, immutable config, short runtime. | Docker audit, host/runtime detection, safe proxy audit. | Stop adapter/proxy; revoke artifact and authorizations; incident review. | **Medium-Critical** | Independent penetration test and runtime confinement proof. |
| Compromised proxy image | Backdoored binary or unexpected files execute. | Signed digest, provenance, SBOM, reproducible build, `scratch`, source review. | Signature/provenance verification and scans. | Block/revoke digest; restore verified prior digest. | Medium | Verified artifact package and rebuild comparison. |
| Docker daemon compromise | Malicious daemon returns crafted data or host already compromised. | Strict bounded parser/projection; daemon never supplies authority. | Response rejection, host security monitoring. | Invalidate evidence, disable proxy, host incident process. | High | Exact daemon/version review and malformed-response tests. |
| Arbitrary Docker relay | Caller injects path, method, query, headers, or body. | Public protocol has no such fields; closed dispatcher constants only. | Static reachability review and denied-input audit. | Disable/revoke artifact. | Low-Medium | Complete route graph and mutation negative suite. |
| Policy drift | Runtime loads unapproved policy or category change. | Canonical digest binding at startup and request; current policy is sole authority. | Digest mismatch/startup failure. | Restore approved policy/config bundle. | Low | Drift tests and exact runtime digest proof. |
| Configuration drift | Limits, identity, socket, or controls change. | Immutable content-bound bundle and no env overrides. | Startup/request recomputation and audit. | Disable and restore known-good bundle. | Low | Runtime inspect versus digest package. |
| Authorization replay | Token reused, including after restart. | One-shot nonce, durable journal before Docker, 15-minute max expiry. | Replay reason event and sequence check. | Revoke issuer/identity; compact only after expiry plus 24h. | Low-Medium | Crash/restart/replay tests. |
| Target substitution | Authorized subject maps to another container. | Registry digest, exact selector derivation, max-two discovery, response identity recheck. | Target mismatch/duplicate audit. | Invalidate observation and authorization. | Medium | Duplicate/name/label/image drift cases. |
| Registry identity mismatch | Stale or forged declared state enters request. | Exact record digest and eligibility remain authorization prerequisites. | Registry-digest mismatch event. | New reviewed authorization after Registry reconciliation. | Low | Current-record/digest fixture tests. |
| Response-data leakage | Docker response contains secrets, commands, mounts, network, logs, or labels. | Operation-specific field projection and total-size bounds. | Canary secret/topology leakage tests. | Reject whole response, destroy unsafe buffers, incident review. | Low-Medium | Complete field inventory per supported API. |
| Audit tampering | Proxy/local actor deletes, rewrites, or suppresses events. | Durable append before Docker, bounded permissions, hash chain, admin retention. | Sequence/gap/capacity checks and external host evidence. | Disable on loss; preserve host logs; revoke evidence. | Medium | Restart/corruption/full/tamper tests; later external sink. |
| Denial of service | Client floods connections or slow frames. | 4 global/2 identity concurrency, rate limits, 1-second frame read, bounded queues. | Saturation/rate events and resource metrics. | Reject new work; stop adapter; workload untouched. | Low-Medium | Load and slow-client tests. |
| Resource exhaustion | Oversized JSON, Docker body, deep nesting, FD/PID/memory pressure. | Byte/depth/count limits, bounded readers, runtime quotas, no retries/streams. | Limit reason events and runtime counters. | Fail closed; restart disabled pending review. | Low | Boundary and OOM/FD/PID tests. |
| Socket-permission drift | Docker or adapter socket recreated with broader access. | Startup/per-request metadata verification and exact group mapping. | Socket-drift/not-ready event. | Remove adapter socket; stop proxy; administrator correction. | Low-Medium | Recreation/chmod/chown/symlink tests. |
| Adapter socket path squatting | Local actor leaves a stale socket, file, symlink, or replacement at the configured path. | Dedicated `02750` leaf, absent-path startup, full `lstat` chain, current-process-only unlink. | Startup/socket-drift denial with safe path class. | Operator verifies process/type/owner/deployment digest before stale cleanup. | Low | Stale/file/symlink/rename/replacement tests. |
| Unix path collision or namespace bypass | Abstract socket or truncated `sun_path` aliases an unintended endpoint. | Filesystem-only absolute ASCII path and pre-bind length validation. | Configuration-rejection audit. | Correct configuration; no truncation or fallback. | Low | Limit, collision, and abstract-namespace tests. |
| Peer-credential confusion | Namespace translation, group inference, or PID reuse is treated as authorization. | Kernel-returned exact numeric UID/GID, equal real/effective/saved IDs, PID audit-only, complete signed authorization. | Peer-context and deployment identity evidence. | Disable; correct identity mapping; issue fresh authorization. | Low-Medium | Real UDS mismatch and exact-host namespace tests. |
| Frame smuggling | Client sends a valid first frame followed by a delayed byte or second request. | Mandatory client half-close and server EOF before any request processing. | Framing rejection before authorization/provider work. | Close connection; investigate caller identity. | Low | No-half-close, delayed-byte, and second-frame tests. |
| Descriptor transfer or inheritance | A privileged Unix-socket FD escapes to a child or is passed with `SCM_RIGHTS`. | Close-on-exec, no child process, no ancillary-data path, restrictive seccomp. | FD inventory and syscall denials. | Disable process and revoke artifact. | Low | Static review and syscall tests. |
| Docker socket replacement/impersonation | Local actor replaces the path or fake daemon accepts the connection. | Pre/post-connect device/inode/metadata validation and outbound `SO_PEERCRED`; no retry. | Peer/socket-drift audit and not-ready state. | Stop proxy; administrator reconciles exact socket. | Low-Medium | Fake-peer, recreation, and time-of-check tests. |
| Socket propagation | Sibling workload sees or receives Docker socket. | Proxy-only bind, private propagation, no file-descriptor passing, namespace review. | Mount inventory across workloads. | Stop deployment and remove mount. | Low | Exact runtime mount-visibility evidence. |
| Supply-chain compromise | Toolchain, module, builder, workflow, registry, signer, or scanner is compromised. | Pinning, trusted builder, SLSA provenance, signature, SBOM, reproducibility, review. | Independent verification and multi-source scans. | Revoke digests/identity; rebuild from reviewed source. | Medium | Complete acceptance package and trust-root review. |
| Artifact or attestation substitution | Correct tag is paired with wrong architecture, SBOM, provenance, or signature subject. | Per-binary/platform-manifest/index subject digests and independently verified attestation graph. | Cross-subject verification report. | Reject/revoke index and rebuild. | Low-Medium | Cross-architecture and wrong-subject tests. |
| Signing identity/workflow compromise | Valid keyless signature originates from an unapproved issuer, workflow, or revision. | Exact OIDC issuer/workflow identity and claims; offline Sigstore bundle and inclusion verification. | Independent signature-policy result. | Revoke identity/artifact and stop deployment. | Medium | Wrong issuer/identity/workflow/claim tests. |
| Rollback failure | Prior artifact/config unavailable or incompatible. | Retain signed known-good set and test before approval. | Periodic rollback verification. | Keep proxy disabled; never mutate workload as workaround. | Medium | Timed rollback rehearsal. |
| Disablement failure | Adapter continues or proxy cannot drain/stop. | Independent service lifecycle, socket removal, 15-second drain, runtime stop authority. | Disablement events and connection checks. | Host administrator stops proxy workload; preserve observed service. | Medium | Failure-injection disablement tests. |
| Clock skew/manipulation | Accepts future/stale authorization or evidence. | 30-second skew limit, authenticated host time prerequisite, monotonic request deadlines. | Clock-skew event and host time monitoring. | Deny access; repair time; issue new authorization. | Low-Medium | Boundary/skew/jump tests. |
| Stale credential/identity | Revoked UID, trust anchor, signer, or mTLS identity remains accepted. | Revocation metadata and startup/request validation; short validity. | Rejection/audit and review cadence. | Rotate/revoke; disable until confirmed. | Medium | Rotation/revocation tests. |
| Version mismatch | Go/runtime/Docker API or contract shape changes. | Exact compatibility matrix and fixed API; unsupported versions fail closed. | Startup/response version events. | Upgrade through new reviewed artifact or roll back. | Low-Medium | Supported/unsupported version fixtures and exact host proof. |
| Protocol bypass | Smuggling, duplicate lengths, alternate encoding, upgrade, gRPC, tunneling, or streaming. | Non-HTTP single-frame protocol, strict parser, one request/connection, fixed upstream HTTP. | Parser denial events and fuzz corpus. | Disable artifact on any bypass. | Low | Smuggling/encoding/fuzz/upgrade suite. |
| Upstream HTTP parser differential | Ambiguous response length, transfer coding, folded headers, or multiple parsers yield different meanings. | Exact request bytes, one narrowly wrapped parser, no `http.Client`/transport, reject ambiguity and trailing bytes. | Protocol rejection classification. | Close connection and disable unsupported artifact/version. | Low-Medium | Raw response corpus and fuzzing. |
| Filter or Docker-ID injection | Metacharacters or path characters broaden discovery or select a different container. | Validated literals, canonical escaping, anchored `QuoteMeta`, exact post-filter identity, closed hex ID grammar. | Target/filter mismatch audit. | Reject whole result and authorization. | Low | Metacharacter, duplicate, mismatch, and path tests. |
| Response amplification | Small request triggers broad list or stream. | Exact filters, max-two upstream discovery, one projected record, 64 KiB, no streams. | Size/record-limit audit. | Reject whole response. | Low | Broad/malicious daemon response tests. |
| Authentication key compromise | Authorization signer is compromised. | Offline/controlled issuer, short validity, one-shot, policy remains restrictive, revocation. | Unexpected issuance and signer audit. | Revoke trust anchor, disable proxy, rotate issuer. | Medium | Issuer threat review and revocation exercise. |
| Runtime escape | Proxy exploits kernel/runtime through allowed syscalls or socket. | Non-root, capability drop, seccomp, AppArmor, read-only root, patched host/runtime. | Host/runtime security monitoring. | Stop deployment; host incident response. | Medium | Profile denial tests and current vulnerability review. |
| Unauthorized recurring use | One-shot path becomes scheduled/continuous. | `max_attempts: 1`, short expiry, restart disabled, no scheduler or EO activation. | Authorization frequency audit. | Disable and revoke; governance review. | Low | Absence-of-scheduler static/runtime evidence. |

## Abuse Cases that Must Remain Impossible

- Send `POST`, `PUT`, `PATCH`, or `DELETE` to Docker.
- Choose a Docker socket, host, URL, path, query, method, header, or body.
- Request logs, events, attach, exec, archive, filesystem, images, volumes, networks, build, plugins, Swarm, or configuration.
- Enumerate a population of containers.
- Stream or upgrade a connection.
- Pass raw provider fields to the adapter.
- Use provider identity as Registry identity.
- Translate proxy success into health or remediation authority.

## Residual-Risk Decision

Even with all controls, a fully compromised proxy can use the Docker socket with daemon-level authority. Isolation, least code, supply-chain proof, and denial policy reduce likelihood and exposure; they do not reduce the Docker daemon's inherent impact. Privileged deployment therefore requires affirmative Architecture Gatekeeper and human Platform Administrator approval for the exact artifact, host, and configuration.

## Related Documents

- [Privileged Proxy Implementation Architecture](Privileged_Proxy_Implementation_Architecture.md)
- [Security Test Specification](../specifications/Privileged_Proxy_Security_Test_Specification.md)
- [Privileged Deployment Acceptance Checklist](../milestones/Milestone_14/Privileged_Deployment_Acceptance_Checklist.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Added socket-path, peer-credential, frame, descriptor, Docker-peer, HTTP parser, filter, artifact-substitution, and signing-identity threats and required evidence. |
| 1.0 | Published the implementation-specific threat model, binding identity/replay/authority controls, residual risks, and later proof requirements without runtime work. |
