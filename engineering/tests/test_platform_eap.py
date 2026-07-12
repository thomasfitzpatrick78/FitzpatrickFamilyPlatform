import json
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
        "svc-platform-backup-recovery",
        "svc-platform-alerting",
        "svc-controlled-container-updates",
        "svc-docker-container-metrics-exporter",
    }
    assert required.issubset(records)
    assert all(records[record_id]["record_type"] == "planned_service" for record_id in required)
    assert all(records[record_id]["lifecycle_status"] == "planned" for record_id in required)


def test_plat_13_6_2_metrics_foundation_active_registry_records_exist():
    records, _, errors = cli.load_registry_records()
    assert not errors
    prometheus = records["svc-prometheus"]
    node_exporter = records["svc-node-exporter"]
    cadvisor = records["svc-cadvisor"]
    assert prometheus["record_type"] == "service"
    assert node_exporter["record_type"] == "service"
    assert cadvisor["record_type"] == "service"
    assert prometheus["lifecycle_status"] == "active"
    assert node_exporter["lifecycle_status"] == "active"
    assert cadvisor["lifecycle_status"] == "active"
    assert prometheus["health_status"] == "healthy"
    assert node_exporter["health_status"] == "healthy"
    assert cadvisor["health_status"] == "degraded"
    assert prometheus["ip_address"] == "192.168.50.127"
    assert prometheus["port"] == "TCP 9090"
    assert node_exporter["exposure"] == "internal Docker network only; no LAN-published port"
    assert cadvisor["host_published_port"] == "none"
    assert "svc-docker-engine" in prometheus["service_dependencies"]
    assert "host-beelink-mini-pc" in node_exporter["host_dependencies"]
    assert "host-beelink-mini-pc" in cadvisor["host_dependencies"]


def test_plat_13_6_2_metrics_foundation_records_versions_digests_and_evidence():
    records, _, errors = cli.load_registry_records()
    assert not errors
    expected = {
        "svc-prometheus": "prom/prometheus@sha256:2659f4c2ebb718e7695cb9b25ffa7d6be64db013daba13e05c875451cf51b0d3",
        "svc-node-exporter": "prom/node-exporter@sha256:4032c6d5bfd752342c3e631c2f1de93ba6b86c41db6b167b9a35372c139e7706",
        "svc-cadvisor": "gcr.io/cadvisor/cadvisor@sha256:3cde6faf0791ebf7b41d6f8ae7145466fed712ea6f252c935294d2608b1af388",
    }
    for record_id, digest in expected.items():
        record = records[record_id]
        assert record["image_digest"] == digest
        assert record["evidence"] == "docs/operations/Metrics_Foundation_Implementation_Evidence.md"
    evidence = cli.ROOT / "docs/operations/Metrics_Foundation_Implementation_Evidence.md"
    assert evidence.is_file()


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
    assert "docker.sock" not in prometheus
    assert "docker.sock" not in node_exporter
    assert "docker.sock" not in cadvisor
    assert "53:53" not in compose
    assert 'expose:\n      - "9100"' in compose
    assert 'expose:\n      - "8080"' in compose
    assert "privileged: false" in compose
    assert "cap_drop:\n      - ALL" in compose
    assert "user: \"65534:65534\"" in compose
    assert "platform-monitoring" in compose


def test_plat_13_6_3_operations_dashboard_templates_are_governed():
    required = [
        "docs/specifications/Platform_Operations_Dashboard.md",
        "docs/operations/Operations_Dashboard_Runbook.md",
        "docs/operations/Operations_Dashboard_Evidence_Template.md",
        "platform/compose/monitoring/grafana/provisioning/datasources/prometheus.yml",
        "platform/compose/monitoring/grafana/provisioning/dashboards/dashboards.yml",
        "platform/compose/monitoring/grafana/dashboards/platform-host.json",
        "platform/compose/monitoring/grafana/dashboards/docker-containers.json",
        "platform/compose/monitoring/grafana/dashboards/pihole-operations.json",
        "platform/compose/monitoring/grafana/dashboards/metrics-foundation-health.json",
    ]
    missing = [path for path in required if not (cli.ROOT / path).is_file()]
    assert not missing
    assert not (cli.ROOT / "platform/compose/monitoring/.env").exists()
    assert not list((cli.ROOT / "platform/compose/monitoring/grafana/provisioning").rglob(".gitkeep"))


