# Goal-Oriented Parallel Delivery Operating-Model Adoption — Exact Governed Work Package

**Document Version:** 1.1
**Status:** Prepared Outside Repository; Proposed for Product Board and Architecture Gatekeeper Acceptance; Not Published
**Implementation State:** Not Authorized; Not Started
**Candidate Initiative Identifier:** `CANDIDATE-EO-15.2` — unassigned and not approved
**Milestone:** Milestone 15
**Governed Repository:** `FitzpatrickFamilyPlatform`
**Target Repository Path:** `docs/milestones/Milestone_15/Goal_Oriented_Parallel_Delivery_Passive_Capability_Work_Package.md`
**Accepted Adoption Subject SHA-256:** `c349b2e699ba14482c0f670eeadf560683f1f0804f10eea03c0c0feb43bc0b40`
**Corrected Passive-Capability Version 1.1 Base SHA-256:** `2262a2fa5902e2e8058286c463ac0410266f63267d6139c9d3f047655bd6707b`
**Accepted Transition-Prompt Version 1.1 SHA-256:** `02ee21a513be8961cb17c7c1fdb9d5621eeeca4710a5e688749cce2c0d60794d`
**Accepted Prompt-Amendment Subject Version 1.1 File SHA-256:** `62166ff4e459894ba38729c119ccd7cba270ff18106d1f2beb79c67b8d3370b3`
**Accepted Prompt-Amendment Subject Version 1.1 Internal SHA-256:** `e9b99763f42ea3b15c1743f3dfb854ac1fe36b423669b2218f87566214d97c53`
**Expected Generated Evidence Baseline:** Prohibited unless a later exact accepted version changes this value under EO-15.1

## 1. Purpose

This work package integrates the accepted Goal-Oriented Parallel Delivery passive capability with the operating-model adaptations demonstrated by the Milestone 15 Alpha, Bravo, Charlie, and Architecture Integration pilot.

It makes the following outcome governable and testable:

- a durable outcome goal coordinates several independently authorized workstreams;
- workstream authority remains separate and non-transferable;
- dependencies are checked just in time;
- a blocker triggers same-turn eligibility recomputation and continued progress in unaffected lanes;
- decision-bound packages are atomically sealed;
- the Owner receives compact material decisions instead of orchestrating engineering steps;
- repository artifacts, not chat or model memory, are sufficient to recover current work;
- generated evidence is safe for Git; and
- completion is audited requirement by requirement.

This package extends the corrected Version 1.1 passive-capability base. It does not replace EO-14.1A execution semantics, EO-14.4A automation semantics, AI Collaboration governance, Architecture Integration ownership, human approval authority, or the Engineering Lifecycle.

Decision 21 Version 1.1 narrowly incorporates the accepted reusable chat-to-Codex transition prompt into the existing Owner interaction brief target. It adds no repository path and changes no non-prompt architecture, authority, ownership, lifecycle, prohibition, or stop semantic. The Version 1.0 prompt and amendment-subject bindings are superseded and not accepted.

This file is outside the governed repository. It authorizes no repository edit, initiative assignment, implementation, staging, commit, push, operational goal/task use, scheduling, dispatch, persistence, model invocation, protected/network action, production, release, customer, or live work.

## 2. Delivery-Leverage Outcome

The package must measurably:

1. reduce Owner prompt and reconstruction burden;
2. prevent known dependencies from becoming avoidably late blockers;
3. increase throughput by keeping independently eligible lanes active;
4. reduce evidence and approval rework through atomic package sealing;
5. reduce privacy risk by eliminating personal and absolute checkout paths from generated Git evidence; and
6. make a fresh session able to recover the goal and next gate from repository artifacts.

Pilot exit metrics are sanitized counts and durations only. No prompt text, personal name, personal path, customer data, credential, protected value, or detailed local report enters Git.

## 3. Binding Authority and Hierarchy

Authority order remains:

1. permanent governance;
2. approved milestone and architecture artifacts;
3. approved and published specifications or work packages;
4. Active continuity and goal/snapshot evidence; and
5. chat, Codex goal/task state, model memory, or other conversation context.

