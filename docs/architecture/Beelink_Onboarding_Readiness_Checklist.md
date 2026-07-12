# Beelink Day 0 / Day 1 Bring-up Guide

**Document Version:** 2.3

**Status:** Superseded by PLAT-13.6 production baseline

**Milestone:** Milestone 13

**Workstream:** PLAT-13.3 - Beelink Bring-up

---

## Purpose

This guide defined the governed Day 0 / Day 1 bring-up plan for the first managed Platform compute node.

PLAT-13.6 records that the Beelink has since become the active production Platform host at `192.168.50.127`, hostname `beelink`, running Ubuntu Server 26.04 LTS and Docker-hosted Pi-hole.

Do not execute the Ubuntu installer procedure in this historical guide against the current production host.

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
- Current onboarding status: superseded; production baseline recorded in PLAT-13.6.
- Planned switch dependency: `net-switch-2-5gbe-1`.
- Power dependency: `dev-ups-battery-backup`.
- Administrative dependency: `dev-toms-macbook-admin`.

Delivered supporting hardware:

- Beelink Mini S, Intel N150, 16GB memory, 512GB storage, 12V / 3A input.
- Two TP-Link TL-SG108S-M2 8-port 2.5G unmanaged switches.
- CyberPower CP850PFCLCD UPS, 850VA / 510W.

Verified BIOS evidence:

- BIOS vendor: American Megatrends.
- BIOS version: MS2V001.
- BIOS build date: 2025-04-08.
- Serial number: BN1506GF80211.
- CPU: Intel N150.
- CPU topology: 4 cores / 4 threads.
- Memory: 16384 MB.
- Memory frequency: 3200 MHz.
- Boot Option Filter: UEFI only.
- CSM Support: Enabled.
- Secure Boot: Disabled / Not Active.
- Fast Boot: Disabled.
- Windows Boot Manager is present on the 512GB SSD.

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

## Day 0 - BIOS Evidence and Decision

The Beelink has been powered on and inspected in BIOS.

Verified BIOS facts:

1. BIOS vendor is American Megatrends.
2. BIOS version is MS2V001.
3. BIOS build date is 2025-04-08.
4. Serial number is BN1506GF80211.
5. CPU is Intel N150.
6. CPU topology is 4 cores / 4 threads.
7. Memory is 16384 MB.
8. Memory frequency is 3200 MHz.
9. Boot Option Filter is UEFI only.
10. CSM Support is Enabled.
11. Secure Boot is Disabled / Not Active.
12. Fast Boot is Disabled.
13. Windows Boot Manager is present on the 512GB SSD.

Architecture Review Board BIOS decision:

1. No BIOS configuration changes are required.
2. The current UEFI-only boot configuration is acceptable.
3. CSM remains enabled.
4. Secure Boot remains disabled.
5. Fast Boot remains disabled.
6. Do not change boot mode.
7. Do not change Intel ME settings.
8. Do not change TPM settings.
9. Do not change Wake-on-LAN settings.
10. Do not change power recovery settings.
11. Do not change chipset settings.
12. Do not change CPU settings.
13. Do not change memory settings.
14. Exit BIOS without saving changes unless selecting the USB installer through a one-time boot menu requires a temporary selection.

Registry evidence checkpoint:

1. BIOS evidence has been added to `registry/records/devices/beelink-mini-pc.yaml`.
2. The serial number has been added to `registry/records/devices/beelink-mini-pc.yaml`.
3. Beelink lifecycle status remains `planned`.
4. Beelink onboarding status is BIOS inspected and pending Ubuntu Server installation.

---

## Day 1 - Approved Ubuntu Operating System

Approved operating system:

- Ubuntu Server 24.04 LTS, 64-bit, minimal/server installation, no desktop.

Rationale:

- Ubuntu Server 24.04 LTS is a mature stable platform that satisfies current Platform Node 001 requirements.
- The Engineering Organization prefers the most mature stable platform that fully satisfies current requirements.

Factory Windows disposition:

