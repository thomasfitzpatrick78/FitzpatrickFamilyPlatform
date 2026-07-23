# Platform EAP Report - Engineering Metrics

**Status:** PASS WITH WARNINGS

**Timestamp:** 2026-07-23T00:23:02.294113+00:00

**Summary:** Engineering metrics generated with status PASS WITH WARNINGS; AI Session Readiness is READY WITH WARNINGS.

## Counts

- Errors: 0
- Warnings: 1
- Information: 4

## AI Session Readiness

- Overall readiness: READY WITH WARNINGS
- Errors: 0
- Warnings: 1
- Validation domains: 9
- Evidence timestamp: 2026-07-23T00:22:59.638018+00:00
- Evidence condition: current
- Evidence path: `reports/engineering/ai_session_readiness/ai_session_readiness_report.json`
- Evidence usable: yes
- Onboarding effect: NONBLOCKING WITH CONDITIONS
- Interpretation: Orientation may proceed only with the reported conditions disclosed and reconciled.
- Caveat: Warnings remain authoritative in the source readiness report and are not remediated by Engineering Metrics.
- Source of truth: `./platform-eap ai-session readiness` and its governed Markdown and JSON reports.

## Results

- INFO: Markdown documents: 137
- INFO: Engineering test files: 8
- INFO: Architecture decisions: 11
- INFO: Engineering health baseline established
- WARNING: AI Session Readiness: READY WITH WARNINGS; evidence current; onboarding effect NONBLOCKING WITH CONDITIONS (`reports/engineering/ai_session_readiness/ai_session_readiness_report.json`)
