#!/usr/bin/env bash
set -euo pipefail

# Preview only the menu, Konsole profile, and launcher helper.
# No RPM installation or personal KDE configuration changes.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$script_dir/../build/yotaos/root-overlay"

if [[ "${EUID}" -eq 0 ]]; then
    echo "Run this as your regular YotaOS user, not root." >&2
    exit 1
fi

if [[ ! -f /etc/os-release ]]; then
    echo "Cannot identify the running OS." >&2
    exit 1
fi

# shellcheck disable=SC1091
source /etc/os-release
if [[ "${ID:-}" != "yotaos" ]]; then
    echo "The preview installer only runs on YotaOS." >&2
    exit 1
fi

menu="$source_dir/etc/xdg/menus/applications-merged/yotaos-security.menu"
helper="$source_dir/usr/libexec/yotaos/security-tool"
profile="$source_dir/usr/share/konsole/YotaOS-Security.profile"

for required in "$menu" "$helper" "$profile"; do
    [[ -f "$required" ]] || { echo "Missing: $required" >&2; exit 1; }
done

sudo -v
sudo install -Dm644 "$menu" \
    /etc/xdg/menus/applications-merged/yotaos-security.menu
sudo install -Dm755 "$helper" \
    /usr/libexec/yotaos/security-tool
sudo install -Dm644 "$profile" \
    /usr/share/konsole/YotaOS-Security.profile

for entry in "$source_dir/usr/share/applications"/yotaos-security-*.desktop; do
    sudo install -Dm644 "$entry" "/usr/share/applications/${entry##*/}"
done

for entry in "$source_dir/usr/share/desktop-directories"/yotaos-security-*.directory; do
    sudo install -Dm644 "$entry" "/usr/share/desktop-directories/${entry##*/}"
done

if command -v kbuildsycoca6 >/dev/null 2>&1; then
    kbuildsycoca6 --noincremental
fi

echo
echo "YotaOS Security menu preview installed."
echo "Close and reopen the fox launcher, then open YotaOS Security."
echo "Only menu assets were installed. New tools still need their RPMs."
echo "A nonpersistent live session will lose these changes at reboot."
