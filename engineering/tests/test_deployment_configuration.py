import ast
import json
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from engineering.platform_eap import cli
from engineering.platform_eap.deployment_configuration import (
    ACTIVATION_STATUS,
    ADAPTER_VERSION,
    AUDIT_CONFIGURATION_VERSION,
    BUNDLE_VERSION,
    COMPATIBILITY_VERSION,
    CONTRACT_VERSION,
    DEPLOYMENT_CONFIGURATION_VERSION,
    DEPLOYMENT_PROFILE_VERSION,
    DIGEST_VERSION,
    ENDPOINT_POLICY_CONFIGURATION_VERSION,
    FIXTURE_ROOT,
    IDENTITY_CONFIGURATION_VERSION,
    RESOURCE_LIMIT_VERSION,
    RUNTIME_CONFIGURATION_VERSION,
    SECURITY_CONFIGURATION_VERSION,
    ConfigurationDigest,
    DeploymentAuthenticationMode,
    DeploymentProfileName,
    FindingSeverity,
    bundle_for,
    configuration_digest,
    contract_summary,
    deployment_profile,
    deterministic_json,
    negotiate_versions,
    repository_configuration,
    repository_endpoint_policy,
    repository_policy,
    validate_adapter,
    validate_audit,
    validate_bundle,
    validate_compatibility,
    validate_configuration,
    validate_endpoint_policy,
    validate_identity,
    validate_profile,
    validate_proxy,
    validate_resource_limits,
    validate_runtime,
    validate_security,
)
from engineering.platform_eap.deployment_configuration_io import (
    bundle_from_json,
    bundle_to_json,
    configuration_from_dict,
    load_json,
)
from engineering.platform_eap.deployment_configuration_fixtures import (
    RepositoryDeploymentFixtureLibrary,
    generated_bundle,
)
from engineering.platform_eap.proxy_foundation import (
    CONFIGURATION_VERSION as PROXY_CONFIGURATION_VERSION,
    POLICY_VERSION,
    PROXY_VERSION,
    ProxyEndpointCategory,
    ProxyMethodCategory,
    ProxyPolicyState,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / FIXTURE_ROOT
BUNDLE_PATH = FIXTURES / "repository-only-bundle.json"


def library():
    return RepositoryDeploymentFixtureLibrary(ROOT)


def bundle():
    return library().bundle_for_profile(DeploymentProfileName.REPOSITORY_ONLY)


def configuration():
    return bundle().configuration


def codes(findings):
    return {item.code for item in findings if item.severity == FindingSeverity.ERROR}


def test_public_contract_versions_are_explicit_and_consistent():
    active = configuration()
    assert active.contract_version == CONTRACT_VERSION
    assert active.configuration_version == DEPLOYMENT_CONFIGURATION_VERSION
    assert active.profile.profile_version == DEPLOYMENT_PROFILE_VERSION
    assert active.identity.identity_version == IDENTITY_CONFIGURATION_VERSION
    assert active.runtime.runtime_version == RUNTIME_CONFIGURATION_VERSION
    assert active.runtime.security.security_version == SECURITY_CONFIGURATION_VERSION
    assert active.runtime.resource_limits.resource_limit_version == RESOURCE_LIMIT_VERSION
    assert active.audit.audit_version == AUDIT_CONFIGURATION_VERSION
    assert active.endpoint_policy.endpoint_policy_version == ENDPOINT_POLICY_CONFIGURATION_VERSION
    assert active.compatibility.compatibility_version == COMPATIBILITY_VERSION
    assert bundle().bundle_version == BUNDLE_VERSION
    assert bundle().digest.digest_version == DIGEST_VERSION


def test_contracts_are_immutable():
    with pytest.raises(FrozenInstanceError):
        configuration().deployment_enabled = True
    with pytest.raises(FrozenInstanceError):
        configuration().runtime.execution_enabled = True
    with pytest.raises(FrozenInstanceError):
        bundle().digest.value = "changed"


def test_repository_bundle_round_trips_deterministically():
    parsed = bundle_from_json(BUNDLE_PATH.read_text(encoding="utf-8"))
    assert parsed == generated_bundle(DeploymentProfileName.REPOSITORY_ONLY)
    assert bundle_to_json(parsed) == bundle_to_json(bundle_from_json(bundle_to_json(parsed)))


@pytest.mark.parametrize("profile", list(DeploymentProfileName))
def test_every_profile_is_descriptive_and_non_executable(profile):
    item = deployment_profile(profile)
    assert not validate_profile(item)
    assert item.deployment_enabled is False
    assert item.execution_enabled is False
    configured = generated_bundle(profile)
    assert not validate_bundle(configured)
    assert configured.configuration.deployment_enabled is False
    assert configured.configuration.runtime.execution_enabled is False


def test_future_production_profile_models_requirements_without_authentication_or_deployment():
    active = generated_bundle(DeploymentProfileName.FUTURE_PRODUCTION).configuration
    assert active.identity.authentication_mode == DeploymentAuthenticationMode.FUTURE_MUTUAL_TLS
    assert "future_mutual_authentication" in active.identity.future_transport_requirements
    assert active.identity.fixture_only is True
    assert active.runtime.security.certificate_loading_allowed is False
    assert active.deployment_enabled is False


def test_profile_and_descriptive_authentication_mode_must_remain_compatible():
    active = generated_bundle(DeploymentProfileName.FUTURE_PRODUCTION).configuration
    changed = replace(active, identity=replace(active.identity, authentication_mode=DeploymentAuthenticationMode.SERVICE_IDENTITY))
    assert "configuration.profile_identity.incompatible" in codes(validate_configuration(changed))


def test_strict_json_rejects_duplicate_unknown_and_malformed_fixtures():
    with pytest.raises(Exception, match="Duplicate JSON field"):
        bundle_from_json(library().duplicate_text())
    with pytest.raises(Exception, match="unknown or unsafe fields"):
        bundle_from_json(library().unknown_text())
    with pytest.raises(Exception, match="not valid JSON"):
        bundle_from_json(library().malformed_text())


def test_strict_parser_rejects_missing_and_nested_unknown_fields():
    payload = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    del payload["configuration"]["audit"]
    with pytest.raises(Exception, match="missing required fields"):
        configuration_from_dict(payload["configuration"])
    payload = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    payload["configuration"]["runtime"]["environment"] = {}
    with pytest.raises(Exception, match="unknown or unsafe fields"):
        configuration_from_dict(payload["configuration"])


@pytest.mark.parametrize("version", ["1.1", "2.0", "9.0"])
def test_future_contract_versions_fail_closed(version):
    payload = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    payload["contract_version"] = version
    with pytest.raises(Exception, match="unsupported version"):
        bundle_from_json(json.dumps(payload))


def test_oversized_configuration_fails_before_parsing():
    with pytest.raises(Exception, match="maximum configuration size"):
        load_json(" " * 131_073)


def test_configuration_digest_is_canonical_stable_and_comparable():
    active = configuration()
    first = configuration_digest(active)
    second = configuration_digest(active)
    assert first == second == bundle().digest
    assert first.algorithm == "sha256"
    assert first.value.startswith("sha256:") and len(first.value) == 71
    changed = replace(active, profile=replace(active.profile, description="changed"))
    assert configuration_digest(changed) != first


def test_bundle_digest_mismatch_fails_closed():
    invalid = replace(bundle(), digest=ConfigurationDigest(CONTRACT_VERSION, DIGEST_VERSION, "sha256", "sha256:" + "0" * 64))
    assert "bundle.digest.mismatch" in codes(validate_bundle(invalid))


def test_runtime_security_contract_requires_all_hardening_controls():
    security = configuration().runtime.security
    assert not validate_security(security)
    assert security.non_root_required
    assert security.read_only_filesystem_required
    assert security.dropped_capabilities == ("ALL",)
    assert security.seccomp_required and security.apparmor_required
    assert security.independent_disablement_required
    assert not security.privilege_escalation_allowed
    assert not security.credential_loading_allowed
    assert not security.certificate_loading_allowed


@pytest.mark.parametrize(
    "change,code",
    [
        ({"non_root_required": False}, "security.least_privilege.required"),
        ({"read_only_filesystem_required": False}, "security.least_privilege.required"),
        ({"dropped_capabilities": ()}, "security.least_privilege.required"),
        ({"seccomp_required": False}, "security.controls.required"),
        ({"apparmor_required": False}, "security.controls.required"),
        ({"independent_disablement_required": False}, "security.controls.required"),
        ({"privilege_escalation_allowed": True}, "security.privileged_loading.prohibited"),
        ({"credential_loading_allowed": True}, "security.privileged_loading.prohibited"),
        ({"certificate_loading_allowed": True}, "security.privileged_loading.prohibited"),
    ],
)
def test_runtime_security_drift_fails_closed(change, code):
    assert code in codes(validate_security(replace(configuration().runtime.security, **change)))


@pytest.mark.parametrize(
    "field,value,code",
    [
        ("memory_limit_bytes", 0, "resources.bounds.invalid"),
        ("cpu_limit_millicores", 1001, "resources.bounds.excessive"),
        ("process_limit", 257, "resources.bounds.excessive"),
        ("concurrency_limit", 0, "resources.bounds.invalid"),
        ("request_timeout_seconds", 61, "resources.bounds.excessive"),
        ("shutdown_timeout_seconds", 61, "resources.bounds.excessive"),
    ],
)
def test_resource_limits_are_positive_and_bounded(field, value, code):
    limits = replace(configuration().runtime.resource_limits, **{field: value})
    assert code in codes(validate_resource_limits(limits))


def test_runtime_remains_non_executable_and_non_deployable():
    runtime = configuration().runtime
    assert not validate_runtime(runtime)
    for field in ("execution_enabled", "runtime_access_enabled", "deployment_enabled"):
        assert "runtime.execution.prohibited" in codes(validate_runtime(replace(runtime, **{field: True})))


def test_service_identity_is_exact_synthetic_and_time_bounded():
    identity = configuration().identity
    assert not validate_identity(identity)
    assert identity.approval_reference.startswith("FIXTURE-APPROVAL-")
    assert identity.fixture_only
    assert identity.identity_scope == "synthetic_repository_fixture"


@pytest.mark.parametrize(
    "change,code",
    [
        ({"service_identity": "*"}, "identity.service_identity.invalid"),
        ({"deployment_id": ""}, "identity.deployment_id.invalid"),
        ({"approval_reference": "REAL-APPROVAL"}, "identity.approval.fixture_required"),
        ({"valid_until": "2026-07-22T10:00:00Z"}, "identity.window.invalid"),
        ({"fixture_only": False}, "identity.fixture_scope.required"),
    ],
)
def test_service_identity_drift_fails_closed(change, code):
    assert code in codes(validate_identity(replace(configuration().identity, **change)))


def test_endpoint_policy_matches_published_proxy_contract_exactly():
    policy = configuration().endpoint_policy
    expected = repository_endpoint_policy()
    assert policy == expected
    assert not validate_endpoint_policy(policy)
    assert policy.proxy_policy_version == POLICY_VERSION
    assert policy.proxy_policy_digest == repository_policy().policy_digest
    assert {item.endpoint_category for item in policy.category_policy} == set(ProxyEndpointCategory)
    assert policy.future_categories == (ProxyEndpointCategory.EVENTS,)
    assert all(item.allowed_methods in {(), (ProxyMethodCategory.READ_ONLY,)} for item in policy.category_policy)


@pytest.mark.parametrize(
    "change,code",
    [
        ({"proxy_policy_digest": "sha256:" + "0" * 64}, "endpoint_policy.digest.mismatch"),
        ({"maximum_request_payload_bytes": 1}, "endpoint_policy.bounds.mismatch"),
        ({"allowed_signals": ()}, "endpoint_policy.signals.invalid"),
        ({"allowed_signals": ("container.unapproved.signal",)}, "endpoint_policy.signals.invalid"),
    ],
)
def test_endpoint_policy_drift_fails_closed(change, code):
    assert code in codes(validate_endpoint_policy(replace(configuration().endpoint_policy, **change)))


def test_proxy_and_adapter_configuration_are_version_bound_and_disabled():
    proxy = configuration().proxy
    adapter = configuration().adapter
    assert not validate_proxy(proxy)
    assert not validate_adapter(adapter)
    assert proxy.proxy_version == PROXY_VERSION
    assert proxy.proxy_configuration_version == PROXY_CONFIGURATION_VERSION
    assert not proxy.socket_access_enabled and not proxy.network_access_enabled and not proxy.listener_enabled and not proxy.runtime_access_enabled
    assert adapter.adapter_version == ADAPTER_VERSION
    assert not adapter.live_provider_enabled and not adapter.named_target_enabled and adapter.fixture_only


@pytest.mark.parametrize("field", ["socket_access_enabled", "network_access_enabled", "listener_enabled", "runtime_access_enabled"])
def test_proxy_runtime_capabilities_cannot_be_enabled(field):
    assert "proxy.runtime_capability.prohibited" in codes(validate_proxy(replace(configuration().proxy, **{field: True})))


def test_audit_configuration_is_secret_safe_and_fixture_bounded():
    audit = configuration().audit
    assert not validate_audit(audit)
    assert audit.secret_redaction_required
    assert not audit.request_payload_logging_allowed
    assert not audit.response_payload_logging_allowed
    assert audit.destination_reference.startswith(f"{FIXTURE_ROOT}/")


def test_compatibility_validation_and_version_negotiation_are_deterministic():
    active = configuration()
    assert not validate_compatibility(active.compatibility)
    first = negotiate_versions(active)
    second = negotiate_versions(active)
    assert first == second
    assert first["compatible"] is True
    assert first["proxy_version"] == PROXY_VERSION
    incompatible = replace(active, compatibility=replace(active.compatibility, adapter_version="unsupported"))
    assert "compatibility.version.incompatible" in codes(validate_compatibility(incompatible.compatibility))
    assert negotiate_versions(incompatible)["compatible"] is False


@pytest.mark.parametrize(
    "scenario,expected_code",
    [
        ("incompatible_versions", "compatibility.version.incompatible"),
        ("invalid_identity", "identity.service_identity.invalid"),
        ("missing_policy", "endpoint_policy.required"),
        ("missing_audit", "audit.required"),
        ("missing_limits", "resources.required"),
        ("wildcard_identity", "identity.service_identity.invalid"),
        ("invalid_resource_limits", "resources.bounds.invalid"),
        ("unsupported_versions", "configuration.version.unsupported"),
        ("digest_mismatch", "bundle.digest.mismatch"),
        ("runtime_enabled", "runtime.execution.prohibited"),
        ("socket_enabled", "proxy.runtime_capability.prohibited"),
    ],
)
def test_negative_fixture_scenarios_fail_closed_deterministically(scenario, expected_code):
    first = library().validate_scenario(scenario)
    second = library().validate_scenario(scenario)
    assert first == second
    assert expected_code in codes(first)


@pytest.mark.parametrize(
    "scenario",
    ["valid_repository_profile", "valid_future_development_profile", "valid_future_validation_profile", "valid_future_production_profile"],
)
def test_positive_fixture_scenarios_validate_deterministically(scenario):
    assert not library().validate_scenario(scenario)
    assert library().bundle_for_scenario(scenario) == library().bundle_for_scenario(scenario)


def test_fixture_catalog_expected_validity_matches_validation():
    for scenario in library().scenario_ids():
        expected = library().scenario(scenario)["expected_valid"]
        assert (not library().validate_scenario(scenario)) is expected


def test_contract_summary_explicitly_blocks_every_live_gate():
    summary = contract_summary()
    assert summary["repository_only"] is True
    assert summary["deployment"] == "disabled"
    assert summary["execution"] == "disabled"
    assert summary["networking"] == "absent"
    assert summary["socket_access"] == "absent"
    assert summary["credential_loading"] == "prohibited"
    assert summary["certificate_loading"] == "prohibited"
    assert summary["named_target_authorization"] == "not_authorized"
    assert summary["activation_status"] == ACTIVATION_STATUS


def test_deployment_modules_have_no_execution_network_socket_credential_certificate_or_environment_capability():
    module_paths = [
        ROOT / "engineering/platform_eap/deployment_configuration.py",
        ROOT / "engineering/platform_eap/deployment_configuration_io.py",
        ROOT / "engineering/platform_eap/deployment_configuration_fixtures.py",
    ]
    forbidden_imports = {"aiohttp", "asyncio", "cryptography", "docker", "http", "os", "paramiko", "pty", "random", "requests", "socket", "ssl", "subprocess", "urllib"}
    forbidden_calls = {"connect", "create_connection", "getenv", "Popen", "run", "system", "spawn"}
    forbidden_text = ("DOCKER_HOST", "/var/run/", "http://", "https://", "BEGIN CERTIFICATE", "BEGIN PRIVATE KEY", "/containers/")
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
            node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, (ast.Attribute, ast.Name))
        }
        assert not forbidden_imports.intersection(imports)
        assert not forbidden_calls.intersection(calls)
        assert not any(value in source for value in forbidden_text)


