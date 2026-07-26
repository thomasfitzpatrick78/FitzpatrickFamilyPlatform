# PLAT-15.1A - Artifact and Archive-Metadata Acquisition and Sealing Authorization Package

**Document Version:** 1.0

**Status:** Proposed

**Approval State:** Product Strategy Board and Architecture Gatekeeper Approved for Repository Publication

**Product Strategy Board Decision:** Version 0.2 Portfolio Fit Approved; Publication-Ready Version 1.0 Confirmed under PLAT-15.1A / PLAT-PB-013

**Architecture Gatekeeper Decision:** Version 0.2 Architecture Approved; Publication-Ready Version 1.0 Applies the Approved Authority Separation and Sequencing

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

This proposed subordinate package defines the exact future authority boundary for Gate 2 of the published [PLAT-15.1A Supported-Linux Validation Environment Preparation Work Package](PLAT_15_1A_Supported_Linux_Validation_Environment_Preparation_Work_Package.md): acquisition of already-bound artifacts and archive metadata, read-only UTM identity inspection, verification, quarantine, and sealing.

Version 1.0 applies the Product Strategy Board- and Architecture Gatekeeper-approved Version 0.2 design and is approved for repository publication. It remains `Not Published` and does not publish or execute itself. It authorizes no present protected-manifest creation, acquisition, download, DNS or HTTPS contact, storage creation, mount, application inspection, installation, execution, VM action, package application, Linux execution, PLAT-15.1A implementation, deployment, activation, release, or live work.

After separate publication, a separately initialized host session may create only the static protected host-authority manifest already authorized in protected human authority. The resulting sanitized identifier and digest still require Gatekeeper acceptance. A later exact per-run execution-authorization addendum and explicit execution decision are required before Gate 2 can become authorized. Gate 2, if then authorized, may produce only protected-local acquisition/sealing evidence and a final sealed-inventory manifest plus bounded sanitized repository evidence. Gate 3 remains the separate Architecture Gatekeeper seal-acceptance decision.

---

## Governing State and Authority Boundary

- PLAT-15.1A remains subordinate to PLAT-PB-013 and AB-011; no new Product Backlog identifier is created.
- ADR-012 remains `Implemented: No`.
- AB-012 remains `Candidate - Remain Backlog` and is not changed by this proposal.
- The environment remains `Not Created`.
- PLAT-15.1A repository implementation remains `Not Started` and blocked.
- The published closed privileged-proxy architecture, Production Provider Adapter boundary, and every source, artifact-acceptance, deployment, daemon-interaction, observation, consumer, recurrence, activation, release, and live gate remain unchanged.
- Product Strategy Board authority is limited to portfolio fit and this subordinate package boundary.
- Chief Architect / Architecture Gatekeeper authority covers the acquisition/sealing architecture, later static-manifest acceptance, per-run execution acceptance, identity evidence, residual risk, and Gate 3.
- Protected human authority has supplied a named host owner and Platform Administrator, an exact host-task root, a future UTM installation target, and authorization in principle for later static-manifest creation and bounded Gate 2 work. Repository evidence records only non-reversible sanitized decision states; it contains no personal identity or absolute host path.
- `Authorized in principle` is not execution authorization. Gate 2 remains `Not Authorized` until the static-manifest digest is accepted, both execution decisions bind the same exact authorization-subject digest, and the final decision-bearing addendum digest is verified.

Conversation approval, protected authority in principle, package approval, repository presence, publication, validation success, a clean baseline, or `READY` does not authorize Gate 2.

---

## Repository-Controlled Identity Register

The values in this section are extracted from the Version 1.0 preparation work package. Official primary-source metadata reviewed on 2026-07-25 did not identify a conflict. Publisher metadata remains research evidence, not possession or verification of an acquired object.

### UTM

| Field | Binding value |
|-------|---------------|
| Product | UTM |
| Version / build | `4.7.5` / `118` |
| Publisher | UTM project; application publisher expected to be Turing Software, LLC |
| Release tag / source revision | `v4.7.5` / `048ca7498ea3a374439149d51739d94c5300bcda` |
| Artifact | `UTM.dmg` |
| Canonical URL | `https://github.com/utmapp/UTM/releases/download/v4.7.5/UTM.dmg` |
| Expected bytes | `250021057` |
| Expected SHA-256 | `a8435c93cfb5f8bbfeea4b134cfad1ac66b67632b75e438c63b1a8ae043bef0e` |
| Required backend after later preparation authority | Apple Virtualization only; no QEMU backend |
| Acquired identity fields | Developer ID certificate chain, leaf common name, TeamIdentifier, designated requirement, code-directory identifiers, secure timestamp, hardened-runtime status, full entitlements, notarization and stapled-ticket evidence, offline Gatekeeper assessment, and mounted-image identity |
| Deliberately unresolved identity | Exact Developer ID common name and TeamIdentifier become binding only after Gate 2 read-only inspection and Gate 3 acceptance |

### Ubuntu Installation Image and Signed Release Evidence

| Field | Binding value |
|-------|---------------|
| Distribution | Ubuntu Server 24.04.4 LTS (Noble Numbat) |
| Architecture | ARM64 / AArch64 |
| Artifact | `ubuntu-24.04.4-live-server-arm64.iso` |
| Canonical URL | `https://cdimage.ubuntu.com/ubuntu/releases/24.04/release/ubuntu-24.04.4-live-server-arm64.iso` |
| Expected bytes | `3059724288` |
| Expected SHA-256 | `9a6ce6d7e66c8abed24d24944570a495caca80b3b0007df02818e13829f27f32` |
| Signed checksum files | `SHA256SUMS` and `SHA256SUMS.gpg` from the same canonical release directory |
| Expected signing identity | Ubuntu CD Image Automatic Signing Key (2012), `cdimage@ubuntu.com` |
| Expected signer fingerprint | `843938DF228D22F7B3742BC0D94AA3F0EFE21092` |
| Required verification | Validate the trusted fingerprint, verify `SHA256SUMS.gpg` over `SHA256SUMS`, then verify the ISO byte count and SHA-256 |

### Go Toolchain

| Field | Binding value |
|-------|---------------|
| Version | Go `1.26.5` |
| Artifact | `go1.26.5.linux-arm64.tar.gz` |
| Canonical URL | `https://go.dev/dl/go1.26.5.linux-arm64.tar.gz` |
| Expected bytes | `63759990` |
| Expected SHA-256 | `fe4789e92b1f33358680864bbe8704289e7bb5fc207d80623c308935bd696d49` |
| Signature model | Official HTTPS metadata plus SHA-256; no detached signature is advertised |
| Required verification | Match official download metadata, byte count, and SHA-256 before sealing and again after every transfer |