def test_plat_13_6_3_operations_dashboard_compose_guardrails():
    compose = (cli.ROOT / "platform/compose/monitoring/compose.yaml").read_text(encoding="utf-8")
    grafana = compose_service_block(compose, "grafana")
    prometheus = compose_service_block(compose, "prometheus")
    node_exporter = compose_service_block(compose, "node-exporter")
    cadvisor = compose_service_block(compose, "cadvisor")
    assert "grafana/grafana:13.1.0" in grafana
    assert ":latest" not in compose
    assert "grafana/grafana:latest" not in compose
    assert "grafana/grafana:main" not in compose
    assert "grafana/grafana:master" not in compose
    assert "grafana/grafana:edge" not in compose
    assert 'ports:\n      - "${MONITORING_BIND_IP:-192.168.50.127}:3000:3000"' in grafana
    assert "0.0.0.0:3000:3000" not in compose
    assert "[::]" not in compose
    assert "network_mode" not in grafana
    assert "network_mode: host" not in compose
    assert "/platform/data/monitoring/grafana:/var/lib/grafana" in grafana
    assert "user: \"472:472\"" in grafana
    assert "docker.sock" not in grafana
    assert "cap_drop:\n      - ALL" in grafana
    assert "GF_AUTH_ANONYMOUS_ENABLED: \"false\"" in grafana
    assert "GF_USERS_ALLOW_SIGN_UP: \"false\"" in grafana
    assert "GF_SECURITY_ADMIN_PASSWORD" in grafana
    assert "GF_PLUGINS_PREINSTALL_DISABLED: \"true\"" in grafana
    assert "GF_PLUGINS_PREINSTALL_AUTO_UPDATE: \"false\"" in grafana
    assert 'ports:\n      - "${MONITORING_BIND_IP:-192.168.50.127}:9090:9090"' in prometheus
    assert "ports:" not in node_exporter
    assert "ports:" not in cadvisor
    assert "53:53" not in compose
    assert "8080:8080" not in compose
    assert "containerd.sock" not in compose


def test_plat_13_6_3_operations_dashboard_env_example_uses_placeholder_only():
    env_example = (cli.ROOT / "platform/compose/monitoring/.env.example").read_text(encoding="utf-8")
    assert "GRAFANA_ADMIN_PASSWORD=REPLACE_WITH_STRONG_BEELINK_LOCAL_PASSWORD" in env_example
    assert "changeme" not in env_example.lower()
    assert "admin123" not in env_example.lower()
    assert "MONITORING_BIND_IP=192.168.50.127" in env_example


def test_plat_13_6_3_operations_dashboard_provisioning_uses_prometheus_only():
    datasource = (cli.ROOT / "platform/compose/monitoring/grafana/provisioning/datasources/prometheus.yml").read_text(encoding="utf-8")
    dashboards = (cli.ROOT / "platform/compose/monitoring/grafana/provisioning/dashboards/dashboards.yml").read_text(encoding="utf-8")
    assert "name: Prometheus" in datasource
    assert "uid: prometheus" in datasource
    assert "url: http://prometheus:9090" in datasource
    assert "isDefault: true" in datasource
    assert "path: /var/lib/grafana/dashboards" in dashboards
    assert "updateIntervalSeconds: 30" in dashboards
    assert "node-exporter:9100" not in datasource
    assert "cadvisor:8080" not in datasource


