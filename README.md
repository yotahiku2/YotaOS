# YotaOS 🦊

**YotaOS** is an experimental, Fedora-based Linux distribution built around **KDE Plasma** for everyday computing, development, and authorized cybersecurity labs.

Our goal: a distinctive, lightweight-feeling desktop with sensible defaults, fox branding, and a curated collection of security tools. YotaOS is an independent community project, **not** an official Fedora or Kali Linux release.

[![YotaOS source checks](https://github.com/yotahiku2/YotaOS/actions/workflows/source-checks.yml/badge.svg)](https://github.com/yotahiku2/YotaOS/actions/workflows/source-checks.yml)

## Project status

**Development preview. Not production-ready.**

| | |
| --- | --- |
| Source version | `0.2-dev` |
| Base | Fedora 44 |
| Architecture | x86_64 |
| Desktop | KDE Plasma |
| Image build system | KIWI NG |
| Security profile | Integrated in source; **not yet verified in a new ISO** |

The older 0.2-dev ISO was successfully boot-tested before the newer installer, splash, and security-profile changes. **Those newer changes have not yet been tested together in an ISO.** Do not assume a new installation is safe or complete until we've validated it in a VM.

## What makes YotaOS different?

- **Fox-first design:** YotaOS wallpaper, Plymouth boot splash, Konsole theme, floating Plasma panel, and a custom Plasma session splash in development.
- **Fedora foundation:** Uses Fedora packages and a pinned Fedora 44 KIWI description as its build base.
- **Developer-friendly:** KDE desktop, terminal-focused workflow, and open build configuration.
- **Cybersecurity tooling:** A dedicated YotaOS Security image profile, with 25 package entries covering networking, wireless analysis, web testing, forensics, debugging, and password auditing.
- **Reproducibility:** Versioned build sources, upstream revision pinning, and GitHub Actions preflight checks.

The project is inspired by the practicality of security-focused Linux systems, but it is **not a Kali fork**.

## Getting started

To inspect the source without building an ISO:

```bash
git clone https://github.com/yotahiku2/YotaOS.git
cd YotaOS
python3 scripts/validate-source.py
```

For Fedora build-host setup, KIWI prerequisites, and full ISO build steps, see **[Building YotaOS](docs/BUILDING.md)**.

> **Important:** Test development images in a virtual machine first. Before installing to physical hardware, back up your data and verify the installer and boot behavior on the target hardware.

## Security toolkit

The new profile is defined in `build/yotaos/components/security.xml`; it inherits the YotaOS desktop and is included by the live profile. Packages are subject to resolution against Fedora's configured repositories during a real KIWI build.

See **[Security toolkit](docs/SECURITY.md)** for the current package list, planned additions, and status.

Only use cybersecurity tools on systems and networks you own or are authorized to test.

## Development and roadmap

**[Roadmap](docs/ROADMAP.md)** · **[Build guide](docs/BUILDING.md)** · **[Security toolkit](docs/SECURITY.md)** · **[Issues](https://github.com/yotahiku2/YotaOS/issues)**

Contributions and bug reports are welcome. Include the YotaOS commit, Fedora base version, hardware/VM configuration, and reproduction steps when opening a bug report.

### Repository layout

| Path | Purpose |
| --- | --- |
| `branding/` | Fox identity and visual assets |
| `build/yotaos/` | KIWI image definitions and filesystem overlay |
| `build/build.sh` | End-to-end Fedora-based ISO build |
| `build/version.conf` | YotaOS source version |
| `packages/` | Planned package manifests |
| `scripts/` | Utility and source-validation scripts |
| `.github/workflows/` | Continuous source checks |

### License and upstream credits

YotaOS combines our own configuration with components from Fedora, KDE Plasma, KIWI NG, and other upstream projects, each governed by its respective license. Refer to individual files and upstream projects for copyright and license information.
