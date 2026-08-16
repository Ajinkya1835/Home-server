# Nextcloud

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

Document deployment and operations for Nextcloud running in Docker with PostgreSQL and Redis.

## Overview

Nextcloud provides self-hosted file sync, sharing, and personal cloud functionality. Data and service state are stored on encrypted external storage mounted at `/mnt/hdd1`.

## Architecture

```text
Client (Web/Mobile/Desktop)
	-> Nextcloud container
		-> PostgreSQL (metadata)
		-> Redis (cache/locking)
		-> Persistent storage on /mnt/hdd1/nextcloud
```

## Installation

1. Ensure Docker Engine and Compose are available.
2. Ensure mount exists: `/mnt/hdd1/nextcloud`.
3. Start stack from the Nextcloud compose directory.

```bash
cd docker/nextcloud
docker compose up -d
```

## Configuration

### Trusted Domains

Use the following trusted domains:

- localhost
- 192.168.29.167
- 100.94.248.64

### Persistent Volumes

Use bind mounts mapped to encrypted disk paths under `/mnt/hdd1/nextcloud`.

### Reverse Proxy / TLS

TODO: Add final reverse proxy and TLS configuration once selected and deployed.

## Folder Structure

```text
/mnt/hdd1/nextcloud/
â”œâ”€â”€ apps/
â”œâ”€â”€ config/
â”œâ”€â”€ data/
â”œâ”€â”€ postgres/
â””â”€â”€ redis/
```

## Common Commands

```bash
# Start/stop/restart
cd docker/nextcloud
docker compose up -d
docker compose down
docker compose restart

# Logs
docker compose logs -f nextcloud
docker compose logs -f postgres
docker compose logs -f redis

# Container shell
docker compose exec nextcloud bash
```

## Updating

```bash
cd docker/nextcloud
docker compose pull
docker compose up -d
docker image prune -f
```

After updates, verify:

- Web login works
- File upload/download works
- Background jobs are healthy

## Backup

Back up three components together:

1. Nextcloud data and config
2. PostgreSQL dump
3. Redis persistence (if enabled)

Example database backup:

```bash
cd docker/nextcloud
docker compose exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > nextcloud.sql
```

See [backup.md](./backup.md) and [recovery.md](./recovery.md).

## Troubleshooting

- HTTP 500 errors:
	- Check `nextcloud` and `postgres` logs
	- Verify DB credentials and connectivity
- "Trusted domain" warning:
	- Confirm domain/IP is present in trusted domains
- Slow uploads:
	- Validate storage health and free space on `/mnt/hdd1`
	- Review PHP upload limits in container config

## References

- Nextcloud admin manual: https://docs.nextcloud.com/server/latest/admin_manual/
- Nextcloud Docker image: https://hub.docker.com/_/nextcloud
- PostgreSQL docs: https://www.postgresql.org/docs/
- Redis docs: https://redis.io/docs/

