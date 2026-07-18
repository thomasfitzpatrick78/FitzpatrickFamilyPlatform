# Engineering Metrics v2

**Document Version:** 1.2

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
| AI collaboration readiness | Governed AI Session Readiness JSON report. | Implemented organizational-onboarding health measure through EO-14.8E. |
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
- AI collaboration readiness must consume the governed validator report without recalculating readiness or silently regenerating the report.
- AI collaboration readiness must remain a state measure and must not be converted to a percentage, weighted score, or inferred trend.
- Missing, malformed, invalid, timestamp-less, or logically inconsistent evidence must be represented as `UNKNOWN`, never as healthy.

---

## Acceptance Criteria

EO-14.3 is ready for review when:

- Metrics are tied to observable repository or operational evidence.
- Immature metrics are identified as candidate or qualitative.
- Investment allocation across EO, PLAT, and FFFA is explicitly represented.
- Metrics do not require new runtime systems or personal data.
- AI collaboration readiness is traceable to the governed validator evidence and preserves readiness state, finding counts, validation-domain count, timestamp, evidence condition, report path, usability, and onboarding effect.

---

## AI Session Readiness Metric Classification

AI Session Readiness is an Engineering Organization organizational-onboarding health measure.

| Classification | Governed Values |
|----------------|-----------------|
| State measure | `READY`, `READY WITH WARNINGS`, `NOT READY`, `UNKNOWN`. |
| Supporting counts | Readiness errors, readiness warnings, and validation domains evaluated. |
| Evidence condition | `current`, `unavailable`, or `malformed`; `stale` may be added only if a future governed freshness threshold exists. |
| Onboarding effect | Nonblocking, nonblocking with disclosed conditions, blocking, or unknown. |

The source of truth remains `./platform-eap ai-session readiness` and its governed Markdown and JSON reports. Engineering Metrics reads the latest governed JSON report. It does not call validator internals, alter the source report, remediate findings, or inspect conversation content.

No arbitrary time-based staleness threshold is governed. Evidence is usable only when the JSON report is available, parseable, contains a valid readiness state and timestamp, preserves structured domains and findings, and is logically consistent with its finding counts.

EO-14.8E is implemented and awaiting Architecture Gatekeeper review. EO-14.8 parent capability implementation is complete pending final review. Alpha, Bravo, and Charlie remain unstarted, and no live infrastructure work is authorized.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Classified and integrated governed AI Session Readiness evidence through EO-14.8E without duplicating validator logic. |
| 1.1 | Added candidate AI collaboration readiness metric and EO-14.8E boundary. |
| 1.0 | Initial Engineering Metrics v2 specification. |
