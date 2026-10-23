# YotaOS Security toolkit

YotaOS is building a Fedora-based security workstation for **authorized labs, defensive analysis, and security education**. It is not a Kali fork.

## Status

The `YotaOS-Security` profile is part of the source tree and is required by `YotaOS-Desktop-Live`. **Package resolution and runtime behavior have not yet been verified by a new full KIWI build.**

The 25 package names below were queried against a Fedora 44 host's configured repositories during development. An individual package's presence on the host does not guarantee resolution in the ISO builder's repositories.

## Packages in the current image manifest

| Category | Fedora package names |
| --- | --- |
| Network analysis | `wireshark`, `wireshark-cli`, `tcpdump`, `nmap-ncat`, `socat`, `traceroute`, `whois`, `python3-scapy` |
| Web security | `nuclei` |
| Password auditing | `hashcat`, `john`, `hydra` |
| Wireless analysis | `aircrack-ng`, `kismet` |
| Digital forensics | `sleuthkit`, `foremost`, `testdisk`, `binwalk` |
| Reverse engineering/debugging | `radare2`, `gdb`, `strace` |
| Development tools | `git`, `gcc`, `make`, `jq` |

Some commands require elevated privileges, additional drivers, external hardware, or explicit permission to access a network. Some run only in the terminal. GUI launchers and curated application-menu categories are planned, not yet shipped.

## Not yet included in the manifest

The following were considered but were not found by the specific Fedora 44 repository check used during development: `nmap`, `sqlmap`, `nikto`, `ghidra`, and `zaproxy`. This **does not prove they are unavailable**. We should verify Fedora package naming, enabled repositories, upstream installation methods, licenses, and build compatibility before integration.

`nmap-ncat` is **not** the full `nmap` network scanner.

## Direction

- Maintain a clean desktop and avoid installing every security tool by default in lighter YotaOS editions.
- Add optional packages or curated profiles for web testing, forensics, malware analysis, and wireless research.
- Prefer distribution-packaged and reproducible dependencies.
- Document repository trust, security updates, tool capabilities, and permissions.
- Test CLI and GUI startup in a disposable VM before announcing features as working.

Cybersecurity tools must be used **only against systems and networks you own or have permission to assess**. Never run destructive checks against third-party targets without authorization.
