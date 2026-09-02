#!/bin/bash
# =============================================================================
# Health Check Script
# =============================================================================

echo "🏥 Running health checks..."

# Backend
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    echo "  ✅ Backend:  healthy"
else
    echo "  ❌ Backend:  unreachable"
fi

# Frontend
if curl -sf http://localhost:80/health > /dev/null 2>&1; then
    echo "  ✅ Frontend: healthy"
else
    echo "  ❌ Frontend: unreachable"
fi

# Neo4j
if curl -sf http://localhost:7474 > /dev/null 2>&1; then
    echo "  ✅ Neo4j:    healthy"
else
    echo "  ❌ Neo4j:    unreachable"
fi
