# PLAT-15.1A - Supported-Linux Validation Environment Preparation Work Package

**Document Version:** 1.1

**Status:** Proposed

**Approval State:** Product Strategy Board and Architecture Gatekeeper Approved for Repository Publication

**Product Strategy Board Decision:** Version 1.1 Approved for Repository Publication under PLAT-15.1A / PLAT-PB-013 and AB-011; No New Backlog Identifier Warranted; Additional Gates Protect Delivery Leverage

**Architecture Gatekeeper Decision:** Version 1.1 Approved for Repository Publication

**Publication Readiness:** Validation Complete; Separate Staging/Commit Authorization Required

**Publication State:** Not Published

**Gate 2 State:** Not Authorized

**Environment State:** Not Created

**PLAT-15.1A Repository Implementation:** Not Started

**PLAT-15.1A State:** Blocked at Supported-Linux Initialization Gate

**Milestone:** Milestone 15

**Parent Authority:** PLAT-15.1A under PLAT-PB-013 and AB-011

**Independent Product Backlog Identifier:** None

---

## Purpose

This proposed subordinate work package defines the exact-manifest preparation contract for one task-specific, disposable, native ARM64 Linux virtual machine intended to satisfy the supported-Linux prerequisite of the published [PLAT-15.1A work package](PLAT_15_1A_Repository_Only_Socket_Capable_Privileged_Proxy_Source_Implementation_Work_Package.md).

It is a decision-ready proposal only. It does not approve or publish itself and does not authorize acquisition, download, installation, VM creation, startup, configuration, inspection through use, source ingress, PLAT-15.1A implementation, Linux validation, result export, shutdown, teardown, deletion, deployment, activation, release, or live work.

The Product Strategy Board retains product and portfolio authority. The Chief Architect / Architecture Gatekeeper retains architecture, security, residual-risk, readiness-evidence, and source-review authority. Every host-affecting action requires a separately recorded authorization from a named Platform Administrator or host owner.

---

## Governing State

- Environment remains `Not Created`.
- PLAT-15.1A repository implementation remains `Not Started`.
- PLAT-15.1A remains `Blocked at Supported-Linux Initialization Gate`.
- ADR-012 remains `Implemented: No`.
- AB-012 remains `Candidate - Remain Backlog`.
- The closed privileged-proxy architecture, Production Provider Adapter boundary, and every artifact, deployment, daemon-interaction, observation, consumer, recurrence, activation, release, and live gate remain unchanged.
- This package creates no Product Backlog identifier and is subordinate to PLAT-15.1A, PLAT-PB-013, and AB-011.
- Published Version 1.0 remains historical repository authority, but its Gate 2 topology and Ubuntu sequencing require correction. Version 1.1 is `Proposed`, approved by the Product Strategy Board and Architecture Gatekeeper for repository publication, and `Not Published`; separate staging/commit authority is next and push remains later. Acceptance record `plat15a-static-manifest-acceptance-001` is immutable historical evidence and `Acceptance Suspended Pending Revision` for execution eligibility. Gate 2 remains `Not Authorized`.

---

## Research Method and Evidence Boundary

Research was read-only and used canonical publisher pages, release metadata, checksum/signature metadata, package manifests, release histories, and vulnerability indexes accessed on 2026-07-25. No executable, installer, disk image, archive, module, package, or environment material was downloaded or retained. No artifact was installed, executed, imported, mounted, or inspected through use.

Publisher metadata is research evidence, not proof through possession. Every future artifact must be acquired only after separate authorization and verified again from canonical metadata before use.

---

## Canonical Research Register

| Subject | Publisher | Canonical source | Access date | Material evidence or limitation |
|---------|-----------|------------------|-------------|---------------------------------|
| UTM stable release | UTM project / Turing Software, LLC | `https://github.com/utmapp/UTM/releases/tag/v4.7.5` and `https://api.github.com/repos/utmapp/UTM/releases/tags/v4.7.5` | 2026-07-25 | Stable v4.7.5, build 118, published 2026-01-03; exact `UTM.dmg` size and GitHub asset digest recorded below. No detached publisher signature is listed. |
| UTM installation and features | UTM project | `https://docs.getutm.app/installation/macos/`, `https://docs.getutm.app/guest-support/linux/`, `https://docs.getutm.app/scripting/cheat-sheet/` | 2026-07-25 | GitHub DMG is an official installation path; ARM64 guests can run virtualized. UTM defaults can add a shared network, so configuration must be audited before first start. Sharing, clipboard, guest agent, scripting, server, and Rosetta features must remain disabled. |
| UTM publisher identity | Apple App Store | `https://apps.apple.com/us/app/utm-virtual-machines/id1538878817?mt=12` | 2026-07-25 | Developer and seller shown as Turing Software, LLC; the listing describes fully virtualized ARM64 Ubuntu on Apple silicon. The exact Developer ID certificate/team identity for the GitHub DMG remains acquisition-time evidence. |
| Apple virtualization and isolation | Apple | `https://developer.apple.com/documentation/virtualization/vzvirtualmachine`, `https://developer.apple.com/documentation/virtualization/vzvirtualmachineconfiguration/networkdevices`, `https://developer.apple.com/documentation/virtualization/creating-and-running-a-linux-virtual-machine` | 2026-07-25 | `VZVirtualMachine` executes the same architecture as the host. The network-device array defaults empty; network exists only when a network device is added. |
| macOS signature/notarization model | Apple | `https://support.apple.com/guide/security-pdf/app-code-signing-process-sec3ad8e6e53/web` | 2026-07-25 | Outside-App-Store applications use Developer ID signing and Apple notarization under default Gatekeeper policy. Acquisition must verify both without bypassing Gatekeeper. |
| Ubuntu image directory and manifest | Canonical / Ubuntu | `https://cdimage.ubuntu.com/ubuntu/releases/24.04/release/` and `https://cdimage.ubuntu.com/ubuntu/releases/24.04/release/ubuntu-24.04.4-live-server-arm64.manifest` | 2026-07-25 | Exact ARM64 ISO, timestamp, manifest, and ISO kernel package recorded below. |
| Ubuntu image checksum and signer | Canonical / Ubuntu | `https://cdimage.ubuntu.com/ubuntu/releases/24.04/release/SHA256SUMS`, `https://cdimage.ubuntu.com/ubuntu/releases/24.04/release/SHA256SUMS.gpg`, `https://documentation.ubuntu.com/security/software-integrity/image-verification/` | 2026-07-25 | Signed-checksum verification uses the Ubuntu CD Image Automatic Signing Key fingerprint recorded below. |
| Ubuntu support lifecycle | Canonical / Ubuntu | `https://documentation.ubuntu.com/release-notes/24.04/` | 2026-07-25 | Ubuntu 24.04 LTS standard security maintenance ends 2029-05-31. |
| Ubuntu kernel advisory | Canonical / Ubuntu | `https://ubuntu.com/security/notices/USN-8567-1` | 2026-07-25 | The 2026-07-20 notice fixes generic-kernel vulnerabilities in `6.8.0-136.136`; the ISO’s `6.8.0-100.100` kernel is not an acceptable final prepared-state kernel without a Gatekeeper-approved exception. |
| Ubuntu archive snapshots | Canonical / Ubuntu | `https://snapshot.ubuntu.com/` and `https://ubuntu.com/server/docs/how-to/software/snapshot-service/` | 2026-07-25 | Canonical supports timestamped Ubuntu archive snapshots for reproducible package states. Version 1.1 binds the advisory cutoff to snapshot `20260725T000000Z`, separates stable signed-release evidence from retained-inventory-derived component indexes, and leaves exact package material to a still-later gate. |
| Go toolchain identity | Go project | `https://go.dev/dl/?mode=json&include=all`, `https://go.dev/doc/devel/release`, `https://go.dev/rebuild` | 2026-07-25 | Go 1.26.5 is a stable supported security point release; exact Linux ARM64 archive metadata and reproducible-build evidence recorded below. |
| Go vulnerability process | Go project | `https://go.dev/doc/security/` and `https://go.dev/doc/security/vuln/database` | 2026-07-25 | Advisory state must be refreshed before acquisition and before the execution manifest is accepted. |
| `golang.org/x/sys` identity | Go project | `https://proxy.golang.org/golang.org/x/sys/@v/v0.47.0.info`, `https://github.com/golang/sys/tree/v0.47.0`, `https://sum.golang.org/lookup/golang.org/x/sys@v0.47.0`, `https://pkg.go.dev/golang.org/x/sys@v0.47.0` | 2026-07-25 | Exact tag revision, publication time, module sums, license, and maintenance origin recorded below. |
| `golang.org/x/sys` advisories | Go project | `https://vuln.go.dev/index/modules.json`, `https://pkg.go.dev/vuln/GO-2022-0493`, `https://pkg.go.dev/vuln/GO-2026-5024` | 2026-07-25 | Two indexed historical advisories are fixed before v0.47.0; absence of a current indexed advisory is not a guarantee against undisclosed defects. |

