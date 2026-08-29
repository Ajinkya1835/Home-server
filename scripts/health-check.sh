#!/usr/bin/env bash
set -euo pipefail

echo '=== HOMELAB HEALTH ==='
echo
printf 'Host: '; hostname
printf 'Uptime: '; uptime -p

echo
echo '=== STORAGE ==='
if findmnt -rn /mnt/hdd1 >/dev/null; then
  echo 'HDD: mounted'
  df -h /mnt/hdd1
else
  echo 'CRITICAL: /mnt/hdd1 is NOT mounted'
  exit 2
fi

if sudo cryptsetup status hdd1 2>/dev/null | grep -q 'is active'; then
  echo 'LUKS: active'
else
  echo 'CRITICAL: LUKS hdd1 is inactive'
  exit 2
fi

echo
echo '=== DOCKER ==='
docker ps --format 'table {{.Names}}\t{{.Status}}'

echo
echo '=== IMMICH ==='
docker inspect immich_server --format 'Status={{.State.Status}} Health={{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}} Restarts={{.RestartCount}}' 2>/dev/null || echo 'Immich server not found'
