# Constrained Docker API Proxy Repository Usage

**Version:** 1.0

**Status:** Repository Fixtures Only; No Socket, Network, Runtime, Deployment, or Privileged Access

## Scope

Platform EAP exposes a deterministic test surface for the constrained proxy contracts. Every input is read from `engineering/tests/fixtures/proxy_foundation/`; no live mode exists.

```bash
./platform-eap proxy contract
./platform-eap proxy validate
./platform-eap proxy policy
./platform-eap proxy fixtures
./platform-eap proxy request allowed_lifecycle
./platform-eap proxy response allowed_lifecycle
./platform-eap proxy decision allowed_lifecycle
./platform-eap proxy mock allowed_lifecycle
```

Artifact-specific validation is also bounded to the governed fixture directory:

```bash
./platform-eap proxy validate request engineering/tests/fixtures/proxy_foundation/proxy-request.json
./platform-eap proxy validate response engineering/tests/fixtures/proxy_foundation/proxy-request.json engineering/tests/fixtures/proxy_foundation/proxy-response.json
./platform-eap proxy validate policy engineering/tests/fixtures/proxy_foundation/proxy-policy.json
./platform-eap proxy validate configuration engineering/tests/fixtures/proxy_foundation/proxy-configuration.json
./platform-eap proxy validate capability engineering/tests/fixtures/proxy_foundation/proxy-capability.json
```

Non-allowed mock scenarios normally return a nonzero status and a machine-readable `ProxyFailure`; this is expected fail-closed evidence. Outputs are deterministic for the same fixture.

## Safety Boundary

The proxy modules have no socket, HTTP, Docker SDK, subprocess, shell, SSH, asynchronous networking, random, credential, or environment-derived execution path. The fixture reader rejects traversal, absolute escape, missing files, and symbolic links. The implementation has no endpoint URL model and no deployment artifact.

Fixture authorization is synthetic. A passing fixture does not approve a Registry subject, named-target observation, provider access, privileged deployment, service activation, or infrastructure mutation.

## Fixture Coverage

Positive fixtures cover lifecycle, health, restart information, and statistics. Negative fixtures cover denied/future categories, wildcards, expiration, duplicates, malformed and unknown input, size bounds, unsupported versions/methods, policy/configuration drift, missing authentication, digest mismatch, and rejected responses.

## Related Documents

- [Repository Architecture](Constrained_Docker_API_Proxy_Architecture.md)
- [Security Review](Privileged_Access_Security_Review_and_Constrained_Docker_API_Proxy_Architecture_Validation.md)
- [Implementation Package](../milestones/Milestone_14/Constrained_Docker_API_Proxy_Foundation_Implementation_Package.md)
