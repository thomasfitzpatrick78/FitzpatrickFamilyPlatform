# Privileged Proxy Security Test Specification

**Document Version:** 1.0

**Status:** Published Future Test Gate; Tests Not Executed

**Milestone:** PLAT-14.1A named prerequisite

---

## Purpose

This specification defines the exact positive and negative test evidence required before a future implementation may enter privileged deployment review. Repository-only fixtures must remain socket-, Docker-, network-, credential-, and deployment-incapable. Later isolated integration tests require separate authorization.

## Common Pass Rule

Unless a row states otherwise, the precondition is an approved synthetic target, exact service identity, valid short-lived one-shot authorization, matching policy/configuration/deployment/Registry/artifact digests, healthy audit store, and supported versions. A test passes only when:

1. the exact result and reason code occur;
2. the mandatory allow/deny/failure audit event contains safe correlation and exact digests;
3. no unapproved Docker request is generated;
4. no raw provider/secret field appears;
5. resource and time limits are honored; and
6. repeated execution is deterministic.

## Positive Tests

| ID | Precondition and input | Expected result / reason | Audit evidence | Pass rule |
|----|------------------------|--------------------------|----------------|-----------|
| P-01 | Valid `ObserveLifecycle` for exact target. | One projected lifecycle result / `request_completed`. | Identity, authorization, request accepted, target verified, completion. | Only fixed inspect behavior; approved fields only. |
| P-02 | Valid `ObserveHealth`; Registry requires health check. | One health result / `request_completed`. | Same plus health category. | No health log/command/output field. |
| P-03 | Valid `ObserveRestartInformation`. | One restart result / `request_completed`. | Same plus restart category. | Exact count/state only. |
| P-04 | Valid conditional `ResolveTargetIdentity`, one match. | Resolution `exact` / `request_completed`. | Conditional policy and target verification. | One result; no raw label map. |
| P-05 | Valid conditional `ObserveStatisticsOnce`. | One bounded stats result / `request_completed`. | Conditional policy, one-shot marker, size. | `stream=false`; no second record or connection reuse. |
| P-06 | Future separately authorized compatibility policy and fixed version check. | Bounded compatibility result / `request_completed`. | Policy version showing `System` authorization. | Under current v1.0 fixture this test must deny; execute only after policy approval. |
| P-07 | Exact configured peer UID/GID/PID plus complete authorization controls. | Peer context accepted; request proceeds only after signed authorization, target/time/scope, and every digest validate. | `identity_accepted` followed by authorization and digest events. | Proves peer credentials are necessary but not independently sufficient. |
| P-08 | Valid signed one-shot authorization. | Authorization accepted. | `authorization_accepted` with reference, never signature. | Signature/content/digests/time verified. |
| P-09 | Matching policy/configuration/deployment/Registry/adapter/proxy/trust-anchor/trust-binding digests. | Digest verification success. | `digest_verified` for each class. | Recomputed canonical digests match. |
| P-10 | Provider returns approved plus prohibited fields. | Approved projection succeeds. | `response_filtered` with removed-field count only. | Canary prohibited values absent from response/logs. |
| P-11 | Audit and replay store available. | Nonce durably committed before provider call. | Ordered acceptance then provider event. | Restart preserves replay denial. |
| P-12 | Independent disablement with no in-flight request. | Adapter socket removed; proxy stops. | `disablement_started`, `shutdown`. | Observed workload untouched. |

## Authentication and Authorization Negative Tests

| ID | Input | Expected result / reason | Audit | Pass rule |
|----|-------|--------------------------|-------|-----------|
| N-01 | No peer credentials/unsupported transport. | Denied / `identity_missing`. | `identity_rejected`. | Zero provider calls. |
| N-02 | Wrong UID or GID. | Denied / `identity_mismatch`. | Safe expected/observed class, not sensitive details. | Zero provider calls. |
| N-03 | Revoked service identity. | Denied / `identity_revoked`. | Revocation reference. | Zero provider calls. |
| N-04 | Missing authorization object. | Denied / `authorization_missing`. | `authorization_rejected`. | Zero provider calls. |
| N-05 | Bad signature or changed signed field. | Denied / `authorization_invalid`. | Signer reference and reason. | Zero provider calls. |
| N-06 | Expired authorization. | Denied / `authorization_expired`. | Window classification. | Zero provider calls. |
| N-07 | Future authorization beyond 30-second skew. | Denied / `authorization_future`. | Clock/skew reason. | Zero provider calls. |
| N-08 | Revoked signer/trust anchor. | Denied / `authorization_revoked`. | Revocation reference. | Zero provider calls. |
| N-09 | Reused nonce before restart. | Denied / `authorization_replayed`. | Replay event. | Zero second provider call. |
| N-10 | Reused nonce after restart. | Denied / `authorization_replayed`. | Recovered-journal replay event. | Durable replay proof. |
| N-10A | Replay store unavailable, ambiguous, corrupt, stale beyond policy, or unable to persist. | Denied / `audit_unavailable` or stable fail-closed replay reason. | Replay-state failure and not-ready event. | Zero provider calls; no best-effort fallback. |
| N-11 | Authorization for another target. | Denied / `target_mismatch`. | Target mismatch. | Zero provider calls. |
| N-12 | Authorization with wildcard/population target. | Denied / `wildcard_denied`. | Request denial. | Parser never creates provider query. |

