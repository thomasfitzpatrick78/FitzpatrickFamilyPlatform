# Production Service Cutover Checklist

**Document Version:** 1.0

**Status:** Active

**Milestone:** Milestone 13

---

## Purpose

This checklist defines reusable production cutover controls for Platform services.

It is written for careful human execution. It does not authorize live changes by itself.

---

## Checklist

| Step | Check | Required Evidence |
|------|-------|-------------------|
| 1 | Approved design and change scope exist | Requirements, specification, or ADR link |
| 2 | Production owner is named | Owner in registry or runbook |
| 3 | Stable host address is verified | DHCP reservation or equivalent validation |
| 4 | Service inventory is complete | Ports, paths, host, dependencies, credentials model |
| 5 | Configuration backup is complete or explicitly deferred by review | Backup path and timestamp |
| 6 | Rollback host or rollback service is available | Rollback validation note |
| 7 | Isolated deployment is possible where practical | Deployment path and non-production exposure |
| 8 | Configuration parity is checked | Source and target configuration notes |
| 9 | Health validation passes | Container or service health evidence |
| 10 | Direct service validation passes | Direct command or browser check |
| 11 | Canary client validation passes where practical | Named canary device or client check |
| 12 | Management plane is reachable | Admin UI or CLI access check |
| 13 | Production port promotion is approved | Port or binding change evidence |
| 14 | Router or shared dependency changes are approved | Router DNS or shared dependency note |
| 15 | Representative client checks pass | Multiple client validation notes |
| 16 | Observation period is completed | Start/end time and observed behavior |
| 17 | Rollback decision point is reviewed | Continue or rollback decision |
| 18 | Registry records are updated | Registry diff or record links |
| 19 | Documentation is updated | Runbook and service objective links |
| 20 | Closeout evidence is captured | Validation report and summary |

---

## DHCP Reservation Prerequisite

A production host must not be promoted until its DHCP reservation or equivalent stable network identity has been created and verified through reboot, lease renewal, or another approved validation method.

This requirement is explicit because the Beelink previously changed address when another device obtained its former lease.

---

## Stop Conditions

Stop and return to architecture review if:

- The host address is not stable.
- The rollback path is not available.
- The selected service or host is unclear.
- Router DNS or another shared dependency would be changed outside approved scope.
- Validation produces inconsistent results.
- Secrets would need to be pasted into the repository.

---

## Related Documents

- [Platform Service Lifecycle](Service_Lifecycle.md)
- [PLAT-13.6 Operations and Observability Specification](../specifications/Platform_Operations_Observability_Specification.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial reusable production service cutover checklist for PLAT-13.6. |