The withdrawn value `fe4789d6403a2226439ff5a980a3f9e4aa0996f4f3155c951d115e54a4ae1d49` has no authority and is a mandatory rejection value.

### `golang.org/x/sys`

| Field | Binding value |
|-------|---------------|
| Module / version | `golang.org/x/sys` / `v0.47.0` |
| Publication time | `2026-06-30T17:07:31Z` |
| Canonical VCS | `https://go.googlesource.com/sys` |
| Tag / revision | `refs/tags/v0.47.0` / `9e7e939dcafac07e8ab4cffa6e5fc74908413f00` |
| Module sum | `h1:o7XGOvZQCADBQQ4Y7VNq2dRWQR7JmOUW8Kxx4ZsNgWs=` |
| `go.mod` sum | `h1:4GL1E5IUh+htKOUEOaiffhrAeqysfVGipDYzABqnCmw=` |
| Offline object set | `v0.47.0.info`, `v0.47.0.mod`, and `v0.47.0.zip`, plus a sealing manifest; no list, latest, alternate version, VCS fallback, transitive module, or sumdb network fallback |
| Canonical proxy base | `https://proxy.golang.org/golang.org/x/sys/@v/` |
| Sum record | `https://sum.golang.org/lookup/golang.org/x/sys@v0.47.0` as verification metadata only |

The future protected sealing manifest must record each proxy object's exact response bytes, byte size, SHA-256, content type, final URL, and relationship to the two repository-bound module sums. Those transport-level byte sizes and SHA-256 values are not present in repository authority and must not be invented before the authorized acquisition.

### Canonical Ubuntu Snapshot

| Field | Binding value |
|-------|---------------|
| Snapshot | `20260725T000000Z` |
| Canonical base | `https://snapshot.ubuntu.com/ubuntu/20260725T000000Z/` |
| Architecture | ARM64 |
| Permitted suites | `noble`, `noble-updates`, and `noble-security` only |
| Excluded suites | `noble-backports` and every other suite |
| Required signed metadata | Per-suite `InRelease`, or `Release` plus `Release.gpg` where applicable, and the ARM64 `Packages` indexes referenced by the accepted signed release records |
| Component rule | Only components proved necessary by the retained installed-package inventory; the component set must not be guessed |
| Package-material rule | No `.deb` material is authorized by Gate 2; exact retained-package closure is generated at Gate 6 and acquired only under Gate 7 |

Gate 2 may seal the signed archive metadata required to calculate the later offline plan. It may not select or acquire package material. Every exact suite/component/index filename, compression form, size, SHA-256, signer fingerprint, and snapshot URL must be derived from and cross-checked against the signed release metadata before the Gate 2 manifest is eligible for Gate 3.

---

## Exact Gate 2 Inventory

| Inventory group | Required objects | Acquisition state |
|-----------------|------------------|-------------------|
| UTM | Exact `UTM.dmg` only | Proposed; not authorized |
| Ubuntu image evidence | Exact ARM64 ISO, `SHA256SUMS`, and `SHA256SUMS.gpg` | Proposed; not authorized |
| Go | Exact Linux ARM64 archive only | Proposed; not authorized |
| x/sys | Exact `.info`, `.mod`, `.zip`, and checksum-database lookup record used as metadata | Proposed; not authorized |
| Ubuntu snapshot | Exact signed suite records and the referenced ARM64 `Packages` indexes required by the proven component set | Proposed; not authorized |
| Gate 2 manifests | Acquisition request, redirect-chain, raw verification, UTM identity, archive-metadata, quarantine, sealed-inventory, no-execution, and completion manifests | Schemas proposed; must be created only under later authority |

No package index may be used to infer authorization for its referenced `.deb` objects. No object outside this inventory is eligible for opportunistic acquisition.

---

## Canonical Source and Network Policy

### Minimum Destination Allowlist

Repository authority permits only these stable canonical HTTPS origins for the corresponding objects:

| Host | Port | Authorized purpose |
|------|------|--------------------|
| `github.com` | `443` | Exact UTM release artifact request only |
| `cdimage.ubuntu.com` | `443` | Exact Ubuntu ISO and its two signed-checksum files only |
| `go.dev` | `443` | Exact Go archive request only |
| `proxy.golang.org` | `443` | Exact x/sys `.info`, `.mod`, and `.zip` objects only |
| `sum.golang.org` | `443` | Exact x/sys checksum lookup record only |
| `snapshot.ubuntu.com` | `443` | Exact snapshot signed metadata and accepted ARM64 indexes only |

The table is architecture policy, not network authority. DNS may be authorized later only for a canonical hostname above or a destination in the exact protected per-run redirect chain. HTTPS may be authorized only on TCP port 443. No IP literal, alternate port, wildcard host, suffix match, or certificate exception is permitted.

`release-assets.githubusercontent.com`, `dl.google.com`, or any other redirect destination is not authorized merely because it is commonly used by a publisher. Exact redirect chains are protected per-run authority, not stable repository facts. A separately authorized redirect-resolution-only preflight may use `HEAD` without accepting artifact bytes to record the chain for the run. The finalized execution addendum must bind every scheme, hostname, port, exact path and query constraint, redirect status, TLS identity, transition count, observation time, and expiry before artifact bytes are acquired. The observed chain expires with the addendum and is never reusable authority.

### Request Constraints

- Allow `HEAD` only under a separately approved redirect-resolution preflight and one bounded `GET` only under the later final execution authorization.
- Require TLS certificate and hostname validation with no override.
- Send no credentials, authorization header, client certificate, cookie, referrer, or persistent client identifier.
- Disable cookie storage, proxy inheritance, telemetry, update checks, retries to alternate hosts, content negotiation that changes the object, resume from an unverified partial, and automatic decompression.
- Reject search, browsing-based selection, mirrors, caches not named in the addendum, package-manager network use, VCS fallback, checksum-database fallback, HTTP downgrade, authentication challenge, hostname, path, query, expiry, TLS-identity, or redirect drift, unexpected content encoding, byte-size mismatch, checksum mismatch, or response outside the authorization window.
- Record complete request and redirect identity, including any time-bound query, only in protected evidence. Repository evidence may retain sanitized origin/destination identifiers, pass/fail, timestamps, and digests but no signed query, personal host/network identifier, IP address, or reversible mapping.

