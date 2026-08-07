# EO-15.2 Clause Disposition Register

**Version:** 1.0
**Status:** Active
**Effective model for new work:** Bounded Outcome Envelope v2

| Prior rule or pattern | Disposition for new work | Effective replacement |
|---|---|---|
| Phase A exact conditional bundle | Historical only | Preserve for already-bound work; use Bounded Outcome Envelope v2 for new work |
| Exact advance file and repair lists | Supersede | Owned roots, excluded roots, conflict checks, and an after-the-fact scope-delta audit |
| Third-attempt Owner escalation | Remove | Two failures trigger internal root-cause reassessment; unchanged retry is prohibited |
| Separate staging, commit, push, fetch, equality, whitespace, cleanup, or derived-hash decisions | Remove | Include them in one accepted outcome and record them as distinct evidence phases |
| Mandatory new Architecture Gatekeeper conversation | Remove | Repository-driven recovery; material architecture changes still stop |
| Exact Markdown hash binding for ordinary governance | Remove | Versioned schemas plus recorded post-change paths and hashes |
| Product Board and Architecture Gatekeeper cards for the same Owner | Consolidate | One plain-language material Owner card with both perspectives |
| Blanket prohibition on routine AI design decisions | Amend | The engineering organization may make routine design choices inside approved architecture |
| Read-only specialists only | Amend | Up to three specialists; at most one writer lane in a dedicated non-overlapping worktree |
| Implementation package required for every change | Amend | Require an envelope; add a work package only for material multi-workstream delivery |
| Initialization, completion, continuity, and goal documents with duplicate state | Consolidate | AuthorityIndex v1 plus DeliveryState v1; keep historical evidence |
| Generated validation reports tracked by default | Remove | Temporary or CI evidence by default; durable snapshots only when governed |
| Prepared Target or Pilot Only documents used as active instructions | Supersede | The Authority Index names the sole active model; historical artifacts are labeled |
| Per-byte downstream adoption approval | Remove | FFFA accepts compatible Platform schema-major-2 updates when Finance invariants pass |
| Passing checks or subagent results treated as authority | Keep | They remain evidence only |
| Repository-first authority and preservation of user changes | Keep | Required initialization and material stop |
| Finance, privacy, customer-data, credential, workbook, and outside-Git controls | Keep | FFFA overlay remains fail closed |
| Separate evidence for implementation, validation, publication, and equality | Keep | Evidence remains separate even when authority is consolidated |
| Merge, release, production, deployment, customer data, destructive action, and live work excluded | Keep | Each requires explicit material authority |

## Supersession Rule

This register changes prospective operating rules only. It does not rewrite historical evidence or silently widen an earlier Phase A package. If an active artifact conflicts with this register, the Authority Index and root instructions control for new work; the conflict must be corrected inside the next accepted bounded outcome.
