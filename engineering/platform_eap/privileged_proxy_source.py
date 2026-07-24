from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from engineering.platform_eap.proxy_foundation import (
    FindingSeverity,
    primitive,
    repository_policy,
    validate_policy,
)
from engineering.platform_eap.proxy_foundation_io import policy_from_json


SOURCE_RELATIVE = Path("engineering/privileged_proxy")
POLICY_RELATIVE = Path("engineering/tests/fixtures/proxy_foundation/proxy-policy.json")
EVIDENCE_FILE = "supply-chain-evidence.json"
EXPECTED_PACKAGES = {
    "audit",
    "authorization",
    "core",
    "policy",
    "projection",
    "protocol",
    "replay",
    "resource",
    "safety",
    "target",
    "upstream",
}
FORBIDDEN_IMPORTS = {
    "C",
    "crypto/tls",
    "crypto/x509",
    "net",
    "os/exec",
    "os/user",
    "plugin",
    "reflect",
    "runtime",
    "syscall",
    "unsafe",
}
FORBIDDEN_PREFIXES = (
    "github.com/docker/",
    "github.com/moby/",
    "golang.org/x/crypto/ssh",
    "golang.org/x/sys/",
    "google.golang.org/grpc",
    "k8s.io/",
    "net/",
)
FORBIDDEN_CALLS = (
    "os.Getenv(",
    "os.Getuid(",
    "os.Getgid(",
    "os.Getpid(",
    "os.Hostname(",
    "os.LookupEnv(",
    "os.Environ(",
    "exec.Command(",
    "plugin.Open(",
    "syscall.Socket(",
    "time.Now(",
)


@dataclass(frozen=True)
class SourceFinding:
    severity: FindingSeverity
    code: str
    message: str
    reference: str | None = None


def _finding(code: str, message: str, reference: str | None = None) -> SourceFinding:
    return SourceFinding(FindingSeverity.ERROR, code, message, reference)


def _go_imports(text: str) -> tuple[str, ...]:
    text = re.sub(r"(?s)`[^`]*`", "", text)
    text = re.sub(r"(?s)/\*.*?\*/", "", text)
    text = re.sub(r"(?m)//.*$", "", text)
    imports: list[str] = []
    for match in re.finditer(r'(?m)^\s*import\s+"([^"]+)"', text):
        imports.append(match.group(1))
    for block in re.finditer(r"(?ms)^\s*import\s*\((.*?)^\s*\)", text):
        imports.extend(re.findall(r'"([^"]+)"', block.group(1)))
    return tuple(imports)


def _go_code_without_literals(text: str) -> str:
    text = re.sub(r"(?s)`[^`]*`", "", text)
    text = re.sub(r'"(?:\\.|[^"\\])*"', '""', text)
    text = re.sub(r"(?s)/\*.*?\*/", "", text)
    return re.sub(r"(?m)//.*$", "", text)


def source_inventory(repository_root: Path) -> tuple[Path, ...]:
    source_root = repository_root / SOURCE_RELATIVE
    return tuple(sorted(path for path in source_root.rglob("*") if path.is_file() and not path.is_symlink()))


