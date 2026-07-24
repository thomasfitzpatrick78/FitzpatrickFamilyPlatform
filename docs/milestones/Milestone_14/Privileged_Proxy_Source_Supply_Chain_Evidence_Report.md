# Privileged Proxy Source Supply-Chain Evidence Report

**Document Version:** 1.1

**Status:** Published Source Evidence; Artifact Evidence Incomplete

---

## Toolchain

| Item | Binding |
|------|---------|
| Go version | `go1.26.5 darwin/arm64` |
| Official archive | `go1.26.5.darwin-arm64.tar.gz` |
| SHA-256 | `efb87ff28af9a188d0536ef5d42e63dd52ba8263cd7344a993cc48dd11dedb6a` |
| Source | `https://go.dev/dl/` |
| Support evidence | Go release history records Go 1.26.5 on 2026-07-07; exact support/security status must be rechecked at artifact acceptance |

The official archive was downloaded to a temporary directory, its checksum matched, and it was extracted without installing into a system path.

## Dependencies and Licenses

`go.mod` binds Go 1.26.5. `go.sum` has zero entries because the module uses the Go standard library only. There is no `require` directive and no Docker SDK, `golang.org/x/sys`, network, web, logging, cryptographic, shell, SSH, container-runtime, or deployment module.

| Component | Version | License evidence |
|-----------|---------|------------------|
| Go toolchain and standard library | 1.26.5 | Go project BSD-3-Clause license at `https://go.dev/LICENSE` |
| External modules | None | Not applicable |

The reviewed `x/sys` architecture snapshot is not retrieved or used because real peer-credential inspection is outside this source gate.

## Build and Module Rules

```text
go mod verify
go test ./...
go test -race ./...
go vet ./...
go build -trimpath -buildvcs=false ./...
```

No binary is committed or published. Build output remains temporary/cache-only. No OCI image, container base, manifest, image SBOM, provenance, or signature is created.

## Source Revision and Inventory

The published source is based on architecture publication commit `9b1eb3c7b60937b5ff14abc03023326ba65dd6cf`. The containing Git publication commit is the canonical source revision and is recorded by repository history and publication evidence. Machine-readable evidence retains a `null` self-reference because a commit cannot embed its own final hash in the same one-commit publication.

Machine-readable evidence is [supply-chain-evidence.json](../../../engineering/privileged_proxy/supply-chain-evidence.json). Platform EAP inventories the Go source, tests, module lock, and evidence without building.

## Vulnerability and SBOM Status

The module has no external dependencies. `govulncheck` is not available in the repository environment, so toolchain/standard-library vulnerability scanning remains a documented gap rather than a fabricated pass. A source inventory is available, but no accepted artifact SBOM exists.

Before artifact acceptance, the later gate must bind:

- accepted source commit and isolated builder/workflow digest;
- current Go vulnerability database and broader advisory review;
- complete source and binary SBOM;
- reproducible-build evidence from two isolated builds;
- provenance attestation and trusted builder identity;
- artifact and manifest digests;
- signature verification;
- supported Docker/API/container-base versions and end-of-life status.

## Provenance and Signing Plan

No SLSA level is claimed. Future artifact work must generate provenance and signatures from an approved isolated builder and verify them independently before privileged deployment review. Production signing keys do not enter this repository or source package.

## Result

**Source publication supply-chain evidence:** Architecture Gatekeeper approved and accepted for transport-free source publication with the explicitly documented `govulncheck`, artifact SBOM, provenance, reproducibility, and signing gaps.

**Binary or OCI artifact acceptance:** Not ready.

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded Architecture Gatekeeper acceptance and one-commit source-publication revision semantics while retaining all artifact-evidence gaps. |
| 1.0 | Bound the exact temporary Go toolchain and standard-library-only module while documenting every remaining artifact-evidence gap. |
