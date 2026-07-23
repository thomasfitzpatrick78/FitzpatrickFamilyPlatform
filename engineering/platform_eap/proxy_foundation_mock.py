from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Mapping

from engineering.platform_eap.proxy_foundation import (
    CONTRACT_VERSION,
    FIXTURE_ROOT,
    MAX_REQUEST_PAYLOAD_BYTES,
    MAX_RESPONSE_PAYLOAD_BYTES,
    MockProxyResult,
    ProxyDataError,
    ProxyDecisionStatus,
    ProxyEndpointCategory,
    ProxyMethodCategory,
    ProxyPolicyState,
    ProxyRequest,
    ProxyResponse,
    ProxyResponseMetadata,
    ProxyResponseRecord,
    authorization_digest,
    decision_to_audit,
    decision_to_failure,
    evaluate_request,
    repository_capability,
    repository_configuration,
    repository_policy,
    validate_response,
)
from engineering.platform_eap.proxy_foundation_io import load_json, request_from_json, response_from_json


CATALOG_FILE = "proxy-fixtures.json"
REQUEST_FILE = "proxy-request.json"
RESPONSE_FILE = "proxy-response.json"


class RepositoryProxyFixtureLibrary:
    """Reads bounded synthetic proxy fixtures from one governed repository root."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve()
        self.fixture_root = (self.repository_root / FIXTURE_ROOT).resolve()
        expected = (self.repository_root / FIXTURE_ROOT).resolve()
        if self.fixture_root != expected or not self.fixture_root.is_dir() or self.fixture_root.is_symlink():
            raise ProxyDataError("Proxy fixture library requires the governed repository fixture root.")

    def _path(self, name: str) -> Path:
        if not name or "/" in name or "\\" in name or name.startswith("."):
            raise ProxyDataError("Proxy fixture name is unsafe.")
        candidate = (self.fixture_root / name).resolve()
        if not candidate.is_relative_to(self.fixture_root) or not candidate.is_file() or candidate.is_symlink():
            raise ProxyDataError(f"Proxy fixture file not found or unsafe: {name}.")
        return candidate

    def _read(self, name: str, maximum_bytes: int = MAX_RESPONSE_PAYLOAD_BYTES) -> str:
        path = self._path(name)
        if path.stat().st_size > maximum_bytes:
            raise ProxyDataError("Proxy fixture exceeds the governed maximum payload size.")
        return path.read_text(encoding="utf-8")

    def catalog(self) -> Mapping[str, object]:
        payload = load_json(self._read(CATALOG_FILE), "proxy fixture catalog", MAX_RESPONSE_PAYLOAD_BYTES)
        if not isinstance(payload, Mapping):
            raise ProxyDataError("Proxy fixture catalog must be a JSON object.")
        fields = {"catalog_version", "contract_version", "fixture_only", "activation_status", "scenarios"}
        if set(payload) != fields or payload["catalog_version"] != "1.0" or payload["contract_version"] != CONTRACT_VERSION or payload["fixture_only"] is not True or payload["activation_status"] != "not_activated":
            raise ProxyDataError("Proxy fixture catalog scope or version is invalid.")
        scenarios = payload["scenarios"]
        if not isinstance(scenarios, list) or not scenarios:
            raise ProxyDataError("Proxy fixture catalog scenarios must be a nonempty array.")
        identifiers = [item.get("scenario_id") for item in scenarios if isinstance(item, Mapping)]
        if len(identifiers) != len(scenarios) or len(identifiers) != len(set(identifiers)) or any(not isinstance(item, str) for item in identifiers):
            raise ProxyDataError("Proxy scenario identifiers must be unique strings.")
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
            raise ProxyDataError(f"Proxy scenario is missing or ambiguous: {scenario_id}.")
        scenario = matches[0]
        fields = {"scenario_id", "endpoint_category", "method_category", "mutation", "expected_decision"}
        if set(scenario) != fields:
            raise ProxyDataError("Proxy scenario contains missing or unknown fields.")
        return scenario

    def base_request(self) -> ProxyRequest:
        return request_from_json(self._read(REQUEST_FILE, MAX_REQUEST_PAYLOAD_BYTES))

    def base_response(self) -> ProxyResponse:
        return response_from_json(self._read(RESPONSE_FILE, MAX_RESPONSE_PAYLOAD_BYTES))

    def malformed_request_text(self) -> str:
        return self._read("malformed-proxy-request.json")

    def request_for(self, scenario_id: str) -> ProxyRequest:
        scenario = self.scenario(scenario_id)
        request = self.base_request()
        category = ProxyEndpointCategory(str(scenario["endpoint_category"]))
        method = ProxyMethodCategory(str(scenario["method_category"]))
        approved = tuple(sorted({*request.authorization.approved_endpoint_categories, category}, key=lambda item: item.value))
        authorization = replace(request.authorization, approved_endpoint_categories=approved, authorization_digest="")
        authorization = replace(authorization, authorization_digest=authorization_digest(authorization))
        request = replace(request, endpoint_category=category, method_category=method, authorization=authorization)
        mutation = str(scenario["mutation"])
        if mutation == "wildcard_target":
            target = replace(request.target, subject_id="*")
            authorization = replace(request.authorization, subject_id="*", authorization_digest="")
            authorization = replace(authorization, authorization_digest=authorization_digest(authorization))
            request = replace(request, target=target, authorization=authorization)
        elif mutation == "expired_authorization":
            authorization = replace(request.authorization, observation_window_end="2026-07-22T11:30:00Z", expires_at="2026-07-22T11:30:00Z", authorization_digest="")
            authorization = replace(authorization, authorization_digest=authorization_digest(authorization))
            request = replace(request, authorization=authorization)
        elif mutation == "duplicate_parameters":
            request = replace(request, parameters=(request.parameters[0], request.parameters[0]))
        elif mutation == "oversized_payload":
            request = replace(request, payload_size_bytes=MAX_REQUEST_PAYLOAD_BYTES + 1)
        elif mutation == "unsupported_version":
            request = replace(request, proxy_version="unsupported-proxy-version")
        elif mutation == "unauthenticated":
            request = replace(request, authentication=replace(request.authentication, authenticated=False))
        elif mutation == "authorization_digest_mismatch":
            request = replace(request, authorization=replace(request.authorization, authorization_digest="sha256:" + "0" * 64))
        elif mutation == "configuration_digest_mismatch":
            authorization = replace(request.authorization, configuration_digest="sha256:" + "1" * 64, authorization_digest="")
            authorization = replace(authorization, authorization_digest=authorization_digest(authorization))
            request = replace(request, authorization=authorization)
        return request

    def response_for(self, scenario_id: str, request: ProxyRequest) -> ProxyResponse:
        response = self.base_response()
        metadata = replace(
            response.metadata,
            request_id=request.request_id,
            target_subject_id=request.target.subject_id,
            registry_subject_reference=request.target.registry_subject_reference,
        )
        response = replace(response, metadata=metadata)
        mutation = str(self.scenario(scenario_id)["mutation"])
        if mutation == "response_too_large":
            response = replace(response, payload_size_bytes=MAX_RESPONSE_PAYLOAD_BYTES + 1)
        return response


class RepositoryMockProxy:
    """Evaluates contracts and returns fixture responses without transport capability."""

    def __init__(self, repository_root: Path) -> None:
        self.fixtures = RepositoryProxyFixtureLibrary(repository_root)

    def evaluate(self, scenario_id: str) -> MockProxyResult:
        request = self.fixtures.request_for(scenario_id)
        policy = repository_policy()
        configuration = repository_configuration()
        mutation = str(self.fixtures.scenario(scenario_id)["mutation"])
        if mutation == "invalid_policy":
            policy = replace(policy, default_state=ProxyPolicyState.ALLOWED)
        elif mutation == "invalid_configuration":
            configuration = replace(configuration, allow_networking=True)
        decision = evaluate_request(request, policy, configuration, repository_capability())
        response: ProxyResponse | None = None
        failure = None
        if decision.decision == ProxyDecisionStatus.ALLOWED:
            candidate = self.fixtures.response_for(scenario_id, request)
            response_findings = validate_response(candidate, request)
            if response_findings:
                decision = replace(
                    decision,
                    decision=ProxyDecisionStatus.RESPONSE_REJECTED,
                    decision_code="response_rejected",
                    safe_message="Synthetic fixture response failed closed validation.",
                )
                failure = decision_to_failure(request, decision)
            else:
                response = candidate
        else:
            failure = decision_to_failure(request, decision)
        audit = decision_to_audit(request, decision)
        return MockProxyResult(CONTRACT_VERSION, decision, response, failure, audit)
