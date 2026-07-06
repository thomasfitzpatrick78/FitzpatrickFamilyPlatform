from pathlib import Path
import shutil

from engineering.platform_eap import cli


def remove_generated_caches():
    for path in cli.ROOT.joinpath("engineering").rglob("__pycache__"):
        shutil.rmtree(path)



def test_repository_validation_passes_with_required_structure():
    remove_generated_caches()
    report = cli.repository_validate()
    assert report.status in {"PASS", "PASS WITH WARNINGS"}
    assert not [r for r in report.results if r.severity == "ERROR"]


def test_governance_validation_passes_with_initial_adrs():
    report = cli.governance_validate()
    assert report.status == "PASS"
    messages = [r.message for r in report.results]
    assert "Finance exclusions are governed by product boundary documents" in messages


def test_release_readiness_aggregates_validation():
    remove_generated_caches()
    report = cli.release_readiness()
    assert report.status in {"PASS", "PASS WITH WARNINGS"}
    assert any("Repository validation" in r.message for r in report.results)
    assert any("Governance validation" in r.message for r in report.results)


def test_milestone_closeout_has_required_artifacts():
    remove_generated_caches()
    report = cli.milestone_closeout()
    assert report.status in {"PASS", "PASS WITH WARNINGS"}
    assert not [r for r in report.results if r.severity == "ERROR"]


def test_engineering_metrics_counts_documents_and_adrs():
    report = cli.engineering_metrics()
    assert report.status == "PASS"
    assert any("Markdown documents" in r.message for r in report.results)
    assert any("Architecture decisions" in r.message for r in report.results)


def test_report_writer_creates_markdown_and_json(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "REPORT_ROOT", tmp_path)
    report = cli.engineering_metrics()
    cli.write_report("engineering_metrics", report)
    assert (tmp_path / "engineering_metrics" / "engineering_metrics_report.md").exists()
    assert (tmp_path / "engineering_metrics" / "engineering_metrics_report.json").exists()


def test_cli_capabilities_outputs_registered_capabilities(capsys):
    result = cli.main(["capabilities"])
    output = capsys.readouterr().out
    assert result == 0
    assert "PLAT-EAP-1" in output
    assert "Engineering Metrics" in output
    assert "PLAT-EAP-6" in output
    assert "Infrastructure Registry Validation" in output
    assert "PLAT-EAP-7" in output
    assert "Platform Digital Twin Integrity Validation" in output
    assert "PLAT-EAP-8" in output
    assert "Registry CLI" in output


def test_cli_invalid_command_returns_usage(capsys):
    result = cli.main(["unknown"])
    output = capsys.readouterr().out
    assert result == 2
    assert "Usage:" in output


def test_registry_cli_list_outputs_registry_records(capsys):
    result = cli.main(["registry", "list"])
    output = capsys.readouterr().out
    assert result == 0
    assert "# Infrastructure Registry Records" in output
    assert "host-beelink-mini-pc" in output
    assert "svc-pihole-dns" in output


def test_registry_cli_show_outputs_record_by_id(capsys):
    result = cli.main(["registry", "show", "svc-pihole-dns"])
    output = capsys.readouterr().out
    assert result == 0
    assert "# Registry Record: svc-pihole-dns" in output
    assert "Path: registry/records/services/pihole-dns.yaml" in output
    assert "name: Pi-hole DNS Service" in output
    assert "host_dependencies: host-raspberry-pi-pihole" in output


def test_registry_cli_show_missing_record_returns_error(capsys):
    result = cli.main(["registry", "show", "missing-record"])
    output = capsys.readouterr().out
    assert result == 1
    assert "Registry record not found: missing-record" in output


def test_registry_cli_services_filters_service_records(capsys):
    result = cli.main(["registry", "services"])
    output = capsys.readouterr().out
    assert result == 0
    assert "# Registry Services" in output
    assert "svc-pihole-dns" in output
    assert "svc-home-assistant" in output
    assert "host-beelink-mini-pc" not in output


def test_registry_cli_hosts_filters_host_records(capsys):
    result = cli.main(["registry", "hosts"])
    output = capsys.readouterr().out
    assert result == 0
    assert "# Registry Hosts" in output
    assert "host-beelink-mini-pc" in output
    assert "svc-pihole-dns" not in output


def test_registry_cli_devices_filters_device_records(capsys):
    result = cli.main(["registry", "devices"])
    output = capsys.readouterr().out
    assert result == 0
    assert "# Registry Devices" in output
    assert "dev-beelink-mini-pc" in output
    assert "net-asus-mesh-router-primary" in output
    assert "svc-pihole-dns" not in output