## Request and Protocol Negative Tests

| ID | Input | Expected result / reason | Audit | Pass rule |
|----|-------|--------------------------|-------|-----------|
| N-13 | Wrong protocol major/minor. | Denied / `protocol_unsupported`. | Version mismatch. | No fallback. |
| N-14 | Unknown operation/future category. | Denied / `operation_denied`. | Category denial. | No generic dispatch. |
| N-15 | Current-policy compatibility operation. | Denied / `category_denied`. | `System` denial and policy digest. | No Docker ping/version request. |
| N-15A | Documentation or dispatcher contains a reserved compatibility mapping without explicit policy/configuration approval. | Denied / `category_denied`. | Reserved-operation denial. | No live compatibility test or Docker request. |
| N-16 | Arbitrary Docker path/URL/method/query/header field. | Denied / `unknown_field`. | Schema rejection. | Forbidden string never reaches dispatcher. |
| N-17 | Caller-supplied Docker container ID. | Denied / `unknown_field`. | Schema rejection. | ID must be derived internally. |
| N-18 | Duplicate JSON key. | Denied / `duplicate_field`. | Parser rejection. | No last-key-wins behavior. |
| N-19 | Unknown key/parameter. | Denied / `unknown_field`. | Parser rejection. | No ignore behavior. |
| N-20 | Alternate Unicode/percent/overlong target encoding. | Denied / `target_invalid`. | Normalization rejection. | No normalized bypass. |
| N-21 | Dot segments, slash, NUL, traversal, or encoded-path string. | Denied / `target_invalid`. | Validation rejection. | No filesystem/provider interpretation. |
| N-22 | Method-override or protocol-upgrade marker. | Denied / `unknown_field` or `request_malformed`. | Protocol denial. | No HTTP semantic interpretation. |
| N-23 | Request body/payload extension. | Denied / `unknown_field`. | Schema denial. | No raw body accepted. |
| N-24 | Frame length 16,385 bytes. | Denied / `request_oversized`. | Size event. | Body not fully allocated or parsed. |
| N-25 | Partial frame, extra frame, trailing bytes, or second request. | Denied / `request_malformed`. | Framing event. | Connection closes. |
| N-26 | Invalid UTF-8, NaN, exponent abuse, deep nesting, huge count. | Denied / `request_malformed`. | Parser-limit event. | Bounded memory/time. |
| N-27 | Deadline over 10 seconds or before request time. | Denied / `deadline_invalid`. | Deadline reason. | No provider call. |
| N-28 | Signal not allowed for operation. | Denied / `signal_denied`. | Signal/category reason. | No provider call. |

## Docker Mediation and Response Negative Tests

| ID | Input/upstream behavior | Expected result / reason | Audit | Pass rule |
|----|-------------------------|--------------------------|-------|-----------|
| N-29 | Exact filter returns no target. | Failed / `target_absent`. | Resolution failure. | No inspect/stats follow-up. |
| N-30 | Filter returns two or more targets. | Failed / `target_duplicate` or `target_ambiguous`. | Count only. | No target selected. |
| N-31 | Response identity differs from authorization. | Failed / `target_mismatch`. | Target mismatch. | Entire response discarded. |
| N-32 | Provider returns unsupported API version. | Failed / `provider_version_unsupported`. | Version mismatch. | No downgrade/negotiation. |
| N-33 | Redirect or unexpected status/header/content type. | Failed / `upstream_protocol_rejected`. | Protocol rejection. | Redirect never followed. |
| N-34 | Chunked, compressed, streaming, upgrade, hijack, or informational response. | Failed / `upstream_protocol_rejected`. | Protocol class. | Connection closed; no pass-through. |
| N-34A | Conflicting/multiple `Content-Length`, `Content-Length` plus `Transfer-Encoding`, invalid transfer coding, folded header, or request-smuggling response pattern. | Failed / `upstream_protocol_rejected`. | Ambiguity class only. | First ambiguous byte sequence closes connection; no alternate parser interpretation. |
| N-34B | Adapter frame with conflicting length semantics, nested HTTP request, absolute-form URI, CONNECT preface, or header-injection delimiters. | Denied / `request_malformed`. | Framing/protocol denial. | Payload is never interpreted as HTTP, gRPC, or tunnel input. |
| N-35 | Attach/exec/log/events or gRPC-equivalent attempt in fixture dispatcher. | Denied / `operation_denied`. | Category/protocol denial. | Static route graph contains no handler. |
| N-36 | Malformed JSON or duplicate upstream fields. | Failed / `response_malformed`. | Response rejection. | No partial result. |
| N-37 | Upstream body 65,537 bytes. | Failed / `response_oversized`. | Size event. | Bounded reader stops and discards. |
| N-38 | More than one projected result. | Failed / `record_limit_exceeded`. | Record count. | No truncation-as-success. |
| N-39 | Prohibited response field carries canary secret. | Failed or safe projection / `response_field_rejected` or `request_completed`. | Removed/rejected classification only. | Canary absent everywhere outside test fixture. |
| N-40 | Health log, command, env, mount, network, raw labels present. | Safe projection or failure under version contract. | Response filtering event. | Every prohibited field absent. |
| N-41 | Malformed/overflow numeric stats. | Failed / `response_malformed`. | Field classification. | No wrap, NaN, or partial stats. |
| N-42 | Docker connect unavailable. | Failed / `provider_unavailable`. | Upstream error class. | Safe message; no raw path/error. |
| N-43 | Docker response exceeds 3 seconds. | Failed / `upstream_timed_out`. | Timeout and latency. | Total under 10 seconds; connection closed. |
| N-44 | Response amplification attempt. | Failed / size/record reason. | Limit event. | Memory remains bounded. |

