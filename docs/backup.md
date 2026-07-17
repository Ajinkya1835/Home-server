# Backup Strategy

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

Define reliable backup routines for service data, databases, and configuration required to recover the homelab.

## Overview

Backups should cover both repository-managed configuration and runtime state on `/mnt/hdd1`.

## Architecture

```text
Backup Scope
	-> Repository config (docker/, docs/, scripts/, systemd/)
	-> Service data on /mnt/hdd1
	-> PostgreSQL logical dumps
	-> Redis persistence (if enabled)
	-> Optional off-site copy (future)
```

## Installation

No additional software is strictly required beyond standard Linux tools. Recommended tools:

```bash
sudo apt install -y rsync tar gzip
```

## Configuration

Set backup destination (external disk, NAS, or secondary host). Example variables:

```bash
BACKUP_ROOT=/mnt/hdd1/backups
DATE=$(date +%F-%H%M)
```

TODO: Define final off-site target and retention policy.

## Folder Structure

```text
/mnt/hdd1/backups/
â”œâ”€â”€ config/
â”œâ”€â”€ postgres/
â”œâ”€â”€ redis/
â””â”€â”€ services/
```

## Common Commands

```bash
# Backup repo config
mkdir -p "$BACKUP_ROOT/config/$DATE"
rsync -a --delete ./ "$BACKUP_ROOT/config/$DATE/"

# Backup Nextcloud data
mkdir -p "$BACKUP_ROOT/services/$DATE"
rsync -a /mnt/hdd1/nextcloud/ "$BACKUP_ROOT/services/$DATE/nextcloud/"

# Backup Immich data
rsync -a /mnt/hdd1/immich/ "$BACKUP_ROOT/services/$DATE/immich/"
```

PostgreSQL dump examples:

```bash
# Nextcloud DB
cd docker/nextcloud
docker compose exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "/mnt/hdd1/backups/postgres/nextcloud-$DATE.sql"

# Immich DB (service name may differ)
cd ../immich
docker compose exec -T database pg_dump -U "$DB_USERNAME" "$DB_DATABASE_NAME" > "/mnt/hdd1/backups/postgres/immich-$DATE.sql"
```

## Updating

- Revalidate backup scripts after changing compose services or volume paths.
- Test restore at least monthly.

## Backup

Recommended schedule:

- Daily: database dumps
- Daily: incremental data sync
- Weekly: full config and service snapshot
- Monthly: restore drill to a test path or test host

Retention example:

- Daily backups: 14 days
- Weekly backups: 8 weeks
- Monthly backups: 6 months

## Troubleshooting

- Backup too slow:
	- Use `rsync --delete --numeric-ids`
	- Exclude cache/temp folders
- SQL dumps fail:
	- Verify DB container name and credentials
	- Check DB container health and logs
- Missing files after restore:
	- Validate destination path and permissions

## References

- Rsync docs: https://download.samba.org/pub/rsync/rsync.1
- PostgreSQL pg_dump: https://www.postgresql.org/docs/current/app-pgdump.html
- Redis persistence: https://redis.io/docs/management/persistence/

