from pathlib import Path
import shutil

from engineering.platform_eap import cli


def remove_generated_caches():
    for path in cli.ROOT.joinpath("engineering").rglob("__pycache__"):
        shutil.rmtree(path)


def compose_service_block(compose: str, service_name: str) -> str:
    marker = f"  {service_name}:\n"
    start = compose.index(marker)
    next_service = compose.find("\n  ", start + len(marker))
    while next_service != -1 and compose[next_service + 3 : next_service + 4] == " ":
        next_service = compose.find("\n  ", next_service + 1)
    end = next_service if next_service != -1 else compose.find("\nnetworks:", start)
    return compose[start:end]



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
    assert "host_dependencies: host-beelink-mini-pc" in output


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
    assert any("explicitly tracks unknown or TBD fields" in r.message for r in results)


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


def test_plat_13_6_required_governed_artifacts_exist():
    required = [
        "docs/governance/Service_Lifecycle.md",
        "docs/governance/Production_Service_Cutover_Checklist.md",
        "docs/architecture/decisions/ADR-007-Governed-Operations-and-Observability.md",
        "docs/specifications/Platform_Operations_Observability_Specification.md",
        "docs/architecture/Backup_Restore_Operations_Specification.md",
        "docs/architecture/Controlled_Container_Update_Specification.md",
        "docs/operations/Pi-hole_Service_Objectives.md",
        "docs/operations/Incident_Response_Runbooks.md",
    ]
    missing = [path for path in required if not (cli.ROOT / path).is_file()]
    assert not missing


def test_plat_13_6_adr_is_indexed():
    index = (cli.ROOT / "docs/architecture/Architecture_Decision_Log.md").read_text(encoding="utf-8")
    adr = (cli.ROOT / "docs/architecture/decisions/ADR-007-Governed-Operations-and-Observability.md").read_text(encoding="utf-8")
    assert "ADR-007 | Governed Operations and Observability" in index
    assert "Option A" in adr
    assert "Prometheus" in adr
    assert "Grafana" in adr


def test_plat_13_6_registry_represents_active_pihole_on_beelink_and_rollback():
    records, _, errors = cli.load_registry_records()
    assert not errors
    beelink = records["host-beelink-mini-pc"]
    pihole = records["svc-pihole-dns"]
    rollback = records["svc-pihole-raspberry-pi-rollback"]
    assert beelink["lifecycle_status"] == "active"
    assert beelink["ip_address"] == "192.168.50.127"
    assert beelink["mac_address"] == "78:55:36:09:D2:45"
    assert pihole["host_dependencies"] == ["host-beelink-mini-pc"]
    assert "svc-docker-engine" in pihole["service_dependencies"]
    assert pihole["ip_address"] == "192.168.50.127"
    assert rollback["lifecycle_status"] == "replacement"
    assert rollback["ip_address"] == "192.168.50.67"


def test_plat_13_6_planned_observability_registry_records_exist():
    records, _, errors = cli.load_registry_records()
    assert not errors
    required = {
        "svc-prometheus",
        "svc-node-exporter",
        "svc-cadvisor",
        "svc-grafana",
        "svc-platform-backup-recovery",
        "svc-platform-alerting",
        "svc-controlled-container-updates",
    }
    assert required.issubset(records)
    assert all(records[record_id]["record_type"] == "planned_service" for record_id in required)
    assert all(records[record_id]["lifecycle_status"] == "planned" for record_id in required)


def test_plat_13_6_2_metrics_foundation_templates_are_governed():
    required = [
        "platform/compose/monitoring/compose.yaml",
        "platform/compose/monitoring/.env.example",
        "platform/compose/monitoring/prometheus/prometheus.yml",
        "platform/compose/monitoring/README.md",
        "docs/operations/Metrics_Foundation_Runbook.md",
        "docs/operations/Metrics_Foundation_Evidence_Template.md",
    ]
    missing = [path for path in required if not (cli.ROOT / path).is_file()]
    assert not missing
    assert not (cli.ROOT / "platform/compose/monitoring/.env").exists()


