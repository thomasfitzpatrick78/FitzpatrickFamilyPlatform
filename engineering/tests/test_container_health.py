import ast
import json
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from engineering.platform_eap import cli
from engineering.platform_eap.automation_capability import (
    AutomationLifecycleState,
    AutomationRunContext,
    AutomationStepType,
    FailurePolicy,
    GovernedAutomationDefinition,
    LiveImpact,
    OrchestrationStep,
    build_automation_handoff,
    validate_automation_run,
)
from engineering.platform_eap.container_health import (
    ACTIVATION_STATUS,
    Confidence,
    CollectionMethod,
    ContainerHealthDataError,
    ContainerParticipation,
    DomainFinding,
    FindingSeverity,
    FreshnessStatus,
    HEALTH_REASON_CODES,
    HealthCheckRequirement,
    HealthStatus,
    IdentityMatchMethod,
    PolicyDataError,
    ReconciliationOutcome,
    RESERVED_HEALTH_REASON_CODES,
    UnsupportedContractVersion,
    assess,
    assessment_presentation_findings,
    declared_subject_from_registry_contract,
    evaluate_bundle,
    load_policy_set,
    normalize_fixture_observation,
    reconcile,
    validate_assessment,
    validate_declared_subject,
    validate_evidence,
    validate_evidence_for_evaluation,
    validate_policy_set,
    validate_reconciliation,
)
from engineering.platform_eap.container_health_io import (
    assessment_from_dict,
    assessment_from_json,
    assessment_to_dict,
    assessment_to_json,
    bundle_from_dict,
    bundle_from_json,
    declared_subject_to_dict,
    evidence_from_dict,
    evidence_to_dict,
    evidence_to_json,
    reconciliation_from_json,
    reconciliation_to_json,
)
from engineering.platform_eap.container_health_rendering import render_assessment_markdown
from engineering.platform_eap.execution_capability import (
    MODEL_VERSION as EXECUTION_MODEL_VERSION,
    CompletionPackage,
    EvidenceRecord,
    EvidenceRequirement,
    EvidenceType,
    ExecutionContext,
    ExecutionResult,
    FindingSeverity as ExecutionFindingSeverity,
    GovernedAssignment,
    GovernedRole,
    OutcomeStatus,
    Participant,
    ValidationFinding,
    validate_assignment,
    validate_completion_package,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "engineering/tests/fixtures/container_health"
EVALUATED_AT = "2026-07-20T12:00:00Z"
HEAD = "c7269fde070a6a2cbce5b33fccb89e8e60950cc7"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def subject(subject_id: str = "svc-fixture-api"):
    records, paths, errors = cli.load_registry_records(FIXTURES / "registry")
    assert not errors
    reference = str(paths[subject_id].relative_to(ROOT))
    return declared_subject_from_registry_contract(
        records,
        paths,
        cli.load_registry_schema(),
        ROOT,
        subject_id,
        reference,
        "test",
    )


def policy_set():
    return load_policy_set(ROOT, subject().policy_reference)


def policy_with_rule(policy_id: str, key: str, value):
    policies = policy_set()
    original = policies.artifact(policy_id)
    rules = original.rules()
    rules[key] = value
    changed = replace(original, rules_json=json.dumps(rules, sort_keys=True))
    return replace(
        policies,
        artifacts=tuple(changed if item.policy_id == policy_id else item for item in policies.artifacts),
    )


def normalized(provider: str = "alpha-healthy.json"):
    return normalize_fixture_observation(load_json(FIXTURES / "providers" / provider), subject(), EVALUATED_AT, policy_set())


def healthy_evidence():
    result = normalized()
    assert not result.findings
    return result.evidence


def error_codes(findings):
    return {finding.code for finding in findings if finding.severity.value == "ERROR"}


def assessment_for(evidence=None, declared=None):
    declared = declared or subject()
    evidence = tuple(healthy_evidence() if evidence is None else evidence)
    policies = policy_set()
    record = reconcile(declared, evidence, EVALUATED_AT, policies)
    return assess(declared, evidence, record, EVALUATED_AT, policies)


def signal(name: str, evidence=None):
    items = healthy_evidence() if evidence is None else evidence
    return next(item for item in items if item.signal_name == name)


def test_domain_models_are_immutable_and_fixture_scoped():
    declared = subject()
    item = healthy_evidence()[0]
    with pytest.raises(FrozenInstanceError):
        declared.subject_id = "changed"
    with pytest.raises(FrozenInstanceError):
        item.value = "changed"
    assert declared.fixture_only is True
    assert declared.registry_reference.startswith("engineering/tests/fixtures/container_health/registry/")
    assert not error_codes(validate_declared_subject(declared))


def test_registry_fixture_set_uses_schema_1_1_public_validation_and_all_participation_paths():
    results = cli.validate_registry(FIXTURES / "registry", cli.REGISTRY_SCHEMA, ROOT)
    assert not [result for result in results if result.severity == "ERROR"]
    assert any("schema version 1.1 validated" in result.message for result in results)
    assert any("Platform Digital Twin integrity validation passed" in result.message for result in results)
    expected = {
        "svc-fixture-api": ContainerParticipation.ACTIVE,
        "svc-fixture-optional": ContainerParticipation.ACTIVE,
        "svc-fixture-inactive": ContainerParticipation.INTENTIONALLY_INACTIVE,
        "svc-fixture-excluded": ContainerParticipation.EXCLUDED,
        "svc-fixture-not-applicable": ContainerParticipation.NOT_APPLICABLE,
    }
    for subject_id, participation in expected.items():
        assert subject(subject_id).participation == participation


@pytest.mark.parametrize(
    "negative_name",
    ["svc-fixture-missing-identity.yaml", "svc-fixture-duplicate-runtime.yaml", "svc-fixture-duplicate-compose.yaml"],
)
def test_registry_fixture_projection_fails_closed_for_missing_duplicate_or_conflicting_identity(negative_name):
    records, paths, errors = cli.load_registry_records(FIXTURES / "registry")
    assert not errors
    negative_path = FIXTURES / "registry-invalid" / negative_name
    invalid = cli.parse_registry_yaml(negative_path)
    records[invalid["id"]] = invalid
    paths[invalid["id"]] = negative_path
    with pytest.raises(ContainerHealthDataError, match="Registry fixture identity contract is invalid"):
        declared_subject_from_registry_contract(
            records,
            paths,
            cli.load_registry_schema(),
            ROOT,
            str(invalid["id"]),
            str(negative_path.relative_to(ROOT)),
            "test",
        )


def test_inactive_excluded_and_not_applicable_registry_subjects_are_not_evaluated():
    for subject_id in ("svc-fixture-inactive", "svc-fixture-excluded", "svc-fixture-not-applicable"):
        result = assessment_for((), subject(subject_id))
        assert result.health_status == HealthStatus.NOT_EVALUATED
        assert result.reason_codes == ("SUBJECT_NOT_ACTIVE",)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("fixture_only", False, "subject.fixture_scope.required"),
        ("registry_reference", "registry/records/services/pihole-dns.yaml", "subject.registry_reference.fixture_required"),
        ("registry_reference", "../outside", "subject.reference.unsafe"),
        ("compose_service", None, "subject.compose_identity.required"),
    ],
)
def test_declared_subject_fails_closed_outside_synthetic_registry_boundary(field, value, code):
    assert code in error_codes(validate_declared_subject(replace(subject(), **{field: value})))


