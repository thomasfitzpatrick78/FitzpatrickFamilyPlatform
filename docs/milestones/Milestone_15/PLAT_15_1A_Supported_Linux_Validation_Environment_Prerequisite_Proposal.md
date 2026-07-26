# PLAT-15.1A - Supported-Linux Validation Environment Prerequisite Proposal

**Document Version:** 1.0

**Status:** Product Strategy Board and Architecture Gatekeeper Approved Direction

**Environment State:** Not Created

**PLAT-15.1A:** Blocked at Supported-Linux Initialization Gate

**Repository Implementation:** Not Started

**Milestone:** Milestone 15

**Parent Authority:** PLAT-15.1A under PLAT-PB-013 and AB-011

**Independent Product Backlog Identifier:** None proposed

---

## Purpose

This proposal records the approved architecture direction for satisfying the supported-Linux prerequisite in the published [PLAT-15.1A work package](PLAT_15_1A_Repository_Only_Socket_Capable_Privileged_Proxy_Source_Implementation_Work_Package.md).

PLAT-15.1A requires T-01 through T-12 and every applicable race test to execute on supported Linux without host-dependent skips. The current host is Darwin/arm64, and no already-existing isolated supported-Linux environment is available. The work package therefore requires implementation to stop rather than weaken, emulate, defer, or skip the Linux acceptance gate.

This document records Product Strategy Board and Architecture Gatekeeper direction approval only. It does not create or approve the subordinate environment-preparation work package, create an environment, authorize PLAT-15.1A implementation, or authorize any host, network, artifact, deployment, daemon, operational, release, or live action.

---

## Selected Direction

**Option A - Disposable local Linux VM** is approved as the bounded prerequisite architecture direction, subject to all of the following conditions:

1. Product Strategy Board approval is limited to the prerequisite direction, portfolio fit, and continued use of PLAT-15.1A without a new independent Product Backlog identifier.
2. The Architecture Gatekeeper approves the exact environment architecture, trust boundaries, supply-chain manifest, isolation controls, validation plan, evidence contract, failure behavior, recovery plan, and teardown proof.
3. A separately proposed, reviewed, approved, and published subordinate environment-preparation work package binds every unresolved exact value and every authorized host action before any acquisition or environment action occurs. Publishing this proposal does not create or approve that work package.
4. A named Platform Administrator or host owner provides separate explicit authorization for every host-affecting action, including acquisition, preparation, creation, import if applicable, startup, provisioning, validation use, result export, shutdown, teardown, and deletion.
5. PLAT-15.1A remains `Not Started` and blocked until environment-readiness evidence has been reviewed and accepted under the future work package.

Option A is narrower and safer than the alternatives because it can keep source and results within the local governed boundary, can use native ARM64 Linux kernel execution without container-runtime or remote-runner authority, can prohibit host filesystem and runtime-socket sharing, and can be deterministically removed after evidence export. Approval of the direction must not be mistaken for approval of a virtualization product, Linux image, toolchain archive, environment creation, environment use, or implementation.

---

## Decision Record

| Decision | Authority | Recorded State |
|----------|-----------|----------------|
| Select Option A under existing PLAT-15.1A / PLAT-PB-013 authority without a new Product Backlog identifier | Product Strategy Board | Approved for governed publication |
| Confirm AB-011 as the governing architecture linkage | Product Strategy Board and Architecture Gatekeeper | Approved; unchanged |
| Approve the disposable native ARM64 Linux VM architecture direction with a strictly offline guest | Chief Architect / Architecture Gatekeeper | Direction approved only |
| Approve a virtualization product, Linux image, checksum manifest, acquisition, provisioning, VM creation, startup, environment use, or PLAT-15.1A implementation | Not approved by this decision | Unauthorized |
| Create or approve the subordinate environment-preparation work package through this proposal publication | Not approved by this decision | Not created; requires separate proposal, review, approval, and publication |
| Promote or activate AB-012 | Not approved by this decision | AB-012 remains `Candidate - Remain Backlog` |

The approval is architecture direction only. Repository publication makes the recorded decision durable but does not expand it.

---

## Current Repository and Prerequisite Evidence