1. The factory Windows installation will be erased.
2. No Windows image or recovery backup will be created.
3. This is an approved Architecture Review Board decision.
4. The internal 512GB SSD will be dedicated to Ubuntu Server.
5. Windows is not part of the Platform operating model.

Scope boundary for this checkpoint:

1. Create the Ubuntu Server installer USB.
2. Boot the Beelink from the installer USB.
3. Install Ubuntu Server 24.04 LTS.
4. Stop when Ubuntu successfully reaches a login prompt.
5. Do not proceed to DHCP reservation, SSH key hardening, firewall setup, package updates, Docker, or service installation in this checkpoint.

---

## Day 1 - Create Ubuntu Server USB Installer on macOS

Use Tom's MacBook to create the installer.

Requirements:

1. Tom's MacBook.
2. A USB flash drive that can be erased.
3. The official Ubuntu website.
4. The official balenaEtcher application, unless a future repository standard selects another USB writing tool.

Steps:

1. On Tom's MacBook, open a browser.
2. Go to the official Ubuntu website.
3. Download Ubuntu Server 24.04 LTS for AMD64.
4. Go to the official balenaEtcher website.
5. Download and install balenaEtcher for macOS.
6. Insert the USB flash drive into Tom's MacBook.
7. Stop if the USB flash drive contains files that must be saved.
8. Open Finder and identify the USB flash drive by name and size.
9. If more than one external drive is connected, eject any drive that is not needed.
10. Stop if there is any uncertainty about which drive is the USB flash drive.
11. Open balenaEtcher.
12. Choose the Ubuntu Server 24.04 LTS ISO file.
13. Choose the USB flash drive.
14. Confirm that the selected target is the USB flash drive, not the MacBook internal disk and not a backup drive.
15. Start the flash operation.
16. Approve the macOS permission prompts if they appear.
17. Wait for balenaEtcher to finish writing and verifying the USB installer.
18. Confirm balenaEtcher reports completion.
19. Eject the USB flash drive from macOS.
20. Remove the USB flash drive from Tom's MacBook.

Important:

- Creating the installer erases the USB flash drive.
- Stop if the selected USB drive is uncertain.
- Use only official Ubuntu and balenaEtcher sources.

---

## Day 1 - Boot Beelink from Ubuntu USB Installer

Steps:

1. If the Beelink is currently in BIOS, exit without saving changes.
2. If the Beelink is powered on, shut it down.
3. Insert the completed Ubuntu Server USB installer into the Beelink.
4. Confirm monitor, keyboard, and mouse are connected.
5. Press the Beelink power button.
6. Try `F7` first to open the one-time boot menu, based on the Beelink chassis label.
7. If `F7` does not open the boot menu, restart and enter BIOS.
8. In BIOS, select the UEFI USB entry for the Ubuntu installer.
9. Prefer the one-time boot menu or one-time UEFI USB selection.
10. Avoid changing permanent boot order unless the installer cannot otherwise be started.
11. Select the UEFI entry for the USB installer.
12. Continue only when the Ubuntu Server installer starts.

Stop conditions:

1. Stop if the USB drive is not listed.
2. Stop if only a non-UEFI USB option is shown.
3. Stop if Windows starts unexpectedly and the installer cannot be selected.
4. Stop before changing BIOS settings other than a temporary USB boot selection.

---

## Day 1 - Install Ubuntu Server 24.04 LTS

Follow the Ubuntu Server installer screens.

Steps:

1. Select the preferred language.
2. Select the keyboard layout.
3. Choose Ubuntu Server installation.
4. Choose the minimal/server installation path.
5. Do not choose a desktop installation.
6. Connect Ethernet during installation only if needed for installer network setup.
7. If the installer detects network automatically, continue.
8. If the installer asks for proxy settings, leave proxy blank unless the home network requires one.
9. Use the default Ubuntu mirror unless there is a clear reason to choose another mirror.
10. At storage setup, choose guided storage.
11. Choose use entire disk.
12. Select the internal 512GB SSD.
13. Confirm that the factory Windows installation will be erased.
14. Confirm that no Windows image or recovery backup will be created.
15. Continue only if the selected disk is the internal 512GB SSD.
16. Stop if the disk selection is uncertain.
17. Set hostname to `platform-node-001`.
18. Create a named non-root administrator account.
19. Use a strong password.
20. Do not use `root` as the normal administrator account.
21. Select OpenSSH server only if the installer offers it as a standard server option.
22. Do not configure SSH keys during this checkpoint unless they are already available and clearly understood.
23. Do not select extra server snaps.
24. Do not select optional services.
25. Do not install Docker.
26. Do not install Pi-hole.
27. Do not install Home Assistant, MQTT, Ollama, monitoring, dashboards, or remote management tools.
28. Let the installation complete.
29. Remove the USB installer only when the installer prompts for removal.
30. Reboot when prompted.
31. Stop when Ubuntu reaches a login prompt.

