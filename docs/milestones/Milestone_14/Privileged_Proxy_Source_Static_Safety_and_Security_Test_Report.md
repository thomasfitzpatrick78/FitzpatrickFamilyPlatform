# Privileged Proxy Source Static Safety and Security-Test Report

**Document Version:** 1.1

**Status:** Published Source Evidence

**Scope:** Transport-free repository source

---

## Static Safety

The Go AST validator inspects every Go source and test file. It fails on:

- `net` and all `net/*` packages;
- TLS/certificate loading, SSH, Docker/Moby/container-runtime clients, gRPC, or Kubernetes clients;
- `os/exec`, shell execution, plugins, reflection-based routing, `unsafe`, `syscall`, cgo, or `golang.org/x/sys`;
- environment/current-user discovery and process-environment mutation;
- filesystem calls outside tests and the bounded replay/audit test-store packages.

Platform EAP independently verifies module shape, import boundaries, package layout, required closed interfaces, policy conformance, non-executable source, and the absence of external modules.

## Test Coverage

The Go suites cover:

- byte-stable canonical request and response encoding;
- duplicate, unknown, malformed, trailing, BOM, whitespace, float, exponent/negative-zero, Unicode-confusable, nesting/collection, and byte-limit rejection;
- abstract peer acceptance and rejection;
- Ed25519 success/failure, key selection/revocation, validity/future/expiry/lifetime, one-shot nonce, approval, service identity, operation/signal, exact selector, and every digest mismatch;
- memory and ordinary-file replay first use, duplicate use, concurrent replay, capacity, persistence, checksum corruption, partial replacement, staleness, unreadable/unwritable state, and independent authorization-reference/nonce reuse;
- complete Proxy Foundation matrix compilation, default deny, reserved `System`, and unknown operation denial;
- five positive typed pipeline operations;
- target substitution, wildcard, case/encoding/confusable inputs, response leakage markers, multiple result types, target mismatch, record limit, and response-size rejection;
- injected-clock rate, concurrency, total-deadline, and upstream-budget behavior;
- canonical audit sequencing/redaction, pre-access sink failure, disablement, cancellation after nonce consumption, and zero upstream invocations for pre-boundary denials;
- static-safety self-tests that prove prohibited imports and calls are detected.

Fuzz seed targets exercise request decoding/canonical JSON, authorization canonical content, digest/reason serialization, replay-journal decoding, and the core request boundary. Active fuzz validation is bounded; no target opens a socket, contacts Docker, uses real time, or writes outside a temporary directory.

## Security Findings

During source review, selector fields were found to require direct signature coverage in addition to the Registry record digest. The implementation now signs and compares selector kind, Compose project/service, and governed runtime name. A selector-substitution test proves denial before upstream invocation.

No material architecture deviation or prohibited capability was found.

## Remaining Security Proof

This report does not prove Unix framing, real `SO_PEERCRED`, socket metadata, Docker request construction, Docker response parsing, production persistence, runtime confinement, binary/image composition, host compatibility, or privileged deployment. Those remain required by the published Security Test Specification.

## Result

**Transport-free source security tests:** Pass; Architecture Gatekeeper approved and accepted this source-level evidence for publication.

**Socket-capable or privileged implementation acceptance:** Not evaluated and not authorized.

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded publication acceptance of the passing source-level security evidence without extending it to sockets, Docker, artifacts, or deployment. |
| 1.0 | Recorded source-level static and security-test coverage while retaining all socket, Docker, artifact, and deployment gates. |
