# Deployment Guide

## Prerequisites

- Docker 24.0+
- Docker Compose v2.20+
- 16 GB RAM minimum (32 GB recommended)
- 50 GB disk space

## Quick Start

```bash
# Clone repository
git clone <repo-url>
cd InsiderThreat

# Copy environment file
cp .env.example .env
# Edit .env with your values

# Start all services
make docker-up

# Verify
bash deployment/scripts/health_check.sh
```

## Services

| Service | Port | URL |
|---------|------|-----|
| Frontend | 80 | http://localhost |
| Backend API | 8000 | http://localhost:8000/api/docs |
| Neo4j Browser | 7474 | http://localhost:7474 |
| Neo4j Bolt | 7687 | bolt://localhost:7687 |

## Configuration

All configuration is managed via:
1. Environment variables (`.env` file)
2. YAML config files (`configs/`)
3. Docker Compose overrides

TODO: Add production deployment guide, SSL setup, monitoring.
