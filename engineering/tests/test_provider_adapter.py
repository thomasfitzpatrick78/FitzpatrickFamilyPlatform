import ast
import json
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from engineering.platform_eap import cli
from engineering.platform_eap.container_health import HealthStatus, validate_evidence
from engineering.platform_eap.provider_adapter import (
    ACTIVATION_STATUS,
    ADAPTER_VERSION,
    CONTRACT_VERSION,
    FIXTURE_ROOT,
    MAX_PAYLOAD_BYTES,
    FindingSeverity,
    MockScenario,
    ObservationMode,
    ProviderAdapterDataError,
    ProviderFailureCategory,
    TargetResolution,
    UnavailableProviderAdapter,
    failure_for_scenario,
    normalize_response,
    repository_adapter_identity,
    repository_capability,
    validate_adapter_identity,
    validate_capability,
    validate_failure,
    validate_request,
    validate_response,
    validate_result,
)
from engineering.platform_eap.provider_adapter_io import (
    adapter_identity_from_dict,
    adapter_identity_to_json,
    capability_from_json,
    capability_to_json,
    contract_summary_to_json,
    load_json,
    provider_failure_from_json,
    provider_failure_to_json,
    provider_normalization_result_from_json,
    provider_normalization_result_to_json,
    provider_request_from_dict,
    provider_request_from_json,
    provider_request_to_json,
    provider_response_from_json,
    provider_response_to_json,
    provider_result_from_json,
    provider_result_to_json,
)
from engineering.platform_eap.provider_adapter_mock import MockProviderAdapter, RepositoryFixtureClient


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / FIXTURE_ROOT
REQUEST_PATH = FIXTURES / "provider-request.json"
CAPABILITY_PATH = FIXTURES / "provider-capability.json"


def request():
    return provider_request_from_json(REQUEST_PATH.read_text(encoding="utf-8"))


def client():
    return RepositoryFixtureClient(ROOT)


def response(fixture_id: str = "healthy_lifecycle"):
    return client().response(fixture_id, request())


def error_codes(findings):
    return {finding.code for finding in findings if finding.severity == FindingSeverity.ERROR}


def test_public_contract_identity_and_capability_are_immutable_repository_only():
    identity = repository_adapter_identity()
    capability = repository_capability()
    with pytest.raises(FrozenInstanceError):
        identity.adapter_id = "changed"
    with pytest.raises(FrozenInstanceError):
        capability.live_access_supported = True
    assert identity.contract_version == CONTRACT_VERSION
    assert identity.adapter_version == ADAPTER_VERSION
    assert identity.fixture_only is True
    assert identity.activation_status == ACTIVATION_STATUS
    assert capability.fixture_only is True
    assert capability.live_access_supported is False
    assert capability.supported_observation_modes == (ObservationMode.REPOSITORY_FIXTURE_ONE_SHOT,)
    assert not error_codes(validate_adapter_identity(identity))
    assert not error_codes(validate_capability(capability))


def test_all_nested_request_contracts_are_immutable_and_versioned():
    value = request()
    for model in (value, value.authorization_context, value.mandatory_signal_set, value.optional_signal_set):
        assert model.contract_version == CONTRACT_VERSION
        with pytest.raises(FrozenInstanceError):
            model.contract_version = "2.0"
    assert not error_codes(validate_request(value))


def test_adapter_identity_and_capability_serialization_are_stable():
    identity_text = adapter_identity_to_json(repository_adapter_identity())
    identity = adapter_identity_from_dict(json.loads(identity_text))
    assert identity == repository_adapter_identity()
    capability_text = capability_to_json(repository_capability())
    assert capability_from_json(capability_text) == repository_capability()
    assert identity_text == adapter_identity_to_json(identity)
    assert capability_text == capability_to_json(capability_from_json(capability_text))


def test_provider_request_serialization_is_stable():
    value = request()
    text = provider_request_to_json(value)
    assert provider_request_from_json(text) == value
    assert provider_request_to_json(provider_request_from_json(text)) == text


def test_provider_response_serialization_is_stable():
    value = response()
    text = provider_response_to_json(value)
    assert provider_response_from_json(text) == value
    assert provider_response_to_json(provider_response_from_json(text)) == text
    assert not error_codes(validate_response(value, request()))