def test_policy_manifest_loads_exact_active_compatible_set():
    policies = policy_set()
    assert policies.manifest_id == "container-policy-set"
    assert len(policies.artifacts) == 8
    assert policies.versions() == tuple(sorted(policies.versions()))
    validate_policy_set(policies)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"status": "draft"}, "active policy manifest"),
        ({"compatible_contract_versions": ("2.0",)}, "incompatible"),
        ({"approval_authority": ("Platform Administrator",)}, "approval authority"),
    ],
)
def test_policy_manifest_missing_inactive_or_incompatible_fails_closed(change, message):
    with pytest.raises(PolicyDataError, match=message):
        validate_policy_set(replace(policy_set(), **change))


def test_policy_loader_rejects_missing_unsafe_and_unknown_manifest_fields(tmp_path):
    with pytest.raises(PolicyDataError, match="regular repository file"):
        load_policy_set(ROOT, "platform/operations/container-health/policies/missing.json")
    with pytest.raises(PolicyDataError, match="Unsafe policy reference"):
        load_policy_set(ROOT, "../outside.json")
    payload = load_json(ROOT / subject().policy_reference)
    payload["runtime_override"] = "healthy"
    manifest = ROOT / "engineering/tests/fixtures/container_health/invalid-policy-manifest.json"
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    try:
        with pytest.raises(PolicyDataError, match="unknown=.*runtime_override"):
            load_policy_set(ROOT, str(manifest.relative_to(ROOT)))
    finally:
        manifest.unlink()


def test_policy_rules_reject_unknown_semantics_and_outcome_changes():
    policies = policy_set()
    health = policies.artifact("container-health")
    rules = health.rules()
    rules["provider_override"] = "healthy"
    changed = replace(health, rules_json=json.dumps(rules, sort_keys=True))
    artifacts = tuple(changed if item.policy_id == health.policy_id else item for item in policies.artifacts)
    with pytest.raises(PolicyDataError, match="unknown"):
        validate_policy_set(replace(policies, artifacts=artifacts))
    reconciliation_policy = policies.artifact("container-reconciliation")
    rules = reconciliation_policy.rules()
    rules["fuzzy_matching_allowed"] = True
    changed = replace(reconciliation_policy, rules_json=json.dumps(rules, sort_keys=True))
    artifacts = tuple(changed if item.policy_id == reconciliation_policy.policy_id else item for item in policies.artifacts)
    with pytest.raises(PolicyDataError, match="fuzzy-match"):
        validate_policy_set(replace(policies, artifacts=artifacts))


@pytest.mark.parametrize(
    ("policy_id", "key", "value", "message"),
    [
        ("container-lifecycle-freshness", "aging_after_seconds", -1, "Freshness policy"),
        ("container-lifecycle-freshness", "maximum_age_seconds", 30, "Freshness policy"),
        ("container-restart-window", "health_thresholds", [3], "without thresholds"),
        ("container-restart-window", "reserved_reason_code", "RESTART_THRESHOLD_ACTIVE", "without thresholds"),
        ("container-resource-pressure", "numeric_health_thresholds", [0.9], "Resource-pressure"),
        ("container-telemetry-availability", "provider_loss_proves_unhealthy", True, "Telemetry-availability"),
        ("container-health", "healthy_default", True, "health policy"),
        ("container-assessment-confidence", "arithmetic_scoring", True, "Assessment-confidence"),
    ],
)
def test_policy_validation_rejects_invalid_duration_threshold_reserved_and_contradictory_rules(policy_id, key, value, message):
    with pytest.raises(PolicyDataError, match=message):
        validate_policy_set(policy_with_rule(policy_id, key, value))


def test_policy_manifest_loading_order_is_exact_and_deterministic():
    assert tuple(item.policy_id for item in policy_set().artifacts) == (
        "container-reconciliation",
        "container-lifecycle-freshness",
        "container-healthcheck-freshness",
        "container-restart-window",
        "container-resource-pressure",
        "container-telemetry-availability",
        "container-health",
        "container-assessment-confidence",
    )


def test_strict_parsers_reject_unknown_fields_and_unsupported_versions():
    evidence_payload = evidence_to_dict(healthy_evidence()[0])
    evidence_payload["provider_health"] = "healthy"
    with pytest.raises(ContainerHealthDataError, match="unknown or unsafe fields: provider_health"):
        evidence_from_dict(evidence_payload)
    future = evidence_to_dict(healthy_evidence()[0])
    future["contract_version"] = "2.0"
    with pytest.raises(UnsupportedContractVersion):
        evidence_from_dict(future)
    bundle = load_json(FIXTURES / "bundles/healthy.json")
    bundle["execute"] = "docker inspect"
    with pytest.raises(ContainerHealthDataError, match="unknown or unsafe fields: execute"):
        bundle_from_dict(bundle)
    duplicate = (FIXTURES / "bundles/healthy.json").read_text(encoding="utf-8").replace(
        '"bundle_version": "plat-14.1a-fixture-v1",',
        '"bundle_version": "plat-14.1a-fixture-v1",\n  "bundle_version": "plat-14.1a-fixture-v1",',
        1,
    )
    with pytest.raises(ContainerHealthDataError, match="Duplicate JSON field"):
        bundle_from_json(duplicate)


def test_policy_loader_rejects_duplicate_json_fields():
    source = ROOT / subject().policy_reference
    duplicate = source.read_text(encoding="utf-8").replace(
        '"manifest_id": "container-policy-set",',
        '"manifest_id": "container-policy-set",\n  "manifest_id": "container-policy-set",',
        1,
    )
    manifest = FIXTURES / "duplicate-policy-manifest.json"
    manifest.write_text(duplicate, encoding="utf-8")
    try:
        with pytest.raises(PolicyDataError, match="Duplicate JSON field"):
            load_policy_set(ROOT, str(manifest.relative_to(ROOT)))
    finally:
        manifest.unlink()


