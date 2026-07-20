# Registry Container Identity Foundation Implementation Package

**Status:** Published Baseline; Idempotency Correction Complete and Unpublished

**Milestone:** Milestone 14

**Dependency:** Named prerequisite of PLAT-14.1A

---

## Implemented Scope

- Additive Infrastructure Registry schema `1.1` with unchanged common required fields.
- Closed allowed-field contract preserving all 39 legacy records.
- Conditional container identity validation for `service` and `planned_service`.
- Exact host, Compose tuple, runtime-name, policy, evidence, image, bounded participation-reason, review, and contradiction validation.
- Deterministic migration evidence, candidate, plan, report, result, and rollback models.
- Strict separate migration approval artifact bound to the exact plan ID, schema and migration-model versions, Registry-migration scope, timestamp, Architecture Gatekeeper authority, review reference, and artifact content hash.
- Complete 21-service evidence catalog, deterministic no-change classification for 18 non-service record domains, and read-only planning/review/status output covering all 39 records.
- Approved-plan dry-run and atomic repository update with full-registry validation.
- Exact-content rollback metadata, drift rejection, and idempotent rollback.
- Compatible Registry CLI commands, read-only approval binding, and comprehensive engineering tests.

## Idempotency Correction

Architecture review confirmed that the original model-v1 plan treated each of the five mutable target records as hashed supporting evidence. First execution changed those evidence files, causing second execution to fail evidence-drift validation before reaching the intended no-change path.

The corrected migration model v2:

- uses the candidate source hash as authority for exact original target bytes;
- excludes an apply target from immutable supporting-evidence hashes;
- binds the canonical patch and deterministically derived expected post-migration hash into the plan ID;
- recognizes only the exact plan-bound post-state as already applied;
- returns write-free `no_change` after all approval, version, subject, path, and immutable-evidence checks pass;
- rejects partial patches, unrelated target drift, source drift, external evidence drift, approval drift, malformed or duplicate-key JSON, and obsolete model-v1 plans;
- preserves atomic application, complete Registry and Digital Twin validation, exact rollback, and idempotent rollback.

The old pending plan `sha256:68703b2424c37c2332dfd405360a90f1d51994969c535288006faeb3f2cafc94` is superseded and ineligible for approval. The regenerated model-v2 plan is pending and unapproved. All five classifications and all 39 Registry records remain unchanged.

## Current Migration Status

No Registry record is migrated.

- Five confirmed non-container or logical subjects have evidence-backed `not_applicable` proposals pending plan approval.
- Sixteen subjects require further review.
- Pi-hole remains unresolved for exact Compose project, Compose service, health-check requirement, and compatible policy reference.
- No subject is newly eligible for PLAT-14.1A health assessment.

## Safety Boundary

Planning, review, and approval binding never write Registry records. Mutation requires a canonical plan bound to a separate strict approval artifact under `registry/migrations/`, an exact artifact content hash, affirmative `registry_record_migration` scope, Architecture Gatekeeper authority, a safe governed review reference, explicit confirmation, a rollback metadata destination, matching record and evidence hashes, Registry-record-only paths, atomic writes, and full Registry validation. Self-asserted plan status or an arbitrary existing document cannot authorize mutation. Failure restores original content. Rollback preflights all entries, requires explicit confirmation, refuses drift, and restores exact prior bytes.

The implementation performs no runtime discovery, provider access, monitoring, reconciliation, health evaluation, dashboard work, activation, or live infrastructure activity.

## Commands

```text
./platform-eap registry schema-version
./platform-eap registry migration plan
./platform-eap registry migration review
./platform-eap registry migration status
./platform-eap registry migration bind-approval --plan PATH --approval PATH
./platform-eap registry migration apply --plan PATH --rollback-output PATH --dry-run
./platform-eap registry migration apply --plan PATH --rollback-output PATH --confirm
./platform-eap registry migration rollback --metadata PATH --confirm
```

## Next Gate

Architecture Gatekeeper review of the unpublished idempotency correction and regenerated pending plan is the next gate. Publication, any later approval artifact, and any Registry record migration remain separate decisions.
