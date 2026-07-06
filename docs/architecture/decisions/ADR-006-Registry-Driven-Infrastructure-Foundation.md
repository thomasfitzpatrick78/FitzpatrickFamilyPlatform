# ADR-006 - Registry Driven Infrastructure Foundation

**Status:** Approved

**Date Approved:** July 2026

**Category:** Infrastructure Architecture

**Milestone:** Milestone 12

**Baseline:** Pending

**Implemented:** No

---

## Context

Milestone 11 established the Fitzpatrick Family Platform repository, governance model, ADR framework, and engineering automation foundation.

Milestone 12 is the first Platform feature milestone. The Platform needs an authoritative way to describe household infrastructure assets and services before runtime automation, monitoring, dashboards, or health checks are introduced.

The first usable Platform capability must be understandable to humans, version controlled, easy to validate, and able to evolve toward automation without forcing premature database or service architecture.

---

## Decision

Milestone 12 will establish a Git-native Infrastructure Registry as the authoritative source for Platform infrastructure assets and services.

The registry will use structured YAML or JSON records stored in the repository. Human-readable infrastructure documentation may be generated from, derived from, or synchronized with the registry records.

The Milestone 12 architecture is validation-first. Registry records shall be designed so deterministic validation can confirm required fields, allowed values, references, ownership, lifecycle state, health state, dependencies, and future monitoring readiness.

---

## Scope

Infrastructure Registry v1.0 shall support records for:

- Physical devices
- Network devices
- Hosts
- Services
- Planned services
- Locations
- Ownership
- Lifecycle status
- Health status
- Dependencies
- Future monitoring readiness

Milestone 12 documentation does not authorize runtime feature implementation, monitoring integrations, dashboards, database storage, automation execution, or finance functionality.

---

## Alternatives Considered

### Documentation-First Inventory

A documentation-first inventory would maintain Markdown pages as the primary source of infrastructure truth.

This is easy for humans to read but difficult to validate consistently. It risks divergence between prose, tables, and future automation needs.

### Registry-Driven Inventory

A registry-driven inventory uses structured records as the authoritative source of truth, with human-readable documentation derived from those records.

This option supports Git-native review, deterministic validation, traceability, and future automation without introducing a database too early.

### SQLite-Backed CMDB

A SQLite-backed configuration management database would provide queryability and stronger relational structure.

This is more complex than the current milestone needs and would introduce runtime persistence architecture before the Platform has validated its infrastructure inventory model.

---

## Consequences

### Positive

- Infrastructure knowledge becomes version controlled and reviewable.
- Registry records can be validated deterministically.
- Human-readable documentation can remain aligned with structured records.
- Future health checks, monitoring, dashboards, and automation can build on the registry.
- The repository remains the authoritative system of record for Platform infrastructure knowledge.

### Tradeoffs

- Structured registry records require schema discipline.
- Markdown-only users may need derived documentation for easier reading.
- Query and dashboard capabilities are deferred until the registry model is validated.

---

## Governance Impact

Infrastructure Registry records become governed repository artifacts.

Changes to registry structure, required fields, lifecycle status values, health status values, dependency rules, or monitoring-readiness semantics require architecture or specification review.

Infrastructure Registry v1.0 remains non-finance Platform scope. Finance assets, banking records, budgets, transactions, and investments remain excluded.

---

## Future Extensibility

Future milestones may extend the registry toward:

- Deterministic schema validation.
- Registry-derived Markdown documentation.
- Health checks.
- Monitoring.
- Dashboards.
- Automation readiness.
- Dependency impact analysis.
- Operating environment review.

Those extensions require their own requirements, architecture, specifications, implementation, validation, and release evidence.

---

## Verification Approach

Milestone 12 planning verification shall confirm:

- ADR-006 is indexed.
- Infrastructure Registry v1.0 is represented in the roadmap and backlog.
- Milestone 12 workstreams are defined.
- Architecture documentation reflects Git-native structured registry design.
- No runtime feature implementation has started.
- Finance functionality has not been introduced.

---

## Related Documents

- [Architecture Decision Log](../Architecture_Decision_Log.md)
- [Infrastructure Registry Architecture](../Infrastructure_Registry_Architecture.md)
- [Infrastructure Registry v1.0 Specification](../../specifications/Infrastructure_Registry_v1.0_Specification.md)
- [Milestone 12 Plan](../../milestones/Milestone_12/Milestone_12_Infrastructure_Registry_v1.0.md)
- [Product Roadmap](../../product/Product_Roadmap.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial ADR selecting Registry Driven Infrastructure Foundation for Milestone 12. |
