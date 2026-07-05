# Fitzpatrick Family Platform

**Repository Status:** Active

**Initial Baseline:** Milestone 11

**Portfolio:** Fitzpatrick Family Portfolio

---

## Purpose

The Fitzpatrick Family Platform is the governed product repository for non-finance household platform capabilities.

The repository begins with complete product governance, architecture governance, engineering governance, standards, validation automation, release evidence, and milestone planning so Platform feature development can begin from a mature baseline.

---

## Product Scope

The Platform owns the following capability domains:

- Infrastructure
- Home Automation
- Energy Management
- AI Services
- Shared Services
- Family Intelligence

The Platform explicitly excludes:

- Finance
- Banking
- Budgeting
- Transactions
- Investments

Finance remains exclusively owned by the Fitzpatrick Family Financial Assistant repository.

---

## Repository Structure

```text
docs/
  architecture/
    decisions/
  governance/
  milestones/
  portfolio/
  product/
  requirements/
  specifications/
  standards/
engineering/
  platform_eap/
  tests/
reports/
  engineering/
platform-eap
```

---

## Validation

Run the complete repository validation suite from the repository root:

```bash
python3 -m pytest engineering/tests
./platform-eap repository validate
./platform-eap governance validate
./platform-eap release readiness
./platform-eap milestone closeout
./platform-eap engineering metrics
./platform-eap capabilities
```

---

## Authoritative Governance

This repository is authoritative for Fitzpatrick Family Platform product, architecture, engineering, milestone, validation, and release knowledge.

Portfolio relationships are documented under `docs/portfolio/`.
