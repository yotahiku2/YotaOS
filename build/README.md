# Image build

The YotaOS ISO uses Fedora 44 KIWI definitions, pinned in `upstream.conf`. The upstream tree is downloaded into `build/upstream/` at build time and isn't tracked in this repository.

`prepare-upstream.sh` fetches the pinned Fedora files. `apply-yotaos.sh` copies in the YotaOS profiles and root overlay. `build.sh` runs those steps and then builds the `YotaOS-Desktop-Live` profile.

The live profile currently pulls in `YotaOS-Security`, which inherits `YotaOS-Desktop`. The profile names are used by build hooks, so don't rename them casually.

The final ISO goes into `build/output/`. KIWI working directories live under `/var/tmp/yotaos-build` and `/var/tmp/yotaos-build-build`. The build script removes the previous contents of those paths before starting a new build.

Generated ISOs and scratch files should not be committed.

See [the build guide](../docs/BUILDING.md) for prerequisites, commands, and VM checks.