| Evidence | Current State |
|----------|---------------|
| Repository | `FitzpatrickFamilyPlatform` on `main`. |
| Synchronized authority | Local `HEAD`, `origin/main`, and fetched live remote equal `6a3bc2a48627806bb424addaae278ea904e2a942`; ahead/behind `0/0`. |
| Tree | `bc29967337ea44c51b2b3048cff493edc0ac52d3`. |
| Starting generated evidence | The only starting changes were the two governed readiness reports with prompt-approved SHA-256 values `369e5b5c3432115ce8029b406872b794f16ad35e13035ee242819165049dfb08` and `3d2741b247b34c7d6cecaeb85eea3a18067834204edc5d1d443b990dd3e4dbeb`. |
| Required initialization regeneration | Repository-governed readiness regeneration returned `READY`, zero errors, and zero warnings. The baseline classifier returned `Expected Generated Evidence`; the qualifying regenerated report hashes are `11b76b7619e55d3e1b46a9a9684f33afc9d24e223526edd9a53e231d604febce` and `8353690568c7a3f224520d79325f2f6f638c6883a65c751acf69d48030f88bd9`. |
| Current execution host | Darwin/arm64; insufficient for Linux kernel-returned `SO_PEERCRED` and supported-Linux race evidence. |
| Existing qualifying environment | None available; no environment was created, started, configured, or used during this proposal session. |
| PLAT-15.1A authority | Published for future repository implementation; implementation remains `Not Started`. |

The regenerated readiness reports remain qualifying governed generated evidence. They do not authorize this proposal, environment work, source implementation, publication, or live work.

---

## Binding Invariants

Any viable environment must preserve all of the following:

- native supported Linux kernel execution on ARM64; no cross-compilation or non-Linux kernel substitute for Linux evidence;
- real kernel-returned `SO_PEERCRED` evidence and Linux filesystem Unix-socket lifecycle behavior;
- execution of T-01 through T-12 and every applicable race test without host-dependent skips;
- no Docker, Podman, containerd, Kubernetes, container daemon, Docker CLI or SDK, real governed socket, host runtime socket, IP-test network, deployment, Registry mutation, infrastructure mutation, observation, activation, release, customer data, or live work;
- no host device, credential, secret, customer-data, sensitive-directory, user/group, service, daemon-configuration, permission, socket, or network-configuration sharing or mutation;
- no persistent binary, OCI artifact, SBOM, provenance, signature, deployment, installation, or operational-readiness claim;
- source and results bound to exact digests, with sanitized evidence only entering the repository;
- fail-closed behavior on identity, checksum, isolation, test, evidence, shutdown, or teardown ambiguity;
- ADR-012 remains `Implemented: No`, AB-012 remains `Candidate - Remain Backlog`, PLAT-15.1A remains `Not Started` until its separate implementation gate resumes, and the closed proxy transport architecture remains unchanged.

---

## Option A - Disposable Local Linux VM

### Proposed Architecture

Use one task-specific, disposable, native ARM64 Linux VM through a separately reviewed and approved macOS virtualization mechanism. The preferred mechanism is a non-daemon host tool using the macOS virtualization or hypervisor framework without privileged persistent services. No mechanism is selected or approved by this proposal.

The VM is a validation boundary, not a deployment target, build service, reusable developer environment, artifact producer, or operational host. Its writable state is limited to VM-local temporary source, module/tool caches, test outputs, and audit material required for the authorized run.

### Static Environment Manifest Gate

The future environment-preparation work package must contain a complete static environment manifest with no `latest`, floating, inferred, or unresolved value before acquisition is authorized:

| Manifest Field | Required Binding |
|----------------|------------------|
| Virtualization mechanism | Exact product or host-tool name, version, source, publisher, signature or notarization evidence, package/archive checksum, required privileges, process model, and proof that no persistent privileged daemon is required. |
| Linux distribution | Exact vendor and distribution name. |
| Linux release | Exact release and point release with active vendor security support through the planned validation period. |
| Image | Exact minimal ARM64 server or installer image filename, canonical vendor URL, publication date, byte size, SHA-256, signed-checksum verification method, and signer identity. A container image or cloud image requiring remote control-plane authority is prohibited. |
| Kernel | Exact expected kernel package and version from the selected image, native `aarch64` architecture, expected boot parameters, and post-boot `uname`/package evidence. Automatic kernel or package upgrades are prohibited. |
| Guest architecture | Native `linux/arm64` / `aarch64`; x86 translation and user-mode or syscall emulation are prohibited. |
| Go toolchain | Exact `go1.26.5.linux-arm64.tar.gz` archive, canonical `go.dev` source, official SHA-256, archive size, support/advisory review, and guest-local post-unpack `go version` evidence. |
| External module | Exact `golang.org/x/sys` `v0.47.0` module and source revision, `go.sum` bindings, archive and metadata verification, license, maintenance, advisory, and vulnerability evidence. Any drift returns to Architecture Gatekeeper review. |
| Isolation contract | No guest network adapter; no bridged, NAT, host-only, or other guest network; no host filesystem, clipboard, device, credential, secret, socket, or sensitive-directory sharing; exact VM-local storage and identity boundaries. |
| Source-ingress contract | Approved bounded transfer mechanism, source-bundle format, generated-file exclusions, authorized guest destination, integrity algorithm, and failure behavior. Actual repository and diff identities belong only in the later per-run execution manifest. |
| Result-egress contract | Exact allowed sanitized filenames, schemas, size limits, checksums, redaction rules, transfer mechanism, and repository destinations. |
| Evidence contract | Exact environment-readiness, pre-test, post-test, result, shutdown, teardown, recovery, and limitation evidence required before any later gate. |

This proposal intentionally does not invent the distribution release, kernel version, image checksum, virtualization-tool version, or archive checksums. Until the future work package binds and the Architecture Gatekeeper approves those exact values, environment preparation remains unauthorized and blocked.

### Per-Run Execution Manifest Gate

The static environment manifest must not contain a future or inferred implementation revision. After the environment-preparation work package is separately approved and the later PLAT-15.1A implementation tree exists, each authorized validation run requires a separate immutable execution manifest containing:

- the approved static environment-manifest identifier and digest;
- actual repository branch, fetched local/tracking/live equality evidence, `HEAD`, and tree;
- the exact scoped implementation diff or worktree digest and changed-path inventory;
- source-bundle filename, size, SHA-256, generated-file exclusions, and guest destination;
- actual VM instance identifier, environment-readiness evidence identifier, bounded non-administrative execution identity, fixture/corpus identities, commands, time window, and result-egress manifest;
- the named Platform Administrator or host owner authorization reference for each host-affecting step; and
- fail-closed treatment for any mismatch, missing field, drift, unauthorized path, or expired approval.

The execution manifest identifies the actual run; it does not amend or silently drift the static environment architecture.

### Trust Boundaries and Data Flow

| Boundary | Required Control |
|----------|------------------|
| Repository authority | Begin from a separately fetched and synchronized repository baseline. Bind the actual source revision, tree, scoped uncommitted diff, and changed paths only in the per-run execution manifest before transfer. No source may be fetched from inside the guest. |
| Host to guest | Use a task-specific, integrity-checked, read-only removable image or equivalent bounded one-time transfer approved in the future work package. Persistent shared folders, bidirectional mounts, clipboard sharing, drag-and-drop, home-directory sharing, SSH, and host-agent integration are prohibited. |
| Guest to host | Export only schema-bounded, sanitized test summaries and checksums through a separate task-specific result medium. Raw environment logs, host paths, usernames, credentials, secrets, process inventories, network state, or unrelated system data must not enter Git. |
| Host resources | Do not share runtime sockets, devices, keychains, credentials, secrets, customer data, sensitive directories, host users/groups, or privileged services. |
| Guest identity | VM-local administrative privilege is permitted only during separately authorized environment preparation. PLAT-15.1A implementation and validation must use a bounded non-administrative VM-local execution identity defined by the static manifest. Its numeric UID/GID evidence is test context only and creates no host identity or authorization. |

### Strictly Offline Networking Architecture

The selected architecture has no guest network adapter at any lifecycle stage. Bridged, NAT, host-only, shared, VPN-inherited, inbound, outbound, private, public, and governed guest networking are prohibited during preparation, source ingress, implementation support, validation, result export, shutdown, and teardown.

