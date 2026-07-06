from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
REPORT_ROOT = ROOT / "reports" / "engineering"


@dataclass
class CheckResult:
    severity: str
    message: str
    path: str | None = None


@dataclass
class Report:
    capability: str
    status: str
    timestamp: str
    summary: str
    results: list[CheckResult]


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
        "## Results",
        "",
    ]
    for result in report.results:
        suffix = f" (`{result.path}`)" if result.path else ""
        lines.append(f"- {result.severity}: {result.message}{suffix}")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps({**asdict(report), "results": [asdict(r) for r in report.results]}, indent=2) + "\n", encoding="utf-8")


def status_from(results: list[CheckResult]) -> str:
    if any(r.severity == "ERROR" for r in results):
        return "FAIL"
    if any(r.severity == "WARNING" for r in results):
        return "PASS WITH WARNINGS"
    return "PASS"



REGISTRY_ROOT = ROOT / "registry"
REGISTRY_SCHEMA = REGISTRY_ROOT / "schema" / "infrastructure_registry_schema.yaml"
REGISTRY_RECORDS = REGISTRY_ROOT / "records"
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


def registry_cli(argv: list[str]) -> int:
    if not argv:
        print("Usage: platform-eap registry <list|show|services|hosts|devices|validate|topology>")
        return 2
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
    print("Usage: platform-eap registry <list|show <record-id>|services|hosts|devices|validate|topology>")
    return 2


def validate_registry(records_root: Path | None = None, schema_path: Path | None = None) -> list[CheckResult]:
    records_base = REGISTRY_RECORDS if records_root is None else records_root
    schema = REGISTRY_SCHEMA if schema_path is None else schema_path
    results: list[CheckResult] = []
    if not REGISTRY_ROOT.exists() and records_root is None:
        results.append(CheckResult("ERROR", "Registry root missing", "registry"))
        return results
    if not schema.exists():
        results.append(CheckResult("ERROR", "Registry schema missing", str(schema.relative_to(ROOT) if schema.is_relative_to(ROOT) else schema)))
    else:
        results.append(CheckResult("INFO", "Registry schema exists", str(schema.relative_to(ROOT) if schema.is_relative_to(ROOT) else schema)))
    files = registry_record_files(records_base)
    if not files:
        results.append(CheckResult("ERROR", "No registry records found", str(records_base.relative_to(ROOT) if records_base.is_relative_to(ROOT) else records_base)))
        return results

    parsed_records, path_by_id, load_errors = load_registry_records(records_base)
    results.extend(load_errors)

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
    contaminants = []
    for base in ["docs", "reports", "engineering"]:
        for pattern in [".DS_Store", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"]:
            contaminants.extend((ROOT / base).rglob(pattern))
    if contaminants:
        for path in contaminants:
            results.append(CheckResult("ERROR", "Generated cache or system artifact found", str(path.relative_to(ROOT))))
    else:
        results.append(CheckResult("INFO", "No governed-path cache or system artifacts detected"))
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


def engineering_metrics() -> Report:
    md_docs = list((ROOT / "docs").rglob("*.md"))
    tests = list((ROOT / "engineering" / "tests").glob("test_*.py"))
    adrs = list((ROOT / "docs" / "architecture" / "decisions").glob("ADR-*.md"))
    results = [
        CheckResult("INFO", f"Markdown documents: {len(md_docs)}"),
        CheckResult("INFO", f"Engineering test files: {len(tests)}"),
        CheckResult("INFO", f"Architecture decisions: {len(adrs)}"),
        CheckResult("INFO", "Engineering health baseline established"),
    ]
    return Report("Engineering Metrics", "PASS", now(), "Engineering metrics generated with status PASS.", results)


def capabilities() -> int:
    print("PLAT-EAP-1\tRepository Validation\tImplemented")
    print("PLAT-EAP-2\tGovernance Validation\tImplemented")
    print("PLAT-EAP-3\tRelease Readiness\tImplemented")
    print("PLAT-EAP-4\tMilestone Closeout\tImplemented")
    print("PLAT-EAP-5\tEngineering Metrics\tImplemented")
    print("PLAT-EAP-6\tInfrastructure Registry Validation\tImplemented")
    print("PLAT-EAP-7\tPlatform Digital Twin Integrity Validation\tImplemented")
    print("PLAT-EAP-8\tRegistry CLI\tImplemented")
    return 0


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
    if argv == ["capabilities"]:
        return capabilities()
    if argv and argv[0] == "registry":
        return registry_cli(argv[1:])
    print("Usage: platform-eap <repository validate|governance validate|release readiness|milestone closeout|engineering metrics|capabilities|registry>")
    return 2
