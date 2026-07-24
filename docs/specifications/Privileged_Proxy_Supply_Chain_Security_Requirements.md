# Privileged Proxy Supply-Chain Security Requirements

**Document Version:** 1.1

**Status:** Architecture Gatekeeper Approved and Published v1.1 Requirements; No Build Authorized

**Milestone:** PLAT-14.1A named prerequisite

---

## Purpose

This specification defines evidence required before a future proxy artifact may enter privileged deployment review. It does not authorize source implementation, dependency download, build, image publication, or deployment.

## Selected Source and Runtime Strategy

- Source: a future reviewed path in this repository at one exact commit.
- Language snapshot: Go `1.26.5`, a review-time input that must be revalidated and explicitly rebound at implementation acceptance.
- Initial external module ceiling: `golang.org/x/sys` `v0.47.0`, also a review-time input requiring exact revalidation and binding at implementation acceptance.
- Final artifact: static `CGO_ENABLED=0` Linux binary in a `scratch` OCI image.
- License posture: Go and `x/sys` are BSD-style; the future proxy source license and complete notice bundle require repository-owner approval.
- Update model: assess Go security releases, `x/sys` releases, Docker Engine/API changes, build-platform advisories, and scanner database changes at implementation, before every deployment, monthly while deployed, and after any relevant advisory.

## Mandatory Evidence

| Evidence | Pass condition |
|----------|----------------|
| Source repository/revision | Exact repository URL, commit SHA, clean tree, reviewed diff, and protected publication path. |
| Toolchain | Exact Go version and official archive/source checksum; still supported on review date. |
| Dependency lock | Complete `go.mod` and `go.sum`; no replacements, local paths, pseudo-versions, or unreviewed transitive module. |
| Source review | All privileged boundary, parser, authorization, Docker dispatcher, audit, and error paths independently reviewed. |
| Reproducible build | Hermetic documented inputs; two isolated builds produce matching binary and OCI manifest digests, or every variance is explained and removed before acceptance. |
| Immutable artifact | Exact per-platform image digest and multi-platform manifest digest; no tag is an approval identity. |
| SBOM | Primary SPDX 3.0.1 JSON-LD inventory covers source, Go toolchain, modules, builder inputs, binary, per-platform image, multi-platform index, licenses, relationships, and checksums; CycloneDX may be supplementary only. |
| Provenance | In-toto Statement using SLSA provenance predicate `https://slsa.dev/provenance/v1`, subject-bound to each binary, platform manifest, and index, with source revision, builder ID, build type, workflow, resolved dependencies, and external parameters. Minimum Build L2; Build L3 before recurrence. |
| Signature | Cosign-compatible keyless OIDC signature from the approved hosted builder with offline-verifiable Sigstore bundle, exact certificate issuer/workflow identity, claims, digest, and transparency inclusion material. No silent local-key fallback. |
| Signature verification | Independent verification checks certificate/identity, issuer, transparency/inclusion material where used, claims, artifact digest, and policy. |
| Base image | `scratch`; builder image/toolchain inputs remain pinned and inventoried. Any nonempty final base requires separate approval, provenance, SBOM, signature, and digest. |
| Vulnerability review | `govulncheck`, Go vulnerability database, OSV/CVE/SCA, binary, image, and secret scans; findings mapped to reachable code and privileged threat model. |
| License review | All direct/transitive licenses, notices, incompatibilities, and distribution duties reviewed. |
| Release notes/advisories | Go, `x/sys`, Docker API, build platform, and signing tool changes reviewed against the selected versions. |
| Runtime support | Exact host architecture, kernel, container runtime, Docker Engine/API, seccomp, and AppArmor compatibility documented. |
| Rollback | Previously approved signed digest, compatible configuration/policy, and retention period remain available and verified. |
| End-of-life | Trigger at upstream support end, critical unsupported dependency, signing-root change, or unmaintained source; disable before unsupported operation. |

Every toolchain, dependency, source, Docker API, container-base, image, maintenance, advisory, vulnerability, license, provenance, signature, SBOM, and end-of-life input must be revalidated at implementation acceptance. Architecture publication grants no permission to retrieve dependencies or produce an artifact.

## Immutable Engineering Identity

Each future privileged artifact possesses one immutable engineering identity derived from all of:

- exact privileged-proxy implementation revision;
- exact repository source revision;
- exact per-platform and index SBOM subject digests;
- exact per-platform and index provenance subject digests;
- exact signature subjects, certificate issuer/workflow identity, verifier policy, and offline bundle;
- exact approved configuration digest.

The acceptance record serializes these constituents in one canonical identity manifest and binds its SHA-256 digest into artifact, deployment, authorization, audit, and rollback evidence. No field is optional. A changed, absent, ambiguously resolved, or mismatched constituent is a different unapproved engineering identity and blocks artifact acceptance.

## Trusted Build and Verification

The trusted build control plane, workflow revision, builder identity, signing identity, and source branch are approval inputs. User-defined build steps must not obtain signing keys. Provenance is verified, not merely present: the artifact subject digest, builder, build type, source, workflow, resolved dependencies, and external parameters must match approved expectations. Two isolated builds must reproduce the binary, platform-manifest, and index digests.

SLSA v1.2 distinguishes provenance existence, hosted signed provenance, and hardened builds. The first privileged deployment requires at least Build L2 and records any gap from Build L3 as a binding risk. Recurring activation requires Build L3 or explicit Architecture Gatekeeper and Platform Administrator exception.

## Blocking Findings

The following block artifact acceptance or privileged deployment:

- floating tag or mutable artifact reference;
- unknown source revision, builder, workflow, or toolchain;
- unpinned or checksum-missing direct/transitive dependency;
- absent/incomplete SBOM;
- absent, invalid, or mismatched provenance;
- absent or unverifiable required signature;
- artifact digest mismatch;
- unsupported Go, Docker API, kernel, runtime, or architecture;
- unresolved applicable Critical vulnerability;
- High vulnerability in an authorization, parser, socket, HTTP, crypto, audit, or sandbox path without approved mitigation and expiry;
- unreviewed license conflict or missing required notice;
- unexpected executable, shell, package manager, CA bundle, credential, or secret;
- unauthorized build path, self-hosted runner without assessed trust, or signing material exposed to build steps;
- irreproducible artifact with unexplained material difference;
- no verified rollback digest.

## Primary References

- [Go release and support policy](https://go.dev/doc/devel/release)
- [Go vulnerability management](https://go.dev/doc/security/vuln/)
- [SLSA v1.2](https://slsa.dev/spec/v1.2/)
- [SLSA artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [Sigstore verification](https://docs.sigstore.dev/cosign/verifying/verify/)
- [SPDX specifications](https://spdx.dev/use/specifications/)

## Related Documents

- [ADR-012](../architecture/decisions/ADR-012-Purpose-Built-Constrained-Privileged-Proxy.md)
- [Privileged Proxy Implementation Architecture](../architecture/Privileged_Proxy_Implementation_Architecture.md)
- [Implementation Acceptance Checklist](../milestones/Milestone_14/Privileged_Proxy_Implementation_Acceptance_Checklist.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Published primary SPDX 3.0.1 JSON-LD, subject-bound SLSA v1 provenance, keyless OIDC signing, per-platform/index reproducibility, and one immutable privileged-artifact engineering identity. |
| 1.0 | Published exact future source, artifact, SBOM, provenance, signature, vulnerability, license, support, revalidation, update, and rollback evidence without authorizing a build. |