Any required Apple network contact is excluded. If stapled/offline UTM verification is insufficient or a tool attempts to contact Apple, stop. A separate future authorization must name the exact Apple endpoint, redirect boundary, purpose, expected disclosure, and evidence policy.

---

## Protected-Local Storage Contract

No storage is created by this proposal. After later approval and named-owner authorization, all Gate 2 paths must be exact children of the protected absolute `HOST_TASK_ROOT` recorded in the static host-authority manifest and activated by exact identity in the per-run addendum. The required relative structure is:

```text
HOST_TASK_ROOT/
  gate-2/
    acquisition/
      partial/
      complete/
    quarantine/
    inspection/
    sealed/
      artifacts/
      ubuntu-release-evidence/
      go-proxy/
      ubuntu-snapshot-metadata/
    manifests/
    evidence/
    cleanup-staging/
```

Every created directory and file, including temporary names, must be enumerated as an exact absolute path before creation. Symlinks, hard-link reuse, aliases, broad roots, home-directory roots, repository roots, shared caches, and paths outside `HOST_TASK_ROOT` are prohibited.

### Ownership, Permissions, and Seal State

- Root and working directories: named owner only, mode `0700` while active.
- Partial, unverified, and quarantined files: named owner only, mode `0600`; never executable.
- Verified sealed files: mode `0400`, no ACL granting another principal, no execute bit, and user-immutable flag where supported.
- Sealed directories: mode `0500` after completion, with an inventory of ownership, mode, ACL, flags, device, inode, size, and SHA-256.
- No file may inherit an extended attribute or ACL that grants execution, sharing, cloud synchronization, indexing, automatic opening, or another principal access.
- User-immutable flags are tamper resistance, not irreversible immutability; Gate 3 evidence must state that the owner can later remove them. Any unseal requires separate authorization and a manifest amendment.

The final seal is a canonical inventory manifest plus SHA-256 over that manifest's canonical bytes. Each object is hashed before verification, after any read-only inspection, after movement to sealed storage, and after any later authorized transfer. A difference is a hard stop.

---

## Protected Authority Artifact Separation

Gate 2 authority is divided into four non-interchangeable protected artifacts:

| Artifact | Creation point | Authority carried |
|----------|----------------|-------------------|
| Static protected host-authority manifest | Later separately initialized host-manifest session after package publication | Host owner, Platform Administrator, exact host/root/installation target, planned child paths, host controls, manifest-creation authorization, lifecycle, and digest only |
| Per-run Gate 2 execution-authorization addendum | After Gatekeeper accepts the static manifest and exact run inputs exist | One task instance, package publication identity, objects, tools, commands, window, redirects/endpoints, active paths, cleanup, retention, risk acceptance, owner authorization, Gatekeeper execution acceptance, and digest |
| Gate 2 execution evidence | Only during the exact authorized run | Acquisition, verification, quarantine, inspection, no-execution, sealing, failure, and cleanup observations |
| Final sealed-inventory manifest | Only after successful Gate 2 execution | Final object and subordinate-evidence digests eligible for Gate 3 review |

No artifact can stand in for another. The static manifest is valid without a Gate 2 execution authorization. `Authorized in principle` is never a valid execution decision.

### Non-Circular Approval Sequence

| Sequence | Gate | Current state | Opens only |
|----------|------|---------------|------------|
| 1 | Package architecture approval | Version 1.0 approved for repository publication; Not Published | Eligibility for separately authorized staging and commit, followed by still-separate push/publication authority |
| 2 | Package publication | Not Authorized | Eligibility for a separately initialized static-manifest session |
| 3 | Static protected-manifest creation | Not Authorized in this session | A protected static manifest and sanitized identifier/digest for review |
| 4 | Static-manifest acceptance | Not Authorized | Eligibility to prepare exact per-run authority and separately resolve redirects |
| 5 | Per-run execution authorization | Not Authorized | One exact task/window after matching owner and Gatekeeper decisions and final addendum-digest verification |
| 6 | Acquisition and read-only sealing | Gate 2 Not Authorized | Protected execution evidence and, on success, a final sealed inventory |
| 7 | Gate 2 completion | No execution evidence exists | Eligibility for Gate 3 review only |
| 8 | Gate 3 seal acceptance | No evidence to review | Eligibility for a separately authorized Gate 4 proposal/action only |

No earlier gate implies or collapses a later gate.

### Static Protected Host-Authority Manifest Schema

