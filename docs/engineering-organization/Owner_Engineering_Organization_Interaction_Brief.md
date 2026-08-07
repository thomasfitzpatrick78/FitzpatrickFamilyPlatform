# Owner Brief — Goal-Oriented Engineering Organization

**Document Version:** 1.2
**Status:** Prepared repository target; effective only after exact governed publication and remote-equality proof
**Milestone:** Milestone 15
**Capability:** EO-15.2 Risk-Tiered Goal-Oriented Delivery and Governed Subagent Adoption

## Purpose

This brief defines the Owner's role and the normal interaction between the Owner, ChatGPT, Codex, and the repository-governed Engineering Organization.

Before publication effectiveness, this file is target-state proposal evidence only. Publication does not assign `CANDIDATE-EO-15.2`, implement the passive capability, activate a pilot, or authorize goal/task operation, scheduling, dispatch, persistence, model invocation, production, release, or live work.

## The Operating Model

The Owner sets direction and makes the few material human decisions. Codex carries an approved outcome forward through parallel engineering work, repository evidence, just-in-time checks, same-turn replanning, validation, and integration without requiring the Owner to manage the engineering steps or reconstruct prior chats.

One durable delivery goal coordinates several independently authorized workstreams:

1. The goal states the outcome and requirement-level completion evidence.
2. Each workstream retains its own role, work package, paths, approvals, prohibitions, and stop conditions.
3. Goal membership never lends or authenticates authority.
4. Codex exposes and continues every independently eligible lane within authority.
5. Dependencies are checked at their latest safe time.
6. A blocked lane triggers same-turn replanning while unaffected lanes continue.
7. The Owner receives one compact material decision card.
8. Completion is proved requirement by requirement from repository and permitted external evidence.

The repository capability remains passive. It validates, evaluates, and renders evidence. It does not select work, create tasks, invoke models, schedule, dispatch, persist runtime state, change infrastructure, or approve decisions.

## The Owner's Role

The Owner is the human source of product intent, portfolio priority, acceptable risk, and final value judgment. When exercising distinct governed authorities, the Owner records Product Board, Architecture Gatekeeper, publication, production, release, or exception decisions separately.

The Owner is responsible for:

- stating the outcome, constraints, priorities, and definition of value;
- deciding material product, architecture, investment, risk, production, release, and exception questions;
- confirming whether an outcome is acceptable to the family or customer;
- changing direction when evidence shows the current goal is wrong; and
- approving exact decision subjects when repository governance requires human authority.

The Owner is not expected to:

- decompose the outcome into every engineering step;
- decide when routine dependency checks run;
- coordinate Alpha, Bravo, Charlie, or other execution lanes;
- restate repository history or paste long continuity prompts;
- remember hashes, path inventories, test commands, or unfinished technical details;
- discover that one blocked lane leaves another lane eligible; or
- repeatedly ask Codex to continue work that remains inside an approved goal and authority envelope.

## ChatGPT's Role

ChatGPT is the Owner's strategy, product, and architecture workshop surface. It supports:

- vision and outcome shaping;
- product and architecture options and tradeoffs;
- Product Board, retrospective, and inspect-and-adapt workshops;
- non-technical explanation;
- decision-subject and approval drafting; and
- challenges to assumptions, value, scope, and risk.

ChatGPT conversation history is working context. It is not durable Engineering Memory, repository authority, implementation authority, or completion evidence. Accepted material decisions must be represented by exact governed artifacts or acceptance records before repository action relies on them.

## Codex's Role

Codex is the governed engineering-delivery surface. Within an approved goal and separate workstream envelopes, Codex:

- orients from the repository and verifies the current baseline;
- maintains or proposes goal, workstream, dependency, decision, and completion evidence;
- coordinates parallel agents without lending authority;
- performs just-in-time dependency checks;
- replans immediately when evidence changes;
- continues independently eligible work without routine Owner prompts;
- reconciles shared paths and serialized publication boundaries;
- runs permitted tests and validators;
- prepares exact evidence, manifests, audits, and decision cards; and
- stops at the smallest decision requiring human authority.