def test_plat_13_6_3_operations_dashboard_json_parses_and_references_prometheus():
    dashboard_paths = sorted((cli.ROOT / "platform/compose/monitoring/grafana/dashboards").glob("*.json"))
    assert [path.name for path in dashboard_paths] == [
        "docker-containers.json",
        "metrics-foundation-health.json",
        "pihole-operations.json",
        "platform-host.json",
    ]
    for path in dashboard_paths:
        dashboard = json.loads(path.read_text(encoding="utf-8"))
        assert dashboard["refresh"] == "30s"
        assert dashboard["title"]
        assert dashboard["description"]
        assert dashboard["panels"]
        panel_text = json.dumps(dashboard["panels"])
        assert '"uid": "prometheus"' in panel_text
        assert "node-exporter:9100" not in panel_text
        assert "cadvisor:8080" not in panel_text
    pihole_dashboard = json.loads((cli.ROOT / "platform/compose/monitoring/grafana/dashboards/pihole-operations.json").read_text(encoding="utf-8"))
    pihole_text = json.dumps(pihole_dashboard).lower()
    assert "query count" not in pihole_text
    assert "blocked percentage" not in pihole_text
    assert "domain ranking" not in pihole_text
    assert "unavailable pending a compatible docker-container metrics exporter" in pihole_text


def test_plat_13_6_3a_dashboard_claims_are_not_misleading():
    docker_dashboard = json.loads((cli.ROOT / "platform/compose/monitoring/grafana/dashboards/docker-containers.json").read_text(encoding="utf-8"))
    docker_text = json.dumps(docker_dashboard).lower()
    assert "observed containers" not in docker_text
    assert "host/systemd cgroup series" in docker_text
    assert "this is not a docker container count" in docker_text
    assert "docker-container discovery is currently" in docker_text
    panel_titles = [panel["title"].lower() for panel in docker_dashboard["panels"]]
    assert "cpu by container" not in panel_titles
    assert "memory by container" not in panel_titles
    assert "count(container_last_seen)" in docker_text
    metrics_dashboard = json.loads((cli.ROOT / "platform/compose/monitoring/grafana/dashboards/metrics-foundation-health.json").read_text(encoding="utf-8"))
    metrics_text = json.dumps(metrics_dashboard).lower()
    assert "cadvisor target health" in metrics_text
    assert "does not prove docker-container discovery" in metrics_text


def test_plat_13_6_3a_grafana_registry_state_is_validation_incomplete():
    records, _, errors = cli.load_registry_records()
    assert not errors
    grafana = records["svc-grafana"]
    assert grafana["record_type"] == "service"
    assert grafana["lifecycle_status"] == "active"
    assert grafana["health_status"] == "degraded"
    assert grafana["monitoring_ready"] is False
    assert grafana["image"] == "grafana/grafana:13.1.0"
    assert grafana["endpoint"] == "http://192.168.50.127:3000"
    assert grafana["storage"] == "/platform/data/monitoring/grafana"
    assert grafana["implementation_status"] == "deployed-pending-validation; PLAT-13.6.3 not complete"
    assert "blocked on Docker 29/containerd" in grafana["validation_status"]


def test_plat_13_6_3_runbook_protects_existing_env_and_proves_persistence():
    runbook = (cli.ROOT / "docs/operations/Operations_Dashboard_Runbook.md").read_text(encoding="utf-8")
    assert ".env.backup.$(date +%Y%m%d-%H%M%S)" in runbook
    assert "Extend the existing Beelink-local" in runbook
    assert "MONITORING_BIND_IP=192.168.50.127" in runbook
    assert "PROMETHEUS_RETENTION=15d" in runbook
    assert "GRAFANA_ADMIN_PASSWORD\"{print $1\"=<set>\"}" in runbook
    assert "database-backed preference" in runbook
    assert "docker compose stop grafana && docker compose rm -f grafana && docker compose up -d grafana" in runbook
    assert "Do not run `down -v`" in runbook
    assert "docker system prune" in runbook


def test_plat_13_6_lifecycle_distinguishes_metrics_complete_from_dashboard_ready():
    spec = (cli.ROOT / "docs/specifications/Platform_Operations_Observability_Specification.md").read_text(encoding="utf-8")
    dashboard_contract = (cli.ROOT / "docs/specifications/Platform_Operations_Dashboard.md").read_text(encoding="utf-8")
    assert "PLAT-13.6.2 operational closeout is complete" in spec
    assert "PLAT-13.6.3 prepared the repository-managed Grafana dashboard layer" in spec
    assert "PLAT-13.6.3A Docker 29 Container Metrics Compatibility Correction" in spec
    assert "Lifecycle state | Deployed for validation; PLAT-13.6.3 closeout blocked" in dashboard_contract
    assert "PLAT-13.6.3 persistence and reboot validation remain incomplete" in dashboard_contract


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


