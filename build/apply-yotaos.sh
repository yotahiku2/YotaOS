#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPSTREAM_DIR="$SCRIPT_DIR/upstream"
YOTA_DIR="$SCRIPT_DIR/yotaos"

source "$SCRIPT_DIR/version.conf"

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

echo "==> Installing YotaOS root overlay"

mkdir -p "$UPSTREAM_DIR/root"

cp -a "$YOTA_DIR/root-overlay/." "$UPSTREAM_DIR/root/"

echo "==> Stamping YotaOS version: $YOTAOS_VERSION"

sed -i     -e "s/^VERSION=.*/VERSION=$YOTAOS_VERSION/"     "$UPSTREAM_DIR/root/usr/share/yotaos/yotaos.conf"

printf '%s\n' "YotaOS $YOTAOS_VERSION"     > "$UPSTREAM_DIR/root/etc/yotaos-release"

sed -i     -e "s/^VERSION=.*/VERSION=\"$YOTAOS_VERSION\"/"     -e "s/^VERSION_ID=.*/VERSION_ID=\"$YOTAOS_VERSION_ID\"/"     -e "s/^PRETTY_NAME=.*/PRETTY_NAME=\"YotaOS $YOTAOS_VERSION\"/"     "$UPSTREAM_DIR/root/usr/lib/os-release"

sed -i     -e "s/^Comment=YotaOS .*/Comment=YotaOS $YOTAOS_VERSION/"     "$UPSTREAM_DIR/root/usr/share/plasma/plasma-welcome/intro-customization.desktop"

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

echo "==> Installing YotaOS GRUB template"

cp "$YOTA_DIR/grub-x86.cfg.iso-template" \
   "$UPSTREAM_DIR/grub-x86.cfg.iso-template"

echo "==> Installing YotaOS branding configuration"

cp "$YOTA_DIR/config/branding.sh" \
   "$UPSTREAM_DIR/yotaos/branding.sh"

python3 - "$UPSTREAM_DIR/config.sh" <<'PYCONFIG'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()

hook = """
# YotaOS branding
if [[ "$kiwi_profiles" == *"YotaOS-Desktop"* ]]; then
    /bin/bash /usr/lib/yotaos/branding.sh
fi

"""

marker = "exit 0"

if hook not in text:
    if marker not in text:
        raise SystemExit("ERROR: config.sh exit marker not found")
    text = text.rsplit(marker, 1)[0] + hook + marker + "\n"
    path.write_text(text)
PYCONFIG

echo "==> YotaOS definitions applied"
echo "==> Profile: YotaOS-Desktop-Live"
