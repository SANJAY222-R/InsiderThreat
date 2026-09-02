<div align="center">

# 🛡️ Insider Threat Detection System

### Temporal Heterogeneous Graph Learning for Explainable Insider Threat Detection in Enterprise Environments

[![CI](https://github.com/your-org/insider-threat-detection/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/insider-threat-detection/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

---

## 📋 Overview

An enterprise-grade system for detecting insider threats using **Temporal Heterogeneous Graph Neural Networks (THGNN)**. The system processes enterprise log data (logon, device, email, HTTP, file events) to build temporal heterogeneous graphs, then applies graph neural networks with attention mechanisms to identify anomalous employee behavior patterns.

Key capabilities:
- 🔍 **Real-time Threat Detection** — Continuous monitoring of employee behavior
- 🧠 **Graph Neural Networks** — THGNN model on heterogeneous temporal graphs
- 📊 **Explainable AI** — Interpretable predictions with feature attribution
- 🖥️ **Interactive Dashboard** — React-based visualization with graph explorer
- 🐳 **Containerized Deployment** — Docker Compose with Neo4j, Nginx

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React + TypeScript)          │
│            Dashboard · Graph Viewer · Investigations     │
├─────────────────────────────────────────────────────────┤
│                    Nginx Reverse Proxy                   │
├─────────────────────────────────────────────────────────┤
│                   Backend API (FastAPI)                  │
│         Auth · Predictions · Graphs · Alerts · XAI      │
├────────────┬───────────────────────┬────────────────────┤
│  AI Module │    Graph Module       │  Database Layer     │
│  PyTorch   │  NetworkX · Neo4j    │  SQLite · Neo4j     │
│  PyG       │  Builders · Analytics│  SQLAlchemy          │
├────────────┴───────────────────────┴────────────────────┤
│                  CERT r4.2 Dataset                      │
│        logon · device · email · http · file · LDAP      │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React, TypeScript, Vite, TailwindCSS, Shadcn UI, Cytoscape.js |
| **Backend** | FastAPI, Pydantic, SQLAlchemy, Loguru |
| **AI/ML** | PyTorch, PyTorch Geometric, scikit-learn, NumPy, Pandas |
| **Graph** | NetworkX, Neo4j, DGL (optional) |
| **Auth** | JWT, OAuth2, passlib |
| **Visualization** | Plotly, Matplotlib, Cytoscape.js |
| **Config** | Hydra, YAML |
| **Deployment** | Docker, Docker Compose, Nginx, GitHub Actions |
| **Testing** | PyTest, httpx |

## 📁 Project Structure

```
InsiderThreat/
├── backend/          # FastAPI backend (Clean Architecture)
├── frontend/         # React + TypeScript frontend
├── ai/               # THGNN model, training, inference, XAI
├── graph/            # Graph construction, analytics, export
├── configs/          # Hydra YAML configurations
├── dataset/          # Dataset metadata & processed data
├── r4.2/             # Raw CERT r4.2 dataset (not tracked)
├── tests/            # PyTest test suite
├── deployment/       # Docker, Nginx, Compose
├── docs/             # Documentation
├── scripts/          # Utility scripts
├── notebooks/        # Jupyter notebooks
├── logs/             # Application logs (not tracked)
└── reports/          # Generated reports (not tracked)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose (optional)

### Development Setup

```bash
# Clone
git clone https://github.com/your-org/insider-threat-detection.git
cd InsiderThreat

# Python setup
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e ".[dev]"

# Frontend setup
cd frontend && npm install && cd ..

# Configuration
cp .env.example .env
# Edit .env with your settings

# Run
make test        # Verify setup
make docker-up   # Start full stack with Docker
```

### Docker Deployment

```bash
docker-compose -f deployment/docker-compose.yml up -d --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost |
| Backend API | http://localhost:8000/api/docs |
| Neo4j Browser | http://localhost:7474 |

## 🧪 Testing

```bash
make test              # All tests
make test-unit         # Unit tests only
make test-integration  # Integration tests only
```

## 📖 Documentation

- [Architecture Overview](docs/architecture/system_overview.md)
- [Developer Setup Guide](docs/developer/setup_guide.md)
- [Coding Standards](docs/developer/coding_standards.md)
- [API Reference](docs/api/api_reference.md)
- [Dataset Guide](docs/dataset/dataset_guide.md)
- [Deployment Guide](docs/deployment/deployment_guide.md)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## 📊 Development Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Architecture Scaffold | ✅ Complete |
| 1 | Data Pipeline & Database | 🔲 Planned |
| 2 | Backend API & Auth | 🔲 Planned |
| 3 | Graph Construction | 🔲 Planned |
| 4 | THGNN Model | 🔲 Planned |
| 5 | Training Pipeline | 🔲 Planned |
| 6 | Inference & Evaluation | 🔲 Planned |
| 7 | XAI & Visualization | 🔲 Planned |
| 8 | Frontend Dashboard | 🔲 Planned |
| 9 | Integration & Deployment | 🔲 Planned |