The Product Board accepted the operating outcome through `goal-delivery-operating-model-adoption-board-acceptance-001`. The Architecture Gatekeeper accepted the architecture for exact work-package preparation through `goal-delivery-operating-model-adoption-gatekeeper-acceptance-001`. Both decisions bind the adoption subject, Owner brief, inspect-and-adapt evidence, constraints, prohibitions, and stop conditions.

The Product Board separately accepted the prompt amendment through `goal-delivery-transition-prompt-amendment-board-acceptance-002`, and the Architecture Gatekeeper independently accepted it through `goal-delivery-transition-prompt-amendment-gatekeeper-acceptance-002`. Those Decision 21 Version 1.1 decisions bind the exact transition prompt, amendment subject, parent adoption package, unchanged 36-path boundary, narrow prompt-only changes, and all preserved prohibitions and stop conditions.

Those decisions authorize this outside-repository preparation only. A valid goal, complete decision reference, passing test, `READY` result, external Codex goal, agent membership, or another workstream decision never creates, authenticates, lends, or widens authority.

## 4. Architecture — Extend Existing Capabilities

### 4.1 Passive goal-delivery capability

Retain the corrected Version 1.1 architecture:

- `goal_delivery_capability.py` owns immutable models, deterministic validation, eligibility, timing, and completion audits;
- `goal_delivery_io.py` owns strict repository-contained JSON loading and serialization;
- `goal_delivery_rendering.py` owns deterministic decision-card and handoff Markdown;
- the CLI exposes only passive validation, evaluation, rendering, and audit commands; and
- all outputs remain standard output with no repository, process, network, environment, or protected side effect.

### 4.2 Repository goal continuity

Add repository-governed operational goal and snapshot artifacts. For every snapshot, the existing `definition` field is exactly one repository-relative regular-file reference string to the exact goal definition. The IO layer must resolve, contain-check, nonsymlink-check, load, and validate that definition before validating the snapshot. It must reject an embedded object, absolute path, traversal, symlink escape, repository mismatch, branch mismatch, and baseline mismatch.

This canonical reference form avoids duplicating the full goal definition in every snapshot while retaining the accepted `GoalSnapshot` field inventory. Fixtures and operational targets must use the same representation; the implementation may not accept an ambiguous union of embedded and referenced definitions.

### 4.3 AI Session integration

AI Session Initialization must identify the active goal and snapshot when the approved work package declares Goal-Oriented Delivery required. Readiness validates that:

- both artifacts are tracked regular nonsymlink files inside the repository;
- their model, repository, branch, baseline, authority references, workstreams, dependencies, active changes, and next gate reconcile with the work package and continuity;
- the snapshot is current under its supplied evidence validity windows; and
- conversation content is not required to recover authority or state.

Readiness remains evidence only. It does not create goals, operate tasks, dispatch agents, update snapshots, authenticate human decisions, or authorize implementation or live work.

### 4.4 Generated-evidence hygiene

`ai_session_readiness.py` must emit:

- sanitized repository identity by name;
- repository-relative tracked paths; and
- no personal name or absolute checkout path in Markdown or JSON.

Absolute paths may be used transiently inside validation logic but must not appear in repository-managed output or stable findings. Focused tests must exercise multiple checkout roots and prove byte-identical sanitized identity output where all repository-relative evidence is otherwise equal.

### 4.5 Owner interaction contract

The Owner brief is governed operating guidance. The Owner supplies outcomes, priority, value judgment, and material decisions. Codex owns routine decomposition, just-in-time checks, parallel coordination, same-turn replanning, evidence, and continued work inside authority. ChatGPT supports strategy, product, architecture, and inspect-and-adapt work. Neither conversation surface becomes repository authority.

The Owner brief must include the accepted reusable transition prompt and optional one-line changed-direction form. The prompt requires applicable `AGENTS.md` and repository-instruction discovery, repository-first recovery and current-state revalidation, persistent-goal use only as coordination state, explicit delegation of independently eligible work to subagents or parallel agents, collection of results in the main task, serialized write-heavy and shared-path work, same-turn replanning, requirement-level authoritative completion evidence, and the smallest seven-field material decision card.

