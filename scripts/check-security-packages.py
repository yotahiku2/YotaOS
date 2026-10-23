#!/usr/bin/env python3
"""Check YotaOS security packages against the currently enabled Fedora repos.

The --resolve mode saves a DNF5 transaction plan; it does not download or
install RPMs. The build's KIWI environment may still differ from the host.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "build/yotaos/components/security.xml"


def query_packages() -> set[str]:
    try:
        result = subprocess.run(
            # Query the complete Fedora catalog and compare exact names.
            ["dnf", "repoquery", "--available", "--qf", "%{name}"],
            capture_output=True, text=True, timeout=240, check=False,
        )
    except subprocess.TimeoutExpired:
        sys.exit("DNF repository query timed out. Check network access.")

    if result.returncode:
        print(result.stderr.strip(), file=sys.stderr)
        sys.exit(f"DNF repoquery failed (exit {result.returncode}).")

    names = set(result.stdout.splitlines())
    if not names:
        print("DNF returned no package names; raw output preview:",
              repr(result.stdout[:300]), file=sys.stderr)
        print("DNF diagnostics:", repr(result.stderr[:500]), file=sys.stderr)
        sys.exit("DNF repository query returned an empty catalog.")
    return names


def resolve_packages(packages: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="yotaos-dnf-plan-") as directory:
        command = [
            "dnf", "--setopt=install_weak_deps=False", "install",
            f"--store={directory}", *packages,
        ]
        print("Resolving all packages in a single DNF5 transaction (no install)...",
              flush=True)
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, timeout=420, check=False,
            )
        except subprocess.TimeoutExpired:
            sys.exit("DNF dependency resolution timed out.")

        print(result.stdout[-12000:])
        if result.returncode:
            sys.exit(
                f"DNF could not resolve the security transaction "
                f"(exit {result.returncode})."
            )
        print("PASS: DNF5 solved the package transaction without installing it.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--resolve", action="store_true",
        help="use DNF5 --store to check a combined dependency transaction",
    )
    args = parser.parse_args()

    if not shutil.which("dnf"):
        sys.exit("This check requires Fedora's dnf command.")

    root = ET.parse(MANIFEST).getroot()
    names = [node.attrib["name"] for node in root.findall(".//package")]
    if len(names) != len(set(names)):
        sys.exit("Duplicate security package names found in KIWI XML.")

    packages = sorted(names)
    available = query_packages()
    missing = [name for name in packages if name not in available]

    print(
        f"Found {len(packages) - len(missing)}/{len(packages)} package names "
        "in the enabled repositories.", flush=True
    )
    if missing:
        print("Missing:")
        for name in missing:
            print(f"  {name}")
        sys.exit("Resolve missing names/repository differences before an ISO build.")

    if args.resolve:
        resolve_packages(packages)
    else:
        print("Names are present; pass --resolve to check combined dependencies.")

    print("This does not run KIWI or verify installed-VM functionality.")


if __name__ == "__main__":
    main()
