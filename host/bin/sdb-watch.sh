#!/bin/bash
OUT=$(smartctl -x -d sat /dev/sdb)
ERR=$(echo "$OUT" | awk '/Device Error Count/ {print $4}')
REA=$(echo "$OUT" | awk '/Reallocated_Sector_Ct/ {print $NF}')
PEN=$(echo "$OUT" | awk '/Current_Pending_Sector/ {print $NF}')
UNC=$(echo "$OUT" | awk '/Offline_Uncorrectable/ {print $NF}')
if [ "${ERR:-0}" -gt 8 ] || [ "${REA:-0}" -gt 0 ] || [ "${PEN:-0}" -gt 0 ] || [ "${UNC:-0}" -gt 0 ]; then
  echo "$(date) sdb WARNING err=$ERR realloc=$REA pending=$PEN uncorr=$UNC" >> /var/log/sdb-watch.log
  logger -p user.crit "sdb SMART warning: err=$ERR realloc=$REA pending=$PEN uncorr=$UNC"
  runuser -u ajinkya -- env NOTIFY_HOME=/home/ajinkya /home/ajinkya/bin/notify "sdb SMART warning" "err=$ERR realloc=$REA pending=$PEN uncorr=$UNC" high
fi
