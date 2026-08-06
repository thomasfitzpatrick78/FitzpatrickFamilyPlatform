# Codex Repository Instructions — FitzpatrickFamilyPlatform

## Authority and initialization

- Treat repository authority in this order: permanent governance; approved milestone and architecture artifacts; approved work package and conditional bundle; Active continuity; task context.
- Start read-only. Verify repository identity, branch, clean status, local/tracking/live equality when required, exact authority, bundle, allowed paths, validation, generated-evidence disposition, roles, repair budget, expiry, prohibitions, and next material gate before writing.
- Stop on drift, ambiguous pre-existing changes, missing authority, out-of-scope paths, shared-path conflict, protected information, or an invalid bundle. Preserve user changes.
- `READY`, a passing check, clean status, tool access, goal membership, or subagent assignment is evidence only and never grants authority.

## Risk-tiered conditional delivery

- Tier 0 is read-only observation and analysis.
- Tier 1 is exact manifest-listed reversible local work, isolated tests, bounded repair, and evidence. Staging or local commit is included only when the accepted bundle says so.
- Tier 2 is named recoverable external non-production work such as a non-protected branch push, draft pull request, approved retrieval, or separately owned worktree. It is included only when explicitly bundled.
- Tier 3 includes customer/protected data, destructive action, protected/default branch, merge, release, deployment, production/live work, architecture or public-contract change, material scope/risk, and PLAT-15.1A protected or Gate 2+ execution. Obtain fresh explicit approval before action.
- Continue automatically through included phases while all predicates pass. Never ask merely to continue, acknowledge a passing phase, collect an agent result, rerun an affected check after a conforming repair, or rebind a permitted derived hash.
- Permit no more than two repair cycles for the same failure and only on manifest-listed repairable paths.

## Main task and subagents

- One main task coordinates the outcome and is the sole same-checkout writer.
- Delegate only genuinely independent, bounded read-heavy work to at most three concurrent specialists: `governed_explorer`, `governed_validator`, and `governed_reviewer`.
- Spawn governed specialists only from a parent turn whose live permission mode is read-only. A custom agent's `sandbox_mode` is supplementary because the parent turn's live permission choice can override it.
- During a workspace-write main-writer phase, do not spawn specialists. Resume specialist inspection only in a separate read-only turn after exact pre/post path proof; this permission transition is part of an accepted bundle and is not an Owner continuation decision.
- Subagents remain read-only, cannot approve or widen authority, and return results to the main task. The main task must wait for and reconcile every result.
- Any independent writer requires later authority, a dedicated worktree and branch, exact ownership, and integration order.

## Evidence

- Classify every command before execution as no-write, isolated temporary output, exact tracked regeneration included in scope, or prohibited.
- Treat report-writing validators as mutations. Never improvise restoration, deletion, staging, or reconciliation of generated reports.
- Record repository-relative sanitized evidence only: no personal names, absolute checkout paths, credentials, protected values, prompt text, or detailed local reports.
- Keep Platform and FFFA authority, manifests, validation, and publication separate.

## Owner decisions

- Return an Owner card only for an unbundled Tier 2 action, Tier 3 action, or bundle invalidation.
- Lead with the recommendation. Present two or three genuine choices using plain language and score commercial architecture, maintainability, and code quality High, Medium, or Low.
- Put technical evidence, paths, hashes, expiry, and authority detail in an audit appendix.

## Phase boundary

- Phase A governs conditional authority and read-only specialists.
- Do not implement or activate the deferred passive Goal-Oriented capability under Phase A.
- Do not represent the prior read-only pilot as delivery success. The first applied pilot after publication must use separate authority to drive meaningful PLAT-15.1A delivery recovery.
