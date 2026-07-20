import json
import hashlib
from dataclasses import replace
from pathlib import Path
import shutil

import pytest

from engineering.platform_eap import cli
from engineering.platform_eap.registry_identity import (
    APPROVAL_MODEL_VERSION,
    REGISTRY_MIGRATION_APPROVAL_AUTHORITY,
    REGISTRY_MIGRATION_APPROVAL_SCOPE,
    MigrationApprovalStatus,
    MigrationDataError,
    bind_migration_approval,
    build_migration_plan,
    build_migration_report,
    execute_migration,
    migration_approval_from_json,
    migration_evidence_catalog_from_json,
    migration_plan_from_json,
    migration_plan_to_dict,
    migration_plan_to_json,
    rollback_metadata_from_json,
    rollback_metadata_to_json,
    rollback_migration,
    _plan_id,
)


def write_record(root: Path, relative: str, content: str) -> Path:
    path = root / "registry" / "records" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return path


def create_registry(tmp_path: Path, service_body: str | None = None) -> tuple[Path, Path]:
    schema = tmp_path / "registry" / "schema" / "infrastructure_registry_schema.yaml"
    schema.parent.mkdir(parents=True)
    shutil.copyfile(cli.REGISTRY_SCHEMA, schema)
    common = """
id: {record_id}
record_type: {record_type}
name: {name}
description: Test record.
owner: owner-platform
location: loc-home
lifecycle_status: {lifecycle}
health_status: {health}
monitoring_ready: false
dependencies: []
"""
    write_record(tmp_path, "owners/platform.yaml", common.format(record_id="owner-platform", record_type="owner", name="Owner", lifecycle="active", health="unmonitored"))
    write_record(tmp_path, "locations/home.yaml", common.format(record_id="loc-home", record_type="location", name="Home", lifecycle="active", health="unmonitored"))
    write_record(tmp_path, "hosts/home.yaml", common.format(record_id="host-home", record_type="host", name="Host", lifecycle="active", health="healthy"))
    if service_body is None:
        service_body = """
id: svc-example
record_type: service
name: Example
description: Test service.
owner: owner-platform
location: loc-home
lifecycle_status: active
health_status: healthy
monitoring_ready: false
dependencies:
  - host-home
host_dependencies:
  - host-home
service_dependencies: []
"""
    write_record(tmp_path, "services/example.yaml", service_body)
    (tmp_path / "docs" / "policies").mkdir(parents=True)
    (tmp_path / "docs" / "governance").mkdir(parents=True)
    (tmp_path / "docs" / "evidence.md").write_text("# Evidence\n", encoding="utf-8")
    (tmp_path / "docs" / "governance" / "approval-authority.md").write_text("# Architecture Gatekeeper\n", encoding="utf-8")
    (tmp_path / "docs" / "policies" / "container-health.json").write_text("{}\n", encoding="utf-8")
    return tmp_path / "registry" / "records", schema


def validate_temp_registry(tmp_path: Path, records: Path, schema: Path):
    return cli.validate_registry(records_root=records, schema_path=schema, repository_root=tmp_path)


def error_messages(results) -> list[str]:
    return [result.message for result in results if result.severity == "ERROR"]


def active_identity(extra: str = "") -> str:
    return f"""
id: svc-example
record_type: service
name: Example
description: Test active container service.
owner: owner-platform
location: loc-home
lifecycle_status: active
health_status: healthy
monitoring_ready: false
dependencies:
  - host-home
host_dependencies:
  - host-home
service_dependencies: []
container_identity_contract_version: 1.0
container_participation: active
container_host_reference: host-home
compose_project: platform
compose_service: example
governed_runtime_name: example-runtime
health_check_requirement: required
container_health_policy_reference: docs/policies/container-health.json
container_identity_evidence:
  - docs/evidence.md
{extra}
"""


def test_schema_is_additive_version_1_1_and_repository_records_remain_valid():
    schema = cli.load_registry_schema()
    assert schema["schema_version"] == "1.1"
    assert schema["supported_previous_schema_versions"] == ["1.0"]
    results = cli.validate_registry()
    assert not error_messages(results)
    assert any("Registry validation passed for 39 records" in result.message for result in results)


def test_legacy_service_remains_valid_and_ineligible(tmp_path):
    records, schema = create_registry(tmp_path)
    results = validate_temp_registry(tmp_path, records, schema)
    assert not error_messages(results)
    parsed, _, errors = cli.load_registry_records(records)
    assert not errors
    assert "container_participation" not in parsed["svc-example"]


def test_valid_active_container_identity_passes(tmp_path):
    records, schema = create_registry(tmp_path, active_identity())
    assert not error_messages(validate_temp_registry(tmp_path, records, schema))


