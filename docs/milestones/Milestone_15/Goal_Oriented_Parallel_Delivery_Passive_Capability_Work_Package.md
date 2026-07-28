# Goal-Oriented Parallel Delivery Passive Capability — Exact Governed Work Package

**Document Version:** 1.1
**Status:** Prepared Outside Repository; Proposed for Product Board and Architecture Gatekeeper Acceptance; Not Published
**Implementation State:** Not Authorized; Not Started
**Candidate Initiative Identifier:** `CANDIDATE-EO-15.2` — unassigned and not approved
**Milestone:** Milestone 15
**Governed Repository:** `FitzpatrickFamilyPlatform`
**Target Repository Path:** `docs/milestones/Milestone_15/Goal_Oriented_Parallel_Delivery_Passive_Capability_Work_Package.md`
**Accepted Architecture Subject:** `Alpha_Goal_Delivery_Proposed_Governed_Work_Package_Subject.json`
**Accepted Subject SHA-256:** `da3da4646fd32bb13aaa7804b2007935bfdf53e66d48e6d019e0313fa9c816ad`
**Architecture Decision State:** Accepted for conversion into this exact work-package artifact only
**Expected Generated Evidence Baseline:** Prohibited unless a later accepted repository version expressly changes this value under EO-15.1

## 1. Purpose

This proposed work package converts the accepted Alpha architecture subject into a repository-ready authority artifact for a passive goal-delivery capability.

The capability would make a portfolio outcome, separately authorized workstream bindings, authority envelopes, dependency freshness and timing, blocked-stream reallocation advice, exact decision cards, integration handoffs, and requirement-level completion audits machine-checkable. It would not create or operate work. Codex goals and tasks remain an external coordination surface. Repository artifacts remain the authority and evidence surface.

This file is currently outside the governed repository. It is not published authority, does not assign an initiative identifier, and authorizes no repository edit, implementation, staging, commit, push, pilot, Codex goal or task action under this package, scheduling, dispatch, persistence, model invocation, protected or network action, activation, production, release, or live work.

## 2. Objective and Delivery-Leverage Outcome

Add a passive repository-governed validation surface that reduces owner prompt burden and prevents known dependency checks from becoming late blockers while preserving every existing authority boundary.

The intended organizational outcome is:

- one durable outcome can reference several independently authorized workstreams without lending authority between them;
- dependency freshness, need-by points, and latest-safe-check time are deterministic and reviewable;
- blocked work exposes other independently eligible work without dispatching it;
- material decisions render as a seven-field exact card;
- completion is audited against acceptance evidence rather than prompt or artifact count; and
- EO-14.1A execution semantics, EO-14.4A automation semantics, repository-first authority, Architecture Integration, and all closed operational gates remain unchanged.

## 3. Binding Authority and Hierarchy

This proposed package is subordinate to permanent governance and current approved milestone and architecture artifacts. When authority conflicts, the repository hierarchy remains:

1. permanent governance;
2. approved milestone and architecture artifacts;
3. an approved and published specification or work package;
4. an Active Workstream Continuity Brief; and
5. chat, Codex goal, Codex task, or other conversation context.

The accepted subject digest binds the architecture, exact paths, ownership split, model, CLI, fixtures, tests, non-goals, stop conditions, and gates in this version. The subject itself remains outside the repository and is evidence of the accepted preparation decision, not future implementation authority.

No goal, task, workstream membership, structurally valid decision reference, `READY`, passing validator, clean tree, or another stream's approval creates, transfers, authenticates, or widens authority.

## 4. Baseline Rules

### 4.1 Publication-preparation baseline

This exact outside-repository artifact was prepared against:

- repository `FitzpatrickFamilyPlatform`;
- branch `main`;
- local `HEAD` `797a658397acde849c0f604b1893dcb1f834c162`;
- locally cached `origin/main` equal to that `HEAD`; and
- ahead/behind `0/0` with a clean worktree and staging area.

Alpha performed no network fetch while preparing this artifact and makes no fresh live-remote claim.

