# Registry Container Identity Migration Framework

**Status:** Implemented; Published

This directory contains governed repository evidence for the Registry Container Identity Foundation migration planner. Planning and review are read-only. The evidence catalog covers every current `service` and `planned_service` record and does not establish live state.

The current plan accounts for all 39 Registry records:

- Five reviewed non-container or logical subjects have proposed `not_applicable` declarations.
- Five confirmed active container services remain review-required because policy, health-check, or approval evidence is incomplete.
- Two planned container services remain review-required and intentionally unactivated.
- Nine subjects remain unresolved.
- Eighteen non-service record-domain subjects are deterministic `not_applicable` / `no_change` candidates based on their governed record types.

Pi-hole remains unresolved for exact Compose project, Compose service, health-check requirement, and compatible policy reference. Its Compose path and runtime-name candidate cannot fill those gaps.

## Commands

```text
./platform-eap registry schema-version
./platform-eap registry migration plan
./platform-eap registry migration review
./platform-eap registry migration status
```

Mutation is never the default. The canonical plan binds record and evidence-file hashes and remains pending until it is bound to a separate governed approval artifact. The artifact must strictly identify the exact plan ID, schema and migration-model versions, approved Registry-migration scope, timezone-aware decision timestamp, Architecture Gatekeeper authority, and governed review reference. Its content hash is bound into the derived plan presentation; executor authorization reloads and verifies the exact artifact.

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

No current Registry record is migrated by this implementation package.
