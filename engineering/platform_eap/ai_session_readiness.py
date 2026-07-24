from __future__ import annotations

import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable


READY = "READY"
READY_WITH_WARNINGS = "READY WITH WARNINGS"
NOT_READY = "NOT READY"

PASS = "PASS"
WARNING = "WARNING"
ERROR = "ERROR"


@dataclass(frozen=True)
class ReadinessCheck:
    check_id: str
    severity: str
    message: str
    evidence: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ValidationDomain:
    name: str
    status: str
    checks: list[ReadinessCheck]


@dataclass(frozen=True)
class RepositoryContext:
    name: str
    path: str
    branch: str | None
    head: str | None
    working_tree: str


@dataclass(frozen=True)
class ReadinessResult:
    capability: str
    command: str
    readiness: str
    generated_at: str
    repository: RepositoryContext
    domains: list[ValidationDomain]

    @property
    def errors(self) -> list[ReadinessCheck]:
        return [check for domain in self.domains for check in domain.checks if check.severity == ERROR]

    @property
    def warnings(self) -> list[ReadinessCheck]:
        return [check for domain in self.domains for check in domain.checks if check.severity == WARNING]


@dataclass(frozen=True)
class WorkstreamRequirement:
    name: str
    filename: str
    authoritative_tokens: tuple[str, ...]
    required_dependencies: tuple[str, ...]
    planning_tokens: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class ReadinessConfiguration:
    expected_repository: str
    active_milestone: str
    permanent_governance: tuple[str, ...]
    collaboration_artifacts: tuple[str, ...]
    templates: tuple[str, ...]
    role_catalog: str
    required_roles: tuple[str, ...]
    planning_artifacts: dict[str, str]
    continuity_root: str
    workstreams: tuple[WorkstreamRequirement, ...]


AI_COLLABORATION_ROOT = "docs/engineering-organization/ai-collaboration"