Before any repository publication action, Architecture Integration must independently prove the repository is still clean, nondiverged, and at this exact publication-preparation baseline. Any drift, dirty state, new untracked path, changed tracking state, authority change, or material repository difference stops publication and requires explicit rebind or regeneration.

### 4.2 Implementation baseline

Publication necessarily creates a later repository commit, so `797a658397acde849c0f604b1893dcb1f834c162` is not implementation initialization authority.

Implementation may initialize only after:

1. this exact work package is accepted for publication and published through its separate gates;
2. the permanent initiative identifier is assigned and recorded by the proper authority;
3. a publication record identifies the exact clean synchronized commit containing this package;
4. Architecture Integration has resolved all shared-path ownership and sequencing;
5. a separately authorized AI Session Initialization binds the implementation session to that exact post-publication commit; and
6. no higher authority has superseded or contradicted the package.

Any implementation baseline must be clean, current, synchronized, and exact. A later clean head does not silently rebind this package.

## 5. Architecture Decision — Extend, Do Not Replace

The implementation shape is three new passive companion modules:

- `engineering/platform_eap/goal_delivery_capability.py`;
- `engineering/platform_eap/goal_delivery_io.py`; and
- `engineering/platform_eap/goal_delivery_rendering.py`.

Architecture Integration may expose the capability through `./platform-eap delivery-goal` only within the accepted shared-path boundary.

Portfolio-goal semantics must not be added to `automation_capability.py`. EO-14.4A owns one approved automation flow and its lifecycle. A portfolio goal spans several separately authorized workstreams. Embedding the goal into EO-14.4A would risk making a workstream appear to inherit an automation's scope, approvals, or transition eligibility.

The companion capability must:

- reuse public EO-14.1A `ValidationFinding`, `FindingSeverity`, repository-path, timestamp, secret-content, assignment IO, and assignment validation interfaces;
- use EO-14.4A strict definition IO and `validate_automation_definition` for referenced automation definitions;
- require referenced EO-14.4A repository scope to remain a subset of its workstream authority envelope;
- require referenced EO-14.1A assignments to match repository identity, baseline, and repository scope;
- avoid private imports, subclassing, alternate assignment/completion models, or alternate automation lifecycle/approval models; and
- treat workstream coordination state as advisory portfolio state, not an EO-14.4A lifecycle state or an authority source.

## 6. Exact Changed-Path Allowlist and Ownership

All paths not listed in this section are prohibited.

### 6.1 Alpha-owned paths — exactly 15

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
12. `engineering/tests/test_goal_delivery_capability.py`
13. `engineering/tests/fixtures/goal_delivery/valid_definition.json`
14. `engineering/tests/fixtures/goal_delivery/valid_snapshot.json`
15. `engineering/tests/fixtures/goal_delivery/awaiting_decision_snapshot.json`

### 6.2 Architecture Integration-owned shared paths — exactly 9

1. `engineering/platform_eap/cli.py`
2. `docs/engineering-organization/Engineering_Organization_Roadmap.md`
3. `docs/engineering-organization/Engineering_Organization_Backlog.md`
4. `docs/portfolio/Engineering_Portfolio_Kanban.md`
5. `docs/milestones/Milestone_15/Milestone_15_Portfolio_Plan.md`
6. `docs/engineering-organization/ai-collaboration/Workstream_Continuity_Brief_Specification.md`
7. `docs/engineering-organization/ai-collaboration/templates/Workstream_Continuity_Brief_Template.md`
8. `docs/engineering-organization/ai-collaboration/operational/milestone-15/Architecture_Integration_Continuity_Brief.md`
9. `docs/engineering-organization/ai-collaboration/operational/milestone-15/Goal_Oriented_Parallel_Delivery_Continuity_Brief.md`

Alpha may specify and test the required CLI hook and traceability content. Architecture Integration owns all changes to the nine shared paths and must sequence them against Charlie and every other active workstream before edit or staging. No shared path may be treated as concurrently Alpha-owned.

