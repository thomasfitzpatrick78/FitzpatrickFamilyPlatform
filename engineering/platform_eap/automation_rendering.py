from __future__ import annotations

from collections.abc import Sequence

from engineering.platform_eap.automation_capability import AutomationHandoff


def _text(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\r", " ").replace("\n", " ")


def _items(values: Sequence[str], empty: str = "None") -> list[str]:
    return [f"- {_text(value)}" for value in values] if values else [f"- {empty}"]


def render_automation_handoff_markdown(handoff: AutomationHandoff) -> str:
    lines = [
        "# Governed Automation Human-Review Handoff",
        "",
        f"**Model version:** `{handoff.model_version}`",
        "",
        f"**Automation:** `{_text(handoff.automation_id)}`",
        "",
        f"**Run:** `{_text(handoff.run_id)}`",
        "",
        f"**Lifecycle state:** `{handoff.current_lifecycle_state.value}`",
        "",
        "## Completed Steps",
        "",
        *_items(handoff.completed_step_ids),
        "",
        "## Pending Steps",
        "",
        *_items(handoff.pending_step_ids),
        "",
        "## EO-14.1A References",
        "",
        *_items(tuple(f"Assignment: {value}" for value in handoff.assignment_ids)),
        *_items(tuple(f"Completion: {value}" for value in handoff.completion_assignment_ids)),
        *_items(tuple(f"Evidence: {value}" for value in handoff.evidence_references)),
        "",
        "## Validation Findings",
        "",
    ]
    if handoff.validation_findings:
        lines.extend(f"- {finding.severity.value} `{_text(finding.code)}`: {_text(finding.message)}" for finding in handoff.validation_findings)
    else:
        lines.append("- None")
    lines.extend([
        "",
        "## Blocking Issues",
        "",
        *_items(handoff.blocking_issues),
        "",
        "## Human Approvals",
        "",
        *_items(tuple(f"Received: {value}" for value in handoff.approvals_received)),
        *_items(tuple(f"Still required: {value}" for value in handoff.approvals_required), "Still required: None"),
        "",
        "## Activation and Live-Change Declarations",
        "",
        f"- Activation occurred: {'yes' if handoff.activation_occurred else 'no'}",
        f"- Live changes occurred: {'yes' if handoff.live_changes_occurred else 'no'}",
        "",
        "## Recommended Next Approval Gate",
        "",
        _text(handoff.recommended_next_approval_gate),
        "",
        "This handoff is advisory and does not authorize its own next step.",
        "",
    ])
    return "\n".join(lines)
