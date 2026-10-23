# YotaOS Security

YotaOS uses Fedora 44 packages for its built-in security toolkit. The desktop is still KDE Plasma; the security menu is modeled on Kali's approach of grouping tools by task. The commands themselves remain the upstream tools.

## Current build target

The KIWI `YotaOS-Security` profile includes **41 package entries**. The app menu contains **40 tool shortcuts** across eight categories and 16 task-based subcategories, plus a dedicated **YotaOS Security Terminal**. Graphical tools open normally; CLI tools open Konsole with the YotaOS Security profile, run their usage command or interactive interface, then leave an interactive shell for further commands.

No launcher starts a network scan, wireless capture, password attempt, or root-required audit by itself.

| Category | Built-in launchers |
| --- | --- |
| Reconnaissance | Nmap, arp-scan, Masscan, Traceroute, WHOIS |
| Network Analysis | Wireshark (GUI), EtherApe (GUI), TShark, tcpdump, Ncat, Scapy, socat, Ettercap |
| Web Testing | Nuclei, Gobuster, WhatWeb |
| Wireless | Aircrack-ng, Airodump-ng, Airmon-ng, Aireplay-ng, Kismet, hcxpcapngtool |
| Password Auditing | Hashcat, John the Ripper, Ophcrack (GUI), Hydra, XHydra (GUI), Medusa |
| Forensics | Sleuth Kit (fls), Foremost, TestDisk, Binwalk |
| Reverse Engineering | radare2, GDB, iaito (GUI), ImHex (GUI), strace |
| Host Auditing | Lynis, chkrootkit, Rootkit Hunter |

Some tools require root access, an appropriate wireless adapter, or a non-virtualized network interface. Those privileges are **not** granted automatically by YotaOS. The KDE menu and terminal profile do not replace any command-line features.

## Preview in an existing YotaOS VM

To test the new menu before a full ISO build, clone this branch in the **YotaOS VM** and run `scripts/preview-security-menu.sh` as the desktop user. It installs only the menu, launchers, helper, and Konsole profile (not the new RPMs). The script refuses to run on a non-YotaOS system or directly as root.

The old and newly added launchers will appear, but the 16 newly added RPMs still need installing before those extra tools work. A live session may have limited write space, and changes will disappear on reboot unless persistence is configured.

## Package status and preflight

The earlier 25-package profile has reached a YotaOS VM; installation was explicitly checked there for Wireshark, tcpdump, Hashcat, Aircrack-ng, Nuclei, and Hydra. The expanded list now adds 16 Fedora 44 packages: `nmap`, `arp-scan`, `masscan`, `etherape`, `ettercap`, `gobuster`, `whatweb`, `hydra-frontend`, `medusa`, `hcxtools`, `lynis`, `chkrootkit`, `rkhunter`, `ophcrack`, `iaito`, `imhex`.

**Fedora 44 CI result (October 23, 2026):** all **41/41** package names were found in Fedora repositories, and a combined DNF5 transaction plan resolved successfully without installing the tools. This validates repository availability and dependency planning, **not** the full KIWI image or application startup. A host with different repositories can still produce a different result. **Before another long build, run on the Fedora host**:

```bash
python3 scripts/check-security-packages.py --resolve
```

The check first verifies exact Fedora RPM names and then asks DNF5 to solve all security packages together using `install --store` without installing or downloading RPMs. GitHub Actions also runs it inside an official Fedora 44 container. A successful Fedora transaction plan still does not prove KIWI's internal repositories or the installed GUI/CLI tools behave correctly. If a package is missing, resolve the repository difference before starting the ISO build.

## Nested menu organization

The default fox launcher is **KDE Application Menu (Kicker)**, which supports nested categories. The previous Application Launcher (Kickoff) flattened them. The fox menu now has three levels: **YotaOS Security → category → task → tool**. For example:

- **Reconnaissance → Host Discovery → Nmap**
- **Wireless → Wireless Auditing → Aircrack-ng**
- **Password Auditing → Password & Hash Auditing → John the Ripper / Ophcrack (GUI)**
- **Reverse Engineering → Binary Analysis → radare2 / iaito (GUI) / ImHex (GUI)**

There are two practical task folders in each of the eight categories (16 subfolders total). The top-level category ordering remains unchanged, and personal KDE Menu Editor overrides can still take precedence.

The new Kicker default applies to **new Plasma layouts**. Existing user panels keep their current widget unless they switch via **Show Alternatives → Application Menu**. The fox icon and the 48 px floating panel layout are unchanged.

**John the Ripper:** Its original program is terminal-based. Openwall maintains a separate Qt GUI named [Johnny](https://github.com/openwall/johnny); it is *not* bundled here because a reliable Fedora 44 package/build path has not been verified. Ophcrack is an additional GUI tool, **not** a frontend for John.

**Aircrack-ng:** The upstream suite is command-line. Third-party programs such as Fern WiFi Cracker offer a GUI, but aren't currently in the verified Fedora package manifest; the original Aircrack-ng tools remain first-class terminal launchers.

## GUI versus CLI

Wireshark, EtherApe, XHydra, Ophcrack, iaito, and ImHex have GUI entries. Each remains a separate upstream application, launched normally. A Konsole window opens for tools without a graphical interface. The dedicated security profile uses the existing YotaOS terminal colors, not a terminal emulator fork.

Kismet has its own user interface and setup requirements; the menu opens a shell with guidance instead of launching its service automatically. TestDisk is an interactive disk utility; deliberately opening a terminal first avoids accidental operations on real drives.

## Still on the wish list

SQLmap, Nikto, Ghidra, OWASP ZAP, Burp Suite Community, and Metasploit are **not bundled by this change**. Some aren't available in the configured Fedora repositories; others need separate trusted upstream packaging, licensing review, and version/checksum handling. They won't appear as pretend launchers. Add them only after their installation path and launch behavior are reproducible.

## Testing

Source CI checks the XML, menu entries, helper script, executable bit, and application references. Fedora 44 CI additionally checks RPM availability and performs a DNF5 combined dependency solve. **Neither runs the full KIWI ISO builder.**

In a running YotaOS VM, from the checkout run:

```bash
python3 scripts/check-security-runtime.py --strict
```

The runtime checker only reports installed RPMs, command availability, the installed menu tree and Konsole setup. It **does not launch any tools**. An older YotaOS ISO is expected to report missing packages and commands; this does not mean the new GitHub source is broken. Once a new ISO is built, manually launch Wireshark, Ophcrack, iaito, ImHex, John and Aircrack-ng to verify the actual user experience.

Only use these tools on systems and networks you own or are authorized to test.