def test_plat_13_6_2_metrics_registry_records_active_live_details():
    records, _, errors = cli.load_registry_records()
    assert not errors
    prometheus = records["svc-prometheus"]
    node_exporter = records["svc-node-exporter"]
    cadvisor = records["svc-cadvisor"]
    assert prometheus["lifecycle_status"] == "active"
    assert node_exporter["lifecycle_status"] == "active"
    assert cadvisor["lifecycle_status"] == "active"
    assert prometheus["image"] == "prom/prometheus:v2.55.1"
    assert prometheus["ip_address"] == "192.168.50.127"
    assert prometheus["retention"] == "15d"
    assert prometheus["runtime_uid_gid"] == "65534:65534"
    assert prometheus["storage_mode"] == "0750"
    assert node_exporter["exposure"] == "internal Docker network only; no LAN-published port"
    assert cadvisor["health_status"] == "degraded"
    assert cadvisor["monitoring_ready"] is False
    assert cadvisor["internal_port"] == "TCP 8080"
    assert "Docker-container discovery" in cadvisor["implementation_status"]
    assert "cap_drop ALL" in cadvisor["privilege_summary"]


def test_plat_13_6_3a_compatibility_finding_and_candidate_are_governed():
    assessment = cli.ROOT / "docs/architecture/Docker_29_Container_Metrics_Compatibility_Assessment.md"
    assert assessment.is_file()
    text = assessment.read_text(encoding="utf-8")
    assert "Docker Engine | `29.6.1`" in text
    assert "Driver type | `io.containerd.snapshotter.v1`" in text
    assert "Changing Docker storage backend" in text
    assert "Rejected" in text
    assert "OpenTelemetry Collector" in text
    records, _, errors = cli.load_registry_records()
    assert not errors
    candidate = records["svc-docker-container-metrics-exporter"]
    assert candidate["record_type"] == "planned_service"
    assert candidate["lifecycle_status"] == "planned"
    assert candidate["health_status"] == "planned"
    assert candidate["monitoring_ready"] is False
    assert "not deployed" in candidate["implementation_status"]


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


def test_plat_13_6_3b_compose_adds_restricted_proxy_and_otel_only():
    compose = (cli.ROOT / "platform/compose/monitoring/compose.yaml").read_text(encoding="utf-8")
    proxy = compose_service_block(compose, "docker-api-proxy")
    otel = compose_service_block(compose, "otel-docker-stats")
    grafana = compose_service_block(compose, "grafana")
    prometheus = compose_service_block(compose, "prometheus")
    node_exporter = compose_service_block(compose, "node-exporter")
    cadvisor = compose_service_block(compose, "cadvisor")

    assert "tecnativa/docker-socket-proxy:0.4.2" in proxy
    assert "otel/opentelemetry-collector-contrib:0.156.0" in otel
    assert ":latest" not in compose
    assert "/var/run/docker.sock:/var/run/docker.sock:ro" in proxy
    assert compose.count("docker.sock") == 2
    assert "docker.sock" not in otel
    assert "containerd.sock" not in compose
    assert "ports:" not in proxy
    assert "ports:" not in otel
    assert 'expose:\n      - "2375"' in proxy
    assert 'expose:\n      - "9464"' in otel
    assert '- "13133"' in otel
    assert "network_mode" not in proxy
    assert "network_mode" not in otel
    assert "network_mode: host" not in compose
    assert "privileged: false" in proxy
    assert "privileged: false" in otel
    assert "cap_drop:\n      - ALL" in proxy
    assert "cap_drop:\n      - ALL" in otel
    assert "no-new-privileges:true" in proxy
    assert "no-new-privileges:true" in otel
    assert "restart: unless-stopped" in proxy
    assert "restart: unless-stopped" in otel
    assert "platform-monitoring" in compose
    assert 'ports:\n      - "${MONITORING_BIND_IP:-192.168.50.127}:3000:3000"' in grafana
    assert 'ports:\n      - "${MONITORING_BIND_IP:-192.168.50.127}:9090:9090"' in prometheus
    assert "ports:" not in node_exporter
    assert "ports:" not in cadvisor