def test_strict_evidence_parser_rejects_missing_timestamp_invalid_enum_and_unsupported_profile():
    payload = evidence_to_dict(healthy_evidence()[0])
    payload.pop("observed_at")
    with pytest.raises(ContainerHealthDataError, match="missing required fields: observed_at"):
        evidence_from_dict(payload)
    payload = evidence_to_dict(healthy_evidence()[0])
    payload["freshness_status"] = "expired"
    with pytest.raises(ContainerHealthDataError, match="unsupported value"):
        evidence_from_dict(payload)
    payload = evidence_to_dict(healthy_evidence()[0])
    payload["profile_version"] = "2.0"
    with pytest.raises(UnsupportedContractVersion):
        evidence_from_dict(payload)
    payload = evidence_to_dict(healthy_evidence()[0])
    payload["completeness_status"] = "complete_enough"
    with pytest.raises(ContainerHealthDataError, match="unsupported value"):
        evidence_from_dict(payload)
    payload = evidence_to_dict(healthy_evidence()[0])
    payload["evidence_confidence"] = "certain"
    with pytest.raises(ContainerHealthDataError, match="unsupported value"):
        evidence_from_dict(payload)
    malformed = replace(healthy_evidence()[0], observed_at="2026-07-20T11:59:50")
    assert "evidence.observed_at.invalid" in error_codes(validate_evidence(malformed))


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("freshness_status", FreshnessStatus.AGING, "evidence.freshness.contradictory"),
        ("maximum_age_seconds", 600, "evidence.freshness.contradictory"),
        ("evaluated_age_seconds", 0, "evidence.freshness.contradictory"),
        ("evidence_confidence", Confidence.LOW, "evidence.confidence.contradictory"),
    ],
)
def test_evidence_cannot_forge_policy_derived_freshness_or_confidence(field, value, code):
    forged = replace(healthy_evidence()[0], **{field: value})
    assert code in error_codes(validate_evidence_for_evaluation(forged, EVALUATED_AT, policy_set()))


def test_valid_canonical_evidence_is_one_signal_registry_linked_and_provider_independent():
    for item in healthy_evidence():
        assert not error_codes(validate_evidence(item))
        assert item.subject_id == subject().subject_id
        assert item.runtime_container_id != item.subject_id
        assert item.signal_name.startswith("container.")
        assert item.provider_id not in item.signal_name


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("signal_name", "docker.container.up", "evidence.signal.unsupported"),
        ("evidence_type", "restart_observation", "evidence.evidence_type.invalid"),
        ("unit", "percent", "evidence.unit.invalid"),
        ("value", "unknown-state", "evidence.value.invalid"),
        ("registry_reference", "/absolute/path", "evidence.reference.unsafe"),
        ("maximum_age_seconds", -1, "evidence.age.invalid"),
    ],
)
def test_evidence_validation_rejects_malformed_or_unsafe_values(field, value, code):
    item = replace(signal("container.lifecycle.observed_state"), **{field: value})
    assert code in error_codes(validate_evidence(item))


def test_windowed_resource_signal_requires_window_and_finite_canonical_value():
    lifecycle = signal("container.lifecycle.observed_state")
    pressure = replace(
        lifecycle,
        evidence_id="evidence-pressure",
        evidence_type="resource_pressure",
        signal_name="container.memory.pressure",
        value="critical",
        observation_window_start=None,
        observation_window_end=None,
    )
    assert "evidence.window.required" in error_codes(validate_evidence(pressure))
    utilization = replace(
        pressure,
        signal_name="container.memory.utilization",
        value_type="decimal",
        value=float("inf"),
        unit="ratio",
        observation_window_start="2026-07-20T11:59:40Z",
        observation_window_end="2026-07-20T11:59:50Z",
    )
    assert "evidence.decimal.invalid" in error_codes(validate_evidence(utilization))


@pytest.mark.parametrize(
    ("seconds_ago", "expected"),
    [(10, FreshnessStatus.CURRENT), (45, FreshnessStatus.AGING), (61, FreshnessStatus.STALE)],
)
def test_fixture_normalization_derives_current_aging_and_stale_freshness(seconds_ago, expected):
    payload = load_json(FIXTURES / "providers/alpha-healthy.json")
    payload["observed_at"] = f"2026-07-20T11:58:{60-seconds_ago:02d}Z" if seconds_ago <= 60 else "2026-07-20T11:58:59Z"
    if seconds_ago == 45:
        payload["observed_at"] = "2026-07-20T11:59:15Z"
    if seconds_ago == 10:
        payload["observed_at"] = "2026-07-20T11:59:50Z"
    result = normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set())
    assert {item.freshness_status for item in result.evidence} == {expected}
    if expected == FreshnessStatus.STALE:
        assert {item.evidence_confidence for item in result.evidence} == {Confidence.NONE}


def test_future_fixture_timestamp_fails_closed():
    payload = load_json(FIXTURES / "providers/alpha-healthy.json")
    payload["observed_at"] = "2026-07-20T12:00:01Z"
    with pytest.raises(ContainerHealthDataError, match="Future-dated"):
        normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set())


@pytest.mark.parametrize(
    ("observed_at", "expected", "age"),
    [
        ("2026-07-20T11:59:30Z", FreshnessStatus.CURRENT, 30),
        ("2026-07-20T11:59:29Z", FreshnessStatus.AGING, 31),
        ("2026-07-20T11:59:00Z", FreshnessStatus.AGING, 60),
        ("2026-07-20T11:58:59Z", FreshnessStatus.STALE, 61),
    ],
)
def test_freshness_policy_boundary_timestamps_are_exact(observed_at, expected, age):
    payload = load_json(FIXTURES / "providers/alpha-healthy.json")
    payload["observed_at"] = observed_at
    result = normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set())
    assert {item.freshness_status for item in result.evidence} == {expected}
    assert {item.evaluated_age_seconds for item in result.evidence} == {age}


def test_confidence_is_categorical_and_derived_without_scores_or_averaging():
    direct = normalized().evidence
    assert {item.evidence_confidence for item in direct} == {Confidence.HIGH}
    payload = load_json(FIXTURES / "providers/alpha-healthy.json")
    payload["collection_method"] = "scraped"
    indirect = normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set()).evidence
    assert {item.evidence_confidence for item in indirect} == {Confidence.MEDIUM}
    payload["collection_method"] = "inferred"
    inferred = normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set()).evidence
    assert {item.evidence_confidence for item in inferred} == {Confidence.LOW}
    payload["observed_at"] = "2026-07-20T11:58:00Z"
    stale = normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set()).evidence
    assert {item.evidence_confidence for item in stale} == {Confidence.NONE}


