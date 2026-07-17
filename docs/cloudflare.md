# Cloudflare and Domain

Back to [README](../README.md)

## Table of Contents

- [Purpose](#purpose)
- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Folder Structure](#folder-structure)
- [Common Commands](#common-commands)
- [Updating](#updating)
- [Backup](#backup)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Purpose

Document Cloudflare usage for DNS, optional proxying, and domain routing for self-hosted services.

## Overview

Cloudflare can provide DNS management and edge security for public endpoints. For sensitive admin services, prefer LAN or Tailscale-only access.

## Architecture

```text
Public Client
	-> Cloudflare DNS/Proxy
		-> Home network public IP (if exposed)
			-> Router port forward
				-> Reverse proxy (optional, TODO)
					-> Docker services
```

## Installation

No host installation required for basic DNS.

Optional components:

- Reverse proxy container on server
- Cloudflare Tunnel connector

TODO: Confirm whether this setup uses direct port forwarding or Cloudflare Tunnel.

## Configuration

Minimum DNS record pattern:

- `A` or `CNAME` records for selected public subdomains

Security recommendations:

- Keep admin surfaces private where possible
- Use strong authentication and least exposure
- Apply TLS end-to-end where feasible

TODO: Add exact domain names and record mappings once finalized.

## Folder Structure

```text
Home-server/
â”œâ”€â”€ docs/cloudflare.md
â””â”€â”€ scripts/ (optional DNS automation scripts)
```

## Common Commands

```bash
# Verify DNS resolution
dig +short example.yourdomain.tld

# Verify HTTPS response headers
curl -I https://example.yourdomain.tld
```

Replace sample hostnames with real subdomains.

## Updating

- Recheck DNS records whenever local service IP/port mapping changes.
- Revalidate TLS certificates after renewals or proxy changes.

## Backup

Back up:

- DNS record export (from Cloudflare dashboard/API)
- Reverse proxy config files (if used)
- Any tunnel credentials/config files

## Troubleshooting

- DNS resolves to wrong IP:
	- Check `A`/`CNAME` record values
	- Check TTL and propagation delay
- 521/522 style origin errors:
	- Verify origin service is reachable and listening
	- Confirm firewall/router forwarding
- SSL errors:
	- Validate TLS mode compatibility with origin cert state

## References

- Cloudflare DNS docs: https://developers.cloudflare.com/dns/
- Cloudflare SSL/TLS docs: https://developers.cloudflare.com/ssl/
- Cloudflare Tunnel docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

