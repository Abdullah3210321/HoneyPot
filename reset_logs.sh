#!/bin/bash
LOG_DIR="/home/cowrie/cowrie/var/log/cowrie"
BACKUP_DIR="$LOG_DIR/backups"
DATE=$(date +%F_%T)

mkdir -p "$BACKUP_DIR"
cp "$LOG_DIR/cowrie.json" "$BACKUP_DIR/cowrie_$DATE.json"
cp "$LOG_DIR/cowrie.log" "$BACKUP_DIR/cowrie_log_$DATE.log"

> "$LOG_DIR/cowrie.json"
> "$LOG_DIR/cowrie.log"

echo "Logs backed up and cleared."
