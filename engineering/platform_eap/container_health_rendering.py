from __future__ import annotations

from collections.abc import Sequence

from engineering.platform_eap.container_health import OperationalHealthAssessment


def _text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("`", "\\`").replace("\r", " ").replace("\n", " ")


def _items(values: Sequence[str], empty: str = "None") -> list[str]:
    if not values:
        return [f"- {empty}"]
    return [f"- `{_text(value)}`" for value in values]


def render_assessment_markdown(assessment: OperationalHealthAssessment) -> str:
    mandatory = [item for item in assessment.evidence_summary if item.role == "mandatory"]
    advisory = [item for item in assessment.evidence_summary if item.role == "advisory"]
    constraining = [item for item in assessment.evidence_summary if item.role == "constraining"]
    limitations = sorted({code for item in assessment.evidence_summary for code in item.finding_codes if "limitation" in code})

    def summaries(items) -> list[str]:
        if not items:
            return ["- None"]
        return [
            f"- `{_text(item.evidence_id)}` — `{_text(item.signal_name)}`; freshness `{item.freshness_status.value}`; "
            f"confidence `{item.evidence_confidence.value}`; observed `{_text(item.observed_at)}`; expires `{_text(item.expires_at)}`"
            for item in items
        ]

    lines = [
        "# Container Operational Health Assessment",
        "",
        f"- Assessment ID: `{_text(assessment.assessment_id)}`",
        f"- Contract version: `{_text(assessment.contract_version)}`",
        f"- Subject ID: `{_text(assessment.subject_id)}`",
        f"- Registry reference: `{_text(assessment.registry_reference)}`",
        f"- Evidence profile: `{_text(assessment.evidence_profile_type)}:{_text(assessment.evidence_profile_version)}`",
        f"- Health status: `{assessment.health_status.value}`",
        f"- Assessment confidence: `{assessment.assessment_confidence.value}`",
        f"- Evaluated at: `{_text(assessment.evaluated_at)}`",
        f"- Valid until: `{_text(assessment.valid_until) if assessment.valid_until else 'not applicable'}`",
        f"- Fixture only: `{'true' if assessment.fixture_only else 'false'}`",
        f"- Activation status: `{_text(assessment.activation_status)}`",
        "",
        "## Policy Trace",
        "",
        f"- Manifest: `{_text(assessment.policy_manifest_id)}:{_text(assessment.policy_manifest_version)}`",
        f"- Health policy: `{_text(assessment.health_policy_version)}`",
        f"- Assessment confidence policy: `{_text(assessment.assessment_confidence_policy_version)}`",
        "",
        "### Constituent Policies",
        "",
        *_items(assessment.policy_versions),
        "",
        "## Evidence Trace",
        "",
        f"- Reconciliation ID: `{_text(assessment.reconciliation_id)}`",
        f"- Reconciliation result: `{assessment.reconciliation_result.value}`",
        "",
        "### Mandatory Evidence",
        "",
        *summaries(mandatory),
        "",
        "### Advisory Evidence",
        "",
        *summaries(advisory),
        "",
        "### Constraining Evidence",
        "",
        *summaries(constraining),
        "",
        "### Provider Limitations",
        "",
        *_items(limitations),
        "",
        "## Reason Codes",
        "",
        *_items(assessment.reason_codes),
        "",
        "## Critical Findings",
        "",
        *_items(assessment.critical_findings),
        "",
        "## Noncritical Findings",
        "",
        *_items(assessment.noncritical_findings),
        "",
        "Repository fixture evidence does not establish live provider compatibility, activation, or infrastructure authority.",
        "",
    ]
    return "\n".join(lines)