def test_assessment_confidence_is_bounded_by_mandatory_evidence_and_not_advisory_evidence():
    runtime_only = load_json(FIXTURES / "providers/alpha-healthy.json")
    runtime_only.pop("subject_id")
    runtime_only.pop("registry_reference")
    runtime_only["compose_project"] = None
    runtime_only["compose_service"] = None
    fallback = normalize_fixture_observation(runtime_only, subject(), EVALUATED_AT, policy_set()).evidence
    fallback_assessment = assessment_for(fallback)
    assert fallback_assessment.health_status == HealthStatus.HEALTHY
    assert fallback_assessment.assessment_confidence == Confidence.MEDIUM

    direct = healthy_evidence()
    lifecycle = signal("container.lifecycle.observed_state", direct)
    low_advisory = replace(
        lifecycle,
        evidence_id="evidence-low-advisory-restart",
        evidence_type="restart",
        signal_name="container.restart.count",
        value=1,
        value_type="integer",
        unit="count",
        collection_method=CollectionMethod.INFERRED,
        evidence_confidence=Confidence.LOW,
        confidence_reason_codes=("AGING_OR_INFERRED",),
    )
    result = assessment_for((*direct, low_advisory))
    assert result.health_status == HealthStatus.HEALTHY
    assert result.assessment_confidence == Confidence.HIGH
    assert next(item for item in result.evidence_summary if item.evidence_id == low_advisory.evidence_id).role == "advisory"


def test_all_completeness_classifications_remain_explicit_and_complete_does_not_imply_confidence():
    item = signal("container.lifecycle.observed_state")
    for value in ("complete", "partial", "missing_required_attributes", "not_assessable"):
        payload = evidence_to_dict(item)
        payload["completeness_status"] = value
        if value == "complete":
            payload["missing_attributes"] = []
        parsed = evidence_from_dict(payload)
        assert parsed.completeness_status.value == value
    medium_complete = replace(item, evidence_confidence=Confidence.MEDIUM)
    assert not error_codes(validate_evidence(medium_complete))


def test_two_provider_shapes_normalize_to_equivalent_canonical_signals_and_health():
    alpha = normalized("alpha-healthy.json")
    beta = normalized("beta-healthy.json")
    alpha_values = {(item.signal_name, item.value, item.unit, item.subject_id) for item in alpha.evidence}
    beta_values = {(item.signal_name, item.value, item.unit, item.subject_id) for item in beta.evidence}
    assert alpha_values == beta_values
    assert {item.provider_id for item in alpha.evidence} != {item.provider_id for item in beta.evidence}
    assert {item.runtime_container_id for item in alpha.evidence} != {item.runtime_container_id for item in beta.evidence}
    assert assessment_for(alpha.evidence).health_status == assessment_for(beta.evidence).health_status == HealthStatus.HEALTHY


def test_identity_precedence_exact_tuple_and_unique_runtime_name_are_explicit():
    alpha = normalized("alpha-healthy.json").evidence
    beta = normalized("beta-healthy.json").evidence
    assert {item.identity_match_method for item in alpha} == {IdentityMatchMethod.SUBJECT_AND_REGISTRY_REFERENCE}
    assert {item.identity_match_method for item in beta} == {IdentityMatchMethod.HOST_COMPOSE_PROJECT_SERVICE}

    runtime_only = load_json(FIXTURES / "providers/alpha-healthy.json")
    runtime_only.pop("subject_id")
    runtime_only.pop("registry_reference")
    runtime_only["compose_project"] = None
    runtime_only["compose_service"] = None
    result = normalize_fixture_observation(runtime_only, subject(), EVALUATED_AT, policy_set())
    assert result.evidence
    assert {item.identity_match_method for item in result.evidence} == {IdentityMatchMethod.HOST_UNIQUE_RUNTIME_NAME}
    assert {item.evidence_confidence for item in result.evidence} == {Confidence.MEDIUM}


def test_explicit_identity_conflict_image_only_and_runtime_id_only_cannot_be_repaired_by_fallbacks():
    explicit_conflict = load_json(FIXTURES / "providers/alpha-healthy.json")
    explicit_conflict["subject_id"] = "svc-other"
    assert not normalize_fixture_observation(explicit_conflict, subject(), EVALUATED_AT, policy_set()).evidence

    image_only = load_json(FIXTURES / "providers/alpha-healthy.json")
    image_only.pop("subject_id")
    image_only.pop("registry_reference")
    image_only["compose_project"] = None
    image_only["compose_service"] = None
    image_only["runtime_name"] = "unmatched-runtime"
    assert image_only["image_reference"] == subject().expected_image_reference
    assert not normalize_fixture_observation(image_only, subject(), EVALUATED_AT, policy_set()).evidence

    runtime_id_only = dict(image_only)
    runtime_id_only.pop("image_reference")
    runtime_id_only["runtime_container_id"] = "alpha-runtime-001"
    assert not normalize_fixture_observation(runtime_id_only, subject(), EVALUATED_AT, policy_set()).evidence


def test_similar_name_and_renamed_compose_service_do_not_fuzzy_match():
    payload = load_json(FIXTURES / "providers/alpha-healthy.json")
    payload.pop("subject_id")
    payload.pop("registry_reference")
    payload["compose_service"] = "fixture-api-renamed"
    payload["runtime_name"] = "fixture-api-similar"
    result = normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set())
    assert not result.evidence
    assert {finding.code for finding in result.findings} == {"subject_mapping_failed"}


def test_known_cadvisor_identity_limitation_cannot_produce_qualifying_evidence():
    result = normalized("alpha-cadvisor-limited.json")
    assert not result.evidence
    assert {finding.code for finding in result.findings} == {"provider_limitation_applies"}


def test_fixture_adapter_rejects_secret_like_unknown_unsafe_and_unsupported_input():
    payload = load_json(FIXTURES / "providers/alpha-healthy.json")
    payload["runtime_name"] = "password=do-not-store"
    with pytest.raises(ContainerHealthDataError, match="secret-like"):
        normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set())
    payload = load_json(FIXTURES / "providers/alpha-healthy.json")
    payload["source_reference"] = "../outside"
    with pytest.raises(ContainerHealthDataError, match="unsafe"):
        normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set())
    payload = load_json(FIXTURES / "providers/alpha-healthy.json")
    payload["provider_shape"] = "future-v2"
    with pytest.raises(UnsupportedContractVersion):
        normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set())


