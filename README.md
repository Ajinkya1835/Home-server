![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu)

![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)

![License](https://img.shields.io/github/license/Ajinkya1835/Home-server)

![Last Commit](https://img.shields.io/github/last-commit/Ajinkya1835/Home-server)
# Home Server
> A self-hosted Ubuntu Server running on a repurposed 2012 MacBook Pro for personal cloud storage, photo management, monitoring, remote access, and automation.

This repository documents my self-hosted home server, running on a repurposed 2012 MacBook Pro turned into a 24/7 Ubuntu Server box. It covers everything from storage and Docker services to remote access, monitoring, and a custom Telegram bot for managing the server from anywhere.

> This project started as a simple personal cloud server and has gradually evolved into a complete home lab. Every service, configuration, and setup guide in this repository reflects the current state of my server.

---

## Features

- **Immich** — self-hosted Google-Photos alternative for photo/video management
- **Docker** — all services containerized, auto-restart on boot/failure
- **Netdata** — real-time system monitoring (CPU, RAM, disk, network, Docker)
- **Uptime Kuma** — uptime monitoring for services and endpoints
- **Portainer** — web UI for Docker management
- **Tailscale** — secure remote access (SSH + web UIs) from anywhere
- **LUKS-encrypted HDD** — 500GB WD Scorpio Blue for bulk storage
- **UFW Firewall** — locked down to only required ports
- **SMART + sensors monitoring** — disk health and temperature tracking
- **Telegram Bot** — check status, temps, logs, restart containers, or reboot the server from your phone
- **Nextcloud** — personal cloud storage, file synchronization, document management, contacts and calendar

---

## Architecture

```
MacBook Pro (2012) — Ubuntu Server 22.04.5 LTS
├── SSD (256GB) — OS, Docker, system files
├── HDD (500GB, LUKS encrypted) — mounted at /mnt/hdd1
│
 Docker
├── Immich
├── Nextcloud
├── PostgreSQL (Immich)
├── PostgreSQL (Nextcloud)
├── Redis (Immich)
├── Redis (Nextcloud)
├── Portainer
├── Uptime Kuma
└── Netdata
```

---

## Hardware

| Component | Spec |
|---|---|
| Host | MacBook Pro (2012) |
| CPU | Intel Core i5-3210M |
| RAM | 8GB |
| Boot Drive | 256GB SSD (Ubuntu Server) |
| Storage Drive | 500GB WD Scorpio Blue HDD, LUKS-encrypted |
| Network | Gigabit Ethernet |
| Uptime | 24/7 |

---

## Running Services

| Service | Purpose | Port |
|---|---|---|
| [Immich](docker/immich/) | Photo & video management | 2283 |
| [Portainer](docker-compose/portainer/) | Docker management UI | 9000 |
| [Uptime Kuma](docker-compose/uptime-kuma/) | Service/uptime monitoring | 3001 |
| [Netdata](docker-compose/netdata/) | Real-time system metrics | 19999 (host network) |
| Service   | Purpose                | Port     |
| --------- | ---------------------- | -------- |
| Nextcloud | Personal Cloud Storage | **8080** |


All containers run with `restart: unless-stopped` for automatic recovery after reboot or crash.

---

## Networking & Security

- **SSH** — enabled, accessible on LAN, remote access via Tailscale
- **Tailscale** — mesh VPN for secure remote SSH and web UI access (e.g. from college)
- **UFW Firewall** — default deny incoming / allow outgoing, with explicit allows:
  ```
  22    (SSH)
  2283  (Immich)
  3001  (Uptime Kuma)
  9000  (Portainer)
  19999 (Netdata)
  ```

Firewall configuration is documented in `docs/networking.md`.

---

## Storage

- **SSD** — root filesystem (`/`), OS + Docker + system files
- **HDD** — encrypted with LUKS, auto-mounted at `/mnt/hdd1` via `/etc/fstab`
/mnt/hdd1

├── immich
├── nextcloud
│   ├── apps
│   ├── config
│   ├── data
│   ├── postgres
│   └── redis

The complete setup is documented in `docs/telegram-bot.md`.

---

## Monitoring

- **Netdata** — CPU, RAM, load, disk, network, Docker container stats, process list
- **Uptime Kuma** — monitors Immich, Portainer, Netdata, and external sites/APIs
- **SMART monitoring** — tracks `/dev/sda` health via `smartd` (systemd service). USB SSD excluded due to startup issues with SMART passthrough.
- **Sensors** — CPU temperature, fan speed, motherboard + Apple SMC sensors via `lm-sensors`

Current disk health (WD5000BPVT): SMART **passed**, 2 pending sectors (watching), 0 reallocated sectors, ~33°C.

---

## Telegram Bot

A Python bot (`systemd` service, auto-starts on boot) that lets me manage the server remotely, restricted to my Telegram account only.

**Commands:**
```
/status        — overall server status
/temps         — CPU/system temperatures
/ram           — RAM usage
/cpu           — CPU usage
/disk          — disk usage
/smart         — SMART health summary
/uptime        — server uptime
/docker        — running containers
/updates       — available system updates
/services      — systemd service status
/logs <container> — recent logs for a container
/restart <container> — restart a container
/reboot        — reboot the server
/shutdown      — shut down the server
```

See [`telegram-bot/`](telegram-bot/) for the bot source and systemd unit.

---

## Remote Access

| Method | Access |
|---|---|
| Local SSH | `ssh ajinkya@192.168.x.x` |
| Remote SSH | via Tailscale |
| Web UIs (Portainer, Immich, Uptime Kuma, Netdata) | via Tailscale, browser |

---

## Verified

- Docker + Compose working, containers restart after reboot
- Immich, Postgres, Redis, ML service healthy
- Portainer, Netdata, Uptime Kuma healthy
- SSH + Tailscale working (including remote access from college)
- Firewall configured and tested
- HDD auto-mount working
- SMART + temperature monitoring configured
- Telegram bot working, restricted to owner
- Automatic boot verified with reboot test
- Nextcloud healthy
- PostgreSQL healthy
- Redis healthy
- Remote access via Tailscale

---

## Roadmap

- Automated Docker backups
- Off-site backup
- Reverse proxy
- HTTPS
- Daily Telegram reports
- Container failure notifications
- Watchtower
- Samba/NFS shares

---

## Repo Structure

```
Home-server/
├── docker/
├── docs/
├── screenshots/
├── scripts/
├── systemd/
├── .gitignore
├── CHANGELOG.md
├── LICENSE
└── README.md
```
## Documentation

- Installation Guide
- Networking
- Cloudflare
- Immich
- Telegram Bot
- Backup
- Recovery
- Troubleshooting
---

## Recreating This Setup

See [`docs/recovery-guide.md`](docs/recovery-guide.md) for step-by-step instructions to rebuild this server from a fresh Ubuntu Server install.