def test_plat_13_6_3b_proxy_policy_is_deny_by_default():
    compose = (cli.ROOT / "platform/compose/monitoring/compose.yaml").read_text(encoding="utf-8")
    proxy = compose_service_block(compose, "docker-api-proxy")
    enabled = [
        'CONTAINERS: "1"',
        'INFO: "1"',
        'PING: "1"',
        'VERSION: "1"',
    ]
    disabled = [
        "AUTH", "BUILD", "COMMIT", "CONFIGS", "DISTRIBUTION", "EVENTS",
        "EXEC", "GRPC", "IMAGES", "NETWORKS", "NODES", "PLUGINS",
        "POST", "SECRETS", "SERVICES", "SESSION", "SWARM", "SYSTEM",
        "TASKS", "VOLUMES", "ALLOW_START", "ALLOW_STOP",
        "ALLOW_RESTARTS", "ALLOW_PAUSE", "ALLOW_UNPAUSE",
    ]
    for setting in enabled:
        assert setting in proxy
    for setting in disabled:
        assert f'{setting}: "0"' in proxy
    assert 'POST: "1"' not in proxy


def test_plat_13_6_3b_otel_config_uses_proxy_and_internal_prometheus_only():
    config = (cli.ROOT / "platform/compose/monitoring/otel/config.yaml").read_text(encoding="utf-8")
    assert "docker_stats:" in config
    assert "endpoint: http://docker-api-proxy:2375" in config
    assert "collection_interval: 15s" in config
    assert "env_vars_to_metric_labels" not in config
    assert "container_labels_to_metric_labels:" in config
    assert "com.docker.compose.project: docker_compose_project" in config
    assert "com.docker.compose.service: docker_compose_service" in config
    assert "com.docker.compose.container-number: docker_compose_container_number" in config
    assert "memory_limiter:" in config
    assert "batch:" in config
    assert "prometheus:" in config
    assert "endpoint: 0.0.0.0:9464" in config
    assert "otlp" not in config.lower()
    assert "traces:" not in config
    assert "logs:" not in config


def test_plat_13_6_3b_prometheus_scrapes_otel_and_preserves_existing_jobs():
    prometheus = (cli.ROOT / "platform/compose/monitoring/prometheus/prometheus.yml").read_text(encoding="utf-8")
    assert "job_name: prometheus" in prometheus
    assert "job_name: node-exporter" in prometheus
    assert "job_name: cadvisor" in prometheus
    assert "job_name: otel-docker-stats" in prometheus
    assert "otel-docker-stats:9464" in prometheus
    assert "scrape_interval: 15s" in prometheus
    assert "docker-api-proxy" not in prometheus
    assert "192.168.50.127:9464" not in prometheus


def test_plat_13_6_3b_registry_records_remain_planned_not_active():
    records, _, errors = cli.load_registry_records()
    assert not errors
    proxy = records["svc-docker-api-proxy"]
    otel = records["svc-otel-docker-stats"]
    candidate = records["svc-docker-container-metrics-exporter"]
    cadvisor = records["svc-cadvisor"]
    grafana = records["svc-grafana"]
    assert proxy["record_type"] == "planned_service"
    assert proxy["lifecycle_status"] == "planned"
    assert proxy["health_status"] == "planned"
    assert proxy["monitoring_ready"] is False
    assert proxy["image"] == "tecnativa/docker-socket-proxy:0.4.2"
    assert proxy["host_published_port"] == "none"
    assert "read-only /var/run/docker.sock" in proxy["socket_model"]
    assert "not deployed" in proxy["implementation_status"]
    assert otel["record_type"] == "planned_service"
    assert otel["lifecycle_status"] == "planned"
    assert otel["health_status"] == "planned"
    assert otel["monitoring_ready"] is False
    assert otel["image"] == "otel/opentelemetry-collector-contrib:0.156.0"
    assert otel["host_published_port"] == "none"
    assert "no Docker or containerd socket" in otel["socket_model"]
    assert "not deployed" in otel["implementation_status"]
    assert "svc-docker-api-proxy" in candidate["service_dependencies"]
    assert "svc-otel-docker-stats" in candidate["service_dependencies"]
    assert cadvisor["lifecycle_status"] == "active"
    assert cadvisor["health_status"] == "degraded"
    assert grafana["lifecycle_status"] == "active"
    assert grafana["health_status"] == "degraded"