---

## Mechanism Alternatives

| Alternative | Assessment | Decision |
|-------------|------------|----------|
| UTM v4.7.5, build 118, Apple Virtualization backend | Official stable macOS application; native same-architecture VM; ISO boot; explicit removable disks; network, sharing, clipboard, Rosetta, and guest integrations can be omitted. Default wizard behavior requires a mandatory pre-start configuration audit. | Recommended, subject to the requested bounded acquisition-and-sealing amendment, exact acquired-artifact signature identity, host compatibility, and process evidence. |
| UTM v4.7.5 QEMU/HVF backend | Can virtualize `aarch64` with hardware acceleration, but adds an embedded QEMU process and broader emulated-device/configuration surface. | Rejected for this task unless Apple backend compatibility fails and the Gatekeeper approves a revised process/device model. |
| Custom application using Apple Virtualization framework | Offers the smallest device configuration, but requires new host software implementation, signing, build-tool acquisition, and maintenance outside this prerequisite. | Rejected as disproportionate new implementation. |
| VMware Fusion or another general desktop hypervisor | Adds broader networking, services, integration, update, licensing, and privileged-helper surface than required. | Rejected for this bounded disposable task. |
| Existing VM, hosted CI/runner, cross-compilation, Darwin-only testing, or user-mode emulation | Inherited-state or remote-authority risk, or failure to provide native Linux-kernel `SO_PEERCRED` and race evidence. | Retains the rejection or conditional-fallback state in the approved prerequisite proposal. |

---

## Recommended Exact Combination

Subject to the unresolved gates below, recommend:

1. UTM v4.7.5 build 118 from the official GitHub `UTM.dmg`, using the Apple Virtualization backend only.
2. Ubuntu Server 24.04.4 LTS ARM64 installed from `ubuntu-24.04.4-live-server-arm64.iso`.
3. A complete offline Ubuntu security baseline for every retained installed package, resolved from Canonical snapshot `20260725T000000Z` across `noble`, `noble-updates`, and `noble-security`, with no PPA or third-party repository. The final inventory must include generic kernel `6.8.0-136-generic`, package version `6.8.0-136.136`, and an offline no-change proof against the same snapshot.
4. Native `aarch64` execution with Apple binary translation/Rosetta disabled and absent.
5. Go `1.26.5` Linux ARM64 from the official archive.
6. `golang.org/x/sys` `v0.47.0` at source revision `9e7e939dcafac07e8ab4cffa6e5fc74908413f00`.
7. A VM with no network adapter at any lifecycle stage, no shared directory, no clipboard, no guest agent, no SSH use, no host socket, and no container-runtime surface.

The combination and corrected bounded acquisition-and-sealing architecture are approved for repository publication only. Version 1.1 remains `Not Published`. It authorizes no acquisition or preparation; each future action remains prohibited until this document is separately published and the named host owner separately authorizes that exact gate.

---

## Approved Bounded Acquisition-and-Sealing Architecture

Canonical public metadata did not independently establish the exact Developer ID common name and TeamIdentifier embedded in the GitHub UTM DMG. Exact retained-package closure also depends on the deterministic package inventory produced by the approved offline installation selection. Requiring both values before any acquisition would therefore be circular.

The Architecture Gatekeeper approved the following narrow architecture in version 0.2. Architecture approval is not action authority and authorizes no acquisition, networking, inspection, mounting, installation, execution, VM activity, or later gate in the current session.

1. **Stable artifact and signed-release-metadata acquisition:** after separate named-owner and Gatekeeper execution authorization, acquire only the exact UTM DMG; Ubuntu ISO, `SHA256SUMS`, and `SHA256SUMS.gpg`; Go Linux ARM64 archive; x/sys proxy objects and checksum metadata; and exact per-suite signed `InRelease`, or `Release` plus `Release.gpg`, for snapshot `20260725T000000Z`. No component-specific `Packages` index and no `.deb` file are authorized.
2. **Stable seal acceptance:** Gatekeeper separately accepts the exact UTM identity, Ubuntu image evidence, Go and module evidence, and per-suite signed Release/InRelease evidence. This acceptance makes no claim that component indexes, actual retained inventory, or package closure exists and opens only separately authorized host installation and offline base preparation.
3. **Actual retained installed-package inventory:** only during separately authorized offline VM base preparation, generate the inventory from the actual retained installed state. Do not infer it from ISO identity, installer defaults, documentation, expected selections, or prior experience. Export a sanitized inventory request through its own separately authorized gate.
4. **Component-index request, acquisition, and acceptance:** derive the exact suite/component set only from the actual retained inventory. Under separate owner authorization and Gatekeeper execution acceptance, acquire only the exact ARM64 indexes for that proved set; verify filename, compression form, size, SHA-256, and snapshot URL against the already accepted signed Release/InRelease records. Acquire no package material. Gatekeeper accepts the sealed component-index inventory before package planning.
5. **Offline package-plan generation and acceptance:** using only the accepted component indexes and actual retained inventory, calculate the complete candidate, dependency, and pre-dependency closure offline with no guest network fallback. Export and separately accept an exact package-material request binding every installed current version, selected version, architecture, suite/component, canonical snapshot URL, byte size, signed-index SHA-256, and dependency reason.
6. **Package-material acquisition and acceptance:** under a still-later separate owner authorization and Gatekeeper decision, acquire only the exact `.deb` files in the accepted package-material request. Verify every file against its accepted signed-index SHA-256, create immutable update media, and seal its inventory and digest. No substitution, mirror, PPA, third-party repository, live `apt` fallback, or additional package is allowed.

Each authority and acceptance is non-interchangeable; no approval or network authorization may cover two acquisition phases. Stable seal acceptance does not authorize component-index acquisition, component-index acceptance does not authorize package planning, package-plan acceptance does not authorize `.deb` acquisition, and package-material acceptance does not authorize update execution. All acquired material remains quarantined at exact protected-local targets until its next separately authorized use or teardown.

### Acquisition Network Boundary

Every separately authorized future acquisition must be allowlisted per object and fail closed:

