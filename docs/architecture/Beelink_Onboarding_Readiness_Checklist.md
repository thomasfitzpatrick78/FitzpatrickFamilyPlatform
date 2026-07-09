# Beelink Day 0 / Day 1 Bring-up Guide

**Document Version:** 2.1

**Status:** Planned

**Milestone:** Milestone 13

**Workstream:** PLAT-13.3 - Beelink Bring-up

---

## Purpose

This guide defines the governed Day 0 / Day 1 bring-up plan for the first managed Platform compute node.

The Beelink Mini S is delivered hardware, but it remains pending onboarding in the Infrastructure Registry until physical setup, OS baseline, network reservation, SSH access, and validation evidence are completed.

The Infrastructure Registry remains authoritative. This guide is an operating procedure derived from registry records, not a second inventory.

---

## Registry Evidence

- Physical device record: `dev-beelink-mini-pc`.
- Host record: `host-beelink-mini-pc`.
- Planned role: Platform Node 001.
- Hostname standard: `platform-node-001`.
- Lifecycle status: `planned`.
- Health status: `planned`.
- Arrival status: delivered; pending physical setup and governed onboarding.
- Planned switch dependency: `net-switch-2-5gbe-1`.
- Power dependency: `dev-ups-battery-backup`.
- Administrative dependency: `dev-toms-macbook-admin`.

Delivered supporting hardware:

- Beelink Mini S, Intel N150, 16GB memory, 512GB storage, 12V / 3A input.
- Two TP-Link TL-SG108S-M2 8-port 2.5G unmanaged switches.
- CyberPower CP850PFCLCD UPS, 850VA / 510W.

---

## Implementation Boundary

PLAT-13.3 is documentation, registry update, and validation work only.

This guide does not approve:

- Pi-hole migration.
- Router DNS changes.
- Home Assistant installation.
- MQTT installation.
- Ollama installation.
- Monitoring or dashboard installation.
- Remote management implementation.
- Network modernization.
- Docker installation.
- Marking the Beelink active before physical setup is completed and verified.

---

## Day 0 - Physical Inspection

1. Confirm the Beelink model label reads Beelink Mini S.
2. Confirm the expected hardware facts: Intel N150 CPU, 16GB memory, 512GB storage, and 12V / 3A power input.
3. Record the serial number in `registry/records/devices/beelink-mini-pc.yaml`.
4. Inspect the chassis, ports, power adapter, and packaging for visible damage.
5. Confirm the Beelink power adapter matches the 12V / 3A input requirement.
6. Confirm the CyberPower UPS model is CP850PFCLCD and capacity is 850VA / 510W.
7. Confirm both TP-Link switches are TL-SG108S-M2 8-port 2.5G unmanaged switches.
8. Do not connect the Beelink to production network equipment until the initial power-on and BIOS inspection path is clear.

Evidence to capture:

- Serial number.
- Physical location.
- Power source.
- Intended Ethernet path.
- Any damaged or missing parts.

---

## Day 0 - Safe First Power-on

1. Connect display, keyboard, and mouse directly to the Beelink.
2. Connect Ethernet only if the OS installation flow requires it; otherwise leave network disconnected for first BIOS inspection.
3. Connect the Beelink to the CyberPower UPS or a known-good surge-protected outlet.
4. Power on the UPS and confirm it reports normal utility power.
5. Connect Beelink power and press the power button.
6. Watch for POST, fan behavior, display output, and unexpected error messages.
7. If the device fails to POST, power it down and leave all lifecycle fields as `planned`.

No-impact rule:

- Do not unplug the Raspberry Pi Pi-hole.
- Do not move router DNS.
- Do not change DHCP settings.
- Do not change switch cabling for active devices.

---

## Day 0 - BIOS Access

1. During boot, press the vendor BIOS setup key shown on screen.
2. If no prompt appears, try common Beelink access keys: `Delete`, `F2`, or `Esc`.
3. Record the BIOS version and boot mode.
4. Do not change settings unless the change is explicitly listed below and reviewed before save.

BIOS settings to inspect:

| Setting | Expected Review | Action |
|---------|-----------------|--------|
| Boot mode | UEFI preferred | Record value; do not change unless OS install requires it. |
| Secure Boot | Determine default state | Record value; decide based on selected OS installer support. |
| Virtualization | Intel virtualization support present | Enable only if OS/runtime plan requires VM support. |
| Wake on LAN | Off unless a future approved management plan requires it | Leave disabled for Day 0 unless already required by reviewed design. |
| Power restore after outage | Review default behavior | Prefer safe/manual restart until UPS behavior is understood. |
| Boot order | Internal storage and installer media order | Change only for OS installation media, then restore expected order. |
| Fan or thermal profile | Confirm default or balanced profile | Record if visible. |