Codex does not independently make product, architecture, scope-expansion, production, release, or live-work decisions. A goal, chat, passing check, `READY` state, clean tree, or tool access never widens authority.

## Repository-First Continuity

A new ChatGPT or Codex session must be able to recover work without prior conversation history. The durable continuity set is:

- approved goal definition and acceptance requirements;
- separately approved workstream authority envelopes;
- current goal and workstream snapshot;
- dependency observations, validity windows, and next-check times;
- accepted decision references and exact subject digests;
- active changes and shared-path lease state;
- evidence references and requirement-level completion state;
- unresolved decisions and exact next gate; and
- this interaction brief.

Chat or model memory may help locate or summarize repository records, but it is never required to reconstruct authority, current state, or completion.

## Normal Interaction

### Starting or changing an outcome

The Owner states the desired outcome, value, constraints, and any priority change. ChatGPT may help shape the decision. Codex reconciles it with repository authority and returns the smallest missing Product Board, Architecture Gatekeeper, or work-package decision.

### During delivery

Codex continues within authority. Progress updates are short and material: a lane completed, a dependency changed, a blocker appeared, a replan occurred, or a human gate is approaching.

### At a human gate

Codex returns one seven-field decision card:

1. decision;
2. recommendation;
3. evidence;
4. authority gained;
5. authority not gained;
6. expiry or invalidation; and
7. exact response form.

After approval, Codex resumes without requiring a separate “continue” prompt.

### At completion

Codex audits every goal acceptance requirement against authoritative evidence. It does not infer completion from effort, artifact count, elapsed time, a green validator, or conversation claims.

## Reusable Chat-to-Codex Transition Prompt

Use this prompt to start or resume governed engineering delivery without transferring authority to conversation context or requiring the Owner to reconstruct prior history:

> Continue the active governed engineering outcome for this repository.
>
> Treat the repository—not this prompt, prior chat, Codex goal/task state, or model memory—as authority. Follow applicable `AGENTS.md` and repository instructions, perform the governed session initialization, and recover the active goal, current snapshot, continuity, workstream authority envelopes, dependencies, accepted decisions, evidence, active changes, shared-path ownership, prohibitions, and next gates from repository artifacts. Independently revalidate the current repository and relevant external state before acting.
>
> Use the persistent Codex goal as a coordination aid when available, never as authority. Continue every independently eligible workstream within its own exact authority. When two or more eligible workstreams can proceed independently, explicitly delegate them to Codex subagents or parallel agents and collect their results in this main task. Do not transfer authority between workstreams. Keep write-heavy or shared-path work serialized through Architecture Integration. Check dependencies at their latest safe time, replan in the same turn when a lane blocks, and keep unaffected eligible lanes moving.
>
> Own routine decomposition, coordination, validation, evidence, continuity updates, and continuation. Keep the main task focused on requirements, decisions, integrated evidence, and final outputs; keep noisy exploration and isolated checks in bounded subagent work. Keep progress updates concise and material. Persist authoritative state, evidence, unresolved issues, and next gates in governed artifacts so another fresh session can recover without this chat.
>
> Completion requires authoritative evidence for every acceptance requirement, every required workstream complete, and no unresolved material issue. Do not infer completion from effort, elapsed time, a passing validator, a clean tree, or a plausible summary.
>
> Stop only when a material human decision, scope expansion, destructive or high-impact action, or genuine external dependency requires it. At that point return one compact decision card containing: decision, recommendation, evidence, authority gained, authority not gained, expiry or invalidation, and an exact response form. Do not ask me to reconstruct prior chats or provide a routine “continue” instruction.
>
> This prompt grants no implementation, staging, commit, push, protected access, production, release, activation, customer, or live-work authority. If the required repository goal or snapshot is absent, stale, inconsistent, or not yet governed, stop with the smallest recovery decision instead of inventing state or authority.