- permit HTTPS `HEAD` or `GET` only to the exact canonical URL recorded in the accepted manifest;
- permit redirects only through the exact ordered HTTPS redirect chain separately recorded and approved for that object, including each scheme, hostname, port, and path constraint;
- permit DNS resolution only for the canonical and approved redirect hostnames; prohibit arbitrary browsing, search, package-manager network fallback, mirrors, proxies, credentials, cookies, telemetry, update checks, and unrelated endpoints;
- reject HTTP downgrade, hostname/path drift, an unapproved redirect, changed object identity, authentication request, or any response whose size/hash differs from the manifest;
- record sanitized request URL identities, redirect identities, response status, content length, timestamps, and final SHA-256 without retaining signed query credentials or personal host/network data; and
- require a new named-host authorization and amended redirect manifest for any additional destination, even when controlled by the same publisher.

UTM notarization verification must first use stapled and offline evidence from the read-only acquired object, including `xcrun stapler validate`, code-signing chain/designated-requirement inspection, and offline Gatekeeper assessment where supported. If the ticket is absent, invalid, or the verification tooling requires an additional Apple endpoint, stop. Any Apple network verification requires a separate authorization naming the exact endpoint/redirect boundary; it is not implied by UTM acquisition authority.

---

## Static Environment Manifest

The approved future static manifest must be immutable, canonical JSON and include every field below. A single SHA-256 digest of its canonical bytes becomes `static_environment_manifest_sha256`.

### Virtualization Mechanism

| Field | Bound value |
|-------|-------------|
| Product | UTM |
| Version/build | `4.7.5` / `118` |
| Publisher | UTM project; application publisher expected to be Turing Software, LLC |
| Release tag/source revision | `v4.7.5`; `048ca7498ea3a374439149d51739d94c5300bcda` |
| Package | `UTM.dmg` |
| Canonical URL | `https://github.com/utmapp/UTM/releases/download/v4.7.5/UTM.dmg` |
| Size | `250021057` bytes |
| SHA-256 | `a8435c93cfb5f8bbfeea4b134cfad1ac66b67632b75e438c63b1a8ae043bef0e` |
| Backend | Apple Virtualization / `VZVirtualMachine`; no QEMU backend |
| Signature model | Verify SHA-256, Developer ID code signature, designated requirement, TeamIdentifier, hardened runtime, and Apple notarization/Gatekeeper acceptance; do not use a Gatekeeper bypass |
| Expected signer identity | Public official sources establish Turing Software, LLC as publisher but do not independently establish the GitHub DMG’s exact Developer ID common name or TeamIdentifier. The approved bounded artifact-identity sealing architecture establishes them from the separately authorized read-only acquired object; the artifact-derived values become immutable expected values only after Gatekeeper acceptance and before installation. |
| Signer mismatch behavior | Any common-name, TeamIdentifier, chain, designated-requirement, notarization, hardened-runtime, entitlement, or publisher mismatch stops. It may not be waived during acquisition or installation. |
| Support status | Latest stable UTM release on access date; no publisher LTS or end-of-support date was found |
| Host privilege | No persistent privileged daemon or kernel extension is permitted; any installation write requiring host administration is separately authorized |
| Process model | Named owner’s interactive UTM application using Apple Virtualization; UTM Server, remote control, automatic startup, headless persistence, and background survival disabled |
| No-daemon proof | Before install and after quit: exact `launchctl` system/user inventories, process inventory, listening socket inventory, installed helper inventory, and UTM preferences show no persistent UTM privileged daemon or server |

### Linux Distribution and Kernel

| Field | Bound value |
|-------|-------------|
| Distribution | Ubuntu Server 24.04.4 LTS (Noble Numbat) |
| Architecture | ARM64 / AArch64 |
| Image | `ubuntu-24.04.4-live-server-arm64.iso` |
| Canonical URL | `https://cdimage.ubuntu.com/ubuntu/releases/24.04/release/ubuntu-24.04.4-live-server-arm64.iso` |
| Image last modified | `2026-02-10T06:57:51Z` |
| Signed checksum publication | `2026-02-12T14:52Z` |
| Size | `3059724288` bytes |
| SHA-256 | `9a6ce6d7e66c8abed24d24944570a495caca80b3b0007df02818e13829f27f32` |
| Checksum signer | Ubuntu CD Image Automatic Signing Key (2012), `cdimage@ubuntu.com` |
| Signer fingerprint | `843938DF228D22F7B3742BC0D94AA3F0EFE21092` |
| Verification | Verify trusted key fingerprint, `gpgv` signature of `SHA256SUMS.gpg` over `SHA256SUMS`, then SHA-256 of the ISO before first attachment and after every transfer |
| ISO kernel | `linux-image-6.8.0-100-generic` package `6.8.0-100.100` |
| Security advisory cutoff | `2026-07-25T00:00:00Z`; Canonical snapshot ID `20260725T000000Z` |
| Allowed suites | `noble`, `noble-updates`, and `noble-security`; only components required by retained installed packages; no `noble-backports`, PPA, or third-party repository |
| Stable signed archive metadata | Exact per-suite snapshot `InRelease`, or `Release` plus `Release.gpg` where applicable, must be verified with the Ubuntu archive keyring and bound by filename, suite, size, SHA-256, signer fingerprint, and canonical snapshot URL. Gate 2 includes no component-specific `Packages` index. |
| Later component indexes | Exact ARM64 indexes may be requested only after actual retained-inventory export. Each filename, compression form, size, SHA-256, suite/component, and snapshot URL must verify against accepted signed Release/InRelease evidence under separate owner authorization and Gatekeeper acceptance. |
| Required complete update | Offline `full-upgrade` of every retained installed package to the candidate from the exact snapshot, including complete dependency and pre-dependency closure; kernel-only remediation is prohibited |
| Required final kernel | The complete baseline must include `linux-image-6.8.0-136-generic` package `6.8.0-136.136`; `uname -r` must return `6.8.0-136-generic` |
| Exact package bundle | Generated only through the bounded offline package-plan and package-material sealing gates. The immutable manifest must bind every retained package’s before/after version, architecture, source package, suite/component, canonical snapshot URL, byte size, signed-index SHA-256, dependency reason, and media path. Any missing retained package, dependency, hash, or index binding stops. |
| Post-update inventory | Canonical `dpkg-query` inventory and per-package status, held-package inventory, removed-package inventory, update-media digest, and `apt-get --simulate full-upgrade` result against the same sealed snapshot. Acceptance requires zero upgrades, installs, removals, held packages, missing dependencies, unauthenticated packages, and repository fallbacks. |
| Support period | Standard security maintenance through 2029-05-31 |
| Security limitation | The point-release ISO predates USN-8567-1 and other post-image updates. No environment-readiness acceptance is possible on the ISO package state. Version 1.1 requires the complete signed offline snapshot baseline above, not only kernel `6.8.0-136.136`. Advisory status must be refreshed before each acquisition and readiness acceptance. |

### Go Toolchain

| Field | Bound value |
|-------|-------------|
| Version | Go `1.26.5` |
| Archive | `go1.26.5.linux-arm64.tar.gz` |
| Canonical URL | `https://go.dev/dl/go1.26.5.linux-arm64.tar.gz` |
| Size | `63759990` bytes |
| SHA-256 | `fe4789e92b1f33358680864bbe8704289e7bb5fc207d80623c308935bd696d49` |
| Verification | Compare official JSON metadata, SHA-256 before and after ingress, extract only during authorized preparation, and require `go version go1.26.5 linux/arm64` |
| Signature model | Official HTTPS download metadata plus SHA-256; no detached signature is advertised |
| Advisory status | Stable supported release dated 2026-07-07; includes security fixes to `crypto/tls` and `os`; official reproducible-build report records PASS for the Linux ARM64 archive |
| Local-only controls | `GOTOOLCHAIN=local`, `GOENV=off`, `GOPROXY=file:///opt/plat15a/goproxy,off`, `GOSUMDB=off`, `GOVCS=*:off`, `GOFLAGS=-mod=readonly`, and an empty network-device inventory |