No protected artifact is created or populated in this session. A later separately authorized session must instantiate the following Draft 2020-12 JSON Schema outside Git. Personal identity, host identity, absolute paths, private authorization, and raw host evidence remain protected local data.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:fitzpatrick-family-platform:plat-15-1a:gate-2:static-protected-host-authority-manifest:1.0",
  "title": "PLAT-15.1A Gate 2 Static Protected Host-Authority Manifest",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "manifest_kind",
    "repository_identifier",
    "named_authority",
    "approved_host_identity",
    "host_task_root",
    "utm_installation_target",
    "planned_child_paths",
    "host_controls",
    "manifest_creation_authorization",
    "lifecycle_controls",
    "manifest_digest"
  ],
  "properties": {
    "schema_version": { "const": "1.0" },
    "manifest_kind": { "const": "plat-15-1a-gate-2-static-protected-host-authority-manifest" },
    "repository_identifier": {
      "type": "object",
      "additionalProperties": false,
      "required": ["sanitized_id", "repository", "gate"],
      "properties": {
        "sanitized_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
        "repository": { "const": "FitzpatrickFamilyPlatform" },
        "gate": { "const": "PLAT-15.1A-Gate-2" }
      }
    },
    "named_authority": {
      "type": "object",
      "additionalProperties": false,
      "required": ["host_owner_legal_name", "platform_administrator_legal_name", "authority_verified_by", "authority_verified_at_utc"],
      "properties": {
        "host_owner_legal_name": { "type": "string", "minLength": 1 },
        "platform_administrator_legal_name": { "type": "string", "minLength": 1 },
        "authority_verified_by": { "type": "string", "minLength": 1 },
        "authority_verified_at_utc": { "type": "string", "format": "date-time" }
      }
    },
    "approved_host_identity": {
      "type": "object",
      "additionalProperties": false,
      "required": ["protected_host_id", "hardware_uuid", "serial_number", "hostname", "os_version", "architecture", "identity_evidence_sha256"],
      "properties": {
        "protected_host_id": { "type": "string", "minLength": 1 },
        "hardware_uuid": { "type": "string", "minLength": 1 },
        "serial_number": { "type": "string", "minLength": 1 },
        "hostname": { "type": "string", "minLength": 1 },
        "os_version": { "type": "string", "minLength": 1 },
        "architecture": { "const": "arm64" },
        "identity_evidence_sha256": { "$ref": "#/$defs/sha256" }
      }
    },
    "host_task_root": { "$ref": "#/$defs/absolute_path" },
    "utm_installation_target": { "$ref": "#/$defs/absolute_path" },
    "planned_child_paths": {
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["path_id", "absolute_path", "parent_path_id", "purpose", "object_type", "owner", "group", "active_mode", "sealed_mode", "deletion_target"],
        "properties": {
          "path_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "absolute_path": { "$ref": "#/$defs/absolute_path" },
          "parent_path_id": { "type": ["string", "null"] },
          "purpose": { "enum": ["acquisition-partial", "acquisition-complete", "quarantine", "inspection", "sealed-artifact", "ubuntu-release-evidence", "go-proxy", "ubuntu-snapshot-metadata", "manifest", "evidence", "cleanup-staging"] },
          "object_type": { "enum": ["directory", "file"] },
          "owner": { "type": "string", "minLength": 1 },
          "group": { "type": "string", "minLength": 1 },
          "active_mode": { "type": "string", "pattern": "^0[0-7]{3}$" },
          "sealed_mode": { "type": "string", "pattern": "^0[0-7]{3}$" },
          "deletion_target": { "type": "boolean" }
        }
      }
    },
    "host_controls": {
      "type": "object",
      "additionalProperties": false,
      "required": ["owner_only", "symlinks_prohibited", "hard_links_prohibited", "sharing_prohibited", "cloud_sync_prohibited", "indexing_prohibited", "retention_policy", "destruction_requires_new_authorization"],
      "properties": {
        "owner_only": { "const": true },
        "symlinks_prohibited": { "const": true },
        "hard_links_prohibited": { "const": true },
        "sharing_prohibited": { "const": true },
        "cloud_sync_prohibited": { "const": true },
        "indexing_prohibited": { "const": true },
        "retention_policy": { "type": "string", "minLength": 1 },
        "destruction_requires_new_authorization": { "const": true }
      }
    },
    "manifest_creation_authorization": {
      "type": "object",
      "additionalProperties": false,
      "required": ["record_id", "decision", "scope_digest_sha256", "authorized_by", "authorized_at_utc"],
      "properties": {
        "record_id": { "type": "string", "minLength": 1 },
        "decision": { "const": "static-protected-manifest-creation" },
        "scope_digest_sha256": { "$ref": "#/$defs/sha256" },
        "authorized_by": { "type": "string", "minLength": 1 },
        "authorized_at_utc": { "type": "string", "format": "date-time" }
      }
    },
    "lifecycle_controls": {
      "type": "object",
      "additionalProperties": false,
      "required": ["created_at_utc", "created_by", "amendments", "retention_until_utc", "retention_basis", "destruction_requires_new_authorization"],
      "properties": {
        "created_at_utc": { "type": "string", "format": "date-time" },
        "created_by": { "type": "string", "minLength": 1 },
        "amendments": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["amendment_id", "prior_digest_sha256", "reason", "approved_by", "approved_at_utc"],
            "properties": {
              "amendment_id": { "type": "string", "minLength": 1 },
              "prior_digest_sha256": { "$ref": "#/$defs/sha256" },
              "reason": { "type": "string", "minLength": 1 },
              "approved_by": { "type": "string", "minLength": 1 },
              "approved_at_utc": { "type": "string", "format": "date-time" }
            }
          }
        },
        "retention_until_utc": { "type": "string", "format": "date-time" },
        "retention_basis": { "type": "string", "minLength": 1 },
        "destruction_requires_new_authorization": { "const": true },
        "destroyed_at_utc": { "type": ["string", "null"], "format": "date-time" },
        "destruction_record_sha256": { "anyOf": [{ "$ref": "#/$defs/sha256" }, { "type": "null" }] }
      }
    },
    "manifest_digest": {
      "type": "object",
      "additionalProperties": false,
      "required": ["algorithm", "canonicalization", "coverage", "sha256"],
      "properties": {
        "algorithm": { "const": "SHA-256" },
        "canonicalization": { "const": "RFC 8785 JCS" },
        "coverage": { "const": "entire manifest with manifest_digest omitted" },
        "sha256": { "$ref": "#/$defs/sha256" }
      }
    }
  },
  "$defs": {
    "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "absolute_path": { "type": "string", "pattern": "^/[^\\u0000]+$", "minLength": 2 }
  }
}
```

The static schema deliberately contains no task instance, acquisition command, redirect chain, execution window, Gate 2 execution authorization, or Gatekeeper execution acceptance. Its manifest-creation authorization permits creation of that static authority record only.

### Per-Run Gate 2 Execution-Authorization Addendum Schema

After publication and separate acceptance of the static protected-manifest digest, a later session may prepare—but may not execute—the following protected addendum. Every value is exact for one run. The package version and published commit/tree fields cannot be populated from this uncommitted proposal.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:fitzpatrick-family-platform:plat-15-1a:gate-2:execution-authorization-addendum:1.0",
  "title": "PLAT-15.1A Gate 2 Per-Run Execution-Authorization Addendum",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "manifest_kind",
    "addendum_id",
    "accepted_static_manifest",
    "package_authority",
    "task_instance",
    "object_inventory",
    "acquisition_tools",
    "command_identifiers",
    "authorization_window",
    "canonical_urls",
    "redirect_chains",
    "network_endpoints",
    "active_child_paths",
    "quarantine_and_cleanup",
    "retention_controls",
    "residual_risk_acceptance",
    "authorization_subject_digest",
    "owner_execution_authorization",
    "gatekeeper_execution_acceptance",
    "addendum_digest"
  ],
  "properties": {
    "schema_version": { "const": "1.0" },
    "manifest_kind": { "const": "plat-15-1a-gate-2-per-run-execution-authorization-addendum" },
    "addendum_id": { "type": "string", "pattern": "^gate2-execution-addendum-[0-9]{3}$" },
    "accepted_static_manifest": {
      "type": "object",
      "additionalProperties": false,
      "required": ["sanitized_id", "schema_version", "sha256", "gatekeeper_acceptance_record_id"],
      "properties": {
        "sanitized_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
        "schema_version": { "const": "1.0" },
        "sha256": { "$ref": "#/$defs/sha256" },
        "gatekeeper_acceptance_record_id": { "type": "string", "minLength": 1 }
      }
    },
    "package_authority": {
      "type": "object",
      "additionalProperties": false,
      "required": ["package_version", "published_commit", "published_tree"],
      "properties": {
        "package_version": { "const": "1.0" },
        "published_commit": { "$ref": "#/$defs/git_oid" },
        "published_tree": { "$ref": "#/$defs/git_oid" }
      }
    },
    "task_instance": { "type": "string", "pattern": "^plat-15-1a-gate2-[0-9]{3}$" },
    "object_inventory": {
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["object_id", "repository_identity_reference", "expected_filename", "expected_bytes", "expected_sha256", "acquisition_required"],
        "properties": {
          "object_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "repository_identity_reference": { "type": "string", "minLength": 1 },
          "expected_filename": { "type": "string", "minLength": 1 },
          "expected_bytes": { "type": ["integer", "null"], "minimum": 0 },
          "expected_sha256": { "anyOf": [{ "$ref": "#/$defs/sha256" }, { "type": "null" }] },
          "acquisition_required": { "const": true }
        }
      }
    },
    "acquisition_tools": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["tool_id", "absolute_executable_path", "version", "executable_sha256", "approved_purpose"],
        "properties": {
          "tool_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "absolute_executable_path": { "$ref": "#/$defs/absolute_path" },
          "version": { "type": "string", "minLength": 1 },
          "executable_sha256": { "$ref": "#/$defs/sha256" },
          "approved_purpose": { "type": "string", "minLength": 1 }
        }
      }
    },
    "command_identifiers": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["command_id", "canonical_argv_sha256", "purpose"],
        "properties": {
          "command_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "canonical_argv_sha256": { "$ref": "#/$defs/sha256" },
          "purpose": { "type": "string", "minLength": 1 }
        }
      }
    },
    "authorization_window": {
      "type": "object",
      "additionalProperties": false,
      "required": ["not_before_utc", "expires_at_utc"],
      "properties": {
        "not_before_utc": { "type": "string", "format": "date-time" },
        "expires_at_utc": { "type": "string", "format": "date-time" }
      }
    },
    "canonical_urls": {
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "items": { "type": "string", "format": "uri", "pattern": "^https://" }
    },
    "redirect_chains": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["object_id", "resolved_at_utc", "expires_at_utc", "resolution_authorization_id", "ordered_hops", "chain_sha256"],
        "properties": {
          "object_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "resolved_at_utc": { "type": "string", "format": "date-time" },
          "expires_at_utc": { "type": "string", "format": "date-time" },
          "resolution_authorization_id": { "type": "string", "minLength": 1 },
          "ordered_hops": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "additionalProperties": false,
              "required": ["sequence", "scheme", "hostname", "port", "exact_path_and_query", "status", "tls_identity_sha256"],
              "properties": {
                "sequence": { "type": "integer", "minimum": 0 },
                "scheme": { "const": "https" },
                "hostname": { "type": "string", "minLength": 1 },
                "port": { "const": 443 },
                "exact_path_and_query": { "type": "string", "minLength": 1 },
                "status": { "type": "integer", "minimum": 200, "maximum": 399 },
                "tls_identity_sha256": { "$ref": "#/$defs/sha256" }
              }
            }
          },
          "chain_sha256": { "$ref": "#/$defs/sha256" }
        }
      }
    },
    "network_endpoints": {
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["hostname", "port", "purpose"],
        "properties": {
          "hostname": { "type": "string", "minLength": 1 },
          "port": { "const": 443 },
          "purpose": { "enum": ["canonical-origin", "approved-redirect"] }
        }
      }
    },
    "active_child_paths": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["static_path_id", "absolute_path", "owner", "group", "mode"],
        "properties": {
          "static_path_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "absolute_path": { "$ref": "#/$defs/absolute_path" },
          "owner": { "type": "string", "minLength": 1 },
          "group": { "type": "string", "minLength": 1 },
          "mode": { "type": "string", "pattern": "^0[0-7]{3}$" }
        }
      }
    },
    "quarantine_and_cleanup": {
      "type": "object",
      "additionalProperties": false,
      "required": ["quarantine_path_ids", "cleanup_target_path_ids", "cleanup_requires_new_authorization"],
      "properties": {
        "quarantine_path_ids": { "type": "array", "minItems": 1, "items": { "type": "string" } },
        "cleanup_target_path_ids": { "type": "array", "items": { "type": "string" } },
        "cleanup_requires_new_authorization": { "const": true }
      }
    },
    "retention_controls": {
      "type": "object",
      "additionalProperties": false,
      "required": ["retention_until_utc", "basis", "destruction_record_required"],
      "properties": {
        "retention_until_utc": { "type": "string", "format": "date-time" },
        "basis": { "type": "string", "minLength": 1 },
        "destruction_record_required": { "const": true }
      }
    },
    "residual_risk_acceptance": {
      "type": "object",
      "additionalProperties": false,
      "required": ["risk_register_sha256", "accepted_by", "accepted_at_utc"],
      "properties": {
        "risk_register_sha256": { "$ref": "#/$defs/sha256" },
        "accepted_by": { "type": "string", "minLength": 1 },
        "accepted_at_utc": { "type": "string", "format": "date-time" }
      }
    },
    "authorization_subject_digest": {
      "type": "object",
      "additionalProperties": false,
      "required": ["algorithm", "canonicalization", "coverage", "sha256"],
      "properties": {
        "algorithm": { "const": "SHA-256" },
        "canonicalization": { "const": "RFC 8785 JCS" },
        "coverage": { "const": "entire addendum with authorization_subject_digest, owner_execution_authorization, gatekeeper_execution_acceptance, and addendum_digest omitted" },
        "sha256": { "$ref": "#/$defs/sha256" }
      }
    },
    "owner_execution_authorization": { "$ref": "#/$defs/execution_decision" },
    "gatekeeper_execution_acceptance": { "$ref": "#/$defs/execution_decision" },
    "addendum_digest": { "$ref": "#/$defs/canonical_digest" }
  },
  "$defs": {
    "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "git_oid": { "type": "string", "pattern": "^[a-f0-9]{40}$" },
    "absolute_path": { "type": "string", "pattern": "^/[^\\u0000]+$", "minLength": 2 },
    "execution_decision": {
      "type": "object",
      "additionalProperties": false,
      "required": ["record_id", "decision", "authorization_subject_sha256", "decided_by", "decided_at_utc"],
      "properties": {
        "record_id": { "type": "string", "minLength": 1 },
        "decision": { "const": "approved-for-exact-gate-2-execution" },
        "authorization_subject_sha256": { "$ref": "#/$defs/sha256" },
        "decided_by": { "type": "string", "minLength": 1 },
        "decided_at_utc": { "type": "string", "format": "date-time" }
      }
    },
    "canonical_digest": {
      "type": "object",
      "additionalProperties": false,
      "required": ["algorithm", "canonicalization", "coverage", "sha256"],
      "properties": {
        "algorithm": { "const": "SHA-256" },
        "canonicalization": { "const": "RFC 8785 JCS" },
        "coverage": { "const": "entire addendum with addendum_digest omitted" },
        "sha256": { "$ref": "#/$defs/sha256" }
      }
    }
  }
}
```

