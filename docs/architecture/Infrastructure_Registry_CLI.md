# Infrastructure Registry CLI

**Document Version:** 1.0

**Status:** Active

**Milestone:** Milestone 12

---

## Purpose

This document defines the read-only Infrastructure Registry CLI introduced in WS-12.7.

The CLI provides the first interactive Platform capability for inspecting the Platform Digital Twin while preserving the Infrastructure Registry as the authoritative source.

---

## Command Boundary

Registry CLI commands are local-file based and read-only.

They inspect YAML registry records under `registry/records/` and reuse Platform EAP registry validation. They do not create, edit, delete, discover, poll, deploy, monitor, or remotely manage infrastructure.

---

## Commands

| Command | Purpose |
|---------|---------|
| `./platform-eap registry list` | List all registry records. |
| `./platform-eap registry show <record-id>` | Show one registry record by ID. |
| `./platform-eap registry services` | List active and planned service records. |
| `./platform-eap registry hosts` | List host records. |
| `./platform-eap registry devices` | List physical and network device records. |
| `./platform-eap registry validate` | Run registry validation and Platform Digital Twin integrity checks. |
| `./platform-eap registry topology` | Summarize classified topology relationships from registry records. |

---

## Output Model

Registry CLI output is deterministic plain text.

List commands print records sorted by record type and ID. `show` prints record fields in sorted key order. `topology` prints only records with classified topology relationships.

---

## Read-Only Guarantees

The Registry CLI does not mutate repository state.

Successful execution does not write registry records, update lifecycle values, change health values, deploy services, run monitoring checks, or create a secondary inventory.

---

## Related Documents

- [ADR-006 - Registry Driven Infrastructure Foundation](decisions/ADR-006-Registry-Driven-Infrastructure-Foundation.md)
- [Infrastructure Registry Architecture](Infrastructure_Registry_Architecture.md)
- [Platform Digital Twin Integrity Model](Platform_Digital_Twin_Integrity_Model.md)
- [Platform Operating Environment](Platform_Operating_Environment.md)
- [Infrastructure Registry v1.0 Specification](../specifications/Infrastructure_Registry_v1.0_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial WS-12.7 read-only Infrastructure Registry CLI documentation. |
