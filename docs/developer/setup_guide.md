# Developer Setup Guide

## Prerequisites

- Python 3.12+
- Node.js 20+
- Git
- Docker (optional, for Neo4j)

## Setup

### 1. Clone & Environment

```bash
git clone <repo-url>
cd InsiderThreat

# Python virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install Python dependencies
pip install -e ".[dev]"

# Frontend
cd frontend
npm install
cd ..
```

### 2. Configuration

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Verify Setup

```bash
# Run linters
make lint

# Run tests
make test

# Start backend
uvicorn backend.app.main:create_app --reload --factory

# Start frontend (separate terminal)
cd frontend && npm run dev
```

## IDE Setup

### VS Code Extensions
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Black Formatter
- ESLint
- Prettier
- Tailwind CSS IntelliSense

## Common Commands

```bash
make help         # Show all commands
make setup        # Install everything
make lint         # Run linters
make test         # Run tests
make format       # Format code
make docker-up    # Start Docker services
make clean        # Clean generated files
```