Image, virtualization mechanism, Go toolchain, module material, source, and result media must be acquired or prepared outside the guest only through separately authorized, checksum-verifying host steps, then transferred through the approved bounded media contract. The guest must prove the absence of a network adapter before source ingress and before and after validation; tests must fail fast on attempted IP networking.

If later research establishes that provisioning networking is unavoidable, that finding is a material architecture change. Work stops and returns to renewed Architecture Gatekeeper review; the future work package may not introduce a networking exception by implementation detail or host authorization alone.

### Daemon, Socket, and Filesystem Exclusion

The future readiness procedure must prove before source ingress and again before tests that:

- Docker, Podman, containerd, Kubernetes, and container-daemon packages, services, sockets, CLIs, SDKs, environment variables, and group memberships are absent;
- `/var/run/docker.sock`, `/run/docker.sock`, rootless runtime sockets, governed sockets, and non-temporary Unix-socket roots are absent and inaccessible;
- no host runtime socket, device, filesystem, credential store, secret, or sensitive directory is mounted or forwarded;
- only the approved task media and VM-local temporary writable storage are visible;
- no guest network adapter exists, only loopback is available to the guest, and test code remains prohibited from using IP networking.

Unexpected presence or unverifiable absence is a hard stop; it is not repaired ad hoc in the implementation session.

### Toolchain and Dependency Handling

Acquisition is a separate future host action. Approved archives must be verified against canonical publisher evidence before use and again after transfer. The guest must use the exact bound toolchain with local-only resolution during tests. Automatic toolchain retrieval, package upgrades, module proxy access, checksum-database network access, VCS network access, and dependency drift are prohibited.

The future work package must define task-specific guest paths, checksum commands, module-cache preparation, `GOTOOLCHAIN=local`, offline module behavior, and failure handling. It must not authorize changes to `go.mod` or `go.sum`; those remain within the later PLAT-15.1A implementation scope and its Architecture Review gate.

### Validation Execution and Evidence

After separate environment-readiness acceptance and PLAT-15.1A implementation initialization, the Linux run must record at least:

- exact image, kernel, distribution, architecture, virtualization mechanism, Go, module, repository, source-bundle, fixture, and corpus identities;
- proof of native Linux kernel execution and real kernel-returned `SO_PEERCRED` behavior;
- pre-test and post-test isolation checks;
- T-01 through T-12 results with no host-dependent skip;
- applicable race-test results, including `go test -race ./...` on supported Linux;
- required bounded fuzz, repository-safe Go, Platform engineering, privileged-proxy, link, secret, hygiene, and whitespace validation results applicable to the implementation gate;
- proof that no daemon, governed socket, IP-test network, persistent artifact, deployment, Registry, customer-data, activation, release, or live action occurred;
- sanitized result-manifest checksums and limitations;
- shutdown and teardown evidence produced only under their separately authorized steps.

Evidence must distinguish source conformance from environment conformance. A passing Linux run does not approve the source, create an artifact, prove deployment readiness, or authorize any later gate.

### Failure, Recovery, and Teardown

Any checksum mismatch, identity drift, unexpected package/service/socket/mount/network, source-digest mismatch, test skip, test failure, evidence ambiguity, export-policy violation, or teardown uncertainty fails closed. Preserve only approved sanitized failure evidence. Do not repair, restart, recreate, reacquire, rerun, or expand access without the authorization defined by the future work package.

The future work package must define deterministic rollback and teardown targets by exact task-specific path and identifier. Teardown must be separately human-authorized and must remove the task-created VM definition, guest disks, attached transfer media, toolchain/module caches, temporary source, test output, and virtualization metadata, then verify their absence. It must not target a broad directory, shared cache, pre-existing image, unrelated VM, or user data. If teardown cannot be verified, the prerequisite remains incomplete and escalates to the Architecture Gatekeeper and human host owner.

### Residual Risks