def test_provider_failure_and_result_serialization_are_stable():
    failure = failure_for_scenario(request(), MockScenario.PROVIDER_UNAVAILABLE)
    failure_text = provider_failure_to_json(failure)
    assert provider_failure_from_json(failure_text) == failure
    assert not error_codes(validate_failure(failure))
    result = UnavailableProviderAdapter().collect_observation(request())
    result_text = provider_result_to_json(result)
    assert provider_result_from_json(result_text) == result
    assert not error_codes(validate_result(result))


def test_normalization_result_serialization_reuses_operational_evidence_contract():
    result = normalize_response(request(), response())
    assert result.failure_result is None
    assert len(result.evidence_records) == 5
    assert all(not [finding for finding in validate_evidence(item) if finding.severity.value == "ERROR"] for item in result.evidence_records)
    text = provider_normalization_result_to_json(result)
    assert provider_normalization_result_from_json(text) == result
    assert provider_normalization_result_to_json(provider_normalization_result_from_json(text)) == text


@pytest.mark.parametrize(
    "loader,payload",
    [
        (provider_request_from_json, REQUEST_PATH.read_text(encoding="utf-8")),
        (capability_from_json, CAPABILITY_PATH.read_text(encoding="utf-8")),
        (provider_response_from_json, provider_response_to_json(response())),
        (provider_failure_from_json, provider_failure_to_json(failure_for_scenario(request(), MockScenario.TIMEOUT))),
        (provider_result_from_json, provider_result_to_json(UnavailableProviderAdapter().collect_observation(request()))),
    ],
)
def test_public_contract_parsers_reject_unknown_fields(loader, payload):
    value = json.loads(payload)
    value["unknown_field"] = True
    with pytest.raises(ProviderAdapterDataError, match="unknown or unsafe fields"):
        loader(json.dumps(value))


def test_strict_json_rejects_duplicate_fields():
    text = REQUEST_PATH.read_text(encoding="utf-8")
    duplicate = text.replace('"contract_version": "1.0",', '"contract_version": "1.0",\n  "contract_version": "1.0",', 1)
    with pytest.raises(ProviderAdapterDataError, match="Duplicate JSON field"):
        provider_request_from_json(duplicate)


@pytest.mark.parametrize("version", ["2.0", "9.0", "1.1"])
def test_future_or_unsupported_contract_versions_fail_closed(version):
    value = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    value["contract_version"] = version
    with pytest.raises(Exception, match="unsupported version"):
        provider_request_from_json(json.dumps(value))


def test_payload_size_limit_fails_before_json_parsing():
    with pytest.raises(ProviderAdapterDataError, match="maximum payload size"):
        load_json(" " * (MAX_PAYLOAD_BYTES + 1), "oversized provider response", MAX_PAYLOAD_BYTES)


@pytest.mark.parametrize(
    "change,code",
    [
        ({"observation_mode": ObservationMode.NAMED_TARGET_ONE_SHOT}, "authorization.named_target.prohibited"),
        ({"fixture_only": False}, "authorization.repository_scope.required"),
        ({"activation_status": "active"}, "authorization.repository_scope.required"),
        ({"subject_id": "svc-pihole-dns"}, "authorization.subject.invalid"),
        ({"subject_id": "*"}, "authorization.subject.invalid"),
        ({"registry_reference": "registry/records/services/pihole-dns.yaml"}, "authorization.registry.fixture_required"),
        ({"authorization_reference": "../outside.json"}, "authorization.authorization_reference.unsafe"),
    ],
)
def test_authorization_context_rejects_live_or_unsafe_scope(change, code):
    value = request()
    changed = replace(value, authorization_context=replace(value.authorization_context, **change))
    assert code in error_codes(validate_request(changed))


@pytest.mark.parametrize(
    "mandatory,optional,code",
    [
        ((), (), "request.signal_set.invalid"),
        (("container.lifecycle.observed_state", "container.lifecycle.observed_state"), (), "request.signal_set.invalid"),
        (("container.lifecycle.observed_state",), ("container.lifecycle.observed_state",), "request.signal_set.invalid"),
        (("provider.unknown.signal",), (), "request.signal.unsupported"),
    ],
)
def test_signal_sets_are_closed_deterministic_and_disjoint(mandatory, optional, code):
    value = request()
    changed = replace(
        value,
        mandatory_signal_set=replace(value.mandatory_signal_set, signals=mandatory),
        optional_signal_set=replace(value.optional_signal_set, signals=optional),
    )
    assert code in error_codes(validate_request(changed))