### `golang.org/x/sys`

| Field | Bound value |
|-------|-------------|
| Module/version | `golang.org/x/sys` `v0.47.0` |
| Publication time | `2026-06-30T17:07:31Z` |
| Canonical VCS | `https://go.googlesource.com/sys` |
| Tag/revision | `refs/tags/v0.47.0`; `9e7e939dcafac07e8ab4cffa6e5fc74908413f00` |
| Module sum | `h1:o7XGOvZQCADBQQ4Y7VNq2dRWQR7JmOUW8Kxx4ZsNgWs=` |
| `go.mod` sum | `h1:4GL1E5IUh+htKOUEOaiffhrAeqysfVGipDYzABqnCmw=` |
| Required future `go.sum` lines | `golang.org/x/sys v0.47.0 h1:o7XGOvZQCADBQQ4Y7VNq2dRWQR7JmOUW8Kxx4ZsNgWs=` and `golang.org/x/sys v0.47.0/go.mod h1:4GL1E5IUh+htKOUEOaiffhrAeqysfVGipDYzABqnCmw=` |
| License | BSD-3-Clause |
| Maintenance | Go project sub-repository; v0.47.0 was the latest tag on access date |
| Advisory status | GO-2022-0493 fixed before `v0.0.0-20220412211240-33da011f77ad`; GO-2026-5024 fixed in `v0.44.0`; v0.47.0 is outside both affected ranges |
| Offline cache | Future authorized acquisition creates a file-based proxy containing only exact `.info`, `.mod`, and `.zip` entries plus a manifest. The guest cache is primed from that proxy; no proxy, sumdb, VCS, or toolchain network fallback exists. |
| Drift behavior | Any different version/revision/sum, missing proxy entry, new transitive module, `go.mod`/`go.sum` mismatch, or attempted retrieval fails closed and returns to Gatekeeper review. |

---

## VM and Isolation Configuration

| Control | Required value |
|---------|----------------|
| Task instance | `plat-15-1a-linux-001`; this is an environment instance label, not a Product Backlog identifier |
| VM name | `PLAT-15.1A-LINUX-ARM64-001` |
| CPU | 4 virtual CPUs, native ARM64 |
| Memory | 8 GiB |
| Primary disk | 32 GiB sparse raw disk, exact path under the approved `HOST_TASK_ROOT` |
| Boot | UEFI; Ubuntu ARM64 ISO read-only during installation only |
| Network devices | Empty array before first start and for every later start |
| Loopback | Guest `lo` only; no non-loopback interface may be present |
| Translation | Rosetta and every x86/amd64 translation or emulation feature disabled and absent |
| Sharing | No VirtioFS, VirtFS, WebDAV, shared folder, clipboard, drag/drop, guest agent, SPICE agent, QEMU agent, SSH ingress/egress, remote control, or UTM Server |
| Sockets/devices | No host socket, vsock, governed socket, USB sharing, host credential, secret, customer data, sensitive host directory, or container-runtime device |
| Container surface | Docker, Podman, containerd, Kubernetes, CLIs, SDKs, services, sockets, groups, and environment variables absent |
| Installation selection | No SSH server role; after installation `openssh-server`, container-runtime packages, guest agents, and sharing agents must be absent before readiness |
| Persistence | Only the exact VM bundle, disks, manifests, and authorized media under `HOST_TASK_ROOT`; no snapshots, clones, saved states, auto-start, or shared caches |

`HOST_TASK_ROOT` means the Gate 2 task root itself, never a retained ancestor and never a parent for another redundant `gate-2` wrapper. Its exact nested acquisition and sealed hierarchy is governed by the Version 1.1 Gate 2 package. `HOST_TASK_ROOT`, the personal host-owner identity, the UTM installation target, and every absolute descendant path belong only in the protected local host-action manifest described below. The repository static manifest retains sanitized identifiers and the protected manifest’s SHA-256 digest, never personal names, usernames, home paths, machine identifiers, or absolute host paths. Retained ancestor containers are distinct non-deletion targets. A home directory, repository root, `/`, wildcard, symlinked target, broad shared directory, or flattened alias is never a permitted deletion target or conformant path substitute.

### Protected Local Host-Action Manifest

The separately authorized host owner maintains an access-controlled canonical JSON manifest outside Git. It binds the personal host-owner identity and authorization record, exact host/machine identity, exact absolute acquisition/install/task/media/output/teardown paths, ownership and permissions, UTM machine identifier, raw-disk names, and exact deletion targets.

Repository evidence may retain only sanitized stable identifiers such as `host-owner-authorization-001` and `host-task-root-001`, the protected manifest schema version, its SHA-256 digest, and a pass/fail statement that the named authority verified it. The repository must not retain the manifest, personal identity, username, host serial/UUID, home path, absolute path, IP/MAC address, credential, secret, or reversible mapping. Any digest drift invalidates all dependent authorization and evidence.

---

## Privilege and Identity Model

1. The future decision must name the Platform Administrator or host owner. No placeholder name authorizes action.
2. Every acquisition, verification, install, directory/media creation, VM definition, first start, preparation start, readiness start, source-use start, export, shutdown, and deletion step requires its own recorded human authorization.
3. Host privilege is limited to the exact approved action. Persistent privileged helpers, daemons, kernel extensions, group changes, security-control bypasses, and broad filesystem permissions are prohibited.
4. VM-local administrative privilege exists only in separately authorized preparation under identity `platprep`.
5. Preparation creates `platrun` with UID/GID `1501`, no administrative or supplemental privileged groups, no sudo rule, no SSH key, no password reuse, and no host identity mapping.
6. Before readiness evidence export, root is locked for interactive login, `platprep` is removed or locked and removed from sudo, and `platrun` is the only guest Linux validation identity.
7. PLAT-15.1A repository implementation occurs only in the governed host repository worktree under the separately initialized Codex Implementation Engineer role and repository governance. It does not occur in the guest and does not use `platrun`.
8. The completed, still-governed host-worktree source diff is packaged only after repository implementation and its host-side validations complete. `platrun` may copy that approved source from read-only media into the guest-local validation directory and run the exact Linux validation manifest; it may not author, modify, repair, or commit source.
9. Guest Linux validation must fail if effective UID is 0, `sudo` succeeds, `platrun` has an unauthorized group/capability/namespace/device/mount/socket, or the guest-local source differs from the per-run execution-manifest digest.

---

## One-Way Transfer Design

### Host-to-Guest Source Ingress

- Preparation material and each later source run use separate read-only ISO-9660 media.
- The preparation ISO may contain only the verified Go archive, exact offline module-proxy entries, static manifest, and their checksums.
- A stable archive-metadata ISO may contain only the accepted per-suite signed Canonical `InRelease`, or `Release` plus `Release.gpg`; it contains no component-specific index.
- After actual retained-inventory export and separate component-index acquisition/acceptance, a different component-index ISO may contain only the exact accepted ARM64 indexes for the proved suite/component set and their sealed manifest.
- A separate security-update ISO may contain only the exact accepted `.deb` closure, local file-repository metadata, sealed package manifest, and checksums.
- A later execution ISO contains a repository archive produced from the exact per-run execution manifest, the manifest itself, and checksums. It contains no `.git`, credentials, secrets, customer data, environment files, caches, sockets, or personal host paths.
- Media is attached read-only while the VM is stopped, verified in-guest, copied to a VM-local task directory, unmounted, and detached while the VM is stopped before any readiness or Linux validation begins. Failure to prove detachment is a hard stop; no validation command may run with preparation, security-update, toolchain/module, or source ingress media attached.
- No shared folder, clipboard, SSH, agent file transfer, network, USB device, or persistent bidirectional channel is permitted.

