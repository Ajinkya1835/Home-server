# Tailscale routing

All application routes are private to the tailnet and use the same MagicDNS host.

| Service | URL | Local backend |
|---|---|---|
| Nextcloud | https://ajinkya.tail32b205.ts.net:8443 | 127.0.0.1:8080 |
| Immich | https://ajinkya.tail32b205.ts.net:8444 | 127.0.0.1:2283 |
| n8n | https://ajinkya.tail32b205.ts.net:8445 | 127.0.0.1:5678 |
| Portainer | https://ajinkya.tail32b205.ts.net:8446 | 127.0.0.1:9000 |
| Grafana | https://ajinkya.tail32b205.ts.net:8447 | 127.0.0.1:3000 |
| Uptime Kuma | https://ajinkya.tail32b205.ts.net:8449 | 127.0.0.1:3001 |
| Homepage | https://ajinkya.tail32b205.ts.net:8450 | 127.0.0.1:3030 |
| Vaultwarden | https://ajinkya.tail32b205.ts.net:8451 | 127.0.0.1:8081 |

Apply/reapply all routes with:

```bash
cd ~/Home-server
bash routing/tailscale-serve.sh
```

Verify with:

```bash
tailscale serve status
```

Do not use old `/vault` routing or the previous `:8448` Vaultwarden endpoint.
