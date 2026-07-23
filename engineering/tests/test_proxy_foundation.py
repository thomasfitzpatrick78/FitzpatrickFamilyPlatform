import ast
import json
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from engineering.platform_eap import cli
from engineering.platform_eap.proxy_foundation import (
    ACTIVATION_STATUS,
    ADAPTER_VERSION,
    CAPABILITY_VERSION,
    CONFIGURATION_VERSION,
    CONTRACT_VERSION,
    FIXTURE_ROOT,
    MAX_REQUEST_PAYLOAD_BYTES,
    MAX_RESPONSE_PAYLOAD_BYTES,
    MAX_RESPONSE_RECORDS,
    POLICY_VERSION,
    PROXY_VERSION,
    FindingSeverity,
    ProxyAuthenticationMode,
    ProxyDecisionStatus,
    ProxyEndpointCategory,
    ProxyMethodCategory,
    ProxyPolicyState,
    authorization_digest,
    configuration_digest,
    contract_summary,
    deterministic_json,
    evaluate_request,
    policy_digest,
    repository_capability,
    repository_configuration,
    repository_identity,
    repository_policy,
    validate_authentication,
    validate_authorization,
    validate_capability,
    validate_configuration,
    validate_policy,
    validate_request,
    validate_response,
    validate_target,
)
from engineering.platform_eap.proxy_foundation_io import (
    capability_from_json,
    capability_to_json,
    configuration_from_json,
    configuration_to_json,
    load_json,
    policy_from_json,
    policy_to_json,
    request_from_dict,
    request_from_json,
    request_to_json,
    response_from_json,
    response_to_json,
    result_to_json,
)
from engineering.platform_eap.proxy_foundation_mock import RepositoryMockProxy, RepositoryProxyFixtureLibrary


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / FIXTURE_ROOT
REQUEST_PATH = FIXTURES / "proxy-request.json"
RESPONSE_PATH = FIXTURES / "proxy-response.json"
POLICY_PATH = FIXTURES / "proxy-policy.json"
CONFIGURATION_PATH = FIXTURES / "proxy-configuration.json"
CAPABILITY_PATH = FIXTURES / "proxy-capability.json"


def library():
    return RepositoryProxyFixtureLibrary(ROOT)


def request():
    return library().base_request()


def response():
    return library().base_response()


def codes(findings):
    return {finding.code for finding in findings if finding.severity == FindingSeverity.ERROR}


def test_public_contract_versions_and_repository_scope_are_explicit():
    identity = repository_identity()
    capability = repository_capability()
    configuration = repository_configuration()
    policy = repository_policy()
    assert (identity.contract_version, capability.contract_version, configuration.contract_version, policy.contract_version) == (CONTRACT_VERSION,) * 4
    assert (identity.proxy_version, capability.proxy_version) == (PROXY_VERSION,) * 2
    assert capability.capability_version == CAPABILITY_VERSION
    assert configuration.configuration_version == CONFIGURATION_VERSION
    assert policy.policy_version == POLICY_VERSION
    assert capability.adapter_version == ADAPTER_VERSION
    assert identity.fixture_only and identity.activation_status == ACTIVATION_STATUS


def test_contract_models_are_frozen():
    with pytest.raises(FrozenInstanceError):
        request().request_id = "changed"
    with pytest.raises(FrozenInstanceError):
        response().payload_size_bytes = 0


@pytest.mark.parametrize(
    "loader,serializer,path",
    [
        (request_from_json, request_to_json, REQUEST_PATH),
        (response_from_json, response_to_json, RESPONSE_PATH),
        (policy_from_json, policy_to_json, POLICY_PATH),
        (configuration_from_json, configuration_to_json, CONFIGURATION_PATH),
        (capability_from_json, capability_to_json, CAPABILITY_PATH),
    ],
)
def test_public_contract_round_trips_are_deterministic(loader, serializer, path):
    model = loader(path.read_text(encoding="utf-8"))
    assert serializer(model) == serializer(loader(serializer(model)))