def test_fixture_library_contains_every_authorized_synthetic_case():
    expected = {
        "healthy_lifecycle",
        "restarting",
        "stopped",
        "healthcheck_failed",
        "healthcheck_missing",
        "cpu_pressure",
        "memory_pressure",
        "missing_lifecycle",
        "missing_identity",
        "provider_unavailable",
        "unsupported_provider_version",
        "conflicting_compose_labels",
        "duplicate_runtime_names",
        "unknown_registry_target",
        "unexpected_container",
        "no_provider_data",
        "provider_limitation",
    }
    assert set(client().fixture_names()) == expected
    assert (FIXTURES / "malformed-provider-response.json").is_file()


@pytest.mark.parametrize(
    "fixture_id",
    [
        "healthy_lifecycle",
        "restarting",
        "stopped",
        "healthcheck_failed",
        "healthcheck_missing",
        "cpu_pressure",
        "memory_pressure",
        "missing_lifecycle",
        "missing_identity",
        "provider_unavailable",
        "unsupported_provider_version",
        "conflicting_compose_labels",
        "duplicate_runtime_names",
        "unknown_registry_target",
        "unexpected_container",
        "no_provider_data",
        "provider_limitation",
    ],
)
def test_every_catalog_fixture_parses_deterministically(fixture_id):
    first = client().response(fixture_id, request())
    second = client().response(fixture_id, request())
    assert first == second
    assert provider_response_to_json(first) == provider_response_to_json(second)
    assert first.fixture_only is True
    assert first.activation_status == ACTIVATION_STATUS


@pytest.mark.parametrize(
    "scenario,category",
    [
        (MockScenario.PROVIDER_UNAVAILABLE, ProviderFailureCategory.PROVIDER_UNAVAILABLE),
        (MockScenario.TIMEOUT, ProviderFailureCategory.PROVIDER_TIMEOUT),
        (MockScenario.AUTHORIZATION_DENIED, ProviderFailureCategory.PROVIDER_AUTHORIZATION_FAILURE),
        (MockScenario.UNSUPPORTED_PROVIDER_VERSION, ProviderFailureCategory.PROVIDER_VERSION_MISMATCH),
        (MockScenario.MALFORMED_PAYLOAD, ProviderFailureCategory.MALFORMED_RESPONSE),
        (MockScenario.CAPABILITY_MISMATCH, ProviderFailureCategory.CAPABILITY_UNSUPPORTED),
        (MockScenario.LARGE_PAYLOAD_REJECTION, ProviderFailureCategory.RESPONSE_OVERSIZED),
    ],
)
def test_mock_provider_direct_failures_are_deterministic(scenario, category):
    adapter = MockProviderAdapter(ROOT, scenario)
    first = adapter.collect_observation(request())
    second = adapter.collect_observation(request())
    assert first == second
    assert first.observation_result is None
    assert first.failure_result is not None
    assert first.failure_result.failure_category == category
    assert not error_codes(validate_failure(first.failure_result))


@pytest.mark.parametrize(
    "scenario,fixture_id",
    [
        (MockScenario.HEALTHY, "healthy_lifecycle"),
        (MockScenario.PARTIAL_RESPONSE, "healthcheck_missing"),
        (MockScenario.MISSING_MANDATORY_SIGNALS, "missing_lifecycle"),
        (MockScenario.CONFLICTING_IDENTITY, "conflicting_compose_labels"),
        (MockScenario.UNKNOWN_TARGET, "unknown_registry_target"),
        (MockScenario.DUPLICATE_TARGETS, "duplicate_runtime_names"),
        (MockScenario.PROVIDER_LIMITATION, "provider_limitation"),
    ],
)
def test_mock_provider_fixture_scenarios_use_governed_catalog(scenario, fixture_id):
    adapter = MockProviderAdapter(ROOT, scenario)
    result = adapter.collect_observation(request())
    assert result.observation_result == client().response(fixture_id, request())
    assert result.failure_result is None


