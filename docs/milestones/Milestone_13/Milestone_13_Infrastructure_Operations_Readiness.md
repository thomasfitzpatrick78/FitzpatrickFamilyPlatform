# Milestone 13 - Infrastructure Operations Readiness

**Document Version:** 1.8

**Status:** Planned

**Milestone:** Milestone 13

---

## Objective

Prepare the Fitzpatrick Family Platform for managed infrastructure operations while preserving the registry-first Platform Digital Twin architecture established in Milestone 12.

---

## Workstream

| Workstream | Name | Objective |
|------------|------|-----------|
| PLAT-13.1 | Infrastructure Operations Readiness | Define static readiness architecture, options, standards, and checklists for future managed infrastructure operations. |
| PLAT-13.3 | Beelink Bring-up | Define governed Day 0 / Day 1 onboarding instructions for the delivered Beelink Mini S without service migration or production DNS changes. |
| PLAT-13.6 | Platform Operations and Observability | Define governed operations, observability, backup, restore, alerting, and controlled update practices for the active Beelink-hosted Pi-hole platform. |
| EO-13.1 | Engineering Organization Governance Evolution | Formalize the AI-operated Engineering Organization as a governed portfolio capability before Milestone 13 closeout. |

---

## Architecture Pattern

Milestone 13 continues the registry-driven Platform lifecycle:

```text
Authoritative Registry -> Validation -> Automation -> Observability -> AI Reasoning
```

PLAT-13.1 and PLAT-13.3 advance the first two stages only. They may prepare future automation and observability, but they do not implement runtime monitoring, polling, discovery, deployment automation, remote management, or dashboards.

---

## Scope

PLAT-13.1 includes:

- Registry completeness improvements for known and planned infrastructure.
- Explicit `TBD` and unknown field handling.
- Operations readiness architecture.
- Remote access architecture options.
- Local service hosting architecture options.
- Container hosting standards.
- Backup and rollback strategy.
- Pi-hole migration readiness plan.
- Beelink onboarding readiness checklist.
- Network modernization readiness checklist.
- Registry-driven Platform lifecycle pattern documentation.
- Static validation and reporting improvements aligned with Platform EAP.

PLAT-13.3 includes:

- Registry updates for delivered Beelink Mini S hardware facts.
- Registry updates for delivered TP-Link TL-SG108S-M2 switches and CyberPower CP850PFCLCD UPS.
- Governed Day 0 / Day 1 Beelink bring-up instructions.
- Ubuntu Server 24.04 LTS operating baseline approval.
- Factory Windows erase disposition with no Windows image created.
- Registry evidence checkpoints after BIOS verification, Ubuntu installation, networking completion, and SSH verification.
- Explicit rollback and no-impact guidance preserving Raspberry Pi Pi-hole service.
- Validation evidence for documentation and registry changes.

PLAT-13.6 includes these work packages:

| Work Package | Name | Objective | Depends On |
|--------------|------|-----------|------------|
| PLAT-13.6.1 | Operations Baseline and Governance | Capture current Beelink, Docker, and Pi-hole production baseline; establish service lifecycle, cutover, severity, evidence, and ownership practices. | PLAT-13.3 |
| PLAT-13.6.2 | Metrics Foundation | Complete governed Prometheus, Node Exporter, cAdvisor, retention, storage, exposure, validation, persistence, reboot, and Pi-hole non-regression evidence. | PLAT-13.6.1 |
| PLAT-13.6.3 | Operations Dashboard | Prepare repository-managed Grafana provisioning, dashboard definitions, live runbook, evidence template, and dashboard governance without live deployment. | PLAT-13.6.2 |
| PLAT-13.6.3A | Docker 29 Container Metrics Compatibility Correction | Correct cAdvisor/Docker 29 container metrics assumptions, dashboard claims, and replacement metrics planning without live deployment. | PLAT-13.6.3 |
| PLAT-13.6.3B | Governed Docker Container Metrics Replacement | Prepare restricted Docker API proxy, OTel Docker Stats Collector, Prometheus scrape job, dashboard migration strategy, registry records, runbook, evidence, and tests without live deployment. | PLAT-13.6.3A |
| PLAT-13.6.4 | Backup and Recovery v1.0 | Define backup scope, exclusions, checksums, retention, restore validation, and reporting. | PLAT-13.6.1 |
| PLAT-13.6.5 | Alerts and Incident Response | Define alert requirements, incident severity, response, escalation, and evidence. | PLAT-13.6.2; PLAT-13.6.4 |
| PLAT-13.6.6 | Controlled Update Management | Define image version, digest, backup, validation, observation, and rollback policy. | PLAT-13.6.4; PLAT-13.6.5 |
| PLAT-13.6.7 | Application and Organization Integration | Update registry, Digital Twin planning, runbooks, product docs, metrics, and reusable service practices. | PLAT-13.6.1 through PLAT-13.6.6 |

