#!/usr/bin/env bash
set -euo pipefail

echo "==> Configuring YotaOS branding"

if [[ -d /usr/share/plymouth/themes/yotaos ]]; then
    plymouth-set-default-theme yotaos
fi