def test_reconciliation_matched_and_preserves_considered_selected_evidence():
    evidence = healthy_evidence()
    record = reconcile(subject(), evidence, EVALUATED_AT, policy_set())
    assert record.result == ReconciliationOutcome.MATCHED
    assert record.evidence_ids == tuple(sorted(item.evidence_id for item in evidence))
    assert record.selected_evidence_ids == record.evidence_ids
    assert not record.rejected_evidence
    assert record.match_method == IdentityMatchMethod.SUBJECT_AND_REGISTRY_REFERENCE
    assert not error_codes(validate_reconciliation(record))
    assert reconciliation_from_json(reconciliation_to_json(record)) == record


def test_reconciliation_contract_rejects_contradictory_match_and_evidence_selection():
    record = reconcile(subject(), healthy_evidence(), EVALUATED_AT, policy_set())
    unmatched = replace(record, result=ReconciliationOutcome.MISSING)
    assert "reconciliation.match_method.contradictory" in error_codes(validate_reconciliation(unmatched))
    unknown = replace(record, selected_evidence_ids=("evidence-never-considered",))
    assert "reconciliation.selected.invalid" in error_codes(validate_reconciliation(unknown))


def test_reconciliation_missing_unexpected_ambiguous_conflicting_stale_and_not_applicable():
    policies = policy_set()
    assert reconcile(subject(), (), EVALUATED_AT, policies).result == ReconciliationOutcome.MISSING
    lifecycle = signal("container.lifecycle.observed_state")
    unexpected = replace(lifecycle, subject_id="svc-unexpected", evidence_id="evidence-unexpected")
    assert reconcile(subject(), (unexpected,), EVALUATED_AT, policies).result == ReconciliationOutcome.UNEXPECTED
    ambiguous = replace(lifecycle, evidence_id="evidence-ambiguous", finding_codes=("ambiguous_identity",), evidence_confidence=Confidence.NONE)
    assert reconcile(subject(), (ambiguous,), EVALUATED_AT, policies).result == ReconciliationOutcome.AMBIGUOUS
    conflicting = replace(lifecycle, evidence_id="evidence-conflicting", value="exited")
    assert reconcile(subject(), (lifecycle, conflicting), EVALUATED_AT, policies).result == ReconciliationOutcome.CONFLICTING
    stale = replace(
        lifecycle,
        observed_at="2026-07-20T11:58:59Z",
        freshness_status=FreshnessStatus.STALE,
        evidence_confidence=Confidence.NONE,
        evaluated_age_seconds=61,
    )
    assert reconcile(subject(), (stale,), EVALUATED_AT, policies).result == ReconciliationOutcome.STALE
    inactive = replace(subject(), participation=ContainerParticipation.INTENTIONALLY_INACTIVE)
    assert reconcile(inactive, (), EVALUATED_AT, policies).result == ReconciliationOutcome.NOT_APPLICABLE


def test_health_statuses_are_deterministic_and_healthy_is_positive_proof_only():
    assert assessment_for().health_status == HealthStatus.HEALTHY
    assert assessment_for(()).health_status == HealthStatus.INSUFFICIENT_EVIDENCE
    inactive = replace(subject(), participation=ContainerParticipation.EXCLUDED)
    assert assessment_for((), inactive).health_status == HealthStatus.NOT_EVALUATED
    exited = replace(signal("container.lifecycle.observed_state"), value="exited")
    assert assessment_for((exited,)).health_status == HealthStatus.UNHEALTHY
    assert "UNEXPECTED_EXIT" in assessment_for((exited,)).reason_codes


def test_required_healthcheck_failure_absence_and_not_configured_fail_closed():
    lifecycle = signal("container.lifecycle.observed_state")
    passing = signal("container.healthcheck.state")
    missing = assessment_for((lifecycle,))
    assert missing.health_status == HealthStatus.INSUFFICIENT_EVIDENCE
    assert missing.reason_codes == ("TELEMETRY_UNAVAILABLE",)
    failing = replace(passing, value="failing")
    assert assessment_for((lifecycle, failing)).health_status == HealthStatus.UNHEALTHY
    not_configured = replace(passing, value="not_configured")
    result = assessment_for((lifecycle, not_configured))
    assert result.health_status == HealthStatus.INSUFFICIENT_EVIDENCE
    assert "REQUIRED_HEALTHCHECK_NOT_CONFIGURED" in result.reason_codes


@pytest.mark.parametrize("state", ["starting", "unavailable"])
def test_required_healthcheck_nonpassing_transitional_states_are_insufficient(state):
    lifecycle = signal("container.lifecycle.observed_state")
    healthcheck = replace(signal("container.healthcheck.state"), value=state)
    assert assessment_for((lifecycle, healthcheck)).health_status == HealthStatus.INSUFFICIENT_EVIDENCE


@pytest.mark.parametrize("state", ["created", "stopped", "restarting"])
def test_active_nonrunning_lifecycle_states_do_not_default_healthy(state):
    lifecycle = replace(signal("container.lifecycle.observed_state"), value=state)
    assert assessment_for((lifecycle,)).health_status == HealthStatus.INSUFFICIENT_EVIDENCE


def test_optional_healthcheck_not_configured_is_neutral():
    declared = replace(subject(), health_check_requirement=HealthCheckRequirement.OPTIONAL)
    lifecycle = signal("container.lifecycle.observed_state")
    result = assessment_for((lifecycle,), declared)
    assert result.health_status == HealthStatus.HEALTHY
    assert "HEALTHCHECK_NOT_REQUIRED" in result.reason_codes


def test_critical_memory_pressure_degrades_and_restart_evidence_remains_advisory():
    evidence = list(healthy_evidence())
    lifecycle = signal("container.lifecycle.observed_state", evidence)
    pressure = replace(
        lifecycle, evidence_id="evidence-pressure", evidence_type="resource_pressure", signal_name="container.memory.pressure",
        value="critical", observation_window_start="2026-07-20T11:59:40Z", observation_window_end="2026-07-20T11:59:50Z",
        freshness_policy_id="container-lifecycle-freshness:1.0",
    )
    result = assessment_for((*evidence, pressure))
    assert result.health_status == HealthStatus.DEGRADED
    assert result.reason_codes == ("MEMORY_PRESSURE_CRITICAL",)
    restart = replace(lifecycle, evidence_id="evidence-restart", evidence_type="restart", signal_name="container.restart.count", value=999, value_type="integer", unit="count")
    restart_result = assessment_for((*evidence, restart))
    assert restart_result.health_status == HealthStatus.HEALTHY
    assert "RESTART_THRESHOLD_EXCEEDED" not in restart_result.reason_codes


