# Codex Repository Instructions — FitzpatrickFamilyPlatform

## Authority and initialization

- Treat repository authority in this order: permanent governance and this file; the Authority Index; an accepted Bounded Outcome Envelope or historical Phase A authority; Delivery State; repository overlays; task context.
- For current EO-15.2 recovery, read `docs/engineering-organization/ai-collaboration/operational/milestone-15/EO_15_2_Authority_Index.json` and follow its referenced envelope and Delivery State.
- Start read-only. Verify repository identity, branch, clean status, local/tracking/live equality when required, active authority, owned and excluded roots, validation, evidence disposition, ownership, expiry, prohibitions, and next material action before writing.
- Stop on drift, ambiguous pre-existing changes, missing authority, out-of-scope paths, shared-path conflict, protected information, or an invalid bundle. Preserve user changes.
- `READY`, a passing check, clean status, tool access, goal membership, or subagent assignment is evidence only and never grants authority.

## Bounded-outcome delivery

- Phase A conditional bundles remain authoritative for historical packages. New work must use an accepted Bounded Outcome Envelope v2.
- An outcome envelope binds the plain-language result, acceptance criteria, owned and excluded roots, allowed action classes, invariants, validation, evidence classes, included publication checkpoints, and completion condition.
- Continue automatically through implementation, diagnosis, conforming repair, validation, evidence, and included publication while the envelope remains valid. Never ask merely to continue or to acknowledge a routine technical result.
- Stop for the Owner only when architecture, security, the customer-data boundary, cost, production scope, required tools, a public contract, protected/live scope, or the approved outcome materially changes. Protected or live action still requires exact affirmative inclusion.
- After two unsuccessful repairs for the same failure, prohibit an unchanged retry and perform an internal root-cause reassessment. A newly justified correction may continue inside the envelope; attempt count alone is not an Owner gate.
- A discovered path may be repaired only when it is inside an owned root, outside every excluded root, required by evidence, nonconflicting, and recorded in the scope-delta audit. Unknown or user-owned changes always stop.
- Governed validators may create deterministic outputs only in approved report roots. Record exact generated paths and hashes after execution; never stage unrelated reports.
- Expiry triggers automatic state, input, tool, cost, security, and material-condition revalidation. Renew the child lease when unchanged; keep hard windows for credentials, protected access, reservations, and other time-sensitive risk.
- Staging, commit, push, fetch, and remote-equality proof remain distinct evidence phases but are not separate Owner decisions when included in the accepted outcome.

## Main task and subagents

- One main task coordinates the outcome, integrates evidence, and is the sole writer in the shared checkout.
- Delegate genuinely independent, bounded work to at most three concurrent specialists. Specialists default to read-only and cannot approve or widen authority.
- An accepted envelope may define at most one writer subagent. It must use a dedicated worktree and branch, non-overlapping owned roots, explicit exclusions, and the main task as integration owner. It cannot publish independently.
- The main task must collect and reconcile every result. Shared-checkout writing, path overlap, protected data, or authority conflict fails closed.

## Evidence

- Classify every command before execution as no-write, isolated temporary output, exact tracked regeneration included in scope, or prohibited.
- Treat report-writing validators as mutations. Default validation reports to terminal, temporary, or CI evidence. Commit a durable snapshot only for a milestone, release, or explicitly governed evidence output.
- Record repository-relative sanitized evidence only: no personal names, absolute checkout paths, credentials, protected values, prompt text, or detailed local reports.
- Keep Platform and FFFA authority, manifests, validation, and publication separate.

## Owner decisions

- Return an Owner card only for a material stop named by the accepted envelope. Routine design inside approved architecture, diagnosis, conforming repair, validation, evidence, staging, commit, push, fetch, and equality do not require another decision when included.
- Lead with the recommendation. Present two or three genuine choices using plain language and score commercial architecture, maintainability, and code quality High, Medium, or Low.
- When the Owner acts as Product Board and Architecture Gatekeeper, combine both perspectives in this one card.
- Put technical evidence, paths, hashes, expiry, and authority detail in an audit appendix.

## Phase boundary

- Phase A remains historical authority only for already-bound conditional bundles.
- Bounded Outcome Envelope v2 is the sole effective model for new work. The current Authority Index and Delivery State are the canonical recovery surfaces.
- Phase B does not reinterpret historical decisions or grant authority by itself.
- A passing validator, assignment, tool, role, goal membership, or child subject remains evidence only and never creates or transfers authority.
