# PLAT-15.1A Version 1.1 Replacement Static Protected-Manifest Architecture Gatekeeper Acceptance Record

**Document Version:** 1.0

**Architecture Gatekeeper Decision:** Accept

**Acceptance State:** Accepted

**Record Preparation Status:** Complete

**Publication Readiness:** Ready - Required Go 1.26.5 validation complete

**Publication State:** Not Published

**Gate 2 State:** Not Authorized

**Environment State:** Not Created

**PLAT-15.1A Repository Implementation:** Not Started

---

## Record Identity

| Field | Repository-safe value |
|-------|-----------------------|
| Acceptance-record ID | `plat15a-static-manifest-acceptance-002` |
| Decision authority | Architecture Gatekeeper |
| Decision | `Accept` |
| Repository recording time | `2026-07-26T19:31:50Z` |
| Published repository / branch | `FitzpatrickFamilyPlatform` / `main` |
| Published package version | `1.1` |
| Published package commit | `3033d2553fdd8829e9af7fc14ace0db2aecdb85e` |
| Published package tree | `e4bd2d00e38f228ee072a7e5946db38e9b4e6ebd` |
| Sanitized manifest ID | `plat-15-1a-gate-2-static-host-002` |
| Static-manifest schema version | `1.1` |
| Manifest kind | `plat-15-1a-gate-2-static-protected-host-authority-manifest` |
| Topology profile | `plat-15-1a-gate-2-exact-hierarchy-v1.1` |
| Amendment ID | `plat15a-static-manifest-v1-1-topology-amendment-001` |

The recording time is repository-safe publication-preparation evidence. It is not a protected decision timestamp and does not replace private authority evidence.

---

## Accepted Digests and Coverage

| Evidence | SHA-256 | Coverage | Result |
|----------|----------|----------|--------|
| Accepted replacement manifest subject | `2fe1e51b0d584511dc9c6561ce7d7930fcc1340f92315641376aa24d591016fb` | RFC 8785 JCS canonical bytes for the complete Version 1.1 manifest with `manifest_digest` omitted | PASS |
| Complete replacement-manifest transport evidence | `ebb4cb66f14bb0abc94c4779a30208a6719e5a99059af1a31f710e928ca70565` | Exact complete canonical Version 1.1 manifest-file bytes | PASS |
| Prior Version 1.0 manifest-subject linkage | `46a1110d3e132420c771a8414c32746c418b0f8583ea5a5e99001ce1f491a9e9` | Lifecycle amendment linkage to the preserved historical subject | PASS |
| Historical Version 1.0 archive transport evidence | `2f0a5ec1602fc4d883958d4c533df6c18a5d6fd3c51bb51a5482c1144add0d6d` | Exact complete canonical historical archive-file bytes | PASS |

The accepted manifest-subject digest and complete-file transport digest have different coverage and are non-interchangeable. A future `accepted_static_manifest.sha256` field may use only the accepted Version 1.1 manifest-subject digest above.

---

## Sanitized Architecture Gatekeeper Review Results

| Review | Result |
|--------|--------|
| Published repository authority and separation of approval and execution gates | PASS |
| Sanitized manifest identity, kind, schema version, and topology profile | PASS |
| Draft 2020-12 Version 1.1 schema | PASS |
| Canonical raw representation and restricted-domain RFC 8785 JCS reproduction | PASS |
| Embedded manifest-subject and complete-file transport digests | PASS |
| Exact planned inventory | PASS - 23 unique entries |
| Mandatory Version 1.1 topology | PASS - all 14 bindings |
| Redundant task-root wrapper | PASS - absent |
| Retained-container boundary | PASS - 2 retained, both non-deletion targets |
| Current protected inventory | PASS - 9 task-tree paths and 2 retained containers present |
| Planned future hierarchy | PASS - 11 paths absent |
| Transient amendment paths | PASS - 3 paths absent |
| Unauthorized protected paths | PASS - 0 |
| Ownership, permissions, ACLs, flags, symlinks, and hard-link controls | PASS |
| Historical archive preservation under current authority | PASS |
| Amendment authority, approved-window execution, and prior-digest linkage | PASS |
| Original creation and host-identity supporting evidence | PASS - unchanged |
| Retention and separate destruction authority | PASS - unexpired and preserved |
| Post-failure reconciliation | PASS |
| Static acceptance and Gate 2 execution separation | PASS |