## Resource, Audit, and Lifecycle Negative Tests

| ID | Input/condition | Expected result / reason | Audit | Pass rule |
|----|-----------------|--------------------------|-------|-----------|
| N-45 | Fifth global or third identity concurrent request. | Denied / `concurrency_exhausted`. | Capacity denial. | No unbounded queue/provider call. |
| N-46 | Seventh request in minute or burst above two. | Denied / `rate_limited`. | Rate denial. | Token bucket deterministic under test clock. |
| N-47 | Slow client exceeds 1-second frame read. | Denied / `request_timed_out`. | Timeout. | FD released. |
| N-48 | Audit store absent, full, read-only, corrupt, or append fails. | Denied / `audit_unavailable`; not ready. | Best available host/startup event. | Zero new provider calls. |
| N-49 | Replay journal commit fails. | Denied / `audit_unavailable`. | Failure event if possible. | Zero provider calls. |
| N-50 | Docker socket mode/owner/inode changes. | Denied / `provider_unavailable`; not ready. | Socket-drift event. | No connection through drifted socket. |
| N-51 | Adapter socket replaced with symlink/wrong mode. | Startup/request denied / `identity_mismatch`. | Socket-drift event. | No acceptance. |
| N-52 | Memory, PID, or FD limit pressure. | Bounded fail-closed response or process stop; restart disabled. | Resource event when possible. | Observed workload unaffected. |
| N-53 | Disablement while requests are in flight. | Reject new; drain/cancel by 15 seconds; stop. | Ordered disablement/shutdown events. | No Docker mutation; adapter stopped first. |
| N-54 | Disablement command/path fails. | `proxy_disabled`/deployment failure. | Failure escalation. | Privileged deployment gate fails. |
| N-55 | Rollback digest/signature/config mismatch. | `rollback_required`; remain disabled. | Rollback rejection. | No fallback to floating/unknown artifact. |
| N-56 | Valid known-good rollback set. | Rollback completes only under later approved procedure. | Old/new exact digests. | Negative suite reruns before access. |
| N-57 | Image digest differs from approved manifest. | Artifact/deployment rejection. | Supply-chain mismatch. | Proxy never starts. |
| N-58 | Missing/invalid SBOM, provenance, signature, or unsupported runtime. | Artifact/deployment rejection. | Supply-chain reason. | No privileged review promotion. |

## Static Implementation Tests

Future source review and automated checks must prove:

- no Docker SDK, reverse-proxy package, generic router, dynamic plugin, shell, subprocess, DNS, TCP, UDP, raw socket, environment override, credential loader, certificate loader, Registry mutation, health calculation, consumer, scheduler, or remediation import/path;
- the Docker dispatcher contains only the reviewed fixed request constructors;
- every public enum and JSON field is closed;
- all parser entry points use bounded readers and reject duplicates;
- every allowed field has an explicit projection and every omitted field is denied by default;
- every security decision emits one reason-coded audit path;
- fuzzing covers public framing/JSON, authorization canonicalization, upstream HTTP parsing, Docker JSON parsing, and response projection.

## Evidence Package

Test evidence records exact source revision, binary/image digest, toolchain and dependency lock, policy/configuration/deployment digests, fixture digests, test seed/corpus version, host/runtime for later integration tests, start/end timestamps, expected and actual reason codes, audit references, and pass/fail. Any skipped negative test is a failure unless the Architecture Gatekeeper explicitly removes the unreachable capability from the test matrix and records why.

## Related Documents

- [Non-Docker Adapter Interface Specification](Privileged_Proxy_Non_Docker_Adapter_Interface_Specification.md)
- [Privileged Proxy Threat Model](../architecture/Privileged_Proxy_Threat_Model.md)
- [Implementation Acceptance Checklist](../milestones/Milestone_14/Privileged_Proxy_Implementation_Acceptance_Checklist.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Published positive, negative, static, resource, audit, replay, authority-expansion, disablement, rollback, and supply-chain tests with exact reason and audit expectations. |
