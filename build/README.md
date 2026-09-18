# YotaOS Build System

YotaOS images are built using KIWI on Fedora.

## Current Target

- Base: Fedora 44
- Architecture: x86_64
- Desktop: KDE Plasma
- Image type: Live ISO
- Upstream profile: KDE-Desktop-Live

## Design

YotaOS uses Fedora's KIWI image definitions as its upstream base and applies
YotaOS-specific changes on top.

The upstream Fedora definitions are not vendored wholesale into this repository.

## Output

Generated images and temporary build artifacts belong in `build/output/`
and must not be committed to Git.
