# Immich

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

Document deployment and operations for Immich, including media storage, database, and cache dependencies.

## Overview

Immich is used as a self-hosted photo and video management platform. It runs in Docker and uses PostgreSQL and Redis for metadata and caching.

## Architecture

```text
Immich Web/Mobile Clients
	-> Immich server containers
		-> PostgreSQL
		-> Redis
		-> Media library on /mnt/hdd1/immich
```

## Installation

1. Ensure Docker and Docker Compose plugin are installed.
2. Ensure `/mnt/hdd1/immich` exists and is writable.
3. Start Immich stack from its compose folder.

```bash
cd docker/immich
docker compose up -d
```

TODO: Confirm exact repository path and compose file name for Immich in this repo.

## Configuration

- Store media on encrypted HDD under `/mnt/hdd1/immich`.
- Keep database and Redis data persistent outside ephemeral container filesystems.
- Use explicit timezone configuration in environment variables.
- Restrict public exposure; prefer LAN or Tailscale access.

## Folder Structure

```text
/mnt/hdd1/immich/
â”œâ”€â”€ library/
â”œâ”€â”€ upload/
â”œâ”€â”€ thumbs/
â””â”€â”€ database/
```

Adjust to match the exact paths defined in your compose files.

## Common Commands

```bash
cd docker/immich

# Lifecycle
docker compose up -d
docker compose down
docker compose restart

# Logs
docker compose logs -f

# Health check
docker compose ps
```

## Updating

```bash
cd docker/immich
docker compose pull
docker compose up -d
docker image prune -f
```

Post-update checks:

- Mobile app login works
- New uploads are visible
- Thumbnail generation is healthy

## Backup

Back up:

- Immich media directory on `/mnt/hdd1/immich`
- PostgreSQL database dump
- Redis persistence file if enabled

Example DB dump pattern:

```bash
docker compose exec -T database pg_dump -U "$DB_USERNAME" "$DB_DATABASE_NAME" > immich.sql
```

## Troubleshooting

- Upload failures:
	- Check free disk space and permissions on mounted media path
- App loads but media missing:
	- Verify volume mappings in compose file
- High CPU usage:
	- Check background jobs, transcoding, and machine learning services

## References

- Immich docs: https://immich.app/docs
- Immich GitHub: https://github.com/immich-app/immich
- PostgreSQL docs: https://www.postgresql.org/docs/
- Redis docs: https://redis.io/docs/

