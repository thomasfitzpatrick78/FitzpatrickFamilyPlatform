# Production Provider Adapter Repository Usage

**Document Version:** 1.0

**Status:** Published Repository Usage; Fixture and Mock Only; Unactivated

---

## Purpose

The Production Provider Adapter Foundation supplies a deterministic repository test boundary for future provider implementations. Every command reads governed synthetic fixtures only. There is no live-provider mode.

## Commands

```text
./platform-eap provider contract
./platform-eap provider capabilities
./platform-eap provider fixtures
./platform-eap provider validate request <fixture-path>
./platform-eap provider validate capability <fixture-path>
./platform-eap provider validate response <request-fixture-path> <response-fixture-path>
./platform-eap provider validate failure <fixture-path>
./platform-eap provider validate result <fixture-path>
./platform-eap provider validate normalization <fixture-path>
./platform-eap provider normalize <request-fixture-path> <fixture-id>
./platform-eap provider mock <scenario> <request-fixture-path>
```

Paths must resolve to regular, non-symlink files beneath `engineering/tests/fixtures/provider_adapter`. Unknown commands and paths outside that boundary fail closed.

## Output Boundary

Commands render stable JSON to standard output and do not write provider results, modify Registry records, assess health, reconcile identity, call providers, inspect hosts, use credentials, activate services, or mutate infrastructure. Successful normalization emits published Operational Evidence records with observed identity, provider provenance, limitation, coverage, timing, availability, and provider-version context preserved.

## Mock Scenarios

The deterministic mock catalog covers healthy, unavailable, timeout, authorization denied, unsupported provider version, malformed payload, partial response, missing mandatory signals, conflicting identity, unknown target, duplicate targets, provider limitation, capability mismatch, and oversize payload behavior. Fixture success proves repository contract behavior only.

## Related Documents

- [Production Provider Adapter Foundation Implementation Package](../milestones/Milestone_14/Production_Provider_Adapter_Foundation_Implementation_Package.md)
- [Production Provider Adapter Contract Specification](../specifications/Production_Provider_Adapter_Contract_Specification.md)
- [Container Operational Health Repository Usage](Container_Operational_Health_Repository_Usage.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Documented repository-only provider commands, fixture boundary, outputs, mock scenarios, and unchanged live-provider prohibition. |
