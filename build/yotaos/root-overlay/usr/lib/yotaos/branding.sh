#!/usr/bin/env bash
set -euo pipefail

echo "==> Configuring YotaOS branding"

if [[ -d /usr/share/plymouth/themes/yotaos ]]; then
    plymouth-set-default-theme yotaos
fi

# Tell Fedora's live system to initialize the KDE session.
# This enables installer shortcuts, Kickoff favorites, and live setup.
mkdir -p /etc/sysconfig
printf '%s\n' 'livesys_session="kde"' > /etc/sysconfig/livesys
