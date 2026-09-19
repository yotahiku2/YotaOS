#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/upstream.conf"
source "$SCRIPT_DIR/version.conf"

# Authenticate sudo once before the long KIWI build and keep the
# credential timestamp alive until this script exits.
sudo -v

while true; do
    sudo -n true
    sleep 60
done 2>/dev/null &
SUDO_KEEPALIVE_PID=$!

cleanup() {
    kill "$SUDO_KEEPALIVE_PID" 2>/dev/null || true
}
trap cleanup EXIT

OUTPUT_DIR="$SCRIPT_DIR/output"
WORK_OUTPUT="/var/tmp/yotaos-build"
BUILD_OUTPUT="${WORK_OUTPUT}-build"
DEST="$OUTPUT_DIR/YotaOS-${YOTAOS_VERSION}-x86_64.iso"

echo "========================================"
echo "              YotaOS Builder"
echo "========================================"
echo
echo "YotaOS version : $YOTAOS_VERSION"
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
sudo rm -rf "$WORK_OUTPUT" "$BUILD_OUTPUT"
mkdir -p "$OUTPUT_DIR"
rm -f "$DEST"

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

ISO="$BUILD_OUTPUT/Fedora.x86_64-${FEDORA_RELEASE}.iso"

if [[ ! -f "$ISO" ]]; then
    echo "ERROR: Expected KIWI ISO was not found:"
    echo "       $ISO"
    echo
    echo "Files produced by KIWI:"
    find "$BUILD_OUTPUT" -maxdepth 1 -type f -printf '  %p\n' 2>/dev/null || true
    exit 1
fi

echo "==> Copying fresh ISO"
echo "    Source: $ISO"
echo "    Dest  : $DEST"

sudo cp -f "$ISO" "$DEST"
sudo chown "$USER:$(id -gn)" "$DEST"
sync

echo
echo "==> Verifying copied ISO"
SOURCE_SHA256="$(sha256sum "$ISO" | awk '{print $1}')"
DEST_SHA256="$(sha256sum "$DEST" | awk '{print $1}')"

if [[ "$SOURCE_SHA256" != "$DEST_SHA256" ]]; then
    echo "ERROR: Copied ISO does not match KIWI output."
    exit 1
fi

echo
echo "========================================"
echo "          YotaOS BUILD COMPLETE"
echo "========================================"
echo
echo "ISO    : $DEST"
echo "SHA256 : $DEST_SHA256"
ls -lh --time-style=long-iso "$DEST"
