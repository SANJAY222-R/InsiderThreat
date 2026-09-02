#!/bin/bash
# =============================================================================
# Backup Script
# =============================================================================
set -euo pipefail

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup in $BACKUP_DIR..."

# Backup database
cp ./data/insider_threat.db "$BACKUP_DIR/" 2>/dev/null || echo "No SQLite DB found"

# Backup Neo4j
docker exec itd-neo4j neo4j-admin database dump neo4j --to-path="$BACKUP_DIR" 2>/dev/null || echo "Neo4j backup skipped"

echo "✅ Backup complete: $BACKUP_DIR"