Until governed goal and snapshot recovery is available, the brief may include the exact accepted interim pilot form. That bridge expires when the governed goal, snapshot, decision ledger, and continuity bundle are published and normally recoverable. Neither prompt form grants authority, operates a goal or task, invokes a model, or activates repository capability behavior.

### 4.6 No operational activation

The repository capability remains passive. It does not create or operate Codex goals/tasks, invoke models, select work, schedule, dispatch, wait, monitor, poll, persist runtime state, change infrastructure, acquire artifacts, access protected systems, or perform production or live work.

Using the published operating model as human and Codex process guidance is distinct from activating runtime coordination. Any automated integration or operational goal/task action under the capability requires a later exact package and decision.

For the goal and snapshot models, `activation_occurred`, `dispatch_occurred`, and `live_changes_occurred` describe effects caused by the repository capability itself. The current Owner-authorized use of external Codex coordination surfaces is contextual evidence, not capability activation or capability dispatch, and it cannot be used to imply repository runtime authority.

## 5. Exact Changed-Path Allowlist and Ownership

All unlisted paths are prohibited. The implementation package contains exactly 36 repository paths.

### 5.1 Codex Implementation Engineer-owned capability paths — 19

1. `docs/milestones/Milestone_15/Goal_Oriented_Parallel_Delivery_Passive_Capability_Work_Package.md`
2. `docs/engineering-organization/Goal_Oriented_Parallel_Delivery_Specification.md`
3. `docs/engineering-organization/Goal_Oriented_Parallel_Delivery_Usage.md`
4. `docs/engineering-organization/Parallel_Workstream_Delivery_Model.md`
5. `docs/engineering-organization/Engineering_Workspace_Model.md`
6. `docs/engineering-organization/Governed_Automation_Framework.md`
7. `docs/engineering-organization/Governed_Automation_Framework_Usage.md`
8. `docs/engineering-organization/ai-collaboration/AI_Collaboration_Governance_Specification.md`
9. `engineering/platform_eap/goal_delivery_capability.py`
10. `engineering/platform_eap/goal_delivery_io.py`
11. `engineering/platform_eap/goal_delivery_rendering.py`
12. `engineering/platform_eap/ai_session_readiness.py`
13. `engineering/tests/test_goal_delivery_capability.py`
14. `engineering/tests/test_ai_session_readiness.py`
15. `engineering/tests/fixtures/goal_delivery/valid_definition.json`
16. `engineering/tests/fixtures/goal_delivery/valid_snapshot.json`
17. `engineering/tests/fixtures/goal_delivery/awaiting_decision_snapshot.json`
18. `docs/engineering-organization/Owner_Engineering_Organization_Interaction_Brief.md`
19. `docs/engineering-organization/Engineering_Memory_Concept.md`

### 5.2 Architecture Integration-owned shared paths — 17

1. `engineering/platform_eap/cli.py`
2. `docs/engineering-organization/Engineering_Organization_Vision.md`
3. `docs/engineering-organization/AI_Role_Catalog.md`
4. `docs/engineering-organization/Human_Role_Catalog.md`
5. `docs/engineering-organization/Engineering_Organization_Roadmap.md`
6. `docs/engineering-organization/Engineering_Organization_Backlog.md`
7. `docs/portfolio/Engineering_Portfolio_Kanban.md`
8. `docs/milestones/Milestone_15/Milestone_15_Portfolio_Plan.md`
9. `docs/engineering-organization/ai-collaboration/AI_Session_Initialization_Standard.md`
10. `docs/engineering-organization/ai-collaboration/AI_Session_Completion_Standard.md`
11. `docs/engineering-organization/ai-collaboration/Workstream_Continuity_Brief_Specification.md`
12. `docs/engineering-organization/ai-collaboration/templates/Workstream_Continuity_Brief_Template.md`
13. `docs/engineering-organization/ai-collaboration/operational/milestone-15/Architecture_Integration_Continuity_Brief.md`
14. `docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Continuity_Brief.md`
15. `docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Pilot_Goal.json`
16. `docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Pilot_Snapshot.json`
17. `docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Pilot_Inspect_and_Adapt.md`