def test_plat_13_6_3b_dashboards_are_provisional_not_false_complete():
    docker_dashboard = json.loads((cli.ROOT / "platform/compose/monitoring/grafana/dashboards/docker-containers.json").read_text(encoding="utf-8"))
    pihole_dashboard = json.loads((cli.ROOT / "platform/compose/monitoring/grafana/dashboards/pihole-operations.json").read_text(encoding="utf-8"))
    metrics_dashboard = json.loads((cli.ROOT / "platform/compose/monitoring/grafana/dashboards/metrics-foundation-health.json").read_text(encoding="utf-8"))
    all_text = json.dumps([docker_dashboard, pihole_dashboard, metrics_dashboard]).lower()
    assert "up{job=\\\"otel-docker-stats\\\"}" in all_text
    assert "pending live deployment" in all_text
    assert "provisional" in all_text
    assert "metric inventory" in all_text
    assert "host/systemd cgroups" in all_text
    assert "query count" not in all_text
    assert "block-rate summaries" in all_text
    assert "client analytics" not in all_text
    assert "domain rankings" not in all_text


def test_plat_13_6_3b_governance_runbook_and_evidence_exist():
    required = [
        "docs/governance/Privileged_Infrastructure_Integration_Standard.md",
        "docs/operations/Docker_Container_Metrics_Replacement_Runbook.md",
        "docs/operations/Docker_Container_Metrics_Replacement_Evidence_Template.md",
        "platform/compose/monitoring/docker-api-proxy/README.md",
        "platform/compose/monitoring/otel/README.md",
    ]
    missing = [path for path in required if not (cli.ROOT / path).is_file()]
    assert not missing
    standard = (cli.ROOT / "docs/governance/Privileged_Infrastructure_Integration_Standard.md").read_text(encoding="utf-8")
    runbook = (cli.ROOT / "docs/operations/Docker_Container_Metrics_Replacement_Runbook.md").read_text(encoding="utf-8")
    evidence = (cli.ROOT / "docs/operations/Docker_Container_Metrics_Replacement_Evidence_Template.md").read_text(encoding="utf-8")
    assert "Deny API capabilities by default" in standard
    assert "A restricted proxy reduces exposure but does not make privileged socket access risk-free" in standard
    for gate in range(1, 16):
        assert f"Gate {gate}" in runbook
    assert "Do not run `docker compose down -v`" in runbook
    assert "Do not send a mutation request that could alter containers merely to prove denial" in runbook
    assert "Proxy Security Evidence" in evidence
    assert "Metric and Metadata Inventory" in evidence


def read_repo_text(relative_path: str) -> str:
    return (cli.ROOT / relative_path).read_text(encoding="utf-8")


def test_eo_13_1_governed_artifacts_exist_and_are_indexed():
    required = [
        "docs/engineering-organization/Engineering_Organization_Manifesto.md",
        "docs/engineering-organization/AI_Role_Catalog.md",
        "docs/engineering-organization/Engineering_Organization_Capability_Maturity_Model.md",
        "docs/governance/Engineering_Principles.md",
        "docs/milestones/templates/Milestone_Closeout_Template.md",
        "docs/milestones/templates/Milestone_Transition_Package_Template.md",
        "docs/architecture/decisions/ADR-008-AI-Operated-Engineering-Organization-Portfolio-Model.md",
    ]
    missing = [path for path in required if not (cli.ROOT / path).is_file()]
    assert not missing
    index = read_repo_text("docs/engineering-organization/README.md")
    assert "Engineering_Organization_Manifesto.md" in index
    assert "Engineering_Organization_Capability_Maturity_Model.md" in index
    assert "Engineering_Principles.md" in index
    adr_index = read_repo_text("docs/architecture/Architecture_Decision_Log.md")
    assert "ADR-008 | AI-Operated Engineering Organization Portfolio Model" in adr_index


