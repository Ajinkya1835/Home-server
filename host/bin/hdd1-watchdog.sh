#!/bin/bash
NTFY="http://127.0.0.1:2586/server-alerts"   # change topic to yours
if mountpoint -q /mnt/hdd1 && timeout 10 test -f /mnt/hdd1/.drive-ok; then
  rm -f /run/hdd1-down; exit 0
fi
[ -f /run/hdd1-down ] && exit 0
touch /run/hdd1-down
for c in $(docker ps -q); do
  if docker inspect --format '{{range .Mounts}}{{.Source}}{{"\n"}}{{end}}' "$c" | grep -q '^/mnt/hdd1'; then
    docker stop -t 20 "$c"
  fi
done
curl -s -d "hdd1 missing: containers using it were stopped" "$NTFY" >/dev/null
