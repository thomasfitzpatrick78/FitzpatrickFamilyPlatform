# Engineering Metrics v2

**Document Version:** 1.0

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** EO-14.3

---

## Purpose

Engineering Metrics v2 defines practical, evidence-based measures for the AI-Operated Engineering Organization.

Metrics must improve decision quality without creating false precision where repository evidence does not yet exist.

---

## Metric Set

| Measure | Evidence Source | Initial Treatment |
|---------|-----------------|-------------------|
| Lead time | Milestone artifacts, git history, release evidence. | Candidate until issue/work-package timestamps are consistent. |
| Cycle time | Work package start and closeout evidence. | Candidate. |
| Throughput | Completed governed work packages per milestone. | Quantitative where closeout evidence exists. |
| Automation coverage | EAP capabilities and validation commands. | Quantitative with capability list and command results. |
| Governance coverage | Required governance artifacts present and linked. | Qualitative plus checklist evidence. |
| Validation coverage | Tests and validators attempted for changed areas. | Quantitative command results with qualitative gaps. |
| Technical debt | Architecture backlog, review findings, deferred decisions. | Qualitative register until formal debt taxonomy exists. |
| Documentation freshness | Document version, milestone, and revision history. | Qualitative. |
| Platform health | Validated dashboard and operational evidence. | Qualitative until PLAT-14.3 defines source boundaries. |
| Customer-facing delivery | Persona, channel, value, and acceptance evidence. | Required milestone traceability. |
| AI contribution | Work package evidence produced by governed AI roles. | Qualitative until role activation data exists. |
| Rework | Reopened work or validation-driven corrections. | Candidate. |
| Escaped defects | Post-closeout defects or production incidents. | Candidate. |
| Investment allocation | EO, PLAT, and FFFA planned/completed work packages. | Quantitative count with qualitative effort notes. |

---

## Rules

- Do not infer calendar measures from incomplete evidence.
- Prefer ranges, counts, and review notes over unsupported precision.
- Distinguish planned, attempted, passed, failed, and deferred validation.
- Include customer-facing value evidence for every milestone.
- Keep metrics repository-derived unless a future approved data source is added.

---

## Acceptance Criteria

EO-14.3 is ready for review when:

- Metrics are tied to observable repository or operational evidence.
- Immature metrics are identified as candidate or qualitative.
- Investment allocation across EO, PLAT, and FFFA is explicitly represented.
- Metrics do not require new runtime systems or personal data.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial Engineering Metrics v2 specification. |
