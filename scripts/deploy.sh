#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo '=== HOMELAB DEPLOY ==='

echo '1/5 Checking encrypted storage...'
findmnt -rn /mnt/hdd1 >/dev/null || { echo 'ERROR: /mnt/hdd1 is not mounted. Refusing deployment.'; exit 2; }
sudo cryptsetup status hdd1 2>/dev/null | grep -q 'is active' || { echo 'ERROR: LUKS hdd1 is inactive. Refusing deployment.'; exit 2; }

echo '2/5 Pulling Git changes...'
git pull --ff-only

echo '3/5 Validating Compose files...'
find . -name compose.yaml -o -name compose.yml | while read -r f; do
  dir="$(dirname "$f")"
  echo "Checking $f"
  (cd "$dir" && docker compose config >/dev/null)
done

echo '4/5 Deploying changed stacks...'
for dir in homepage immich monitoring n8n nextcloud vaultwarden; do
  if [ -f "$dir/compose.yaml" ]; then
    echo "Deploying $dir"
    (cd "$dir" && docker compose up -d)
  fi
done

echo '5/5 Final health check...'
"$ROOT/scripts/health-check.sh"

echo '=== DEPLOY COMPLETE ==='
