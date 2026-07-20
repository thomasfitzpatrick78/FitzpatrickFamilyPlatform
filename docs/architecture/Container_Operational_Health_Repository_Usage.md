# Container Operational Health Repository Usage

**Document Version:** 1.1

**Status:** Architecture Gatekeeper Accepted and Published; Fixture Only; Not Activated

**Milestone:** PLAT-14.1A

---

## Purpose

The Option B PLAT-14.1A capability validates synthetic Registry-linked container evidence, applies the repository-owned versioned policies derived from the published specification, reconciles declared fixture identity with canonical one-signal evidence, derives deterministic Operational Health Assessments, and renders authoritative JSON or deterministic Markdown.

It is repository-only. It does not inspect containers, connect to a provider, mutate Registry records, activate EO capabilities, write persistent operational evidence, or perform live work.

## Policy Set

The policy manifest is `platform/operations/container-health/policies/container-policy-set-v1.0.json`. It binds reconciliation, lifecycle freshness, health-check freshness, restart, resource-pressure, telemetry-availability, health, and assessment-confidence policy version `1.0`.

Policy evaluation is permitted only for explicit fixture inputs with `fixture_only: true` and `activation_status: not_activated`. This policy status is not service or EO activation.

## CLI

```text
./platform-eap container-health evidence validate <path>
./platform-eap container-health reconcile <input-path>
./platform-eap container-health assess <input-path>
./platform-eap container-health assessment validate <path>
./platform-eap container-health assessment render <path>
```

Commands are network-free, provider-free, side-effect-free, and read-only. JSON and Markdown are written only to standard output. Inputs must be regular repository files; traversal, repository escape, and symlink input fail closed.

Exit codes are `0` for a valid domain result, `2` for malformed or unsafe input, `3` for an unsupported contract/profile major version, and `4` for a missing, inactive, malformed, or incompatible policy set. A valid `unhealthy` or `insufficient_evidence` assessment is not a process failure.

## Fixture Boundary

Synthetic Registry declarations live under `engineering/tests/fixtures/container_health/registry/`. Provider-shaped fixtures live under `engineering/tests/fixtures/container_health/providers/`. The two supported test shapes normalize equivalent facts to equivalent canonical signals while retaining different provider provenance and runtime identifiers.

The Registry fixtures are schema `1.1` records and are validated through the same public Registry and Digital Twin validation interfaces as the authoritative set. An evaluation bundle must explicitly identify the governed synthetic Registry fixture root. Its declared subject and all evidence identity references must match the public Registry-derived projection. The environment is fixed to `test`; no fixture may reference `registry/records/` or an authoritative service.

Identity resolution is ordered and exact:

1. subject ID plus Registry reference;
2. host, Compose project, and Compose service;
3. host plus governed runtime name only when Registry uniqueness has already validated;
4. expected image identity as corroboration only;
5. runtime container ID as provenance only.

Case-folded, substring, suffix, partial, and fuzzy fallback matching are prohibited.

These are test translators, not production provider adapters. Fixture success does not prove Docker, Compose, Prometheus, OpenTelemetry, cAdvisor, Grafana, security, timing, cardinality, Pi-hole non-regression, or live readiness.

## Authoritative Results

Operational Evidence, Reconciliation, and Operational Health Assessment JSON are the three authoritative serialized records. The in-memory evaluation result groups those records with deterministic rendering metadata; it is not a fourth consumer-summary contract. Markdown is generated from the assessment and does not recalculate health.

Assessment confidence is the lowest confidence of mandatory supporting evidence. Advisory restart, resource, or provider-availability evidence does not lower an otherwise supported result. Stale advisory resource evidence remains visible with `RESOURCE_EVIDENCE_STALE`, while stale or unusable mandatory evidence cannot support Healthy. The version `1.0` reason catalog contains 20 active codes and the separately reserved `RESTART_THRESHOLD_EXCEEDED` code, which cannot be emitted.

## EO Contract Reuse

The end-to-end test uses the published EO-14.1A assignment, evidence, completion, validation, and participant contracts and the published EO-14.4A definition, run, validation, and advisory handoff contracts. It does not recreate execution or orchestration semantics and records no activation or live change.

## Related Documents

- [Container Operational Health Specification](../specifications/Container_Operational_Health_Specification.md)
- [Platform Operational Evidence and Health Contract Specification](../specifications/Platform_Operational_Evidence_and_Health_Contract_Specification.md)
- [PLAT-14.1A Implementation Package](../milestones/Milestone_14/PLAT_14_1A_Container_Operational_Health_Implementation_Package.md)

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Recorded publication of the Architecture Gatekeeper-accepted fixture-only repository capability without provider access, Registry migration, activation, or live work. |
| 1.0 | Documented the fixture-only policy, evidence, reconciliation, assessment, output, CLI, and EO-integration boundaries. |
