# Privileged Proxy Source Repository Usage

**Document Version:** 1.1

**Status:** Published Source Guidance; No Runtime Authority

---

## Scope

These commands inspect or test repository source only. They do not start a service, open a socket, contact Docker, load credentials, deploy, or observe a target.

## Platform EAP Inspection

```bash
./platform-eap privileged-proxy source validate
./platform-eap privileged-proxy source contract
./platform-eap privileged-proxy source policy
./platform-eap privileged-proxy source fixtures
./platform-eap privileged-proxy source supply-chain
./platform-eap privileged-proxy source static-safety
./platform-eap privileged-proxy source acceptance
```

These commands do not build by default. They read the source tree, governed Proxy Foundation policy fixture, module files, synthetic tests, and supply-chain evidence.

## Authorized Local Validation

Use the exact reviewed temporary Go toolchain or a separately approved equivalent:

```bash
go version
go mod verify
go test ./...
go test -race ./...
go vet ./...
go build -trimpath -buildvcs=false ./...
```

Build output must remain in the Go cache or a temporary ignored location. Do not install a binary, create an image, run with privilege, or add a service.

The deterministic seed corpus runs during normal `go test`. Any active fuzzing must be time-bounded and must target only one named fuzz function at a time, for example:

```bash
go test ./engineering/privileged_proxy/protocol -run=^$ -fuzz=FuzzDecodeRequest -fuzztime=3s
```

## Synthetic-Key Rule

Tests generate Ed25519 keys deterministically in `_test.go` files and label them `TEST ONLY — NOT A CREDENTIAL`. No production private key, certificate, bearer token, trust deployment, or credential-like runtime configuration belongs in this repository.

## Ordinary-File Test Stores

Replay and audit file implementations accept only an explicit absolute test root and a safe basename. Tests use temporary directories. These implementations are evidence for deterministic state semantics only; they are not the approved production persistence mechanism.

## Stop Conditions

Stop and request Architecture Gatekeeper direction before adding:

- a Unix, TCP, or UDP listener or connection;
- real `SO_PEERCRED`, `/proc`, current-user, environment, host, or group discovery;
- a networking, HTTP, Docker, container-runtime, shell, SSH, plugin, cgo, unsafe, or deployment dependency;
- a Docker method, route, query, header, body, client, CLI, SDK, socket, or test server;
- credentials, certificates, trust deployment, a binary, image, OCI artifact, service, target, observation, consumer, recurrence, or activation.

## Related Documents

- [Source Implementation Package](../milestones/Milestone_14/Privileged_Proxy_Source_Implementation_Package.md)
- [Static Safety and Security-Test Report](../milestones/Milestone_14/Privileged_Proxy_Source_Static_Safety_and_Security_Test_Report.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded publication of the repository-only source guidance without adding runtime authority. |
| 1.0 | Added repository-only inspection and validation guidance without runtime authority. |