The addendum uses two non-interchangeable digests. `authorization_subject_digest.sha256` covers the exact run plan with both decision objects and both digest objects omitted; the owner and Gatekeeper decisions must reference that same value. After both decisions exist, `addendum_digest.sha256` covers the entire decision-bearing addendum with only `addendum_digest` omitted. This makes the authorization subject stable before decision, seals the completed record afterward, and creates no self-reference. Any other coverage rule fails closed.

### Execution Evidence and Final Sealed Inventory

Gate 2 acquisition, verification, quarantine, read-only UTM inspection, no-execution, sealing, failure, and cleanup evidence is produced only after the final addendum is accepted. The final sealed-inventory manifest is produced only after successful Gate 2 execution and binds every object, subordinate evidence manifest, protected path identifier, permission/flag state, and digest. Neither artifact may be pre-created as evidence, and neither carries execution authority.

Schema validation alone is insufficient. Static-manifest review must prove every planned child is lexically and physically beneath the approved root, no component is a symlink, sharing and cloud synchronization are disabled, the root is not `/`, a home directory, repository root, shared directory, or wildcard expansion, and every deletion target would be task-created. Addendum review must prove exact equality to the accepted static digest, published package identity, current tool identities, current redirect observations, exact window, exact active paths, and both execution decisions.