### Guest-to-Host Sanitized Evidence Egress

Readiness and execution evidence use different, single-use result media. Capacity is derived from the evidence contract’s allowlisted maximum bytes and filesystem overhead, not left open:

| Medium | Evidence byte contract | Bound image |
|--------|------------------------|-------------|
| Component-index request | canonical actual retained-package inventory 4 MiB; suite/component derivation 1 MiB; checksums/export metadata 1 MiB | 8 MiB raw FAT16 `PLAT15A_INDEX_REQUEST_001.img`, label `PLAT15IDX` |
| Package request | canonical retained-package plan 4 MiB; signed-metadata digest inventory 1 MiB; checksums/export metadata 1 MiB | 8 MiB raw FAT16 `PLAT15A_PACKAGE_REQUEST_001.img`, label `PLAT15PKG` |
| Readiness evidence | readiness manifest 4 MiB; package/isolation inventories 12 MiB; bounded logs 8 MiB; checksums/export metadata 4 MiB | 32 MiB raw FAT16 `PLAT15A_READINESS_RESULTS_001.img`, label `PLAT15RDY` |
| Execution evidence | execution manifest 4 MiB; T-01 through T-12 logs 12 MiB; Go/race/fuzz logs 16 MiB; Python source-validation logs 8 MiB; isolation/inventory evidence 16 MiB; checksums/export metadata 4 MiB | 64 MiB raw FAT32 `PLAT15A_EXECUTION_RESULTS_001.img`, label `PLAT15EXE` |

- Each image is separately authorized, attached only to the applicable export gate, and contains only its evidence kind under `PLAT15A_INDEX_REQUEST/`, `PLAT15A_PACKAGE_REQUEST/`, `PLAT15A_READINESS/`, or `PLAT15A_EXECUTION/`.
- The guest writes the approved canonical manifest, allowlisted sanitized logs/reports, and `SHA256SUMS`, then unmounts the image, records block-device identity and checksum, and shuts down before host access.
- The host detaches the image from the stopped VM and mounts it read-only for sanitization verification and copying.
- Readiness evidence must be exported and host-verified before readiness evidence acceptance. Execution evidence must be exported and host-verified before source-evidence acceptance.
- A byte-contract overrun, image-capacity change, mixed evidence kind, unexpected file, remount failure, or sanitization failure stops. Capacity changes require a revised evidence contract and Gatekeeper review.
- Reattachment after host read is prohibited. Any correction uses a new separately authorized medium with a new identifier and export attempt.
- Media creation must verify the intended FAT type from the on-disk boot sector and a structural read-only reopen. Component-index-request, package-request, and readiness media fail if formatted as FAT32; execution media fails unless it is FAT32. Filesystem or capacity substitution requires Gatekeeper review.

### Complete Offline Security-Baseline Procedure

1. Install the exact minimal server selection from the verified ISO with no network device and record the canonical actual retained-package inventory under preparation administration.
2. Export only that actual inventory and deterministic suite/component derivation on the dedicated 8 MiB component-index-request medium; shut down, host-verify, sanitize, and obtain Gatekeeper request acceptance before any component-index network authority is prepared.
3. Under separate owner authorization and Gatekeeper execution acceptance, acquire and seal only the exact ARM64 component indexes named by the accepted request. Verify every filename, compression form, size, SHA-256, and snapshot URL against the already accepted signed Release/InRelease evidence. Acquire no `.deb` file.
4. Obtain separate Gatekeeper acceptance of the sealed component-index inventory, then attach its dedicated read-only ISO while the VM is stopped.
5. With no guest network adapter or fallback, use only the accepted component indexes and actual retained inventory to calculate the complete `full-upgrade` candidate, dependency, and pre-dependency closure for snapshot `20260725T000000Z`.
6. Export the exact canonical package-material plan on the dedicated 8 MiB package-request medium, shut down, and complete host sanitization and Gatekeeper plan acceptance before any package-material acquisition.
7. Under a still-later separate owner authorization and Gatekeeper decision, acquire and seal only the accepted request's exact `.deb` objects; following acceptance, attach the immutable security-update ISO read-only. Configure APT to the ISO file repository only, prohibit unauthenticated packages and every network fallback, and execute the accepted complete update under `platprep`.
8. Record the exact before/after/removed/held inventory, archive signer/index bindings, installed `.deb` hashes, and update results. An unexpected plan change, extra/missing package, held package, dependency substitution, script failure, or hash mismatch stops. Run an offline same-snapshot `full-upgrade` simulation; it must report zero upgrades, installs, removals, held packages, missing dependencies, and unauthenticated packages.
9. Unmount and detach all preparation, stable-metadata, component-index, update, and installer media while the VM is stopped. Only after detachment proof passes may identity lockdown and readiness validation begin.

---

## Separate Manifests

### Immutable Static Environment Manifest

The preparation work package binds mechanism, publisher, sealed artifact manifests, checksums/signatures, VM hardware, device exclusions, complete OS security baseline, toolchain, offline module proxy, privilege model, isolation checks, distinct transfer-media formats and capacities, evidence schema, failure behavior, rollback, recovery, and sanitized teardown identifiers. It binds the protected local host-action manifest schema and digest but never its personal identity or absolute-path contents. It must not contain a future repository HEAD or implementation diff.

### Per-Run Execution Manifest

Each later implementation/validation run must separately bind:

- local, fetched tracking, and live remote repository commit;
- repository tree;
- exact scoped implementation diff digest and changed-path inventory;
- source ISO filename, byte size, and SHA-256;
- static environment manifest digest and accepted environment-readiness evidence digest;
- exact T-01 through T-12 mapping and race/fuzz commands;
- bounded execution identity and task directories;
- separate execution-result image identity, fixed 64 MiB capacity, byte-contract allocation, and sanitization policy;
- named human authorizations for start, use, export, shutdown, and teardown.

Any repository, source, test, dependency, toolchain, image, kernel, configuration, or authorization drift invalidates the execution manifest. It may not be patched in place.

---

## Environment-Readiness Gate

Readiness is a separately authorized preparation result, not PLAT-15.1A implementation or Linux test execution. It must prove:

1. exact UTM version/build, signature/notarization result, configured backend, and no persistent privileged daemon/server;
2. exact VM name, machine identifier, configuration digest, CPU/memory/disk values, and empty network/socket/share/clipboard/agent/USB device inventories;
3. `uname -s` = `Linux`, `uname -m` = `aarch64`, and `uname -r` = `6.8.0-136-generic`;
4. Ubuntu release `24.04.4 LTS`, complete retained-package before/after inventory, signed snapshot `20260725T000000Z` metadata/package bindings, zero held or unauthenticated packages, `linux-image-6.8.0-136-generic=6.8.0-136.136`, and a same-snapshot offline no-change simulation;
5. `go version go1.26.5 linux/arm64`, exact GOROOT digest inventory, `GOTOOLCHAIN=local`, and no retrieval fallback;
6. exact x/sys file-proxy entries, source revision, module sums, and no additional module;
7. only loopback exists and no network adapter, route, DNS resolver path, listening IP socket, or network-capable test configuration exists;
8. absence of Docker, Podman, containerd, Kubernetes, runtime sockets, governed sockets, SSH service/use, guest agents, shared mounts, clipboard, host credentials, secrets, customer data, and sensitive host resources;
9. `platrun` UID/GID 1501 is non-administrative and cannot use sudo or acquire privilege;
10. every preparation/security/source ingress medium is detached before validation, and the 32 MiB readiness-result medium works only in its designed direction and lifecycle;
11. adequate CPU, memory, disk, file-descriptor, process, and temporary-path limits for T-01 through T-12, supported-Linux race tests, bounded fuzz, and repository validation;
12. deterministic failure, recovery, export sanitization, shutdown, teardown, and exact absence-verification procedures are executable.