def test_provider_limitation_and_partial_mandatory_coverage_are_insufficient_not_unhealthy():
    evidence = list(healthy_evidence())
    lifecycle = signal("container.lifecycle.observed_state", evidence)
    limitation = replace(
        lifecycle, evidence_id="evidence-limitation", evidence_type="telemetry_availability",
        signal_name="container.telemetry.provider_limitation", value="applies",
    )
    limited = assessment_for((*evidence, limitation))
    assert limited.health_status == HealthStatus.INSUFFICIENT_EVIDENCE
    assert "PROVIDER_LIMITATION_APPLIES" in limited.reason_codes
    coverage = replace(
        lifecycle, evidence_id="evidence-coverage", evidence_type="telemetry_availability",
        signal_name="container.telemetry.collection_coverage", value="partial",
    )
    partial = assessment_for((*evidence, coverage))
    assert partial.health_status == HealthStatus.INSUFFICIENT_EVIDENCE
    assert "MANDATORY_TELEMETRY_PARTIAL" in partial.reason_codes


def test_provider_unavailability_is_observation_quality_not_service_failure():
    evidence = list(healthy_evidence())
    lifecycle = signal("container.lifecycle.observed_state", evidence)
    unavailable = replace(
        lifecycle, evidence_id="evidence-provider-unavailable", evidence_type="telemetry_availability",
        signal_name="container.telemetry.provider_availability", value="unavailable",
    )
    result = assessment_for((*evidence, unavailable))
    assert result.health_status == HealthStatus.HEALTHY
    assert "UNEXPECTED_EXIT" not in result.reason_codes
    assert "ADVISORY_TELEMETRY_PARTIAL" in result.reason_codes
    assert result.assessment_confidence == Confidence.HIGH


def test_expected_mandatory_signal_unavailable_is_insufficient_evidence():
    evidence = list(healthy_evidence())
    lifecycle = signal("container.lifecycle.observed_state", evidence)
    unavailable = replace(
        lifecycle,
        evidence_id="evidence-expected-signal-unavailable",
        evidence_type="telemetry_availability",
        signal_name="container.telemetry.expected_signal_availability",
        value="missing",
    )
    result = assessment_for((*evidence, unavailable))
    assert result.health_status == HealthStatus.INSUFFICIENT_EVIDENCE
    assert result.reason_codes == ("TELEMETRY_UNAVAILABLE",)
    assert result.assessment_confidence == Confidence.NONE


def test_stale_resource_evidence_is_retained_as_advisory_without_changing_health():
    evidence = list(healthy_evidence())
    lifecycle = signal("container.lifecycle.observed_state", evidence)
    stale_resource = replace(
        lifecycle,
        evidence_id="evidence-stale-memory-utilization",
        evidence_type="resource_pressure",
        signal_name="container.memory.utilization",
        value=0.5,
        value_type="decimal",
        unit="ratio",
        observed_at="2026-07-20T11:58:59Z",
        observation_window_start="2026-07-20T11:58:49Z",
        observation_window_end="2026-07-20T11:58:59Z",
        freshness_status=FreshnessStatus.STALE,
        evaluated_age_seconds=61,
        evidence_confidence=Confidence.NONE,
        confidence_reason_codes=("CURRENT_USE_UNQUALIFIED",),
    )
    result = assessment_for((*evidence, stale_resource))
    assert result.health_status == HealthStatus.HEALTHY
    assert "RESOURCE_EVIDENCE_STALE" in result.reason_codes
    summary = next(item for item in result.evidence_summary if item.evidence_id == stale_resource.evidence_id)
    assert summary.role == "advisory"
    assert summary.freshness_status == FreshnessStatus.STALE


def test_conclusive_absence_can_prove_unhealthy_but_missing_observation_cannot():
    lifecycle = replace(
        signal("container.lifecycle.observed_state"), value="missing", finding_codes=("conclusive_absence",)
    )
    result = assessment_for((lifecycle,))
    assert result.health_status == HealthStatus.UNHEALTHY
    assert result.reason_codes == ("DECLARED_SUBJECT_ABSENT",)
    assert assessment_for(()).health_status == HealthStatus.INSUFFICIENT_EVIDENCE


def test_assessment_validity_is_bounded_by_earliest_mandatory_evidence_expiry():
    result = assessment_for()
    assert result.valid_until == "2026-07-20T12:00:50Z"
    assert "ASSESSMENT_EXPIRED" not in {finding.code for finding in assessment_presentation_findings(result, "2026-07-20T12:00:50Z")}
    expired_codes = {finding.code for finding in assessment_presentation_findings(result, "2026-07-20T12:00:51Z")}
    assert "ASSESSMENT_EXPIRED" in expired_codes


def test_json_and_markdown_are_byte_stable_and_renderer_does_not_recalculate_health():
    first = assessment_for()
    second = assessment_for()
    assert assessment_to_json(first) == assessment_to_json(second)
    assert render_assessment_markdown(first) == render_assessment_markdown(second)
    rendered = render_assessment_markdown(first)
    assert "Health status: `healthy`" in rendered
    assert "Activation status: `not_activated`" in rendered
    assert "does not establish live provider compatibility" in rendered
    assert assessment_from_json(assessment_to_json(first)) == first


def test_published_reason_catalog_and_golden_outputs_are_complete_and_stable():
    assert len(HEALTH_REASON_CODES) == 20
    assert RESERVED_HEALTH_REASON_CODES == {"RESTART_THRESHOLD_EXCEEDED"}
    assert len(HEALTH_REASON_CODES | RESERVED_HEALTH_REASON_CODES) == 21
    assert HEALTH_REASON_CODES.isdisjoint(RESERVED_HEALTH_REASON_CODES)
    assert "RESTART_THRESHOLD_EXCEEDED" not in assessment_for((*healthy_evidence(), replace(
        signal("container.lifecycle.observed_state"),
        evidence_id="evidence-restart-golden",
        evidence_type="restart",
        signal_name="container.restart.count",
        value=999,
        value_type="integer",
        unit="count",
    ))).reason_codes

    static_assessment = assessment_from_json((FIXTURES / "assessments/healthy.json").read_text(encoding="utf-8"))
    bundle = bundle_from_json((FIXTURES / "bundles/healthy.json").read_text(encoding="utf-8"))
    evaluated = evaluate_bundle(bundle, load_policy_set(ROOT, bundle.declared_subject.policy_reference))
    assert static_assessment == evaluated.assessment
    assert not error_codes(validate_assessment(static_assessment))
    assert assessment_to_json(static_assessment) == (FIXTURES / "assessments/healthy.json").read_text(encoding="utf-8")
    assert assessment_from_json(assessment_to_json(static_assessment)) == static_assessment
    assert render_assessment_markdown(static_assessment) == (FIXTURES / "expected/healthy.md").read_text(encoding="utf-8")
    reconciliation = reconciliation_from_json((FIXTURES / "reconciliations/healthy.json").read_text(encoding="utf-8"))
    assert reconciliation == evaluated.reconciliation
    assert not error_codes(validate_reconciliation(reconciliation))
    assert reconciliation_to_json(reconciliation) == (FIXTURES / "reconciliations/healthy.json").read_text(encoding="utf-8")
    assert reconciliation_from_json(reconciliation_to_json(reconciliation)) == reconciliation


