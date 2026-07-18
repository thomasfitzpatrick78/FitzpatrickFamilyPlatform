# AI Session Readiness Validator Specification

**Document Version:** 1.2

**Status:** Implemented; Awaiting Architecture Gatekeeper Review

**Milestone:** EO-14.8D

---

## Purpose

This specification governs the implemented AI Session Readiness Validator.

The command is:

```text
./platform-eap ai-session readiness
```

EO-14.8D implements a reusable validation engine, Platform EAP routing, structured results, Markdown and JSON reports, and focused tests. Architecture Gatekeeper approval remains pending.

---

## Validator Boundary

The validator must assess repository readiness for onboarding an AI participant.

The validator must not inspect, score, or validate conversation content.

---

## Validation Domains

| Domain | Expected Assessment |
|--------|---------------------|
| Repository identity | Expected repository, branch, HEAD, and working-tree status are available. |
| Permanent governance | Required permanent governance artifacts are present. |
| AI Collaboration Governance artifacts | Charter, specification, lifecycle, standards, Steward specification, and continuity specification are present. |
| AI Role Catalog | Assigned role is valid and lifecycle state is known. |
| Active milestone artifacts | Milestone plan, roadmap, backlog, and Kanban are present and internally consistent. |
| Workstream continuity | Required active continuity briefs and required fields are present and valid. |
| Architecture traceability | Workstream has required architecture or specification references. |
| Role validity | Role authority and prohibited actions are traceable. |
| Dependency and integration-gate consistency | Dependencies and integration gates are not contradictory. |
| Duplicate or conflicting active briefs | No more than one brief is Active for a workstream. |
| Missing next gates | Workstream has a defined next lifecycle or review gate. |
| Readiness and freshness | Last verification and baseline evidence are present and internally consistent without imposing an unapproved age threshold. |

---

## Outcomes

| Outcome | Meaning |
|---------|---------|
| READY | Repository evidence supports onboarding an AI participant. |
| READY WITH WARNINGS | Repository evidence is sufficient, but nonblocking warnings require disclosure. |
| NOT READY | Blocking repository condition prevents governed onboarding. |

The validator must not produce percentage scores.

---

## Report Expectations

Reports record:

- command name;
- timestamp;
- repository identity;
- outcome;
- counts by severity;
- validation-domain results;
- warnings;
- errors;
- next-gate findings.

Reports use `reports/engineering/ai_session_readiness/` and remain the source evidence consumed by the implemented EO-14.8E metrics integration.

EO-14.8E consumes the governed JSON report through the public Engineering Metrics capability. The validator remains authoritative for readiness calculation. Engineering Metrics and Platform Health visibility must not duplicate validator checks, regenerate the report as a hidden side effect, alter readiness evidence, or remediate findings.

---

## Testing Requirements

EO-14.8D includes focused tests for:

- READY outcome;
- READY WITH WARNINGS outcome;
- NOT READY outcome;
- missing required artifact;
- invalid role reference;
- duplicate Active brief condition after continuity briefs are implemented;
- missing or invalid freshness evidence without an arbitrary expiration rule;
- no conversation-content inspection.

---

## Non-Goals

- Initializing an AI session.
- Creating, modifying, or superseding continuity briefs.
- Remediating readiness findings.
- Validating chat prompts or conversation content.
- Evaluating AI model quality.
- Authorizing implementation, release, or live execution.
- Calculating Engineering Metrics or Platform Health independently of the governed readiness report.

---

## Related Documents

- [AI Collaboration Governance Capability Charter](AI_Collaboration_Governance_Capability_Charter.md)
- [AI Collaboration Governance Specification](AI_Collaboration_Governance_Specification.md)
- [AI Session Initialization Standard](AI_Session_Initialization_Standard.md)
- [Workstream Continuity Brief Specification](Workstream_Continuity_Brief_Specification.md)
- [Governed Automation Framework](../Governed_Automation_Framework.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.2 | Recorded EO-14.8E read-only report consumption while retaining validator source-of-truth authority. |
| 1.1 | Recorded EO-14.8D implementation, report location, validation domains, tests, and non-remediation boundary. |
| 1.0 | Initial future AI Session Readiness Validator specification. |