The complete readiness evidence must first be exported on the dedicated readiness medium, host-verified and sanitized, and only then presented for Architecture Gatekeeper acceptance. Gatekeeper acceptance is required before a new PLAT-15.1A repository implementation initialization may begin.

---

## Host and Guest Validation Contract

After readiness acceptance, PLAT-15.1A repository implementation occurs in the governed host worktree under a new fetched and synchronized initialization. The source ISO excludes `.git`; therefore Git/repository-state validation is host-only and may not be represented as guest evidence.

### Host-Only Repository Validation

Before source-media creation, the governed host worktree must run and retain:

- exact repository identity, branch, HEAD/tree, tracking/live-remote equality, changed-path, diff-digest, staging, and untracked-state checks;
- `python3 -m pytest -p no:cacheprovider engineering/tests`;
- `./platform-eap repository validate`;
- `./platform-eap governance validate`;
- `./platform-eap release readiness`;
- `./platform-eap milestone closeout`;
- `./platform-eap engineering metrics`;
- `./platform-eap capabilities` and `./platform-eap registry validate`;
- `./platform-eap ai-session readiness`;
- documentation link, secret, hygiene, symlink, `git diff --check`, and applicable staged-whitespace checks; and
- the approved host-platform Go checks required by the implementation work package.

These results remain host evidence and are referenced by digest in the per-run execution manifest. They are not copied into the guest as claims of guest execution.

### Guest Linux Validation

Only after host implementation and host validation complete may the exact source archive and execution manifest be transferred on read-only source media. After mandatory media detachment, `platrun` validates—but never authors or repairs—the exact guest-local source by running:

- T-01 through T-12 with no host-dependent skip;
- `go mod verify` with `GOTOOLCHAIN=local`, `GOPROXY=off`, `GOSUMDB=off`, `GOVCS=*:off`, and retrieval disabled;
- `go test ./...`;
- `go test -race ./...` with the sealed native compiler/libc closure;
- approved bounded fuzz/corpus checks;
- `./platform-eap privileged-proxy source validate` and `./platform-eap privileged-proxy source static-safety` using the sealed Python standard-library runtime; and
- pre/post isolation, process, mount, device, socket, package, privilege, media-detachment, architecture, and resource checks.

The guest must not run or claim Git/tracking/live-remote, repository/governance/release/milestone/readiness/metrics/capabilities/Registry, full Python engineering-suite, documentation-link, or staged-working-tree validation. Those checks require the governed host worktree or are not Linux-specific.

### Guest Executable and Ubuntu Package Closure

The signed snapshot package plan must include every exact dependency of each guest-required executable. At minimum, it must bind these logical roots and their complete dependency/pre-dependency closure at snapshot `20260725T000000Z`:

| Guest purpose | Executable | Package or sealed source |
|---------------|------------|--------------------------|
| Go build/test/race/fuzz | `/usr/local/go/bin/go`, Go tools under exact GOROOT | verified Go 1.26.5 Linux ARM64 archive |
| Native race/cgo support | `/usr/bin/cc`, `/usr/bin/gcc`, linker/assembler, libc headers | `build-essential` and its exact signed Ubuntu closure |
| Source static validation | `/usr/bin/python3` | `python3`, `python3-minimal`, and exact signed Ubuntu closure; Python standard library only, no PyPI package |
| Linux syscall evidence | `/usr/bin/strace` | `strace` |
| Interface/socket evidence | `/usr/sbin/ip`, `/usr/bin/ss` | `iproute2` |
| Process/open-file evidence | `/usr/bin/ps`, `/usr/bin/lsof` | `procps`, `lsof` |
| Media/mount evidence | `/usr/bin/lsblk`, `/usr/bin/findmnt`, `/usr/bin/mount`, `/usr/bin/umount` | `util-linux` and exact closure |
| Package/inventory evidence | `/usr/bin/dpkg-query`, `/usr/bin/apt-get` during preparation only | `dpkg`, `apt` and exact closure |
| Bounded shell/file/hash operations | `/bin/sh`, `/bin/bash`, `env`, `timeout`, `uname`, `id`, `stat`, `sha256sum`, `find`, `grep`, `sed`, `awk`, `tar`, `file` | `dash`, `bash`, `coreutils`, `findutils`, `grep`, `sed`, `mawk`, `tar`, `file` and exact closure |

The sealed manifest records exact package versions, architectures, signed-index hashes, installed executable paths, executable SHA-256 values, and post-update inventory. A missing executable/package, PyPI or network dependency, unsealed transitive dependency, compiler/runtime mismatch, or attempted retrieval is a hard stop.

The run must include syscall-observing proof for native Linux `AF_UNIX` and kernel-returned `SO_PEERCRED`. No real daemon, governed socket, Docker path, IP network, artifact, deployment, Registry mutation, observation, activation, release, or live operation may occur.

Any skip, failure, timeout, race, unexpected package/process/socket/mount, network evidence, dependency miss, or evidence ambiguity fails the run. It does not authorize repair, network enablement, reacquisition, restart, rerun, or scope expansion.

---

## Evidence and Sanitization Schema

Every readiness or later execution result must use canonical JSON. The evidence kinds and result media may not be combined. Each schema includes:

- `schema_version`;
- `evidence_kind`;
- `task_instance`;
- `static_environment_manifest_sha256`;
- optional `execution_manifest_sha256`;
- `started_at_utc` and `completed_at_utc`;
- sanitized authorization record identifiers and protected-local-manifest digest, without personal identity, absolute host paths, credentials, or signatures containing secrets;
- exact mechanism, VM, OS, kernel, architecture, toolchain, module, repository, tree, source-diff, media, fixture, and corpus identities;
- pre/post isolation observations;
- command identifier, exit code, result, duration, and bounded sanitized output digest;
- T-01 through T-12 result map;
- race/fuzz/validator result map;
- evidence-kind-specific export-medium identity, capacity, byte-contract allocation, inventory, and per-file SHA-256;
- shutdown/teardown state where separately authorized;
- limitations, unresolved risks, and stop reason.

Sanitization must remove personal host paths, usernames, host identifiers, IP/MAC addresses, credentials, secrets, environment values, customer data, raw process command lines unrelated to the task, and unbounded test output. Repository-relative paths, package identities, public checksums, synthetic fixture identifiers, numeric guest UID/GID 1501, and exact governed command names may remain.

Export fails closed if a file is not allowlisted, a secret/hygiene scan fails, a path is absolute or personal, output is unbounded, or the manifest and file checksums disagree.

---

## Authorization Sequence

Each row is a separate gate. Approval or success at one row does not imply the next.

