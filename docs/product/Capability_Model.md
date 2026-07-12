# Capability Model

**Document Version:** 1.7

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document defines stable portfolio and Platform capability domains.

Capabilities represent stable product domains. Epics evolve beneath capabilities. Features evolve beneath epics.

---

## Capability Hierarchy

### Engineering Organization

**Purpose:** Govern the AI-operated Engineering Organization as the operating capability that creates and evolves the Shared Platform and customer-facing applications.

**Business Objective:** Improve delivery quality, architecture discipline, evidence, safety, and customer-value traceability through measurable organizational capability evolution.

**Child Capabilities:** AI Roles and Responsibilities; Engineering Governance; Architecture Governance; Product and Portfolio Governance; Delivery Automation; Governed Live Execution; Engineering Metrics; Capability Maturity; Knowledge and Evidence Management; Operations Intelligence.

**Milestone 13 Capability:** EO-13.1 formalizes the Engineering Organization as a first-class governed capability, establishes the Engineering Investment Rule, requires Engineering Organization Evolution at milestone closeout, and adds governed role, manifesto, principles, maturity, closeout, and transition artifacts.

### Shared Platform

**Purpose:** Provide the reusable technical foundation, infrastructure, services, observability, registry, and Digital Twin capabilities used by the portfolio.

**Business Objective:** Reduce duplicated technical work while preserving repository boundaries, operational safety, and validated current-state knowledge.

**Child Capabilities:** Infrastructure; Home Automation; Energy Management; AI Services; Shared Services; Family Intelligence.

### Infrastructure

**Purpose:** Support household technical foundations, environments, backup, recovery, and operational reliability.

**Business Objective:** Make future household systems durable and maintainable.

**Initial Epics:** Infrastructure Registry v1.0; household environment inventory; backup and recovery coordination; repository and runtime readiness; operations and observability.

**Milestone 12 Capability:** Infrastructure Registry v1.0 is the first usable Platform capability. It will support physical devices, network devices, hosts, services, planned services, locations, ownership, lifecycle status, health status, dependencies, and future monitoring readiness.

**Milestone 13 Capability:** Platform Operations and Observability establishes governed ownership, service lifecycle, cutover, observability, backup, restore validation, incident response, and controlled update practices for the Beelink-hosted Pi-hole production service and future Platform services. PLAT-13.6.2 has completed the initial Metrics Foundation with Prometheus, Node Exporter, and cAdvisor. PLAT-13.6.3 prepares the governed Grafana Operations Dashboard package, PLAT-13.6.3A corrects Docker 29/containerd container metrics assumptions, and PLAT-13.6.3B prepares a restricted Docker API proxy plus OTel Docker Stats replacement before dashboard closeout.

**Container Metrics Capability:** Docker is the current runtime implementation. Future implementations may include Podman, containerd, Kubernetes, Incus, or LXC. Grafana and customer-facing applications consume governed Container Metrics through Prometheus rather than runtime-specific APIs. Runtime-specific collectors and proxies are replaceable implementation components.

### Home Automation

**Purpose:** Support safe, understandable household automation workflows.

**Business Objective:** Improve household convenience and reliability while preserving explicit family control.

**Initial Epics:** Device inventory; automation planning; operational review.

### Energy Management

**Purpose:** Support household energy tracking, optimization, and planning.

**Business Objective:** Improve visibility into energy use and household efficiency decisions.

**Initial Epics:** Utility data review; energy usage tracking; energy planning.

### AI Services

**Purpose:** Provide governed AI assistance for household operations.

**Business Objective:** Use AI to explain, summarize, and assist without replacing human judgment.

**Initial Epics:** Governed prompt library; AI review workflows; privacy-aware assistant patterns.

### Shared Services

**Purpose:** Provide reusable platform services for non-finance household capabilities.

**Business Objective:** Avoid duplicated platform concerns while preserving simple product boundaries.

**Initial Epics:** Shared configuration; shared reporting; shared validation conventions.

### Family Intelligence

**Purpose:** Help the family understand household patterns and make informed decisions.

**Business Objective:** Turn household data into explainable and actionable context.

**Initial Epics:** Household trend summaries; cross-domain insights; decision-support views.

### Customer-Facing Applications

**Purpose:** Represent user-facing products and experiences that prove customer outcomes.

**Business Objective:** Ensure portfolio planning and milestone closeout remain tied to direct household value.

**Initial Application:** Fitzpatrick Family Financial Assistant is the flagship customer-facing application.

**Planning Boundary:** Detailed FFFA scope remains governed in its own repository or approved cross-repository planning artifacts. This repository records portfolio traceability without inventing application implementation scope.

---

## Explicit Exclusions

Finance, banking, budgeting, transactions, and investments are excluded from this capability model.

---

## Related Documents

- [Product Vision](Product_Vision.md)
- [Product Backlog](Product_Backlog.md)
- [Product Roadmap](Product_Roadmap.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.7 | Added EO-13.1 Engineering Organization and Customer-Facing Applications top-level capabilities plus technology-neutral Container Metrics abstraction. |
| 1.6 | Added PLAT-13.6.3B Docker-container metrics replacement preparation. |
| 1.5 | Added PLAT-13.6.3A Docker-container metrics compatibility correction. |
| 1.4 | Added PLAT-13.6.3 governed Operations Dashboard repository preparation. |
| 1.3 | Recorded PLAT-13.6.2 Metrics Foundation as the first active observability capability slice. |
| 1.2 | Added Milestone 13 Platform Operations and Observability capability scope. |
| 1.1 | Added Infrastructure Registry v1.0 as the first usable Infrastructure capability for Milestone 12. |
| 1.0 | Initial Platform capability model. |
