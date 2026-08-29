#!/usr/bin/env bash
set -euo pipefail

HOST="ajinkya.tail32b205.ts.net"

# Private tailnet-only HTTPS routes for currently deployed services.
# Nextcloud and Uptime Kuma are intentionally omitted because they are retired.
sudo tailscale serve --https=8444 --bg http://127.0.0.1:2283
sudo tailscale serve --https=8445 --bg http://127.0.0.1:5678
sudo tailscale serve --https=8446 --bg http://127.0.0.1:9000
sudo tailscale serve --https=8447 --bg http://127.0.0.1:3000
sudo tailscale serve --https=8450 --bg http://127.0.0.1:3030
sudo tailscale serve --https=8451 --bg http://127.0.0.1:8081

printf '\nTailscale routes applied:\n'
printf 'Immich      https://%s:8444\n' "$HOST"
printf 'n8n         https://%s:8445\n' "$HOST"
printf 'Portainer   https://%s:8446\n' "$HOST"
printf 'Grafana     https://%s:8447\n' "$HOST"
printf 'Homepage    https://%s:8450\n' "$HOST"
printf 'Vaultwarden https://%s:8451\n' "$HOST"

echo
sudo tailscale serve status
