#!/usr/bin/env python3
"""Fast, offline checks for the YotaOS source tree (not an ISO boot test)."""

from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    component_paths = [
        "build/yotaos/components/desktop.xml",
        "build/yotaos/components/security.xml",
        "build/yotaos/live.xml",
    ]
    profiles = {}

    for filename in component_paths:
        root = ET.parse(ROOT / filename).getroot()
        require(root.tag == "image", f"{filename}: expected an <image> root")

        for profile in root.findall("./profiles/profile"):
            name = profile.attrib["name"]
            require(name not in profiles, f"Duplicate profile: {name}")
            profiles[name] = {
                entry.attrib["profile"] for entry in profile.findall("./requires")
            }

        for package_group in root.findall("./packages"):
            require(package_group.get("profiles") in {
                profile.attrib["name"]
                for profile in root.findall("./profiles/profile")
            }, f"{filename}: package group references an undefined profile")

    require(profiles["YotaOS-Desktop-Live"] >= {
        "YotaOS-Security", "LiveInstall"
    }, "Live image must include Security and LiveInstall")
    require("YotaOS-Desktop" in profiles["YotaOS-Security"],
            "Security profile must inherit the desktop")

    security_root = ET.parse(ROOT / "build/yotaos/components/security.xml").getroot()
    names = [p.attrib["name"] for p in security_root.findall(".//package")]
    require(names and len(names) == len(set(names)),
            "Security package list is empty or contains duplicates")

    apply_script = read("build/apply-yotaos.sh")
    require('$YOTA_DIR/components/security.xml' in apply_script,
            "Build does not copy security.xml")
    require('this://./yotaos/security.xml' in apply_script,
            "Build does not include security.xml in Fedora.kiwi")
    require('--image-profile=YotaOS-Desktop-Live' in read("build/build.sh"),
            "Builder must select the YotaOS live profile")

    branding = read("build/yotaos/root-overlay/usr/lib/yotaos/branding.sh")
    require('livesys_session="kde"' in branding,
            "KDE live-session initialization is missing")
    extra = ROOT / "build/yotaos/root-overlay/var/lib/livesys/livesys-session-extra"
    require(extra.is_file() and "Exec=liveinst" in extra.read_text(encoding="utf-8"),
            "Live installer shortcut setup is missing")

    look = "build/yotaos/root-overlay/usr/share/plasma/look-and-feel/org.yotaos.desktop"
    require("Theme=org.yotaos.desktop" in read(f"{look}/contents/defaults"),
            "YotaOS Plasma splash is not selected")
    splash = read(f"{look}/contents/splash/Splash.qml")
    require("images/yotaos-fox.png" in splash,
            "YotaOS Plasma splash does not reference the fox")
    require((ROOT / f"{look}/contents/splash/images/yotaos-fox.png").is_file(),
            "YotaOS fox splash asset is missing")

    print(f"PASS: {len(component_paths)} KIWI XML files, "
          f"{len(names)} security packages, profile wiring, "
          "installer setup, and splash assets")
    print("NOTE: This does not validate Fedora package resolution or ISO runtime.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, ValueError, ET.ParseError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
