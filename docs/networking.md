# Networking

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

Define networking and access control for LAN and remote connectivity to the home server.

## Overview

The server is reachable on local LAN and remotely through Tailscale. Public exposure should remain minimal unless a reverse proxy and TLS are intentionally configured.

## Architecture

```text
LAN Clients
	-> Ubuntu Server (UFW)
		 -> Docker published ports (selected)

Remote Clients
	-> Tailscale mesh VPN
		 -> Ubuntu Server private tailnet IP
```

## Installation

```bash
sudo apt update
sudo apt install -y ufw
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

## Configuration

### UFW Baseline

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 2283/tcp
sudo ufw allow 3001/tcp
sudo ufw allow 9000/tcp
sudo ufw allow 19999/tcp
sudo ufw allow 8080/tcp
sudo ufw enable
```

### Tailscale

- Approve the device in the tailnet admin console.
- Prefer Tailscale IP access for admin interfaces.
- Disable broad public exposure where possible.

## Folder Structure

```text
Home-server/
â”œâ”€â”€ docs/networking.md
â”œâ”€â”€ docs/cloudflare.md
â””â”€â”€ scripts/ (network utility scripts, if added)
```

## Common Commands

```bash
# Firewall
sudo ufw status verbose

# IP and listeners
ip -br a
sudo ss -tulpen

# Tailscale
tailscale status
tailscale ip -4
```

## Updating

```bash
sudo apt update && sudo apt upgrade -y
sudo tailscale version
```

Review firewall rules after adding or removing published service ports.

## Backup

Back up network-critical configuration:

```bash
sudo cp /etc/ufw/user.rules ~/ufw-user.rules.backup
sudo cp /etc/ufw/user6.rules ~/ufw-user6.rules.backup
```

TODO: Add reverse proxy configuration backup path once reverse proxy is deployed.

## Troubleshooting

- Cannot connect over LAN:
	- Verify service container is running
	- Verify host port binding with `ss -tulpen`
- Cannot connect over Tailscale:
	- Verify `tailscale status`
	- Check device approval and ACL policies
- Port accessible locally but not remotely:
	- Verify UFW allows target port

## References

- UFW docs: https://help.ubuntu.com/community/UFW
- Tailscale docs: https://tailscale.com/kb
- Ubuntu networking docs: https://ubuntu.com/server/docs/network-configuration

