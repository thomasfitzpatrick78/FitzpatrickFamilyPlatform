# Registry Container Identity Migration Framework

**Status:** Published Baseline; Exact Five-Record Migration Completed and Validated

This directory contains governed repository evidence for the Registry Container Identity Foundation migration planner. Planning and review are read-only. The evidence catalog covers every current `service` and `planned_service` record and does not establish live state.

The current plan accounts for all 39 Registry records:

- Five reviewed non-container or logical subjects have governed `not_applicable` current-state declarations.
- Five confirmed active container services remain review-required because policy, health-check, or approval evidence is incomplete.
- Two planned container services remain review-required and intentionally unactivated.
- Nine subjects remain unresolved.
- Eighteen non-service record-domain subjects are deterministic `not_applicable` / `no_change` candidates based on their governed record types.

Pi-hole remains unresolved for exact Compose project, Compose service, health-check requirement, and compatible policy reference. Its Compose path and runtime-name candidate cannot fill those gaps.

## Plan Identity and Idempotency

The original pending model-v1 plan `sha256:68703b2424c37c2332dfd405360a90f1d51994969c535288006faeb3f2cafc94` is superseded and ineligible for approval. It duplicated each mutable apply target as immutable hashed supporting evidence, so a first application would make second execution fail evidence-drift validation.

Migration model `registry-container-identity-migration-v2` separates four authority roles:

1. `source_sha256` binds the exact original target Registry record;
2. `evidence` binds only supporting files expected to remain immutable during application;
3. `proposed_fields` is the exact canonical patch;
4. `expected_post_sha256` binds the exact source-plus-patch result.

All approval, version, authority, scope, artifact-hash, subject, path, and supporting-evidence checks remain mandatory before state evaluation. Exact source state permits first application. Exact expected post-state returns write-free `no_change`. Partial application, unrelated target drift, stale source, external evidence drift, and obsolete plans fail closed.

Historical approved plan `sha256:5addac8821f1a177792240b04c4727e1cc21144c75ab140a1fc8beb93490549f` retains the exact pre-migration source, patch, evidence, and expected-post contract that was reviewed, bound, and executed. It is not regenerated from post-migration records. Current read-only plan `sha256:78b3ddcab944e35a5c70bbe991971ab0c939c7c17f7860651a010cecfc24598a` describes the migrated Repository with 0 apply, 16 review-required, and 23 no-change candidates. Its five governed current-state declarations do not imply a new approval.

## Approval Evidence

Architecture Gatekeeper approved all five exact patches in principle. The governed review document is `docs/milestones/Milestone_14/Registry_Container_Identity_Migration_Approval_Review.md`; the exact JSON artifact is `approvals/registry-container-identity-plan-5addac8821f1-approval.json`.

The exact artifact is bound to `registry-container-identity-plan-5addac8821f1-bound.json`. Its content hash is `13f7fdaa41f29d4624f58d361ac7a50ef142ba156f1a1b20113e787a17871bf3`; the bound-plan content hash is `c50f417dd23ae181022f994bdbd628ddabe86257d1e6d30cd7b70ceab2dfd9fc`. The bound plan executed exactly five patches. Rollback artifact `rollbacks/registry-container-identity-plan-5addac8821f1-rollback.json` has SHA-256 `5bf638d614c92657e7989cf67a31b5e7e3cf2ef8d480df15c00b7d6ee507bdaa` and validates exact original and migrated states. A second confirmed execution returned `no_change` without altering Registry or rollback bytes. The 16 review-required subjects remain unchanged, and Pi-hole remains unresolved and unapproved.

## Commands

```text
./platform-eap registry schema-version
./platform-eap registry migration plan
./platform-eap registry migration review
./platform-eap registry migration status
./platform-eap registry migration validate-completed --plan PATH --rollback PATH
```

Mutation is never the default. The canonical plan binds source, immutable-evidence, patch, and expected-post-state hashes and remains pending until it is bound to a separate governed approval artifact. The artifact must strictly identify the exact plan ID, schema and migration-model versions, approved Registry-migration scope, timezone-aware decision timestamp, Architecture Gatekeeper authority, and governed review reference. Its content hash is bound into the derived plan presentation; executor authorization reloads and verifies the exact artifact.

```text
./platform-eap registry migration apply --plan PATH --rollback-output PATH --dry-run
./platform-eap registry migration apply --plan PATH --rollback-output PATH --confirm
./platform-eap registry migration rollback --metadata PATH --confirm
```

After an Architecture Gatekeeper approval artifact is separately created under `registry/migrations/`, the read-only binding command emits a derived plan without modifying the source plan or Registry:

```text
./platform-eap registry migration bind-approval --plan PATH --approval PATH
```

Changing serialized plan approval fields, pointing to an arbitrary repository document, or changing the approval artifact after binding cannot authorize execution. Apply requires an explicit rollback output even during CLI dry-run so review uses the same bounded command shape. Actual execution writes only reviewed Registry record fields, validates the entire Registry, and restores original files automatically if validation or rollback-metadata publication fails. Rollback refuses drift and restores exact prior file bytes.

Exactly five Registry records were migrated by the historical approved plan. No provider, runtime, health-assessment, activation, rollback, or live-infrastructure action occurred.