@pytest.mark.parametrize(
    "command",
    [
        ["deployment", "contract"],
        ["deployment", "validate"],
        ["deployment", "fixtures"],
        ["deployment", "digest", "RepositoryOnly"],
        ["deployment", "profile", "FutureDevelopment"],
        ["deployment", "compatibility", "FutureProduction"],
        ["deployment", "identity", "RepositoryOnly"],
        ["deployment", "runtime", "RepositoryOnly"],
        ["deployment", "security", "RepositoryOnly"],
        ["deployment", "bundle", "RepositoryOnly"],
    ],
)
def test_deployment_cli_repository_commands_succeed(command, capsys):
    assert cli.main(command) == 0
    assert capsys.readouterr().out


def test_deployment_cli_negative_scenario_returns_findings(capsys):
    assert cli.main(["deployment", "validate", "socket_enabled"]) == 2
    output = capsys.readouterr().out
    assert "Status: FAIL" in output
    assert "proxy.runtime_capability.prohibited" in output


def test_deployment_cli_has_no_live_or_apply_mode(capsys):
    assert cli.main(["deployment", "apply"]) == 2
    assert "Usage:" in capsys.readouterr().out
    assert cli.main(["deployment", "live"]) == 2
    assert "Usage:" in capsys.readouterr().out


def test_capability_inventory_records_configuration_without_deployment(capsys):
    assert cli.main(["capabilities"]) == 0
    output = capsys.readouterr().out
    assert "PLAT-EAP-15" in output
    assert "No Deployment" in output


def test_fixture_library_rejects_traversal():
    with pytest.raises(Exception, match="unsafe"):
        library()._path("../repository-only-bundle.json")


def test_fixtures_contain_no_authoritative_registry_or_live_target_reference():
    for path in FIXTURES.iterdir():
        text = path.read_text(encoding="utf-8")
        assert "registry/records/" not in text
        assert "svc-pihole" not in text
        assert "192.168." not in text
