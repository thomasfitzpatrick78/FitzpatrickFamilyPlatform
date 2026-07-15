# Customer Environment Cutover Checklist

**Document Version:** 1.0

**Status:** Active

**Owner:** Engineering Organization / Architecture Gatekeeper

**Maintenance Expectation:** Review after each governed customer-environment
cutover and promote reusable findings into Engineering Organization governance
when supported by evidence.

---

# Purpose

Provide a reusable governed checklist for customer-environment cutovers across
customer-facing applications.

This checklist covers customer data stores, customer reports, customer
acceptance workbooks, and future customer-facing applications. It does not
authorize live infrastructure changes, credentials, certificates, customer data
commits, or customer review claims.

---

# Planning

- [ ] Customer environment identified.
- [ ] Source system identified.
- [ ] Data scope approved.
- [ ] Customer-data classification recorded.
- [ ] Owners and approvers identified.
- [ ] Rollback strategy approved.

# Environment Isolation

- [ ] Customer and engineering data stores separated.
- [ ] Test configuration isolated.
- [ ] Development configuration isolated.
- [ ] Customer-path guard implemented.
- [ ] CI cannot access customer data.
- [ ] Synthetic test data verified.

# Backup and Recovery

- [ ] Pre-cutover backup created.
- [ ] Backup checksum verified.
- [ ] Restore process verified.
- [ ] Rollback decision point defined.
- [ ] Original environment preserved.

# Data Migration or Onboarding

- [ ] Source files preserved.
- [ ] Data provenance recorded.
- [ ] Import attribution verified.
- [ ] Counts reconciled.
- [ ] Rejected records explained.
- [ ] Duplicate behavior understood.
- [ ] Sensitive data excluded from Git.

# Validation

- [ ] Account integrity verified.
- [ ] Transaction integrity verified.
- [ ] Reporting boundary verified.
- [ ] Reporting calculations validated.
- [ ] Data-quality limitations recorded.
- [ ] Customer-facing output preflight completed.

# Security and Privacy

- [ ] No credentials committed.
- [ ] No raw customer data committed.
- [ ] No customer database committed.
- [ ] Access restricted.
- [ ] Logs reviewed for sensitive content.
- [ ] Temporary artifacts removed.

# Approval

- [ ] Engineering validation passed.
- [ ] Governance validation passed.
- [ ] Architecture Gatekeeper approval obtained.
- [ ] Customer review authorized.
- [ ] Customer review not claimed before completion.

# Post-Cutover

- [ ] New environment monitored.
- [ ] Rollback window retained.
- [ ] Acceptance evidence recorded.
- [ ] Defects entered into backlog.
- [ ] Old environment retained or retired through a separate approval.
- [ ] Lessons reviewed for governance promotion.

---

# Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial reusable customer environment cutover checklist. |