@pytest.mark.parametrize(
    "actual,expected",
    [
        (policy_from_json(POLICY_PATH.read_text(encoding="utf-8")), repository_policy()),
        (configuration_from_json(CONFIGURATION_PATH.read_text(encoding="utf-8")), repository_configuration()),
        (capability_from_json(CAPABILITY_PATH.read_text(encoding="utf-8")), repository_capability()),
    ],
)
def test_machine_readable_governed_artifacts_match_public_models(actual, expected):
    assert actual == expected


def test_strict_json_rejects_duplicate_and_unknown_fields():
    source = REQUEST_PATH.read_text(encoding="utf-8")
    duplicate = source.replace('"contract_version": "1.0",', '"contract_version": "1.0",\n  "contract_version": "1.0",', 1)
    with pytest.raises(Exception, match="Duplicate JSON field"):
        request_from_json(duplicate)
    payload = json.loads(source)
    payload["runtime_endpoint"] = "prohibited"
    with pytest.raises(Exception, match="unknown or unsafe fields"):
        request_from_dict(payload)


@pytest.mark.parametrize("version", ["1.1", "2.0", "9.0"])
def test_future_and_unsupported_contract_versions_fail_closed(version):
    payload = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    payload["contract_version"] = version
    with pytest.raises(Exception, match="unsupported version"):
        request_from_json(json.dumps(payload))


def test_unknown_endpoint_category_fails_closed_in_parser():
    payload = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    payload["endpoint_category"] = "UnknownCategory"
    with pytest.raises(Exception, match="unsupported value"):
        request_from_json(json.dumps(payload))


def test_malformed_fixture_and_payload_size_fail_before_use():
    with pytest.raises(Exception, match="not valid JSON"):
        request_from_json(library().malformed_request_text())
    with pytest.raises(Exception, match="maximum payload size"):
        load_json(" " * (MAX_RESPONSE_PAYLOAD_BYTES + 1), "oversized", MAX_RESPONSE_PAYLOAD_BYTES)
    with pytest.raises(Exception, match="maximum payload size"):
        request_from_json(" " * (MAX_REQUEST_PAYLOAD_BYTES + 1))


def test_endpoint_category_matrix_classifies_every_category_exactly_once():
    policy = repository_policy()
    assert {entry.endpoint_category for entry in policy.entries} == set(ProxyEndpointCategory)
    assert len(policy.entries) == len(ProxyEndpointCategory)
    states = {entry.endpoint_category: entry.state for entry in policy.entries}
    assert states[ProxyEndpointCategory.LIFECYCLE_OBSERVATION] == ProxyPolicyState.ALLOWED
    assert states[ProxyEndpointCategory.HEALTH_OBSERVATION] == ProxyPolicyState.ALLOWED
    assert states[ProxyEndpointCategory.RESTART_INFORMATION] == ProxyPolicyState.ALLOWED
    assert states[ProxyEndpointCategory.STATISTICS] == ProxyPolicyState.CONDITIONALLY_ALLOWED
    assert states[ProxyEndpointCategory.IDENTITY_DISCOVERY] == ProxyPolicyState.CONDITIONALLY_ALLOWED
    assert states[ProxyEndpointCategory.EVENTS] == ProxyPolicyState.FUTURE
    for category in {
        ProxyEndpointCategory.IMAGES,
        ProxyEndpointCategory.VOLUMES,
        ProxyEndpointCategory.NETWORKS,
        ProxyEndpointCategory.BUILD,
        ProxyEndpointCategory.EXEC,
        ProxyEndpointCategory.ARCHIVE,
        ProxyEndpointCategory.FILESYSTEM,
        ProxyEndpointCategory.SECRETS,
        ProxyEndpointCategory.PLUGINS,
        ProxyEndpointCategory.SWARM,
        ProxyEndpointCategory.SYSTEM,
        ProxyEndpointCategory.CONFIGURATION,
    }:
        assert states[category] == ProxyPolicyState.DENIED


def test_policy_configuration_and_capability_validate_cleanly_and_bind_digests():
    policy = repository_policy()
    configuration = repository_configuration()
    capability = repository_capability()
    assert not validate_policy(policy)
    assert not validate_configuration(configuration)
    assert not validate_capability(capability)
    assert policy.policy_digest == policy_digest(policy)
    assert configuration.configuration_digest == configuration_digest(configuration)
    assert capability.live_access_supported is False
    assert capability.networking_supported is False
    assert capability.socket_access_supported is False


