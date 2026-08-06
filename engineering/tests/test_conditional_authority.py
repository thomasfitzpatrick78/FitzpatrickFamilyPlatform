import copy
import importlib.util
import json
from pathlib import Path
import tomllib

import pytest


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "engineering" / "platform_eap" / "conditional_authority.py"
SPEC = importlib.util.spec_from_file_location("conditional_authority", MODULE_PATH)
assert SPEC and SPEC.loader
conditional_authority = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(conditional_authority)


def valid_bundle():
    return {
        "schema_version": "1.0",
        "bundle_id": "eo-15-2-tier1-test",
        "status": "Accepted",
        "outcome": {
            "plain_language_result": "Validate the exact Phase A target",
            "organizational_or_customer_value": "Reduce Owner orchestration",
            "acceptance_criteria": ["The focused suite passes"],
        },
        "authority": {
            "decision_references": [{
                "artifact": "docs/decisions/accepted.md",
                "sha256": "b" * 64,
                "decision_date": "2099-01-01",
                "approved_effect": "Apply and validate exact local targets",
            }],
            "authority_gained": ["Exact local target application and validation"],
            "authority_not_gained": ["Publication"],
            "fresh_tier_3_approval": False,
            "tier_3_approval_evidence": [],
        },
        "repositories": [{
            "name": "FitzpatrickFamilyPlatform",
            "required_baseline": "a" * 40,
            "branch": "main",
            "tracking_branch": "origin/main",
            "live_remote_equality_required": True,
            "allowed_paths": ["AGENTS.md", "engineering/conditional.py"],
            "excluded_paths": ["reports/private.md"],
        }],
        "tiers": {
            "tier_0_actions": ["read repository evidence"],
            "tier_1_actions": ["apply exact targets", "run isolated validation"],
            "tier_2_actions": [],
            "tier_3_actions": [],
        },
        "publication": {
            "staging_included": False,
            "local_commit_included": False,
            "push_included": False,
            "draft_pull_request_included": False,
            "protected_branch_included": False,
            "merge_included": False,
            "release_included": False,
            "tier_2_recovery": [],
        },
        "ownership": {
            "main_writer": "Codex main task",
            "maximum_concurrent_specialists": 3,
            "specialists": [
                {"role": "governed_explorer", "mode": "read-only", "lane": "authority"},
                {"role": "governed_validator", "mode": "read-only", "lane": "validation"},
                {"role": "governed_reviewer", "mode": "read-only", "lane": "review"},
            ],
            "worktrees": [],
            "branches": [],
            "shared_path_leases": [],
        },
        "validation": {
            "commands": ["python3 -m pytest engineering/tests/test_conditional_authority.py"],
            "working_directories": ["engineering"],
            "expected_results": ["all tests pass"],
            "generated_evidence": ["isolated temporary output"],
        },
        "repair_policy": {
            "maximum_cycles_for_same_failure": 2,
            "repairable_paths": ["AGENTS.md"],
            "invariants": ["No new path", "No weaker validation"],
        },
        "evidence": {
            "per_phase": ["Entry and exit result"],
            "completion": ["Final manifest and exact path audit"],
            "sanitization": [
                "no personal name", "no absolute checkout path", "no credential",
                "no customer or protected value", "no prompt text",
            ],
        },
        "invalidation_triggers": [
            "baseline drift", "ambiguous changes", "new path", "second writer",
            "specialist write", "protected data", "architecture change",
            "unclassified evidence", "third same-failure attempt",
        ],
        "expiry": "2099-12-31T23:59:59Z",
        "completion_condition": "Every acceptance criterion passes and evidence is sealed",
    }


def errors_for(mutator):
    bundle = copy.deepcopy(valid_bundle())
    mutator(bundle)
    return conditional_authority.validate_bundle(bundle)


def test_valid_tier_1_bundle_passes():
    assert conditional_authority.validate_bundle(valid_bundle()) == []


def test_project_agent_configuration_and_namespaced_definitions():
    config = tomllib.loads((ROOT / ".codex/config.toml").read_text(encoding="utf-8"))
    assert config["agents"]["max_concurrent_threads_per_session"] == 3
    expected = {"governed_explorer": "medium", "governed_reviewer": "high", "governed_validator": "high"}
    paths = sorted((ROOT / ".codex/agents").glob("*.toml"))
    assert [path.stem for path in paths] == sorted(expected)
    for path in paths:
        agent = tomllib.loads(path.read_text(encoding="utf-8"))
        assert agent["name"] == path.stem
        assert agent["sandbox_mode"] == "read-only"
        assert agent["model_reasoning_effort"] == expected[path.stem]
        assert "parent turn is not in read-only permission mode" in agent["developer_instructions"]