Registry evidence checkpoint:

1. Immediately after BIOS inspection, update the registry evidence with the BIOS version, boot mode, Secure Boot setting, virtualization setting, Wake on LAN setting, power restore setting, and any intentional boot order change.
2. Do not wait until the end of the procedure to capture BIOS evidence.
3. Do not change Beelink lifecycle status during this checkpoint.

---

## Day 1 - OS Decision and Installation Approach

Approved Day 1 operating system:

- Ubuntu Server 24.04 LTS.

Rationale:

- Ubuntu Server 24.04 LTS is a mature stable platform that satisfies current Platform Node 001 requirements.
- The Engineering Organization prefers the most mature stable platform that fully satisfies current requirements.

Factory Windows disposition:

- The factory Windows installation will be erased during Ubuntu Server installation.
- No Windows image will be created.
- This node is being commissioned as Platform Node 001 and Windows is not part of the Platform operating model.

Preferred Day 1 direction:

- Install Ubuntu Server 24.04 LTS for long-lived Platform host use.
- Keep the installation minimal.
- Avoid desktop environment packages unless needed for local recovery.
- Use full-disk installation and erase the factory Windows installation.
- Record the selected OS in `registry/records/hosts/beelink-mini-pc.yaml` after installation.

Decision gates before install:

1. Confirm Ubuntu Server 24.04 LTS supports Intel N150 hardware, wired networking, SSH server, and future Docker readiness.
2. Confirm installation media checksum where practical.
3. Confirm the target disk is the Beelink internal 512GB storage.
4. Confirm no Pi-hole, Home Assistant, MQTT, Ollama, monitoring, dashboard, or remote management service will be installed during OS baseline.
5. Confirm the Raspberry Pi remains the active Pi-hole DNS host.

Installation approach:

1. Create OS installer media from the admin workstation.
2. Boot the Beelink from installer media.
3. Install Ubuntu Server 24.04 LTS to internal storage.
4. Apply only baseline OS security updates.
5. Record OS name, version, kernel if relevant, and install date in the host record or follow-up evidence.
6. Leave service deployment for a later approved workstream.

Registry evidence checkpoint:

1. Immediately after Ubuntu installation and first successful boot, update the registry evidence with OS name, OS version, kernel version, installation date, hostname, CPU, memory, and storage facts.
2. Record the factory Windows disposition as erased with no Windows image created in the host registry evidence.
3. Do not wait until the end of the procedure to capture OS evidence.
4. Do not change Beelink lifecycle status during this checkpoint.

---

## Day 1 - Hostname Standard

The standard hostname for Platform Node 001 is:

```text
platform-node-001
```

Rules:

- Use lowercase letters, numbers, and hyphens.
- Do not reuse Raspberry Pi hostnames or service names.
- Record any deviation in the host registry record before validation.

---

## Day 1 - Static DHCP Reservation Plan

The Beelink should use router-managed static DHCP reservation rather than unmanaged manual IP assignment unless a later network architecture decision changes this standard.

Steps:

1. Boot the installed OS on the local network without changing router DNS.
2. Identify the wired Ethernet MAC address from the OS or router client list.
3. Select an IP address that does not conflict with existing active infrastructure.
4. Create a DHCP reservation for hostname `platform-node-001`.
5. Reboot or renew DHCP lease and confirm the reserved IP is assigned.
6. Record the MAC address and reserved IP in `registry/records/hosts/beelink-mini-pc.yaml`.

Registry evidence checkpoint:

1. Immediately after network onboarding, update the registry evidence with the Ethernet MAC address, reserved IP address, hostname, intended switch/router path, and confirmation that router DNS was not changed.
2. Do not wait until the end of the procedure to capture networking evidence.
3. Do not change Beelink lifecycle status during this checkpoint.

Guardrails:

- Do not change the DHCP server itself unless already active on the router.
- Do not point clients or router DNS to the Beelink.
- Do not move Pi-hole IP `192.168.50.67`.
- Do not treat IP reachability as service readiness.

---

## Day 1 - SSH Setup

SSH is allowed for local-network administration after the OS baseline is complete.

Steps:

1. Install or enable the OpenSSH server from the selected OS package repository.
2. Create or select a non-root administrative account.
3. Add Tom's admin workstation public SSH key to the administrative account.
4. Disable direct root SSH login if the OS permits it.
5. Prefer key-based authentication.
6. Confirm local-network SSH login from Tom's MacBook.
7. Record SSH access status in the host registry record.

Registry evidence checkpoint:

1. Immediately after SSH validation, update the registry evidence with SSH status, admin user approach, key-based access status, root login policy, and confirmation that SSH is local-network only.
2. Do not wait until the end of the procedure to capture SSH evidence.
3. Do not change Beelink lifecycle status during this checkpoint.

Do not expose SSH to the internet. Remote management remains a planned service and is not implemented by this workstream.

---

## Day 1 - Admin User Approach

Use a named non-root administrative account with sudo privileges.

Rules:

- Do not use `root` for routine administration.
- Do not use shared family passwords in repository files.
- Do not commit secrets, SSH private keys, or recovery codes.
- Record the admin username only if it is safe and useful for future operations.
- Keep break-glass recovery local to the device and outside the repository.

---

## Day 1 - Docker Installation Readiness

Docker is explicitly out of scope for this guide.

The procedure stops after the operating baseline has been validated. Docker installation will be performed in a future workstream.

Before Docker installation is approved in a future workstream, confirm:

1. OS name and version are recorded.
2. Hostname is `platform-node-001`.
3. Static DHCP reservation is recorded.
4. SSH local administration is validated.
5. Storage layout and backup target are documented.
6. Pi-hole rollback host remains intact.
7. Container hosting standards have been reviewed.
8. A future service deployment plan identifies exact workloads and rollback criteria.

Stop condition:

- If Docker installation is requested during PLAT-13.3, stop and return to Architecture Review Board review.

---

## Validation Checklist

| Category | Validation Item | Required Evidence |
|----------|-----------------|-------------------|
| Registry | Hardware facts recorded | Updated Beelink, switch, and UPS records |
| Lifecycle | Beelink remains planned or pending onboarding | `lifecycle_status: planned` and onboarding status |
| Power | UPS model corrected to CP850PFCLCD | Updated UPS record |
| BIOS | BIOS settings inspected | Recorded BIOS notes |
| OS | Ubuntu Server 24.04 LTS installed only after Day 0 gates | Host OS field updated when complete |
| Hostname | Hostname set to `platform-node-001` | OS hostname and registry record |
| Network | Static DHCP reservation planned or recorded | MAC and IP fields when known |
| SSH | Local SSH key-based access validated | SSH status field or evidence note |
| Services | No service migration or install performed | Pi-hole remains on Raspberry Pi |
| Docker | Docker not installed | Procedure stops after operating baseline validation |
| Validation | Platform EAP commands pass | Validation reports or command output |

---

## Rollback and No-impact Guidance

Rollback for PLAT-13.3 means returning to the current state where the Beelink is not a production service host.

Safe rollback actions:

- Power down the Beelink.
- Remove only the Beelink network cable if connected.
- Leave Raspberry Pi Pi-hole online and unchanged.
- Leave router DNS and DHCP options unchanged except for a Beelink reservation if one was created.
- Remove or disable only the Beelink DHCP reservation if it causes conflict.
- Keep registry lifecycle status as `planned` until a later validated active transition.

No-impact constraints:

- Existing DNS service must remain on Raspberry Pi.
- No client DNS change may depend on the Beelink.
- No planned service may be installed as part of bring-up.
- No network modernization may be bundled into Beelink onboarding.
- Docker may not be installed as part of PLAT-13.3.

---

## Activation Gate

The Beelink may become active Platform Node 001 only after a future reviewed update confirms:

- Physical inspection completed.
- BIOS baseline recorded.
- OS installed and recorded.
- Hostname set.
- Static DHCP reservation recorded.
- SSH local administration validated.
- Storage and backup approach recorded.
- Docker readiness recorded as a future workstream, with Docker not installed during PLAT-13.3.
- Validation commands pass.
- Architecture review approves lifecycle transition from `planned` to `active`.

---

## Revision History

| Version | Description |
|---------|-------------|
| 2.1 | Applied Architecture Review Board decisions for Ubuntu Server 24.04 LTS, factory Windows erase disposition, milestone-level registry evidence capture, and Docker out-of-scope boundary. |
| 2.0 | Replaced readiness checklist with governed PLAT-13.3 Day 0 / Day 1 Beelink bring-up guide using delivered hardware facts. |
| 1.0 | Initial Beelink onboarding readiness checklist. |
