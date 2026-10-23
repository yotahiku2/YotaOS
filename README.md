# YotaOS

YotaOS is my Fedora-based Linux project, built around KDE Plasma. I want it to work as a normal desktop first, with development and cybersecurity tools available without turning the base system into a mix of random shiz.

The design has its own identity: the fox, a dark desktop, a compact floating panel, and a terminal prompt that looks tuff. Under the hood, it's still Fedora and KDE. That's a deliberate choice; there's no reason to code my own display manager..

Maintained by [@yotahiku2](https://github.com/yotahiku2).

[![Source checks](https://github.com/yotahiku2/YotaOS/actions/workflows/source-checks.yml/badge.svg)](https://github.com/yotahiku2/YotaOS/actions/workflows/source-checks.yml)

## Where it stands

YotaOS is **in development**, not ready for regular installation on important hardware.

| | |
| --- | --- |
| Source version | `0.2-dev` |
| Base | Fedora 44, x86_64 |
| Desktop | KDE Plasma |
| Image builder | KIWI NG |
| Security packages | 41 entries in the next KIWI profile (not yet ISO-tested) |

The original 0.2-dev ISO booted successfully in a VM with the custom desktop layout. Since that build, I've changed the live installer setup, Plasma session splash, and security package selection. **Those changes still need a fresh ISO build and install test.**

## Design decisions

- **Fedora as the base.** Use its packages and boot infrastructure instead of writing replacements for everything.
- **KDE Plasma for the desktop.** The YotaOS layout keeps a 48 px floating panel, fox launcher, dark colors, and a custom wallpaper.
- **Keep the default usable.** Browser, file manager, editor, and terminal belong in the desktop image.
- **Security tools as a profile.** Networking, forensics, wireless analysis, and debugging packages have their own KIWI component. A smaller base edition is a future goal, not a separate release today.
- **Builds should be repeatable.** The Fedora KIWI source revision is pinned, YotaOS changes are kept in an overlay, and CI checks source files before a full build.

More on the desktop and package choices: [DESIGN.md](DESIGN.md).

## Build it

On a Fedora build machine with KIWI dependencies installed:

```bash
git clone https://github.com/yotahiku2/YotaOS.git
cd YotaOS
python3 scripts/validate-source.py
python3 scripts/check-security-packages.py
./build/build.sh
```

The last command runs a full ISO build, which can take hours and requires substantial free space. Read the [build notes](docs/BUILDING.md) before running it. Test new images in a disposable VM before touching real partitions.

## Repository

- `build/yotaos/` contains the image profiles and filesystem overlay.
- `build/upstream.conf` pins the Fedora KIWI source.
- `build/version.conf` controls the YotaOS image version.
- `branding/` keeps the source artwork.
- `scripts/` contains build-related checks.
- `packages/base.txt` is a planning list; the active package selection is in the KIWI XML files.

[Current roadmap](docs/ROADMAP.md) · [Security packages](docs/SECURITY.md) · [Report a problem](https://github.com/yotahiku2/YotaOS/issues)

YotaOS is an independent project, not an official Fedora or Kali Linux distribution. Fedora, KDE, KIWI, and included applications remain the work of their respective upstream projects and retain their own licenses. Use security tools only on systems you own or have permission to test.
