#!/usr/bin/env python3
"""Read-only smoke check for security tools in a running YotaOS environment.

Checks installed RPM names, expected commands, and YotaOS menu assets.
It does not launch GUIs, start security scans, or request privileges.
"""

import argparse
import configparser
from pathlib import Path
import shutil
import subprocess
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "build/yotaos/root-overlay"
MANIFEST = ROOT / "build/yotaos/components/security.xml"
LAUNCHERS = OVERLAY / "usr/share/applications"


def installed_rpms() -> set[str]:
    if not shutil.which("rpm"):
        sys.exit("The rpm command is unavailable; run this on YotaOS or Fedora.")
    result = subprocess.run(
        ["rpm", "-qa", "--qf", r"%{NAME}\n"],
        capture_output=True, text=True, timeout=60, check=False,
    )
    if result.returncode:
        sys.exit(f"rpm query failed: {result.stderr.strip()}")
    return set(result.stdout.splitlines())


def installed_menu_counts() -> tuple[int, int]:
    path = Path("/etc/xdg/menus/applications-merged/yotaos-security.menu")
    if not path.is_file():
        return (0, 0)
    try:
        top = ET.parse(path).getroot().find("./Menu")
    except ET.ParseError:
        return (0, 0)
    if top is None or top.findtext("Name") != "YotaOS Security":
        return (0, 0)
    groups = top.findall("./Menu")
    return (len(groups), sum(len(g.findall("./Menu")) for g in groups))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="exit nonzero when any expected package or command is absent")
    args = parser.parse_args()

    packages = sorted({
        element.attrib["name"]
        for element in ET.parse(MANIFEST).getroot().findall(".//package")
    })
    installed = installed_rpms()
    missing_rpms = sorted(set(packages) - installed)
    print(f"RPM packages: {len(packages) - len(missing_rpms)}/{len(packages)} installed")
    if missing_rpms:
        print("  Missing packages:", ", ".join(missing_rpms))

    apps = sorted(LAUNCHERS.glob("yotaos-security-*.desktop"))
    missing_commands = []
    for app in apps:
        if app.name == "yotaos-security-terminal.desktop":
            continue
        settings = configparser.ConfigParser(interpolation=None)
        settings.read(app, encoding="utf-8")
        section = settings["Desktop Entry"]
        executable = section.get("TryExec", "").strip()
        if executable == "konsole":
            # CLI helper consumes the last argument in the fixed Exec template.
            executable = section.get("Exec", "").rsplit(" ", 1)[-1]
        if not executable or shutil.which(executable) is None:
            missing_commands.append((section.get("Name", app.stem), executable))

    n = len(apps) - 1
    print(f"Tool binaries: {n - len(missing_commands)}/{n} available")
    if missing_commands:
        print("  Missing commands:")
        for name, executable in missing_commands:
            print(f"    {name}: {executable or '<unset>'}")

    menu = installed_menu_counts()
    print(f"Installed menu: {menu[0]} categories / {menu[1]} subcategories")
    helper = Path("/usr/libexec/yotaos/security-tool").is_file()
    profile = Path("/usr/share/konsole/YotaOS-Security.profile").is_file()
    print(f"Konsole helper/profile: {'yes' if helper else 'no'} / "
          f"{'yes' if profile else 'no'}")
    if not shutil.which("konsole"):
        print("Konsole: not found; CLI desktop entries cannot open")

    print("NOTE: Presence checks only; GUI startup, permissions, and hardware "
          "still require manual VM testing.")
    failed = bool(missing_rpms or missing_commands or menu != (8, 16)
                  or not helper or not profile or not shutil.which("konsole"))
    return 1 if failed and args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
