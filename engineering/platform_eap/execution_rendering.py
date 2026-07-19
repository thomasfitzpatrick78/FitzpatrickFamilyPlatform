from __future__ import annotations

from collections.abc import Sequence

from engineering.platform_eap.execution_capability import CompletionPackage


def _markdown_text(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\r", " ")
        .replace("\n", " ")
    )


def _markdown_list(values: Sequence[str], empty: str = "None") -> list[str]:
    if not values:
        return [f"- {empty}"]
    return [f"- {_markdown_text(value)}" for value in values]


def render_completion_markdown(package: CompletionPackage) -> str:
    result = package.execution_result
    lines = [
        "# Governed Execution Completion Package",
        "",
        f"**Model version:** `{package.model_version}`",
        "",
        f"**Assignment:** `{_markdown_text(package.assignment.assignment_id)}` - {_markdown_text(package.assignment.title)}",
        "",
        f"**Participant:** `{_markdown_text(package.participant.participant_id)}`",
        "",
        f"**Governed role:** `{package.assignment.governed_role.value}`",
        "",
        f"**Outcome:** `{result.outcome_status.value}`",
        "",
        "## Summary",
        "",
        _markdown_text(result.summary),
        "",
        "## Actions Performed",
        "",
        *_markdown_list(result.actions_performed),
        "",
        "## Files Changed",
        "",
        *_markdown_list(result.files_changed),
        "",
        "## Validations Executed",
        "",
        *_markdown_list(result.validations_executed),
        "",
        "## Evidence Inventory",
        "",
    ]
    if package.evidence_inventory:
        for evidence in package.evidence_inventory:
            artifact = (
                f"; artifact `{_markdown_text(evidence.artifact_path)}`"
                if evidence.artifact_path
                else ""
            )
            lines.append(
                f"- `{_markdown_text(evidence.evidence_id)}`: "
                f"{evidence.evidence_type.value}; {_markdown_text(evidence.result)}{artifact}"
            )
    else:
        lines.append("- None")
    lines.extend(["", "## Validation Findings", ""])
    if package.validation_findings:
        for finding in package.validation_findings:
            lines.append(
                f"- {finding.severity.value} `{_markdown_text(finding.code)}`: "
                f"{_markdown_text(finding.message)}"
            )
    else:
        lines.append("- None recorded")
    lines.extend(
        [
            "",
            "## Unresolved Issues and Decisions",
            "",
            *_markdown_list((*result.unresolved_issues, *package.unresolved_decisions)),
            "",
            "## Deviations or Escalations",
            "",
            *_markdown_list(result.deviations_or_escalations),
            "",
            "## Repository and Live-Action Declarations",
            "",
            f"- Commit occurred: {'yes' if package.commit_occurred else 'no'}",
            f"- Push occurred: {'yes' if package.push_occurred else 'no'}",
            f"- Activation occurred: {'yes' if package.activation_occurred else 'no'}",
            f"- Live changes occurred: {'yes' if package.live_changes_occurred else 'no'}",
            "",
            "## Recommended Next Approval Gate",
            "",
            _markdown_text(package.recommended_next_approval_gate),
            "",
            "This recommendation is advisory and does not authorize the next lifecycle step.",
            "",
        ]
    )
    return "\n".join(lines)