The amendment's terminal assertion was a non-authoritative diagnostic defect caused by freezing directory link counts across authorized child-file creation. The authorized archive, amendment-scope creation, and atomic manifest replacement completed before that assertion. The assertion did not invalidate the authoritative Version 1.1 amendment operation.

---

## Historical Decision Chain

Acceptance record `plat15a-static-manifest-acceptance-001` remains immutable historical evidence and suspended for execution eligibility. Its accepted subject digest remains prohibited from every future execution addendum. The published suspension record remains immutable historical evidence.

This distinct acceptance, `plat15a-static-manifest-acceptance-002`, satisfies the published Version 1.1 replacement-acceptance requirement for the exact sanitized manifest identity and subject digest recorded above. It does not edit, erase, supersede as history, or reinterpret either historical record. Eligibility for later protected authority begins only after this sanitized record is separately validated, staged, committed, pushed, and publication equality is proved through their separately authorized gates.

---

## Authority Boundary

After separate repository publication, this acceptance opens only eligibility to prepare an exact protected per-run stable-artifact execution-authorization addendum and separately governed redirect-resolution authority. Both require later explicit authorization.

This acceptance does not authorize:

- creation of a per-run addendum;
- redirect or endpoint resolution;
- acquisition, download, artifact inspection, mounting, installation, or execution;
- environment or VM creation or startup;
- Linux execution;
- source, test, module, or repository implementation;
- deployment, activation, release, or live work.

Gate 2 remains `Not Authorized`; the environment remains `Not Created`; PLAT-15.1A implementation remains `Not Started`.

---

## Publication Validation and Next Gate

The exact required Go 1.26.5 Darwin ARM64 validation completed under separate, time-bounded authority. Tool identity, disabled retrieval controls, exclusive use, successful mandatory checks, and complete removal of the temporary toolchain, caches, build state, telemetry-off configuration, and other task-created state were proved. No protected PLAT-15.1A state was inspected or modified.

Every mandatory repository validation has passed. The immediate repository gate is separate staging-and-commit authorization for the exact validated 16-path publication package. Push remains a later separate authorization.

---

## Repository-Safe Data Boundary

This record contains only repository-safe decision state, repository publication identity, sanitized identifiers, accepted manifest digests, historical digest linkage, non-sensitive counts, and sanitized PASS results. It contains no personal or machine identity, protected path, reversible mapping, raw protected evidence, supporting-evidence digest, private authorization content, protected timestamp, filesystem identifier, credential, secret, or acquired-artifact data.

---

## Related Repository Authority

- [Version 1.1 Gate 2 Acquisition and Sealing Authorization Package](PLAT_15_1A_Artifact_and_Archive_Metadata_Acquisition_and_Sealing_Authorization_Package.md)
- [Static Protected-Manifest Acceptance Suspension Record](PLAT_15_1A_Static_Protected_Manifest_Acceptance_Suspension_Record.md)
- [Historical Version 1.0 Acceptance Record](PLAT_15_1A_Static_Protected_Manifest_Architecture_Gatekeeper_Acceptance_Record.md)
- [PLAT-15.1A Continuity Brief](../../engineering-organization/ai-collaboration/operational/milestone-15/PLAT_15_1A_Continuity_Brief.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded completion of the separately authorized exact Go 1.26.5 validation and cleanup proof; marked the package ready only for separate staging-and-commit authorization while retaining publication and all protected and execution gates closed. |
| 1.0 | Recorded the distinct Architecture Gatekeeper acceptance of the corrected Version 1.1 static-manifest identity and subject digest; preserved the historical acceptance and suspension records; retained every execution and delivery gate closed; and recorded the unavailable Go 1.26.5 validation gate without claiming publication readiness. |