DEFAULT_CONFIGURATION = ReadinessConfiguration(
    expected_repository="FitzpatrickFamilyPlatform",
    active_milestone="Milestone 14",
    permanent_governance=(
        "docs/governance/Permanent_Project_Operating_Model.md",
        "docs/governance/Engineering_Lifecycle.md",
        "docs/governance/Engineering_Principles.md",
        "docs/governance/Definition_of_Done.md",
        "docs/governance/Repository_Principles.md",
    ),
    collaboration_artifacts=(
        f"{AI_COLLABORATION_ROOT}/AI_Collaboration_Governance_Capability_Charter.md",
        f"{AI_COLLABORATION_ROOT}/AI_Collaboration_Governance_Specification.md",
        f"{AI_COLLABORATION_ROOT}/AI_Collaboration_Lifecycle.md",
        f"{AI_COLLABORATION_ROOT}/AI_Session_Initialization_Standard.md",
        f"{AI_COLLABORATION_ROOT}/AI_Session_Completion_Standard.md",
        f"{AI_COLLABORATION_ROOT}/Workstream_Continuity_Brief_Specification.md",
        f"{AI_COLLABORATION_ROOT}/AI_Collaboration_Steward_Specification.md",
        f"{AI_COLLABORATION_ROOT}/AI_Session_Readiness_Validator_Specification.md",
        f"{AI_COLLABORATION_ROOT}/AI_Collaboration_Governance_Framework.md",
        f"{AI_COLLABORATION_ROOT}/README.md",
    ),
    templates=(
        f"{AI_COLLABORATION_ROOT}/templates/AI_Collaboration_Steward_Review_Template.md",
        f"{AI_COLLABORATION_ROOT}/templates/AI_Session_Completion_Report_Template.md",
        f"{AI_COLLABORATION_ROOT}/templates/AI_Session_Initialization_Record_Template.md",
        f"{AI_COLLABORATION_ROOT}/templates/Workstream_Continuity_Brief_Template.md",
    ),
    role_catalog="docs/engineering-organization/AI_Role_Catalog.md",
    required_roles=(
        "Chief Architect / Architecture Gatekeeper",
        "Codex Implementation Engineer",
        "Execution Agent",
        "Operations Analyst",
        "AI Collaboration Steward",
    ),
    planning_artifacts={
        "milestone": "docs/milestones/Milestone_14/Milestone_14_Portfolio_Plan.md",
        "kanban": "docs/portfolio/Engineering_Portfolio_Kanban.md",
        "roadmap": "docs/product/Product_Roadmap.md",
        "backlog": "docs/product/Product_Backlog.md",
    },
    continuity_root=f"{AI_COLLABORATION_ROOT}/operational/milestone-14",
    workstreams=(
        WorkstreamRequirement(
            "Architecture Integration",
            "Architecture_Integration_Continuity_Brief.md",
            ("Milestone Plan", "Engineering Portfolio Kanban", "EO-14.8A", "EO-14.8B"),
            (),
            {
                "milestone": ("EO-14.8",),
                "kanban": ("Architecture Gatekeeper", "EO-14.8"),
                "roadmap": ("EO-14.8",),
                "backlog": ("EO-14.8",),
            },
        ),
        WorkstreamRequirement(
            "Alpha",
            "Alpha_Continuity_Brief.md",
            ("Milestone Plan", "Engineering Portfolio Kanban", "EO-14.1", "EO-14.4"),
            ("Architecture Integration",),
            {
                "milestone": ("Alpha", "EO-14.1A", "EO-14.4A"),
                "kanban": ("Alpha", "EO-14.1A", "EO-14.4A"),
                "roadmap": ("EO-14.1A", "EO-14.4A"),
                "backlog": ("Execution Agent Specification", "Governed Automation Framework"),
            },
        ),
        WorkstreamRequirement(
            "Bravo",
            "Bravo_Continuity_Brief.md",
            ("Milestone Plan", "Engineering Portfolio Kanban", "PLAT-14.1", "PLAT-13.6.3B"),
            ("Architecture Integration", "Alpha"),
            {
                "milestone": ("Bravo", "PLAT-14.1A"),
                "kanban": ("Bravo", "PLAT-14.1A"),
                "roadmap": ("PLAT-14.1A",),
                "backlog": ("Container Metrics Modernization",),
            },
        ),
        WorkstreamRequirement(
            "Charlie",
            "Charlie_Continuity_Brief.md",
            ("Milestone Plan", "Engineering Portfolio Kanban", "EO-14.2", "EO-14.3"),
            ("Architecture Integration", "Bravo"),
            {
                "milestone": ("Charlie", "EO-14.2A", "EO-14.3A"),
                "kanban": ("Charlie", "EO-14.2A", "EO-14.3A"),
                "roadmap": ("EO-14.2A", "EO-14.3A"),
                "backlog": ("Operations Analyst Specification", "Engineering Metrics v2"),
            },
        ),
    ),
)


ALLOWED_BRIEF_STATES = {"Active", "Paused", "Superseded", "Closed", "Draft"}
ALLOWED_ENGINEERING_STAGES = {
    "Vision",
    "Capability",
    "Backlog",
    "Requirements",
    "Architecture Options",
    "Architecture Selection",
    "Specification",
    "Repository Implementation",
    "Architecture Review",
    "Controlled Live Deployment",
    "Evidence",
    "Registry and Digital Twin Reconciliation",
    "Operational Validation",
    "Release",
    "Milestone Closeout",
    "Engineering Organization Evolution",
}


GitRunner = Callable[[list[str]], tuple[bool, str]]


def _default_git_runner(root: Path) -> GitRunner:
    def run(args: list[str]) -> tuple[bool, str]:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        return completed.returncode == 0, completed.stdout.strip()

    return run