@pytest.mark.parametrize(
    "participation_body",
    [
        """
container_identity_contract_version: 1.0
container_participation: intentionally_inactive
health_check_requirement: required
container_identity_evidence:
  - docs/evidence.md
participation_reason: approved_maintenance_or_shutdown
""",
        """
container_identity_contract_version: 1.0
container_participation: excluded
container_identity_evidence:
  - docs/evidence.md
participation_reason: unsupported_identity_model
participation_review_reference: docs/governance/approval-authority.md
participation_review_expires_at: 2027-01-01T00:00:00Z
""",
    ],
)
def test_valid_inactive_and_excluded_contracts_pass(tmp_path, participation_body):
    records, schema = create_registry(tmp_path)
    target = records / "services" / "example.yaml"
    target.write_text(target.read_text(encoding="utf-8") + participation_body, encoding="utf-8")
    assert not error_messages(validate_temp_registry(tmp_path, records, schema))


def test_participation_reason_and_review_expiration_fail_closed(tmp_path):
    body = active_identity(
        "participation_reason: guessed_reason\n"
        "participation_review_expires_at: 2027-01-01T00:00:00Z\n"
    )
    records, schema = create_registry(tmp_path, body)
    messages = error_messages(validate_temp_registry(tmp_path, records, schema))
    assert any("Participation reason is unsupported" in message for message in messages)
    assert any("requires a governed review reference" in message for message in messages)


@pytest.mark.parametrize(
    ("removed", "expected"),
    [
        ("container_host_reference: host-home\n", "missing required fields: container_host_reference"),
        ("compose_project: platform\n", "missing required fields: compose_project"),
        ("compose_service: example\n", "missing required fields: compose_service"),
        ("health_check_requirement: required\n", "missing required fields: health_check_requirement"),
        ("container_health_policy_reference: docs/policies/container-health.json\n", "missing required fields: container_health_policy_reference"),
    ],
)
def test_active_identity_requires_complete_contract(tmp_path, removed, expected):
    records, schema = create_registry(tmp_path, active_identity().replace(removed, ""))
    assert any(expected in message for message in error_messages(validate_temp_registry(tmp_path, records, schema)))


def test_container_host_must_resolve_and_match_dependency(tmp_path):
    records, schema = create_registry(tmp_path, active_identity().replace("container_host_reference: host-home", "container_host_reference: host-missing"))
    messages = error_messages(validate_temp_registry(tmp_path, records, schema))
    assert any("does not resolve to a host" in message for message in messages)
    assert any("must appear in host_dependencies" in message for message in messages)


def test_unknown_fields_and_future_contract_versions_fail_closed(tmp_path):
    body = active_identity("future_container_field: unsafe\n").replace("container_identity_contract_version: 1.0", "container_identity_contract_version: 2.0")
    records, schema = create_registry(tmp_path, body)
    messages = error_messages(validate_temp_registry(tmp_path, records, schema))
    assert any("Unknown Registry fields: future_container_field" in message for message in messages)
    assert any("contract version must be 1.0" in message for message in messages)


def test_future_registry_schema_version_fails_closed(tmp_path):
    records, schema = create_registry(tmp_path)
    schema.write_text(schema.read_text(encoding="utf-8").replace("schema_version: 1.1", "schema_version: 1.2"), encoding="utf-8")
    assert any("Unsupported Registry schema version: 1.2" in message for message in error_messages(validate_temp_registry(tmp_path, records, schema)))


def test_provider_runtime_and_operational_health_fields_cannot_be_declared_identity(tmp_path):
    records, schema = create_registry(tmp_path, active_identity("provider_labels: subject=svc-example\nruntime_container_id: abc123\ncontainer_health_status: healthy\n"))
    messages = error_messages(validate_temp_registry(tmp_path, records, schema))
    assert any("container_health_status, provider_labels, runtime_container_id" in message for message in messages)


def test_not_applicable_rejects_container_and_health_fields(tmp_path):
    body = active_identity().replace("container_participation: active", "container_participation: not_applicable")
    records, schema = create_registry(tmp_path, body)
    assert any("Not-applicable identity contains prohibited fields" in message for message in error_messages(validate_temp_registry(tmp_path, records, schema)))


def test_compose_tuple_and_runtime_name_are_unique_per_host(tmp_path):
    records, schema = create_registry(tmp_path, active_identity())
    duplicate = active_identity().replace("svc-example", "svc-second").replace("name: Example", "name: Second")
    write_record(tmp_path, "services/second.yaml", duplicate)
    messages = error_messages(validate_temp_registry(tmp_path, records, schema))
    assert any("Compose identity tuple duplicates subject" in message for message in messages)
    assert any("Governed runtime name duplicates subject" in message for message in messages)


def test_same_compose_service_on_different_host_is_allowed(tmp_path):
    records, schema = create_registry(tmp_path, active_identity())
    host = (records / "hosts" / "home.yaml").read_text(encoding="utf-8").replace("host-home", "host-second").replace("name: Host", "name: Second Host")
    write_record(tmp_path, "hosts/second.yaml", host)
    second = active_identity().replace("svc-example", "svc-second").replace("name: Example", "name: Second").replace("host-home", "host-second").replace("example-runtime", "second-runtime")
    write_record(tmp_path, "services/second.yaml", second)
    assert not error_messages(validate_temp_registry(tmp_path, records, schema))


