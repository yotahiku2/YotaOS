# YotaOS Security

YotaOS uses Fedora 44 packages for its built-in security toolkit. The desktop is still KDE Plasma; the security menu is modeled on Kali's approach of grouping tools by task. The commands themselves remain the upstream tools.

## Current build target

The KIWI `YotaOS-Security` profile includes **38 package entries**. The app menu contains **37 tool shortcuts** across eight categories, plus a dedicated **YotaOS Security Terminal**. Graphical tools open normally; CLI tools open Konsole with the YotaOS Security profile, show where the command is installed, and leave an interactive prompt with a help hint.

No launcher starts a network scan, wireless capture, password attempt, or root-required audit by itself.

| Category | Built-in launchers |
| --- | --- |
| Reconnaissance | Nmap, arp-scan, Masscan, Traceroute, WHOIS |
| Network Analysis | Wireshark (GUI), EtherApe (GUI), TShark, tcpdump, Ncat, Scapy, socat, Ettercap |
| Web Testing | Nuclei, Gobuster, WhatWeb |
| Wireless | Aircrack-ng, Airodump-ng, Airmon-ng, Aireplay-ng, Kismet, hcxpcapngtool |
| Password Auditing | Hashcat, John the Ripper, Hydra, XHydra (GUI), Medusa |
| Forensics | Sleuth Kit (fls), Foremost, TestDisk, Binwalk |
| Reverse Engineering | radare2, GDB, strace |
| Host Auditing | Lynis, chkrootkit, Rootkit Hunter |

Some tools require root access, an appropriate wireless adapter, or a non-virtualized network interface. Those privileges are **not** granted automatically by YotaOS. The KDE menu and terminal profile do not replace any command-line features.

## Package status and preflight

The first 25 security/developer package entries were installed in an earlier VM-tested image. The expanded list adds 13 Fedora 44 packages: `nmap`, `arp-scan`, `masscan`, `etherape`, `ettercap`, `gobuster`, `whatweb`, `hydra-frontend`, `medusa`, `hcxtools`, `lynis`, `chkrootkit`, `rkhunter`.

The Fedora package index lists these new packages for Fedora 44, but the local package repository configuration can differ. A previous host-side query failed to find `nmap` even though Fedora's package index lists it for Fedora 44. **Before another long build, run on the Fedora host**:

```bash
python3 scripts/check-security-packages.py
```

This is a read-only check of available names in the host's enabled DNF repositories. A successful check still does not prove that KIWI's internal dependency resolution will succeed. If a package is missing, resolve the repository difference before starting the ISO build.

## GUI versus CLI

Wireshark, EtherApe, and XHydra have their own GUI entries. A Konsole window opens for tools without a graphical interface. The dedicated security profile uses the existing YotaOS terminal colors, not a terminal emulator fork.

Kismet has its own user interface and setup requirements; the menu opens a shell with guidance instead of launching its service automatically. TestDisk is an interactive disk utility; deliberately opening a terminal first avoids accidental operations on real drives.

## Still on the wish list

SQLmap, Nikto, Ghidra, OWASP ZAP, Burp Suite Community, and Metasploit are **not bundled by this change**. Some aren't available in the configured Fedora repositories; others need separate trusted upstream packaging, licensing review, and version/checksum handling. They won't appear as pretend launchers. Add them only after their installation path and launch behavior are reproducible.

## Testing

Source CI checks the XML, menu entries, helper script, executable bit, and application references. It does **not** run the full Fedora ISO builder. On a fresh VM, check `command -v nmap`, `command -v john`, `command -v aircrack-ng`, `command -v xhydra`, and several GUI launchers before calling the expanded edition ready.

Only use these tools on systems and networks you own or are authorized to test.