- The virtualization mechanism and exact supply-chain manifest are not yet selected or approved.
- A vendor-signed image checksum proves archive identity, not correct guest configuration or absence of vulnerable packages.
- A native VM narrows but does not eliminate hypervisor, host-kernel, image, toolchain, dependency, or result-sanitization risk.
- Offline execution can hide missing dependency preparation until validation begins; the correct response is to stop, not enable network access.
- Teardown proof cannot demonstrate physical data erasure from all storage layers; it must truthfully prove removal of the exact task-created logical state and disclose that limitation.
- VM-local root or administrator access, if required for guest preparation, must be separately authorized, bounded to preparation, and ended before implementation or validation; it cannot imply host or production privilege.

---

## Option B - Existing Approved Linux Environment

Option B is viable only if an already-existing trusted Linux VM or host later becomes available and is separately approved. None is assumed to exist now.

Before use, its owner must provide evidence at least equivalent to Option A for repository/source authority, exact distribution/release/kernel/architecture, native Linux execution, toolchain and dependency checksums, isolation, absence of container daemons and governed sockets, networking restrictions, filesystem sharing, credentials, secrets, temporary source handling, sanitized results, caches, failure behavior, recovery, and removal of task-created state.

Additional requirements are:

- documented ownership, purpose, authorization history, tenancy, patch state, change control, access-control boundary, and concurrent-user/process boundary;
- proof that pre-existing state cannot influence tests and PLAT-15.1A state cannot persist for a later user or task;
- no production, customer, shared-development, CI, deployment, or container-host responsibility;
- no reliance on inherited credentials, agents, mounts, network routes, caches, or daemon access;
- an approved method to return the environment to its exact pre-task state without deleting or mutating unrelated owner data.

Because no qualifying environment currently exists and inherited-state risk is materially higher, Option B is not selected. Product Strategy Board and Architecture Gatekeeper review would be required if a concrete candidate later appears, and separate human owner authorization would remain mandatory.

---

## Option C - Hosted CI or Remote Runner

Reject Option C for this prerequisite unless a later proposal demonstrates a compelling need and receives expanded governance.

- GitHub Actions remains deferred in the [Product Roadmap](../../product/Product_Roadmap.md).
- Remote infrastructure, accounts, credentials, secrets, source transfer, logs, artifacts, retention, runner identity, image provenance, networking, geographic or tenancy boundaries, and deletion guarantees expand authority beyond the local repository-only package.
- Hosted logs and caches can retain source, paths, environment metadata, or evidence outside the local governed boundary.
- Ephemeral-runner claims require independent provider and teardown evidence and do not by themselves satisfy the isolation or deletion gate.
- A workflow would create durable automation and remote execution surface beyond this prerequisite.

No workflow, runner, cloud resource, account, credential, secret, or remote contact is authorized.

---

## Option D - Cross-Compilation, Darwin Tests, or Non-Kernel Emulation

Reject Option D as insufficient. Cross-compilation can show that source compiles for `linux/arm64`, and Darwin tests can exercise platform-independent logic, but neither supplies:

- real Linux kernel-returned `SO_PEERCRED` evidence;
- Linux filesystem Unix-socket lifecycle semantics;
- supported-Linux race evidence;
- syscall-observing Linux integration evidence; or
- the published no-skip acceptance gate.

User-mode emulation, mocked credentials, injected peer context, or an emulated userspace without native Linux kernel execution cannot replace these proofs. They may be supplementary evidence only if separately authorized within PLAT-15.1A; they cannot satisfy the supported-Linux prerequisite.

---

## Comparative Decision

| Criterion | Option A: Disposable local VM | Option B: Existing approved Linux | Option C: Hosted CI or remote | Option D: Cross/Darwin/emulation |
|-----------|-------------------------------|----------------------------------|-------------------------------|------------------------------------|
| Real Linux kernel and `SO_PEERCRED` | Yes, if exact native VM is approved | Yes, if exact candidate is proven | Potentially, but remote trust expands | No qualifying proof |
| Local governed source boundary | Strongest viable fit | Candidate-dependent | No | Yes, but evidence insufficient |
| Isolation control | Task-specific and designable | Inherited-state risk | Provider-dependent | Insufficient execution model |
| Credentials or remote authority | Not required by preferred design | Candidate-dependent | Required or materially expanded | Not required |
| Deterministic task-state teardown | Designable and auditable | Candidate-dependent | Provider-dependent | Not applicable to missing proof |
| Current availability | Not created | None available | Not authorized | Available but insufficient |
| Decision | Recommend bounded direction | Retain as conditional fallback | Presumptively reject | Reject |

