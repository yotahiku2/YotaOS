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

## 0.3-dev — Security edition (in progress)

- [x] Add a separate YotaOS-Security KIWI profile
- [x] Integrate 25 security/developer package entries into the live-profile source
- [ ] Resolve all requested packages in the actual KIWI build
- [ ] Smoke-test representative CLI/GUI tools in a fresh VM
- [ ] Provide organized security application categories without duplicating system launchers
- [ ] Investigate missing tools, licenses, and reliable distribution methods

## Future milestones

- [ ] Clear base vs. security edition choices, with documented image sizes
- [ ] Friendly welcome and setup experience
- [ ] User-facing security updates, release notes, and reproducible artifact checksums
- [ ] Test clean installation, upgrades, and boot on varied hardware before a 1.0 release
- [ ] Publish screenshots, release artifacts, download instructions, and a project site

## Development workflow

Submit meaningful changes in small reviewed pull requests. GitHub Actions runs fast source checks, but **passing CI does not mean an ISO was built or tested**. Batch features into infrequent full KIWI builds, then verify VM behavior and record failures before recommending real hardware installation.
