#!/bin/bash
O=$HOME/fullcheck-$(date +%F-%H%M).txt
C=$HOME/docker/homepage/config
{
echo "=== UPTIME/RESOURCES"; uptime; free -h | head -2; df -h / /mnt/hdd1 /mnt/backup
echo "=== MOUNTS"; mountpoint /mnt/hdd1; mountpoint /mnt/backup
echo "=== CONTAINERS"; docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo "=== RESTARTS/OOM"; docker inspect -f "{{.Name}} restarts={{.RestartCount}} oom={{.State.OOMKilled}}" $(docker ps -aq)
echo "=== LISTENING (non-local)"; ss -tlnH | awk "\$4 !~ /^127\\./ && \$4 !~ /^\\[::1\\]/ {print \$4}" | sort -u
echo "=== TAILSCALE SERVE"; tailscale serve status 2>&1 | grep -E "https|proxy"
echo "=== SERVICE RESPONSES"; for p in 2283 8081 3000 9000 5678 8888 8080 8096 8090 2586 3030 3001 4000 6080; do printf "%s " $p; curl -s -o /dev/null -m 4 -w "%{http_code}\n" http://127.0.0.1:$p/; done
echo "=== PROMETHEUS TARGETS"; docker exec prometheus wget -qO- http://localhost:9090/api/v1/targets | grep -o "\"job\":\"[^\"]*\"\|\"health\":\"[a-z]*\"" | paste - -
echo "=== FIRING ALERTS"; curl -s http://127.0.0.1:9093/api/v2/alerts | head -c 300; echo
echo "=== IMMICH DB"; docker exec immich_postgres psql -U postgres -d immich -Atc "select count(*) from asset"
echo "=== BACKUPS"; ls -lh /mnt/backup/server-backups | tail -4; sudo -n tail -3 /root/backup.log 2>&1
echo "=== CRON"; crontab -l | grep -v "^#"; sudo -n crontab -l 2>/dev/null | grep -v "^#"
echo "=== SYSTEMD FAILED"; systemctl --failed --no-legend
echo "=== ERRORS 24h"; for c in $(docker ps --format "{{.Names}}"); do echo "$c $(docker logs --since 24h $c 2>&1 | grep -ciE "error|fatal|panic")"; done
echo "=== HOMEPAGE RECENT ERRORS"; docker logs homepage --since 30m 2>&1 | grep -i error | cut -c1-180 | sort | uniq -c
echo "=== HOMEPAGE TILES VS CONTAINERS"
grep -E "^\s+container:" $C/services.yaml | awk "{print \$2}" | sort -u > /tmp/hp_tiles
docker ps --format "{{.Names}}" | sort > /tmp/running
echo "-- running but NO tile:"; comm -13 /tmp/hp_tiles /tmp/running
echo "-- tile but container NOT running:"; comm -23 /tmp/hp_tiles /tmp/running
echo "=== HOMEPAGE LINKS VS TAILSCALE PORTS"
grep -oE "ts\.net:[0-9]+" $C/services.yaml | sort -u > /tmp/hp_ports
tailscale serve status 2>&1 | grep -oE "ts\.net:[0-9]+" | sort -u > /tmp/ts_ports
echo "-- ports served but not linked:"; comm -13 /tmp/hp_ports /tmp/ts_ports
echo "-- linked but not served:"; comm -23 /tmp/hp_ports /tmp/ts_ports
echo "=== HOMEPAGE ENV KEYS SET"; cut -d= -f1 $HOME/docker/homepage/.env
echo "=== HOMEPAGE YAML"; python3 -c "import yaml,glob;[yaml.safe_load(open(f)) for f in glob.glob(\"$C/*.yaml\")];print(\"all yaml valid\")"
} 2>&1 | sed -E "s/(tskey-[A-Za-z0-9_-]+|eyJ[A-Za-z0-9._-]{20,}|bot[0-9]+:[A-Za-z0-9_-]+)/[HIDDEN]/g" | tee "$O"
echo; echo "Saved: $O"
