#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/upstream.conf"

OUTPUT_DIR="$SCRIPT_DIR/output"
WORK_OUTPUT="/var/tmp/yotaos-build"

echo "========================================"
echo "              YotaOS Builder"
echo "========================================"
echo
echo "Fedora release : $FEDORA_RELEASE"
echo "Fedora revision: $FEDORA_REVISION"
echo "Architecture   : x86_64"
echo "Profile        : YotaOS-Desktop-Live"
echo

echo "==> [1/4] Preparing pinned Fedora upstream"
"$SCRIPT_DIR/prepare-upstream.sh"

echo
echo "==> [2/4] Applying YotaOS definitions"
"$SCRIPT_DIR/apply-yotaos.sh"

echo
echo "==> [3/4] Cleaning previous build"
sudo rm -rf "$WORK_OUTPUT" "$WORK_OUTPUT-build"
mkdir -p "$OUTPUT_DIR"

echo
echo "==> [4/4] Building YotaOS ISO"
cd "$SCRIPT_DIR/upstream"

sudo ./kiwi-build \
    --kiwi-file="$FEDORA_KIWI_FILE" \
    --image-type="$FEDORA_IMAGE_TYPE" \
    --image-profile=YotaOS-Desktop-Live \
    --output-dir="$WORK_OUTPUT"

echo
echo "==> Build finished"
echo "==> Copying ISO to YotaOS output directory"

ISO="$(find "${WORK_OUTPUT}-build" "$WORK_OUTPUT" \
    -maxdepth 1 -type f -name '*.iso' 2>/dev/null | head -n 1)"

if [[ -z "$ISO" ]]; then
    echo "ERROR: Build completed but no ISO was found."
    exit 1
fi

DEST="$OUTPUT_DIR/YotaOS-0.1-dev-x86_64.iso"

sudo cp "$ISO" "$DEST"
sudo chown "$USER:$(id -gn)" "$DEST"

echo
echo "========================================"
echo "          YotaOS BUILD COMPLETE"
echo "========================================"
echo
echo "ISO: $DEST"
ls -lh "$DEST"