---

## Authority and Approval Matrix

| Decision or Action | Product Strategy Board | Architecture Gatekeeper | Separate Human Host Authorization |
|--------------------|------------------------|--------------------------|-----------------------------------|
| Select Option A as the prerequisite direction and retain PLAT-15.1A without a new Product Backlog identifier | Approved | Direction approved | Not an action authorization |
| Approve exact virtualization, Linux, kernel, image, toolchain, dependency, isolation, validation, evidence, failure, recovery, and teardown design | Confirm portfolio boundary | Approve exact architecture and residual risk | Confirm host acceptability; no execution yet |
| Publish proposal decision and future subordinate work package | Approve product decision | Approve architecture/security content | Not an action authorization |
| Acquire virtualization mechanism, image, toolchain, or module material | No implied authority | Architecture must already be approved | Named Platform Administrator or host owner explicitly authorizes the exact action |
| Create, import, configure, start, provision, or inspect the VM | No implied authority | Must remain inside approved design | Named Platform Administrator or host owner explicitly authorizes every host-affecting action |
| Resume PLAT-15.1A source implementation | Existing PLAT-15.1A priority remains | Only after accepted environment readiness and new governed initialization | No environment use without explicit authorization |
| Execute Linux validation and export sanitized evidence | No implied later-gate authority | Review scope and evidence contract | Explicit authorization for use and export |
| Shut down and tear down task-created state | No implied authority | Review proof contract and exceptions | Explicit authorization for exact shutdown and deletion targets |
| Accept PLAT-15.1A source | No automatic product-state change | Architecture Gatekeeper decision after evidence acceptance and teardown | Not a source-acceptance authority |

---

## Distinct Lifecycle Gates

```text
1. Architecture/Specification Proposal Publication
        |
        v
2. Separate Environment-Preparation Work-Package Proposal, Review, Approval, and Publication
        |
        v
3. Separately Human-Authorized Environment Acquisition, Creation, and Startup
        |
        v
4. New PLAT-15.1A Initialization and Repository Source Implementation
        |
        v
5. Separately Authorized Offline Supported-Linux Validation Execution
        |
        v
6. Environment and Linux Evidence Acceptance
        |
        v
7. Separately Human-Authorized Shutdown and Deterministic Teardown
        |
        v
8. Architecture Gatekeeper Source Review
```

Success, approval, publication, or completion at one gate does not imply or authorize the next gate.

---

## Required Future Authorization and Publication Changes

After this proposal is successfully published, and before any environment can be downloaded, installed, created, started, or used, the next permitted activity is proposal and review of the following exact repository changes:

1. Propose `docs/milestones/Milestone_15/PLAT_15_1A_Supported_Linux_Validation_Environment_Preparation_Work_Package.md` as a subordinate PLAT-15.1A work package, not a new independent Product Backlog item. It must bind the complete static environment manifest, acquisition sources and checksums, named Platform Administrator or host owner, per-action host authorization contract, preparation-only administrative privilege, non-administrative execution identity, strict offline isolation checks, source/result transfer contracts, per-run execution-manifest schema, evidence schema, rollback, recovery, shutdown, teardown, and stop conditions.
2. Review that proposed work package through the Product Strategy Board and Architecture Gatekeeper. It remains unauthorized until separately approved and published.
3. Update the active PLAT-15.1A continuity brief only after that separate decision to record the exact published environment-preparation authority, continued `Not Started` implementation state, and next gate.
4. Create the governed initialization, completion, and qualifying generated-readiness evidence required for that future publication package.

Publishing this proposal does not create, approve, authorize, or publish the subordinate preparation work package. The filename above identifies the next proposal/review artifact only.

Do not modify ADR-012, AB-012, Registry records, deployment records, infrastructure state, source, tests, `go.mod`, or `go.sum` to authorize the environment prerequisite. Any future need to change those paths returns to the Product Strategy Board or Architecture Gatekeeper rather than expanding the prerequisite package.

