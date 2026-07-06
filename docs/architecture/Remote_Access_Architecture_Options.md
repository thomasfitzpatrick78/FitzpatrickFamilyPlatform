# Remote Access Architecture Options

**Document Version:** 1.0

**Status:** Planned

**Milestone:** Milestone 13

---

## Purpose

This document records remote access options for future Platform infrastructure administration.

No remote access service is implemented by PLAT-13.1.

---

## Option Criteria

Future remote access must:

- Use registry records for host and service targeting.
- Preserve explicit operator control.
- Support strong authentication.
- Avoid exposing administrative services directly to the internet.
- Keep Raspberry Pi rollback access independent from future Beelink hosting where practical.

---

## Options

| Option | Fit | Benefits | Risks / Unknowns |
|--------|-----|----------|------------------|
| Local-only SSH | Baseline for current Raspberry Pi access | Simple, already known for `pi@192.168.50.67` | Requires local network presence; not sufficient for offsite support |
| VPN into home network | Strong candidate for future remote administration | Keeps services private; common operational model | Product choice, key custody, and router support TBD |
| Mesh overlay network | Candidate for device-to-device administration | Can reduce router configuration needs | Vendor trust, account model, and recovery access TBD |
| Reverse tunnel / brokered access | Limited candidate | Useful where inbound access is unavailable | Higher safety burden; requires explicit approval before implementation |

---

## Recommendation

Keep local-only SSH as the current baseline. Select a VPN or mesh overlay option only after Beelink and network modernization records move from planned to active and the authentication model is documented.

---

## Non-Goals

This document does not implement VPN, tunnels, remote agents, remote management daemons, firewall changes, or dashboards.

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.0 | Initial remote access architecture options. |