## 7. Passive Model Contract

The stable candidate model version is `eo-goal-delivery-v1`. All domain records are frozen value objects.

### 7.1 Bounded enums

| Enum | Values |
|---|---|
| Goal state | `proposed`, `active`, `awaiting_decision`, `blocked`, `integrating`, `completed`, `cancelled` |
| Authority state | `proposed`, `authorized`, `suspended`, `closed` |
| Authority-decision status | `accepted`, `rejected`, `superseded`, `expired` |
| Workstream coordination state | `proposed`, `pending`, `eligible`, `active`, `awaiting_decision`, `blocked`, `integrating`, `complete` |
| Dependency kind | `repository`, `toolchain`, `environment`, `protected_authority`, `data_dependent_authority`, `external_event`, `integration`, `human_decision` |
| Dependency status | `unknown`, `unsatisfied`, `satisfied`, `unavailable`, `expired` |
| Decision recommendation | `approve`, `reject`, `regenerate`, `defer` |

### 7.2 Required records and fields

| Record | Exact fields |
|---|---|
| `GoalAcceptanceRequirement` | `requirement_id`, `statement`, `required_evidence_types`, `required_evidence_references` |
| `AuthorityDecisionReference` | `decision_id`, `human_authority`, `subject_sha256`, `decision_status`, `decided_at`, `governing_artifact_reference` |
| `AuthorityEnvelope` | `workstream_id`, `assigned_role`, `work_package_references`, `authority_decision_references`, `owned_repository_paths`, `owned_artifact_classes`, `permitted_actions`, `approval_required_actions`, `prohibited_actions`, `required_checks`, `publication_authority`, `stop_conditions`, `integration_return` |
| `WorkstreamDefinition` | `workstream_id`, `title`, `objective`, `acceptance_requirement_ids`, `authority_envelope`, `dependency_ids`, `automation_definition_references`, `execution_assignment_references` |
| `DependencyDefinition` | `dependency_id`, `kind`, `description`, `dependent_workstream_ids`, `prerequisite_workstream_ids`, `evidence_source_references`, `freshness_seconds`, `need_by_at`, `verification_duration_seconds`, `decision_allowance_seconds`, `execution_margin_seconds` |
| `GoalDefinition` | `model_version`, `goal_id`, `name`, `outcome`, `governing_artifact_references`, `repository_identity`, `branch`, `baseline_head`, `acceptance_requirements`, `workstreams`, `dependencies`, `wip_limit_per_stream`, `minimum_parallel_streams`, `completion_gate`, `prohibited_actions` |
| `DependencyObservation` | `dependency_id`, `status`, `checked_at`, `valid_until`, `evidence_references`, `limitation` |
| `WorkstreamObservation` | `workstream_id`, `authority_state`, `coordination_state`, `active_item_id`, `completed_acceptance_requirement_ids`, `evidence_references`, `blocking_issue_ids`, `next_best_action`, `integration_evidence_references` |
| `DecisionSubject` | `decision_id`, `workstream_id`, `human_authority`, `subject_id`, `subject_sha256` |
| `GoalSnapshot` | `model_version`, `definition`, `snapshot_id`, `observed_at`, `goal_state`, `workstream_observations`, `dependency_observations`, `open_decision_cards`, `completion_evidence_by_requirement`, `unresolved_issues`, `activation_occurred`, `dispatch_occurred`, `live_changes_occurred` |
| `PortfolioEligibilityDecision` | `coordination_eligible_workstream_ids`, `blocked_workstream_ids`, `late_dependency_ids`, `stale_dependency_ids`, `findings`, `recommended_next_gate`, `advisory_only` |
| `DecisionCard` | `decision`, `recommendation`, `evidence`, `authority_gained`, `authority_not_gained`, `expiry_or_invalidation`, `response_form` |
| `CompletionAudit` | `complete`, `requirement_evidence`, `missing_requirement_ids`, `incomplete_workstream_ids`, `findings`, `next_gate`, `advisory_only` |

