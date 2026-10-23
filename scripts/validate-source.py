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

    # KDE menu fragments can nest Menu elements. Validate the category tree
    # and the files it references without needing a Plasma runtime in CI.
    overlay = ROOT / "build/yotaos/root-overlay"
    menu = ET.parse(
        overlay / "etc/xdg/menus/applications-merged/yotaos-security.menu"
    ).getroot()
    require(menu.tag == "Menu" and menu.findtext("Name") == "Applications",
            "Invalid application menu root")
    require([m.text for m in menu.findall("./Layout/Menuname")][:1] ==
            ["YotaOS Security"], "Security menu should appear first")

    section = menu.find("./Menu")
    require(section is not None and section.findtext("Name") == "YotaOS Security",
            "YotaOS Security category is missing")
    directories = overlay / "usr/share/desktop-directories"
    applications = overlay / "usr/share/applications"
    require((directories / section.findtext("Directory")).is_file(),
            "YotaOS Security directory is missing")

    groups = section.findall("./Menu")
    expected_groups = [
        ("Reconnaissance", ["Host Discovery", "Port & Route Mapping"]),
        ("Network Analysis", ["Packet Capture", "Traffic & Connections"]),
        ("Web Testing", ["Website Discovery", "Security Checks"]),
        ("Wireless", ["Monitoring & Capture", "Wireless Auditing"]),
        ("Password Auditing", ["Password & Hash Auditing", "Login Auditing"]),
        ("Forensics", ["Disk & Recovery", "File & Firmware Analysis"]),
        ("Reverse Engineering", ["Binary Analysis", "Process Tracing"]),
        ("Host Auditing", ["System Audits", "Rootkit Checks"]),
    ]
    require([g.findtext("Name") for g in groups] ==
            [name for name, _ in expected_groups],
            "Unexpected Security menu category order")
    require([m.text for m in section.findall("./Layout/Menuname")] ==
            [name for name, _ in expected_groups],
            "Top-level Security category layout is incomplete")

    gui_launchers = {
        "wireshark", "etherape", "xhydra", "ophcrack", "iaito", "imhex"
    }
    items = []
    cli_tools = []
    for group, (_, expected_subgroups) in zip(groups, expected_groups):
        folder = group.findtext("Directory")
        require(folder and (directories / folder).is_file(),
                f"Missing category directory: {group.findtext('Name')}")
        require(not group.findall("./Include/Filename"),
                f"Tools must be placed in subcategories: {group.findtext('Name')}")
        subgroups = group.findall("./Menu")
        require([s.findtext("Name") for s in subgroups] == expected_subgroups,
                f"Unexpected subcategory names: {group.findtext('Name')}")
        require([m.text for m in group.findall("./Layout/Menuname")] ==
                expected_subgroups,
                f"Unexpected subcategory order: {group.findtext('Name')}")
        for subgroup in subgroups:
            subdirectory = subgroup.findtext("Directory")
            require(subdirectory and (directories / subdirectory).is_file(),
                    f"Missing directory: {subgroup.findtext('Name')}")
            entries = subgroup.findall("./Include/Filename")
            require(entries, f"Empty subcategory: {subgroup.findtext('Name')}")
            for node in entries:
                filename = node.text
                require(filename and filename.startswith("yotaos-security-")
                        and filename.endswith(".desktop"),
                        f"Invalid desktop filename: {filename}")
                launcher = applications / filename
                require(launcher.is_file(), f"Missing launcher: {filename}")
                data = launcher.read_text(encoding="utf-8")
                require("[Desktop Entry]" in data and "Type=Application" in data
                        and "Exec=" in data and "TryExec=" in data,
                        f"Incomplete launcher: {filename}")
                shortname = filename.removeprefix("yotaos-security-").removesuffix(".desktop")
                if shortname in gui_launchers:
                    require(f"Exec={shortname}\n" in data
                            and f"TryExec={shortname}\n" in data,
                            f"Incorrect GUI launcher: {filename}")
                else:
                    require("Exec=konsole --profile YotaOS-Security "
                            f"-e /usr/libexec/yotaos/security-tool {shortname}\n"
                            in data, f"Incorrect Konsole launcher: {filename}")
                    cli_tools.append(shortname)
                items.append(filename)

    terminal_file = "yotaos-security-terminal.desktop"
    require([f.text for f in section.findall("./Include/Filename")] ==
            [terminal_file], "Security terminal shortcut missing")
    terminal = applications / terminal_file
    require(terminal.is_file() and
            "Exec=konsole --profile YotaOS-Security\n" in
            terminal.read_text(encoding="utf-8"),
            "Security terminal launcher is invalid")
    require(len(items) == 40 and len(set(items)) == len(items),
            "Expected 40 unique tool launchers")
    require(set(items + [terminal_file]) ==
            {p.name for p in applications.glob("yotaos-security-*.desktop")},
            "Missing or unreferenced Security launcher")
    require(len(gui_launchers) == 6 and
            gui_launchers <=
            {name.removeprefix("yotaos-security-").removesuffix(".desktop")
             for name in items},
            "GUI launchers missing")

    helper = overlay / "usr/libexec/yotaos/security-tool"
    require(helper.is_file() and bool(helper.stat().st_mode & 0o111),
            "Security terminal helper must be executable")
    helper_text = helper.read_text(encoding="utf-8")
    for name in cli_tools:
        require(f'{name}) tool="{name}";' in helper_text,
                f"Helper doesn't recognize tool: {name}")
    profile = overlay / "usr/share/konsole/YotaOS-Security.profile"
    require(profile.is_file() and "ColorScheme=YotaOS" in
            profile.read_text(encoding="utf-8"),
            "YotaOS Security Konsole profile missing")
    plasma_layout = read("build/yotaos/root-overlay/usr/share/plasma/"
                         "look-and-feel/org.yotaos.desktop/contents/"
                         "layouts/org.kde.plasma.desktop-layout.js")
    require('yotaLauncher.writeConfig("highlightNewlyInstalledApps", false)'
            in plasma_layout, "Default Kickoff should disable New badges")

    print(f"PASS: {len(component_paths)} KIWI XML files, "
          f"{len(names)} security packages, profile wiring, "
          f"installer, splash, and {len(items) + 1} Security menu launchers")
    print("NOTE: This does not validate Fedora package resolution or ISO runtime.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, ValueError, ET.ParseError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