def validate_source(repository_root: Path) -> tuple[SourceFinding, ...]:
    root = repository_root.resolve()
    source_root = (root / SOURCE_RELATIVE).resolve()
    findings: list[SourceFinding] = []
    if not source_root.is_dir() or source_root.is_symlink():
        return (_finding("source.root.missing", "Privileged proxy source root is missing or unsafe.", str(SOURCE_RELATIVE)),)
    packages = {path.name for path in source_root.iterdir() if path.is_dir() and not path.is_symlink()}
    missing_packages = sorted(EXPECTED_PACKAGES - packages)
    if missing_packages:
        findings.append(_finding("source.packages.missing", f"Required packages are missing: {', '.join(missing_packages)}.", str(SOURCE_RELATIVE)))
    go_files = tuple(sorted(source_root.rglob("*.go")))
    if not go_files:
        findings.append(_finding("source.go.missing", "No Go source files were found.", str(SOURCE_RELATIVE)))
    for path in go_files:
        relative = path.relative_to(root)
        if path.is_symlink() or path.stat().st_mode & 0o111:
            findings.append(_finding("source.file.unsafe", "Go source must be regular and non-executable.", str(relative)))
            continue
        text = path.read_text(encoding="utf-8")
        executable_code = _go_code_without_literals(text)
        if re.search(r"(?m)^\s*package\s+main\s*$", text):
            findings.append(_finding("source.executable.prohibited", "Executable package main is prohibited.", str(relative)))
        for imported in _go_imports(text):
            if imported in FORBIDDEN_IMPORTS or imported.startswith(FORBIDDEN_PREFIXES):
                findings.append(_finding("source.import.prohibited", f"Prohibited capability import: {imported}.", str(relative)))
        for call in FORBIDDEN_CALLS:
            if call in executable_code:
                findings.append(_finding("source.call.prohibited", f"Prohibited capability call: {call[:-1]}.", str(relative)))
    module = root / "go.mod"
    checksum = root / "go.sum"
    if not module.is_file() or module.is_symlink():
        findings.append(_finding("source.module.missing", "go.mod is required.", "go.mod"))
    else:
        module_text = module.read_text(encoding="utf-8")
        expected = "module fitzpatrickfamilyplatform\n\ngo 1.26.5\n"
        if module_text != expected or re.search(r"(?m)^\s*require\b", module_text):
            findings.append(_finding("source.module.invalid", "go.mod must bind Go 1.26.5 with no external modules.", "go.mod"))
    if not checksum.is_file() or checksum.is_symlink() or checksum.read_text(encoding="utf-8").strip() != "":
        findings.append(_finding("source.module_lock.invalid", "go.sum must exist and remain empty for the standard-library-only module.", "go.sum"))
    policy_path = root / POLICY_RELATIVE
    try:
        published = policy_from_json(policy_path.read_text(encoding="utf-8"))
        policy_findings = validate_policy(published)
        if policy_findings or published != repository_policy():
            findings.append(_finding("source.policy.mismatch", "Published Proxy Foundation policy is invalid or drifted.", str(POLICY_RELATIVE)))
    except (OSError, UnicodeError, ValueError) as exc:
        findings.append(_finding("source.policy.unavailable", f"Published Proxy Foundation policy is unavailable: {exc}.", str(POLICY_RELATIVE)))
    evidence = source_root / EVIDENCE_FILE
    if not evidence.is_file() or evidence.is_symlink():
        findings.append(_finding("source.supply_chain.missing", "Source supply-chain evidence is missing.", str(SOURCE_RELATIVE / EVIDENCE_FILE)))
    else:
        try:
            payload = json.loads(evidence.read_text(encoding="utf-8"))
            required = {
                "build",
                "dependencies",
                "evidence_version",
                "go_toolchain",
                "licenses",
                "provenance",
                "scope",
                "source_revision",
                "vulnerability_review",
            }
            if not isinstance(payload, Mapping) or set(payload) != required:
                findings.append(_finding("source.supply_chain.invalid", "Supply-chain evidence fields are missing or unknown.", str(SOURCE_RELATIVE / EVIDENCE_FILE)))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            findings.append(_finding("source.supply_chain.invalid", f"Supply-chain evidence is invalid: {exc}.", str(SOURCE_RELATIVE / EVIDENCE_FILE)))
    required_symbols = {
        source_root / "core/service.go": ("func (service *Service) Handle(",),
        source_root / "authorization/authorization.go": ("ed25519.Verify(",),
        source_root / "replay/replay.go": ("type Journal interface", "type MemoryJournal struct", "type FileJournal struct"),
        source_root / "upstream/upstream.go": ("type Observer interface", "func Dispatch("),
        source_root / "safety/safety.go": ("func ValidateTree(",),
    }
    for path, symbols in required_symbols.items():
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for symbol in symbols:
            if symbol not in text:
                findings.append(_finding("source.contract.missing", f"Required source contract is missing: {symbol}.", str(path.relative_to(root))))
    return tuple(findings)


def contract_summary(repository_root: Path) -> Mapping[str, object]:
    findings = validate_source(repository_root)
    return {
        "activation_status": "not_activated",
        "approved_operations": [
            "ResolveTargetIdentity",
            "ObserveHealth",
            "ObserveLifecycle",
            "ObserveRestartInformation",
            "ObserveStatisticsOnce",
        ],
        "docker_capability": "absent",
        "network_capability": "absent",
        "privileged_execution": "absent",
        "protocol_version": "1.0",
        "repository_validation": "PASS" if not findings else "FAIL",
        "scope": "transport-free repository source",
        "socket_capability": "absent",
    }


def policy_summary() -> Mapping[str, object]:
    return primitive(repository_policy())


def fixture_summary(repository_root: Path) -> Mapping[str, object]:
    files = source_inventory(repository_root)
    tests = [str(path.relative_to(repository_root)) for path in files if path.name.endswith("_test.go")]
    return {
        "fixture_scope": "synthetic and repository-only",
        "test_files": tests,
        "transport": "absent",
    }


def supply_chain_summary(repository_root: Path) -> Mapping[str, object]:
    path = repository_root / SOURCE_RELATIVE / EVIDENCE_FILE
    return json.loads(path.read_text(encoding="utf-8"))


def acceptance_summary(repository_root: Path) -> Mapping[str, object]:
    findings = validate_source(repository_root)
    return {
        "artifact_acceptance": "not_satisfied",
        "named_target_observation": "not_authorized",
        "privileged_deployment": "not_authorized",
        "socket_behavior": "not_satisfied",
        "source_foundation": "satisfied" if not findings else "not_satisfied",
        "static_no_network_no_docker": "satisfied" if not findings else "not_satisfied",
        "transport_free_core": "satisfied" if not findings else "not_satisfied",
    }