def test_assessment_parser_and_validator_reject_unknown_health_and_unsafe_state():
    payload = assessment_to_dict(assessment_for())
    payload["provider_score"] = 99
    with pytest.raises(ContainerHealthDataError, match="unknown or unsafe fields: provider_score"):
        assessment_from_dict(payload)
    payload = assessment_to_dict(assessment_for())
    payload["contract_version"] = "2.0"
    with pytest.raises(UnsupportedContractVersion):
        assessment_from_dict(payload)
    unsafe = replace(assessment_for(), activation_status="activated")
    assert "assessment.activation.invalid" in error_codes(validate_assessment(unsafe))
    incomplete_trace = replace(assessment_for(), policy_versions=())
    assert "assessment.policy_trace.invalid" in error_codes(validate_assessment(incomplete_trace))


def test_fixture_normalization_rejects_unsupported_collection_method():
    payload = load_json(FIXTURES / "providers/alpha-healthy.json")
    payload["collection_method"] = "remote_execution"
    with pytest.raises(ContainerHealthDataError, match="collection_method is unsupported"):
        normalize_fixture_observation(payload, subject(), EVALUATED_AT, policy_set())


def test_cli_reconcile_assess_validate_and_render_are_read_only_and_deterministic(capsys):
    bundle = "engineering/tests/fixtures/container_health/bundles/healthy.json"
    assessment_path = "engineering/tests/fixtures/container_health/assessments/healthy.json"
    assert cli.main(["container-health", "reconcile", bundle]) == 0
    reconciliation_output = capsys.readouterr().out
    assert json.loads(reconciliation_output)["result"] == "matched"
    assert cli.main(["container-health", "assess", bundle]) == 0
    first = capsys.readouterr().out
    assert cli.main(["container-health", "assess", bundle]) == 0
    second = capsys.readouterr().out
    assert first == second
    assert json.loads(first)["health_status"] == "healthy"
    assert cli.main(["container-health", "assessment", "validate", assessment_path]) == 0
    assert "Status: PASS" in capsys.readouterr().out
    assert cli.main(["container-health", "assessment", "render", assessment_path]) == 0
    assert "# Container Operational Health Assessment" in capsys.readouterr().out


def test_cli_exit_codes_distinguish_malformed_version_and_policy_failures(capsys, monkeypatch):
    assert cli.main(["container-health", "assess", "/etc/passwd"]) == 2
    assert "inside the repository" in capsys.readouterr().out
    bundle = load_json(FIXTURES / "bundles/healthy.json")
    bundle["bundle_version"] = "future-v2"
    path = ROOT / "engineering/tests/fixtures/container_health/bundles/future.json"
    path.write_text(json.dumps(bundle), encoding="utf-8")
    try:
        assert cli.main(["container-health", "assess", str(path.relative_to(ROOT))]) == 3
    finally:
        path.unlink()
    assert "unsupported" in capsys.readouterr().out.lower()
    def reject_policy(*_):
        raise PolicyDataError("Assessments may use only an active policy manifest.")

    monkeypatch.setattr(cli, "load_policy_set", reject_policy)
    assert cli.main(["container-health", "assess", "engineering/tests/fixtures/container_health/bundles/healthy.json"]) == 4
    assert "active policy manifest" in capsys.readouterr().out


def test_cli_valid_unhealthy_and_not_evaluated_are_successful_domain_results(capsys):
    healthy = load_json(FIXTURES / "bundles/healthy.json")
    unhealthy = json.loads(json.dumps(healthy))
    lifecycle = next(item for item in unhealthy["evidence"] if item["signal_name"] == "container.lifecycle.observed_state")
    lifecycle["value"] = "exited"
    inactive = json.loads(json.dumps(healthy))
    inactive["declared_subject"] = declared_subject_to_dict(subject("svc-fixture-inactive"))
    inactive["evidence"] = []
    cases = (("unhealthy-cli.json", unhealthy, "unhealthy"), ("not-evaluated-cli.json", inactive, "not_evaluated"))
    for name, payload, expected in cases:
        path = FIXTURES / "bundles" / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        try:
            assert cli.main(["container-health", "assess", str(path.relative_to(ROOT))]) == 0
            assert json.loads(capsys.readouterr().out)["health_status"] == expected
        finally:
            path.unlink()


def test_cli_rejects_registry_mismatch_unsafe_fixture_root_and_broken_evidence_reference(capsys):
    original = load_json(FIXTURES / "bundles/healthy.json")
    cases = []
    mismatch = json.loads(json.dumps(original))
    mismatch["declared_subject"]["environment"] = "production"
    cases.append(("registry-mismatch.json", mismatch))
    unsafe_root = json.loads(json.dumps(original))
    unsafe_root["registry_records_root"] = "registry"
    cases.append(("unsafe-registry-root.json", unsafe_root))
    broken_reference = json.loads(json.dumps(original))
    broken_reference["evidence"][0]["source_reference"] = "engineering/tests/fixtures/container_health/providers/missing.json"
    cases.append(("broken-evidence-reference.json", broken_reference))
    for name, payload in cases:
        path = FIXTURES / "bundles" / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        try:
            assert cli.main(["container-health", "assess", str(path.relative_to(ROOT))]) != 0
            assert "Status: FAIL" in capsys.readouterr().out
        finally:
            path.unlink()


def test_cli_evidence_validation_and_capability_listing(capsys):
    payload = evidence_to_json(healthy_evidence()[0])
    path = ROOT / "engineering/tests/fixtures/container_health/evidence.json"
    path.write_text(payload, encoding="utf-8")
    try:
        assert cli.main(["container-health", "evidence", "validate", str(path.relative_to(ROOT))]) == 0
        assert "Status: PASS" in capsys.readouterr().out
    finally:
        path.unlink()
    assert cli.main(["capabilities"]) == 0
    assert "Fixture Only; Not Activated" in capsys.readouterr().out


