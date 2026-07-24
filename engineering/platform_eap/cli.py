from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from engineering.platform_eap.ai_session_readiness import (
    AISessionReadinessValidator,
    NOT_READY,
    PASS as READINESS_PASS,
    write_readiness_report,
)
from engineering.platform_eap.execution_capability import (
    ExecutionDataError,
    FindingSeverity,
    validate_assignment,
    validate_completion_package,
)
from engineering.platform_eap.execution_io import assignment_from_json, completion_from_json
from engineering.platform_eap.execution_rendering import render_completion_markdown
from engineering.platform_eap.automation_capability import (
    build_automation_handoff,
    evaluate_transition,
    validate_automation_definition,
    validate_automation_run,
)
from engineering.platform_eap.automation_io import (
    AutomationDataError,
    definition_from_json,
    run_from_json,
    transition_decision_to_json,
    transition_from_json,
)
from engineering.platform_eap.automation_rendering import render_automation_handoff_markdown
from engineering.platform_eap.registry_identity import (
    MigrationDataError,
    SUPERSEDED_MIGRATION_PLAN_IDS,
    bind_migration_approval,
    build_migration_plan,
    build_migration_report,
    execute_migration,
    migration_evidence_catalog_from_json,
    migration_plan_from_json,
    migration_plan_to_json,
    render_migration_review,
    rollback_metadata_from_json,
    rollback_migration,
    schema_version_from,
    validate_completed_migration,
    validate_container_identity_contract,
)
from engineering.platform_eap.container_health import (
    ContainerHealthDataError,
    FindingSeverity as ContainerFindingSeverity,
    PolicyDataError,
    UnsupportedContractVersion,
    declared_subject_from_registry_contract,
    evaluate_bundle,
    load_policy_set,
    validate_assessment,
    validate_evidence,
)
from engineering.platform_eap.container_health_io import (
    assessment_from_json,
    assessment_to_json,
    bundle_from_json,
    evidence_from_json,
    reconciliation_to_json,
)
from engineering.platform_eap.container_health_rendering import render_assessment_markdown
from engineering.platform_eap.provider_adapter import (
    FindingSeverity as ProviderFindingSeverity,
    MockScenario,
    ProviderAdapterDataError,
    UnsupportedProviderContractVersion,
    repository_adapter_identity,
    repository_capability,
    validate_capability,
    validate_failure,
    validate_request,
    validate_response,
    validate_result,
)
from engineering.platform_eap.provider_adapter_io import (
    capability_from_json,
    capability_to_json,
    contract_summary_to_json,
    provider_failure_from_json,
    provider_normalization_result_from_json,
    provider_normalization_result_to_json,
    provider_request_from_json,
    provider_response_from_json,
    provider_result_from_json,
    provider_result_to_json,
)
from engineering.platform_eap.provider_adapter_mock import MockProviderAdapter, RepositoryFixtureClient
from engineering.platform_eap.proxy_foundation import (
    FindingSeverity as ProxyFindingSeverity,
    ProxyDataError,
    ProxyDecisionStatus,
    UnsupportedProxyContractVersion,
    contract_summary as proxy_contract_summary,
    repository_capability as repository_proxy_capability,
    repository_configuration as repository_proxy_configuration,
    repository_policy as repository_proxy_policy,
    validate_capability as validate_proxy_capability,
    validate_configuration as validate_proxy_configuration,
    validate_policy as validate_proxy_policy,
    validate_request as validate_proxy_request,
    validate_response as validate_proxy_response,
)
from engineering.platform_eap.proxy_foundation_io import (
    capability_from_json as proxy_capability_from_json,
    capability_to_json as proxy_capability_to_json,
    configuration_from_json as proxy_configuration_from_json,
    configuration_to_json as proxy_configuration_to_json,
    contract_summary_to_json as proxy_contract_summary_to_json,
    decision_to_json as proxy_decision_to_json,
    policy_from_json as proxy_policy_from_json,
    policy_to_json as proxy_policy_to_json,
    request_from_json as proxy_request_from_json,
    request_to_json as proxy_request_to_json,
    response_from_json as proxy_response_from_json,
    response_to_json as proxy_response_to_json,
    result_to_json as proxy_result_to_json,
)
from engineering.platform_eap.proxy_foundation_mock import RepositoryMockProxy, RepositoryProxyFixtureLibrary
from engineering.platform_eap.deployment_configuration import (
    DeploymentConfigurationDataError,
    DeploymentProfileName,
    FindingSeverity as DeploymentFindingSeverity,
    UnsupportedDeploymentConfigurationVersion,
    contract_summary as deployment_contract_summary,
    deterministic_json as deployment_json,
    negotiate_versions as negotiate_deployment_versions,
    validate_bundle as validate_deployment_bundle,
)
from engineering.platform_eap.deployment_configuration_io import contract_summary_to_json as deployment_contract_summary_to_json
from engineering.platform_eap.deployment_configuration_fixtures import RepositoryDeploymentFixtureLibrary
from engineering.platform_eap.privileged_proxy_source import (
    acceptance_summary as privileged_proxy_source_acceptance,
    contract_summary as privileged_proxy_source_contract,
    fixture_summary as privileged_proxy_source_fixtures,
    policy_summary as privileged_proxy_source_policy,
    supply_chain_summary as privileged_proxy_source_supply_chain,
    validate_source as validate_privileged_proxy_source,
)

ROOT = Path(__file__).resolve().parents[2]
REPORT_ROOT = ROOT / "reports" / "engineering"


@dataclass
class CheckResult:
    severity: str
    message: str
    path: str | None = None


@dataclass(frozen=True)
class AISessionReadinessMetric:
    status: str
    error_count: int | None
    warning_count: int | None
    domain_count: int | None
    generated_at: str | None
    evidence_status: str
    report_path: str
    evidence_usable: bool
    blocking_status: str
    interpretation: str
    caveat: str
    source_of_truth: str = "./platform-eap ai-session readiness"


@dataclass
class Report:
    capability: str
    status: str
    timestamp: str
    summary: str
    results: list[CheckResult]
    ai_session_readiness: AISessionReadinessMetric | None = None
    platform_health: dict[str, object] | None = None


