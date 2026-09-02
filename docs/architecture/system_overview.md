# System Architecture Overview

## High-Level Architecture

The Insider Threat Detection System follows a **Clean Architecture** pattern with
clear separation between presentation, business logic, and data access layers.

```
┌────────────────────────────────────────────────────────┐
│                    Frontend (React)                     │
│              Dashboard · Graph Viewer · Reports         │
├────────────────────────────────────────────────────────┤
│                   Nginx Reverse Proxy                   │
├────────────────────────────────────────────────────────┤
│                  Backend API (FastAPI)                   │
│        Auth · Predictions · Graphs · Alerts · Reports   │
├─────────────┬──────────────────────┬──────────────────┤
│  AI Module  │    Graph Module      │  Database Layer   │
│  (PyTorch)  │  (NetworkX/Neo4j)    │ (SQLite/Neo4j)    │
│  THGNN      │  Builders/Analytics  │ SQLAlchemy        │
├─────────────┴──────────────────────┴──────────────────┤
│               CERT r4.2 Dataset                         │
│     logon · device · email · http · file · LDAP         │
└────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Technology | Responsibility |
|-----------|-----------|----------------|
| Frontend | React, TypeScript, Vite | User interface, visualization |
| Backend | FastAPI, Pydantic | REST API, business logic |
| AI Module | PyTorch, PyG | THGNN model training & inference |
| Graph Module | NetworkX, Neo4j | Graph construction & analytics |
| Database | SQLite (dev), Neo4j | Data persistence |
| Config | Hydra, YAML | Configuration management |
| Deployment | Docker, Nginx | Containerization, reverse proxy |

## Data Flow

1. Raw enterprise logs (CERT r4.2) → Feature Engineering
2. Features → Graph Construction (heterogeneous temporal graph)
3. Graph → THGNN Model Training
4. Trained Model → Real-time Inference
5. Predictions → Explainability Module → Dashboard

TODO: Add detailed component diagrams per module.