The five documents listed in section 5.1 items 4–8 are capability specifications owned for implementation drafting by the Codex Implementation Engineer. Architecture Integration must nevertheless review their consistency with shared lifecycle and role semantics before staging.

No path may be edited concurrently by both owners. Charlie publication must be committed, pushed, fetched, and proved remotely equal before any Alpha or adoption shared-path repository application.

## 6. Exact Prepared Repository Targets

The outside-repository preparation package binds these exact proposed target artifacts:

| Target repository path | Prepared source | SHA-256 |
|---|---|---|
| `docs/engineering-organization/Owner_Engineering_Organization_Interaction_Brief.md` | `Target_Bytes_v1/docs/engineering-organization/Owner_Engineering_Organization_Interaction_Brief.md` | `d84bd7b3e9091449e6c40db61446787edf348ef54015cd7be4c0e61d97187c21` |
| `docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Pilot_Goal.json` | `Target_Bytes_v1/docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Pilot_Goal.json` | `a7211fffba1dde92e7593a7992067f6809c72747063984aefe410d73aa69b9f6` |
| `docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Pilot_Snapshot.json` | `Target_Bytes_v1/docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Pilot_Snapshot.json` | `83c8a2a88a66729cd6a118dcbc3522d7c777328f7a2cbbb00a96d7a610328204` |
| `docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Pilot_Inspect_and_Adapt.md` | `Target_Bytes_v1/docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Pilot_Inspect_and_Adapt.md` | `838a874518187d58a274624e7ed7e485e059e86c411e811943ab9642cd76f2d3` |

These prepared bytes are proposed targets only. The Owner brief and inspect-and-adapt bytes may become current repository evidence only after exact package acceptance, application, validation, staging, commit, push, fetch, and local/tracking/live remote equality proof.

The goal and snapshot are schema-complete bootstrap proposals prepared against baseline `797a658397acde849c0f604b1893dcb1f834c162`. Charlie publication necessarily changes the future application baseline, and snapshot evidence validity changes with time. Therefore an authorized application package must regenerate and rebind only their baseline, observation times, validity windows, current workstream/dependency state, evidence references, issues, and next decision after Charlie remote equality. It may not change the accepted outcome, requirements, authority model, record shapes, prohibitions, or completion gate without a new Product Board and Architecture Gatekeeper decision.

Decision 24 publication-package preparation performs that narrow rebind against exact Charlie equality baseline `b5ecc7dde4cf581a6c1bfc02b7ee7361c95279fd` and snapshot observation `2026-07-27T23:59:21Z`. The work-package publication target is serialized after the accepted Alpha Version 1.1 target SHA-256 `2262a2fa5902e2e8058286c463ac0410266f63267d6139c9d3f047655bd6707b`. No accepted outcome, requirement, authority semantic, record shape, prohibition, completion gate, path, or ownership boundary changes.

## 7. Required Specification and Policy Changes

### Engineering Organization Vision

Add the durable goal as the coordination unit and identify reduced Owner orchestration and session-independent recovery as success measures.

### AI and Human Role Catalogs

Preserve all existing authority boundaries while adding:

- Owner outcome/value/material-decision responsibilities;
- ChatGPT strategy and workshop support as non-authoritative working context;
- Codex goal coordination, just-in-time checks, same-turn replanning, and evidence duties inside approved envelopes; and
- an explicit rule that the Owner is not the routine delivery orchestrator.

### Parallel Workstream Delivery Model

Evolve “one Codex task per workstream” into:

- one durable goal per approved outcome;
- one authority envelope and at most one active item per workstream;
- multiple agents/tasks only as execution surfaces subordinate to the goal and separate authority;
- Architecture Integration serialization for shared paths; and
- automatic continuation inside current authority until a material decision or genuine external blocker.

### Engineering Workspace and Memory

Add the repository goal, snapshot, decision ledger, dependency observations, and completion evidence as durable Engineering Memory. Conversation history and model memory remain optional aids, never required inputs.

### AI Session Standards and Continuity

Initialization identifies and validates active goal/snapshot evidence. Completion updates or proposes snapshot, evidence, decisions, unresolved issues, and next gate. Continuity briefs reference the goal and snapshot instead of duplicating authority or relying on a prompt transcript.

