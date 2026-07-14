# Home Server — Self-Hosted Media, Monitoring & Automation

This repository documents my self-hosted home server, running on a repurposed 2012 MacBook Pro turned into a 24/7 Ubuntu Server box. It covers everything from storage and Docker services to remote access, monitoring, and a custom Telegram bot for managing the server from anywhere.

> This started as a simple Nextcloud + Cloudflare project (see [`docs/history.md`](docs/history.md) for the original writeup) and has since evolved into a full home lab with photo management, monitoring, and automation.

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

---

## Architecture

```
MacBook Pro (2012) — Ubuntu Server 22.04.5 LTS
├── SSD (256GB) — OS, Docker, system files
├── HDD (500GB, LUKS encrypted) — mounted at /mnt/hdd1
│
├── Docker
│   ├── Immich (server, postgres, redis, machine-learning)
│   ├── Portainer
│   ├── Uptime Kuma
│   └── Netdata (host network)
│
├── Telegram Bot (Python, systemd service)
├── SMART monitoring (systemd)
├── Tailscale (remote SSH + web UI access)
└── UFW (firewall)
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
| [Immich](docker-compose/immich/) | Photo & video management | 2283 |
| [Portainer](docker-compose/portainer/) | Docker management UI | 9000 |
| [Uptime Kuma](docker-compose/uptime-kuma/) | Service/uptime monitoring | 3001 |
| [Netdata](docker-compose/netdata/) | Real-time system metrics | 19999 (host network) |

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

See [`scripts/firewall-setup.sh`](scripts/firewall-setup.sh) for the UFW rules.

---

## Storage

- **SSD** — root filesystem (`/`), OS + Docker + system files
- **HDD** — encrypted with LUKS, auto-mounted at `/mnt/hdd1` via `/etc/fstab`

See [`docs/storage-setup.md`](docs/storage-setup.md) for the LUKS + fstab configuration.

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

---

## Roadmap

- Automated backup scripts
- Daily Telegram health report
- Telegram alerts for container failures / SMART changes
- Samba file sharing
- Reverse proxy with HTTPS (Caddy/Nginx)
- GitHub Actions for configuration backup
- Docker auto-update notifications (Watchtower or similar)
- Immich backup automation
- Home Assistant integration

---

## Repo Structure

```
Home-server/
├── README.md
├── docker-compose/
│   ├── immich/docker-compose.yml
│   ├── portainer/docker-compose.yml
│   ├── uptime-kuma/docker-compose.yml
│   └── netdata/docker-compose.yml
├── telegram-bot/
│   ├── bot.py
│   ├── requirements.txt
│   └── telegram-bot.service
├── scripts/
│   ├── firewall-setup.sh
│   ├── luks-hdd-setup.sh
│   └── smart-setup.sh
└── docs/
    ├── storage-setup.md
    ├── recovery-guide.md
    └── history.md
```

---

## Recreating This Setup

See [`docs/recovery-guide.md`](docs/recovery-guide.md) for step-by-step instructions to rebuild this server from a fresh Ubuntu Server install.
