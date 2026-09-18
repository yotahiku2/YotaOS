#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPSTREAM_DIR="$SCRIPT_DIR/upstream"
YOTA_DIR="$SCRIPT_DIR/yotaos"

if [[ ! -f "$UPSTREAM_DIR/Fedora.kiwi" ]]; then
    echo "ERROR: Fedora upstream tree is missing."
    echo "Run: ./build/prepare-upstream.sh"
    exit 1
fi

echo "==> Applying YotaOS image definitions"

# Copy YotaOS definitions into the disposable Fedora KIWI tree.
mkdir -p "$UPSTREAM_DIR/yotaos"

cp "$YOTA_DIR/components/desktop.xml" \
   "$UPSTREAM_DIR/yotaos/desktop.xml"

cp "$YOTA_DIR/live.xml" \
   "$UPSTREAM_DIR/yotaos/live.xml"

# Add our components to Fedora.kiwi exactly once.
python3 - "$UPSTREAM_DIR/Fedora.kiwi" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()

marker = '\t<include from="this://./components/liveinstall.xml"/>'

addition = (
    '\t<include from="this://./yotaos/desktop.xml"/>\n'
    '\t<include from="this://./yotaos/live.xml"/>\n'
)

if addition in text:
    print("==> YotaOS includes already present")
elif marker not in text:
    raise SystemExit("ERROR: Expected Fedora KIWI include was not found")
else:
    text = text.replace(marker, marker + "\n" + addition.rstrip(), 1)
    path.write_text(text)
    print("==> Added YotaOS includes to Fedora.kiwi")
PY

echo "==> YotaOS definitions applied"
echo "==> Profile: YotaOS-Desktop-Live"