### Governed Automation

Clarify that EO-14.4A automation remains one approved automation flow. Goal coordination remains advisory portfolio state and may reference automations only through existing strict validation and subset authority checks.

## 8. Passive Model Amendments

Retain every Version 1.1 record and enum. Add no runtime lifecycle or agent registry.

The implementation must additionally validate:

1. an operational snapshot's canonical repository-relative `definition` reference and rejection of embedded or ambiguous representations;
2. required goal/snapshot references declared by a governed work package;
3. exact decision references without treating structural validity as human-authentication proof;
4. current dependency observations and latest-safe-check calculation;
5. every active workstream has one active item at most;
6. every blocked or awaiting-decision stream coexists with a stable list of all independently eligible streams;
7. shared-path overlaps and lease conflicts fail closed;
8. completion evidence is mapped to every acceptance requirement;
9. activation, dispatch, and live-change flags remain false; and
10. all output contains sanitized repository identity and repository-relative evidence only.

The three passive-state flags cover effects of the repository capability. They do not deny or conceal separately authorized coordination performed through an external Codex surface, and external coordination does not satisfy, authenticate, or activate the repository capability.

## 9. Atomic Package-Sealing Contract

Every decision-bound external package must:

1. finish all substantive target artifacts;
2. stop all writers;
3. run semantic, schema, path, privacy, applicability, and test checks;
4. compute target hashes;
5. produce manifest and audit;
6. compute manifest and audit hashes;
7. produce the decision card last;
8. independently recompute every bound hash; and
9. reject any later write unless the package is explicitly superseded and rebound.

Tests must demonstrate that a manifest or audit changed after decision-card creation causes exact binding failure.

## 10. Validator-Output Preflight Contract

Before an authorized repository application runs a validator, the package must classify every potentially modified tracked report and pre-authorize exactly one outcome:

- include and reconcile exact generated evidence;
- run only in an isolated projection and keep reports outside the governed diff; or
- stop before the mutating validator.

Current report restoration and later report publication require separate exact decisions. A passing validator never authorizes its generated paths for staging.

## 11. Required Tests

In addition to every corrected Version 1.1 test, focused coverage must prove:

1. repository goal and snapshot strict parsing and byte-stable serialization;
2. canonical repository-relative snapshot definition handling and rejection of embedded or ambiguous forms;
3. repository containment, traversal, symlink, branch, baseline, and identity failures;
4. exact authority references are structurally required but not authenticated by the validator;
5. goal membership never transfers authority;
6. one active item per workstream;
7. blocked-lane same-turn eligibility returns every unaffected eligible lane without dispatch;
8. dependency latest-safe-check timing and stale evidence behavior;
9. completion fails until every acceptance requirement has authoritative evidence;
10. atomic sealing detects any post-card artifact change;
11. AI Session Readiness requires declared goal continuity and reconciles work package, goal, snapshot, Git state, and continuity;
12. AI Session Readiness emits no personal name or absolute checkout path from different synthetic checkout roots;
13. generated Markdown and JSON use sanitized repository identity and repository-relative paths;
14. Owner brief and inspect-and-adapt target artifacts have required sections and no forbidden content;
15. the Owner brief carries the exact accepted recommended prompt and optional changed-direction form;
16. the interim pilot form is exact and carries its governed-recovery expiry condition;
17. applicable `AGENTS.md` and repository-instruction discovery is required before work;
18. the persistent Codex goal is coordination state and never authority;
19. independently eligible work is explicitly delegated and collected in the main task while shared-path writes remain serialized;
20. completion requires requirement-level authoritative evidence and no unresolved material issue;
21. incomplete recovery or authority produces the smallest exact seven-field decision card;
22. activation, dispatch, persistence, model invocation, protected, network, production, release, customer, and live-work behavior remain absent; and
23. all new CLI commands remain standard-output-only and leave the repository byte-identical.

## 12. Validation Plan

An authorized implementation must run, in a correctly named isolated projection first:

