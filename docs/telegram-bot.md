# Telegram Bot

Back to [README](../README.md)

## Purpose

Document deployment, operation, and hardening of the Telegram bot used for remote server management.

## Overview

The bot is intended for owner-only operations such as status checks, logs, container restarts, and controlled reboot/shutdown actions.

## Architecture

```text
Telegram Client
	-> Telegram API
		-> Bot process (systemd service on Ubuntu host)
			-> Local command execution (docker/system metrics)
```

## Installation

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

Example setup pattern:

```bash
cd ~/Home-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

TODO: Add exact bot source path in repository once committed.

## Configuration

Store runtime secrets in environment variables, not in source code.

Required values:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_CHAT_ID`

Never commit real values.

## Folder Structure

```text
Home-server/
â”œâ”€â”€ systemd/
â”‚   â””â”€â”€ (telegram bot service unit)
â”œâ”€â”€ scripts/
â”‚   â””â”€â”€ (bot helpers, if used)
â””â”€â”€ docs/telegram-bot.md
```

## Common Commands

```bash
# systemd status
sudo systemctl status telegram-bot

# start/stop/restart
sudo systemctl start telegram-bot
sudo systemctl stop telegram-bot
sudo systemctl restart telegram-bot

# logs
journalctl -u telegram-bot -n 100 --no-pager
journalctl -u telegram-bot -f
```

## Updating

```bash
cd ~/Home-server
git pull
sudo systemctl restart telegram-bot
```

Validate bot responsiveness after restart using `/status`.

## Backup

Back up:

- Bot source files
- systemd unit file
- non-secret config files

Do not back up real tokens in plaintext.

## Troubleshooting

- Bot not responding:
	- Check service state and logs
	- Validate network connectivity and Telegram API reachability
- Command execution failures:
	- Verify service user permissions for Docker/system commands
- Unauthorized usage concerns:
	- Confirm strict chat ID allowlist is enforced

## References

- Telegram Bot API: https://core.telegram.org/bots/api
- Python venv docs: https://docs.python.org/3/library/venv.html
- systemd docs: https://www.freedesktop.org/software/systemd/man/systemd.service.html

