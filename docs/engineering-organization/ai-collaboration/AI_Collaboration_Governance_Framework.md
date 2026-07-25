# AI Collaboration Governance Framework

**Document Version:** 1.8

**Status:** EO-14.8 Baseline and EO-15.1 Repository Update Published

**Milestone:** EO-14.8

---

## Purpose

This framework defines how the approved AI Collaboration Governance specifications are organized for reusable repository use and repository-side operational visibility.

It implements repository structure, navigation, lifecycle linkage, role linkage, blank templates, the EO-14.8D repository-readiness validation entry point, and EO-14.8E read-only Engineering Metrics and Platform Health evidence integration. It does not remediate findings, inspect conversations, or authorize live work.

---

## Framework Principles

- Use repository evidence before conversation context.
- Use approved specifications before templates.
- Use templates only for future approved workstreams.
- Keep current-state and planned-state claims distinct.
- Preserve existing Engineering Lifecycle authority.
- Escalate conflicts to the appropriate governance role.

---

## Artifact Relationships

```text
Capability Charter
        |
        v
AI Collaboration Governance Specification
        |
        +--> AI Collaboration Lifecycle
        +--> AI Session Initialization Standard
        +--> AI Session Completion Standard
        +--> Workstream Continuity Brief Specification
        +--> AI Collaboration Steward Specification
        +--> AI Session Readiness Validator Specification
        |
        v
Reusable Templates
```

---

## Repository Use

Future approved workstreams may use this framework by:

1. Reviewing the Capability Charter and governing specification.
2. Confirming the assigned AI role and authority boundaries.
3. Classifying the starting repository baseline and completing session initialization using the initialization standard.
4. Creating or updating continuity evidence only when the workstream is authorized to do so.
5. Completing the session using the completion standard.
6. Returning unresolved conflicts to the appropriate governance role.

---

## Template Inventory

| Template | Governing Standard |
|----------|--------------------|
| [AI Session Initialization Record Template](templates/AI_Session_Initialization_Record_Template.md) | AI Session Initialization Standard. |
| [AI Session Completion Report Template](templates/AI_Session_Completion_Report_Template.md) | AI Session Completion Standard. |
| [Workstream Continuity Brief Template](templates/Workstream_Continuity_Brief_Template.md) | Workstream Continuity Brief Specification. |
| [AI Collaboration Steward Review Template](templates/AI_Collaboration_Steward_Review_Template.md) | AI Collaboration Steward Specification. |

---

## Steward Framework

The AI Collaboration Steward framework consists of:

- the planned role definition in the AI Role Catalog;
- the AI Collaboration Steward Specification;
- the AI Collaboration Steward Review Template;
- escalation paths through existing governance.

This framework does not activate the Steward role, assign a Steward, or authorize Steward decisions.

---

## Validator Boundary

The AI Session Readiness Validator is implemented as a reusable validation engine with `./platform-eap ai-session readiness` as its Platform EAP entry point.

EO-15.1 adds `./platform-eap ai-session baseline --work-package <repository-path>` as the read-only initialization classifier. It distinguishes `Clean`, `Expected Generated Evidence`, and `Dirty`, requires current-HEAD attribution and byte-for-byte reproduction for the two governed readiness outputs, rejects every additional or ambiguous change, and permits generated evidence only when canonical tracked work-package context contains exactly one permission declaration with the exact value `Permitted`.

The validator reads repository and Git evidence, returns domain-structured results, and generates repository-managed Markdown and JSON reports under `reports/engineering/ai_session_readiness/`. It does not inspect conversation content, initialize sessions, alter continuity briefs, or remediate findings.

Engineering Metrics consumes the governed JSON report without calling validator internals or changing readiness evidence. The structured metrics report also exposes the same four-state evidence through a repository-side Platform Health source object. Missing or malformed evidence remains `UNKNOWN`.

EO-14.8E and the integrated EO-14.8 parent capability remain the published Engineering Organization baseline. Milestone 14 operational continuity is closed. Milestone 15 Architecture Integration remains active, and EO-15.1 repository implementation is Architecture Gatekeeper approved and published. The standing generated-evidence policy is authoritative after successful publication and post-publication verification; it does not alter the published EO-14.8 baseline or authorize implementation by itself. Steward automation, role activation, Platform implementation, FFFA implementation, and live work remain unauthorized by continuity, baseline classification, or readiness.

---

## Related Documents

- [AI Collaboration Governance Capability Charter](AI_Collaboration_Governance_Capability_Charter.md)
- [AI Collaboration Governance Specification](AI_Collaboration_Governance_Specification.md)
- [AI Collaboration Lifecycle](AI_Collaboration_Lifecycle.md)
- [AI Role Catalog](../AI_Role_Catalog.md)
- [Engineering Lifecycle](../../governance/Engineering_Lifecycle.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.8 | Recorded Architecture Gatekeeper approval and governed publication of EO-15.1 while preserving all activation and live-work boundaries. |
| 1.7 | Required exactly one generated-evidence permission declaration and fail-closed handling of duplicate or conflicting work-package metadata. |
| 1.6 | Enforced work-package-specific generated-evidence permission through the production baseline command and recorded placeholder-safe Transition Review validation. |
| 1.5 | Integrated EO-15.1 fail-closed baseline classification and Transition Review validation as unpublished repository implementation pending Architecture Gatekeeper review. |
| 1.4 | Advanced operational continuity to Milestone 15 while preserving the published EO-14.8 framework and no-activation boundary. |
| 1.3 | Closed and published the Architecture Gatekeeper-approved EO-14.8 capability baseline and recorded next Alpha initialization support. |
| 1.2 | Integrated EO-14.8E read-only Engineering Metrics and repository-side Platform Health visibility. |
| 1.1 | Integrated the EO-14.8D reusable readiness engine, Platform EAP entry point, structured reports, and validation boundary. |
| 1.0 | Initial reusable AI Collaboration Governance repository framework. |