| Gate | Required decision or authorization | Result opened |
|------|------------------------------------|---------------|
| 1. Version 1.1 repository proposal publication | Separate publication preparation, staging/commit, and push decisions complete | Corrected repository authority only |
| 2. Stable artifact and signed-release-metadata acquisition/sealing | Replacement static-manifest acceptance plus exact named-owner and Gatekeeper execution authorization for one stable-artifact run | Sealed UTM, Ubuntu image, Go/module, and per-suite signed-release evidence only; no index, package, install, or VM authority |
| 3. Stable seal acceptance | Gatekeeper accepts UTM identity, Ubuntu image evidence, Go/module evidence, and signed Release/InRelease evidence | Eligibility for exact host preparation only |
| 4. Host installation and preparation-media creation | Named host owner authorizes exact protected-local paths and commands | Host preparation only |
| 5. VM creation and offline base preparation | Named host owner authorizes exact VM, devices, disks, start, preparation-admin use, and observation of actual retained installed state | Base preparation and actual retained-inventory generation only |
| 6. Component-index-request export and host verification | Named host owner authorizes the dedicated request medium; actual retained inventory, derivation, sanitization, checksums, and media lifecycle pass | Component-index request eligible for Gatekeeper review only |
| 7. Component-index acquisition/sealing | Gatekeeper accepts the request; named owner and Gatekeeper separately authorize one exact index-acquisition run | Sealed exact ARM64 indexes for the proved suite/component set only; no `.deb` material |
| 8. Component-index acceptance | Gatekeeper accepts the sealed index inventory against stable signed-release evidence | Eligibility for offline package-plan generation only |
| 9. Offline package-plan generation and export | Named host owner authorizes offline calculation from accepted indexes and actual inventory plus dedicated request-medium export | Exact package-material request eligible for Gatekeeper review only |
| 10. Package-plan acceptance | Gatekeeper accepts the complete candidate, dependency, and pre-dependency closure | Eligibility to prepare exact `.deb` acquisition authority only |
| 11. Package-material acquisition/sealing | Named owner and Gatekeeper authorize one exact network run for only the accepted request's `.deb` objects | Sealed package material eligible for review only |
| 12. Package-material acceptance | Gatekeeper accepts every `.deb` against the accepted signed index and sealed-media inventory | Exact offline security-update material only |
| 13. Complete offline security update and readiness run | Named host owner authorizes exact update media, preparation, identity lockdown, readiness checks, and dedicated 32 MiB readiness-result medium | Readiness evidence generation/export only |
| 14. Readiness-evidence export and host verification | Named host owner authorizes export; sanitization, byte contract, checksums, and media lifecycle pass | Readiness evidence eligible for Gatekeeper review |
| 15. Environment-readiness acceptance | Gatekeeper accepts the already exported exact readiness evidence | Eligibility for new PLAT-15.1A repository initialization |
| 16. PLAT-15.1A repository implementation initialization | Repository fetch/synchronization and governed initialization pass | Governed host-worktree implementation only; no guest use |
| 17. Governed repository implementation | Approved role completes exact scoped host-worktree source and host validation; repository remains governed and uncommitted | Eligibility to prepare one per-run source/execution manifest |
| 18. Offline Linux validation | Separate execution manifest and named host authorization; source media detached before validation | Exact guest validation run only under `platrun` |
| 19. Execution-evidence export and host verification | Named host owner authorizes dedicated 64 MiB execution-result medium; sanitization, byte contract, checksums, and lifecycle pass | Execution evidence eligible for Gatekeeper review |
| 20. Source-evidence acceptance | Gatekeeper accepts the already exported source/validation evidence | Source-review eligibility only |
| 21. Shutdown and teardown | Named host owner authorizes exact stopped VM and protected-local deletion targets | Exact teardown only; retained ancestor containers excluded |
| 22. Architecture Gatekeeper source review | Gatekeeper reviews governed repository source and accepted evidence | Acceptance, rejection, or revision decision only |

---

## Version 1.0 to Version 1.1 Gate Migration

| Version 1.0 gate | Version 1.1 gate or disposition |
|------------------|---------------------------------|
| 1. Repository proposal publication | 1. Version 1.1 repository proposal publication |
| 2. Artifact and archive-metadata acquisition/sealing | 2. Stable artifact and signed-release-metadata acquisition/sealing; component indexes removed |
| 3. Gatekeeper seal acceptance | 3. Stable seal acceptance; no claim of component indexes or package closure |
| 4. Host installation and preparation-media creation | 4. Host installation and preparation-media creation |
| 5. VM creation and offline base preparation | 5. VM creation and offline base preparation; limited to actual retained-inventory generation before package planning |
| No Version 1.0 equivalent | 6. Component-index-request export and host verification |
| No Version 1.0 equivalent | 7. Component-index acquisition/sealing |
| No Version 1.0 equivalent | 8. Component-index acceptance |
| 6. Offline package-request export | 9. Offline package-plan generation and export plus 10. Package-plan acceptance |
| 7. Package-material acquisition/sealing | 11. Package-material acquisition/sealing plus 12. Package-material acceptance |
| 8. Complete offline security update and readiness run | 13. Complete offline security update and readiness run |
| 9. Readiness-evidence export and host verification | 14. Readiness-evidence export and host verification |
| 10. Environment-readiness acceptance | 15. Environment-readiness acceptance |
| 11. PLAT-15.1A repository implementation initialization | 16. PLAT-15.1A repository implementation initialization |
| 12. Governed repository implementation | 17. Governed repository implementation |
| 13. Offline Linux validation | 18. Offline Linux validation |
| 14. Execution-evidence export and host verification | 19. Execution-evidence export and host verification |
| 15. Source-evidence acceptance | 20. Source-evidence acceptance |
| 16. Shutdown and teardown | 21. Shutdown and teardown |
| 17. Architecture Gatekeeper source review | 22. Architecture Gatekeeper source review |

The mapping is authoritative for Version 1.1 cross-references. No Version 1.0 decision migrates as execution authority, and no earlier Version 1.1 gate implies a later gate.

---

## Failure, Rollback, Recovery, and Teardown

### Failure and Recovery

- Stop immediately; preserve only the bounded evidence allowed for the failed gate.
- Do not enable networking, add a share, install an agent, change privilege, substitute a version, use a mirror, update a package, repair a manifest, reacquire, restart, or rerun without new authorization.
- A failed preparation attempt may be abandoned and its exact task state later torn down. Re-creation is a new task instance and new authorization, not recovery in place.
- A failed execution run does not change the accepted static environment. Source or execution-manifest defects return to repository review; environment defects return to preparation review.

### Exact Teardown Targets

The protected local host-action manifest must enumerate the exact UTM application target if task-installed, VM bundle, primary disk, UEFI/NVRAM state, installer/preparation/update/request/source media, distinct readiness/execution result media, static/execution/sealing manifests, temporary acquisition directory, toolchain/module staging, and sanitized output staging. Repository evidence retains only sanitized target identifiers and the protected manifest digest. Pre-existing UTM installations or unrelated VMs are never deletion targets.

Teardown requires:

1. proof the VM is shut down, not paused or saved;
2. exact identity match for every target;
3. separate human authorization for deletion;
4. deletion only of enumerated task-created targets;
5. post-deletion filesystem, UTM inventory, process, launch-service, mount, socket, and media-attachment absence checks;
6. a teardown manifest recording what was and was not removed.

Logical deletion cannot prove physical erasure from APFS snapshots, SSD wear-leveling, backups, caches outside the enumerated task root, or storage-provider internals. Evidence must state this limitation truthfully. Any unexpected residual state or unverifiable target leaves teardown incomplete and escalates.

---

## Hard Stop Conditions

