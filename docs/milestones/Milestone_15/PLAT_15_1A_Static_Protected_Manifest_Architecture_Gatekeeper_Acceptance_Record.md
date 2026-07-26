# PLAT-15.1A Static Protected-Manifest Architecture Gatekeeper Acceptance Record

**Document Version:** 1.0

**Architecture Gatekeeper Decision:** Accept

**Acceptance State:** Accepted

**Record Publication State:** Not Published

**Gate 2 State:** Not Authorized

---

## Record Identity

| Field | Repository-safe value |
|-------|-----------------------|
| Acceptance-record ID | `plat15a-static-manifest-acceptance-001` |
| Manifest-creation record ID | `plat15a-static-manifest-creation-001` |
| Decision authority | Architecture Gatekeeper |
| Decision | `Accept` |
| Repository acceptance-recording time | `2026-07-26T14:59:48Z` |
| Published package version | `1.0` |
| Published package commit | `fc9d2bd298e478d3ecf5f6f770de1429fc3e9bab` |
| Published package tree | `51ac7efc3f6f394f33986a321431b108e2a0d7e5` |
| Sanitized manifest ID | `plat-15-1a-gate-2-static-host-001` |
| Static-manifest schema version | `1.0` |

The recording time is the UTC time at which this repository-safe record was prepared. It is not a private decision timestamp and does not replace protected authority evidence.

---

## Accepted Digests and Coverage

| Evidence | SHA-256 | Coverage | Result |
|----------|---------|----------|--------|
| Accepted canonical static-manifest subject | `46a1110d3e132420c771a8414c32746c418b0f8583ea5a5e99001ce1f491a9e9` | RFC 8785 JCS-equivalent canonical bytes for the complete static manifest with `manifest_digest` omitted | PASS |
| Complete static-manifest file transport evidence | `2f0a5ec1602fc4d883958d4c533df6c18a5d6fd3c51bb51a5482c1144add0d6d` | Exact complete canonical manifest-file bytes | PASS |

Future `accepted_static_manifest.sha256` must contain the accepted canonical static-manifest subject SHA-256. The complete-file transport SHA-256 is separate evidence. The two values are non-interchangeable.

---

## Sanitized Gatekeeper Review Results

| Review | Result |
|--------|--------|
| Repository authority, package version, commit, and tree | PASS |
| Static-manifest sanitized identity and schema version | PASS |
| Embedded and independently recomputed manifest-subject digest | PASS |
| Complete-file transport digest | PASS |
| Draft 2020-12 Version 1.0 schema | PASS |
| Restricted-domain RFC 8785 JCS-equivalent canonicalization | PASS |
| Current-host match against protected evidence | PASS |
| Exact protected path boundary and future-path absence | PASS |
| Ownership, permission, ACL, symlink, and hard-link controls | PASS |
| Static-only authorization scope and retained-container classification | PASS |
| Unexpired retention, empty amendment list, and destruction authorization controls | PASS |
| Execution, acquisition, redirect, addendum, and later-decision absence | PASS |

The Architecture Gatekeeper accepts the exact sanitized manifest identity and canonical subject digest above. Passing validation did not imply acceptance; this explicit decision records acceptance.

---

## Authority Boundary

This acceptance applies only to the static protected host-authority manifest represented by the sanitized identity and accepted subject digest above. It does not authorize:

- preparation of a per-run execution-authorization addendum;
- redirect resolution or network endpoint contact;
- artifact acquisition, download, inspection, mount, installation, or execution;
- VM creation, start, or use;
- Gate 2 execution or completion;
- repository implementation, deployment, activation, release, or live work.

Gate 2 remains `Not Authorized`.

---

## Publication and Next Gate

This Version 1.0 acceptance record is publication-ready and remains `Not Published`. Its preparation does not authorize staging, commit, push, or publication.

The immediate next repository gate is separate staging-and-commit authorization for the exact sanitized acceptance-record publication package. Push remains a later separate authorization.

Only after this acceptance record is separately published may a separately authorized session prepare the exact protected per-run execution-authorization addendum and separately governed redirect resolution. Publication does not itself authorize either action or Gate 2.

---

## Repository-Safe Data Boundary

This record intentionally contains only repository-safe identifiers, repository authority, accepted static-manifest hashes, digest coverage, decision state, and sanitized review results. It contains no protected identity, protected location, private authorization, supporting-evidence digest, credential, or reversible mapping.

---

## Related Repository Authority

- [Gate 2 Artifact and Archive-Metadata Acquisition and Sealing Authorization Package](PLAT_15_1A_Artifact_and_Archive_Metadata_Acquisition_and_Sealing_Authorization_Package.md)
- [Supported-Linux Validation Environment Preparation Work Package](PLAT_15_1A_Supported_Linux_Validation_Environment_Preparation_Work_Package.md)
- [PLAT-15.1A AI Session Initialization Record](../../engineering-organization/ai-collaboration/operational/milestone-15/PLAT_15_1A_AI_Session_Initialization_Record.md)
- [PLAT-15.1A AI Session Completion Report](../../engineering-organization/ai-collaboration/operational/milestone-15/PLAT_15_1A_AI_Session_Completion_Report.md)
- [PLAT-15.1A Continuity Brief](../../engineering-organization/ai-collaboration/operational/milestone-15/PLAT_15_1A_Continuity_Brief.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Recorded the Architecture Gatekeeper's explicit acceptance of the sanitized Version 1.0 static-manifest identity and canonical subject digest; retained the complete-file hash as separate transport evidence; kept the record Not Published and Gate 2 Not Authorized; and opened only the separate repository staging-and-commit gate. |