1. focused goal-delivery and AI-readiness tests;
2. `python3 -m pytest -p no:cacheprovider engineering/tests`;
3. strict goal-definition and snapshot validation against the exact proposed targets;
4. eligibility evaluation and decision-card rendering;
5. completion audit proving the current pilot is not falsely complete;
6. a sanitized-output scan for personal names, absolute paths, credentials, customer data, protected values, external URLs, and executable directives;
7. Repository Validation;
8. Governance Validation;
9. AI Session Readiness;
10. applicable Engineering Metrics and capability validation;
11. Markdown-link and tracked-artifact hygiene checks;
12. literal changed-path and target-hash audit;
13. `git diff --check`; and
14. after separately authorized staging, `git diff --cached --check`.

Any mutating validator output must follow the preflight contract. Validation results are evidence, never implementation, staging, publication, activation, release, or live-work authority.

## 13. Fresh-Session Recovery Acceptance Test

A reviewer starts from a clean, synchronized repository and receives only:

- repository location;
- the command to perform governed initialization; and
- the assigned governed role.

The reviewer must recover, without prior chat history or model memory:

- the goal outcome and acceptance requirements;
- current workstreams and separate authority envelopes;
- current Git and shared-path state;
- dependency observations and latest-safe checks;
- accepted and missing decisions;
- completed and missing evidence;
- prohibited actions and stop conditions; and
- the exact next material gate.

The reviewer records a sanitized recovery audit. Any required prompt transcript, inaccessible conversation, personal path, unstated approval, or memory-only fact fails the test.

## 14. Owner Interaction Acceptance

The published operating model must make the following normal behavior explicit:

- the Owner states outcomes, value, priority, constraints, and material decisions;
- ChatGPT facilitates strategy, product, architecture, and inspect-and-adapt work;
- Codex executes and coordinates authorized engineering work, checks dependencies, replans, validates, and continues;
- the reusable transition prompt requires repository-first recovery, applicable `AGENTS.md`, explicit delegation of independently eligible work, main-task integration, and serialization of write-heavy or shared-path work;
- the persistent Codex goal remains coordination state and not authority;
- the optional Owner addition contains only changed outcome, priority, constraint, or exact decision information;
- the interim pilot form expires when normal governed goal and snapshot recovery is available;
- the Owner is not responsible for routine task decomposition, dependency timing, agent coordination, state reconstruction, or continuation prompts; and
- Codex stops only for material human authority, scope expansion, destructive/high-impact action, or a genuine external dependency.

## 15. Pilot Measures and Completion Audit

The inspect-and-adapt artifact records sanitized:

- material Owner-decision count;
- “continue-only” prompt count;
- decision wait time;
- late dependency count;
- blocked streams with eligible alternatives;
- eligible-lane continuation rate;
- binding-drift regenerations;
- safety-review stops caused by insufficient risk language;
- chat-history reconstruction events; and
- acceptance requirements with authoritative evidence.

The completion audit remains advisory. It cannot close the goal, milestone, release, or pilot by itself.

## 16. Explicit Non-Goals and Prohibitions

- Assign `CANDIDATE-EO-15.2` or any permanent initiative identifier by implication.
- Replace or reinterpret EO-14.1A participant, role, assignment, execution, validation, evidence, completion, or handoff semantics.
- Replace or reinterpret EO-14.4A automation lifecycle, approvals, transitions, or activation state.
- Create a generalized agent runtime, participant registry, discovery mechanism, plugin framework, autonomous work selection, or dynamic authority system.
- Treat a structurally valid decision reference as authenticated human approval.
- Treat chat history, Codex goal state, or model memory as authority.
- Create or operate goals/tasks, schedule, dispatch, wait, poll, monitor, persist runtime state, or invoke a model as an effect of the repository capability.
- Access credentials, protected systems, customer data, production, or live infrastructure.
- Implement Charlie behavior or PLAT-15.1A Gate 2 under this package.
- Stage, commit, push, merge, tag, publish, activate, deploy, release, or perform live work without separate exact authority.

## 17. Stop Conditions

Stop and return an exact decision card if:

