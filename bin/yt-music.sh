#!/bin/bash
URL="https://music.youtube.com/playlist?list=PLVLhdr6OA2zc"
DEST="/mnt/backup/media/music/Playlists"
ARCHIVE="/home/ajinkya/yt-music-archive.txt"
LOG="/home/ajinkya/yt-music.log"
STALLS=0

touch "$ARCHIVE"
exec 9>/tmp/yt-music.lock
flock -n 9 || { echo "Already running"; exit 1; }

log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

wait_for_ready() {
  until mountpoint -q /mnt/backup; do log "Waiting for /mnt/backup mount..."; sleep 30; done
  until curl -4 -sI --max-time 10 https://www.youtube.com >/dev/null; do
    log "Waiting for internet..."; sleep 30
  done
}

while true; do
  wait_for_ready
  BEFORE=$(wc -l < "$ARCHIVE")
  log "Starting run (archive has $BEFORE tracks)"

  /usr/local/bin/yt-dlp -x --audio-format best --yes-playlist --no-mtime \
    --embed-metadata --embed-thumbnail \
    --download-archive "$ARCHIVE" --ignore-errors --no-overwrites \
    --retries 20 --fragment-retries 20 --extractor-retries 5 --retry-sleep 10 \
    --socket-timeout 30 --force-ipv4 \
    -o "$DEST/%(playlist_title)s/%(artist,uploader)s - %(title)s.%(ext)s" \
    "$URL"
  RC=$?

  AFTER=$(wc -l < "$ARCHIVE")
  log "Run ended: exit=$RC, archive $BEFORE -> $AFTER"

  if [ "$RC" -eq 0 ]; then
    log "Playlist fully downloaded. Done."
    exit 0
  fi

  if [ "$AFTER" -gt "$BEFORE" ]; then
    STALLS=0
  else
    STALLS=$((STALLS+1))
    log "No progress ($STALLS/3)"
    if [ "$STALLS" -ge 3 ]; then
      log "No progress in 3 runs. Remaining items are likely unavailable. Done."
      exit 0
    fi
  fi
  sleep 60
done
