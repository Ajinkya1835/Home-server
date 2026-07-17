# Installation Guide

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

This document defines a practical installation flow for the Home-server stack on Ubuntu Server 22.04 LTS.

## Overview

The host is a 2012 MacBook Pro running Ubuntu Server and Dockerized services. Core setup order is:

1. Base OS hardening and updates
2. Encrypted storage mount
3. Docker and Docker Compose
4. Networking and remote access (UFW + Tailscale)
5. Core services (PostgreSQL, Redis, Nextcloud, Immich, monitoring)

## Architecture

```text
MacBook Pro (Mid 2012)
	-> Ubuntu Server 22.04 LTS
		-> Docker Engine + Compose
			-> Nextcloud + PostgreSQL + Redis
			-> Immich + PostgreSQL + Redis
			-> Portainer
			-> Uptime Kuma
			-> Netdata
		-> Tailscale
		-> UFW Firewall
		-> Encrypted HDD mounted at /mnt/hdd1
```

## Installation

### 1. System update

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y curl wget git ca-certificates gnupg lsb-release
```

### 2. Docker Engine and Compose plugin

```bash
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

Log out and back in after adding the user to the Docker group.

### 3. Create base folders

```bash
mkdir -p ~/Home-server
cd ~/Home-server
mkdir -p docker docs screenshots scripts systemd
```

### 4. Prepare encrypted HDD paths

```bash
sudo mkdir -p /mnt/hdd1/{immich,nextcloud,postgres,redis}
```

### 5. Enable firewall baseline

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw enable
```

### 6. Install Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

## Configuration

- Docker daemon: ensure service is enabled on boot.
- UFW: allow only ports used by published services.
- Trusted domains (Nextcloud):
	- localhost
	- 192.168.29.167
	- 100.94.248.64
- Storage mapping: bind persistent data to `/mnt/hdd1/*` paths.

## Folder Structure

```text
Home-server/
â”œâ”€â”€ docker/
â”‚   â””â”€â”€ nextcloud/
â”œâ”€â”€ docs/
â”œâ”€â”€ screenshots/
â”œâ”€â”€ scripts/
â””â”€â”€ systemd/
```

## Common Commands

```bash
# Docker status
docker ps
docker compose version

# Service management
sudo systemctl status docker
sudo systemctl restart docker

# Firewall
sudo ufw status verbose

# Tailscale
tailscale status
```

## Updating

```bash
sudo apt update && sudo apt upgrade -y
docker compose pull
docker compose up -d
docker image prune -f
```

Run compose commands from the correct service folder.

## Backup

At minimum, back up:

- Compose and env files from repository folders
- `/mnt/hdd1/nextcloud`
- `/mnt/hdd1/immich`
- Database dumps for PostgreSQL
- Redis persistence files (if enabled)

See [backup.md](./backup.md) for detailed backup procedures.

## Troubleshooting

- Docker not starting:
	- Check `sudo systemctl status docker`
	- Check logs: `journalctl -u docker -n 100 --no-pager`
- Mount missing after reboot:
	- Verify `/etc/fstab` entry and UUID
	- Validate with `sudo mount -a`
- Remote access issue:
	- Verify `tailscale status`
	- Confirm firewall rules with `sudo ufw status`

See [troubleshooting.md](./troubleshooting.md) for deeper diagnostics.

## References

- Ubuntu Server docs: https://ubuntu.com/server/docs
- Docker Engine docs: https://docs.docker.com/engine/
- Docker Compose docs: https://docs.docker.com/compose/
- Tailscale docs: https://tailscale.com/kb
- UFW docs: https://help.ubuntu.com/community/UFW