- wrong repository, branch, HEAD, tree, tracking state, or authority;
- missing named host owner or per-action authorization;
- unresolved or changed artifact identity, checksum, signature, signer, package closure, version, support, or advisory state, except the exact UTM signer fields during the Gatekeeper-approved artifact-identity sealing gate whose sole purpose is to establish them;
- UTM release/build drift or Gatekeeper/signature/notarization failure;
- inability to prove no persistent privileged daemon/server/helper;
- network adapter or non-loopback interface at any lifecycle stage;
- Rosetta, translation, user-mode emulation, shared folder, clipboard, SSH use, agent, remote control, USB sharing, host socket, or credential exposure;
- unexpected Docker, Podman, containerd, Kubernetes, daemon, socket, package, group, mount, service, or process;
- guest-side source authoring, repair, commit, or representation of `platrun` as the repository implementation identity;
- administrative guest validation identity or privilege escalation;
- missing offline toolchain/module/package dependency or incomplete retained-package security baseline;
- repository/source/tree/diff or manifest drift;
- T-01 through T-12 skip/failure, race/fuzz/validator failure, or unsupported Linux evidence;
- export-policy, secret, hygiene, checksum, or sanitization failure;
- shutdown, teardown, or absence proof ambiguity;
- any requirement for source implementation in preparation, environment use before readiness acceptance, portfolio/backlog/ADR/Registry change, deployment, activation, release, or live work.

---

## Unresolved Decisions and Risks

1. Name and authority of the Platform Administrator or host owner.
2. Separately authorized correction and acceptance of the protected `HOST_TASK_ROOT` hierarchy and exact task-created descendants; no protected value is inspected or recorded by this proposal.
3. Exact acquired-artifact Developer ID common name, TeamIdentifier, notarization ticket, designated requirement, and entitlement inventory remain unknown until the separately authorized Gatekeeper-approved artifact-identity sealing gate.
4. Host macOS version and Apple Virtualization compatibility with UTM 4.7.5 build 118 and Ubuntu 24.04.4 ARM64.
5. Actual retained inventory, exact required component set, index URLs and redirect chains, index sizes and SHA-256 values, package closure, and `.deb` identities are deliberately generated and accepted at their separate later gates rather than inferred before the base inventory exists.
6. Completion and later evidence acceptance of snapshot `20260725T000000Z` complete retained-package `full-upgrade` plus no-change proof for the February point-release ISO.
7. Exact raw-disk filenames and UTM machine identifier, which can be generated only during authorized creation and must be captured before readiness.
8. Future advisory drift for UTM, Ubuntu, Go, and x/sys between this research date and any acquisition or execution.
9. Replacement static-manifest digests, a new uniquely identified acceptance record, and proof that the suspended Version 1.0 digest is absent from every future addendum.
10. Separate publication preparation, staging/commit authorization, followed later by separate push authorization and fetched equality proof.

Each item is blocking for the gate it affects. None may be filled by inference during execution.

---

## Product Strategy Board Decision

The Product Strategy Board confirms that the Version 1.1 correction remains within existing PLAT-15.1A / PLAT-PB-013 authority and AB-011. No new Product Backlog or Architecture Backlog identifier is warranted. The added gates protect Delivery Leverage by preventing unusable component acquisition, preserving exact provenance, and avoiding rework from an inferred package inventory; they are not avoidable process. PLAT-15.1A remains blocked and implementation remains `Not Started`. Product Strategy Board decision: **Version 1.1 approved for repository publication**. The package remains `Not Published`; staging/commit and push remain separate gates.

---

## Architecture Gatekeeper Decision

The Architecture Gatekeeper finds the corrected proposal decision-ready because it preserves:

- UTM 4.7.5 build 118 with Apple Virtualization and zero guest network devices;
- bounded stable artifact and signed-release acquisition separate from retained-inventory-driven component-index acquisition;
- Canonical snapshot `20260725T000000Z` with complete retained-package offline updating;
- governed host-worktree implementation followed by guest-only `platrun` validation;
- mandatory detachment of every ingress medium before validation;
- separate readiness and execution evidence exports before their corresponding acceptance gates;
- protected-local host authority/path data with sanitized repository identifiers and digest only; and
- the revised 22-gate lifecycle and explicit Version 1.0 migration mapping.

Version 1.1 additionally makes `HOST_TASK_ROOT` the Gate 2 task root without a redundant wrapper, mandates exact intermediate-container parent bindings, limits Gate 2 inventory to deterministic pre-VM objects, and separates actual retained inventory, component indexes, offline package planning, and `.deb` acquisition into non-interchangeable gates.

Architecture Gatekeeper decision: **Version 1.1 approved for repository publication**. Version 1.1 remains `Proposed` and `Not Published`; approval opens only separately authorized staging/commit and later push. It does not authorize protected amendment, staging, commit, push, acquisition, networking, UTM DMG mounting or inspection, installation, package retrieval, VM creation/use, implementation, Linux execution, deployment, activation, release, or live work.

---

## Publication Criteria

This proposal may advance to publication only after:

- applicable repository checks pass; exact Go 1.26.5 checks run only if that exact toolchain is already available without acquisition;
- the Version 1.1 Board and Gatekeeper repository-publication approvals remain recorded without implying publication or host action;
- status remains environment `Not Created`, implementation `Not Started`, and PLAT-15.1A blocked;
- repository-mandated validations and exact path audit pass;
- a separate publication package is authorized, staged, committed, and pushed through distinct approvals.

Even after publication, acquisition and every host action remain separately unauthorized until explicitly approved.

---

## Publication and Later Gates

This Version 1.1 document is approved for repository publication and is currently `Proposed` and `Not Published`. Its presence does not create publication, protected amendment, acquisition, or preparation authority.

Publication requires only the exact validated repository changes under separate staging/commit authorization and later separate push authorization. Publication would not authorize acquisition, installation, VM creation/startup, preparation, readiness execution, PLAT-15.1A implementation, Linux validation, evidence acceptance, export, shutdown, teardown, deployment, activation, release, or live work.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Corrected the Gate 2 root topology; suspended the incomplete Version 1.0 static-manifest acceptance for execution eligibility; separated stable signed-release acquisition from actual retained-inventory generation, component-index request/acquisition/acceptance, offline package-plan generation/acceptance, and later `.deb` acquisition/acceptance; expanded the lifecycle to 22 distinct gates; added the Version 1.0 migration mapping; retained portfolio linkage; and kept protected, publication, environment, implementation, deployment, activation, release, and live gates closed. |
| 1.0 | Recorded Board and Gatekeeper approval plus the approved sealing architecture; applied FAT16 to the 8 MiB/32 MiB media, separated host-only repository validation from guest Linux validation, bound guest executables and signed Ubuntu package closure, constrained acquisition to canonical/approved redirect destinations, required stapled/offline UTM notarization evidence first, retained the 17 gates, recorded successful exact Go 1.26.5 validation with retrieval disabled, and kept staging/commit and push separately authorized. |
| 0.2 | Recorded Board portfolio approval and Gatekeeper revision-required state; requested bounded acquisition-and-sealing gates for UTM signer and complete Ubuntu snapshot security closure; separated host-worktree implementation from guest validation; made ingress detachment mandatory; separated and capacity-bound readiness/execution evidence media; placed both exports before acceptance; protected personal host/path data locally; and retained exact Go 1.26.5 validation as a publication blocker. |
| 0.1 | Proposed UTM 4.7.5 Apple Virtualization with Ubuntu 24.04.4 ARM64, required offline kernel 6.8.0-136.136, Go 1.26.5, x/sys v0.47.0, strict no-network/no-sharing isolation, separate manifests and transfer media, preparation-only administration, bounded execution identity, evidence and teardown contracts, and explicit unresolved approval gates. |