def test_registry_cli_validate_reuses_registry_validation(capsys):
    remove_generated_caches()
    result = cli.main(["registry", "validate"])
    output = capsys.readouterr().out
    assert result == 0
    assert "# Registry Validation" in output
    assert "Status: PASS" in output
    assert "Mode: read-only local-file validation" in output
    assert "Platform Digital Twin integrity validation passed" in output


def test_registry_cli_topology_outputs_relationship_summary(capsys):
    result = cli.main(["registry", "topology"])
    output = capsys.readouterr().out
    assert result == 0
    assert "# Registry Topology Summary" in output
    assert "Mode: read-only local-file summary" in output
    assert "svc-pihole-dns" in output
    assert "host_dependencies=host-raspberry-pi-pihole" in output


def test_registry_cli_invalid_usage_returns_usage(capsys):
    result = cli.main(["registry", "show"])
    output = capsys.readouterr().out
    assert result == 2
    assert "Usage: platform-eap registry" in output


def test_registry_cli_is_read_only(capsys):
    target = cli.REGISTRY_RECORDS / "services" / "pihole-dns.yaml"
    before = target.read_text(encoding="utf-8")
    result = cli.main(["registry", "show", "svc-pihole-dns"])
    capsys.readouterr()
    after = target.read_text(encoding="utf-8")
    assert result == 0
    assert after == before



def write_registry_record(base: Path, relative_path: str, content: str) -> None:
    path = base / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def create_minimal_registry(tmp_path: Path) -> tuple[Path, Path]:
    records = tmp_path / "records"
    schema = tmp_path / "schema.yaml"
    schema.write_text("schema_id: test\n", encoding="utf-8")
    write_registry_record(
        records,
        "owners/platform.yaml",
        """
        id: owner-family-platform
        record_type: owner
        name: Platform Owner
        description: Test owner.
        owner: owner-family-platform
        location: loc-home
        lifecycle_status: active
        health_status: unmonitored
        monitoring_ready: false
        dependencies: []
        """,
    )
    write_registry_record(
        records,
        "locations/home.yaml",
        """
        id: loc-home
        record_type: location
        name: Home
        description: Test location.
        owner: owner-family-platform
        location: loc-home
        lifecycle_status: active
        health_status: unmonitored
        monitoring_ready: false
        dependencies: []
        """,
    )
    write_registry_record(
        records,
        "hosts/home-server.yaml",
        """
        id: host-home-server
        record_type: host
        name: Home Server
        description: Test host.
        owner: owner-family-platform
        location: loc-home
        lifecycle_status: planned
        health_status: planned
        monitoring_ready: true
        dependencies: []
        """,
    )
    return records, schema


def test_registry_validation_passes_for_repository_records():
    remove_generated_caches()
    results = cli.validate_registry()
    assert not [r for r in results if r.severity == "ERROR"]
    assert any("Registry validation passed" in r.message for r in results)


def test_repository_validation_includes_registry_validation():
    remove_generated_caches()
    report = cli.repository_validate()
    assert report.status in {"PASS", "PASS WITH WARNINGS"}
    assert any("Registry validation passed" in r.message for r in report.results)


