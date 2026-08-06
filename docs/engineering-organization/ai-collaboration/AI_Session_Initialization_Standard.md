# AI Session Initialization Standard

**Document Version:** 1.5

**Status:** Architecture Gatekeeper Approved; Published

**Milestone:** EO-14.8B

---

## Purpose

This standard defines mandatory AI session initialization checks before planning, architecture, implementation, validation, live work, release, or closeout begins.

---

## Mandatory Checks

| Check | Required Evidence |
|-------|-------------------|
| Repository identity | Repository path and expected repository name. |
| Branch and HEAD | Current branch and current commit. |
| Working-tree state | `git status -sb` and active changed files. |
| Baseline classification | `./platform-eap ai-session baseline` result of `Clean`, `Expected Generated Evidence`, or `Dirty`. |
| Remote synchronization status | Remote tracking state where available. |
| Permanent governance | Applicable permanent governance artifacts reviewed. |
| Current milestone | Active milestone plan and milestone status reviewed. |
| Roadmap, backlog, and Kanban | Product roadmap, product backlog, Engineering Organization roadmap/backlog, and portfolio Kanban reconciled as applicable. |
| Applicable ADRs, specifications, work packages, and continuity briefs | Relevant repository-governed authority artifacts identified. |
| Assigned AI role | Role from AI Role Catalog or approved work package confirmed. |
| Authority and prohibited actions | Allowed actions, prohibited actions, required approvals, and stop conditions confirmed. |
| Parallel workstreams and dependencies | Active parallel workstreams, integration gates, and dependency order reconciled. |
| Current lifecycle stage | Engineering Lifecycle stage and AI Collaboration Lifecycle stage declared. |
| Contradictions | Narrative context compared with repository evidence and any conflict escalated. |
| Readiness result | READY, READY WITH WARNINGS, or NOT READY. |

## Repository Baseline Classification

After remote synchronization is established where required and before implementation begins, run:

```text
./platform-eap ai-session baseline --work-package docs/milestones/Milestone_<n>/<Approved>_Work_Package.md
```

The classifier applies the repository-governed baseline contract:

| Baseline State | Required Evidence | Session Action |
|----------------|-------------------|----------------|
| `Clean` | No repository changes are present; repository identity, branch, tracking branch, conflict state, and ahead/behind checks pass. | Continue when all other authority and readiness gates pass. |
| `Expected Generated Evidence` | The only changes are the two unstaged AI Session Readiness outputs, the exact governed producer is `./platform-eap ai-session readiness`, both outputs identify current HEAD and zero errors, current authority is consistent, both files reproduce byte-for-byte, and the tracked authoritative work package contains exactly one `**Expected Generated Evidence Baseline:** Permitted` declaration. | Continue when all other gates pass. |
| `Dirty` | Any additional or untracked path, staged or ambiguous state, merge conflict, authority drift, provenance failure, reproduction mismatch, synchronization failure, missing or invalid work-package context, absent, duplicate, conflicting, or invalid permission metadata, or `Prohibited` work-package value exists. | Stop for reconciliation or explicit disposition. |

Path-only allowlisting is insufficient. The classifier must fail closed and must not modify the repository, redefine Git status, infer remote freshness without a fetch, or authorize implementation, architecture, product, release, deployment, activation, production, or live work.

Machine-readable evidence is available through:

```text
./platform-eap ai-session baseline --work-package docs/milestones/Milestone_<n>/<Approved>_Work_Package.md --json
```

The baseline command is an initialization gate. `Clean` does not require a work-package exception, but supplying the active work-package path preserves complete session evidence. `Expected Generated Evidence` fails closed to `Dirty` unless the canonical, tracked work package has exactly one permission declaration and its value is exactly `Permitted`. Duplicate or conflicting declarations are ambiguous and therefore `Dirty`. Conversation approval and command-line booleans are not permission sources. Later readiness validation during the same authorized implementation session may report disclosed active source changes as warnings; those changes do not retroactively alter the recorded starting baseline or authorize a future session to inherit them.

---

## Reconciliation Statement

Before planning, architecture, implementation, or live work begins, the AI participant must provide a reconciliation statement that identifies:

- the repository and branch;
- the current HEAD;
- the workstream or work package;
- the assigned role;
- the current lifecycle stage;
- active repository changes that must be preserved;
- known dependencies and integration gates;
- prohibited actions;
- readiness outcome.
- baseline classification and, for `Expected Generated Evidence`, the changed paths and SHA-256 hashes.

---

## Readiness Outcomes

| Outcome | Meaning |
|---------|---------|
| READY | Required checks pass and no blocking conflicts exist. |
| READY WITH WARNINGS | Required checks are sufficient to proceed, but warnings or nonblocking gaps must be disclosed. |
| NOT READY | Work must stop until repository state, authority, scope, or governance conflicts are resolved. |

Readiness outcomes must not use a percentage score.

---

## Non-Goals

- Conversation-content scoring.
- AI model evaluation.
- Prompt-quality scoring.
- Validator implementation.
- Platform EAP command implementation.
- Continuity template implementation.

---

## EO-15.2 Conditional-Bundle Initialization

When EO-15.2 applies, initialization also records the bundle identity and digest, risk tier, repositories and branches, baseline and remote-freshness requirement, allowed and excluded paths, publication inclusions, main writer, specialist lanes, generated-evidence disposition, repair budget, expiry, invalidation predicates, and exact next material gate.

The main task performs this reconciliation. A specialist performs only its bounded lane attestation.

---

## Related Documents

- [AI Collaboration Governance Capability Charter](AI_Collaboration_Governance_Capability_Charter.md)
- [AI Collaboration Lifecycle](AI_Collaboration_Lifecycle.md)
- [AI Session Completion Standard](AI_Session_Completion_Standard.md)
- [AI Session Readiness Validator Specification](AI_Session_Readiness_Validator_Specification.md)
- [Engineering Lifecycle](../../governance/Engineering_Lifecycle.md)
- [AI Role Catalog](../AI_Role_Catalog.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.5 | Added EO-15.2 risk-tiered conditional authority and governed subagent adoption. |
| 1.4 | Recorded Architecture Gatekeeper approval and publication of the fail-closed baseline classification standard. |
| 1.3 | Required exactly one governed permission declaration and classified duplicate or conflicting work-package metadata `Dirty`. |
| 1.2 | Required canonical tracked work-package context and exact governed opt-in metadata before the production classifier may return `Expected Generated Evidence`. |
| 1.1 | Added the fail-closed `Clean`, `Expected Generated Evidence`, and `Dirty` repository baseline classification required before governed work begins. |
| 1.0 | Initial AI Session Initialization Standard. |