Proposed execution order:

1. PLAT-13.6.1 Operations Baseline and Governance.
2. PLAT-13.6.4 Backup and Recovery v1.0.
3. PLAT-13.6.2 Metrics Foundation.
4. PLAT-13.6.3 Operations Dashboard.
5. PLAT-13.6.5 Alerts and Incident Response.
6. PLAT-13.6.6 Controlled Update Management.
7. PLAT-13.6.7 Application and Organization Integration.

EO-13.1 prepares, but does not complete, Milestone 13 closeout governance for:

1. Production Platform Operations Foundation.
2. Engineering Governance Maturation.
3. AI Engineering Organization Governance.
4. Platform as Reference Implementation.
5. Execution Agent and Operations Analyst roadmap.
6. Engineering Investment Rule.
7. Engineering Organization Evolution.
8. Privileged Infrastructure Integration Standard.
9. Container Metrics abstraction.
10. Transition to coordinated EO, PLAT, and FFFA workstreams.

---

## Non-Goals

PLAT-13.1 does not implement:

- Beelink bring-up.
- Pi-hole migration execution.
- Runtime monitoring.
- Device polling.
- Network discovery.
- Deployment automation.
- Dashboards.
- Remote management implementation.
- Finance functionality.

PLAT-13.3 does not implement:

- Pi-hole migration.
- Router DNS changes.
- Home Assistant, MQTT, Ollama, monitoring, dashboard, or remote management installation.
- Network modernization.
- Docker installation.
- Beelink active lifecycle transition before physical setup and validation.

PLAT-13.6 does not implement beyond the completed PLAT-13.6.2 Metrics Foundation:

- Live Grafana deployment, alerting, backup scripts, restore tests, timers, or controlled update automation.
- Router DNS changes.
- Production DNS changes.
- Raspberry Pi rollback decommissioning.
- Unattended production container updates.
- Internet exposure of monitoring interfaces.

EO-13.1 does not implement:

- Live infrastructure execution.
- Docker, Pi-hole, DNS, router, Prometheus, Grafana, or networking changes.
- PLAT-13.6 closeout.
- Milestone 13 closeout.
- Release, tag, push, deployment, or production lifecycle promotion.

---

## Acceptance Criteria

PLAT-13.1 is ready for architecture review when:

- Registry records represent the known Raspberry Pi Pi-hole baseline.
- Beelink, TP-Link switches, and CyberPower UPS are represented as planned infrastructure.
- Unknown and `TBD` fields are explicit in registry records.
- Operations readiness options and checklists are documented.
- Pi-hole migration readiness is documented without forcing repair or upgrade on the Raspberry Pi.
- Platform EAP reports explicit unknown fields during static registry validation.
- Existing repository validation commands have been attempted and results are recorded.

PLAT-13.3 is ready for architecture review when:

- Delivered hardware facts are recorded in registry records.
- The UPS model is recorded as CyberPower CP850PFCLCD, not CP1000PFCLCD.
- The Beelink Day 0 / Day 1 bring-up guide covers physical inspection, safe first power-on, BIOS inspection, OS approach, hostname, static DHCP reservation, SSH setup, admin user approach, Docker readiness, validation, and rollback/no-impact guidance.
- The guide identifies Ubuntu Server 24.04 LTS as the approved operating system and factory Windows as erased with no Windows image created.
- The guide requires registry evidence capture immediately after BIOS verification, Ubuntu installation, networking completion, and SSH verification.
- The Beelink remains `planned` or pending onboarding until physical setup is completed and verified.
- Validation commands have been attempted and results are recorded.