def test_plat_13_6_2_metrics_foundation_compose_guardrails():
    compose = (cli.ROOT / "platform/compose/monitoring/compose.yaml").read_text(encoding="utf-8")
    prometheus = compose_service_block(compose, "prometheus")
    node_exporter = compose_service_block(compose, "node-exporter")
    cadvisor = compose_service_block(compose, "cadvisor")
    assert ":latest" not in compose
    assert "prom/prometheus:v2.55.1" in compose
    assert "prom/node-exporter:v1.8.2" in compose
    assert "gcr.io/cadvisor/cadvisor:v0.49.1" in compose
    assert 'ports:\n      - "${MONITORING_BIND_IP:-192.168.50.127}:9090:9090"' in prometheus
    assert "ports:" not in node_exporter
    assert "ports:" not in cadvisor
    assert 'expose:\n      - "9100"' in node_exporter
    assert 'expose:\n      - "8080"' in cadvisor
    assert "network_mode" not in compose
    assert "53:53" not in compose
    assert "${MONITORING_BIND_IP:-192.168.50.127}:9090:9090" in compose
    assert "0.0.0.0:9090:9090" not in compose
    assert "[::]" not in compose
    assert "network_mode: host" not in compose
    assert "9090:9090" in compose
    assert "docker.sock" not in compose
    assert "53:53" not in compose
    assert 'expose:\n      - "9100"' in compose
    assert 'expose:\n      - "8080"' in compose
    assert "privileged: false" in compose
    assert "cap_drop:\n      - ALL" in compose
    assert "user: \"65534:65534\"" in compose
    assert "platform-monitoring" in compose


def test_plat_13_6_2_metrics_foundation_prometheus_targets_are_internal_service_names():
    prometheus = (cli.ROOT / "platform/compose/monitoring/prometheus/prometheus.yml").read_text(encoding="utf-8")
    assert "prometheus:9090" in prometheus
    assert "node-exporter:9100" in prometheus
    assert "cadvisor:8080" in prometheus
    assert "192.168.50.127:9100" not in prometheus
    assert "192.168.50.127:8080" not in prometheus


def test_plat_13_6_2_metrics_foundation_runbook_has_gates_and_scope_boundaries():
    runbook = (cli.ROOT / "docs/operations/Metrics_Foundation_Runbook.md").read_text(encoding="utf-8")
    for gate in range(1, 13):
        assert f"Gate {gate}" in runbook
    assert "Rollback Procedure" in runbook
    assert "Do not deploy Grafana" in runbook
    assert "Do not change Pi-hole configuration" in runbook
    assert "Do not change router DNS" in runbook
    assert "node_filesystem_size_bytes" in runbook
    assert "docker compose up -d --force-recreate --no-deps prometheus" in runbook
    assert "Do not run `docker compose down -v`" in runbook
    assert "Do not run `docker system prune`" in runbook
    assert "This is the required stop point" in runbook


def test_plat_13_6_2_metrics_registry_keeps_lifecycle_planned_but_records_ready_details():
    records, _, errors = cli.load_registry_records()
    assert not errors
    prometheus = records["svc-prometheus"]
    node_exporter = records["svc-node-exporter"]
    cadvisor = records["svc-cadvisor"]
    assert prometheus["lifecycle_status"] == "planned"
    assert node_exporter["lifecycle_status"] == "planned"
    assert cadvisor["lifecycle_status"] == "planned"
    assert prometheus["planned_image"] == "prom/prometheus:v2.55.1"
    assert prometheus["planned_bind_address"] == "192.168.50.127"
    assert prometheus["planned_retention"] == "15d"
    assert prometheus["planned_runtime_uid_gid"] == "65534:65534"
    assert prometheus["planned_storage_mode"] == "0750"
    assert node_exporter["planned_exposure"] == "internal Docker network only; no LAN-published port"
    assert cadvisor["planned_port"] == "TCP 8080 internal Docker network only; not published to host"
    assert "cap_drop ALL" in cadvisor["privilege_summary"]


def test_plat_13_6_cutover_checklist_governs_dhcp_prerequisite():
    checklist = (cli.ROOT / "docs/governance/Production_Service_Cutover_Checklist.md").read_text(encoding="utf-8")
    lifecycle = (cli.ROOT / "docs/governance/Service_Lifecycle.md").read_text(encoding="utf-8")
    assert "DHCP reservation" in checklist
    assert "verified through reboot, lease renewal" in checklist
    assert "stable network identity" in lifecycle


def test_plat_13_6_documents_do_not_commit_secret_assignments():
    suspicious = []
    needles = [
        "PIHOLE_PASSWORD=",
        "GF_SECURITY_ADMIN_PASSWORD=",
        "password:",
        "token:",
        "api_key:",
    ]
    for path in list((cli.ROOT / "docs").rglob("*.md")) + list((cli.ROOT / "registry").rglob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle in text:
                suspicious.append(f"{path.relative_to(cli.ROOT)} contains {needle}")
    assert not suspicious
