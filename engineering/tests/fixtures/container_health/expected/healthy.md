# Container Operational Health Assessment

- Assessment ID: `assessment-10c7ca6d115f932fa900`
- Contract version: `1.0`
- Subject ID: `svc-fixture-api`
- Registry reference: `engineering/tests/fixtures/container_health/registry/svc-fixture-api.yaml`
- Evidence profile: `container:1.0`
- Health status: `healthy`
- Assessment confidence: `high`
- Evaluated at: `2026-07-20T12:00:00Z`
- Valid until: `2026-07-20T12:00:50Z`
- Fixture only: `true`
- Activation status: `not_activated`

## Policy Trace

- Manifest: `container-policy-set:1.0`
- Health policy: `1.0`
- Assessment confidence policy: `1.0`

### Constituent Policies

- `container-assessment-confidence:1.0`
- `container-health:1.0`
- `container-healthcheck-freshness:1.0`
- `container-lifecycle-freshness:1.0`
- `container-reconciliation:1.0`
- `container-resource-pressure:1.0`
- `container-restart-window:1.0`
- `container-telemetry-availability:1.0`

## Evidence Trace

- Reconciliation ID: `reconciliation-bda7207e1d351686e28b`
- Reconciliation result: `matched`

### Mandatory Evidence

- `evidence-fixture-healthcheck` — `container.healthcheck.state`; freshness `current`; confidence `high`; observed `2026-07-20T11:59:50Z`; expires `2026-07-20T12:00:50Z`
- `evidence-fixture-lifecycle` — `container.lifecycle.observed_state`; freshness `current`; confidence `high`; observed `2026-07-20T11:59:50Z`; expires `2026-07-20T12:00:50Z`

### Advisory Evidence

- None

### Constraining Evidence

- None

### Provider Limitations

- None

## Reason Codes

- `ALL_MANDATORY_CRITERIA_PASSED`

## Critical Findings

- None

## Noncritical Findings

- None

Repository fixture evidence does not establish live provider compatibility, activation, or infrastructure authority.