def git_output(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"git unavailable: {exc}"


def write_report(name: str, report: Report) -> None:
    folder = REPORT_ROOT / name
    folder.mkdir(parents=True, exist_ok=True)
    md = folder / f"{name}_report.md"
    js = folder / f"{name}_report.json"
    errors = [r for r in report.results if r.severity == "ERROR"]
    warnings = [r for r in report.results if r.severity == "WARNING"]
    info = [r for r in report.results if r.severity == "INFO"]
    lines = [
        f"# Platform EAP Report - {report.capability}",
        "",
        f"**Status:** {report.status}",
        "",
        f"**Timestamp:** {report.timestamp}",
        "",
        f"**Summary:** {report.summary}",
        "",
        "## Counts",
        "",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        f"- Information: {len(info)}",
        "",
    ]
    if report.ai_session_readiness is not None:
        readiness = report.ai_session_readiness
        lines.extend(
            [
                "## AI Session Readiness",
                "",
                f"- Overall readiness: {readiness.status}",
                f"- Errors: {readiness.error_count if readiness.error_count is not None else 'unknown'}",
                f"- Warnings: {readiness.warning_count if readiness.warning_count is not None else 'unknown'}",
                f"- Validation domains: {readiness.domain_count if readiness.domain_count is not None else 'unknown'}",
                f"- Evidence timestamp: {readiness.generated_at or 'unavailable'}",
                f"- Evidence condition: {readiness.evidence_status}",
                f"- Evidence path: `{readiness.report_path}`",
                f"- Evidence usable: {'yes' if readiness.evidence_usable else 'no'}",
                f"- Onboarding effect: {readiness.blocking_status}",
                f"- Interpretation: {readiness.interpretation}",
                f"- Caveat: {readiness.caveat}",
                f"- Source of truth: `{readiness.source_of_truth}` and its governed Markdown and JSON reports.",
                "",
            ]
        )
    lines.extend(["## Results", ""])
    for result in report.results:
        suffix = f" (`{result.path}`)" if result.path else ""
        lines.append(f"- {result.severity}: {result.message}{suffix}")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    payload = asdict(report)
    for optional_section in ("ai_session_readiness", "platform_health"):
        if payload[optional_section] is None:
            payload.pop(optional_section)
    js.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def status_from(results: list[CheckResult]) -> str:
    if any(r.severity == "ERROR" for r in results):
        return "FAIL"
    if any(r.severity == "WARNING" for r in results):
        return "PASS WITH WARNINGS"
    return "PASS"


def validate_tracked_repository_artifacts() -> list[CheckResult]:
    tracked_output = git_output(["ls-files", "-z"])
    if tracked_output.startswith("git unavailable:"):
        return [CheckResult("ERROR", "Unable to inspect tracked repository content")]

    prohibited_names = {".DS_Store", "__pycache__", ".pytest_cache"}
    prohibited_paths = sorted(
        path
        for path in tracked_output.split("\0")
        if path and prohibited_names.intersection(Path(path).parts)
    )
    if prohibited_paths:
        return [
            CheckResult("ERROR", "Prohibited tracked repository artifact found", path)
            for path in prohibited_paths
        ]
    return [CheckResult("INFO", "No prohibited tracked repository artifacts detected")]



REGISTRY_ROOT = ROOT / "registry"
REGISTRY_SCHEMA = REGISTRY_ROOT / "schema" / "infrastructure_registry_schema.yaml"
REGISTRY_RECORDS = REGISTRY_ROOT / "records"
REGISTRY_MIGRATION_CATALOG = REGISTRY_ROOT / "migrations" / "container_identity" / "evidence_catalog.json"
REGISTRY_REQUIRED_FIELDS = {
    "id",
    "record_type",
    "name",
    "description",
    "owner",
    "location",
    "lifecycle_status",
    "health_status",
    "monitoring_ready",
    "dependencies",
}
REGISTRY_ALLOWED_TYPES = {
    "location",
    "owner",
    "physical_device",
    "network_device",
    "host",
    "service",
    "planned_service",
}
REGISTRY_ALLOWED_LIFECYCLE = {"planned", "active", "retired", "replacement"}
REGISTRY_ALLOWED_HEALTH = {"planned", "healthy", "degraded", "unmonitored", "unknown"}
REGISTRY_FORBIDDEN_SCOPE_TERMS = {"finance", "banking", "budgeting", "transaction", "investment"}
REGISTRY_CLASSIFIED_DEPENDENCY_FIELDS = {
    "network_dependencies",
    "host_dependencies",
    "service_dependencies",
    "power_dependencies",
    "administrative_dependencies",
}
REGISTRY_DEPENDENCY_TYPE_RULES = {
    "network_dependencies": {"network_device"},
    "host_dependencies": {"host"},
    "service_dependencies": {"service", "planned_service"},
    "power_dependencies": {"physical_device"},
    "administrative_dependencies": {"physical_device", "host"},
}
REGISTRY_SERVICE_TYPES = {"service", "planned_service"}
REGISTRY_VALID_HOST_LIFECYCLES = {"active", "planned"}
REGISTRY_UNKNOWN_MARKERS = {"TBD", "unknown"}


def parse_registry_yaml(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list_key: str | None = None
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current_list_key is None:
                raise ValueError(f"List item without list key on line {line_number}")
            value = stripped[2:].strip()
            existing = data.setdefault(current_list_key, [])
            if not isinstance(existing, list):
                raise ValueError(f"List key {current_list_key} is not a list on line {line_number}")
            existing.append(value)
            continue
        if ":" not in stripped:
            raise ValueError(f"Unsupported YAML syntax on line {line_number}")
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_list_key = None
        if not key:
            raise ValueError(f"Missing key on line {line_number}")
        if key in data:
            raise ValueError(f"Duplicate key {key} on line {line_number}")
        if value == "[]":
            data[key] = []
        elif value == "":
            data[key] = []
            current_list_key = key
        elif value.lower() == "true":
            data[key] = True
        elif value.lower() == "false":
            data[key] = False
        else:
            data[key] = value
    return data


def load_registry_schema(schema_path: Path | None = None) -> dict[str, object]:
    path = REGISTRY_SCHEMA if schema_path is None else schema_path
    return parse_registry_yaml(path)


def registry_record_files(records_root: Path | None = None) -> list[Path]:
    base = REGISTRY_RECORDS if records_root is None else records_root
    if not base.exists():
        return []
    return sorted(base.rglob("*.yaml"))


def record_dependencies(record: dict[str, object]) -> list[str]:
    dependencies: list[str] = []
    for field in ["dependencies", *sorted(REGISTRY_CLASSIFIED_DEPENDENCY_FIELDS)]:
        values = record.get(field)
        if isinstance(values, list):
            dependencies.extend(value for value in values if isinstance(value, str))
    return dependencies


def service_has_host_path(record_id: str, records: dict[str, dict[str, object]], visiting: set[str] | None = None) -> bool:
    visiting = set() if visiting is None else visiting
    if record_id in visiting:
        return False
    visiting.add(record_id)
    record = records.get(record_id, {})
    host_dependencies = record.get("host_dependencies")
    if isinstance(host_dependencies, list):
        for dependency in host_dependencies:
            target = records.get(str(dependency))
            if target and target.get("record_type") == "host" and target.get("lifecycle_status") in REGISTRY_VALID_HOST_LIFECYCLES:
                return True
    service_dependencies = record.get("service_dependencies")
    if isinstance(service_dependencies, list):
        for dependency in service_dependencies:
            target = records.get(str(dependency))
            if target and target.get("record_type") in REGISTRY_SERVICE_TYPES:
                if service_has_host_path(str(dependency), records, visiting):
                    return True
    return False


def dependency_cycle_messages(records: dict[str, dict[str, object]]) -> list[str]:
    graph = {
        record_id: [dependency for dependency in record.get("service_dependencies", []) if dependency in records]
        for record_id, record in records.items()
        if record.get("record_type") in REGISTRY_SERVICE_TYPES and isinstance(record.get("service_dependencies", []), list)
    }
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []
    cycles: set[tuple[str, ...]] = set()

    def visit(record_id: str) -> None:
        if record_id in visited:
            return
        if record_id in visiting:
            start = stack.index(record_id)
            cycle = stack[start:] + [record_id]
            cycles.add(tuple(cycle))
            return
        visiting.add(record_id)
        stack.append(record_id)
        for dependency in graph.get(record_id, []):
            visit(dependency)
        stack.pop()
        visiting.remove(record_id)
        visited.add(record_id)

    for record_id in sorted(graph):
        visit(record_id)
    return [" -> ".join(cycle) for cycle in sorted(cycles)]


def record_unknown_fields(record: dict[str, object]) -> list[str]:
    unknown_fields: list[str] = []
    for key, value in record.items():
        if isinstance(value, str) and any(marker.lower() in value.lower() for marker in REGISTRY_UNKNOWN_MARKERS):
            unknown_fields.append(key)
    return sorted(unknown_fields)


def load_registry_records(records_root: Path | None = None) -> tuple[dict[str, dict[str, object]], dict[str, Path], list[CheckResult]]:
    records_base = REGISTRY_RECORDS if records_root is None else records_root
    records: dict[str, dict[str, object]] = {}
    path_by_id: dict[str, Path] = {}
    errors: list[CheckResult] = []
    for path in registry_record_files(records_base):
        display = str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
        try:
            record = parse_registry_yaml(path)
        except ValueError as exc:
            errors.append(CheckResult("ERROR", f"Registry YAML parse failed: {exc}", display))
            continue
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            errors.append(CheckResult("ERROR", "Registry record id is required", display))
            continue
        if record_id in records:
            errors.append(CheckResult("ERROR", f"Duplicate registry id: {record_id}", display))
            continue
        records[record_id] = record
        path_by_id[record_id] = path
    return records, path_by_id, errors


def registry_display_path(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def registry_sorted_records(records: dict[str, dict[str, object]], record_types: set[str] | None = None) -> list[dict[str, object]]:
    filtered = [record for record in records.values() if record_types is None or str(record.get("record_type")) in record_types]
    return sorted(filtered, key=lambda record: (str(record.get("record_type", "")), str(record.get("id", ""))))


def format_registry_value(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "[]"
    return str(value)


def print_registry_records(records: list[dict[str, object]]) -> None:
    print("ID	TYPE	LIFECYCLE	HEALTH	NAME")
    for record in records:
        print(
            f"{record.get('id', '')}	{record.get('record_type', '')}	"
            f"{record.get('lifecycle_status', '')}	{record.get('health_status', '')}	{record.get('name', '')}"
        )


def _registry_cli_path(value: str, *, must_exist: bool) -> Path:
    if not value or "\\" in value:
        raise MigrationDataError("Registry migration path must be a repository-relative path.")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts:
        raise MigrationDataError("Registry migration path must be a safe repository-relative path.")
    resolved_root = ROOT.resolve()
    resolved = (ROOT / candidate).resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise MigrationDataError("Registry migration path escapes the repository.")
    if must_exist and not resolved.is_file():
        raise MigrationDataError(f"Registry migration file does not exist: {value}.")
    return resolved


def _current_registry_migration_plan(catalog_path: Path | None = None):
    records, path_by_id, errors = load_registry_records()
    if errors:
        raise MigrationDataError("Registry records must load successfully before migration planning.")
    schema = load_registry_schema()
    source = REGISTRY_MIGRATION_CATALOG if catalog_path is None else catalog_path
    try:
        catalog = migration_evidence_catalog_from_json(source.read_text(encoding="utf-8"))
    except (OSError, MigrationDataError) as exc:
        raise MigrationDataError(f"Migration evidence catalog cannot be read: {exc}.") from exc
    return build_migration_plan(records, path_by_id, schema, catalog, ROOT)


def _parse_migration_apply_arguments(argv: list[str]) -> tuple[Path, Path, bool, bool]:
    values: dict[str, str] = {}
    modes: set[str] = set()
    index = 1
    while index < len(argv):
        argument = argv[index]
        if argument in {"--plan", "--rollback-output"}:
            if argument in values or index + 1 >= len(argv) or argv[index + 1].startswith("--"):
                raise MigrationDataError(f"Migration apply requires one value for {argument}.")
            values[argument] = argv[index + 1]
            index += 2
            continue
        if argument in {"--dry-run", "--confirm"}:
            if argument in modes:
                raise MigrationDataError(f"Migration apply argument is duplicated: {argument}.")
            modes.add(argument)
            index += 1
            continue
        raise MigrationDataError(f"Migration apply contains unsupported argument: {argument}.")
    if set(values) != {"--plan", "--rollback-output"}:
        raise MigrationDataError("Migration apply requires --plan and --rollback-output.")
    if len(modes) != 1:
        raise MigrationDataError("Migration apply requires exactly one of --dry-run or --confirm.")
    return (
        _registry_cli_path(values["--plan"], must_exist=True),
        _registry_cli_path(values["--rollback-output"], must_exist=False),
        "--dry-run" in modes,
        "--confirm" in modes,
    )


def _registry_migration_cli(argv: list[str]) -> int:
    try:
        if argv == ["plan"]:
            print(migration_plan_to_json(_current_registry_migration_plan()), end="")
            return 0
        if len(argv) == 3 and argv[:2] == ["plan", "--catalog"]:
            print(migration_plan_to_json(_current_registry_migration_plan(_registry_cli_path(argv[2], must_exist=True))), end="")
            return 0
        if argv == ["review"]:
            print(render_migration_review(_current_registry_migration_plan()), end="")
            return 0
        if len(argv) == 3 and argv[:2] == ["review", "--plan"]:
            plan = migration_plan_from_json(_registry_cli_path(argv[2], must_exist=True).read_text(encoding="utf-8"))
            print(render_migration_review(plan), end="")
            return 0
        if argv == ["status"]:
            plan = _current_registry_migration_plan()
            report = build_migration_report(plan)
            print("# Registry Container Identity Migration Status")
            print(f"Plan ID: {report.plan_id}")
            print(f"Migration model: {plan.model_version}")
            print(f"Superseded plan IDs: {', '.join(SUPERSEDED_MIGRATION_PLAN_IDS)}")
            print(f"Approval status: {report.approval_status.value}")
            print(f"Candidates: {report.candidate_count}")
            print(f"Apply: {report.apply_count}")
            print(f"Review required: {report.review_required_count}")
            print(f"No change: {report.no_change_count}")
            print(f"Unresolved subjects: {len(report.unresolved_subject_ids)}")
            print("Mode: read-only current repository planning")
            return 0
        if len(argv) == 5 and argv[0] == "bind-approval" and argv[1] == "--plan" and argv[3] == "--approval":
            plan_path = _registry_cli_path(argv[2], must_exist=True)
            approval_path = _registry_cli_path(argv[4], must_exist=True)
            approval_reference = str(approval_path.relative_to(ROOT))
            approval_parts = Path(approval_reference).parts
            if len(approval_parts) < 4 or approval_parts[:2] != ("registry", "migrations") or approval_path.suffix != ".json":
                raise MigrationDataError("Migration approval artifact must be a JSON file under registry/migrations.")
            plan = migration_plan_from_json(plan_path.read_text(encoding="utf-8"))
            bound_plan = bind_migration_approval(plan, approval_reference, approval_path.read_bytes())
            print(migration_plan_to_json(bound_plan), end="")
            return 0
        if argv and argv[0] == "apply":
            plan_path, rollback_path, dry_run, confirm = _parse_migration_apply_arguments(argv)
            plan = migration_plan_from_json(plan_path.read_text(encoding="utf-8"))
            result = execute_migration(
                plan,
                ROOT,
                dry_run=dry_run,
                confirm=confirm,
                rollback_output=None if dry_run else rollback_path,
                validate=validate_registry,
            )
            print(json.dumps(asdict(result), indent=2, sort_keys=True))
            return 0
        if len(argv) == 5 and argv[0] == "validate-completed" and argv[1] == "--plan" and argv[3] == "--rollback":
            plan_path = _registry_cli_path(argv[2], must_exist=True)
            rollback_path = _registry_cli_path(argv[4], must_exist=True)
            plan = migration_plan_from_json(plan_path.read_text(encoding="utf-8"))
            metadata = rollback_metadata_from_json(rollback_path.read_text(encoding="utf-8"))
            result = validate_completed_migration(plan, metadata, ROOT)
            print(json.dumps(asdict(result), indent=2, sort_keys=True))
            return 0
        if len(argv) == 4 and argv[:2] == ["rollback", "--metadata"] and argv[3] == "--confirm":
            metadata_path = _registry_cli_path(argv[2], must_exist=True)
            metadata = rollback_metadata_from_json(metadata_path.read_text(encoding="utf-8"))
            result = rollback_migration(metadata, ROOT, confirm=True, validate=validate_registry)
            print(json.dumps(asdict(result), indent=2, sort_keys=True))
            return 0
    except (MigrationDataError, OSError) as exc:
        print(f"Registry migration error: {exc}")
        return 1
    print("Usage: platform-eap registry migration <plan [--catalog PATH]|review [--plan PATH]|status|bind-approval --plan PATH --approval PATH|apply --plan PATH --rollback-output PATH (--dry-run|--confirm)|validate-completed --plan PATH --rollback PATH|rollback --metadata PATH --confirm>")
    return 2


def registry_cli(argv: list[str]) -> int:
    if not argv:
        print("Usage: platform-eap registry <list|show|services|hosts|devices|validate|topology|schema-version|migration>")
        return 2
    if argv == ["schema-version"]:
        try:
            schema = load_registry_schema()
        except (OSError, ValueError) as exc:
            print(f"Registry schema could not be read: {exc}")
            return 1
        print(f"Infrastructure Registry schema version: {schema_version_from(schema)}")
        return 0
    if argv[0] == "migration":
        return _registry_migration_cli(argv[1:])
    if argv == ["validate"]:
        results = validate_registry()
        status = status_from(results)
        errors = [result for result in results if result.severity == "ERROR"]
        warnings = [result for result in results if result.severity == "WARNING"]
        print("# Registry Validation")
        print(f"Status: {status}")
        print("Mode: read-only local-file validation")
        print(f"Errors: {len(errors)}")
        print(f"Warnings: {len(warnings)}")
        for result in results:
            suffix = f" ({result.path})" if result.path else ""
            print(f"{result.severity}: {result.message}{suffix}")
        return 1 if errors else 0

    records, path_by_id, errors = load_registry_records()
    if errors:
        print("Registry records could not be loaded.")
        for error in errors:
            suffix = f" ({error.path})" if error.path else ""
            print(f"{error.severity}: {error.message}{suffix}")
        return 1

    command = argv[0]
    if command == "list" and len(argv) == 1:
        print("# Infrastructure Registry Records")
        print(f"Records: {len(records)}")
        print_registry_records(registry_sorted_records(records))
        return 0
    if command == "show" and len(argv) == 2:
        record_id = argv[1]
        record = records.get(record_id)
        if record is None:
            print(f"Registry record not found: {record_id}")
            return 1
        print(f"# Registry Record: {record_id}")
        print(f"Path: {registry_display_path(path_by_id[record_id])}")
        for key in sorted(record):
            print(f"{key}: {format_registry_value(record[key])}")
        return 0
    if command == "services" and len(argv) == 1:
        selected = registry_sorted_records(records, {"service", "planned_service"})
        print("# Registry Services")
        print(f"Records: {len(selected)}")
        print_registry_records(selected)
        return 0
    if command == "hosts" and len(argv) == 1:
        selected = registry_sorted_records(records, {"host"})
        print("# Registry Hosts")
        print(f"Records: {len(selected)}")
        print_registry_records(selected)
        return 0
    if command == "devices" and len(argv) == 1:
        selected = registry_sorted_records(records, {"physical_device", "network_device"})
        print("# Registry Devices")
        print(f"Records: {len(selected)}")
        print_registry_records(selected)
        return 0
    if command == "topology" and len(argv) == 1:
        print("# Registry Topology Summary")
        print("Mode: read-only local-file summary")
        for record in registry_sorted_records(records):
            relationship_lines = []
            for field in sorted(REGISTRY_CLASSIFIED_DEPENDENCY_FIELDS):
                values = record.get(field)
                if isinstance(values, list) and values:
                    relationship_lines.append(f"{field}={', '.join(str(value) for value in values)}")
            if relationship_lines:
                print(f"{record.get('id')} ({record.get('record_type')}): {'; '.join(relationship_lines)}")
        return 0
    print("Usage: platform-eap registry <list|show <record-id>|services|hosts|devices|validate|topology|schema-version|migration>")
    return 2


def validate_registry(
    records_root: Path | None = None,
    schema_path: Path | None = None,
    repository_root: Path | None = None,
) -> list[CheckResult]:
    records_base = REGISTRY_RECORDS if records_root is None else records_root
    schema = REGISTRY_SCHEMA if schema_path is None else schema_path
    identity_root = ROOT if repository_root is None else repository_root
    results: list[CheckResult] = []
    if not REGISTRY_ROOT.exists() and records_root is None:
        results.append(CheckResult("ERROR", "Registry root missing", "registry"))
        return results
    schema_data: dict[str, object] = {}
    if not schema.exists():
        results.append(CheckResult("ERROR", "Registry schema missing", str(schema.relative_to(ROOT) if schema.is_relative_to(ROOT) else schema)))
    else:
        results.append(CheckResult("INFO", "Registry schema exists", str(schema.relative_to(ROOT) if schema.is_relative_to(ROOT) else schema)))
        try:
            schema_data = load_registry_schema(schema)
        except (OSError, ValueError) as exc:
            results.append(CheckResult("ERROR", f"Registry schema parse failed: {exc}", str(schema.relative_to(ROOT) if schema.is_relative_to(ROOT) else schema)))
    files = registry_record_files(records_base)
    if not files:
        results.append(CheckResult("ERROR", "No registry records found", str(records_base.relative_to(ROOT) if records_base.is_relative_to(ROOT) else records_base)))
        return results

    parsed_records, path_by_id, load_errors = load_registry_records(records_base)
    results.extend(load_errors)
    if schema_data:
        for finding in validate_container_identity_contract(parsed_records, path_by_id, schema_data, identity_root):
            results.append(CheckResult(finding.severity, finding.message, finding.path))

    owner_ids = {rid for rid, record in parsed_records.items() if record.get("record_type") == "owner"}
    location_ids = {rid for rid, record in parsed_records.items() if record.get("record_type") == "location"}

    for record_id, record in parsed_records.items():
        path = path_by_id[record_id]
        display = str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
        missing = sorted(field for field in REGISTRY_REQUIRED_FIELDS if field not in record)
        for field in missing:
            results.append(CheckResult("ERROR", f"Missing required registry field: {field}", display))
        record_type = record.get("record_type")
        if record_type not in REGISTRY_ALLOWED_TYPES:
            results.append(CheckResult("ERROR", f"Invalid registry record_type: {record_type}", display))
        lifecycle = record.get("lifecycle_status")
        if lifecycle not in REGISTRY_ALLOWED_LIFECYCLE:
            results.append(CheckResult("ERROR", f"Invalid lifecycle_status: {lifecycle}", display))
        health = record.get("health_status")
        if health not in REGISTRY_ALLOWED_HEALTH:
            results.append(CheckResult("ERROR", f"Invalid health_status: {health}", display))
        if not isinstance(record.get("monitoring_ready"), bool):
            results.append(CheckResult("ERROR", "monitoring_ready must be boolean", display))
        owner = record.get("owner")
        if owner not in owner_ids:
            results.append(CheckResult("ERROR", f"Owner reference not found: {owner}", display))
        location = record.get("location")
        if location not in location_ids:
            results.append(CheckResult("ERROR", f"Location reference not found: {location}", display))
        dependencies = record.get("dependencies")
        if not isinstance(dependencies, list):
            results.append(CheckResult("ERROR", "dependencies must be a list", display))
        else:
            for dependency in dependencies:
                if dependency not in parsed_records:
                    results.append(CheckResult("ERROR", f"Dependency reference not found: {dependency}", display))
        for field in sorted(REGISTRY_CLASSIFIED_DEPENDENCY_FIELDS):
            if field not in record:
                continue
            classified = record.get(field)
            if not isinstance(classified, list):
                results.append(CheckResult("ERROR", f"{field} must be a list", display))
                continue
            allowed_types = REGISTRY_DEPENDENCY_TYPE_RULES[field]
            for dependency in classified:
                target = parsed_records.get(str(dependency))
                if target is None:
                    results.append(CheckResult("ERROR", f"{field} reference not found: {dependency}", display))
                    continue
                target_type = target.get("record_type")
                if target_type not in allowed_types:
                    results.append(CheckResult("ERROR", f"{field} reference has invalid record_type: {dependency} ({target_type})", display))
                if field == "host_dependencies" and record_type in REGISTRY_SERVICE_TYPES:
                    target_lifecycle = target.get("lifecycle_status")
                    if target_lifecycle not in REGISTRY_VALID_HOST_LIFECYCLES:
                        results.append(CheckResult("ERROR", f"Service host reference is not active or planned: {dependency}", display))
        if record_type == "service" and lifecycle == "active" and not service_has_host_path(record_id, parsed_records):
            results.append(CheckResult("ERROR", f"Active service has no valid host relationship: {record_id}", display))
        if record_type == "planned_service" and "host_dependencies" in record and not service_has_host_path(record_id, parsed_records):
            results.append(CheckResult("ERROR", f"Planned service has no valid planned or active host target: {record_id}", display))
        raw_text = path.read_text(encoding="utf-8").lower()
        for term in REGISTRY_FORBIDDEN_SCOPE_TERMS:
            if term in raw_text:
                results.append(CheckResult("ERROR", f"Forbidden finance scope term found in registry record: {term}", display))
        unknown_fields = record_unknown_fields(record)
        if unknown_fields:
            results.append(CheckResult("INFO", f"Registry record explicitly tracks unknown or TBD fields: {', '.join(unknown_fields)}", display))
    for cycle in dependency_cycle_messages(parsed_records):
        results.append(CheckResult("ERROR", f"Circular registry dependency detected: {cycle}"))
    if not any(result.severity == "ERROR" for result in results):
        results.append(CheckResult("INFO", f"Registry schema version {schema_version_from(schema_data)} validated"))
        results.append(CheckResult("INFO", f"Registry validation passed for {len(parsed_records)} records"))
        results.append(CheckResult("INFO", "Platform Digital Twin integrity validation passed"))
    return results

def repository_validate() -> Report:
    required_dirs = [
        "docs/governance", "docs/product", "docs/architecture/decisions", "docs/portfolio",
        "docs/requirements", "docs/specifications", "docs/standards", "docs/milestones",
        "engineering/platform_eap", "engineering/tests", "reports/engineering", "registry/schema", "registry/records",
    ]
    required_files = [
        "README.md", "docs/governance/Permanent_Project_Operating_Model.md",
        "docs/governance/Repository_Principles.md", "docs/governance/Engineering_Lifecycle.md",
        "docs/governance/Definition_of_Done.md", "docs/product/Product_Vision.md",
        "docs/product/Capability_Model.md", "docs/product/Product_Backlog.md",
        "docs/product/Product_Roadmap.md", "docs/product/Product_Governance.md",
        "docs/architecture/Architecture_Decision_Log.md", "docs/architecture/Architecture_Backlog.md",
        "docs/architecture/Infrastructure_Registry_Architecture.md",
        "docs/specifications/Infrastructure_Registry_v1.0_Specification.md",
        "registry/schema/infrastructure_registry_schema.yaml",
        "docs/standards/Documentation_Standards.md", "docs/standards/Development_Workflow.md",
    ]
    results: list[CheckResult] = []
    for item in required_dirs:
        results.append(CheckResult("INFO" if (ROOT / item).is_dir() else "ERROR", "Required directory exists" if (ROOT / item).is_dir() else "Required directory missing", item))
    for item in required_files:
        results.append(CheckResult("INFO" if (ROOT / item).is_file() else "ERROR", "Required file exists" if (ROOT / item).is_file() else "Required file missing", item))
    results.extend(validate_tracked_repository_artifacts())
    results.extend(validate_registry())
    branch = git_output(["branch", "--show-current"])
    results.append(CheckResult("INFO", f"Current branch: {branch}"))
    dirty = git_output(["status", "--short", "--", ".", ":!reports/engineering"])
    if dirty:
        results.append(CheckResult("WARNING", "Working tree has active source changes"))
    else:
        results.append(CheckResult("INFO", "Working tree clean outside generated engineering reports"))
    status = status_from(results)
    return Report("Repository Validation", status, now(), f"Repository validation completed with status {status}.", results)


def governance_validate() -> Report:
    required = [
        "docs/governance/Permanent_Project_Operating_Model.md",
        "docs/governance/Repository_Principles.md",
        "docs/governance/Engineering_Lifecycle.md",
        "docs/governance/Definition_of_Done.md",
        "docs/governance/Product_Portfolio.md",
        "docs/architecture/Architecture_Decision_Log.md",
        "docs/architecture/decisions/ADR-001-Platform-Repository-Creation.md",
        "docs/architecture/decisions/ADR-002-Platform-Product-Boundary.md",
        "docs/architecture/decisions/ADR-003-Repository-Managed-Governance.md",
        "docs/architecture/decisions/ADR-004-Platform-Engineering-Automation-Foundation.md",
        "docs/architecture/decisions/ADR-005-Portfolio-Integration-and-Repository-Independence.md",
        "docs/architecture/decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md",
    ]
    results = []
    for item in required:
        results.append(CheckResult("INFO" if (ROOT / item).exists() else "ERROR", "Governance artifact exists" if (ROOT / item).exists() else "Governance artifact missing", item))
    forbidden_terms = ["banking implementation", "transaction implementation", "budget implementation", "investment implementation"]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").rglob("*.md"))
    for term in forbidden_terms:
        if term.lower() in combined.lower():
            results.append(CheckResult("ERROR", f"Forbidden finance implementation term found: {term}"))
    results.append(CheckResult("INFO", "Finance exclusions are governed by product boundary documents"))
    status = status_from(results)
    return Report("Governance Validation", status, now(), f"Governance validation completed with status {status}.", results)


def release_readiness() -> Report:
    repo = repository_validate()
    gov = governance_validate()
    results = [CheckResult("INFO", f"Repository validation: {repo.status}"), CheckResult("INFO", f"Governance validation: {gov.status}")]
    if repo.status == "FAIL" or gov.status == "FAIL":
        results.append(CheckResult("ERROR", "Release readiness blocked by validation failure"))
    elif "WARNINGS" in repo.status or "WARNINGS" in gov.status:
        results.append(CheckResult("WARNING", "Release readiness has validation warnings"))
    else:
        results.append(CheckResult("INFO", "Release readiness criteria satisfied"))
    status = status_from(results)
    return Report("Release Readiness", status, now(), f"Release readiness completed with status {status}.", results)


def milestone_closeout() -> Report:
    required = [
        "docs/milestones/Milestone_11/Milestone_11_Platform_Repository_Foundation.md",
        "docs/requirements/Milestone_11_Platform_Repository_Foundation_Requirements.md",
        "docs/specifications/Platform_Repository_Foundation_Specification.md",
    ]
    results = [CheckResult("INFO" if (ROOT / item).exists() else "ERROR", "Closeout artifact exists" if (ROOT / item).exists() else "Closeout artifact missing", item) for item in required]
    readiness = release_readiness()
    results.append(CheckResult("INFO" if readiness.status.startswith("PASS") else "ERROR", f"Release readiness: {readiness.status}"))
    status = status_from(results)
    return Report("Milestone Closeout", status, now(), f"Milestone closeout completed with status {status}.", results)


AI_SESSION_READINESS_REPORT = REPORT_ROOT / "ai_session_readiness" / "ai_session_readiness_report.json"
READINESS_STATES = {"READY", "READY WITH WARNINGS", "NOT READY"}


def _display_path(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def _unknown_readiness(path: Path, evidence_status: str, detail: str) -> AISessionReadinessMetric:
    return AISessionReadinessMetric(
        status="UNKNOWN",
        error_count=None,
        warning_count=None,
        domain_count=None,
        generated_at=None,
        evidence_status=evidence_status,
        report_path=_display_path(path),
        evidence_usable=False,
        blocking_status="UNKNOWN",
        interpretation="No reliable AI onboarding readiness conclusion is possible.",
        caveat=f"{detail} Run ./platform-eap ai-session readiness, then regenerate Engineering Metrics.",
    )


def load_ai_session_readiness_metric(report_path: Path | None = None) -> AISessionReadinessMetric:
    path = AI_SESSION_READINESS_REPORT if report_path is None else report_path
    if not path.is_file():
        return _unknown_readiness(path, "unavailable", "The governed AI Session Readiness JSON report is unavailable.")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return _unknown_readiness(path, "malformed", f"The governed readiness JSON report cannot be parsed: {exc}.")
    if not isinstance(payload, dict):
        return _unknown_readiness(path, "malformed", "The governed readiness JSON report must contain an object.")

    required = {"command", "readiness", "generated_at", "domains", "errors", "warnings"}
    missing = sorted(required - payload.keys())
    if missing:
        return _unknown_readiness(path, "malformed", f"Required readiness fields are missing: {', '.join(missing)}.")

    readiness = payload.get("readiness")
    generated_at = payload.get("generated_at")
    domains = payload.get("domains")
    errors = payload.get("errors")
    warnings = payload.get("warnings")
    if payload.get("command") != "./platform-eap ai-session readiness":
        return _unknown_readiness(path, "malformed", "The readiness source command is missing or invalid.")
    if not isinstance(readiness, str) or readiness not in READINESS_STATES:
        return _unknown_readiness(path, "malformed", f"The readiness state is invalid: {readiness!r}.")
    if not isinstance(generated_at, str) or not generated_at.strip():
        return _unknown_readiness(path, "malformed", "The readiness generation timestamp is missing.")
    try:
        datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    except ValueError:
        return _unknown_readiness(path, "malformed", "The readiness generation timestamp is invalid.")
    if not isinstance(domains, list) or not isinstance(errors, list) or not isinstance(warnings, list):
        return _unknown_readiness(path, "malformed", "Readiness domains, errors, and warnings must be arrays.")
    if not domains:
        return _unknown_readiness(path, "malformed", "The readiness report contains no validation domains.")
    if any(
        not isinstance(domain, dict)
        or not isinstance(domain.get("name"), str)
        or not isinstance(domain.get("status"), str)
        or not isinstance(domain.get("checks"), list)
        for domain in domains
    ):
        return _unknown_readiness(path, "malformed", "Each readiness domain must contain a name, status, and checks array.")
    if any(not isinstance(finding, dict) for finding in [*errors, *warnings]):
        return _unknown_readiness(path, "malformed", "Each readiness finding must be a structured object.")

    error_count = len(errors)
    warning_count = len(warnings)
    logically_consistent = (
        (readiness == "READY" and error_count == 0 and warning_count == 0)
        or (readiness == "READY WITH WARNINGS" and error_count == 0 and warning_count > 0)
        or (readiness == "NOT READY" and error_count > 0)
    )
    if not logically_consistent:
        return _unknown_readiness(path, "malformed", "The readiness state and finding counts are logically inconsistent.")

    if readiness == "READY":
        blocking_status = "NONBLOCKING"
        interpretation = "The repository can onboard a new AI participant without known readiness warnings."
        caveat = "Readiness describes repository onboarding evidence; it does not authorize implementation, remediation, release, or live activity."
    elif readiness == "READY WITH WARNINGS":
        blocking_status = "NONBLOCKING WITH CONDITIONS"
        interpretation = "Orientation may proceed only with the reported conditions disclosed and reconciled."
        caveat = "Warnings remain authoritative in the source readiness report and are not remediated by Engineering Metrics."
    else:
        blocking_status = "BLOCKING"
        interpretation = "AI participant onboarding must stop until blocking findings are addressed and the validator is rerun."
        caveat = "Engineering Metrics reports the blocking evidence but does not remediate it."
    return AISessionReadinessMetric(
        status=readiness,
        error_count=error_count,
        warning_count=warning_count,
        domain_count=len(domains),
        generated_at=generated_at,
        evidence_status="current",
        report_path=_display_path(path),
        evidence_usable=True,
        blocking_status=blocking_status,
        interpretation=interpretation,
        caveat=caveat,
    )


def ai_session_readiness_health_source(metric: AISessionReadinessMetric) -> dict[str, object]:
    return {
        "state": metric.status,
        "error_count": metric.error_count,
        "warning_count": metric.warning_count,
        "evidence_status": metric.evidence_status,
        "last_generated_at": metric.generated_at,
        "source_available": metric.evidence_status != "unavailable",
        "source_usable": metric.evidence_usable,
        "source_report_path": metric.report_path,
    }


def engineering_metrics(readiness_report_path: Path | None = None) -> Report:
    md_docs = list((ROOT / "docs").rglob("*.md"))
    tests = list((ROOT / "engineering" / "tests").glob("test_*.py"))
    adrs = list((ROOT / "docs" / "architecture" / "decisions").glob("ADR-*.md"))
    readiness = load_ai_session_readiness_metric(readiness_report_path)
    results = [
        CheckResult("INFO", f"Markdown documents: {len(md_docs)}"),
        CheckResult("INFO", f"Engineering test files: {len(tests)}"),
        CheckResult("INFO", f"Architecture decisions: {len(adrs)}"),
        CheckResult("INFO", "Engineering health baseline established"),
    ]
    readiness_severity = "INFO" if readiness.status == "READY" else "WARNING"
    results.append(
        CheckResult(
            readiness_severity,
            f"AI Session Readiness: {readiness.status}; evidence {readiness.evidence_status}; onboarding effect {readiness.blocking_status}",
            readiness.report_path,
        )
    )
    status = status_from(results)
    if readiness.status == "UNKNOWN":
        summary = (
            f"Engineering metrics generated with status {status}. AI Session Readiness evidence is "
            f"{readiness.evidence_status}; run ./platform-eap ai-session readiness and regenerate Engineering Metrics."
        )
    else:
        summary = f"Engineering metrics generated with status {status}; AI Session Readiness is {readiness.status}."
    return Report(
        "Engineering Metrics",
        status,
        now(),
        summary,
        results,
        ai_session_readiness=readiness,
        platform_health={"ai_session_readiness": ai_session_readiness_health_source(readiness)},
    )


def capabilities() -> int:
    print("PLAT-EAP-1\tRepository Validation\tImplemented")
    print("PLAT-EAP-2\tGovernance Validation\tImplemented")
    print("PLAT-EAP-3\tRelease Readiness\tImplemented")
    print("PLAT-EAP-4\tMilestone Closeout\tImplemented")
    print("PLAT-EAP-5\tEngineering Metrics\tImplemented")
    print("PLAT-EAP-6\tInfrastructure Registry Validation\tImplemented")
    print("PLAT-EAP-7\tPlatform Digital Twin Integrity Validation\tImplemented")
    print("PLAT-EAP-8\tRegistry CLI\tImplemented")
    print("PLAT-EAP-9\tAI Session Readiness Validation\tImplemented")
    print("PLAT-EAP-10\tGoverned Execution Capability\tImplemented")
    print("PLAT-EAP-11\tGoverned Automation Orchestration Capability\tImplemented")
    print("PLAT-EAP-12\tContainer Operational Health Repository Capability\tImplemented; Fixture Only; Not Activated")
    print("PLAT-EAP-13\tProduction Provider Adapter Foundation\tImplemented; Repository Fixtures Only; No Live Provider")
    print("PLAT-EAP-14\tConstrained Proxy Foundation\tImplemented; Repository Fixtures Only; No Socket or Network Access")
    print("PLAT-EAP-15\tPrivileged Deployment Configuration Foundation\tImplemented; Repository Configuration Only; No Deployment")
    return 0


def _execution_input_path(path_value: str) -> Path:
    root = ROOT.resolve()
    supplied = Path(path_value)
    candidate = (supplied if supplied.is_absolute() else root / supplied).resolve()
    if not candidate.is_relative_to(root):
        raise ExecutionDataError("Execution input path must remain inside the repository.")
    if not candidate.is_file():
        raise ExecutionDataError(f"Execution input file not found: {path_value}.")
    return candidate


def _print_execution_findings(title: str, findings: list[object]) -> int:
    errors = [finding for finding in findings if getattr(finding, "severity", None) == FindingSeverity.ERROR]
    warnings = [finding for finding in findings if getattr(finding, "severity", None) == FindingSeverity.WARNING]
    print(f"# {title}")
    print(f"Status: {'FAIL' if errors else 'PASS WITH WARNINGS' if warnings else 'PASS'}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    for finding in findings:
        path = f" ({finding.path})" if finding.path else ""
        print(f"{finding.severity.value}: {finding.code}: {finding.message}{path}")
    return 1 if errors else 0


def execution_cli(argv: list[str]) -> int:
    usage = "Usage: platform-eap execution <assignment validate|completion validate|completion render> <repository-json-path>"
    if len(argv) != 3:
        print(usage)
        return 2
    resource, command, path_value = argv
    try:
        path = _execution_input_path(path_value)
        text = path.read_text(encoding="utf-8")
        if resource == "assignment" and command == "validate":
            assignment = assignment_from_json(text)
            return _print_execution_findings(
                "Governed Assignment Validation",
                validate_assignment(assignment, repository_root=ROOT),
            )
        if resource == "completion" and command in {"validate", "render"}:
            package = completion_from_json(text)
            findings = validate_completion_package(package, repository_root=ROOT)
            if command == "validate":
                return _print_execution_findings("Governed Completion Validation", findings)
            if any(finding.severity == FindingSeverity.ERROR for finding in findings):
                return _print_execution_findings("Governed Completion Validation", findings)
            print(render_completion_markdown(package), end="")
            return 0
    except (ExecutionDataError, OSError, UnicodeError) as exc:
        print("# Governed Execution Capability")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 1
    print(usage)
    return 2


def automation_cli(argv: list[str]) -> int:
    usage = (
        "Usage: platform-eap automation "
        "<definition validate <repository-json-path>|run validate <repository-json-path>|"
        "transition evaluate <run-json-path> <transition-json-path>|handoff render <run-json-path>>"
    )
    try:
        if len(argv) == 3:
            resource, command, path_value = argv
            path = _execution_input_path(path_value)
            text = path.read_text(encoding="utf-8")
            if resource == "definition" and command == "validate":
                definition = definition_from_json(text)
                return _print_execution_findings(
                    "Governed Automation Definition Validation",
                    validate_automation_definition(definition, repository_root=ROOT),
                )
            if resource == "run" and command == "validate":
                run = run_from_json(text)
                return _print_execution_findings(
                    "Governed Automation Run Validation",
                    validate_automation_run(run, repository_root=ROOT),
                )
            if resource == "handoff" and command == "render":
                run = run_from_json(text)
                findings = validate_automation_run(run, repository_root=ROOT)
                if any(finding.severity == FindingSeverity.ERROR for finding in findings):
                    return _print_execution_findings("Governed Automation Run Validation", findings)
                print(render_automation_handoff_markdown(build_automation_handoff(run, ROOT)), end="")
                return 0
        if len(argv) == 4 and argv[:2] == ["transition", "evaluate"]:
            run_path = _execution_input_path(argv[2])
            transition_path = _execution_input_path(argv[3])
            run = run_from_json(run_path.read_text(encoding="utf-8"))
            request = transition_from_json(transition_path.read_text(encoding="utf-8"))
            decision = evaluate_transition(run, request, ROOT)
            print(transition_decision_to_json(decision), end="")
            return 0 if decision.allowed else 1
    except (AutomationDataError, ExecutionDataError, OSError, UnicodeError) as exc:
        print("# Governed Automation Capability")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 1
    print(usage)
    return 2


def _container_health_input_path(path_value: str) -> Path:
    root = ROOT.resolve()
    supplied = Path(path_value)
    unresolved = supplied if supplied.is_absolute() else root / supplied
    if unresolved.is_symlink():
        raise ContainerHealthDataError("Container-health input path must not be a symbolic link.")
    candidate = unresolved.resolve()
    if not candidate.is_relative_to(root):
        raise ContainerHealthDataError("Container-health input path must remain inside the repository.")
    if not candidate.is_file():
        raise ContainerHealthDataError(f"Container-health input file not found: {path_value}.")
    return candidate


def _container_health_directory_path(path_value: str) -> Path:
    root = ROOT.resolve()
    supplied = Path(path_value)
    unresolved = supplied if supplied.is_absolute() else root / supplied
    if unresolved.is_symlink():
        raise ContainerHealthDataError("Container-health directory path must not be a symbolic link.")
    candidate = unresolved.resolve()
    if not candidate.is_relative_to(root):
        raise ContainerHealthDataError("Container-health directory path must remain inside the repository.")
    if not candidate.is_dir():
        raise ContainerHealthDataError(f"Container-health directory not found: {path_value}.")
    return candidate


def _print_container_findings(title: str, findings: tuple[object, ...]) -> int:
    errors = [finding for finding in findings if getattr(finding, "severity", None) == ContainerFindingSeverity.ERROR]
    warnings = [finding for finding in findings if getattr(finding, "severity", None) == ContainerFindingSeverity.WARNING]
    print(f"# {title}")
    print(f"Status: {'FAIL' if errors else 'PASS WITH WARNINGS' if warnings else 'PASS'}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    for finding in findings:
        reference = f" ({finding.reference})" if getattr(finding, "reference", None) else ""
        print(f"{finding.severity.value}: {finding.code}: {finding.message}{reference}")
    return 2 if errors else 0


def _validate_container_health_registry_bundle(bundle):
    records_root = _container_health_directory_path(bundle.registry_records_root)
    if records_root != (ROOT / "engineering/tests/fixtures/container_health/registry").resolve():
        raise ContainerHealthDataError("Container-health evaluation accepts only the governed synthetic Registry fixture root.")
    registry_results = validate_registry(records_root=records_root, schema_path=REGISTRY_SCHEMA, repository_root=ROOT)
    errors = [result for result in registry_results if result.severity == "ERROR"]
    if errors:
        raise ContainerHealthDataError("Registry fixture validation failed: " + "; ".join(result.message for result in errors))
    records, path_by_id, load_errors = load_registry_records(records_root)
    if load_errors:
        raise ContainerHealthDataError("Registry fixture records could not be loaded.")
    schema = load_registry_schema()
    expected = declared_subject_from_registry_contract(
        records,
        path_by_id,
        schema,
        ROOT,
        bundle.declared_subject.subject_id,
        bundle.declared_subject.registry_reference,
        bundle.declared_subject.environment,
    )
    if expected != bundle.declared_subject:
        raise ContainerHealthDataError("Evaluation bundle declared subject does not match the validated Registry fixture.")
    for evidence in bundle.evidence:
        if (
            evidence.subject_id != expected.subject_id
            or evidence.registry_reference != expected.registry_reference
            or evidence.container_service_reference != expected.registry_reference
            or evidence.environment != expected.environment
            or evidence.host_reference != expected.host_reference
        ):
            raise ContainerHealthDataError("Evaluation bundle evidence does not match the validated Registry fixture subject.")
        _container_health_input_path(evidence.source_reference)
        _container_health_input_path(evidence.container_service_reference)
        if evidence.coverage_reference is not None:
            _container_health_input_path(evidence.coverage_reference)


def container_health_cli(argv: list[str]) -> int:
    usage = (
        "Usage: platform-eap container-health "
        "<evidence validate <path>|reconcile <input-path>|assess <input-path>|"
        "assessment validate <path>|assessment render <path>>"
    )
    try:
        if len(argv) == 3 and argv[:2] == ["evidence", "validate"]:
            path = _container_health_input_path(argv[2])
            evidence = evidence_from_json(path.read_text(encoding="utf-8"))
            return _print_container_findings("Container Operational Evidence Validation", validate_evidence(evidence))
        if len(argv) == 2 and argv[0] in {"reconcile", "assess"}:
            path = _container_health_input_path(argv[1])
            bundle = bundle_from_json(path.read_text(encoding="utf-8"))
            _validate_container_health_registry_bundle(bundle)
            policy_set = load_policy_set(ROOT, bundle.declared_subject.policy_reference)
            result = evaluate_bundle(bundle, policy_set)
            if argv[0] == "reconcile":
                print(reconciliation_to_json(result.reconciliation), end="")
            else:
                findings = validate_assessment(result.assessment)
                if any(finding.severity == ContainerFindingSeverity.ERROR for finding in findings):
                    return _print_container_findings("Container Operational Health Assessment Validation", findings)
                print(assessment_to_json(result.assessment), end="")
            return 0
        if len(argv) == 3 and argv[0] == "assessment" and argv[1] in {"validate", "render"}:
            path = _container_health_input_path(argv[2])
            assessment = assessment_from_json(path.read_text(encoding="utf-8"))
            findings = validate_assessment(assessment)
            if argv[1] == "validate":
                return _print_container_findings("Container Operational Health Assessment Validation", findings)
            if any(finding.severity == ContainerFindingSeverity.ERROR for finding in findings):
                return _print_container_findings("Container Operational Health Assessment Validation", findings)
            print(render_assessment_markdown(assessment), end="")
            return 0
    except UnsupportedContractVersion as exc:
        print("# Container Operational Health Repository Capability")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 3
    except PolicyDataError as exc:
        print("# Container Operational Health Repository Capability")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 4
    except (ContainerHealthDataError, OSError, UnicodeError) as exc:
        print("# Container Operational Health Repository Capability")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 2
    print(usage)
    return 2


def _provider_fixture_path(path_value: str) -> Path:
    root = ROOT.resolve()
    fixture_root = (root / "engineering/tests/fixtures/provider_adapter").resolve()
    supplied = Path(path_value)
    unresolved = supplied if supplied.is_absolute() else root / supplied
    if unresolved.is_symlink():
        raise ProviderAdapterDataError("Provider input path must not be a symbolic link.")
    candidate = unresolved.resolve()
    if not candidate.is_relative_to(fixture_root):
        raise ProviderAdapterDataError("Provider commands accept only governed provider-adapter fixtures.")
    if not candidate.is_file():
        raise ProviderAdapterDataError(f"Provider fixture file not found: {path_value}.")
    return candidate


def _print_provider_findings(title: str, findings: tuple[object, ...]) -> int:
    errors = [finding for finding in findings if getattr(finding, "severity", None) == ProviderFindingSeverity.ERROR]
    warnings = [finding for finding in findings if getattr(finding, "severity", None) == ProviderFindingSeverity.WARNING]
    print(f"# {title}")
    print(f"Status: {'FAIL' if errors else 'PASS WITH WARNINGS' if warnings else 'PASS'}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    for finding in findings:
        reference = f" ({finding.reference})" if getattr(finding, "reference", None) else ""
        print(f"{finding.severity.value}: {finding.code}: {finding.message}{reference}")
    return 2 if errors else 0


def provider_cli(argv: list[str]) -> int:
    usage = (
        "Usage: platform-eap provider "
        "<contract|capabilities|fixtures|validate request <path>|validate capability <path>|"
        "validate response <request-path> <response-path>|validate failure <path>|validate result <path>|"
        "validate normalization <path>|normalize <request-path> <fixture-id>|mock <scenario> <request-path>>"
    )
    try:
        if argv == ["contract"]:
            print(contract_summary_to_json(repository_adapter_identity(), repository_capability()), end="")
            return 0
        if argv == ["capabilities"]:
            print(capability_to_json(repository_capability()), end="")
            return 0
        if argv == ["fixtures"]:
            client = RepositoryFixtureClient(ROOT)
            print("# Repository Provider Fixtures")
            print("Scope: synthetic; repository-only; no live provider")
            for name in client.fixture_names():
                print(name)
            return 0
        if len(argv) == 3 and argv[:2] == ["validate", "request"]:
            path = _provider_fixture_path(argv[2])
            request = provider_request_from_json(path.read_text(encoding="utf-8"))
            return _print_provider_findings("Provider Request Validation", validate_request(request))
        if len(argv) == 3 and argv[:2] == ["validate", "capability"]:
            path = _provider_fixture_path(argv[2])
            capability = capability_from_json(path.read_text(encoding="utf-8"))
            return _print_provider_findings("Provider Capability Validation", validate_capability(capability))
        if len(argv) == 4 and argv[:2] == ["validate", "response"]:
            request_path = _provider_fixture_path(argv[2])
            response_path = _provider_fixture_path(argv[3])
            request = provider_request_from_json(request_path.read_text(encoding="utf-8"))
            response = provider_response_from_json(response_path.read_text(encoding="utf-8"))
            return _print_provider_findings("Provider Response Validation", validate_response(response, request))
        if len(argv) == 3 and argv[:2] == ["validate", "failure"]:
            path = _provider_fixture_path(argv[2])
            failure = provider_failure_from_json(path.read_text(encoding="utf-8"))
            return _print_provider_findings("Provider Failure Validation", validate_failure(failure))
        if len(argv) == 3 and argv[:2] == ["validate", "result"]:
            path = _provider_fixture_path(argv[2])
            result = provider_result_from_json(path.read_text(encoding="utf-8"))
            return _print_provider_findings("Provider Result Validation", validate_result(result))
        if len(argv) == 3 and argv[:2] == ["validate", "normalization"]:
            path = _provider_fixture_path(argv[2])
            result = provider_normalization_result_from_json(path.read_text(encoding="utf-8"))
            findings = tuple((*validate_failure(result.failure_result),)) if result.failure_result is not None else ()
            return _print_provider_findings("Provider Normalization Result Validation", findings)
        if len(argv) == 3 and argv[0] == "normalize":
            request_path = _provider_fixture_path(argv[1])
            request = provider_request_from_json(request_path.read_text(encoding="utf-8"))
            adapter = MockProviderAdapter(ROOT)
            provider_result = adapter.collect_fixture(request, argv[2])
            if provider_result.failure_result is not None:
                print(provider_result_to_json(provider_result), end="")
                return 1
            assert provider_result.observation_result is not None
            normalized = adapter.normalize(request, provider_result.observation_result)
            print(provider_normalization_result_to_json(normalized), end="")
            return 1 if normalized.failure_result is not None else 0
        if len(argv) == 3 and argv[0] == "mock":
            scenario = MockScenario(argv[1])
            request_path = _provider_fixture_path(argv[2])
            request = provider_request_from_json(request_path.read_text(encoding="utf-8"))
            adapter = MockProviderAdapter(ROOT, scenario)
            adapter.initialize()
            result = adapter.collect_observation(request)
            adapter.shutdown()
            print(provider_result_to_json(result), end="")
            return 1 if result.failure_result is not None else 0
    except UnsupportedProviderContractVersion as exc:
        print("# Production Provider Adapter Foundation")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 3
    except (ProviderAdapterDataError, OSError, UnicodeError, ValueError) as exc:
        print("# Production Provider Adapter Foundation")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 2
    print(usage)
    return 2


def _proxy_fixture_path(path_value: str) -> Path:
    root = ROOT.resolve()
    fixture_root = (root / "engineering/tests/fixtures/proxy_foundation").resolve()
    supplied = Path(path_value)
    unresolved = supplied if supplied.is_absolute() else root / supplied
    if unresolved.is_symlink():
        raise ProxyDataError("Proxy input path must not be a symbolic link.")
    candidate = unresolved.resolve()
    if not candidate.is_relative_to(fixture_root):
        raise ProxyDataError("Proxy commands accept only governed proxy-foundation fixtures.")
    if not candidate.is_file():
        raise ProxyDataError(f"Proxy fixture file not found: {path_value}.")
    return candidate


def _print_proxy_findings(title: str, findings: tuple[object, ...]) -> int:
    errors = [finding for finding in findings if getattr(finding, "severity", None) == ProxyFindingSeverity.ERROR]
    warnings = [finding for finding in findings if getattr(finding, "severity", None) == ProxyFindingSeverity.WARNING]
    print(f"# {title}")
    print(f"Status: {'FAIL' if errors else 'PASS WITH WARNINGS' if warnings else 'PASS'}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    for finding in findings:
        reference = f" ({finding.reference})" if getattr(finding, "reference", None) else ""
        print(f"{finding.severity.value}: {finding.code}: {finding.message}{reference}")
    return 2 if errors else 0


def proxy_cli(argv: list[str]) -> int:
    usage = (
        "Usage: platform-eap proxy "
        "<contract|validate|validate request <path>|validate response <request-path> <response-path>|"
        "validate policy <path>|validate configuration <path>|validate capability <path>|policy|"
        "decision <scenario>|fixtures|request <scenario>|response <scenario>|mock <scenario>>"
    )
    try:
        library = RepositoryProxyFixtureLibrary(ROOT)
        if argv == ["contract"]:
            print(proxy_contract_summary_to_json(proxy_contract_summary()), end="")
            return 0
        if argv == ["policy"]:
            print(proxy_policy_to_json(repository_proxy_policy()), end="")
            return 0
        if argv == ["validate"]:
            request = library.base_request()
            response = library.base_response()
            findings = tuple(
                (*validate_proxy_policy(repository_proxy_policy()), *validate_proxy_configuration(repository_proxy_configuration()),
                 *validate_proxy_capability(repository_proxy_capability()), *validate_proxy_request(request),
                 *validate_proxy_response(response, request))
            )
            return _print_proxy_findings("Repository Proxy Foundation Validation", findings)
        if len(argv) == 3 and argv[:2] == ["validate", "request"]:
            path = _proxy_fixture_path(argv[2])
            return _print_proxy_findings("Proxy Request Validation", validate_proxy_request(proxy_request_from_json(path.read_text(encoding="utf-8"))))
        if len(argv) == 4 and argv[:2] == ["validate", "response"]:
            request_path = _proxy_fixture_path(argv[2])
            response_path = _proxy_fixture_path(argv[3])
            request = proxy_request_from_json(request_path.read_text(encoding="utf-8"))
            response = proxy_response_from_json(response_path.read_text(encoding="utf-8"))
            return _print_proxy_findings("Proxy Response Validation", validate_proxy_response(response, request))
        if len(argv) == 3 and argv[:2] == ["validate", "policy"]:
            path = _proxy_fixture_path(argv[2])
            return _print_proxy_findings("Proxy Policy Validation", validate_proxy_policy(proxy_policy_from_json(path.read_text(encoding="utf-8"))))
        if len(argv) == 3 and argv[:2] == ["validate", "configuration"]:
            path = _proxy_fixture_path(argv[2])
            return _print_proxy_findings("Proxy Configuration Validation", validate_proxy_configuration(proxy_configuration_from_json(path.read_text(encoding="utf-8"))))
        if len(argv) == 3 and argv[:2] == ["validate", "capability"]:
            path = _proxy_fixture_path(argv[2])
            return _print_proxy_findings("Proxy Capability Validation", validate_proxy_capability(proxy_capability_from_json(path.read_text(encoding="utf-8"))))
        if argv == ["fixtures"]:
            print("# Repository Proxy Fixtures")
            print("Scope: synthetic; repository-only; no socket; no network; no runtime")
            for name in library.scenario_ids():
                print(name)
            return 0
        if len(argv) == 2 and argv[0] == "request":
            print(proxy_request_to_json(library.request_for(argv[1])), end="")
            return 0
        if len(argv) == 2 and argv[0] == "response":
            request = library.request_for(argv[1])
            print(proxy_response_to_json(library.response_for(argv[1], request)), end="")
            return 0
        if len(argv) == 2 and argv[0] == "decision":
            decision = RepositoryMockProxy(ROOT).evaluate(argv[1]).decision
            print(proxy_decision_to_json(decision), end="")
            return 0 if decision.decision == ProxyDecisionStatus.ALLOWED else 1
        if len(argv) == 2 and argv[0] == "mock":
            result = RepositoryMockProxy(ROOT).evaluate(argv[1])
            print(proxy_result_to_json(result), end="")
            return 0 if result.decision.decision == ProxyDecisionStatus.ALLOWED else 1
    except UnsupportedProxyContractVersion as exc:
        print("# Repository-Only Constrained Proxy Foundation")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 3
    except (ProxyDataError, OSError, UnicodeError, ValueError) as exc:
        print("# Repository-Only Constrained Proxy Foundation")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 2
    print(usage)
    return 2


def privileged_proxy_cli(argv: list[str]) -> int:
    usage = (
        "Usage: platform-eap privileged-proxy source "
        "<validate|contract|policy|fixtures|supply-chain|static-safety|acceptance>"
    )
    if not argv or argv[0] != "source":
        print(usage)
        return 2
    action = argv[1:]
    try:
        if action == ["validate"] or action == ["static-safety"]:
            findings = validate_privileged_proxy_source(ROOT)
            errors = [finding for finding in findings if finding.severity == ProxyFindingSeverity.ERROR]
            print("# Privileged Proxy Source Validation")
            print(f"Status: {'FAIL' if errors else 'PASS'}")
            print(f"Errors: {len(errors)}")
            print("Scope: repository-only; transport-free; no socket; no network; no Docker; no deployment")
            for finding in findings:
                reference = f" ({finding.reference})" if finding.reference else ""
                print(f"{finding.severity.value}: {finding.code}: {finding.message}{reference}")
            return 2 if errors else 0
        payload: object | None = None
        if action == ["contract"]:
            payload = privileged_proxy_source_contract(ROOT)
        elif action == ["policy"]:
            payload = privileged_proxy_source_policy()
        elif action == ["fixtures"]:
            payload = privileged_proxy_source_fixtures(ROOT)
        elif action == ["supply-chain"]:
            payload = privileged_proxy_source_supply_chain(ROOT)
        elif action == ["acceptance"]:
            payload = privileged_proxy_source_acceptance(ROOT)
        if payload is not None:
            print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
            return 0
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print("# Privileged Proxy Source Validation")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 2
    print(usage)
    return 2


def _print_deployment_findings(title: str, findings: tuple[object, ...]) -> int:
    errors = [finding for finding in findings if getattr(finding, "severity", None) == DeploymentFindingSeverity.ERROR]
    warnings = [finding for finding in findings if getattr(finding, "severity", None) == DeploymentFindingSeverity.WARNING]
    print(f"# {title}")
    print(f"Status: {'FAIL' if errors else 'PASS WITH WARNINGS' if warnings else 'PASS'}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    for finding in findings:
        reference = f" ({finding.reference})" if getattr(finding, "reference", None) else ""
        print(f"{finding.severity.value}: {finding.code}: {finding.message}{reference}")
    return 2 if errors else 0


def deployment_cli(argv: list[str]) -> int:
    usage = (
        "Usage: platform-eap deployment "
        "<contract|validate [scenario]|digest <profile>|profile <profile>|compatibility <profile>|fixtures|"
        "identity <profile>|runtime <profile>|security <profile>|bundle <profile>>"
    )
    try:
        library = RepositoryDeploymentFixtureLibrary(ROOT)
        if argv == ["contract"]:
            print(deployment_contract_summary_to_json(deployment_contract_summary()), end="")
            return 0
        if argv == ["validate"]:
            bundle = library.bundle_for_profile(DeploymentProfileName.REPOSITORY_ONLY)
            return _print_deployment_findings("Deployment Configuration Validation", validate_deployment_bundle(bundle))
        if len(argv) == 2 and argv[0] == "validate":
            return _print_deployment_findings("Deployment Configuration Scenario Validation", library.validate_scenario(argv[1]))
        if argv == ["fixtures"]:
            print("# Repository Deployment Configuration Fixtures")
            print("Scope: descriptive; repository-only; no deployment; no execution; no network")
            for name in library.scenario_ids():
                print(name)
            return 0
        if len(argv) == 2 and argv[0] in {"digest", "profile", "compatibility", "identity", "runtime", "security", "bundle"}:
            profile = DeploymentProfileName(argv[1])
            bundle = library.bundle_for_profile(profile)
            configuration = bundle.configuration
            if argv[0] == "digest":
                print(deployment_json(bundle.digest), end="")
            elif argv[0] == "profile":
                print(deployment_json(configuration.profile), end="")
            elif argv[0] == "compatibility":
                print(deployment_json(negotiate_deployment_versions(configuration)), end="")
            elif argv[0] == "identity":
                print(deployment_json(configuration.identity), end="")
            elif argv[0] == "runtime":
                print(deployment_json(configuration.runtime), end="")
            elif argv[0] == "security":
                print(deployment_json(configuration.runtime.security), end="")
            else:
                print(deployment_json(bundle), end="")
            return 0
    except UnsupportedDeploymentConfigurationVersion as exc:
        print("# Privileged Deployment Configuration Foundation")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 3
    except (DeploymentConfigurationDataError, OSError, UnicodeError, ValueError) as exc:
        print("# Privileged Deployment Configuration Foundation")
        print("Status: FAIL")
        print(f"ERROR: {exc}")
        return 2
    print(usage)
    return 2


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_report(name: str, builder: Callable[[], Report]) -> int:
    report = builder()
    write_report(name, report)
    print(f"# {report.capability}")
    print(f"Status: {report.status}")
    print(report.summary)
    errors = [r for r in report.results if r.severity == "ERROR"]
    warnings = [r for r in report.results if r.severity == "WARNING"]
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    return 1 if errors else 0


def ai_session_readiness() -> int:
    try:
        result = AISessionReadinessValidator(ROOT).validate()
        markdown_path, json_path = write_readiness_report(
            result,
            REPORT_ROOT / "ai_session_readiness",
        )
    except Exception as exc:
        print("# AI Session Readiness Validation")
        print("Status: EXECUTION FAILURE")
        print(f"Unexpected execution failure: {exc}")
        return 3

    print("# AI Session Readiness Validation")
    print(f"Overall readiness: {result.readiness}")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")
    for domain in result.domains:
        print(f"Domain: {domain.name} - {domain.status}")
        for check in domain.checks:
            if check.severity == READINESS_PASS:
                continue
            evidence = f" ({', '.join(check.evidence)})" if check.evidence else ""
            print(f"{check.severity}: {check.message}{evidence}")
    print(f"Markdown report: {markdown_path.relative_to(ROOT)}")
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    return 1 if result.readiness == NOT_READY or result.errors else 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv == ["repository", "validate"]:
        return run_report("repository", repository_validate)
    if argv == ["governance", "validate"]:
        return run_report("governance", governance_validate)
    if argv == ["release", "readiness"]:
        return run_report("release", release_readiness)
    if argv == ["milestone", "closeout"]:
        return run_report("milestone_closeout", milestone_closeout)
    if argv == ["engineering", "metrics"]:
        return run_report("engineering_metrics", engineering_metrics)
    if argv == ["ai-session", "readiness"]:
        return ai_session_readiness()
    if argv == ["capabilities"]:
        return capabilities()
    if argv and argv[0] == "registry":
        return registry_cli(argv[1:])
    if argv and argv[0] == "execution":
        return execution_cli(argv[1:])
    if argv and argv[0] == "automation":
        return automation_cli(argv[1:])
    if argv and argv[0] == "container-health":
        return container_health_cli(argv[1:])
    if argv and argv[0] == "provider":
        return provider_cli(argv[1:])
    if argv and argv[0] == "proxy":
        return proxy_cli(argv[1:])
    if argv and argv[0] == "privileged-proxy":
        return privileged_proxy_cli(argv[1:])
    if argv and argv[0] == "deployment":
        return deployment_cli(argv[1:])
    print("Usage: platform-eap <repository validate|governance validate|release readiness|milestone closeout|engineering metrics|ai-session readiness|capabilities|registry|execution|automation|container-health|provider|proxy|privileged-proxy|deployment>")
    return 2