def test_default_adapter_is_deterministically_unavailable_without_live_access():
    adapter = UnavailableProviderAdapter()
    assert not error_codes(adapter.validate_configuration())
    result = adapter.collect_observation(request())
    assert result.failure_result is not None
    assert result.failure_result.failure_category == ProviderFailureCategory.PROVIDER_UNAVAILABLE
    assert result.failure_result.failure_code == "PROVIDER_NOT_IMPLEMENTED"


def test_healthy_normalization_preserves_identity_provenance_coverage_and_timestamps():
    source = response()
    result = normalize_response(request(), source)
    assert result.failure_result is None
    assert result.coverage == source.coverage
    assert result.limitations == source.limitations
    assert result.unknown_signals == source.coverage.unknown_signals
    assert {item.signal_name for item in result.evidence_records} == set(request().requested_signals())
    for item in result.evidence_records:
        assert item.subject_id == request().authorization_context.subject_id
        assert item.registry_reference == request().authorization_context.registry_reference
        assert item.provider_id == source.provenance.provider_id
        assert item.provider_version == source.provenance.provider_version
        assert item.source_reference == source.provenance.fixture_reference
        assert item.normalized_at == source.metadata.collection_ended_at


@pytest.mark.parametrize(
    "fixture_id,category",
    [
        ("healthcheck_missing", ProviderFailureCategory.SIGNAL_UNAVAILABLE),
        ("missing_lifecycle", ProviderFailureCategory.SIGNAL_UNAVAILABLE),
        ("missing_identity", ProviderFailureCategory.AMBIGUOUS_TARGET),
        ("conflicting_compose_labels", ProviderFailureCategory.AMBIGUOUS_TARGET),
        ("duplicate_runtime_names", ProviderFailureCategory.AMBIGUOUS_TARGET),
        ("unknown_registry_target", ProviderFailureCategory.UNKNOWN_TARGET),
        ("provider_limitation", ProviderFailureCategory.PROVIDER_LIMITATION),
    ],
)
def test_normalization_failure_paths_emit_no_misleading_evidence(fixture_id, category):
    result = normalize_response(request(), response(fixture_id))
    assert result.evidence_records == ()
    assert result.failure_result is not None
    assert result.failure_result.failure_category == category
    assert not hasattr(result.failure_result, "health_status")


def test_provider_version_mismatch_fails_strict_response_validation():
    findings = validate_response(response("unsupported_provider_version"), request())
    assert "response.provider_version.unsupported" in error_codes(findings)
    result = normalize_response(request(), response("unsupported_provider_version"))
    assert result.failure_result is not None
    assert result.evidence_records == ()


def test_unknown_signals_are_preserved_as_metadata_and_never_emitted_as_evidence():
    source = response("unexpected_container")
    result = normalize_response(request(), source)
    assert result.unknown_signals == ("provider.unexpected.container",)
    assert result.evidence_records == ()


def test_material_limitations_propagate_to_failure():
    source = response("provider_limitation")
    result = normalize_response(request(), source)
    assert result.limitations == source.limitations
    assert result.failure_result is not None
    assert result.failure_result.limitations == source.limitations


def test_provider_contract_never_emits_or_calculates_health():
    normalized = normalize_response(request(), response())
    serialized = provider_normalization_result_to_json(normalized)
    assert '"health_status"' not in serialized
    assert '"assessment_confidence"' not in serialized
    assert not any(status.value in serialized for status in HealthStatus)
    assert normalized.failure_result is None


def test_provider_modules_have_no_network_socket_subprocess_shell_or_random_path():
    module_paths = [
        ROOT / "engineering/platform_eap/provider_adapter.py",
        ROOT / "engineering/platform_eap/provider_adapter_io.py",
        ROOT / "engineering/platform_eap/provider_adapter_mock.py",
    ]
    forbidden_imports = {"docker", "http", "requests", "socket", "subprocess", "urllib", "random"}
    forbidden_calls = {"connect", "create_connection", "Popen", "run", "system", "spawn"}
    for path in module_paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in (node.names if isinstance(node, ast.Import) else [ast.alias(name=node.module or "")])
        }
        calls = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
        assert not forbidden_imports.intersection(imports)
        assert not forbidden_calls.intersection(calls)


def test_contract_summary_explicitly_prohibits_health_and_live_provider_mode():
    payload = json.loads(contract_summary_to_json(repository_adapter_identity(), repository_capability()))
    assert payload["health_status_authority"] == "prohibited"
    assert payload["live_provider_mode"] == "absent"
    assert payload["activation_status"] == ACTIVATION_STATUS


