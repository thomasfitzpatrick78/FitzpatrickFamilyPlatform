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


def repository_validate() -> Report:
    required_dirs = [
        "docs/governance", "docs/product", "docs/architecture/decisions", "docs/portfolio",
        "docs/requirements", "docs/specifications", "docs/standards", "docs/milestones",
        "engineering/platform_eap", "engineering/tests", "reports/engineering",
    ]
    required_files = [
        "README.md", "docs/governance/Permanent_Project_Operating_Model.md",
        "docs/governance/Repository_Principles.md", "docs/governance/Engineering_Lifecycle.md",
        "docs/governance/Definition_of_Done.md", "docs/product/Product_Vision.md",
        "docs/product/Capability_Model.md", "docs/product/Product_Backlog.md",
        "docs/product/Product_Roadmap.md", "docs/product/Product_Governance.md",
        "docs/architecture/Architecture_Decision_Log.md", "docs/architecture/Architecture_Backlog.md",
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
    print("Usage: platform-eap <repository validate|governance validate|release readiness|milestone closeout|engineering metrics|capabilities>")
    return 2