def test_eo_13_1_engineering_investment_rule_is_permanent_governance():
    operating_model = read_repo_text("docs/governance/Permanent_Project_Operating_Model.md")
    definition = read_repo_text("docs/governance/Definition_of_Done.md")
    lifecycle = read_repo_text("docs/governance/Engineering_Lifecycle.md")
    for text in [operating_model, definition, lifecycle]:
        assert "Engineering Investment Rule" in text
        assert "Engineering Organization" in text
        assert "Shared Platform" in text
        assert "customer-facing application" in text.lower()
    assert "Architecture Gatekeeper approval" in operating_model
    assert "Product Strategy Board approval" in operating_model
    assert "formally approved exception" in operating_model


def test_eo_13_1_closeout_requires_three_pillars_and_evolution():
    template = read_repo_text("docs/milestones/templates/Milestone_Closeout_Template.md")
    definition = read_repo_text("docs/governance/Definition_of_Done.md")
    lifecycle = read_repo_text("docs/governance/Engineering_Lifecycle.md")
    for text in [template, definition, lifecycle]:
        assert "Engineering Organization Evolution" in text
        assert "Engineering Organization improvement" in text
        assert "Shared Platform improvement" in text
        assert "Customer-facing application improvement" in text
    required_subsections = [
        "AI roles introduced or refined",
        "Engineering-process improvements",
        "Governance artifacts added or changed",
        "Repeated practices evaluated for promotion",
        "Reusable architecture or delivery patterns",
        "Capability maturity movement",
        "Engineering effectiveness observations",
        "Lessons learned",
        "Implications for the next milestone",
    ]
    for subsection in required_subsections:
        assert subsection in template


def test_eo_13_1_ai_role_catalog_contains_approved_roles_and_boundaries():
    catalog = read_repo_text("docs/engineering-organization/AI_Role_Catalog.md")
    roles = [
        "Chief Architect / Architecture Gatekeeper",
        "Engineering Organization Advisor",
        "Product Strategy Board",
        "Codex Implementation Engineer",
        "Execution Agent",
        "Operations Analyst",
    ]
    for role in roles:
        assert f"### {role}" in catalog
    assert "Architecture decisions | Chief Architect / Architecture Gatekeeper" in catalog
    assert "Product decisions | Product Strategy Board" in catalog
    assert "Repository implementation | Codex Implementation Engineer" in catalog
    assert "Live execution | Execution Agent, when approved" in catalog
    assert "Operational interpretation | Operations Analyst, when approved" in catalog
    assert "Must not act as autonomous architecture authority" in catalog
    assert catalog.count("**Lifecycle State:** Planned") >= 2
    assert catalog.count("**Lifecycle State:** Active") >= 4


def test_eo_13_1_maturity_model_uses_evidence_not_unsupported_scores():
    maturity = read_repo_text("docs/engineering-organization/Engineering_Organization_Capability_Maturity_Model.md")
    for level in ["Level 0", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]:
        assert level in maturity
    for capability in [
        "Architecture governance",
        "Product governance",
        "Repository governance",
        "Delivery automation",
        "AI role coordination",
        "Live execution safety",
        "Observability",
        "Capability planning",
    ]:
        assert capability in maturity
    assert "does not assign maturity scores unless evidence is captured" in maturity
    assert "distinguish current state from planned state" in maturity


def test_eo_13_1_portfolio_model_distinguishes_reference_and_flagship_application():
    sources = [
        read_repo_text("docs/engineering-organization/Engineering_Organization_Manifesto.md"),
        read_repo_text("docs/product/Product_Vision.md"),
        read_repo_text("docs/governance/Product_Portfolio.md"),
        read_repo_text("docs/architecture/decisions/ADR-008-AI-Operated-Engineering-Organization-Portfolio-Model.md"),
    ]
    combined = "\n".join(sources)
    assert "Fitzpatrick Family Platform is the reference implementation" in combined
    assert "Fitzpatrick Family Financial Assistant is the flagship customer-facing application" in combined
    assert "Engineering Organization" in combined
    assert "Shared Platform" in combined
    assert "Customer-Facing Applications" in combined
    assert "first-class governed capability" in combined