@pytest.mark.parametrize("command", [["provider", "contract"], ["provider", "capabilities"], ["provider", "fixtures"]])
def test_provider_cli_repository_metadata_commands(command, capsys):
    assert cli.main(command) == 0
    output = capsys.readouterr().out
    assert output
    assert "live" in output.lower() or command == ["provider", "capabilities"]


def test_provider_cli_validates_request_and_capability(capsys):
    assert cli.main(["provider", "validate", "request", str(REQUEST_PATH.relative_to(ROOT))]) == 0
    assert "Status: PASS" in capsys.readouterr().out
    assert cli.main(["provider", "validate", "capability", str(CAPABILITY_PATH.relative_to(ROOT))]) == 0
    assert "Status: PASS" in capsys.readouterr().out


def test_provider_cli_normalizes_governed_fixture_deterministically(capsys):
    args = ["provider", "normalize", str(REQUEST_PATH.relative_to(ROOT)), "healthy_lifecycle"]
    assert cli.main(args) == 0
    first = capsys.readouterr().out
    assert cli.main(args) == 0
    second = capsys.readouterr().out
    assert first == second
    payload = json.loads(first)
    assert len(payload["evidence_records"]) == 5
    assert payload["failure_result"] is None


@pytest.mark.parametrize("scenario", [scenario.value for scenario in MockScenario if scenario != MockScenario.HEALTHY])
def test_provider_cli_mock_failure_paths_are_bounded(scenario, capsys):
    args = ["provider", "mock", scenario, str(REQUEST_PATH.relative_to(ROOT))]
    exit_code = cli.main(args)
    output = capsys.readouterr().out
    assert output
    payload = json.loads(output)
    if payload["failure_result"] is not None:
        assert exit_code == 1
        assert payload["observation_result"] is None
    else:
        assert exit_code == 0
        assert payload["observation_result"]["fixture_only"] is True


def test_provider_cli_has_no_live_mode_and_rejects_paths_outside_fixture_root(capsys):
    assert cli.main(["provider", "live"]) == 2
    assert "Usage:" in capsys.readouterr().out
    assert cli.main(["provider", "validate", "request", "registry/records/services/pihole-dns.yaml"]) == 2
    assert "only governed provider-adapter fixtures" in capsys.readouterr().out


def test_fixture_client_rejects_path_traversal_and_malformed_content():
    with pytest.raises(ProviderAdapterDataError, match="unsafe"):
        client()._fixture_path("../provider-request.json")
    with pytest.raises(ProviderAdapterDataError, match="not valid JSON"):
        load_json(client().malformed_text(), "malformed provider fixture", MAX_PAYLOAD_BYTES)


def test_capability_file_matches_public_repository_capability():
    assert capability_from_json(CAPABILITY_PATH.read_text(encoding="utf-8")) == repository_capability()


def test_result_contract_requires_exactly_one_observation_or_failure():
    healthy = MockProviderAdapter(ROOT).collect_observation(request())
    invalid = replace(healthy, failure_result=failure_for_scenario(request(), MockScenario.PROVIDER_UNAVAILABLE))
    assert "result.exactly_one.required" in error_codes(validate_result(invalid))


def test_response_rejects_unrequested_signal_and_wrong_value_type():
    active_request = request()
    healthy = MockProviderAdapter(ROOT).collect_observation(active_request).observation_result
    assert healthy is not None
    extra_signal = replace(healthy.signals[0], signal_name="container.memory.limit", value_type="integer", unit="bytes", value="one")
    invalid = replace(
        healthy,
        signals=tuple(sorted((*healthy.signals, extra_signal), key=lambda signal: signal.signal_name)),
        coverage=replace(
            healthy.coverage,
            returned_signals=tuple(sorted((*healthy.coverage.returned_signals, "container.memory.limit"))),
        ),
    )
    codes = error_codes(validate_response(invalid, active_request))
    assert "response.coverage.unrequested_signal" in codes
    assert "response.signal.value_type_invalid" in codes


def test_request_parser_rejects_unknown_nested_authorization_field():
    payload = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    payload["authorization_context"]["provider_url"] = "fixture.invalid"
    with pytest.raises(ProviderAdapterDataError, match="unknown or unsafe fields"):
        provider_request_from_dict(payload)