Repository evidence may retain only non-reversible sanitized identifiers, schema versions, static-manifest and addendum SHA-256 values after their separate acceptance, decision-state descriptions, authorization record identifiers, and pass/fail review results. It must never retain either protected artifact, personal identity, machine identity, absolute path, redirect query, private authorization, or a reversible mapping.

---

## Acquisition, Verification, and Sealing Procedure

### 1. Preflight

Before any network or filesystem action, require:

1. this package approved and published;
2. the static protected host-authority manifest created in a separate initialized host session under the already supplied manifest-creation authority;
3. Architecture Gatekeeper acceptance of that static manifest's sanitized identifier and exact digest;
4. if redirects are required, a separately authorized redirect-resolution-only `HEAD` preflight that receives no artifact bytes and records exact time-bound chains in protected evidence;
5. a finalized per-run execution-authorization addendum binding the accepted static digest, published package commit/tree, exact task, object inventory, tools, commands, UTC window, canonical URLs, redirect chains, endpoints, active paths, quarantine/cleanup, retention, and residual risk;
6. owner execution authorization and Architecture Gatekeeper execution acceptance for the same exact authorization-subject digest, followed by verification of the final decision-bearing addendum digest;
7. Gate 2 marked authorized only for that task instance and window, with a repository-safe record containing only sanitized identifiers, accepted digests, and decision states; and
8. proof that no acquisition object already exists at a target path and no target resolves through a symlink.

Any missing, expired, inconsistent, or drifted value stops before storage or network activity.

### 2. Acquisition and Immediate Quarantine

- Create only the enumerated paths with exact owner-only permissions.
- Receive each response into its unique `.partial` target with no execute bit and no automatic open, mount, unpack, quarantine bypass, or handler invocation.
- Stream-hash and count bytes without interpreting executable content.
- On transport failure, retain only the exact partial object in quarantine with a failure manifest; do not resume, retry, substitute, or delete it without separate authorization.
- Move a complete object to the verification area only when transport identity, received byte count, and preliminary SHA-256 match the approved expectation where one exists.

### 3. Cryptographic and Provenance Verification

- UTM: exact byte count and SHA-256, official release/tag/source linkage, then the separately bounded read-only identity procedure below.
- Ubuntu ISO: trusted key fingerprint, detached signature over `SHA256SUMS`, exact checksum record, ISO byte count, and ISO SHA-256.
- Go: official version/file/OS/architecture metadata, byte count, SHA-256, and reproducible-build status.
- x/sys: exact `.info`, `.mod`, and `.zip`; publication time, tag revision, module sum, `go.mod` sum, and absence of any additional module object. Do not execute `go` to acquire or resolve the module.
- Ubuntu snapshot: signature chain for every accepted `InRelease` or `Release`/`Release.gpg`, exact snapshot timestamp, suite, component, architecture, index filename, compression form, byte size, and SHA-256 from signed metadata.

Verification is repeated after movement into sealed storage. No decompression, extraction, installation, package application, module-cache priming, VM attachment, or source use is part of Gate 2.

### 4. UTM Read-Only Identity Inspection

The future Gate 2 authorization may permit only this bounded inspection after the DMG's expected bytes and SHA-256 match:

1. record the DMG file identity, ownership, mode, flags, extended attributes, byte size, and SHA-256;
2. attach the image read-only, without browsing, automatic opening, application launch, copying to an installation target, or license/update interaction;
3. record the mounted device, filesystem, volume name/UUID, mount flags, root identity, and exact `UTM.app` bundle path;
4. inspect, without execution, the complete Developer ID certificate chain, leaf signer common name, TeamIdentifier, designated requirement, code-directory identifiers, secure timestamp, hardened-runtime status, nested-code signature validity, and full entitlements;
5. validate the stapled ticket and perform only the supported offline Gatekeeper assessment;
6. record whether any verification attempted or required network access; any such requirement stops before contact;
7. hash the DMG again, detach the mounted image, and prove mount, process, Launch Services, helper, daemon, VM, and application absence; and
8. quarantine on any publisher, signature, chain, designated-requirement, TeamIdentifier, entitlement, hardened-runtime, ticket, Gatekeeper, mounted-image, or no-execution mismatch.

No app bundle is copied, installed, registered, launched, translocated for execution, or used to create or inspect a VM. Gate 2 discovers the signer fields; only Gate 3 may accept them as future expected identity.

### 5. No-Execution Evidence