- the corrected Version 1.1 base digest is absent or changes;
- the accepted transition-prompt or Version 1.1 amendment-subject file or internal digest is absent or changes;
- a Version 1.0 prompt or amendment-subject binding is treated as accepted or operative;
- the adoption subject or any prepared target hash changes;
- Charlie publication and remote equality are incomplete before shared-path application;
- a path falls outside the 36-path allowlist or ownership is ambiguous;
- repository, branch, baseline, tracking, active changes, or shared-path lease differs from the accepted initialization;
- the candidate is represented as assigned or implementation-ready;
- goal membership, a validator, chat context, or another stream is used to infer authority;
- the snapshot requires conversation history to recover state;
- generated evidence contains a personal name or absolute checkout path;
- a mutating validator has no pre-authorized output disposition;
- atomic sealing is incomplete or a bound artifact changes after the decision card;
- any test or validator has a blocking error;
- runtime dispatch, persistence, scheduling, model invocation, protected/network/customer/production/release/live behavior becomes necessary; or
- publication, implementation, staging, commit, push, activation, or an adjacent workstream action is requested without separate authority.

## 18. Acceptance and Delivery Gates

### Gate A — Exact consolidated work-package acceptance

The Product Board accepts the operating outcome, Owner interaction, accepted Version 1.1 transition prompt, and Delivery Leverage. The Architecture Gatekeeper accepts this exact package digest, corrected base digest, prompt-amendment bindings, 36-path allowlist, architecture, contracts, tests, targets, non-goals, and stops. Acceptance authorizes only the effect explicitly stated.

### Gate B — Repository publication-package preparation

After Charlie remote equality and a clean synchronized baseline, prepare one exact repository publication package for the accepted work package and permitted governance targets. Reconcile every shared path and generated report before mutation.

### Gate C — Work-package publication

Apply, validate, stage, commit, push, fetch, and prove local/tracking/live equality through separate exact gates. Publication does not assign the candidate or authorize implementation.

### Gate D — Initiative assignment and implementation initialization

The Product Board assigns a permanent initiative identifier and status through an explicit portfolio decision. A separate fetched and synchronized AI Session Initialization binds the exact post-publication commit, role, paths, tests, authority, and stop conditions.

### Gate E — Capability implementation

The Codex Implementation Engineer changes only the 19 owned paths. Architecture Integration changes only the 17 shared paths under separate sequencing. No concurrent shared-path edit is permitted.

### Gate F — Validation and Architecture Gatekeeper acceptance

Run all focused, governed, privacy, continuity, fresh-session, and completion tests. The Gatekeeper reviews the exact diff and evidence. Acceptance does not authorize publication unless stated.

### Gate G — Implementation publication

Stage, commit, push, fetch, and remote-equality proof remain separate exact gates.

### Gate H — Operating-model effectiveness and fresh-session proof

After implementation publication, perform the fresh-session recovery test and inspect-and-adapt measures. The Owner brief and goal continuity become current process guidance only as stated by their published lifecycle fields.

### Gate I — Later operational-use or activation decision

Any automatic goal/task creation or operation, scheduling, dispatch, persistence, model invocation, integration into a runtime service, protected access, production action, release, or live work requires a later exact package and approval.

## 19. Definition of Done

The consolidated implementation is complete for review only when:

- every one of the 36 paths matches the accepted target or specified implementation contract;
- every focused and governed test passes;
- goal and snapshot targets validate;
- a blocked lane exposes independently eligible lanes without dispatch;
- dependency timing and stale evidence behavior are deterministic;
- generated evidence contains no personal name or absolute checkout path;
- the Owner brief and role catalogs preserve human authority and remove routine Owner orchestration;
- a fresh session recovers the exact goal without chat history;
- atomic sealing and mutating-validator preflight are proved;
- every acceptance requirement has a truthful evidence status;
- no runtime activation or live behavior exists; and
- repository status and next gate are exact.

Definition of Done is evidence for review. It is not publication, initiative assignment, activation, release, goal completion, or live-work authority.

## 20. Current Decision Boundary

The only completed action represented by this version is exact outside-repository work-package and target preparation under Decisions 11, 12, and 21 Version 1.1.

The next material decision is whether the Product Board and Architecture Gatekeeper accept the atomically sealed package, corrected base digest, target hashes, and 36-path implementation boundary for later repository publication-package preparation only.