def test_fixture_only_eo_assignment_completion_and_automation_handoff_reuse_published_contracts():
    manifest = load_json(FIXTURES / "eo/contract-integration.json")
    assert manifest["artifact_references"] == [
        "engineering/tests/fixtures/container_health/bundles/healthy.json",
        "engineering/tests/fixtures/container_health/reconciliations/healthy.json",
        "engineering/tests/fixtures/container_health/assessments/healthy.json",
        "engineering/tests/fixtures/container_health/expected/healthy.md",
    ]
    assert len(manifest["completion_evidence_ids"]) == len(manifest["artifact_references"]) == 4
    assignment = GovernedAssignment(
        EXECUTION_MODEL_VERSION,
        manifest["assignment_id"],
        "Evaluate Container Operational Health repository fixtures",
        GovernedRole.EXECUTION_AGENT,
        ("engineering/tests/fixtures/container_health",),
        ("validate repository fixture evidence",),
        ("access providers", "activate execution", "mutate infrastructure"),
        ("container-health-tests",),
        (EvidenceRequirement("PLAT-14.1A-REQ", EvidenceType.ARTIFACT, "container-health-tests"),),
        (),
        tuple(manifest["artifact_references"]),
        HEAD,
    )
    participant = Participant("fixture-participant")
    context = ExecutionContext(
        EXECUTION_MODEL_VERSION, participant, GovernedRole.EXECUTION_AGENT, assignment.assignment_id,
        "FitzpatrickFamilyPlatform", "main", HEAD, "fixture-only evaluation", EVALUATED_AT, (),
    )
    evidence_inventory = tuple(
        EvidenceRecord(
            EXECUTION_MODEL_VERSION, evidence_id, EvidenceType.ARTIFACT, "fixture-only PLAT-14.1A evaluation",
            "Validated repository fixture artifact.", EVALUATED_AT, assignment.assignment_id, "container-health-tests", path,
        )
        for evidence_id, path in zip(manifest["completion_evidence_ids"], manifest["artifact_references"])
    )
    result = ExecutionResult(
        EXECUTION_MODEL_VERSION, assignment.assignment_id, OutcomeStatus.COMPLETED,
        "Fixture-only Container Operational Health contracts validated.",
        ("validate repository fixture evidence",), (), ("container-health-tests",),
        tuple(item.evidence_id for item in evidence_inventory), (), (), EVALUATED_AT,
    )
    completion = CompletionPackage(
        EXECUTION_MODEL_VERSION, assignment, participant, context, result,
        (ValidationFinding(ExecutionFindingSeverity.INFO, "container-health.fixture.pass", "Fixture evaluation passed."),),
        evidence_inventory, (), "Architecture Gatekeeper review", False, False, False, False,
    )
    assert not {finding.code for finding in validate_assignment(assignment, repository_root=ROOT) if finding.severity == ExecutionFindingSeverity.ERROR}
    assert not {finding.code for finding in validate_completion_package(completion, repository_root=ROOT) if finding.severity == ExecutionFindingSeverity.ERROR}

    definition = GovernedAutomationDefinition(
        "eo-14.4a-v1", manifest["automation_id"], "Fixture assessment review", "Coordinate advisory human review only.",
        ("engineering/tests/fixtures/container_health/eo/contract-integration.json",),
        (
            OrchestrationStep("completion", "Completion Review", AutomationStepType.EXECUTION_COMPLETION_REVIEW, (), (), None, assignment.assignment_id, (EvidenceType.ARTIFACT,), ("completion.valid",), ("handoff",), True, LiveImpact.NONE, True),
            OrchestrationStep("handoff", "Human Handoff", AutomationStepType.HUMAN_HANDOFF, ("completion",), (), None, None, (), (), (), True, LiveImpact.NONE, True),
        ),
        AutomationLifecycleState.DRAFTED,
        (AutomationLifecycleState.COMPLETED, AutomationLifecycleState.FAILED, AutomationLifecycleState.CANCELLED),
        (), FailurePolicy.BLOCK_PENDING_HUMAN_REVIEW, (assignment.assignment_id,), (assignment.assignment_id,),
        tuple(item.evidence_id for item in evidence_inventory), LiveImpact.REPOSITORY_ONLY,
        ("engineering/tests/fixtures/container_health",),
    )
    run = AutomationRunContext(
        "eo-14.4a-v1", definition, "PLAT-14.1A-FIXTURE-RUN", "FitzpatrickFamilyPlatform", "main", HEAD,
        "fixture-only evaluation", EVALUATED_AT, AutomationLifecycleState.IN_PROGRESS, "handoff", ("completion",), (),
        (assignment,), (completion,), (), "none",
    )
    automation_errors = {finding.code for finding in validate_automation_run(run, ROOT) if finding.severity == ExecutionFindingSeverity.ERROR}
    assert not automation_errors
    handoff = build_automation_handoff(run, ROOT)
    assert handoff.activation_occurred is False
    assert handoff.live_changes_occurred is False
    assert "human" in handoff.recommended_next_approval_gate.lower()
    assert manifest["activation_status"] == ACTIVATION_STATUS
    assert not any(manifest[key] for key in ("model_execution_occurred", "provider_access_occurred", "runtime_activation_occurred", "live_changes_occurred"))


def test_container_health_module_has_no_network_subprocess_plugin_or_file_writer_surface():
    source = (ROOT / "engineering/platform_eap/container_health.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert not imports & {"socket", "subprocess", "requests", "urllib", "http", "docker", "prometheus_client"}
    calls = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
    assert not calls & {"write_text", "write_bytes", "open", "unlink", "rename"}


def test_container_health_uses_only_public_registry_execution_and_automation_interfaces():
    governed_modules = {
        "engineering.platform_eap.registry_identity",
        "engineering.platform_eap.execution_capability",
        "engineering.platform_eap.automation_capability",
    }
    for relative in (
        "engineering/platform_eap/container_health.py",
        "engineering/platform_eap/container_health_io.py",
        "engineering/platform_eap/container_health_rendering.py",
        "engineering/platform_eap/cli.py",
    ):
        tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in governed_modules:
                assert not [alias.name for alias in node.names if alias.name.startswith("_")]


def test_authoritative_registry_records_are_not_fixture_inputs():
    fixture_text = "\n".join(
        path.read_text(encoding="utf-8")
        for suffix in ("*.json", "*.yaml")
        for path in FIXTURES.rglob(suffix)
    )
    assert "registry/records/" not in fixture_text
    assert "svc-pihole-dns" not in fixture_text
