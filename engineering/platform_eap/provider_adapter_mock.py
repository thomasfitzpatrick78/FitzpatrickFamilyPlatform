from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Mapping

from engineering.platform_eap.container_health import CollectionMethod
from engineering.platform_eap.execution_capability import contains_secret_like_content
from engineering.platform_eap.provider_adapter import (
    ACCEPTED_CONTENT_TYPES,
    ACTIVATION_STATUS,
    ADAPTER_VERSION,
    CAPABILITY_VERSION,
    CONTRACT_VERSION,
    FIXTURE_CATALOG_VERSION,
    FIXTURE_ROOT,
    MAX_PAYLOAD_BYTES,
    CoverageStatus,
    FindingSeverity,
    MockScenario,
    NormalizedSignal,
    ObservationMetadata,
    ObservedIdentity,
    ProductionProviderAdapter,
    ProviderAdapterDataError,
    ProviderConfidence,
    ProviderCoverage,
    ProviderFinding,
    ProviderLimitation,
    ProviderNormalizationResult,
    ProviderProvenance,
    ProviderRequest,
    ProviderResponse,
    ProviderResult,
    TargetResolution,
    failure_for_scenario,
    normalize_response,
    repository_adapter_identity,
    repository_capability,
    validate_adapter_identity,
    validate_capability,
    validate_request,
)
from engineering.platform_eap.provider_adapter_io import load_json


CATALOG_REFERENCE = f"{FIXTURE_ROOT}/provider-fixtures.json"
MALFORMED_REFERENCE = f"{FIXTURE_ROOT}/malformed-provider-response.json"


def _strict_keys(payload: Mapping[str, object], required: set[str], context: str) -> None:
    missing = sorted(required - payload.keys())
    unknown = sorted(payload.keys() - required)
    if missing or unknown:
        raise ProviderAdapterDataError(f"{context} fields invalid; missing={missing}, unknown={unknown}.")


