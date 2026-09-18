#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/upstream.conf"

UPSTREAM_URL="https://forge.fedoraproject.org/releng/kiwi-descriptions.git"
UPSTREAM_DIR="$SCRIPT_DIR/upstream"

echo "==> Preparing Fedora ${FEDORA_RELEASE} KIWI definitions"
echo "==> Branch: ${FEDORA_BRANCH}"

rm -rf "$UPSTREAM_DIR"

git clone \
    --branch "$FEDORA_BRANCH" \
    --single-branch \
    "$UPSTREAM_URL" \
    "$UPSTREAM_DIR"

git -C "$UPSTREAM_DIR" checkout --detach "$FEDORA_REVISION"

echo
echo "==> Upstream ready"
echo "==> Revision: $(git -C "$UPSTREAM_DIR" rev-parse HEAD)"
echo "==> Location: $UPSTREAM_DIR"
