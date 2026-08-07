# Engineering Principles

**Document Version:** 1.1

**Status:** Active

**Milestone:** EO-13.1

---

## Purpose

This document translates the Engineering Organization manifesto into enforceable engineering principles for repository, architecture, automation, operations, and milestone governance.

---

## Principles

### Repository First

The repository is the authoritative engineering record. Decisions, requirements, architecture, specifications, tests, evidence, and closeout records become durable only when represented in governed repository artifacts.

### Evidence Before Assumption

Operational evidence, telemetry, tests, validation output, and inspected repository state supersede unsupported assumptions.

### Architecture Before Implementation

Implementation follows approved requirements, architecture options, architecture selection, specifications, security boundaries, and validation criteria.

### Human Approval Before Production

AI may recommend, prepare, validate, and execute within authorized boundaries. Production changes require explicit human authorization until a separately governed approval model is approved.

### Governed Automation

Automation executes approved architecture and runbooks. Automation must preserve stop conditions, approval gates, evidence capture, and rollback expectations.

### Least Privilege

Services, agents, users, tokens, sockets, and integrations receive only the access required for approved scope. Privileged integrations require explicit review.

### Observable by Design

Operational capabilities define telemetry, dashboards, evidence templates, health expectations, and validation before lifecycle promotion.

### Platform Before Duplication

Shared Platform capabilities should absorb reusable concerns when doing so reduces repeated work without coupling unrelated products or bypassing repository boundaries.

### Customer Value Every Milestone

Every milestone must measurably strengthen the Engineering Organization, the Shared Platform, and at least one customer-facing application unless a governed exception is approved.

### Reusable Practices Become Governance

Repeated successful practices must be evaluated for promotion into governed artifacts such as templates, standards, lifecycle gates, tests, or role definitions.

### Strategic Architecture Quality

Material architecture choices should prefer maintainability, quality, security, and reduced rework over short-term convenience. Commercial- or industrial-grade patterns should be considered where practical.

### Multiple-Option Architecture Evaluation

Meaningful architecture decisions require option evaluation before selection, including tradeoffs, rejected options, and consequences.

### Current-State and Planned-State Separation

Documents, registry records, dashboards, and reports must distinguish implemented current state from planned or prepared future state.

### Safe Rollback and Stop Conditions

Live runbooks must include stop conditions, rollback paths, non-goals, and evidence checkpoints before execution is authorized.

### Continuous Organizational Improvement

The Engineering Organization is itself improved through measured capability evolution, closeout learning, and roadmap feedback.

---

## Historical EO-15.2 Phase A Risk-Tiered Delivery Principles

These clauses interpret already-bound Phase A packages only. They are superseded prospectively by the Bounded-Outcome Principles below.

- Preserve distinct evidence for every lifecycle phase without requiring a separate Owner decision when outcome, scope, risk, authority, and intended effect remain unchanged.
- Continue automatically through accepted Tier 0 and Tier 1 work and explicitly bundled Tier 2 work.
- Require fresh pre-action human approval for Tier 3 product, architecture, protected-data, destructive, publication, production, release, and live actions.
- Present only material Owner decisions in plain language with the recommendation first and two or three genuine options scored High, Medium, or Low for commercial architecture, maintainability, and code quality.
- Use one accountable main writer and bounded read-only specialists; assignment and evidence never transfer authority.

---

## Related Documents

- [Engineering Organization Manifesto](../engineering-organization/Engineering_Organization_Manifesto.md)
- [Permanent Project Operating Model](Permanent_Project_Operating_Model.md)
- [Engineering Lifecycle](Engineering_Lifecycle.md)
- [Definition of Done](Definition_of_Done.md)
- [Privileged Infrastructure Integration Standard](Privileged_Infrastructure_Integration_Standard.md)

---

## Bounded-Outcome Principles

- Govern the approved result and its material boundaries, not every routine technical step.
- Continue automatically inside a valid envelope; never ask the Owner merely to continue.
- Escalate material changes, unknown ownership, conflicts, protected data, or unapproved live impact—not attempt count alone.
- Reassess root cause after repeated failure and prohibit unchanged blind retries.
- Treat deterministic reports and one-use child subjects as governed evidence classes, not new authority.
- Keep one accountable main integrator and shared-checkout writer. Permit at most one additional writer only in an accepted dedicated worktree with non-overlapping owned roots, and preserve all user-owned changes.
- Present Owner decisions in plain language with genuine evaluated options only when a material choice exists.

## Revision History

| Version | Description |
|---------|-------------|
| 4.3 | Added bounded-outcome and material-decision-only engineering principles. |
| 1.1 | Added EO-15.2 risk-tiered conditional authority and governed subagent adoption. |
| 1.0 | Initial governed engineering principles. |
