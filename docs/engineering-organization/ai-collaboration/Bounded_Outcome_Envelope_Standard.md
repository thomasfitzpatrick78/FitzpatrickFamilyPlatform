# Bounded Outcome Envelope Standard

**Version:** 2.0
**Status:** Active — Sole Model for New Work

## Purpose

A bounded outcome envelope makes the approved result—not each technical phase—the unit of authority. It lets engineering continue through implementation, diagnosis, conforming repair, validation, evidence, and included publication without continuation-only Owner decisions.

The envelope never authenticates itself. Repository authority, the cited Owner decision, current repository state, and any protected checkpoint must be independently verified before action.

## Required Contract

Each accepted envelope records:

1. a plain-language result, organizational or customer value, and objective acceptance criteria;
2. exact decision references and authority gained and not gained;
3. repository baselines, branches, owned roots, excluded roots, and remote-equality requirements;
4. allowed action classes and any separately bound Tier 3 checkpoint;
5. one accountable integrator, at most three concurrent specialists, and at most one dedicated non-overlapping writer worktree;
6. validation commands, acceptance evidence, and fresh-task recovery;
7. repair controls, including reassessment after two failures and prohibition of blind retries;
8. governed evidence output classes, report roots, and sanitization;
9. the governed material stop conditions; and
10. automatic expiry revalidation and one plain-language completion return.

The machine-readable schema is implemented by `engineering/platform_eap/outcome_envelope.py`; the reusable authoring example is `templates/Bounded_Outcome_Envelope_Template.json`.

## Material Owner Stops

Return to the Owner only when architecture, a public contract, security, privacy, the customer-data boundary, cost, production, release, destructive action, required tools, or the approved outcome materially changes. A protected action must also be expressly included in the envelope and bound to its exact decision subject.

Routine implementation choices, passing checkpoints, collected specialist results, conforming repairs, deterministic report regeneration, staging, commit, push, fetch, and equality proof do not create separate decisions when they are included in the accepted outcome.

## Repair and Scope Reconciliation

Two unsuccessful attempts for the same failure trigger an internal root-cause reassessment, not automatic Owner escalation. The same action may not be repeated unchanged. A new correction may proceed when it is justified by evidence and remains inside the envelope.

A newly discovered path is conforming only when it is inside an owned root, outside every excluded root, necessary for the approved outcome, free of ambiguous user changes or conflicts, and recorded in the scope-delta audit. Otherwise the work stops.

## Generated Evidence and Child Subjects

Governed generators declare output classes and approved report roots. Exact paths and hashes are recorded after generation. One-use child subjects remain replay-protected technical controls; a conforming sealed failure may receive a new bounded child lease without a new Owner decision. Child leases cannot repeat blindly, widen scope, or change a material condition.

## Expiry and Publication

Expiry requires automatic revalidation of repository state, inputs, tools, cost, security, and material conditions. An unchanged envelope may receive a renewed child lease. Credentials, protected access, external reservations, and other time-sensitive risk retain hard windows.

Staging, commit, protected publication, fetch, and remote-equality proof remain separately recorded evidence phases. When the accepted envelope includes them, they execute without separate continuation approvals. Merge, release, deployment, production, customer data, destructive action, and live work remain excluded unless expressly and materially approved.

## Compatibility

Phase A conditional-bundle validation is preserved only for historical packages already bound to it. New work uses this standard and does not rewrite or silently reinterpret earlier evidence. Compatible schema-major-2 updates may be adopted by downstream repositories when their overlays and invariants pass. A final architecture-conformance report is completion evidence unless it identifies a material deviation.

## Revision History

| Version | Description |
|---|---|
| 2.0 | Made the model sole and active for new work, added one governed writer lane, expanded material stops, and established compatible-major downstream adoption. |
| 1.0 | Established bounded-outcome authority, material stops, internal repair reassessment, governed output classes, child leases, expiry revalidation, and included publication evidence. |