def _strings(value: object, context: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ProviderAdapterDataError(f"{context} must be an array of strings.")
    return tuple(value)


def _optional_string(value: object, context: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ProviderAdapterDataError(f"{context} must be a string or null.")
    return value


class RepositoryFixtureClient:
    """Reads only governed synthetic provider fixtures from the repository."""

    def __init__(self, repository_root: Path, fixture_root: Path | None = None) -> None:
        self.repository_root = repository_root.resolve()
        self.fixture_root = (fixture_root or (self.repository_root / FIXTURE_ROOT)).resolve()
        expected = (self.repository_root / FIXTURE_ROOT).resolve()
        if self.fixture_root != expected or not self.fixture_root.is_dir() or self.fixture_root.is_symlink():
            raise ProviderAdapterDataError("Provider fixture client requires the governed repository fixture root.")

    def _fixture_path(self, name: str) -> Path:
        if not name or "/" in name or "\\" in name or name.startswith("."):
            raise ProviderAdapterDataError("Provider fixture name is unsafe.")
        candidate = (self.fixture_root / name).resolve()
        if not candidate.is_relative_to(self.fixture_root) or not candidate.is_file() or candidate.is_symlink():
            raise ProviderAdapterDataError(f"Provider fixture file not found or unsafe: {name}.")
        return candidate

    def _read(self, name: str) -> str:
        path = self._fixture_path(name)
        if path.stat().st_size > MAX_PAYLOAD_BYTES:
            raise ProviderAdapterDataError("Provider fixture exceeds the maximum payload size.")
        text = path.read_text(encoding="utf-8")
        if contains_secret_like_content(text):
            raise ProviderAdapterDataError("Provider fixture contains secret-like content.")
        return text

    def fixture_names(self) -> tuple[str, ...]:
        catalog = self._catalog()
        fixtures = catalog["fixtures"]
        assert isinstance(fixtures, list)
        return tuple(sorted(str(item["fixture_id"]) for item in fixtures if isinstance(item, Mapping)))

    def malformed_text(self) -> str:
        return self._read("malformed-provider-response.json")

    def _catalog(self) -> Mapping[str, object]:
        text = self._read("provider-fixtures.json")
        payload = load_json(text, "provider fixture catalog", MAX_PAYLOAD_BYTES)
        if not isinstance(payload, Mapping):
            raise ProviderAdapterDataError("Provider fixture catalog must be a JSON object.")
        fields = {"catalog_version", "fixture_only", "activation_status", "content_type", "provider", "defaults", "fixtures"}
        _strict_keys(payload, fields, "provider fixture catalog")
        if payload["catalog_version"] != FIXTURE_CATALOG_VERSION or payload["fixture_only"] is not True or payload["activation_status"] != ACTIVATION_STATUS:
            raise ProviderAdapterDataError("Provider fixture catalog version or repository scope is invalid.")
        if payload["content_type"] not in ACCEPTED_CONTENT_TYPES:
            raise ProviderAdapterDataError("Provider fixture catalog content type is unsupported.")
        fixtures = payload["fixtures"]
        if not isinstance(fixtures, list) or not fixtures:
            raise ProviderAdapterDataError("Provider fixture catalog requires a nonempty fixtures array.")
        identifiers = [item.get("fixture_id") for item in fixtures if isinstance(item, Mapping)]
        if len(identifiers) != len(fixtures) or len(identifiers) != len(set(identifiers)):
            raise ProviderAdapterDataError("Provider fixture identifiers must be unique strings.")
        return payload

    def response(self, fixture_id: str, request: ProviderRequest) -> ProviderResponse:
        catalog = self._catalog()
        provider = catalog["provider"]
        defaults = catalog["defaults"]
        fixtures = catalog["fixtures"]
        if not isinstance(provider, Mapping) or not isinstance(defaults, Mapping) or not isinstance(fixtures, list):
            raise ProviderAdapterDataError("Provider fixture catalog provider/default structures are invalid.")
        _strict_keys(provider, {"provider_type", "provider_id", "provider_version"}, "provider fixture catalog provider")
        _strict_keys(defaults, {"collection_started_at", "collection_ended_at", "observed_at", "identity"}, "provider fixture catalog defaults")
        matches = [item for item in fixtures if isinstance(item, Mapping) and item.get("fixture_id") == fixture_id]
        if len(matches) != 1:
            raise ProviderAdapterDataError(f"Provider fixture identifier is missing or ambiguous: {fixture_id}.")
        case = matches[0]
        fields = {"fixture_id", "target_resolution_result", "provider_version", "coverage_status", "identity", "signals", "limitations", "warnings", "unknown_signals"}
        _strict_keys(case, fields, f"provider fixture {fixture_id}")
        base_identity = defaults["identity"]
        override_identity = case["identity"]
        if not isinstance(base_identity, Mapping) or not isinstance(override_identity, Mapping):
            raise ProviderAdapterDataError(f"Provider fixture identity is invalid: {fixture_id}.")
        identity_fields = {"runtime_container_id", "runtime_name", "compose_project", "compose_service", "image_reference", "image_digest", "host_reference", "runtime_engine", "orchestrator"}
        _strict_keys(base_identity, identity_fields, "provider fixture default identity")
        if any(key not in identity_fields for key in override_identity):
            raise ProviderAdapterDataError(f"Provider fixture identity contains unknown fields: {fixture_id}.")
        merged_identity = {**base_identity, **override_identity}
        signals_value = case["signals"]
        limitations_value = case["limitations"]
        if not isinstance(signals_value, list) or not isinstance(limitations_value, list):
            raise ProviderAdapterDataError(f"Provider fixture signals or limitations are invalid: {fixture_id}.")
        signals: list[NormalizedSignal] = []
        signal_fields = {"signal_name", "value", "value_type", "unit", "observation_window_start", "observation_window_end", "collection_method"}
        for index, value in enumerate(signals_value):
            if not isinstance(value, Mapping):
                raise ProviderAdapterDataError(f"Provider fixture signal must be an object: {fixture_id}[{index}].")
            _strict_keys(value, signal_fields, f"provider fixture signal {fixture_id}[{index}]")
            scalar = value["value"]
            if not isinstance(scalar, (str, int, float, bool)):
                raise ProviderAdapterDataError(f"Provider fixture signal value must be scalar: {fixture_id}[{index}].")
            try:
                method = CollectionMethod(str(value["collection_method"]))
            except ValueError as exc:
                raise ProviderAdapterDataError(f"Provider fixture collection method is unsupported: {fixture_id}[{index}].") from exc
            signals.append(
                NormalizedSignal(
                    str(value["signal_name"]),
                    scalar,
                    str(value["value_type"]),
                    _optional_string(value["unit"], "provider fixture signal unit"),
                    str(defaults["observed_at"]),
                    _optional_string(value["observation_window_start"], "provider fixture signal window start"),
                    _optional_string(value["observation_window_end"], "provider fixture signal window end"),
                    method,
                )
            )
        limitations: list[ProviderLimitation] = []
        for index, value in enumerate(limitations_value):
            if not isinstance(value, Mapping):
                raise ProviderAdapterDataError(f"Provider fixture limitation must be an object: {fixture_id}[{index}].")
            _strict_keys(value, {"limitation_code", "affected_signals", "material", "safe_reference"}, f"provider fixture limitation {fixture_id}[{index}]")
            if not isinstance(value["material"], bool):
                raise ProviderAdapterDataError(f"Provider fixture limitation material must be boolean: {fixture_id}[{index}].")
            limitations.append(
                ProviderLimitation(
                    str(value["limitation_code"]),
                    _strings(value["affected_signals"], "provider fixture limitation affected_signals"),
                    value["material"],
                    str(value["safe_reference"]),
                )
            )
        returned = tuple(sorted(signal.signal_name for signal in signals))
        requested = request.requested_signals()
        missing = tuple(sorted(set(requested).difference(returned)))
        unknown = tuple(sorted(_strings(case["unknown_signals"], f"provider fixture {fixture_id} unknown_signals")))
        warnings = tuple(sorted(_strings(case["warnings"], f"provider fixture {fixture_id} warnings")))
        raw_digest = "sha256:" + hashlib.sha256(json.dumps(case, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        material = any(limitation.material for limitation in limitations)
        try:
            coverage_status = CoverageStatus(str(case["coverage_status"]))
            resolution = TargetResolution(str(case["target_resolution_result"]))
        except ValueError as exc:
            raise ProviderAdapterDataError(f"Provider fixture coverage or target-resolution value is unsupported: {fixture_id}.") from exc
        if resolution == TargetResolution.EXACT and coverage_status == CoverageStatus.COMPLETE and not material:
            confidence = ProviderConfidence.HIGH
            reasons = ("COMPLETE_COVERAGE", "DIRECT_FIXTURE_OBSERVATION", "EXACT_IDENTITY")
        elif resolution == TargetResolution.EXACT and returned:
            confidence = ProviderConfidence.LOW
            reasons = ("PARTIAL_OR_LIMITED_FIXTURE_EVIDENCE",)
        else:
            confidence = ProviderConfidence.NONE
            reasons = ("IDENTITY_OR_PROVIDER_EVIDENCE_UNUSABLE",)
        identifier_seed = {"fixture": fixture_id, "request": request.request_id}
        identifier = hashlib.sha256(json.dumps(identifier_seed, sort_keys=True).encode("utf-8")).hexdigest()[:16]
        return ProviderResponse(
            CONTRACT_VERSION,
            ObservationMetadata(
                f"provider-observation-{identifier}",
                f"provider-correlation-{identifier}",
                str(defaults["collection_started_at"]),
                str(defaults["collection_ended_at"]),
                str(defaults["observed_at"]),
                None,
                None,
            ),
            ObservedIdentity(
                resolution,
                _optional_string(merged_identity["runtime_container_id"], "provider fixture identity runtime_container_id"),
                _optional_string(merged_identity["runtime_name"], "provider fixture identity runtime_name"),
                _optional_string(merged_identity["compose_project"], "provider fixture identity compose_project"),
                _optional_string(merged_identity["compose_service"], "provider fixture identity compose_service"),
                _optional_string(merged_identity["image_reference"], "provider fixture identity image_reference"),
                _optional_string(merged_identity["image_digest"], "provider fixture identity image_digest"),
                _optional_string(merged_identity["host_reference"], "provider fixture identity host_reference"),
                str(merged_identity["runtime_engine"]),
                _optional_string(merged_identity["orchestrator"], "provider fixture identity orchestrator"),
            ),
            ProviderProvenance(
                str(provider["provider_type"]),
                str(provider["provider_id"]),
                str(case["provider_version"]),
                repository_adapter_identity().adapter_id,
                ADAPTER_VERSION,
                CAPABILITY_VERSION,
                CATALOG_REFERENCE,
                raw_digest,
            ),
            ProviderCoverage(coverage_status, requested, returned, missing, unknown),
            tuple(limitations),
            confidence,
            tuple(sorted(reasons)),
            warnings,
            tuple(signals),
            True,
            ACTIVATION_STATUS,
        )


class MockProviderAdapter(ProductionProviderAdapter):
    def __init__(self, repository_root: Path, scenario: MockScenario = MockScenario.HEALTHY) -> None:
        self.client = RepositoryFixtureClient(repository_root)
        self.scenario = scenario
        self._initialized = False

    def initialize(self) -> tuple[ProviderFinding, ...]:
        self._initialized = True
        return (ProviderFinding(FindingSeverity.INFO, "mock.initialized", "Repository mock provider initialized without networking or live access."),)

    def validate_configuration(self) -> tuple[ProviderFinding, ...]:
        return tuple((*validate_adapter_identity(repository_adapter_identity()), *validate_capability(repository_capability())))

    def validate_authorization(self, request: ProviderRequest) -> tuple[ProviderFinding, ...]:
        return validate_request(request)

    def discover_capabilities(self):
        return repository_capability()

    def _fixture_for_scenario(self) -> str | None:
        return {
            MockScenario.HEALTHY: "healthy_lifecycle",
            MockScenario.UNSUPPORTED_PROVIDER_VERSION: "unsupported_provider_version",
            MockScenario.PARTIAL_RESPONSE: "healthcheck_missing",
            MockScenario.MISSING_MANDATORY_SIGNALS: "missing_lifecycle",
            MockScenario.CONFLICTING_IDENTITY: "conflicting_compose_labels",
            MockScenario.UNKNOWN_TARGET: "unknown_registry_target",
            MockScenario.DUPLICATE_TARGETS: "duplicate_runtime_names",
            MockScenario.PROVIDER_LIMITATION: "provider_limitation",
        }.get(self.scenario)

    def collect_observation(self, request: ProviderRequest) -> ProviderResult:
        request_findings = validate_request(request)
        if any(finding.severity == FindingSeverity.ERROR for finding in request_findings):
            return ProviderResult(CONTRACT_VERSION, None, failure_for_scenario(request, MockScenario.AUTHORIZATION_DENIED))
        if self.scenario == MockScenario.MALFORMED_PAYLOAD:
            try:
                load_json(self.client.malformed_text(), "malformed mock provider response", MAX_PAYLOAD_BYTES)
            except ProviderAdapterDataError:
                return ProviderResult(CONTRACT_VERSION, None, failure_for_scenario(request, self.scenario))
            raise ProviderAdapterDataError("Malformed provider fixture unexpectedly parsed successfully.")
        fixture_id = self._fixture_for_scenario()
        if fixture_id is None:
            return ProviderResult(CONTRACT_VERSION, None, failure_for_scenario(request, self.scenario))
        response = self.client.response(fixture_id, request)
        if self.scenario == MockScenario.UNSUPPORTED_PROVIDER_VERSION:
            return ProviderResult(CONTRACT_VERSION, None, failure_for_scenario(request, self.scenario))
        return ProviderResult(CONTRACT_VERSION, response, None)

    def collect_fixture(self, request: ProviderRequest, fixture_id: str) -> ProviderResult:
        request_findings = validate_request(request)
        if any(finding.severity == FindingSeverity.ERROR for finding in request_findings):
            return ProviderResult(CONTRACT_VERSION, None, failure_for_scenario(request, MockScenario.AUTHORIZATION_DENIED))
        return ProviderResult(CONTRACT_VERSION, self.client.response(fixture_id, request), None)

    def normalize(self, request: ProviderRequest, response: ProviderResponse) -> ProviderNormalizationResult:
        return normalize_response(request, response)

    def shutdown(self) -> tuple[ProviderFinding, ...]:
        self._initialized = False
        return (ProviderFinding(FindingSeverity.INFO, "mock.shutdown", "Repository mock provider shut down without networking or live access."),)