The protected completion evidence must include bounded pre/post inventories for processes, mounted images, launch services, login items, privileged helpers, system/user launch jobs, listening sockets, VM bundles, UTM preferences, file execute bits, and task-root access events where available. It must show:

- no acquired application, executable, installer, archive payload, daemon, VM, ISO, module, or package was launched or applied;
- no `UTM` or `utmctl` process, UTM Server, VM process, helper installation, login item, or persistent service appeared;
- only approved system metadata, hashing, signature, mount, unmount, and file-permission operations touched the objects;
- the DMG was mounted read-only only for the bounded inspection and was detached; and
- no application update, telemetry, Apple online validation, package-manager, Go proxy fallback, VCS, or other unrelated endpoint was contacted.

These controls provide bounded evidence, not a claim of universal forensic proof. That limitation must remain explicit.

### 6. Seal and Manifest Generation

For every accepted object, record canonical source, approved redirect chain, response identity, size, SHA-256, signature/provenance result, protected path identifier, ownership, permissions, flags, timestamps, and verification tool identities. Apply the read-only seal only after all checks pass. Generate:

- one per-object manifest;
- the UTM acquired-identity manifest;
- the Ubuntu release-evidence manifest;
- the x/sys proxy manifest;
- the Ubuntu snapshot-metadata manifest;
- the no-execution manifest;
- the complete sealed-inventory manifest; and
- the Gate 2 completion manifest.

Canonical JSON uses UTF-8, RFC 8785 JCS, UTC timestamps, lowercase hexadecimal SHA-256, no floating-point values, and no secret or credential field. Every manifest is hashed; the top-level sealed-inventory digest binds all subordinate manifest digests.

---

## Quarantine, Failure, Cleanup, and Rollback

Any mismatch, unexpected response, partial transfer, unapproved redirect, signature failure, tool ambiguity, signer drift, network attempt, unexpected execution/process/mount, path or permission drift, sanitization failure, or incomplete evidence fails Gate 2.

- Stop immediately and prevent further acquisition.
- Move only the exact failed or partial object into its predeclared quarantine target when that move is already authorized; otherwise leave it untouched and record the stop.
- Preserve failure evidence within the bounded Gate 2 execution evidence. Do not make a mismatched object eligible by renaming, rehashing, reacquiring, or accepting a different source.
- Do not retry, resume, repair, mount again, unseal, or substitute without a new authorization and amended task instance.
- Cleanup is a separate exact-target action. It may remove only paths enumerated as task-created deletion targets after identity revalidation and explicit owner authorization.
- Cleanup must never target `/`, a home directory, repository root, shared cache, wildcard, unresolved variable, symlink, pre-existing UTM installation, unrelated VM, or unrelated user data.
- Rollback means removal of exact Gate 2-created logical state and verification of absence. It cannot prove physical erasure from APFS snapshots, SSD wear-leveling, backups, caches outside the task root, or storage-provider internals.
- If cleanup or absence cannot be proven, Gate 2 remains failed or incomplete and escalates to the host owner and Architecture Gatekeeper.

---

## Evidence Separation and Sanitization

### Protected Local Evidence

The following remain outside Git: personal names; usernames; host serial, UUID, hostname, hardware or network identity; absolute paths; raw authorization signatures; full command output; DNS answers; IP/MAC addresses; mount/device identifiers; UTM signer and entitlement raw output; file inodes; ACLs; quarantine contents; detailed redirect response headers; and the complete static manifest, per-run addendum, execution evidence, and sealed inventory.

### Repository-Safe Evidence

Repository evidence may contain only:

- public repository-controlled artifact identities;
- sanitized task, owner-authorization, host, path, and object identifiers;
- static-manifest and per-run-addendum schema versions and SHA-256 values after their respective acceptance;
- approved redirect hostnames and path constraints without personal network data;
- PASS/FAIL results, bounded timestamps, public signer fingerprints, and public object hashes;
- sealed manifest digests, limitations, stop reason, and Gate 3 recommendation; and
- confirmation of no acquisition beyond scope, no execution, no installation, no VM activity, and no later-gate action.

Sanitization fails closed on an absolute or home-relative path, personal identity, host identifier, credential, cookie, authorization header, signed query value, IP/MAC address, secret, unbounded log, unexpected filename, or digest mismatch.

---

## Gate 2 Acceptance Criteria

Gate 2 is complete and eligible for Gate 3 review only when all of the following are true:

1. the accepted static protected-manifest digest, exact authorization-subject digest, matching owner/Gatekeeper execution decisions, and final decision-bearing addendum digest were valid before action;
2. only the exact inventory and approved redirect chains were contacted;
3. every required object is complete and no extra object exists;
4. all repository-bound sizes, hashes, sums, revisions, signatures, suites, and architecture values match;
5. every snapshot metadata identity is bound to the signed release record, and no `.deb` was acquired;
6. UTM read-only inspection produced complete signer, requirement, runtime, entitlement, notarization, ticket, Gatekeeper, and mounted-image evidence;
7. no Apple network verification occurred;
8. no acquired executable, application, installer, daemon, VM, archive payload, module, ISO, or package ran or was applied;
9. every accepted object was reverified after final movement and sealed with exact permissions and manifest bindings;
10. every partial or rejected object is accounted for in quarantine or an approved exact-target cleanup record;
11. protected and repository-safe evidence passed sanitization and digest verification; and
12. the Gate 2 completion record explicitly opens only Gate 3 review.

Gate 2 completion does not accept the UTM signer identity or any seal. It only makes the exact sealed evidence eligible for Architecture Gatekeeper review.

---

## Separate Gate 3 Architecture Gatekeeper Decision

At Gate 3, the Architecture Gatekeeper must independently review:

- the accepted static-manifest and per-run-addendum digests and their distinct authorization chain;
- complete acquisition and redirect evidence;
- all object, signature, checksum, module, and snapshot metadata;
- UTM Developer ID chain/common name, TeamIdentifier, designated requirement, hardened runtime, entitlements, ticket, offline Gatekeeper result, and mounted-image identity;
- no-execution and no-network-exception evidence;
- quarantine, cleanup, limitations, and residual risks; and
- the sanitized repository record against the protected evidence.

Gate 3 may accept, reject, or require revision. Acceptance makes only the exact sealed artifacts and metadata eligible for a separately authorized Gate 4 host-preparation proposal/action. It does not authorize installation or any later gate.

---

## Sanitized Protected-Authority Decision State