The future package may authorize repository publication only after its exact validation and review gates pass. Normal publication remains a separate explicit action and must not imply environment preparation or host authorization.

---

## Exact Host Actions That Remain Unauthorized

This proposal does not authorize any person or tool to:

- select by execution, install, update, download, or acquire virtualization software, a Linux image, a Go toolchain, module content, or supporting package;
- create, import, clone, configure, start, resume, pause, stop, shut down, snapshot, inspect through use, or delete a VM;
- attach or create guest disks, transfer media, shared folders, devices, sockets, networks, credentials, secrets, or host integrations;
- use Docker, Podman, containerd, Kubernetes, Lima, Colima, CI, cloud, SSH, a remote runner, or a real or governed socket;
- alter host virtualization, networking, users, groups, permissions, services, daemons, sockets, credentials, or security settings;
- transfer source into an environment, execute PLAT-15.1A tests, export evidence, or remove environment state;
- implement PLAT-15.1A source or tests, change dependencies, stage, commit, push, tag, release, deploy, activate, or perform live work.

---

## Condition to Resume PLAT-15.1A Implementation Initialization

PLAT-15.1A implementation initialization may resume only when all of the following are true at the same time:

1. the Product Strategy Board has approved the bounded prerequisite direction and the decision is published;
2. the Architecture Gatekeeper has approved and published the future subordinate environment-preparation work package with every exact manifest value resolved;
3. separately authorized preparation has created the exact environment without prohibited access or drift;
4. environment-readiness evidence proves exact identity, native supported Linux, checksum integrity, daemon/socket/filesystem/network/credential isolation, offline test capability, source/result transfer controls, and executable teardown and recovery procedures;
5. the Architecture Gatekeeper has accepted that environment-readiness evidence for PLAT-15.1A use;
6. the human host owner has explicitly authorized the bounded environment use required by the implementation session;
7. a new Codex Implementation Engineer session fetches and proves local/tracking/live repository equality, completes repository-governed AI Session Initialization, classifies a `Clean` or qualifying `Expected Generated Evidence` baseline, reconciles unchanged PLAT-15.1A authority, and finds no stop condition.

If any condition is absent, expired, changed, ambiguous, or superseded, implementation remains `Not Started` and blocked.

---

## Decisions Recorded

### Product Strategy Board

Approved Option A as the bounded supported-Linux prerequisite architecture direction under existing PLAT-15.1A / PLAT-PB-013 authority. No new Product Backlog identifier is created, and no environment, implementation, operational, or host action is authorized by implication.

### Architecture Gatekeeper

Approved the Option A direction only, with a strictly offline guest, separate static environment and per-run execution manifests, named host authorization, preparation-only VM-local administrative privilege, non-administrative implementation/validation identity, and separate evidence, failure, recovery, and teardown gates. The subordinate environment-preparation work package remains uncreated and unapproved; Options C and D remain rejected, and Option B remains only a future candidate-specific fallback.

---

## Publication Gate

The proposal direction is approved, but the repository changes remain unstaged, uncommitted, and unpublished. Publication requires an exact approved changed-path inventory, repository-mandated validation, separate authorization to stage and commit, and a later separately authorized normal push followed by fetched local/tracking/live equality proof.

Proposal publication would publish architecture and planning evidence only. It would not create or approve the subordinate preparation work package and would not authorize environment acquisition or preparation, source implementation, Linux validation, evidence acceptance, teardown, artifact work, deployment, daemon interaction, observation, consumer work, recurrence, activation, release, or live work.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Recorded Product Strategy Board and Architecture Gatekeeper approval of Option A direction only; made the guest strictly offline; separated static environment and per-run execution manifests; required named host authorization, preparation-only administrative privilege, and non-administrative implementation/validation identity; retained the environment as Not Created and repository implementation as Not Started; and left the subordinate preparation work package uncreated and unapproved. |
| 0.1 | Proposed Option A as the bounded supported-Linux prerequisite direction, retained exact future manifest and host actions behind separate approval, rejected insufficient and authority-expanding alternatives, and preserved PLAT-15.1A as Not Started with every later gate closed. |