PLAT-13.6 is ready for Architecture Gatekeeper review when:

- ADR-007 records the approved governed Prometheus observability stack.
- Service lifecycle and production cutover checklist are integrated into governance.
- Present Beelink, Docker, Pi-hole, and Raspberry Pi rollback facts are represented in registry records.
- Prometheus, Node Exporter, and cAdvisor are documented with live PLAT-13.6.2 evidence.
- Grafana dashboard artifacts are prepared for Architecture Gatekeeper review without claiming live implementation.
- PLAT-13.6.3A records the Docker 29/containerd cAdvisor compatibility limitation and keeps dashboard claims accurate.
- PLAT-13.6.3B prepares the replacement source as implementation-ready only; proxy, OTel, Prometheus target, Pi-hole identity, persistence, and reboot evidence remain future live gates.
- Planned backup, restore, alert, and update capabilities remain documented without claiming live implementation.
- Tests and EAP validations have been attempted and results are recorded.

EO-13.1 is ready for Architecture Gatekeeper review when:

- The AI-operated Engineering Organization is represented as a first-class governed capability.
- The three-pillar portfolio model is explicit.
- The Engineering Investment Rule is governed.
- Engineering Organization Evolution is mandatory at closeout.
- AI Role Catalog, Manifesto, Engineering Principles, maturity model, closeout template, and transition template are indexed.
- Product vision, capability model, roadmap, backlog, lifecycle, and Definition of Done are aligned.
- Milestone 14 contains coordinated EO, PLAT, and FFFA planning.
- Existing PLAT-13.6.3A and PLAT-13.6.3B working-tree changes are preserved.
- PLAT-13.6 and Milestone 13 remain open.

---

## Related Documents

- [Infrastructure Operations Readiness](../../architecture/Infrastructure_Operations_Readiness.md)
- [Remote Access Architecture Options](../../architecture/Remote_Access_Architecture_Options.md)
- [Local Service Hosting Architecture Options](../../architecture/Local_Service_Hosting_Architecture_Options.md)
- [Container Hosting Standards](../../architecture/Container_Hosting_Standards.md)
- [Backup and Rollback Strategy](../../architecture/Backup_and_Rollback_Strategy.md)
- [Registry-Driven Platform Lifecycle](../../architecture/Registry_Driven_Platform_Lifecycle.md)
- [Beelink Day 0 / Day 1 Bring-up Guide](../../architecture/Beelink_Onboarding_Readiness_Checklist.md)
- [PLAT-13.6 Operations and Observability Specification](../../specifications/Platform_Operations_Observability_Specification.md)
- [Platform Service Lifecycle](../../governance/Service_Lifecycle.md)
- [Production Service Cutover Checklist](../../governance/Production_Service_Cutover_Checklist.md)
- [Engineering Organization Manifesto](../../engineering-organization/Engineering_Organization_Manifesto.md)
- [AI Role Catalog](../../engineering-organization/AI_Role_Catalog.md)
- [Engineering Principles](../../governance/Engineering_Principles.md)
- [Milestone Closeout Template](../templates/Milestone_Closeout_Template.md)
- [Milestone Transition Package Template](../templates/Milestone_Transition_Package_Template.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.8 | Added EO-13.1 governance evolution, closeout preparation, and Milestone 14 transition alignment while keeping PLAT-13.6 and Milestone 13 open. |
| 1.7 | Added PLAT-13.6.3B governed Docker container metrics replacement preparation. |
| 1.6 | Added PLAT-13.6.3A Docker 29 container metrics compatibility correction scope. |
| 1.5 | Prepared PLAT-13.6.3 Operations Dashboard repository package while preserving Grafana as not deployed. |
| 1.4 | Recorded PLAT-13.6.2 Metrics Foundation live operational closeout while preserving later work packages as planned. |
| 1.3 | Added PLAT-13.6 Platform Operations and Observability work packages, dependencies, non-goals, and review criteria. |
| 1.2 | Applied PLAT-13.3 Architecture Review Board decisions for OS baseline, Windows disposition, registry evidence checkpoints, and Docker deferral. |
| 1.1 | Added PLAT-13.3 Beelink bring-up planning scope and architecture review criteria. |
| 1.0 | Initial PLAT-13.1 Infrastructure Operations Readiness plan. |