def test_eo_13_1_capability_model_contains_three_pillars_and_child_capabilities():
    capability = read_repo_text("docs/product/Capability_Model.md")
    assert "### Engineering Organization" in capability
    assert "### Shared Platform" in capability
    assert "### Customer-Facing Applications" in capability
    for child in [
        "AI Roles and Responsibilities",
        "Engineering Governance",
        "Architecture Governance",
        "Product and Portfolio Governance",
        "Delivery Automation",
        "Governed Live Execution",
        "Engineering Metrics",
        "Capability Maturity",
        "Knowledge and Evidence Management",
        "Operations Intelligence",
    ]:
        assert child in capability


def test_eo_13_1_milestone_14_has_coordinated_planning_streams_only():
    roadmap = read_repo_text("docs/product/Product_Roadmap.md")
    backlog = read_repo_text("docs/product/Product_Backlog.md")
    eo_backlog = read_repo_text("docs/engineering-organization/Engineering_Organization_Backlog.md")
    for text in [roadmap, backlog]:
        assert "EO - Engineering Organization" in roadmap
        assert "PLAT - Shared Platform" in roadmap
        assert "FFFA - Customer-Facing Application" in roadmap
        assert "planned, not approved for implementation" in text.lower()
    for item in ["EO-14.1", "EO-14.2", "EO-14.3", "EO-14.4", "EO-14.5", "EO-14.6", "EO-14.7"]:
        assert item in eo_backlog
    assert "FFFA-PB-001" in backlog
    assert "Existing FFFA backlog and roadmap governance" in backlog


def test_eo_13_1_preserves_open_milestone_and_plat_13_6_state():
    milestone = read_repo_text("docs/milestones/Milestone_13/Milestone_13_Infrastructure_Operations_Readiness.md")
    assert "**Status:** Planned" in milestone
    assert "PLAT-13.6 | Platform Operations and Observability" in milestone
    assert "EO-13.1 | Engineering Organization Governance Evolution" in milestone
    assert "PLAT-13.6 and Milestone 13 remain open" in milestone
    assert "does not implement" in milestone
    assert "Release, tag, push, deployment, or production lifecycle promotion" in milestone


def test_eo_13_1_container_metrics_abstraction_preserves_plat_13_6_3b():
    spec = read_repo_text("docs/specifications/Platform_Operations_Observability_Specification.md")
    assessment = read_repo_text("docs/architecture/Docker_29_Container_Metrics_Compatibility_Assessment.md")
    compose = read_repo_text("platform/compose/monitoring/compose.yaml")
    assert "Container Metrics is the governed capability" in spec
    assert "Docker is the current implementation context" in spec
    assert "Podman, containerd, Kubernetes, Incus, or LXC" in spec
    assert "through Prometheus rather than runtime-specific APIs" in spec
    assert "no live architecture change" in spec
    assert "tecnativa/docker-socket-proxy:0.4.2" in compose
    assert "otel/opentelemetry-collector-contrib:0.156.0" in compose
    assert "replaceable implementation component" in assessment


def test_eo_13_1_repository_only_scope_does_not_add_runtime_artifacts_or_secrets():
    forbidden_paths = [
        "platform/compose/monitoring/.env",
        "platform/compose/monitoring/grafana/grafana.db",
        "platform/compose/monitoring/prometheus/data",
        ".DS_Store",
        ".pytest_cache",
    ]
    for relative_path in forbidden_paths:
        assert not (cli.ROOT / relative_path).exists()
    suspicious = []
    for path in list((cli.ROOT / "docs").rglob("*.md")) + list((cli.ROOT / "registry").rglob("*.yaml")):
        text = path.read_text(encoding="utf-8").lower()
        if "real_password" in text or "private_key" in text or "api_token=" in text:
            suspicious.append(str(path.relative_to(cli.ROOT)))
    assert not suspicious
