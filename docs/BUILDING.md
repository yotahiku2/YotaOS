# Building YotaOS

YotaOS currently uses Fedora 44 KIWI image descriptions to produce an x86_64 KDE live ISO. The build is designed to run on a **Fedora Linux host**; other Linux distributions are not tested.

## Prerequisites

- A Fedora host with network access, sufficient free disk space, and working `sudo`
- `git`, `python3`, KIWI NG CLI and ISO-media dependencies
- Enough **native Linux filesystem** space for the downloaded RPMs and KIWI work directory; plan for **tens of GB** of scratch space, not just the final ISO
- Time: a full build can take hours on HDDs

Install the main development tools on Fedora:

```bash
sudo dnf install -y git python3 kiwi-cli kiwi-systemdeps-iso-media
```

Package availability and exact dependency sets can change as Fedora repositories evolve.

## Clone and validate

```bash
git clone https://github.com/yotahiku2/YotaOS.git
cd YotaOS
python3 scripts/validate-source.py
bash -n build/build.sh build/prepare-upstream.sh build/apply-yotaos.sh
```

GitHub Actions runs quick source checks. A separate **Fedora 44 security package preflight** uses Fedora's official container and DNF5 to check package availability and solve an install plan without installing the security RPMs. Neither check boots YotaOS or proves KIWI will use identical repositories.

Before a full build on your Fedora host, run:

```bash
python3 scripts/check-security-packages.py --resolve
```

This checks all security packages together in a disposable DNF5 transaction plan. It does not remove existing files or install the packages.

## Full ISO build

```bash
./build/build.sh
```

The builder:

1. Reads `build/upstream.conf` and `build/version.conf`.
2. Clones the pinned Fedora KIWI descriptions into generated `build/upstream/`.
3. Copies YotaOS profile definitions and filesystem overlays into that disposable upstream tree.
4. Builds the `YotaOS-Desktop-Live` KIWI profile.
5. Copies the verified ISO into `build/output/YotaOS-<version>-x86_64.iso`.

The active version and output path come from `build/version.conf`. Do not rename an old ISO and treat it as a newly built version: the version is also stamped inside the image.

**Caution:** `build/build.sh` deletes its previous build work directories under `/var/tmp/yotaos-build` (and its KIWI build output counterpart) and replaces the same-version ISO at the destination. Keep files you care about elsewhere.

## Test before hardware installation

1. Boot the freshly generated ISO in GNOME Boxes or another UEFI-capable VM.
2. Confirm YotaOS branding, KDE session startup, and the visible **Install YotaOS** shortcut.
3. Open the installer and verify that it can discover the intended **VM disk**. Do not test partitioning on a drive containing important data.
4. Run `python3 scripts/check-security-runtime.py --strict` from your YotaOS checkout. This read-only check reports installed RPMs, visible commands, menu folders and Konsole integration. It never launches scans or applications. Try a selection of CLI and GUI applications manually as a separate step.
5. Test an installation into a **disposable VM virtual disk**, reboot, and confirm the normal created user can sign in.

Not all planned tools or desktop changes are verified just because CI passes. For packaging issues, retain the KIWI logs and list the Fedora repositories used.
