# YotaOS roadmap

YotaOS is experimental; milestone names describe **development goals**, not finished release guarantees.

## 0.1-dev — early prototype (historical)

- [x] Bootable Fedora-based KDE live image
- [x] Initial YotaOS identity and fox branding

## 0.2-dev — desktop and installer refinement (in progress)

- [x] Custom floating Plasma panel, wallpaper and terminal identity (previous VM testing)
- [x] Custom fox Plasma splash source
- [x] Source change intended to activate Fedora's KDE live-session installer setup
- [x] YotaOS-branded installer shortcut source
- [ ] Verify installer shortcut, KDE live setup, and fox splash in a **fresh** ISO/VM
- [ ] Complete a disposable VM installation and reboot

## 0.3 — Security edition (development build; ISO/VM testing pending)

- [x] Add a separate YotaOS-Security KIWI profile
- [x] Integrate 25 security/developer package entries into the live-profile source
- [ ] Resolve all requested packages in the actual KIWI build
- [x] Add Fedora 44 package availability and DNF5 transaction preflight in CI (source)
- [x] Fedora 44 CI found 41/41 packages and solved their DNF5 dependencies (October 23, 2026)
- [x] Add read-only runtime RPM, CLI and GUI presence checker (source change)
- [ ] Smoke-test representative CLI/GUI tools in a fresh VM
- [x] Provide organized security application categories and a YotaOS Security terminal profile (source and live menu tested)
- [x] Design two-level Security categories with 16 task-focused submenus (source changes)
- [x] Select Kicker as the default fox menu for nested categories (source change; manual widget switch VM-tested)
- [x] Add GUI package definitions for Ophcrack, iaito, and ImHex (source changes)
- [ ] Verify expanded tool packages, GUI launchers, and nested menu in a fresh live/installed VM
- [ ] Investigate missing tools, licenses, and reliable distribution methods

## Future milestones

- [ ] Clear base vs. security edition choices, with documented image sizes
- [ ] Friendly welcome and setup experience
- [ ] User-facing security updates, release notes, and reproducible artifact checksums
- [ ] Test clean installation, upgrades, and boot on varied hardware before a 1.0 release
- [ ] Publish screenshots, release artifacts, download instructions, and a project site

## Development workflow

Submit meaningful changes in small reviewed pull requests. GitHub Actions runs fast source checks, but **passing CI does not mean an ISO was built or tested**. Batch features into infrequent full KIWI builds, then verify VM behavior and record failures before recommending real hardware installation.
