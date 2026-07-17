# Troubleshooting

Back to [README](../README.md)

## Purpose

Provide a centralized troubleshooting playbook for host, storage, networking, and containerized services.

## Overview

Use this workflow:

1. Confirm host health
2. Confirm storage mount and free space
3. Confirm Docker engine and target containers
4. Confirm network/firewall/Tailscale path
5. Inspect service-specific logs

## Architecture

```text
Host Layer
	-> OS services (systemd, disk, network)
Container Layer
	-> Docker daemon
	-> Service containers
Access Layer
	-> LAN and Tailscale
```

## Installation

Install diagnostic tools:

```bash
sudo apt update
sudo apt install -y htop iotop smartmontools lm-sensors net-tools curl jq
```

## Configuration

Recommended baseline:

- Docker service enabled on boot
- UFW default deny incoming
- Tailscale active for remote admin access
- SMART monitoring configured for persistent drives

## Folder Structure

```text
Home-server/
â”œâ”€â”€ docs/troubleshooting.md
â”œâ”€â”€ scripts/ (diagnostic helpers)
â””â”€â”€ systemd/ (service units)
```

## Common Commands

```bash
# Host checks
uptime
free -h
df -h
sudo dmesg -T | tail -n 100

# Docker checks
docker ps -a
docker stats --no-stream
sudo systemctl status docker

# Network checks
ip -br a
sudo ss -tulpen
sudo ufw status verbose
tailscale status

# Disk health
sudo smartctl -a /dev/sda
sensors
```

## Updating

- Keep this troubleshooting document aligned with new services and ports.
- Add known incidents with root cause and resolution.

## Backup

Before high-risk changes:

- Export compose and environment templates
- Snapshot/backup `/mnt/hdd1` service data
- Dump PostgreSQL databases

See [backup.md](./backup.md).

## Troubleshooting

### Docker daemon not running

```bash
sudo systemctl status docker
sudo journalctl -u docker -n 100 --no-pager
```

### Container restart loop

```bash
docker compose ps
docker compose logs --tail=200 <service_name>
```

Typical causes: wrong env variables, permission mismatch, missing bind mount path, database unavailable.

### Storage path unavailable

```bash
findmnt /mnt/hdd1
sudo mount -a
```

If mount fails, validate UUID and filesystem state.

### Service inaccessible remotely

- Verify service bound to expected port
- Verify UFW allows the port
- Verify Tailscale node connectivity and ACLs

## References

- Docker troubleshoot docs: https://docs.docker.com/engine/daemon/troubleshoot/
- Ubuntu server docs: https://ubuntu.com/server/docs
- SMART docs: https://www.smartmontools.org/
- Tailscale troubleshooting: https://tailscale.com/kb/1023/troubleshooting