### 7.3 Timing rule

The exact timing calculation is:

`latest_safe_check_at = need_by_at - verification_duration_seconds - decision_allowance_seconds - execution_margin_seconds`

Every timestamp and duration is supplied input. The capability has no clock, timer, polling, scheduling, sleep, monitor, reminder, or wait behavior.

## 8. Validation and Advisory Evaluation Contract

The implementation must fail closed and deterministically:

1. Reject unsupported versions, unknown or missing fields, duplicate IDs, dangling references, self-dependencies, dependency cycles, unsafe or absolute paths, symlink escape, secret-like content, external URLs, executable directives, malformed timestamps, nonpositive freshness, negative timing allowances, and invalid baseline heads.
2. Reject authority-envelope path overlap, referenced automation/assignment scope widening, repository mismatch, and baseline mismatch.
3. Reject `authorized`, `eligible`, `active`, `integrating`, or `complete` claims without a work-package reference and structurally complete authority-decision reference. Structural completeness is not authenticated human approval.
4. Exclude `proposed`, `suspended`, and `closed` workstreams from coordination eligibility even when dependencies are satisfied.
5. Treat evidence checked after `valid_until` as stale or expired, never current.
6. Report lateness when `observed_at` is after `latest_safe_check_at` and no current satisfied observation exists.
7. Return every independently coordination-eligible workstream in stable workstream-ID order. Never select, dispatch, activate, schedule, or mutate one.
8. Enforce `wip_limit_per_stream` equal to one in v1. Treat `minimum_parallel_streams` only as an advisory flow target.
9. Fail when `activation_occurred`, `dispatch_occurred`, or `live_changes_occurred` is true.
10. Pass completion only when every acceptance requirement has its required evidence, every required workstream is complete, and no unresolved issue remains. The audit remains advisory and closes no milestone, automation, workstream, release, or Codex goal.

## 9. Strict IO, CLI, and Rendering Contract

Strict JSON must reject unknown fields and serialize as UTF-8 with two-space indentation, `ensure_ascii=false`, and one trailing newline.

Required CLI commands are exactly:

```text
./platform-eap delivery-goal definition validate <repository-json-path>
./platform-eap delivery-goal snapshot validate <repository-json-path>
./platform-eap delivery-goal eligibility evaluate <repository-json-path>
./platform-eap delivery-goal decision-card render <repository-json-path> <decision-id>
./platform-eap delivery-goal handoff render <repository-json-path>
./platform-eap delivery-goal completion audit <repository-json-path>
```

Every input and referenced artifact must resolve to a regular nonsymlink file inside the repository. Validation emits bounded text; eligibility and completion audit emit stable JSON; decision cards and handoffs emit deterministic Markdown. All output is standard output only.

Exit codes are:

- `0`: pass or advisory decision allowed;
- `1`: validation or advisory-decision failure;
- `2`: invalid usage; and
- `3`: unexpected internal failure.

There is no output-file option and no repository, process, network, protected-local, environment, or external side effect.

## 10. Fixture Contract

Fixtures must be sanitized, fictitious, and repository-relative. They may contain no personal names, absolute paths, credentials, customer data, protected values, network locations, or executable instructions.

- `valid_definition.json`: two independently authorized synthetic workstreams and one dependency with complete passive authority references.
- `valid_snapshot.json`: one active and one independently coordination-eligible workstream with current evidence.
- `awaiting_decision_snapshot.json`: one exact seven-field decision-card input while another workstream remains coordination eligible.

Fixtures are contract evidence only. They do not assert real approval, authorize a stream, or create a Codex goal or task.

## 11. Required Focused Tests

Focused coverage must prove:

1. immutable models, strict byte-stable JSON round trips, unknown-field rejection, and bounded enums;
2. goal membership alone never yields authority or coordination eligibility;
3. proposed, suspended, and closed streams remain ineligible;
4. incomplete authority references fail closed and are never described as authenticated approval;
5. overlap, traversal, absolute paths, symlinks, secret-like values, external URLs, executable directives, scope widening, repository mismatch, and baseline mismatch fail;
6. unknown, self, direct-cycle, and transitive-cycle dependencies fail;
7. only current satisfied evidence supports advisory eligibility;
8. exact latest-safe-check boundary behavior and lateness one second after it;
9. a blocked stream exposes every other independently eligible stream in stable order without dispatch or mutation;
10. one active item per stream and advisory-only minimum parallelism;
11. exactly seven complete decision-card fields while another eligible stream remains available;
12. EO-14.4A references use existing strict IO/validation and remain inside envelope scope;
13. EO-14.1A assignment references use existing public IO/validation without semantic duplication;
14. completion fails for every missing requirement, incomplete stream, unresolved issue, or missing evidence type/reference;
15. true activation, dispatch, or live-change flags fail closed;
16. every CLI command enforces repository-contained regular-file input, stable output, documented exit codes, and zero repository mutation; and
17. existing EO-14.1A, EO-14.4A, AI-session readiness, and container-health suites remain unchanged and passing.

Required focused invocation:

```text
python3 -m pytest -p no:cacheprovider engineering/tests/test_goal_delivery_capability.py
```

Required governed suite:

```text
python3 -m pytest -p no:cacheprovider engineering/tests
```

The implementation session must also run Repository Validation, Governance Validation, and AI Session Readiness and reconcile every generated artifact before publication preparation.

## 12. Roles and Ownership

| Decision or action | Required authority |
|---|---|
| Assign permanent initiative ID and confirm portfolio outcome/priority | Product Strategy Board |
| Accept architecture, exact package, scope, contracts, residual risk, and completion evidence | Chief Architect / Architecture Gatekeeper |
| Implement accepted Alpha-owned paths after published authority and initialization | Codex Implementation Engineer |
| Own, sequence, and integrate the nine shared paths | Architecture Integration |
| Stage, commit, push, merge, tag, or publish | Separate exact repository publication authority |
| Activate a pilot, create/operate goals or tasks under this capability, deploy, release, or perform live work | Later separate authority under existing governance |

The separately Board-authorized preparation coordination goal is external to this package. It creates no repository authority and is not activated, modified, or operated by implementation of this package.

## 13. Explicit Non-Goals and Prohibitions

- Modify, subclass, duplicate, or reinterpret EO-14.1A execution models or EO-14.4A automation models, lifecycle, transitions, approvals, authority, or activation status.
- Create a scheduler, clock, timer, polling loop, monitor, reminder, queue, registry, database, persistence layer, retry worker, background process, resident controller, task dispatcher, or cross-task runtime.
- Create or operate a Codex goal or task as an effect of this package, invoke a model, or choose product or architecture decisions autonomously.
- Authenticate approval from prose or claim structural validation proves authority.
- Execute assignments, mutate repositories from the capability, write reports or files, contact networks, access protected-local evidence, acquire artifacts, create environments, or perform Linux validation.
- Implement PLAT-15.1A source, Charlie Operations Intelligence behavior, provider mappings, dashboards, APIs, notifications, remediation, deployment, activation, release, production, customer-data, or live work.
- Extend AI Session Readiness in this package; consumption of goal snapshots is deferred.
- Commit, push, merge, tag, publish, pilot, or activate without separate exact authority.
- Treat publication of this package as implementation completion or operational readiness.

## 14. Stop Conditions

Stop and return an exact decision card if:

- the publication-preparation baseline is dirty, behind, diverged, changed, or materially different;
- the permanent initiative ID, role, Product Board decision, Architecture Review, work-package acceptance, publication authority, implementation authority, or Gatekeeper decision is absent, ambiguous, contradictory, expired, or superseded;
- a required change lies outside the exact allowlist;
- an Alpha-owned path conflicts with an active workstream;
- Architecture Integration has not disposed a shared-path ownership or sequencing conflict;
- implementation would duplicate or reinterpret EO-14.1A or EO-14.4A semantics;
- structural validation, goal membership, `READY`, a passing validator, or a clean tree would need to be treated as authenticated approval or action authority;
- persistence, scheduling, dispatch, model invocation, executable content, credentials, protected access, network access, customer data, production behavior, activation, release, or live work becomes necessary;
- tests require invented approval, unsupported evidence, personal data, protected data, or external systems;
- generated evidence contains sensitive, absolute-path, customer, protected, or local-only material; or
- publication, implementation, commit, push, pilot, activation, or an adjacent stream action is requested without its separate exact authority.

