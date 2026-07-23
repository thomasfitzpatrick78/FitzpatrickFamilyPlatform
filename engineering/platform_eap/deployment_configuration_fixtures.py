from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Mapping

from engineering.platform_eap.deployment_configuration import (
    FIXTURE_ROOT,
    MAX_CONFIGURATION_BYTES,
    ConfigurationBundle,
    DeploymentConfigurationDataError,
    DeploymentProfileName,
    bundle_for,
    repository_configuration,
    validate_bundle,
)
from engineering.platform_eap.deployment_configuration_io import bundle_from_json, load_json


CATALOG_FILE = "deployment-fixtures.json"
PROFILE_FILES = {DeploymentProfileName.REPOSITORY_ONLY: "repository-only-bundle.json"}


class RepositoryDeploymentFixtureLibrary:
    """Reads governed deployment-description fixtures without deployment capability."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve()
        self.fixture_root = (self.repository_root / FIXTURE_ROOT).resolve()
        if self.fixture_root != (self.repository_root / FIXTURE_ROOT).resolve() or not self.fixture_root.is_dir() or self.fixture_root.is_symlink():
            raise DeploymentConfigurationDataError("Deployment fixture library requires the governed repository fixture root.")

    def _path(self, name: str) -> Path:
        if not name or "/" in name or "\\" in name or name.startswith("."):
            raise DeploymentConfigurationDataError("Deployment fixture name is unsafe.")
        candidate = (self.fixture_root / name).resolve()
        if not candidate.is_relative_to(self.fixture_root) or not candidate.is_file() or candidate.is_symlink():
            raise DeploymentConfigurationDataError(f"Deployment fixture file not found or unsafe: {name}.")
        return candidate

    def _read(self, name: str) -> str:
        path = self._path(name)
        if path.stat().st_size > MAX_CONFIGURATION_BYTES:
            raise DeploymentConfigurationDataError("Deployment fixture exceeds the maximum configuration size.")
        return path.read_text(encoding="utf-8")

    def catalog(self) -> Mapping[str, object]:
        payload = load_json(self._read(CATALOG_FILE), "deployment fixture catalog")
        if not isinstance(payload, Mapping):
            raise DeploymentConfigurationDataError("Deployment fixture catalog must be an object.")
        fields = {"catalog_version", "contract_version", "fixture_only", "deployment_enabled", "scenarios"}
        if set(payload) != fields or payload["catalog_version"] != "1.0" or payload["contract_version"] != "1.0" or payload["fixture_only"] is not True or payload["deployment_enabled"] is not False:
            raise DeploymentConfigurationDataError("Deployment fixture catalog scope or version is invalid.")
        scenarios = payload["scenarios"]
        if not isinstance(scenarios, list) or not scenarios:
            raise DeploymentConfigurationDataError("Deployment fixture catalog requires scenarios.")
        identifiers = [item.get("scenario_id") for item in scenarios if isinstance(item, Mapping)]
        if len(identifiers) != len(scenarios) or len(identifiers) != len(set(identifiers)) or any(not isinstance(item, str) for item in identifiers):
            raise DeploymentConfigurationDataError("Deployment scenario identifiers must be unique strings.")
        return payload

    def scenario_ids(self) -> tuple[str, ...]:
        scenarios = self.catalog()["scenarios"]
        assert isinstance(scenarios, list)
        return tuple(sorted(str(item["scenario_id"]) for item in scenarios if isinstance(item, Mapping)))

    def scenario(self, scenario_id: str) -> Mapping[str, object]:
        scenarios = self.catalog()["scenarios"]
        assert isinstance(scenarios, list)
        matches = [item for item in scenarios if isinstance(item, Mapping) and item.get("scenario_id") == scenario_id]
        if len(matches) != 1:
            raise DeploymentConfigurationDataError(f"Deployment scenario is missing or ambiguous: {scenario_id}.")
        fields = {"scenario_id", "profile", "mutation", "expected_valid"}
        if set(matches[0]) != fields:
            raise DeploymentConfigurationDataError("Deployment scenario contains missing or unknown fields.")
        return matches[0]

    def bundle_for_profile(self, profile: DeploymentProfileName) -> ConfigurationBundle:
        if profile == DeploymentProfileName.REPOSITORY_ONLY:
            return bundle_from_json(self._read(PROFILE_FILES[profile]))
        return generated_bundle(profile)

    def malformed_text(self) -> str:
        return self._read("malformed-configuration.json")

    def duplicate_text(self) -> str:
        return self._read("duplicate-field-configuration.json")

    def unknown_text(self) -> str:
        return self._read("unknown-field-configuration.json")

    def bundle_for_scenario(self, scenario_id: str) -> ConfigurationBundle:
        scenario = self.scenario(scenario_id)
        profile = DeploymentProfileName(str(scenario["profile"]))
        bundle = self.bundle_for_profile(profile)
        configuration = bundle.configuration
        mutation = str(scenario["mutation"])
        if mutation == "incompatible_versions":
            compatibility = replace(configuration.compatibility, proxy_version="unsupported-proxy")
            configuration = replace(configuration, compatibility=compatibility)
        elif mutation == "invalid_identity":
            configuration = replace(configuration, identity=replace(configuration.identity, service_identity=""))
        elif mutation == "missing_policy":
            configuration = replace(configuration, endpoint_policy=None)
        elif mutation == "missing_audit":
            configuration = replace(configuration, audit=None)
        elif mutation == "missing_limits":
            configuration = replace(configuration, runtime=replace(configuration.runtime, resource_limits=None))
        elif mutation == "wildcard_identity":
            configuration = replace(configuration, identity=replace(configuration.identity, service_identity="*"))
        elif mutation == "invalid_resource_limits":
            limits = configuration.runtime.resource_limits
            assert limits is not None
            configuration = replace(configuration, runtime=replace(configuration.runtime, resource_limits=replace(limits, concurrency_limit=0)))
        elif mutation == "unsupported_versions":
            configuration = replace(configuration, configuration_version="unsupported-deployment-configuration")
        elif mutation == "runtime_enabled":
            configuration = replace(configuration, runtime=replace(configuration.runtime, execution_enabled=True))
        elif mutation == "socket_enabled":
            configuration = replace(configuration, proxy=replace(configuration.proxy, socket_access_enabled=True))
        updated = bundle_for(configuration)
        if mutation == "digest_mismatch":
            updated = replace(updated, digest=replace(updated.digest, value="sha256:" + "0" * 64))
        return updated

    def validate_scenario(self, scenario_id: str):
        return validate_bundle(self.bundle_for_scenario(scenario_id))


def generated_bundle(profile: DeploymentProfileName) -> ConfigurationBundle:
    """Returns the canonical in-memory fixture bundle for artifact generation tests."""

    return bundle_for(repository_configuration(profile))
