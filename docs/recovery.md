# Recovery Guide

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

Provide a deterministic recovery runbook after hardware failure, OS reinstall, or major service corruption.

## Overview

Recovery targets:

1. Recreate host baseline (Ubuntu, Docker, networking)
2. Reattach encrypted storage
3. Restore service data and databases
4. Bring containers up in dependency order
5. Validate external access and service health

## Architecture

```text
Fresh Ubuntu Host
	-> Install Docker + networking tools
	-> Mount /mnt/hdd1
	-> Restore config and data
	-> Start PostgreSQL/Redis first
	-> Start application services
	-> Validate from LAN + Tailscale
```

## Installation

Base setup on rebuilt host:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose-plugin ufw curl
sudo systemctl enable --now docker
```

## Configuration

### Storage

- Unlock and mount encrypted disk.
- Verify mountpoint is `/mnt/hdd1`.

### Network

- Reapply UFW baseline rules.
- Rejoin Tailscale.

### Services

- Restore compose and env files.
- Restore service data and database dumps.

## Folder Structure

```text
Recovery Inputs
â”œâ”€â”€ repository backup
â”œâ”€â”€ /mnt/hdd1 service data backup
â””â”€â”€ database dumps
```

## Common Commands

```bash
# Check mounts
findmnt /mnt/hdd1

# Docker sanity
docker ps
docker compose version

# Start a stack
cd docker/nextcloud
docker compose up -d

# Follow logs
docker compose logs -f
```

## Updating

- Keep this recovery document aligned with actual compose file paths.
- Update trusted domain entries if LAN/Tailscale IPs change.

## Backup

Recovery quality depends on backup quality. Before declaring backup policy complete:

- Confirm SQL dumps are restorable
- Confirm service file backups include compose and env examples
- Confirm data backup includes `/mnt/hdd1/immich` and `/mnt/hdd1/nextcloud`

See [backup.md](./backup.md).

## Troubleshooting

- Containers fail after restore:
	- Check volume paths and permissions
	- Validate DB container readiness before app startup
- Nextcloud/Immich cannot connect to DB:
	- Verify credentials and service names in compose env
- Tailscale missing after rebuild:
	- Reinstall and run `sudo tailscale up`

## References

- Ubuntu recovery patterns: https://ubuntu.com/server/docs
- Docker troubleshooting: https://docs.docker.com/engine/daemon/troubleshoot/
- Tailscale setup: https://tailscale.com/kb