| Decision | Repository-safe state |
|----------|-----------------------|
| Named host owner and Platform Administrator | Supplied in protected authority; repository records only sanitized authority identifier `host-owner-authority-001`. |
| Exact host-task root and future UTM installation target | Supplied in protected authority; no personal identity, host identity, or absolute path is retained in Git. |
| Static protected-manifest creation | Authorized in principle for a later, separately initialized host-manifest session after package publication. This authority creates only the static manifest. |
| Gate 2 acquisition and sealing | Authorized in principle only. This is not execution authorization and does not satisfy either per-run execution decision. |

These decisions resolve the Version 0.1 architecture-review blockers without opening Gate 2. Before any Gate 2 action, the actual static-manifest identifier/digest must be accepted, redirect chains must be resolved under separate authority, the exact per-run addendum must be finalized, both the owner and Architecture Gatekeeper must approve the same authorization-subject digest for its exact task and window, and the final decision-bearing addendum digest must verify.

---

## Hard Stop Conditions

- wrong repository, branch, HEAD, tree, tracking/live state, authority, role, or package version;
- missing or ambiguous named owner, Platform Administrator, host identity, absolute root, static-manifest identifier/digest, static acceptance, per-run-addendum digest, execution decision, redirect chain, authorization window, or exact target;
- any official source conflict with repository identity;
- any checksum, size, signature, signer, module sum, revision, snapshot, suite, component, architecture, filename, or provenance mismatch;
- an additional object, package, module, source, metadata class, endpoint, redirect, proxy, mirror, credential, cookie, telemetry, update, retry, downgrade, or fallback requirement;
- any Apple network-verification requirement;
- any write mount, automatic open, application execution, installation, registration, helper/daemon creation, VM activity, extraction, package application, or cache priming;
- incomplete retained-package inventory presented as an exact package closure;
- path, symlink, ownership, permission, ACL, flag, quarantine, sealing, manifest, or sanitization ambiguity;
- any requirement to modify source, tests, `go.mod`, `go.sum`, ADR-012, AB-012, Registry, deployment, operations, FFFA, customer-data, host, environment, or VM state in this proposal session; or
- any implication that Gate 2 or Gate 3 authorizes installation, VM creation, package application, Linux execution, PLAT-15.1A implementation, deployment, activation, release, or live work.

---

## Product Strategy Board Proposal Assessment

The package fits the existing PLAT-15.1A / PLAT-PB-013 priority and AB-011 architecture-enablement path. It creates no new product capability and narrows future supply-chain work into an auditable gate. The supplied protected authority resolved the Version 0.1 portfolio blockers without exposing protected values; Version 0.2 received portfolio approval and Version 1.0 applies the approved design. Product Strategy Board decision: **Approved for repository publication**. Staging/commit and push/publication remain separate governed actions and do not authorize static-manifest creation, Gate 2, or any host action.

---

## Architecture Gatekeeper Review

Version 1.0 preserves the conformant Version 0.2 architecture: exact-object acquisition, stable canonical-origin policy, protected and time-bound redirect chains, offline-first UTM identity inspection, signed Ubuntu metadata, exact Go/module identity, protected-local authority, read-only seals, evidence separation, and a distinct Gate 3 decision.

Architecture Gatekeeper decision: **Approved for repository publication**. The Version 0.1 circularity remains resolved by separating static host authority, per-run execution authority, execution evidence, and final sealed inventory. Static authority remains valid without execution approval; Gate 2 becomes authorized only after package publication, static-manifest creation and acceptance, redirect resolution under separate authority, exact addendum finalization, and matching owner/Gatekeeper execution decisions. The unresolved acquired UTM signer identity and later retained-package closure remain deliberately evidence-driven and are not defects while the approved stop gates remain intact.

---

## Explicit Non-Authorization

Even successful Gate 2 completion would not authorize installation, VM creation, VM startup, package application, Linux execution, source ingress, PLAT-15.1A source or test implementation, `go.mod` or `go.sum` change, artifact acceptance, deployment, daemon interaction, observation, consumer work, activation, release, or live work.

This Version 1.0 package remains `Proposed`, approved by the Product Strategy Board and Architecture Gatekeeper for repository publication, `Not Published`, and Gate 2 `Not Authorized`.

---

## Related Documents

- [PLAT-15.1A Source Implementation Work Package](PLAT_15_1A_Repository_Only_Socket_Capable_Privileged_Proxy_Source_Implementation_Work_Package.md)
- [PLAT-15.1A Supported-Linux Prerequisite Proposal](PLAT_15_1A_Supported_Linux_Validation_Environment_Prerequisite_Proposal.md)
- [PLAT-15.1A Supported-Linux Environment Preparation Work Package](PLAT_15_1A_Supported_Linux_Validation_Environment_Preparation_Work_Package.md)
- [PLAT-15.1A Continuity Brief](../../engineering-organization/ai-collaboration/operational/milestone-15/PLAT_15_1A_Continuity_Brief.md)
- [Product Backlog](../../product/Product_Backlog.md)
- [Architecture Backlog](../../architecture/Architecture_Backlog.md)
- [ADR-012](../../architecture/decisions/ADR-012-Purpose-Built-Constrained-Privileged-Proxy.md)
- [Current Architecture State](../../architecture/Current_Architecture_State.md)
- [Milestone 15 Portfolio Plan](Milestone_15_Portfolio_Plan.md)
- [Engineering Portfolio Kanban](../../portfolio/Engineering_Portfolio_Kanban.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Promoted the approved Version 0.2 design to publication-ready repository authority; versioned both protected schemas for publication; retained the four-artifact separation, non-circular digest model, protected time-bound redirects, and eight distinct gates; recorded validation-complete publication readiness with separate staging/commit authority required; and kept publication, protected-manifest creation, Gate 2, host, environment, implementation, deployment, activation, release, and live gates closed. |
| 0.2 | Reconciled protected authority without retaining protected values; separated static host authority, per-run execution authorization, execution evidence, and final sealed inventory; made redirect chains exact, protected, time-bound, and separately resolved before bytes; defined the non-circular gate sequence; and recorded Board/Gatekeeper approval for repository publication preparation only while retaining publication, static-manifest creation, Gate 2, host, environment, implementation, deployment, activation, release, and live gates closed. |
| 0.1 | Proposed the exact future Gate 2 artifact/archive-metadata acquisition and read-only sealing authority, protected-local JSON schema, canonical/redirect network boundary, verification and quarantine controls, no-execution evidence, Gate 2 acceptance criteria, separate Gate 3 decision, and four blocking named-owner decisions while retaining every host, environment, implementation, publication, deployment, activation, release, and live gate closed. |