def test_registry_validation_detects_missing_required_field(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    target = records / "hosts/home-server.yaml"
    target.write_text(target.read_text(encoding="utf-8").replace("name: Home Server\n", ""), encoding="utf-8")
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("Missing required registry field: name" in r.message for r in results)


def test_registry_validation_detects_invalid_status_values(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    target = records / "hosts/home-server.yaml"
    target.write_text(target.read_text(encoding="utf-8").replace("lifecycle_status: planned", "lifecycle_status: improvised"), encoding="utf-8")
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("Invalid lifecycle_status" in r.message for r in results)


def test_registry_validation_detects_duplicate_ids(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    write_registry_record(
        records,
        "hosts/duplicate.yaml",
        (records / "hosts/home-server.yaml").read_text(encoding="utf-8"),
    )
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("Duplicate registry id" in r.message for r in results)


def test_registry_validation_detects_missing_dependency_reference(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    target = records / "hosts/home-server.yaml"
    target.write_text(target.read_text(encoding="utf-8").replace("dependencies: []", "dependencies:\n  - missing-record"), encoding="utf-8")
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("Dependency reference not found: missing-record" in r.message for r in results)


def test_registry_validation_rejects_finance_scope_terms(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    target = records / "hosts/home-server.yaml"
    target.write_text(target.read_text(encoding="utf-8").replace("Test host.", "Finance host."), encoding="utf-8")
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("Forbidden finance scope term" in r.message for r in results)



def test_registry_validation_detects_missing_classified_dependency_reference(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    target = records / "hosts/home-server.yaml"
    target.write_text(
        target.read_text(encoding="utf-8") + "network_dependencies:\n  - missing-network\n",
        encoding="utf-8",
    )
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("network_dependencies reference not found: missing-network" in r.message for r in results)


def test_registry_validation_requires_classified_dependency_lists(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    target = records / "hosts/home-server.yaml"
    target.write_text(
        target.read_text(encoding="utf-8") + "power_dependencies: dev-ups\n",
        encoding="utf-8",
    )
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("power_dependencies must be a list" in r.message for r in results)



def test_registry_validation_detects_invalid_classified_dependency_type(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    target = records / "hosts/home-server.yaml"
    target.write_text(
        target.read_text(encoding="utf-8") + "network_dependencies:\n  - host-home-server\n",
        encoding="utf-8",
    )
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("network_dependencies reference has invalid record_type" in r.message for r in results)


def test_registry_validation_requires_active_service_host_relationship(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    write_registry_record(
        records,
        "services/orphan.yaml",
        """
        id: svc-orphan
        record_type: service
        name: Orphan Service
        description: Active service without a host relationship.
        owner: owner-family-platform
        location: loc-home
        lifecycle_status: active
        health_status: unmonitored
        monitoring_ready: false
        dependencies: []
        service_dependencies: []
        """,
    )
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("Active service has no valid host relationship: svc-orphan" in r.message for r in results)


def test_registry_validation_allows_active_service_indirect_host_relationship(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    write_registry_record(
        records,
        "services/base.yaml",
        """
        id: svc-base
        record_type: service
        name: Base Service
        description: Active service hosted on the test host.
        owner: owner-family-platform
        location: loc-home
        lifecycle_status: active
        health_status: unmonitored
        monitoring_ready: false
        dependencies:
          - host-home-server
        host_dependencies:
          - host-home-server
        service_dependencies: []
        """,
    )
    write_registry_record(
        records,
        "services/dependent.yaml",
        """
        id: svc-dependent
        record_type: service
        name: Dependent Service
        description: Active service with indirect host relationship.
        owner: owner-family-platform
        location: loc-home
        lifecycle_status: active
        health_status: unmonitored
        monitoring_ready: false
        dependencies:
          - svc-base
        service_dependencies:
          - svc-base
        """,
    )
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert not [r for r in results if r.severity == "ERROR"]
    assert any("Platform Digital Twin integrity validation passed" in r.message for r in results)


def test_registry_validation_rejects_planned_service_with_invalid_host_target(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    target = records / "hosts/home-server.yaml"
    target.write_text(target.read_text(encoding="utf-8").replace("lifecycle_status: planned", "lifecycle_status: retired"), encoding="utf-8")
    write_registry_record(
        records,
        "planned_services/retired-host-service.yaml",
        """
        id: svc-retired-host
        record_type: planned_service
        name: Retired Host Service
        description: Planned service with invalid host lifecycle.
        owner: owner-family-platform
        location: loc-home
        lifecycle_status: planned
        health_status: planned
        monitoring_ready: false
        dependencies:
          - host-home-server
        host_dependencies:
          - host-home-server
        """,
    )
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("Service host reference is not active or planned: host-home-server" in r.message for r in results)
    assert any("Planned service has no valid planned or active host target: svc-retired-host" in r.message for r in results)


def test_registry_validation_detects_circular_dependencies(tmp_path):
    records, schema = create_minimal_registry(tmp_path)
    write_registry_record(
        records,
        "services/alpha.yaml",
        """
        id: svc-alpha
        record_type: service
        name: Alpha Service
        description: First service in dependency cycle.
        owner: owner-family-platform
        location: loc-home
        lifecycle_status: active
        health_status: unmonitored
        monitoring_ready: false
        dependencies:
          - host-home-server
          - svc-beta
        host_dependencies:
          - host-home-server
        service_dependencies:
          - svc-beta
        """,
    )
    write_registry_record(
        records,
        "services/beta.yaml",
        """
        id: svc-beta
        record_type: service
        name: Beta Service
        description: Second service in dependency cycle.
        owner: owner-family-platform
        location: loc-home
        lifecycle_status: active
        health_status: unmonitored
        monitoring_ready: false
        dependencies:
          - host-home-server
          - svc-alpha
        host_dependencies:
          - host-home-server
        service_dependencies:
          - svc-alpha
        """,
    )
    results = cli.validate_registry(records_root=records, schema_path=schema)
    assert any("Circular registry dependency detected" in r.message for r in results)