def current_plan():
    records, paths, errors = cli.load_registry_records()
    assert not errors
    catalog = migration_evidence_catalog_from_json(cli.REGISTRY_MIGRATION_CATALOG.read_text(encoding="utf-8"))
    return build_migration_plan(records, paths, cli.load_registry_schema(), catalog, cli.ROOT)


def test_repository_migration_plan_is_deterministic_complete_and_non_mutating():
    before = {path: path.read_bytes() for path in cli.registry_record_files()}
    first = current_plan()
    second = current_plan()
    after = {path: path.read_bytes() for path in cli.registry_record_files()}
    report = build_migration_report(first)
    assert migration_plan_to_json(first) == migration_plan_to_json(second)
    assert first.plan_id == second.plan_id
    assert report.candidate_count == 39
    assert report.apply_count == 5
    assert report.review_required_count == 16
    assert report.no_change_count == 18
    assert before == after


def test_repository_apply_candidates_separate_mutable_sources_from_supporting_evidence():
    plan = current_plan()
    apply_candidates = [candidate for candidate in plan.candidates if candidate.action.value == "apply"]
    assert len(apply_candidates) == 5
    for candidate in apply_candidates:
        assert candidate.expected_post_sha256 is not None
        assert candidate.expected_post_sha256 != candidate.source_sha256
        assert all(item.reference != candidate.record_reference for item in candidate.evidence)
        assert [item.reference for item in candidate.evidence] == [
            "docs/architecture/Registry_Container_Identity_Foundation_Architecture.md"
        ]


def test_repository_apply_candidate_hashes_match_independently_derived_content():
    plan = current_plan()
    for candidate in plan.candidates:
        source = (cli.ROOT / candidate.record_reference).read_bytes()
        assert hashlib.sha256(source).hexdigest() == candidate.source_sha256
        for evidence in candidate.evidence:
            assert hashlib.sha256((cli.ROOT / evidence.reference).read_bytes()).hexdigest() == evidence.source_sha256
        if candidate.action.value != "apply":
            assert candidate.expected_post_sha256 is None
            continue
        additions = []
        for key, value in candidate.proposed_fields:
            if isinstance(value, str):
                additions.append(f"{key}: {value}")
            elif isinstance(value, bool):
                additions.append(f"{key}: {'true' if value else 'false'}")
            else:
                assert isinstance(value, list) and value
                additions.extend([f"{key}:", *(f"  - {item}" for item in value)])
        expected = source.rstrip(b"\n") + b"\n" + "\n".join(additions).encode("utf-8") + b"\n"
        assert hashlib.sha256(expected).hexdigest() == candidate.expected_post_sha256


def test_non_service_record_domains_are_explicit_deterministic_no_change_candidates():
    plan = current_plan()
    host = next(candidate for candidate in plan.candidates if candidate.subject_id == "host-beelink-mini-pc")
    assert host.classification.value == "not_applicable"
    assert host.action.value == "no_change"
    assert host.proposed_fields == ()
    assert host.unresolved_fields == ()


def test_pihole_remains_unresolved_without_guessed_values():
    plan = current_plan()
    pihole = next(candidate for candidate in plan.candidates if candidate.subject_id == "svc-pihole-dns")
    assert pihole.action.value == "review_required"
    assert dict(pihole.proposed_fields) == {}
    assert pihole.unresolved_fields == (
        "compose_project",
        "compose_service",
        "container_health_policy_reference",
        "health_check_requirement",
    )


def one_subject_catalog() -> dict[str, object]:
    return {
        "model_version": "registry-container-identity-evidence-v1",
        "entries": [
            {
                "subject_id": "svc-example",
                "classification": "confirmed_non_container_service",
                "proposed_fields": {
                    "container_identity_contract_version": "1.0",
                    "container_participation": "not_applicable",
                    "container_identity_evidence": ["docs/evidence.md"],
                    "participation_reason": "logical_or_repository_capability",
                },
                "evidence": [{"reference": "docs/evidence.md", "assertion": "Governed review confirms a logical service."}],
                "unresolved_fields": [],
                "warnings": [],
            }
        ],
    }


def temp_plan(tmp_path: Path, records: Path, schema: Path):
    parsed, paths, errors = cli.load_registry_records(records)
    assert not errors
    return build_migration_plan(parsed, paths, cli.load_registry_schema(schema), one_subject_catalog(), tmp_path)


def approval_payload(plan, **overrides) -> dict[str, object]:
    payload: dict[str, object] = {
        "model_version": APPROVAL_MODEL_VERSION,
        "plan_id": plan.plan_id,
        "schema_version": plan.schema_version,
        "migration_model_version": plan.model_version,
        "approval_status": "approved",
        "approval_scope": REGISTRY_MIGRATION_APPROVAL_SCOPE,
        "approval_timestamp": "2026-07-20T12:00:00-04:00",
        "approval_authority": REGISTRY_MIGRATION_APPROVAL_AUTHORITY,
        "approval_authority_reference": "docs/governance/approval-authority.md",
        "decision_notes": "Approved for the exact repository-only Registry record migration plan.",
    }
    payload.update(overrides)
    return payload