@pytest.mark.parametrize(
    "changed,code",
    [
        ({"default_state": ProxyPolicyState.ALLOWED}, "policy.default_deny.required"),
        ({"policy_digest": "sha256:" + "0" * 64}, "policy.digest.mismatch"),
        ({"fixture_only": False}, "policy.repository_scope.required"),
    ],
)
def test_policy_drift_fails_closed(changed, code):
    assert code in codes(validate_policy(replace(repository_policy(), **changed)))


@pytest.mark.parametrize(
    "changed,code",
    [
        ({"allow_networking": True}, "configuration.privileged_capability.prohibited"),
        ({"allow_runtime_access": True}, "configuration.privileged_capability.prohibited"),
        ({"allow_streaming": True}, "configuration.privileged_capability.prohibited"),
        ({"require_authentication": False}, "configuration.fail_closed.required"),
        ({"configuration_digest": "sha256:" + "0" * 64}, "configuration.digest.mismatch"),
    ],
)
def test_configuration_drift_fails_closed(changed, code):
    assert code in codes(validate_configuration(replace(repository_configuration(), **changed)))


def test_authentication_abstractions_are_contracts_only():
    assert {mode.value for mode in ProxyAuthenticationMode} == {
        "LocalUnixIdentity", "MutualTLS", "ServiceIdentity", "AdministratorAuthorization", "NamedTargetAuthorization"
    }
    assert not validate_authentication(request().authentication)
    assert "authentication.required" in codes(validate_authentication(replace(request().authentication, authenticated=False)))


@pytest.mark.parametrize("mode", [mode for mode in ProxyAuthenticationMode if mode != ProxyAuthenticationMode.SERVICE_IDENTITY])
def test_conceptual_authentication_modes_are_not_enabled(mode):
    active = request()
    changed = replace(active, authentication=replace(active.authentication, mode=mode))
    decision = evaluate_request(changed, repository_policy(), repository_configuration(), repository_capability())
    assert decision.decision == ProxyDecisionStatus.UNAUTHORIZED
    assert decision.decision_code == "authentication_mode_unsupported"


@pytest.mark.parametrize(
    "target_change,code",
    [
        ({"subject_id": "*"}, "target.exact.required"),
        ({"registry_subject_reference": "registry/records/services/example.yaml"}, "target.registry_fixture.required"),
        ({"environment": "production"}, "target.fixture_scope.required"),
        ({"fixture_only": False}, "target.fixture_scope.required"),
    ],
)
def test_target_validation_rejects_wildcard_live_and_authoritative_targets(target_change, code):
    assert code in codes(validate_target(replace(request().target, **target_change)))


@pytest.mark.parametrize(
    "authorization_change,code",
    [
        ({"approval_reference": ""}, "authorization.approval_reference.required"),
        ({"approval_reference": "APPROVAL-REAL"}, "authorization.approval.fixture_required"),
        ({"authorization_digest": "sha256:" + "0" * 64}, "authorization.digest.mismatch"),
        ({"configuration_digest": "sha256:" + "1" * 64}, "authorization.configuration_digest.mismatch"),
        ({"proxy_version": "unsupported"}, "authorization.version.mismatch"),
        ({"subject_id": "*"}, "authorization.subject_id.required"),
        ({"fixture_only": False}, "authorization.fixture_scope.required"),
    ],
)
def test_authorization_contract_fails_closed(authorization_change, code):
    assert code in codes(validate_authorization(replace(request().authorization, **authorization_change)))


def test_authorization_digest_is_canonical_and_expiration_is_enforced():
    authorization = request().authorization
    assert authorization.authorization_digest == authorization_digest(authorization)
    expired = replace(authorization, observation_window_end="2026-07-22T11:30:00Z", expires_at="2026-07-22T11:30:00Z", authorization_digest="")
    expired = replace(expired, authorization_digest=authorization_digest(expired))
    changed = replace(request(), authorization=expired)
    assert "authorization.expired" in codes(validate_request(changed))