## 15. Acceptance Gates

### Gate A — Exact work-package acceptance

The Product Board must accept the outcome and ownership model. The Architecture Gatekeeper must accept this exact artifact digest, architecture, allowlist, contracts, tests, non-goals, stops, and gates. The permanent initiative identifier must be assigned separately or this package must continue to identify it only as an unapproved candidate.

Passing Gate A authorizes only what the decision explicitly states. Recommended next authority is repository publication-package initialization, not implementation.

### Gate B — Governed repository publication

Before repository mutation:

1. independently reverify exact baseline and authority;
2. bind the accepted artifact digest and target repository path;
3. prove the initial publication changed-path allowlist and Architecture Integration disposition;
4. create only the accepted repository artifact and exact authorized traceability changes;
5. run required documentation, governance, and repository validation;
6. reconcile generated evidence;
7. prove exact changed and staged paths plus staged whitespace; and
8. obtain separate commit and later push authority.

Commit, push, and remote-equality proof remain separate. Publication is not claimed until a permitted push is followed by fetch and exact local/tracking/live equality proof.

### Gate C — Implementation initialization

Implementation remains closed until the published package, permanent initiative ID, exact post-publication baseline, clean synchronized state, role assignment, shared-path sequencing, and a separately authorized AI Session Initialization all exist.

### Gate D — Implementation and validation

The Codex Implementation Engineer may change only Alpha-owned paths. Architecture Integration alone changes shared paths. Focused and governed tests, validations, evidence reconciliation, changed-path audit, and requirement-level evidence are mandatory.

### Gate E — Architecture Gatekeeper implementation acceptance

The Gatekeeper reviews the exact source diff, tests, reuse boundaries, unresolved risks, and requirement audit. Acceptance does not authorize publication unless stated separately.

### Gate F — Implementation publication

Staging, commit, push, fetch, and remote-equality proof are separate gates. No pilot or activation follows by implication.

### Gate G — Later pilot decision

Any pilot use, goal/task creation or operation under the repository capability, scheduling, dispatch, persistence, integration into AI Session Readiness, deployment, activation, release, production, or live work requires a later separately approved package and decision.

## 16. Definition of Done for a Future Implementation

Future implementation is ready for Gatekeeper source review only when:

- all accepted subject and package requirements map to exact changed-path and test evidence;
- only the 15 Alpha-owned and Architecture Integration-disposed shared paths changed;
- EO-14.1A and EO-14.4A contracts remain authoritative and unchanged in semantics;
- every required focused and governed test passes without cache artifacts;
- Repository Validation, Governance Validation, and AI Session Readiness pass under current authority;
- generated evidence is reconciled and sanitized;
- no runtime, scheduling, dispatch, persistence, model, protected, network, customer, production, activation, release, or live behavior exists;
- repository status and next gate are truthful; and
- the Gatekeeper receives exact diff, path, test, finding, risk, and evidence references.

Definition of Done is evidence for review. It is never publication, activation, release, or live-work authority.

## 17. Current Decision Boundary

The only completed action represented by this version is conversion of accepted subject SHA-256 `da3da4646fd32bb13aaa7804b2007935bfdf53e66d48e6d019e0313fa9c816ad` into this outside-repository exact work-package artifact.

The next material decision is whether the Product Board and Architecture Gatekeeper accept the exact artifact for governed repository publication-package initialization. Until that exact decision is recorded, this artifact remains proposed, outside the repository, not published, and not implementation authority.