def write_approval(tmp_path: Path, plan, *, name: str = "approval.json", content: bytes | None = None, **overrides) -> tuple[str, bytes]:
    reference = f"registry/migrations/container_identity/approvals/{name}"
    path = tmp_path / reference
    path.parent.mkdir(parents=True, exist_ok=True)
    if content is None:
        content = (json.dumps(approval_payload(plan, **overrides), indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.write_bytes(content)
    return reference, content


def approved_temp_plan(tmp_path: Path, records: Path, schema: Path):
    plan = temp_plan(tmp_path, records, schema)
    reference, content = write_approval(tmp_path, plan)
    return bind_migration_approval(plan, reference, content)


def current_plan_shaped_approved_plan(tmp_path: Path):
    records, schema = create_registry(tmp_path)
    subject_ids = (
        "svc-example",
        "svc-logical-two",
        "svc-logical-three",
        "svc-logical-four",
        "svc-logical-five",
    )
    template = (records / "services" / "example.yaml").read_text(encoding="utf-8")
    for subject_id in subject_ids[1:]:
        write_record(
            tmp_path,
            f"services/{subject_id.removeprefix('svc-')}.yaml",
            template.replace("svc-example", subject_id).replace("name: Example", f"name: {subject_id}"),
        )
    architecture_evidence = tmp_path / "docs" / "architecture" / "non-container-services.md"
    architecture_evidence.parent.mkdir(parents=True)
    architecture_evidence.write_text("# Reviewed Non-Container Services\n", encoding="utf-8")
    entries = []
    for subject_id in subject_ids:
        record_reference = f"registry/records/services/{'example' if subject_id == 'svc-example' else subject_id.removeprefix('svc-')}.yaml"
        entries.append(
            {
                "subject_id": subject_id,
                "classification": "confirmed_non_container_service",
                "proposed_fields": {
                    "container_identity_contract_version": "1.0",
                    "container_participation": "not_applicable",
                    "container_identity_evidence": [record_reference, "docs/architecture/non-container-services.md"],
                    "participation_reason": "logical_or_repository_capability",
                },
                "evidence": [
                    {"reference": record_reference, "assertion": "The source Registry record establishes the logical capability."},
                    {"reference": "docs/architecture/non-container-services.md", "assertion": "Architecture review confirms the non-container classification."},
                ],
                "unresolved_fields": [],
                "warnings": [],
            }
        )
    parsed, paths, errors = cli.load_registry_records(records)
    assert not errors
    plan = build_migration_plan(
        parsed,
        paths,
        cli.load_registry_schema(schema),
        {"model_version": "registry-container-identity-evidence-v1", "entries": entries},
        tmp_path,
    )
    reference, content = write_approval(tmp_path, plan)
    return records, schema, bind_migration_approval(plan, reference, content)


def self_asserted_approval_plan(plan, reference: str, content: bytes):
    return replace(
        plan,
        approval_status=MigrationApprovalStatus.APPROVED,
        approval_reference=reference,
        approval_sha256=hashlib.sha256(content).hexdigest(),
    )


def test_migration_plan_json_is_strict_and_rejects_future_versions(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    assert migration_plan_from_json(migration_plan_to_json(plan)) == plan
    payload = migration_plan_to_dict(plan)
    payload["unexpected"] = True
    with pytest.raises(MigrationDataError, match="unknown fields"):
        migration_plan_from_json(json.dumps(payload))
    payload = migration_plan_to_dict(plan)
    payload["model_version"] = "future"
    with pytest.raises(MigrationDataError, match="unsupported"):
        migration_plan_from_json(json.dumps(payload))


def test_authoritative_migration_json_rejects_duplicate_keys(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    plan_json = migration_plan_to_json(plan).replace(
        '"model_version": "registry-container-identity-migration-v2",',
        '"model_version": "registry-container-identity-migration-v2",\n  "model_version": "registry-container-identity-migration-v2",',
        1,
    )
    with pytest.raises(MigrationDataError, match="duplicate field: model_version"):
        migration_plan_from_json(plan_json)
    approval_json = json.dumps(approval_payload(plan)).replace(
        '"approval_status": "approved"',
        '"approval_status": "approved", "approval_status": "approved"',
        1,
    )
    with pytest.raises(MigrationDataError, match="duplicate field: approval_status"):
        migration_approval_from_json(approval_json)
    catalog_json = cli.REGISTRY_MIGRATION_CATALOG.read_text(encoding="utf-8").replace(
        '"model_version": "registry-container-identity-evidence-v1"',
        '"model_version": "registry-container-identity-evidence-v1", "model_version": "registry-container-identity-evidence-v1"',
        1,
    )
    with pytest.raises(MigrationDataError, match="duplicate field: model_version"):
        migration_evidence_catalog_from_json(catalog_json)
    rollback = execute_migration(approved_temp_plan(tmp_path, records, schema), tmp_path, dry_run=True).rollback_metadata
    rollback_json = rollback_metadata_to_json(rollback).replace(
        '"model_version": "registry-container-identity-rollback-v1",',
        '"model_version": "registry-container-identity-rollback-v1",\n  "model_version": "registry-container-identity-rollback-v1",',
        1,
    )
    with pytest.raises(MigrationDataError, match="duplicate field: model_version"):
        rollback_metadata_from_json(rollback_json)


def test_plan_rejects_obsolete_model_and_invalid_expected_post_hash(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    payload = migration_plan_to_dict(plan)
    payload["model_version"] = "registry-container-identity-migration-v1"
    with pytest.raises(MigrationDataError, match="model version is unsupported"):
        migration_plan_from_json(json.dumps(payload))
    payload = migration_plan_to_dict(plan)
    payload["candidates"][0]["expected_post_sha256"] = "not-a-digest"
    with pytest.raises(MigrationDataError, match="expected_post_sha256"):
        migration_plan_from_json(json.dumps(payload))


def test_plan_rejects_action_and_classification_contradictions(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    payload = migration_plan_to_dict(plan)
    payload["candidates"][0]["action"] = "review_required"
    with pytest.raises(MigrationDataError, match="action does not match"):
        migration_plan_from_json(json.dumps(payload))


def test_planner_rejects_target_record_symlink_as_immutable_supporting_evidence(tmp_path):
    records, schema = create_registry(tmp_path)
    target = records / "services" / "example.yaml"
    alias = tmp_path / "docs" / "target-alias.yaml"
    alias.symlink_to(target)
    catalog = one_subject_catalog()
    catalog["entries"][0]["evidence"] = [
        {"reference": "docs/target-alias.yaml", "assertion": "Alias must not convert mutable source into immutable evidence."}
    ]
    parsed, paths, errors = cli.load_registry_records(records)
    assert not errors
    with pytest.raises(MigrationDataError, match="immutable supporting evidence distinct"):
        build_migration_plan(parsed, paths, cli.load_registry_schema(schema), catalog, tmp_path)


def test_planner_rejects_removed_or_changed_supporting_evidence(tmp_path):
    records, schema = create_registry(tmp_path)
    parsed, paths, errors = cli.load_registry_records(records)
    assert not errors
    catalog = one_subject_catalog()
    catalog["entries"][0]["evidence"] = []
    with pytest.raises(MigrationDataError, match="requires evidence"):
        build_migration_plan(parsed, paths, cli.load_registry_schema(schema), catalog, tmp_path)
    catalog = one_subject_catalog()
    catalog["entries"][0]["evidence"][0]["reference"] = "docs/missing-evidence.md"
    with pytest.raises(MigrationDataError, match="unsafe or missing"):
        build_migration_plan(parsed, paths, cli.load_registry_schema(schema), catalog, tmp_path)


def test_executor_requires_approved_plan_and_explicit_confirmation(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    with pytest.raises(MigrationDataError, match="bound to an approved migration artifact"):
        execute_migration(plan, tmp_path, dry_run=True)
    approved = approved_temp_plan(tmp_path, records, schema)
    with pytest.raises(MigrationDataError, match="explicit confirmation"):
        execute_migration(approved, tmp_path, dry_run=False, rollback_output=tmp_path / "rollback.json")


def test_arbitrary_existing_repository_document_cannot_authorize_migration(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    reference = "docs/governance/approval-authority.md"
    content = (tmp_path / reference).read_bytes()
    asserted = self_asserted_approval_plan(plan, reference, content)
    with pytest.raises(MigrationDataError, match="artifact reference is unsafe"):
        execute_migration(asserted, tmp_path, dry_run=True)


def test_changing_only_serialized_plan_approval_fields_cannot_authorize_execution(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    reference, content = write_approval(tmp_path, plan, content=b"{}\n")
    payload = migration_plan_to_dict(plan)
    payload.update(
        {
            "approval_status": "approved",
            "approval_reference": reference,
            "approval_sha256": hashlib.sha256(content).hexdigest(),
        }
    )
    asserted = migration_plan_from_json(json.dumps(payload))
    with pytest.raises(MigrationDataError, match="missing required fields"):
        execute_migration(asserted, tmp_path, dry_run=True)


def test_missing_approval_artifact_fails_closed(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = approved_temp_plan(tmp_path, records, schema)
    assert plan.approval_reference is not None
    (tmp_path / plan.approval_reference).unlink()
    with pytest.raises(MigrationDataError, match="reference is unsafe or missing"):
        execute_migration(plan, tmp_path, dry_run=True)


def test_malformed_approval_artifact_fails_closed(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    reference, content = write_approval(tmp_path, plan, content=b"not-json\n")
    asserted = self_asserted_approval_plan(plan, reference, content)
    with pytest.raises(MigrationDataError, match="not valid JSON"):
        execute_migration(asserted, tmp_path, dry_run=True)


def test_unknown_approval_fields_fail_closed(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    reference, content = write_approval(tmp_path, plan, unexpected=True)
    asserted = self_asserted_approval_plan(plan, reference, content)
    with pytest.raises(MigrationDataError, match="unknown fields: unexpected"):
        execute_migration(asserted, tmp_path, dry_run=True)


def test_unsupported_approval_model_version_fails_closed(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    reference, content = write_approval(tmp_path, plan, model_version="future-approval-v2")
    asserted = self_asserted_approval_plan(plan, reference, content)
    with pytest.raises(MigrationDataError, match="model version is unsupported"):
        execute_migration(asserted, tmp_path, dry_run=True)


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"plan_id": "sha256:" + "0" * 64}, "does not approve the submitted plan ID"),
        ({"schema_version": "2.0"}, "schema version does not match"),
        ({"migration_model_version": "future-migration-v2"}, "migration model version does not match"),
        ({"approval_scope": "documentation_publication"}, "scope does not permit Registry record migration"),
        ({"approval_status": "pending"}, "does not contain an affirmative approval decision"),
        ({"approval_status": "rejected"}, "does not contain an affirmative approval decision"),
    ],
)
def test_mismatched_or_nonaffirmative_approval_artifact_fails_closed(tmp_path, overrides, expected):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    reference, content = write_approval(tmp_path, plan, **overrides)
    asserted = self_asserted_approval_plan(plan, reference, content)
    with pytest.raises(MigrationDataError, match=expected):
        execute_migration(asserted, tmp_path, dry_run=True)


def test_approval_authority_reference_must_resolve_to_governed_documentation(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    reference, content = write_approval(tmp_path, plan, approval_authority_reference="docs/evidence.md")
    asserted = self_asserted_approval_plan(plan, reference, content)
    with pytest.raises(MigrationDataError, match="authority reference is unsafe"):
        execute_migration(asserted, tmp_path, dry_run=True)


def test_non_gatekeeper_approval_authority_fails_closed(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    reference, content = write_approval(tmp_path, plan, approval_authority="Migration Caller")
    asserted = self_asserted_approval_plan(plan, reference, content)
    with pytest.raises(MigrationDataError, match="authority is not authorized"):
        execute_migration(asserted, tmp_path, dry_run=True)


def test_approval_artifact_drift_after_binding_fails_closed(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = approved_temp_plan(tmp_path, records, schema)
    assert plan.approval_reference is not None
    approval_path = tmp_path / plan.approval_reference
    approval_path.write_text(approval_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(MigrationDataError, match="has drifted"):
        execute_migration(plan, tmp_path, dry_run=True)


def test_executor_dry_run_is_read_only(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = approved_temp_plan(tmp_path, records, schema)
    target = records / "services" / "example.yaml"
    before = target.read_bytes()
    result = execute_migration(plan, tmp_path, dry_run=True)
    assert result.status == "dry_run_complete"
    assert result.changed_record_references == ("registry/records/services/example.yaml",)
    assert target.read_bytes() == before


def test_executor_apply_is_deterministic_and_rollback_restores_exact_file(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = approved_temp_plan(tmp_path, records, schema)
    target = records / "services" / "example.yaml"
    before = target.read_bytes()
    validate = lambda: validate_temp_registry(tmp_path, records, schema)
    rollback_path = tmp_path / "registry" / "migrations" / "rollback.json"
    result = execute_migration(plan, tmp_path, dry_run=False, confirm=True, rollback_output=rollback_path, validate=validate)
    assert result.status == "applied"
    assert rollback_path.is_file()
    assert "container_participation: not_applicable" in target.read_text(encoding="utf-8")
    second = execute_migration(plan, tmp_path, dry_run=False, confirm=True, rollback_output=tmp_path / "registry" / "migrations" / "rollback-second.json", validate=validate)
    assert second.status == "no_change"
    assert not (tmp_path / "registry" / "migrations" / "rollback-second.json").exists()
    rolled_back = rollback_migration(result.rollback_metadata, tmp_path, confirm=True, validate=validate)
    assert rolled_back.status == "rolled_back"
    assert target.read_bytes() == before
    assert rollback_migration(result.rollback_metadata, tmp_path, confirm=True, validate=validate).status == "no_change"


def test_current_plan_shaped_self_evidence_second_execution_is_no_change(tmp_path):
    records, schema, plan = current_plan_shaped_approved_plan(tmp_path)
    validate = lambda: validate_temp_registry(tmp_path, records, schema)
    before = {path: path.read_bytes() for path in sorted(records.rglob("*.yaml"))}
    assert all(
        item.reference != candidate.record_reference
        for candidate in plan.candidates
        if candidate.action.value == "apply"
        for item in candidate.evidence
    )
    first = execute_migration(
        plan,
        tmp_path,
        dry_run=False,
        confirm=True,
        rollback_output=tmp_path / "registry" / "migrations" / "rollback.json",
        validate=validate,
    )
    after_first = {path: path.read_bytes() for path in sorted(records.rglob("*.yaml"))}
    second = execute_migration(
        plan,
        tmp_path,
        dry_run=False,
        confirm=True,
        rollback_output=tmp_path / "registry" / "migrations" / "rollback-second.json",
        validate=validate,
    )
    after_second = {path: path.read_bytes() for path in sorted(records.rglob("*.yaml"))}
    assert first.status == "applied"
    assert second.status == "no_change"
    assert after_second == after_first
    assert not (tmp_path / "registry" / "migrations" / "rollback-second.json").exists()
    rolled_back = rollback_migration(first.rollback_metadata, tmp_path, confirm=True, validate=validate)
    assert rolled_back.status == "rolled_back"
    assert {path: path.read_bytes() for path in sorted(records.rglob("*.yaml"))} == before
    assert rollback_migration(first.rollback_metadata, tmp_path, confirm=True, validate=validate).status == "no_change"


def test_current_plan_shaped_partial_and_unrelated_target_drift_fail_closed(tmp_path):
    records, _schema, plan = current_plan_shaped_approved_plan(tmp_path)
    candidate = next(item for item in plan.candidates if item.action.value == "apply")
    target = tmp_path / candidate.record_reference
    target.write_text(
        target.read_text(encoding="utf-8") + "container_identity_contract_version: 1.0\n",
        encoding="utf-8",
    )
    with pytest.raises(MigrationDataError, match="partially applied or contains unrelated drift"):
        execute_migration(plan, tmp_path, dry_run=True)

    other_root = tmp_path / "unrelated"
    _other_records, _other_schema, other_plan = current_plan_shaped_approved_plan(other_root)
    other_candidate = next(item for item in other_plan.candidates if item.action.value == "apply")
    other_target = other_root / other_candidate.record_reference
    other_target.write_text(other_target.read_text(encoding="utf-8") + "runtime_status: changed\n", encoding="utf-8")
    with pytest.raises(MigrationDataError, match="candidate source is stale"):
        execute_migration(other_plan, other_root, dry_run=True)


def test_current_plan_shaped_external_evidence_and_subject_drift_fail_closed(tmp_path):
    _records, _schema, plan = current_plan_shaped_approved_plan(tmp_path)
    evidence = tmp_path / "docs" / "architecture" / "non-container-services.md"
    evidence.write_text("# Changed Architecture Evidence\n", encoding="utf-8")
    with pytest.raises(MigrationDataError, match="evidence has drifted"):
        execute_migration(plan, tmp_path, dry_run=True)

    other_root = tmp_path / "subject"
    _other_records, _other_schema, other_plan = current_plan_shaped_approved_plan(other_root)
    candidate = next(item for item in other_plan.candidates if item.action.value == "apply")
    target = other_root / candidate.record_reference
    target.write_text(target.read_text(encoding="utf-8").replace(candidate.subject_id, "svc-replaced", 1), encoding="utf-8")
    with pytest.raises(MigrationDataError, match="does not contain subject"):
        execute_migration(other_plan, other_root, dry_run=True)


def test_current_plan_shaped_approval_and_source_drift_fail_closed(tmp_path):
    _records, _schema, plan = current_plan_shaped_approved_plan(tmp_path)
    assert plan.approval_reference is not None
    approval = tmp_path / plan.approval_reference
    approval.write_text(approval.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(MigrationDataError, match="approval artifact has drifted"):
        execute_migration(plan, tmp_path, dry_run=True)

    other_root = tmp_path / "source"
    _other_records, _other_schema, other_plan = current_plan_shaped_approved_plan(other_root)
    candidate = next(item for item in other_plan.candidates if item.action.value == "apply")
    target = other_root / candidate.record_reference
    target.write_text(target.read_text(encoding="utf-8") + "# source drift before application\n", encoding="utf-8")
    with pytest.raises(MigrationDataError, match="candidate source is stale"):
        execute_migration(other_plan, other_root, dry_run=True)


def test_executor_rejects_plan_bound_incorrect_expected_post_state(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    apply_index = next(index for index, item in enumerate(plan.candidates) if item.action.value == "apply")
    candidate = replace(plan.candidates[apply_index], expected_post_sha256="0" * 64)
    candidates = tuple(candidate if index == apply_index else item for index, item in enumerate(plan.candidates))
    incorrect = replace(plan, candidates=candidates, plan_id=_plan_id(plan.schema_version, candidates))
    reference, content = write_approval(tmp_path, incorrect)
    approved = bind_migration_approval(incorrect, reference, content)
    with pytest.raises(MigrationDataError, match="expected post-state hash is invalid"):
        execute_migration(approved, tmp_path, dry_run=True)


def test_migration_plan_is_independent_of_catalog_entry_order():
    records, paths, errors = cli.load_registry_records()
    assert not errors
    catalog = dict(migration_evidence_catalog_from_json(cli.REGISTRY_MIGRATION_CATALOG.read_text(encoding="utf-8")))
    catalog["entries"] = list(reversed(catalog["entries"]))
    reordered = build_migration_plan(records, paths, cli.load_registry_schema(), catalog, cli.ROOT)
    canonical = current_plan()
    assert migration_plan_to_json(reordered) == migration_plan_to_json(canonical)
    assert reordered.plan_id == canonical.plan_id


def test_rollback_metadata_round_trip_is_strict(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = approved_temp_plan(tmp_path, records, schema)
    result = execute_migration(plan, tmp_path, dry_run=True)
    assert rollback_metadata_from_json(rollback_metadata_to_json(result.rollback_metadata)) == result.rollback_metadata
    payload = json.loads(rollback_metadata_to_json(result.rollback_metadata))
    payload["entries"][0]["original_content"] += "# tampered\n"
    with pytest.raises(MigrationDataError, match="does not match"):
        rollback_metadata_from_json(json.dumps(payload))


def test_executor_restores_original_when_post_write_validation_fails(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = approved_temp_plan(tmp_path, records, schema)
    target = records / "services" / "example.yaml"
    before = target.read_bytes()
    rollback_path = tmp_path / "registry" / "migrations" / "rollback.json"
    validate = lambda: [cli.CheckResult("ERROR", "forced validation failure")]
    with pytest.raises(MigrationDataError, match="validation failed"):
        execute_migration(plan, tmp_path, dry_run=False, confirm=True, rollback_output=rollback_path, validate=validate)
    assert target.read_bytes() == before
    assert not rollback_path.exists()


def test_executor_refuses_drifted_evidence(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = approved_temp_plan(tmp_path, records, schema)
    evidence = tmp_path / "docs" / "evidence.md"
    evidence.write_text("# Changed evidence\n", encoding="utf-8")
    with pytest.raises(MigrationDataError, match="evidence has drifted"):
        execute_migration(plan, tmp_path, dry_run=True)


def test_executor_refuses_stale_plan_and_rollback_refuses_drift(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = approved_temp_plan(tmp_path, records, schema)
    target = records / "services" / "example.yaml"
    target.write_text(target.read_text(encoding="utf-8") + "# reviewed drift\n", encoding="utf-8")
    with pytest.raises(MigrationDataError, match="stale"):
        execute_migration(plan, tmp_path, dry_run=True)


def test_rollback_refuses_drift_without_partial_restoration(tmp_path):
    records, schema = create_registry(tmp_path)
    plan = approved_temp_plan(tmp_path, records, schema)
    rollback_path = tmp_path / "registry" / "migrations" / "rollback.json"
    result = execute_migration(plan, tmp_path, dry_run=False, confirm=True, rollback_output=rollback_path)
    target = records / "services" / "example.yaml"
    drifted = target.read_text(encoding="utf-8") + "# reviewed drift\n"
    target.write_text(drifted, encoding="utf-8")
    with pytest.raises(MigrationDataError, match="has drifted"):
        rollback_migration(result.rollback_metadata, tmp_path, confirm=True)
    assert target.read_text(encoding="utf-8") == drifted


def test_registry_cli_reports_schema_plan_review_and_status(capsys):
    assert cli.main(["registry", "schema-version"]) == 0
    assert "schema version: 1.1" in capsys.readouterr().out
    assert cli.main(["registry", "migration", "plan"]) == 0
    plan_output = capsys.readouterr().out
    assert '"approval_status": "pending"' in plan_output
    assert cli.main(["registry", "migration", "review"]) == 0
    assert "No Registry record is modified" in capsys.readouterr().out
    assert cli.main(["registry", "migration", "status"]) == 0
    assert "Candidates: 39" in capsys.readouterr().out


def test_registry_cli_binds_matching_governed_approval_artifact(tmp_path, monkeypatch, capsys):
    records, schema = create_registry(tmp_path)
    plan = temp_plan(tmp_path, records, schema)
    plan_reference = "registry/migrations/container_identity/plan.json"
    plan_path = tmp_path / plan_reference
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(migration_plan_to_json(plan), encoding="utf-8")
    approval_reference, _content = write_approval(tmp_path, plan)
    monkeypatch.setattr(cli, "ROOT", tmp_path)
    assert cli.main(
        ["registry", "migration", "bind-approval", "--plan", plan_reference, "--approval", approval_reference]
    ) == 0
    bound = migration_plan_from_json(capsys.readouterr().out)
    assert bound.approval_status == MigrationApprovalStatus.APPROVED
    assert bound.approval_reference == approval_reference
    assert bound.approval_sha256 is not None


def test_registry_cli_mutation_arguments_fail_closed_without_crashing(capsys):
    assert cli.main(["registry", "migration", "apply", "--plan"]) == 1
    assert "requires one value for --plan" in capsys.readouterr().out
    assert cli.main(["registry", "migration", "apply", "--plan", "plan.json", "--rollback-output", "rollback.json"]) == 1
    assert "exactly one" in capsys.readouterr().out