@pytest.mark.parametrize("field,value", [("bundle_id", ""), ("bundle_id", "REPLACE"), ("status", "Proposed")])
def test_rejects_non_executable_or_placeholder_bundle(field, value):
    assert errors_for(lambda bundle: bundle.__setitem__(field, value))


@pytest.mark.parametrize("value", ["g" * 40, "A" * 40, "a" * 39, 42])
def test_rejects_invalid_commit_hash(value):
    errors = errors_for(lambda bundle: bundle["repositories"][0].__setitem__("required_baseline", value))
    assert any("40 lowercase hex" in error for error in errors)


@pytest.mark.parametrize("value", ["/absolute", "../outside", "docs/*", "docs\\file", "./docs/file"])
def test_rejects_unsafe_paths(value):
    errors = errors_for(lambda bundle: bundle["repositories"][0]["allowed_paths"].__setitem__(0, value))
    assert any("safe repository-relative" in error or "unique valid" in error for error in errors)


def test_repairable_paths_must_be_allowed():
    errors = errors_for(lambda bundle: bundle["repair_policy"].__setitem__("repairable_paths", ["outside.md"]))
    assert any("subset" in error for error in errors)


def test_publication_flags_are_exact_booleans():
    errors = errors_for(lambda bundle: bundle["publication"].__setitem__("push_included", "false"))
    assert any("must be a boolean" in error for error in errors)


def test_publication_flag_requires_matching_tier_action():
    errors = errors_for(lambda bundle: bundle["publication"].__setitem__("local_commit_included", True))
    assert any("create local commit" in error for error in errors)


def test_tier_2_requires_recovery_branch_and_lease():
    def mutate(bundle):
        bundle["tiers"]["tier_2_actions"] = ["push named non-protected branch"]
        bundle["publication"]["push_included"] = True
    errors = errors_for(mutate)
    assert any("tier_2_recovery" in error for error in errors)
    assert any("branches and shared_path_leases" in error for error in errors)


def test_tier_3_boolean_without_digest_evidence_fails():
    def mutate(bundle):
        bundle["tiers"]["tier_3_actions"] = ["publish protected branch"]
        bundle["publication"]["protected_branch_included"] = True
        bundle["authority"]["fresh_tier_3_approval"] = True
    errors = errors_for(mutate)
    assert any("Tier 3 is prohibited" in error for error in errors)


def test_tier_3_remains_prohibited_even_with_claimed_digest_evidence():
    bundle = valid_bundle()
    bundle["tiers"]["tier_3_actions"] = ["publish protected branch"]
    bundle["publication"]["protected_branch_included"] = True
    bundle["authority"]["fresh_tier_3_approval"] = True
    bundle["authority"]["tier_3_approval_evidence"] = [{
        "artifact": "docs/decisions/tier3.md",
        "sha256": "c" * 64,
        "decision_date": "2099-01-01",
        "expiry": "2099-12-31T23:59:59Z",
        "approved_actions": ["publish protected branch"],
    }]
    errors = conditional_authority.validate_bundle(bundle)
    assert any("Tier 3 is prohibited" in error for error in errors)


def test_validation_contract_must_align_one_to_one():
    errors = errors_for(lambda bundle: bundle["validation"].__setitem__("expected_results", []))
    assert any("align one-to-one" in error for error in errors)


def test_generated_evidence_class_is_closed():
    errors = errors_for(lambda bundle: bundle["validation"]["generated_evidence"].__setitem__(0, "unknown"))
    assert any("allowed classification" in error for error in errors)


@pytest.mark.parametrize("role,mode", [("explorer", "read-only"), ("governed_explorer", "workspace-write")])
def test_specialist_contract_fails_closed(role, mode):
    def mutate(bundle):
        bundle["ownership"]["specialists"][0]["role"] = role
        bundle["ownership"]["specialists"][0]["mode"] = mode
    errors = errors_for(mutate)
    assert errors


def test_unknown_nested_field_fails_closed():
    errors = errors_for(lambda bundle: bundle["authority"].__setitem__("unexpected", True))
    assert any("unknown fields" in error for error in errors)


def test_repository_bundle_loader_rejects_absolute_path(tmp_path):
    path = tmp_path / "bundle.json"
    path.write_text(json.dumps(valid_bundle()), encoding="utf-8")
    with pytest.raises(ValueError, match="repository-relative"):
        conditional_authority.load_repository_bundle(str(path), tmp_path)


def test_repository_bundle_loader_rejects_symlink(tmp_path):
    target = tmp_path / "bundle.json"
    target.write_text(json.dumps(valid_bundle()), encoding="utf-8")
    link = tmp_path / "link.json"
    link.symlink_to(target)
    with pytest.raises(ValueError, match="symlink"):
        conditional_authority.load_repository_bundle("link.json", tmp_path)