@pytest.mark.parametrize(
    "scenario_id,expected",
    [
        ("allowed_lifecycle", ProxyDecisionStatus.ALLOWED),
        ("allowed_health", ProxyDecisionStatus.ALLOWED),
        ("allowed_restart", ProxyDecisionStatus.ALLOWED),
        ("allowed_statistics", ProxyDecisionStatus.ALLOWED),
        ("denied_images", ProxyDecisionStatus.DENIED),
        ("denied_exec", ProxyDecisionStatus.DENIED),
        ("denied_filesystem", ProxyDecisionStatus.DENIED),
        ("denied_secrets", ProxyDecisionStatus.DENIED),
        ("denied_plugins", ProxyDecisionStatus.DENIED),
        ("denied_swarm", ProxyDecisionStatus.DENIED),
        ("denied_build", ProxyDecisionStatus.DENIED),
        ("denied_archive", ProxyDecisionStatus.DENIED),
        ("denied_configuration", ProxyDecisionStatus.DENIED),
        ("denied_events_future_gate", ProxyDecisionStatus.FUTURE),
        ("wildcard_target", ProxyDecisionStatus.INVALID_TARGET),
        ("expired_authorization", ProxyDecisionStatus.EXPIRED_AUTHORIZATION),
        ("duplicate_parameters", ProxyDecisionStatus.DENIED),
        ("oversized_payload", ProxyDecisionStatus.PAYLOAD_TOO_LARGE),
        ("unsupported_version", ProxyDecisionStatus.DENIED),
        ("invalid_policy", ProxyDecisionStatus.INVALID_POLICY),
        ("invalid_configuration", ProxyDecisionStatus.INVALID_CONFIGURATION),
        ("response_too_large", ProxyDecisionStatus.RESPONSE_REJECTED),
        ("unsupported_method", ProxyDecisionStatus.UNSUPPORTED_METHOD),
        ("missing_authorization", ProxyDecisionStatus.UNAUTHORIZED),
        ("authorization_digest_mismatch", ProxyDecisionStatus.UNAUTHORIZED),
        ("configuration_digest_mismatch", ProxyDecisionStatus.UNAUTHORIZED),
    ],
)
def test_fixture_scenarios_are_deterministic_and_fail_closed(scenario_id, expected):
    first = RepositoryMockProxy(ROOT).evaluate(scenario_id)
    second = RepositoryMockProxy(ROOT).evaluate(scenario_id)
    assert first == second
    assert result_to_json(first) == result_to_json(second)
    assert first.decision.decision == expected
    assert first.audit_event.fixture_only is True
    if expected == ProxyDecisionStatus.ALLOWED:
        assert first.response is not None and first.failure is None
    else:
        assert first.response is None and first.failure is not None


def test_fixture_catalog_expected_decisions_match_mock_pipeline():
    for scenario_id in library().scenario_ids():
        expected = library().scenario(scenario_id)["expected_decision"]
        assert RepositoryMockProxy(ROOT).evaluate(scenario_id).decision.decision.value == expected


def test_request_validation_rejects_duplicate_parameters_and_oversized_payload():
    active = request()
    duplicate = replace(active, parameters=(active.parameters[0], active.parameters[0]))
    oversized = replace(active, payload_size_bytes=MAX_REQUEST_PAYLOAD_BYTES + 1)
    assert "request.parameters.duplicate" in codes(validate_request(duplicate))
    assert "request.payload.too_large" in codes(validate_request(oversized))


@pytest.mark.parametrize(
    "response_change,code",
    [
        ({"payload_size_bytes": MAX_RESPONSE_PAYLOAD_BYTES + 1}, "response.payload.too_large"),
        ({"records": tuple(response().records) * (MAX_RESPONSE_RECORDS + 1)}, "response.records.too_many"),
    ],
)
def test_response_bounds_fail_closed(response_change, code):
    assert code in codes(validate_response(replace(response(), **response_change), request()))


def test_response_identity_provenance_limitations_and_timestamps_are_validated():
    active = response()
    wrong = replace(active, metadata=replace(active.metadata, target_subject_id="other"))
    assert "response.identity.mismatch" in codes(validate_response(wrong, request()))
    outside = replace(active, metadata=replace(active.metadata, provenance_reference="outside.json"))
    assert "response.provenance.invalid" in codes(validate_response(outside, request()))
    stale = replace(active, metadata=replace(active.metadata, completed_at="2026-07-22T11:00:00Z"))
    assert "response.timestamps.invalid" in codes(validate_response(stale, request()))