def _metadata_value(text: str, field_name: str) -> str | None:
    match = re.search(rf"^\*\*{re.escape(field_name)}:\*\*\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def _table_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or line.count("|") < 3:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0] in {"Field", "----"} or set(cells[0]) <= {"-", ":"}:
            continue
        fields[cells[0]] = cells[1]
    return fields


def _domain(name: str, checks: list[ReadinessCheck]) -> ValidationDomain:
    if any(check.severity == ERROR for check in checks):
        status = "FAIL"
    elif any(check.severity == WARNING for check in checks):
        status = "PASS WITH WARNINGS"
    else:
        status = "PASS"
    return ValidationDomain(name, status, checks)


def _check_artifacts(root: Path, paths: tuple[str, ...], prefix: str) -> list[ReadinessCheck]:
    checks: list[ReadinessCheck] = []
    for relative in paths:
        exists = (root / relative).is_file()
        checks.append(
            ReadinessCheck(
                f"{prefix}.{Path(relative).stem}",
                PASS if exists else ERROR,
                f"Required artifact {'exists' if exists else 'is missing'}: {relative}",
                [relative],
            )
        )
    return checks


def _canonical_dependencies(value: str, workstream_names: tuple[str, ...]) -> set[str]:
    return {name for name in workstream_names if re.search(rf"\b{re.escape(name)}\b", value, re.IGNORECASE)}


def _dependency_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []
    cycles: set[tuple[str, ...]] = set()

    def canonical_cycle(nodes: list[str]) -> tuple[str, ...]:
        body = nodes[:-1]
        rotations = [tuple(body[index:] + body[:index]) for index in range(len(body))]
        chosen = min(rotations)
        return (*chosen, chosen[0])

    def visit(node: str) -> None:
        if node in visiting:
            start = stack.index(node)
            cycles.add(canonical_cycle(stack[start:] + [node]))
            return
        if node in visited:
            return
        visiting.add(node)
        stack.append(node)
        for target in sorted(graph.get(node, set())):
            visit(target)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in sorted(graph):
        visit(node)
    return [list(cycle) for cycle in sorted(cycles)]


class AISessionReadinessValidator:
    def __init__(
        self,
        root: Path,
        configuration: ReadinessConfiguration = DEFAULT_CONFIGURATION,
        git_runner: GitRunner | None = None,
        generated_at: Callable[[], str] | None = None,
    ) -> None:
        self.root = root.resolve()
        self.configuration = configuration
        self.git_runner = git_runner or _default_git_runner(self.root)
        self.generated_at = generated_at or (lambda: datetime.now(timezone.utc).isoformat())

    def validate(self) -> ReadinessResult:
        repository_domain, context = self._repository_identity()
        domains = [
            repository_domain,
            _domain(
                "Permanent Governance",
                _check_artifacts(self.root, self.configuration.permanent_governance, "governance"),
            ),
            _domain(
                "AI Collaboration Capability",
                _check_artifacts(
                    self.root,
                    self.configuration.collaboration_artifacts + self.configuration.templates,
                    "ai-collaboration",
                ),
            ),
            self._role_readiness(),
            self._active_milestone(),
        ]
        briefs, continuity_domain = self._workstream_continuity()
        domains.extend(
            [
                continuity_domain,
                self._architecture_traceability(briefs),
                self._parallel_consistency(briefs),
                self._readiness_freshness(briefs),
            ]
        )
        all_checks = [check for domain in domains for check in domain.checks]
        if any(check.severity == ERROR for check in all_checks):
            readiness = NOT_READY
        elif any(check.severity == WARNING for check in all_checks):
            readiness = READY_WITH_WARNINGS
        else:
            readiness = READY
        return ReadinessResult(
            capability="AI Session Readiness Validation",
            command="./platform-eap ai-session readiness",
            readiness=readiness,
            generated_at=self.generated_at(),
            repository=context,
            domains=domains,
        )

    def _repository_identity(self) -> tuple[ValidationDomain, RepositoryContext]:
        checks: list[ReadinessCheck] = []
        expected = self.configuration.expected_repository
        identity_ok = self.root.name == expected and (self.root / ".git").exists()
        checks.append(
            ReadinessCheck(
                "repository.identity",
                PASS if identity_ok else ERROR,
                f"Repository identity {'matches' if identity_ok else 'does not match'} expected {expected}.",
                [str(self.root)],
            )
        )
        branch_ok, branch_output = self.git_runner(["branch", "--show-current"])
        branch = branch_output.strip() if branch_ok and branch_output.strip() else None
        checks.append(
            ReadinessCheck(
                "repository.branch",
                PASS if branch else ERROR,
                f"Current branch: {branch}" if branch else "Current branch is not detectable; resolve detached or invalid Git state.",
            )
        )
        head_ok, head_output = self.git_runner(["rev-parse", "HEAD"])
        head = head_output.strip() if head_ok and re.fullmatch(r"[0-9a-fA-F]{7,40}", head_output.strip()) else None
        checks.append(
            ReadinessCheck(
                "repository.head",
                PASS if head else ERROR,
                f"Current HEAD: {head}" if head else "Current HEAD is not detectable; restore a valid repository baseline.",
            )
        )
        conflict_ok, conflicts = self.git_runner(["diff", "--name-only", "--diff-filter=U"])
        if not conflict_ok:
            checks.append(ReadinessCheck("repository.conflicts", ERROR, "Git conflict state could not be inspected."))
        elif conflicts:
            checks.append(
                ReadinessCheck(
                    "repository.conflicts",
                    ERROR,
                    "Unresolved merge conflicts prevent safe orientation.",
                    conflicts.splitlines(),
                )
            )
        else:
            checks.append(ReadinessCheck("repository.conflicts", PASS, "No unresolved merge conflicts detected."))
        status_ok, status_output = self.git_runner(
            ["status", "--short", "--", ".", ":!reports/engineering/ai_session_readiness"]
        )
        if not status_ok:
            working_tree = "unavailable"
            checks.append(ReadinessCheck("repository.working-tree", ERROR, "Working-tree state could not be inspected."))
        elif status_output:
            working_tree = "active source changes"
            checks.append(
                ReadinessCheck(
                    "repository.working-tree",
                    WARNING,
                    "Working tree has active source changes; preserve and reconcile them before editing.",
                    status_output.splitlines(),
                )
            )
        else:
            working_tree = "clean outside generated readiness reports"
            checks.append(ReadinessCheck("repository.working-tree", PASS, "Working tree is clean outside generated readiness reports."))
        return _domain("Repository Identity", checks), RepositoryContext(
            name=self.root.name,
            path=str(self.root),
            branch=branch,
            head=head,
            working_tree=working_tree,
        )

    def _role_readiness(self) -> ValidationDomain:
        path = self.root / self.configuration.role_catalog
        if not path.is_file():
            return _domain(
                "Role Readiness",
                [ReadinessCheck("roles.catalog", ERROR, "AI Role Catalog is missing.", [self.configuration.role_catalog])],
            )
        text = path.read_text(encoding="utf-8")
        headings = set(re.findall(r"^###\s+(.+?)\s*$", text, re.MULTILINE))
        checks = [
            ReadinessCheck("roles.catalog", PASS, "AI Role Catalog exists.", [self.configuration.role_catalog])
        ]
        for role in self.configuration.required_roles:
            exists = role in headings
            checks.append(
                ReadinessCheck(
                    f"roles.{re.sub(r'[^a-z0-9]+', '-', role.lower()).strip('-')}",
                    PASS if exists else ERROR,
                    f"Required role {'is governed' if exists else 'is missing from the AI Role Catalog'}: {role}",
                    [self.configuration.role_catalog],
                )
            )
        return _domain("Role Readiness", checks)

    def _active_milestone(self) -> ValidationDomain:
        checks: list[ReadinessCheck] = []
        milestone = self.configuration.active_milestone
        for name, relative in self.configuration.planning_artifacts.items():
            path = self.root / relative
            if not path.is_file():
                checks.append(ReadinessCheck(f"milestone.{name}", ERROR, f"Required planning artifact is missing: {relative}", [relative]))
                continue
            text = path.read_text(encoding="utf-8")
            if milestone not in text:
                checks.append(
                    ReadinessCheck(
                        f"milestone.{name}",
                        ERROR,
                        f"{relative} does not identify {milestone}.",
                        [relative],
                    )
                )
            else:
                checks.append(ReadinessCheck(f"milestone.{name}", PASS, f"{name.title()} identifies {milestone}.", [relative]))
            declared = _metadata_value(text, "Milestone")
            if declared and declared != milestone and name in {"roadmap", "backlog"}:
                checks.append(
                    ReadinessCheck(
                        f"milestone.{name}.metadata",
                        WARNING,
                        f"{relative} metadata still declares {declared} while its governed planning content includes {milestone}; reconcile the metadata when approved.",
                        [relative],
                    )
                )
        return _domain("Active Milestone Readiness", checks)

    def _workstream_continuity(self) -> tuple[dict[str, list[tuple[str, dict[str, str], str]]], ValidationDomain]:
        checks: list[ReadinessCheck] = []
        briefs: dict[str, list[tuple[str, dict[str, str], str]]] = {}
        continuity_root = self.root / self.configuration.continuity_root
        if not continuity_root.is_dir():
            checks.append(
                ReadinessCheck(
                    "continuity.root",
                    ERROR,
                    "Active milestone continuity directory is missing.",
                    [self.configuration.continuity_root],
                )
            )
            return briefs, _domain("Workstream Continuity", checks)
        for path in sorted(continuity_root.glob("*_Continuity_Brief.md")):
            text = path.read_text(encoding="utf-8")
            fields = _table_fields(text)
            identity = fields.get("Workstream ID and title", "")
            name = next((item.name for item in self.configuration.workstreams if identity.startswith(item.name)), identity.split(" - ", 1)[0])
            status = _metadata_value(text, "Status") or fields.get("Status", "")
            relative = str(path.relative_to(self.root))
            briefs.setdefault(name, []).append((status, fields, relative))
        required_fields = (
            "Repository",
            "Baseline",
            "Current milestone",
            "Workstream ID and title",
            "Assigned role",
            "Objective",
            "Current Engineering Lifecycle stage",
            "Authoritative artifacts",
            "Completed work and evidence",
            "Active repository changes",
            "Parallel workstreams",
            "Dependencies",
            "Integration gates",
            "Unresolved decisions",
            "Risks",
            "Stop conditions",
            "Permitted actions",
            "Prohibited actions",
            "Next gate",
            "Last verification date",
            "Superseded brief reference",
        )
        for requirement in self.configuration.workstreams:
            expected_path = f"{self.configuration.continuity_root}/{requirement.filename}"
            entries = briefs.get(requirement.name, [])
            expected_exists = (self.root / expected_path).is_file()
            checks.append(
                ReadinessCheck(
                    f"continuity.{requirement.name.lower().replace(' ', '-')}.exists",
                    PASS if expected_exists else ERROR,
                    f"{requirement.name} continuity brief {'exists' if expected_exists else 'is missing'}.",
                    [expected_path],
                )
            )
            active = [entry for entry in entries if entry[0] == "Active"]
            if len(active) != 1:
                checks.append(
                    ReadinessCheck(
                        f"continuity.{requirement.name.lower().replace(' ', '-')}.active",
                        ERROR,
                        f"{requirement.name} must have exactly one Active continuity brief; found {len(active)}.",
                        [entry[2] for entry in entries],
                    )
                )
            for status, fields, relative in entries:
                if status not in ALLOWED_BRIEF_STATES:
                    checks.append(ReadinessCheck("continuity.lifecycle-state", ERROR, f"Invalid continuity lifecycle state: {status or '<missing>'}.", [relative]))
                missing = [field_name for field_name in required_fields if not fields.get(field_name, "").strip()]
                for field_name in missing:
                    checks.append(
                        ReadinessCheck(
                            f"continuity.required-field.{re.sub(r'[^a-z0-9]+', '-', field_name.lower()).strip('-')}",
                            ERROR,
                            f"{requirement.name} continuity brief is missing required field: {field_name}.",
                            [relative],
                        )
                    )
                if not missing:
                    checks.append(ReadinessCheck("continuity.required-fields", PASS, f"{requirement.name} contains all required continuity fields.", [relative]))
        return briefs, _domain("Workstream Continuity", checks)

    def _architecture_traceability(self, briefs: dict[str, list[tuple[str, dict[str, str], str]]]) -> ValidationDomain:
        checks: list[ReadinessCheck] = []
        planning_text: dict[str, str] = {}
        for name, relative in self.configuration.planning_artifacts.items():
            path = self.root / relative
            planning_text[name] = path.read_text(encoding="utf-8") if path.is_file() else ""
        for requirement in self.configuration.workstreams:
            active = [entry for entry in briefs.get(requirement.name, []) if entry[0] == "Active"]
            if not active:
                continue
            _, fields, relative = active[0]
            authoritative = fields.get("Authoritative artifacts", "")
            for token in requirement.authoritative_tokens:
                present = token in authoritative
                checks.append(
                    ReadinessCheck(
                        f"traceability.{requirement.name.lower().replace(' ', '-')}.authority",
                        PASS if present else ERROR,
                        f"{requirement.name} {'traces' if present else 'does not trace'} to authoritative evidence: {token}.",
                        [relative],
                    )
                )
            for artifact_name, tokens in requirement.planning_tokens.items():
                relative_plan = self.configuration.planning_artifacts[artifact_name]
                for token in tokens:
                    present = token in planning_text[artifact_name]
                    checks.append(
                        ReadinessCheck(
                            f"traceability.{requirement.name.lower().replace(' ', '-')}.{artifact_name}",
                            PASS if present else ERROR,
                            f"{requirement.name} {'is' if present else 'is not'} traceable through {artifact_name}: {token}.",
                            [relative_plan],
                        )
                    )
        return _domain("Architecture Traceability", checks)

    def _parallel_consistency(self, briefs: dict[str, list[tuple[str, dict[str, str], str]]]) -> ValidationDomain:
        checks: list[ReadinessCheck] = []
        names = tuple(requirement.name for requirement in self.configuration.workstreams)
        graph: dict[str, set[str]] = {}
        for requirement in self.configuration.workstreams:
            active = [entry for entry in briefs.get(requirement.name, []) if entry[0] == "Active"]
            if not active:
                continue
            _, fields, relative = active[0]
            dependencies = _canonical_dependencies(fields.get("Dependencies", ""), names)
            dependencies.discard(requirement.name)
            graph[requirement.name] = dependencies
            for required in requirement.required_dependencies:
                present = required in dependencies
                checks.append(
                    ReadinessCheck(
                        f"parallel.{requirement.name.lower().replace(' ', '-')}.dependency",
                        PASS if present else ERROR,
                        f"{requirement.name} {'retains' if present else 'is missing'} required dependency: {required}.",
                        [relative],
                    )
                )
            assigned = fields.get("Assigned role", "")
            if requirement.name == "Architecture Integration":
                gatekeeper = "Architecture Gatekeeper" in assigned
                stage = fields.get("Current Engineering Lifecycle stage", "").split(";", 1)[0].strip().rstrip(".")
                checks.append(
                    ReadinessCheck(
                        "parallel.architecture-integration.authority",
                        PASS if gatekeeper and stage == "Architecture Review" else ERROR,
                        "Architecture Integration retains the Architecture Gatekeeper coordination path."
                        if gatekeeper and stage == "Architecture Review"
                        else "Architecture Integration must retain Architecture Gatekeeper ownership and the Architecture Review stage.",
                        [relative],
                    )
                )
            if requirement.name in {"Alpha", "Bravo", "Charlie"}:
                combined = " ".join(
                    [
                        fields.get("Completed work and evidence", ""),
                        fields.get("Current work", ""),
                        fields.get("Objective", ""),
                    ]
                ).lower()
                false_start = bool(re.search(r"\bimplementation (?:work )?has started\b", combined))
                checks.append(
                    ReadinessCheck(
                        f"parallel.{requirement.name.lower()}.implementation-state",
                        ERROR if false_start else PASS,
                        f"{requirement.name} does not falsely claim implementation has begun."
                        if not false_start
                        else f"{requirement.name} claims implementation has begun while planning records it as unstarted.",
                        [relative],
                    )
                )
        for cycle in _dependency_cycles(graph):
            checks.append(
                ReadinessCheck(
                    "parallel.circular-dependency",
                    ERROR,
                    f"Circular active-workstream dependency detected: {' -> '.join(cycle)}.",
                    [entry[2] for values in briefs.values() for entry in values if entry[0] == "Active"],
                )
            )
        if not any(check.check_id == "parallel.circular-dependency" for check in checks):
            checks.append(ReadinessCheck("parallel.circular-dependency", PASS, "No circular active-workstream dependency detected."))
        kanban_path = self.root / self.configuration.planning_artifacts["kanban"]
        if kanban_path.is_file():
            kanban = kanban_path.read_text(encoding="utf-8")
            for name in ("Alpha", "Bravo", "Charlie"):
                workstream_rows = [
                    line for line in kanban.splitlines() if line.startswith("|") and f"{name} -" in line
                ]
                if name == "Alpha":
                    eo_14_1a = [line.lower() for line in workstream_rows if "| eo-14.1a |" in line.lower()]
                    eo_14_4a = [line.lower() for line in workstream_rows if "| eo-14.4a |" in line.lower()]
                    planning_state_ok = (
                        len(eo_14_1a) == 1
                        and "repository implementation complete" in eo_14_1a[0]
                        and len(eo_14_4a) == 1
                        and "repository implementation complete and published" in eo_14_4a[0]
                        and "architecture gatekeeper approved" in eo_14_4a[0]
                    )
                    warning_message = (
                        "Kanban does not preserve EO-14.1A and EO-14.4A as published repository "
                        "implementations with automation unactivated."
                    )
                elif name == "Bravo":
                    plat_14_1a = [line.lower() for line in workstream_rows if "| plat-14.1a |" in line.lower()]
                    published_state = (
                        len(plat_14_1a) == 1
                        and "done; architecture gatekeeper accepted / published / fixture only / unactivated" in plat_14_1a[0]
                        and "implementation accepted and published" in plat_14_1a[0]
                    )
                    source_review_state = (
                        len(plat_14_1a) == 1
                        and "architecture review; source foundation complete / unpublished" in plat_14_1a[0]
                        and "published fixture-only/unactivated foundations and architecture remain accepted" in plat_14_1a[0]
                        and "pending architecture gatekeeper publication decision" in plat_14_1a[0]
                    )
                    source_published_state = (
                        len(plat_14_1a) == 1
                        and "architecture review; transport-free source published" in plat_14_1a[0]
                        and "architecture gatekeeper approved, accepted, and published" in plat_14_1a[0]
                        and "socket-capable privileged proxy implementation review" in plat_14_1a[0]
                    )
                    planning_state_ok = (
                        published_state or source_review_state or source_published_state
                    )
                    warning_message = (
                        "Kanban does not preserve the PLAT-14.1A published fixture-only/unactivated "
                        "baseline and current Architecture Gatekeeper source-publication state."
                    )
                else:
                    planning_state_ok = bool(workstream_rows) and all(
                        "implementation not started" in line.lower() for line in workstream_rows
                    )
                    warning_message = f"Kanban does not clearly preserve {name}'s unstarted implementation state."
                if not planning_state_ok:
                    checks.append(
                        ReadinessCheck(
                            f"parallel.{name.lower()}.planning-state",
                            WARNING,
                            warning_message,
                            [self.configuration.planning_artifacts["kanban"]],
                        )
                    )
        return _domain("Parallel Workstream Consistency", checks)

    def _readiness_freshness(self, briefs: dict[str, list[tuple[str, dict[str, str], str]]]) -> ValidationDomain:
        checks: list[ReadinessCheck] = []
        catalog_path = self.root / self.configuration.role_catalog
        catalog = catalog_path.read_text(encoding="utf-8") if catalog_path.is_file() else ""
        governed_roles = set(re.findall(r"^###\s+(.+?)\s*$", catalog, re.MULTILINE))
        for requirement in self.configuration.workstreams:
            active = [entry for entry in briefs.get(requirement.name, []) if entry[0] == "Active"]
            if not active:
                continue
            status, fields, relative = active[0]
            assigned = fields.get("Assigned role", "")
            referenced_roles = [role for role in governed_roles if role in assigned]
            role_clauses = [clause.strip() for clause in assigned.split(";") if clause.strip()]
            unknown_role_clauses = [
                clause for clause in role_clauses if not any(role in clause for role in governed_roles)
            ]
            roles_valid = bool(referenced_roles) and not unknown_role_clauses
            checks.append(
                ReadinessCheck(
                    f"freshness.{requirement.name.lower().replace(' ', '-')}.role",
                    PASS if roles_valid else ERROR,
                    f"{requirement.name} assigned role is governed: {', '.join(sorted(referenced_roles))}."
                    if roles_valid
                    else f"{requirement.name} has an invalid assigned role reference: {', '.join(unknown_role_clauses) or assigned or '<missing>'}.",
                    [relative, self.configuration.role_catalog],
                )
            )
            stage = fields.get("Current Engineering Lifecycle stage", "").split(";", 1)[0].strip().rstrip(".")
            checks.append(
                ReadinessCheck(
                    f"freshness.{requirement.name.lower().replace(' ', '-')}.stage",
                    PASS if stage in ALLOWED_ENGINEERING_STAGES else ERROR,
                    f"{requirement.name} Engineering Lifecycle stage {'is valid' if stage in ALLOWED_ENGINEERING_STAGES else 'is invalid'}: {stage or '<missing>'}.",
                    [relative],
                )
            )
            next_gate = fields.get("Next gate", "").strip()
            checks.append(
                ReadinessCheck(
                    f"freshness.{requirement.name.lower().replace(' ', '-')}.next-gate",
                    PASS if next_gate and next_gate.upper() != "TBD" else ERROR,
                    f"{requirement.name} next gate is present." if next_gate and next_gate.upper() != "TBD" else f"{requirement.name} next gate is missing or unresolved.",
                    [relative],
                )
            )
            verification = fields.get("Last verification date", "").strip().rstrip(".")
            try:
                date.fromisoformat(verification)
                valid_date = True
            except ValueError:
                valid_date = False
            checks.append(
                ReadinessCheck(
                    f"freshness.{requirement.name.lower().replace(' ', '-')}.verification",
                    PASS if valid_date else ERROR,
                    f"{requirement.name} freshness evidence is present: {verification}."
                    if valid_date
                    else f"{requirement.name} last verification date is missing or invalid.",
                    [relative],
                )
            )
            repository = fields.get("Repository", "")
            baseline = fields.get("Baseline", "")
            identity_ok = self.configuration.expected_repository in repository and bool(
                re.search(r"\bHEAD\b[^0-9a-fA-F]*[0-9a-fA-F]{7,40}\b", baseline)
            )
            checks.append(
                ReadinessCheck(
                    f"freshness.{requirement.name.lower().replace(' ', '-')}.baseline",
                    PASS if identity_ok else ERROR,
                    f"{requirement.name} repository identity and baseline evidence are present."
                    if identity_ok
                    else f"{requirement.name} repository identity or HEAD baseline evidence is missing.",
                    [relative],
                )
            )
            for entry_status, entry_fields, entry_relative in briefs.get(requirement.name, []):
                superseded = entry_fields.get("Superseded brief reference", "").strip()
                none_value = superseded.lower().rstrip(".") in {"none", "n/a", "not applicable"}
                supersession_ok = (entry_status == "Superseded" and superseded and not none_value) or (
                    entry_status != "Superseded" and (not superseded or none_value)
                )
                checks.append(
                    ReadinessCheck(
                        f"freshness.{requirement.name.lower().replace(' ', '-')}.supersession",
                        PASS if supersession_ok else ERROR,
                        f"{requirement.name} supersession fields are consistent with {entry_status}."
                        if supersession_ok
                        else f"{requirement.name} supersession fields conflict with lifecycle state {entry_status}.",
                        [entry_relative],
                    )
                )
        return _domain("Readiness and Freshness", checks)


def write_readiness_report(result: ReadinessResult, report_root: Path) -> tuple[Path, Path]:
    report_root.mkdir(parents=True, exist_ok=True)
    markdown_path = report_root / "ai_session_readiness_report.md"
    json_path = report_root / "ai_session_readiness_report.json"
    lines = [
        "# Platform EAP Report - AI Session Readiness",
        "",
        f"**Readiness:** {result.readiness}",
        "",
        f"**Timestamp:** {result.generated_at}",
        "",
        f"**Command:** `{result.command}`",
        "",
        "## Repository State",
        "",
        f"- Repository: `{result.repository.name}`",
        f"- Path: `{result.repository.path}`",
        f"- Branch: `{result.repository.branch or 'unavailable'}`",
        f"- HEAD: `{result.repository.head or 'unavailable'}`",
        f"- Working tree: {result.repository.working_tree}",
        "",
        "## Counts",
        "",
        f"- Errors: {len(result.errors)}",
        f"- Warnings: {len(result.warnings)}",
    ]
    for domain in result.domains:
        lines.extend(["", f"## {domain.name}", "", f"**Status:** {domain.status}", ""])
        for check in domain.checks:
            evidence = f" Evidence: {', '.join(f'`{item}`' for item in check.evidence)}." if check.evidence else ""
            lines.append(f"- {check.severity}: {check.message}{evidence}")
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    payload = asdict(result)
    payload["errors"] = [asdict(check) for check in result.errors]
    payload["warnings"] = [asdict(check) for check in result.warnings]
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return markdown_path, json_path
