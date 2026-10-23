#!/usr/bin/env python3
"""Check the Fedora host's enabled repos before spending time on a KIWI build."""

import shutil
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "build/yotaos/components/security.xml"


def main():
    if not shutil.which("dnf"):
        sys.exit("This check requires Fedora's dnf command.")

    root = ET.parse(MANIFEST).getroot()
    packages = sorted({node.attrib["name"] for node in root.findall(".//package")})

    try:
        result = subprocess.run(
            ["dnf", "repoquery", "--available", "--qf", "%{name}", *packages],
            capture_output=True, text=True, timeout=180, check=False,
        )
    except subprocess.TimeoutExpired:
        sys.exit("DNF repository query timed out. Check network/repository access.")

    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        sys.exit("Could not query Fedora repositories.")

    available = set(result.stdout.splitlines())
    missing = [name for name in packages if name not in available]

    print(f"Found {len(packages) - len(missing)}/{len(packages)} packages "
          "in the host's enabled repositories.")
    if missing:
        print("Missing from this query:")
        for name in missing:
            print(f"  {name}")
        print("Check repository configuration before building the ISO.")
        sys.exit(1)

    print("All security package names found on the host.")
    print("This does not guarantee KIWI's repositories can resolve them.")


if __name__ == "__main__":
    main()
