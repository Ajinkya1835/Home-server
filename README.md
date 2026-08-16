![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)
![License](https://img.shields.io/github/license/Ajinkya1835/Home-server)
![Last Commit](https://img.shields.io/github/last-commit/Ajinkya1835/Home-server)

# Home Server

> A self-hosted Ubuntu Server running on a repurposed 2012 MacBook Pro for personal cloud storage, photo management, monitoring, remote access, and automation.

This repository documents my self-hosted home server, running on a repurposed 2012 MacBook Pro turned into a 24/7 Ubuntu Server box. It covers storage, Docker services, remote access, monitoring, and operations notes for recovery and maintenance.

## Table of Contents

- [Current Architecture](#current-architecture)
- [Hardware](#hardware)
- [Features](#features)
- [Services](#services)
- [Docker Containers](#docker-containers)
- [Folder Structure](#folder-structure)
- [Documentation Index](#documentation-index)
- [Installation Order](#installation-order)
- [Backup Strategy](#backup-strategy)
- [Screenshots](#screenshots)
- [Repository Status and Cleanup](#repository-status-and-cleanup)
- [Roadmap](#roadmap)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Credits](#credits)

## Current Architecture

```text
MacBook Pro Mid 2012
  -> Ubuntu Server 22.04 LTS
    -> Docker
      -> Immich
      -> Nextcloud
      -> Portainer
      -> Netdata
      -> Uptime Kuma
      -> PostgreSQL
      -> Redis
    -> Tailscale
    -> Telegram Bot
    -> SMART Monitoring
    -> Encrypted HDD (/mnt/hdd1)
```

## Hardware

| Component | Spec |
|---|---|
| Host | MacBook Pro (Mid 2012) |
| CPU | Intel Core i5-3210M |
| RAM | 8GB |
| Storage | Internal SSD + external encrypted HDD |
| OS | Ubuntu Server 22.04 LTS |

## Features

- Self-hosted photo and video management with Immich
- Personal cloud storage with Nextcloud
- Dockerized services with restart policies
- Monitoring with Netdata and Uptime Kuma
- Secure remote management over Tailscale
- Owner-only Telegram bot for operational commands
- Encrypted persistent storage mounted at `/mnt/hdd1`
- Host security baseline using UFW

## Services

| Service | Purpose | Access |
|---|---|---|
| Immich | Photo and video management | LAN / Tailscale |
| Nextcloud | Personal cloud storage | LAN / Tailscale |
| Portainer | Docker management UI | LAN / Tailscale |
| Uptime Kuma | Availability checks | LAN / Tailscale |
| Netdata | Real-time host metrics | LAN / Tailscale |
| PostgreSQL | Application metadata storage | Internal Docker network |
| Redis | Caching and queueing | Internal Docker network |

## Docker Containers

Current runtime stack:

- `immich`
- `nextcloud`
- `portainer`
- `uptime-kuma`
- `netdata`
- `postgresql` (service-specific)
- `redis` (service-specific)

Repository note:

- Existing compose content currently present in this repository is under `docker/nextcloud/`.
- TODO: Add or sync compose files for other services if they are managed outside this repository.

## Folder Structure

```text
Home-server/
â”œâ”€â”€ docker/
â”‚   â””â”€â”€ nextcloud/
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ installation.md
â”‚   â”œâ”€â”€ nextcloud.md
â”‚   â”œâ”€â”€ immich.md
â”‚   â”œâ”€â”€ cloudflare.md
â”‚   â”œâ”€â”€ networking.md
â”‚   â”œâ”€â”€ backup.md
â”‚   â”œâ”€â”€ recovery.md
â”‚   â”œâ”€â”€ troubleshooting.md
â”‚   â””â”€â”€ telegram-bot.md
â”œâ”€â”€ screenshots/
â”œâ”€â”€ scripts/
â”œâ”€â”€ systemd/
â”œâ”€â”€ CHANGELOG.md
â”œâ”€â”€ LICENSE
â”œâ”€â”€ README.md
â””â”€â”€ .gitignore
```

## Documentation Index

- [Installation Guide](docs/installation.md)
- [Nextcloud](docs/nextcloud.md)
- [Immich](docs/immich.md)
- [Cloudflare and Domain](docs/cloudflare.md)
- [Networking](docs/networking.md)
- [Backup Strategy](docs/backup.md)
- [Recovery Guide](docs/recovery.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Telegram Bot](docs/telegram-bot.md)

## Installation Order

1. Install Ubuntu Server 22.04 LTS and apply updates
2. Install Docker Engine + Compose plugin
3. Configure encrypted HDD mount at `/mnt/hdd1`
4. Configure firewall (UFW) and Tailscale
5. Deploy stateful dependencies (PostgreSQL, Redis)
6. Deploy application services (Nextcloud, Immich)
7. Deploy management and monitoring services (Portainer, Uptime Kuma, Netdata)
8. Configure Telegram bot and systemd service
9. Validate service health and backup jobs

## Backup Strategy

- Persistent data is stored on `/mnt/hdd1`
- Backup coverage includes:
  - Service data directories
  - PostgreSQL logical dumps
  - Redis persistence (if enabled)
  - Repository configuration files
- Recovery procedures are documented in [docs/recovery.md](docs/recovery.md)

## Screenshots

Place screenshots in `screenshots/` and reference them here.

Example structure:

```text
screenshots/
â”œâ”€â”€ immich-dashboard.png
â”œâ”€â”€ nextcloud-home.png
â”œâ”€â”€ netdata-overview.png
â””â”€â”€ uptime-kuma-status.png
```

## Repository Status and Cleanup

Verified in this repository:

- Required top-level files exist: `README.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore`
- Required top-level folders exist: `docker/`, `docs/`, `scripts/`, `systemd/`, `screenshots/`
- No duplicate documentation files inside `docs/`
- No duplicate folder names in project paths (excluding `.git` internals)

## Roadmap

- Reverse proxy and HTTPS hardening
- Scheduled and tested backup automation
- Off-site backup replication
- Alerting improvements for container failures
- Domain and Cloudflare production routing

## Future Improvements

- Add service-level compose files for all documented containers where missing
- Add healthcheck-driven startup ordering for dependent services
- Add restore drill scripts for faster disaster recovery
- Add structured operational runbooks in `scripts/` and `systemd/`

## License

`LICENSE` file exists in this repository.

TODO: Add finalized license text if this project is intended for public reuse.

## Credits

Maintained by Ajinkya as a personal homelab documentation and operations repository.

Community docs and tools used:

- Ubuntu Server
- Docker and Docker Compose
- Immich
- Nextcloud
- Tailscale
- Netdata
- Uptime Kuma