def test_policy_engine_is_pure_and_deterministic():
    active = request()
    first = evaluate_request(active, repository_policy(), repository_configuration(), repository_capability())
    second = evaluate_request(active, repository_policy(), repository_configuration(), repository_capability())
    assert first == second
    assert first.decision == ProxyDecisionStatus.ALLOWED


def test_contract_summary_explicitly_blocks_every_live_gate():
    summary = contract_summary()
    assert summary["repository_only"] is True
    assert summary["live_access"] == "absent"
    assert summary["networking"] == "absent"
    assert summary["socket_access"] == "absent"
    assert summary["deployment"] == "not_authorized"
    assert summary["privileged_access"] == "not_authorized"
    assert summary["named_target_authorization"] == "not_authorized"


def test_proxy_modules_have_no_network_socket_process_shell_environment_or_random_capability():
    module_paths = [
        ROOT / "engineering/platform_eap/proxy_foundation.py",
        ROOT / "engineering/platform_eap/proxy_foundation_io.py",
        ROOT / "engineering/platform_eap/proxy_foundation_mock.py",
    ]
    forbidden_imports = {"aiohttp", "asyncio", "docker", "http", "paramiko", "pty", "random", "requests", "socket", "subprocess", "urllib", "os"}
    forbidden_calls = {"connect", "create_connection", "getenv", "Popen", "run", "system", "spawn"}
    forbidden_text = ("/var/run/", "DOCKER_HOST", "http://", "https://", "/containers/", "/images/", "/exec/")
    for path in module_paths:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in (node.names if isinstance(node, ast.Import) else [ast.alias(name=node.module or "")])
        }
        calls = {
            (node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id)
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, (ast.Attribute, ast.Name))
        }
        assert not forbidden_imports.intersection(imports)
        assert not forbidden_calls.intersection(calls)
        assert not any(text in source for text in forbidden_text)


@pytest.mark.parametrize(
    "command",
    [
        ["proxy", "contract"],
        ["proxy", "validate"],
        ["proxy", "policy"],
        ["proxy", "fixtures"],
        ["proxy", "request", "allowed_lifecycle"],
        ["proxy", "response", "allowed_lifecycle"],
        ["proxy", "decision", "allowed_lifecycle"],
        ["proxy", "mock", "allowed_lifecycle"],
    ],
)
def test_proxy_cli_repository_commands_succeed(command, capsys):
    assert cli.main(command) == 0
    assert capsys.readouterr().out


def test_proxy_cli_validates_each_governed_artifact(capsys):
    request_path = str(REQUEST_PATH.relative_to(ROOT))
    response_path = str(RESPONSE_PATH.relative_to(ROOT))
    for command in (
        ["proxy", "validate", "request", request_path],
        ["proxy", "validate", "response", request_path, response_path],
        ["proxy", "validate", "policy", str(POLICY_PATH.relative_to(ROOT))],
        ["proxy", "validate", "configuration", str(CONFIGURATION_PATH.relative_to(ROOT))],
        ["proxy", "validate", "capability", str(CAPABILITY_PATH.relative_to(ROOT))],
    ):
        assert cli.main(command) == 0
        assert "Status: PASS" in capsys.readouterr().out


def test_proxy_cli_rejects_live_mode_and_paths_outside_fixture_root(capsys):
    assert cli.main(["proxy", "live"]) == 2
    assert "Usage:" in capsys.readouterr().out
    assert cli.main(["proxy", "validate", "request", "registry/records/services/pihole-dns.yaml"]) == 2
    assert "only governed proxy-foundation fixtures" in capsys.readouterr().out


def test_platform_eap_capability_inventory_includes_repository_proxy(capsys):
    assert cli.main(["capabilities"]) == 0
    output = capsys.readouterr().out
    assert "PLAT-EAP-14" in output
    assert "No Socket or Network Access" in output


def test_fixture_library_rejects_traversal():
    with pytest.raises(Exception, match="unsafe"):
        library()._path("../proxy-request.json")


def test_no_authoritative_registry_record_is_referenced_or_mutated_by_fixtures():
    for path in FIXTURES.iterdir():
        text = path.read_text(encoding="utf-8")
        assert "registry/records/" not in text
        assert "svc-pihole" not in text