Checkpoint report to provide after installation:

1. Whether Ubuntu reached a login prompt.
2. The username created.
3. Any IP address shown on screen.
4. Any installer warnings or errors.
5. Whether Windows was removed successfully.
6. Any unexpected screen.

Do not continue past the login prompt in this checkpoint.

---

## Deferred - Network Onboarding

Network onboarding is deferred until the next approved checkpoint.

Do not perform these steps yet:

1. Do not create an ASUS router DHCP reservation.
2. Do not change router DNS.
3. Do not assign a static IP.
4. Do not record a final MAC address or IP address until the networking checkpoint is approved.
5. Do not treat any temporary installer IP address as the final Platform Node 001 address.

---

## Deferred - SSH Hardening and Administration

SSH hardening is deferred until the next approved checkpoint.

Do not perform these steps yet:

1. Do not copy MacBook SSH keys.
2. Do not disable password login.
3. Do not change root SSH login policy.
4. Do not expose SSH to the internet.
5. Do not implement remote management.

---

## Deferred - Operating Baseline Expansion

Operating baseline expansion is deferred until the next approved checkpoint.

Do not perform these steps yet:

1. Do not run package updates after first login.
2. Do not configure firewall rules.
3. Do not configure automatic updates.
4. Do not configure monitoring.
5. Do not configure dashboards.
6. Do not install Docker.
7. Do not install Platform services.

---

## Validation Checklist

| Category | Validation Item | Required Evidence |
|----------|-----------------|-------------------|
| Registry | Hardware facts recorded | Updated Beelink, switch, and UPS records |
| Lifecycle | Beelink remains planned or pending onboarding | `lifecycle_status: planned` and onboarding status |
| Power | UPS model corrected to CP850PFCLCD | Updated UPS record |
| BIOS | BIOS settings inspected with no configuration changes required | Verified BIOS facts recorded |
| BIOS Decision | CSM remains enabled, Secure Boot remains disabled, Fast Boot remains disabled | No saved BIOS changes |
| USB Installer | Ubuntu Server 24.04 LTS AMD64 installer created from macOS | balenaEtcher completion confirmation |
| OS | Ubuntu Server 24.04 LTS installed only after Day 0 gates | Stop at Ubuntu login prompt |
| Hostname | Hostname set to `platform-node-001` during installation | Login prompt or installer summary |
| Network | DHCP reservation and final network onboarding deferred | No router DNS changes |
| SSH | SSH hardening and key setup deferred | No SSH verification claimed |
| Services | No service migration or install performed | Pi-hole remains on Raspberry Pi |
| Docker | Docker not installed | Procedure stops at Ubuntu login prompt |
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
| 2.3 | Marked runbook superseded by PLAT-13.6 production baseline and warned against re-running installer steps on the active host. |
| 2.2 | Added verified BIOS evidence, no-change BIOS decision, macOS Ubuntu USB installer steps, USB boot steps, Ubuntu installation steps, and stop-at-login checkpoint boundary. |
| 2.1 | Applied Architecture Review Board decisions for Ubuntu Server 24.04 LTS, factory Windows erase disposition, milestone-level registry evidence capture, and Docker out-of-scope boundary. |
| 2.0 | Replaced readiness checklist with governed PLAT-13.3 Day 0 / Day 1 Beelink bring-up guide using delivered hardware facts. |
| 1.0 | Initial Beelink onboarding readiness checklist. |
