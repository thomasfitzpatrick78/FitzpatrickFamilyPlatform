# Governance State Interface Standard

**Version:** 1.0
**Status:** Active

## Purpose

Repository state, not task memory, must tell a new main task or specialist which governance is effective, what outcome is authorized, what work is complete, and what happens next.

Three machine-readable interfaces provide that continuity:

- **BoundedOutcomeEnvelope v2** defines the approved result, scope, actions, material stops, validation, evidence, publication, expiry, and ownership.
- **AuthorityIndex v1** identifies the sole effective governance model, active workstreams, historical or superseded artifacts, and repository overlays.
- **DeliveryState v1** records current authority, baseline, completed work, active changes, repair assessments, subagent lanes, evidence, blockers, and next action.

The validators confirm structure and fail-closed invariants. They do not authenticate a decision, grant authority, or replace live repository checks.

## Recovery Order

A fresh task reads:

1. root `AGENTS.md`;
2. the Authority Index;
3. the referenced active Bounded Outcome Envelope;
4. the referenced Delivery State;
5. repository-specific safety overlays; and
6. current Git and tool evidence.

Chat reconstruction, a mandatory new conversation, an initialization report, a completion report, a continuity brief, or a goal snapshot is not required when the three interfaces contain the same current facts. Historical artifacts remain evidence and are not rewritten.

## Evidence Side Effects

Validation output defaults to terminal, temporary storage, or CI artifacts. A durable tracked report is committed only for a milestone, release, or an explicitly governed evidence snapshot. Exact changed paths and hashes are recorded after implementation; ordinary governance does not bind advance Markdown bytes.

## Compatibility

Schema-major 2 Bounded Outcome policies are compatible when repository overlays and invariants pass. A repository may accept a later compatible 2.x policy without a new Owner decision. A major-version change or material local invariant change requires a new decision.
