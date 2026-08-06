# Risk-Tiered Goal-Oriented Delivery and Governed Subagent Adoption Specification

**Document Version:** 1.0
**Status:** Prepared Target; Not Effective Until Governed Publication
**Initiative:** EO-15.2
**Phase:** A

## Purpose

This specification defines a delivery operating model that increases throughput and reduces Owner orchestration while preserving material human authority, repository integrity, privacy, and architectural quality.

The model separates evidence checkpoints from Owner decisions. Evidence remains required at every applicable phase. A new Owner decision is required only when outcome, scope, risk, authority, or intended effect changes materially.

## Outcomes

Phase A must produce:

1. materially higher engineering throughput;
2. zero continuation-only Owner prompts;
3. plain-language, material-decision-only Owner interaction;
4. two or three genuine options scored for commercial architecture, maintainability, and code quality;
5. repository-first fresh-task recovery;
6. one accountable integrator and writer per checkout;
7. bounded, read-only specialist parallelism; and
8. complete evidence without treating evidence as authority.

## Authority

Repository authority remains ordered as follows:

1. permanent governance;
2. approved milestone and architecture artifacts;
3. approved work package and accepted conditional bundle;
4. Active continuity evidence; and
5. task context, goal state, subagent state, or model memory.

An assignment, tool, test, validator, clean tree, `READY` result, goal membership, bundle membership, or subagent result never creates, authenticates, transfers, or widens authority.

## Risk Tiers

### Tier 0 — Observe

Tier 0 includes repository reads, searches, static inspection, planning, option analysis, and documentation review.

- It may proceed automatically after the outcome is accepted.
- Read-only specialists may work concurrently.
- It produces a summary, not an Owner decision.
- Network access, Git metadata mutation, protected data, and report-writing validation are not Tier 0 by implication.

### Tier 1 — Reversible Local Delivery

Tier 1 includes only exact manifest-listed repository targets, isolated tests, static validation, bounded repair, and sanitized evidence. Staging or a local commit is Tier 1 only when the accepted bundle names the exact repository, branch, action, and predicates.

- The main task is the sole same-checkout writer.
- Specialists remain read-only.
- The same failure permits at most two repair cycles.
- A conforming narrow repair may change only paths marked repairable in the accepted manifest.
- A derived final manifest records repaired bytes and validation without a new Owner decision.

### Tier 2 — Recoverable External Non-Production Work

Tier 2 includes a named non-protected branch push, draft pull request, approved public dependency retrieval, or separately owned writer worktree.

- It proceeds automatically only when the accepted bundle names the action, subject, branch or worktree, recovery method, evidence, and expiry.
- Otherwise it returns one plain-language Owner decision.
- A writer worktree requires its own branch, owner, path lease, authority envelope, and integration order.

### Tier 3 — Material Work

Tier 3 includes:

- customer or protected data;
- credentials, privacy boundaries, or security trust boundaries;
- destructive or difficult-to-recover action;
- protected/default-branch publication, merge, tag, or release;
- production, deployment, activation, backup, restore, or live work;
- new architecture, public/shared contract change, or architecture exception;
- product outcome, priority, customer promise, material scope, budget, or residual-risk change; and
- PLAT-15.1A artifact acquisition, VM/Linux action, Gate 2 or later execution unless an exact later decision expressly authorizes it.

Tier 3 always requires fresh explicit human approval before action.

## Conditional Phase Bundle

Every bundle must define:

1. plain-language outcome and value;
2. exact repositories, baselines, branches, target paths, and exclusions;
3. acceptance criteria and validation;
4. allowed actions by tier;
5. whether staging, local commit, push, draft pull request, or publication is included;
6. main-writer identity, specialist lanes, worktree and branch ownership, and shared-path leases;
7. two-cycle repair policy and exact repairable paths;
8. evidence required after each phase and at completion;
9. generated-evidence classification and disposition;
10. automatic invalidation triggers; and
11. expiry and completion conditions.

The bundle must use the governed template and must reject unknown fields in any machine-validated representation.

The Phase A repository validator is deliberately limited to Tier 0 through Tier 2 structural and semantic validation. It rejects every Tier 3 bundle even when the bundle claims approval evidence. Tier 3 requires a separately sealed human decision subject plus governed initialization that independently loads, hashes, authenticates, scope-checks, and freshness-checks the exact approval records. Repository validator success never makes a Tier 3 action executable.

## Automatic Continuation

After an accepted bundle becomes valid, the main task continues automatically through every included phase whose entry predicates pass. It does not ask the Owner to continue after initialization, exploration, application, a passing test, each specialist result, a conforming repair, hash rebinding, evidence generation, or transition between separately authorized repository steps.

The main task records distinct evidence for each phase. Combining authority does not combine or omit evidence.

## Invalidation

A bundle becomes invalid immediately on:

- dirty, behind, diverged, conflicted, stale, remotely unverified, or materially different baseline;
- ambiguous pre-existing changes;
- out-of-scope or new path;
- shared-path collision or second same-checkout writer;
- more than three concurrent specialists or any specialist write;
- protected or customer data;
- architecture, public-contract, trust-boundary, destructive, production, live, or unapproved publication need;
- unclassified validator side effect or generated evidence outside its declared disposition;
- missing or changed acceptance criteria;
- expiry;
- a third attempt for the same failure; or
- inability to recover authority, current phase, evidence, and next material gate without task history.

The main task stops the invalid action. It continues only independently eligible action expressly allowed by the bundle.

## Main Task and Specialists

One main Codex task coordinates the approved outcome and integrates all evidence.

- The main task performs complete governed initialization once.
- It is the sole writer in the shared checkout.
- It delegates only genuinely independent, bounded, read-heavy lanes.
- Normal concurrency is at most three specialists.
- It waits for and reconciles every delegated result.
- It owns routine decomposition, sequencing, validation, evidence, and continuation.

The governed specialists are:

- **`governed_explorer`:** repository, authority, lifecycle, dependency, and path discovery.
- **`governed_validator`:** validation-side-effect analysis and permitted read-only or isolated checks.
- **`governed_reviewer`:** correctness, security, privacy, regression, maintainability, test, and governance review.

Governed specialists may be spawned only when the parent turn's live permission mode is read-only. A custom agent's declared sandbox is supplementary because current Codex clients reapply the parent turn's live permission choice to spawned agents. Workspace-write main-writer phases therefore run without subagents and are bracketed by exact pre/post path proof. This is a technical phase transition inside accepted authority, not an Owner continuation gate.

Specialists cannot write, approve, broaden scope, publish, access protected systems, or transfer authority. A specialist performs a bounded lane attestation rather than repeating the entire main-task initialization.

## Owner Decision Card Version 2

An Owner card is created only for an unbundled Tier 2 action, Tier 3 action, or bundle invalidation.

### Owner layer

1. one-sentence decision;
2. plain-language impact;
3. recommendation first;
4. two or three genuine options with High, Medium, or Low scores for commercial architecture, maintainability, and code quality;
5. concise strengths, weaknesses, reversibility, delay, and what happens next; and
6. one exact short reply.

Unsafe options are not manufactured. `Stop` or `Defer` is a genuine option when appropriate.

### Audit appendix

The technical layer records authority gained and not gained, evidence, paths, hashes, expiry, invalidation, recovery, and remaining gates.

## Generated Evidence

Every command is classified before execution as:

1. no repository write;
2. isolated temporary output only;
3. exact deterministic tracked regeneration included in the manifest; or
4. prohibited.

A passing validator never authorizes generated paths. Tracked generated output may not be improvised, restored, discarded, or staged outside the accepted disposition.

Repository-managed evidence excludes personal names, absolute checkout paths, credentials, customer details, protected values, prompt text, and detailed local reports.

## Platform and FFFA Separation

The Platform owns the canonical shared operating policy. FFFA adopts an exact published policy version through its own profile, digest binding, repository decision, implementation package, validation, and publication.

Platform acceptance or publication never activates FFFA. FFFA may narrow shared policy for Finance privacy and safety but may not use the profile to broaden Platform authority.

## Phase B Boundary

Phase B retains the future passive Goal-Oriented capability: machine-checkable goal/snapshot models, dependency timing, eligibility, completion audits, and fresh-task recovery. Phase A does not implement or activate that capability.

Any Phase B work requires a later exact package, current baseline, revised path inventory, Phase A conformance, and separate Product Board and Architecture Gatekeeper decisions.

## PLAT-15.1A Delivery-Recovery Acceptance

The previous pilot is not delivery success evidence because the Owner reports 108 decisions without PLAT-15.1A completion.

The first applied pilot must be a separately scoped PLAT-15.1A recovery phase inside the same accepted umbrella activation subject that conditionally implements and publishes Phase A. Platform and PLAT authority remain distinct, but no second Owner continuation decision occurs between passing publication predicates and pilot entry.

The pilot must:

- produce zero continuation-only prompts;
- make every Owner prompt material and plain-language;
- require no more than five material decisions before the next completed delivery segment or proven external blocker;
- complete every independently executable action before returning a blocker;
- reduce material Owner decisions per comparable completed delivery segment by at least 80 percent against the Owner-reported 108-decision history; record the comparison method, total decisions, continuation prompts, repairs, elapsed time, and external blockers; and
- keep EO-15.2 open until PLAT-15.1A completes or a separately accepted genuine external blocker makes completion impossible within approved scope.

Phase A publication alone does not authorize PLAT-15.1A execution. The umbrella activation subject must separately bind the exact PLAT phase, its evidence, protected boundaries, and expiry before the Owner approves that subject.

## Conformance

Phase A conformance requires:

- exact policy, bundle template, Owner card template, repository instructions, project configuration, and three specialist profiles;
- separate Platform and FFFA manifests and authority;
- focused static tests;
- fresh-task instruction and specialist discovery from each repository root;
- zero unlisted paths or same-checkout writer conflicts;
- no protected-data access or unapproved generated evidence;
- proof that no continuation-only Owner prompt is required inside a valid bundle; and
- Architecture Gatekeeper review of final bytes and evidence before publication.
