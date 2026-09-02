#!/bin/bash
# =============================================================================
# Deployment Script
# =============================================================================
set -euo pipefail

echo "🚀 Deploying Insider Threat Detection System..."

# Build and start services
docker-compose -f deployment/docker-compose.yml up -d --build

echo "✅ Deployment complete!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:80"
echo "   Neo4j:    http://localhost:7474"