### Optional Owner addition

Append only when something changed after the latest governed snapshot:

> New Owner direction or decision: `<state only the changed outcome, priority, constraint, or exact accepted decision>`

The Owner does not need to paste a chat transcript, path inventory, test history, hash ledger, or technical work plan when those facts already belong in governed continuity.

### Retired interim pilot form

The following form is historical evidence and must not be used for new work:

> Continue the active governed engineering outcome for `<repository identity>` using the latest atomically sealed pilot decision and acceptance artifacts in `<external coordination location>`. First verify their exact hashes and independently revalidate the governed repository. Treat those external artifacts as temporary evidence only to the extent explicitly accepted; repository authority and each workstream's exact decisions remain controlling. Use the persistent Codex goal as coordination state, not authority. Explicitly delegate independently eligible workstreams to Codex subagents or parallel agents, preserve serialized shared-path writes, use just-in-time dependency checks and same-turn replanning, keep the main task focused on integrated evidence and decisions, and stop at the smallest material human gate with the seven-field decision card. Do not ask me to reconstruct prior chats. This prompt grants no additional authority.

The interim form expired when AuthorityIndex v1, BoundedOutcomeEnvelope v2, and DeliveryState v1 became recoverable through root initialization.

## Generated-Evidence Hygiene

Repository-managed evidence contains no personal name, personal path, absolute checkout path, credential, customer detail, or protected value. Validators emit sanitized repository identity and repository-relative evidence. Detailed local reports remain outside Git when they cannot satisfy that rule.

## Activation Boundary

The passive capability and this operating model can be specified, implemented, tested, and published without operational activation. Any later integration that creates or operates goals/tasks, schedules or dispatches work, persists state, invokes models, accesses protected systems, changes production, or performs live work requires its own exact governed package and human decision.

## Success Test

The operating model is successful when:

- independently eligible work continues when one lane blocks;
- dependency checks occur before the latest safe time;
- Owner attention is concentrated on material decisions;
- a fresh session recovers the goal from repository artifacts;
- decision packages are atomically sealed before approval;
- repository evidence is Git-safe;
- the passive capability is implemented, validated, accepted, and published; and
- any operational activation remains separately governed.

## EO-15.2 Owner Interaction Amendment

The governed capability is `EO-15.2 — Risk-Tiered Goal-Oriented Delivery and Governed Subagent Adoption`.

Codex continues automatically through accepted Tier 0 and Tier 1 work and expressly bundled Tier 2 work. It returns only for an unbundled Tier 2 action, Tier 3 action, or invalidated bundle.

The Owner-facing card uses plain language: decision, why it matters, recommendation first, two or three scored options, what happens next, and one exact short reply. Technical evidence, authority, paths, hashes, expiry, and recovery appear in an audit appendix. This amendment supersedes the seven-field technical card as the Owner-facing layer.

---

## Related Documents

- `Engineering_Organization_Vision.md`
- `Parallel_Workstream_Delivery_Model.md`
- `Engineering_Workspace_Model.md`
- `Engineering_Memory_Concept.md`
- `AI_Role_Catalog.md`
- `Human_Role_Catalog.md`
- `Goal_Oriented_Parallel_Delivery_Specification.md`
- `AI_Session_Initialization_Standard.md`
- `AI_Session_Completion_Standard.md`

## Revision History

| Version | Description |
|---|---|
| 1.2 | Added EO-15.2 risk-tiered conditional authority and governed subagent adoption. |
| 1.1 | Added the reusable repository-first chat-to-Codex transition prompt, optional changed-direction form, and expiring interim pilot bridge without changing authority or lifecycle semantics. |
| 1.0 | Defined the Owner, ChatGPT, Codex, repository-first continuity, compact decision, generated-evidence hygiene, and activation contracts from the Milestone 15 pilot. |
