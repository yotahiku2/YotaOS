# Design notes

This is the direction I'm building YotaOS toward. It's a set of decisions and tradeoffs, not a list of promised features.

## Foundation

- Fedora on x86_64, using its package and boot infrastructure.
- KDE Plasma, because it can be customized without replacing the whole desktop stack.
- KIWI image descriptions pinned to a Fedora revision. YotaOS changes live in separate profiles and a root filesystem overlay.
- Start with a VM-tested live ISO; only call something installable after checking the installer and a reboot into an installed VM.

## Desktop

The fox is the YotaOS mark. The older geometric logo can stay in the artwork directory, but it isn't the default identity.

Use a dark navy desktop with cyan and purple highlights. Keep the artwork restrained; the desktop shouldn't be covered in decorative effects. The panel is centered at the bottom, 48 px high, about two-thirds of the screen wide, and uses adaptive opacity.

Plasma stays familiar: Kicker (Application Menu), task manager, tray, clock, and show-desktop are all standard widgets. Kicker is the deliberate choice because it supports the nested Security menu. Styling the existing widgets is preferable to inventing replacements.

The terminal has a dark color scheme and a green-accented two-line prompt. It shows the current directory and Git branch when applicable. Commands and output should remain easy to read; the brand color isn't a reason to color everything green.

## Packages

A normal desktop should be usable without opening a terminal to install basic applications. The security profile adds a curated set of utilities for authorized lab work. Not every tool needs a launcher, and not every tool belongs in the default image.

Keep the package lists explicit. Prefer Fedora-packaged tools where possible, and test dependencies against the same repositories used by the ISO builder. If a tool needs an external repository or a complicated installer, document it before adding it.

## Constraints

- Don't patch firmware or replace Fedora's signed boot components just for branding.
- Keep the original working ISO until a newer image boots and installs successfully.
- Check source files quickly in CI, then group changes into fewer full ISO builds.
- Avoid features that require permanently running background services without a clear reason.
- Keep upstream credits and licenses intact.

The [roadmap](docs/ROADMAP.md) tracks what's implemented versus what's still waiting for a build or VM test.
