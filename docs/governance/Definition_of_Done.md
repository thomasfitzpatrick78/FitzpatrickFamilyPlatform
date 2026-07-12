# Definition of Done

**Document Version:** 1.3

**Status:** Active

**Milestone:** Milestone 11

---

## Purpose

This document defines the minimum completion criteria for Platform work.

---

## Completion Criteria

A work item is complete only when applicable criteria are satisfied:

- Product scope confirmed.
- Product backlog reviewed and updated.
- Requirements documented and approved.
- Architecture approved and ADR documented when applicable.
- Specifications updated.
- Implementation completed only within approved scope.
- Tests added or updated when implementation changes behavior.
- Repository validation passes.
- Governance validation passes.
- Release readiness passes for release work.
- Milestone closeout package is ready for milestone completion.
- Engineering metrics generated when applicable.
- Documentation synchronized.
- Evidence reports generated.
- Repository hygiene is clean.
- Production service work includes lifecycle, cutover, backup, rollback, observability, and evidence expectations where applicable.
- Production service promotion requires stable network identity such as a verified DHCP reservation where applicable.
- Privileged infrastructure integrations satisfy the privileged integration standard before lifecycle promotion.
- No finance functionality is introduced.

---

## Milestone Completion

A milestone is complete only when:

- Milestone objectives are satisfied.
- All approved workstreams are closed.
- Validation reports pass.
- Release artifacts are complete.
- Architecture Gatekeeper approval is recorded.
- Engineering Organization improvement is identified and evidenced.
- Shared Platform improvement is identified and evidenced.
- At least one customer-facing application improvement is identified and evidenced.
- Current-state versus planned-state claims are accurate.
- Applicable operational evidence is captured.
- Registry and Digital Twin state is reconciled.
- Reusable practices are evaluated for governance promotion.
- Engineering Organization Evolution is completed.
- Transition implications are recorded.
- Commit, push, and tag are completed when authorized.

The Engineering Investment Rule applies at milestone level. Individual workstreams may be repository-only, platform-only, governance-only, or application-only when milestone-level evidence still demonstrates all three pillars. Exceptions require Architecture Gatekeeper and Product Strategy Board approval, rationale, compensating plan, and visible closeout disclosure.

## Milestone Closeout Required Sections

Every milestone closeout package must include:

- Release summary.
- Engineering Organization improvement.
- Shared Platform improvement.
- Customer-facing application improvement.
- Engineering Organization Evolution.
- Capability maturity observations.
- Architecture and governance decisions.
- Operational evidence.
- Risks and debt.
- Practices promoted into governance.
- Next milestone implications.

---

## Related Documents

- [Engineering Lifecycle](Engineering_Lifecycle.md)
- [Engineering Principles](Engineering_Principles.md)
- [Milestone Closeout Template](../milestones/templates/Milestone_Closeout_Template.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.3 | Added Engineering Investment Rule, milestone closeout evidence, and Engineering Organization Evolution completion criteria. |
| 1.2 | Added privileged infrastructure integration completion expectation. |
| 1.1 | Added production service lifecycle, cutover, and stable network identity completion expectations. |
| 1.0 | Initial Platform Definition of Done. |
