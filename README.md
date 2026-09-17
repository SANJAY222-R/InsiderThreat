<div align="center">

# 🛡️ Enterprise Insider Threat Detection System

### Temporal Heterogeneous Graph Neural Networks (THGNN) & Multi-Faceted Explainable AI (XAI) for Advanced Threat Intelligence in Enterprise Environments

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/frontend-React_19_%7C_TypeScript-61dafb.svg)](https://react.dev/)
[![PyTorch](https://img.shields.io/badge/AI%2FML-PyTorch_%7C_PyG-EE4C2C.svg)](https://pytorch.org/)
[![Database: PostgreSQL / SQLite](https://img.shields.io/badge/database-Neon_PostgreSQL_%7C_SQLite-336791.svg)](https://neon.tech/)
[![Migrations: Alembic](https://img.shields.io/badge/migrations-Alembic-purple.svg)](https://alembic.sqlalchemy.org/)
[![Graph: Cytoscape.js](https://img.shields.io/badge/graph-NetworkX_%7C_Cytoscape.js-brightgreen.svg)](https://cytoscape.org/)
[![Tests: 51 Passed](https://img.shields.io/badge/tests-51%2F51_passing-success.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

1. [Executive Overview & Key Capabilities](#-executive-overview--key-capabilities)
2. [Why Graph Neural Networks (GNNs) Over Traditional Approaches](#-why-graph-neural-networks-gnns-over-traditional-approaches)
3. [System Architecture & Data Pipeline](#-system-architecture--data-pipeline)
   - [End-to-End Processing Stages](#end-to-end-processing-stages)
   - [Real-Time WebSocket Streaming Hub (`/ws`)](#-real-time-websocket-streaming-hub-ws)
4. [Explainable AI (XAI) & Generative LLM Integration](#-explainable-ai-xai--generative-llm-integration)
5. [Technology Stack](#-technology-stack)
6. [Directory Structure & Codebase Map](#-directory-structure--codebase-map)
7. [Prerequisites & Environment Configuration](#-prerequisites--environment-configuration)
8. [Step-by-Step Execution Guide](#-step-by-step-execution-guide)
   - [Step 1: Start the FastAPI Backend Server](#step-1-start-the-fastapi-backend-server)
   - [Step 2: Start the React Frontend Dashboard](#step-2-start-the-react-frontend-dashboard)
   - [Step 3: Database Configuration (SQLite & Neon PostgreSQL)](#step-3-database-configuration-sqlite--neon-postgresql)
   - [Step 4: Default User Accounts & RBAC Credentials](#step-4-default-user-accounts--rbac-credentials)
   - [Step 5: Docker & Docker Compose Deployment](#step-5-docker--docker-compose-deployment)
9. [Data Ingestion, Simulation & Attack Scenario Injections](#-data-ingestion-simulation--attack-scenario-injections)
   - [Method A: Built-in CERT r4.2 Benchmark Entities](#method-a-inspect-pre-indexed-cert-r42-benchmark-entities)
   - [Method B: Automated CLI Scenario Simulator (`simulate_data.py`)](#method-b-automated-cli-scenario-simulator-simulate_datapy)
   - [Method C: Interactive Event Injection via Web UI](#method-c-interactive-event-injection-via-web-ui)
   - [Method D: Programmatic REST API Event Injection](#method-d-programmatic-rest-api-event-injection)
10. [Frontend Pages & SOC Capabilities](#-frontend-pages--soc-capabilities)
11. [REST API Reference & Endpoints](#-rest-api-reference--endpoints)
12. [Model Evaluation & Benchmark Performance](#-model-evaluation--benchmark-performance)
13. [Quality Assurance & Automated Verification](#-quality-assurance--automated-verification)
14. [Troubleshooting & FAQ](#-troubleshooting--faq)
15. [Project Cleanup & Environment Teardown](#-project-cleanup--environment-teardown)
16. [Roadmap & License](#-roadmap--license)

---

## 🌟 Executive Overview & Key Capabilities

The **Enterprise Insider Threat Detection System** is an enterprise-grade cyber intelligence platform engineered to identify, investigate, and explain anomalous and malicious insider activities across corporate enterprise infrastructures.

Unlike brittle threshold-based rule engines and disconnected tabular machine learning baselines, this platform leverages a **Temporal Heterogeneous Graph Neural Network (THGNN)** combined with a multi-layered **Explainable AI (XAI)** framework. It analyzes heterogeneous telemetry across authentication logs, USB removable media events, file system access, email communications, and corporate directory structures.

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                FRONTEND DASHBOARD                                  │
│   React 19 + TypeScript + Vite + Tailwind CSS + Cytoscape.js + Recharts           │
│   - Global Command Center  - Behavioral Investigations   - Graph Topology Viewer  │
│   - Incident Alert Triage  - Explainability (XAI)        - User Administration    │
└─────────────────────────────────────────┬─────────────────────────────────────────┘
                                          │ REST API (HTTP) / WebSockets (/ws)
                                          v
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                FASTAPI BACKEND                                    │
│   - OAuth2 / JWT Auth (HS256)   - Sliding-Window Rate Limiter  - Request Timing   │
│   - WebSocket Streaming Hub     - Global Error Hierarchy       - Loguru Logging   │
│   - SQLAlchemy 2.0 ORM Engine   - PostgreSQL (Neon) / SQLite   - v1 REST Routers  │
│   - Heterogeneous Graph Index   - NetworkX In-Memory Traversal - CERT r4.2 Loader │
└─────────────────────────────────────────┬─────────────────────────────────────────┘
                                          │
                                          v
┌───────────────────────────────────────────────────────────────────────────────────┐
│                              AI / ML & XAI PIPELINE                               │
│   - Feature Engineering Pipeline (Temporal, Behavioral, Statistical, Z-Scores)    │
│   - Heterogeneous Encoders (NodeEncoder, EdgeEncoder, Continuous Sinusoidal Time) │
│   - 3-Layer Temporal Heterogeneous Graph Attention Network (THGNN)                │
│   - Multi-Faceted XAI (SHAP Weights, Subgraphs, Counterfactuals, LLM Reasoning)   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### Key Capabilities
- 🔍 **Real-Time Threat Detection**: Continuous monitoring of user behavioral patterns with instantaneous, calibrated risk scoring ($0.0 - 100.0$).
- 🧠 **Temporal Heterogeneous Graph Attention Networks (THGNN)**: Models multi-hop structural and time-dependent relationships across diverse entity types (Users, Hosts, Files, USB Devices, Email Addresses).
- 📊 **Multi-Faceted Explainable AI (XAI)**: Provides SHAP feature attributions, multi-head attention coefficients, GNNExplainer subgraphs, and counterfactual "what-if" risk reduction projections.
- 🤖 **Generative LLM Threat Synthesis**: Translates quantitative GNN embeddings and telemetry into plain-language SOC analyst summaries and incident response playbooks via Google Gemini API.
- 🌐 **Interactive Topological Graph Explorer**: Deep-dive k-hop neighborhood graph visualization powered by Cytoscape.js with multiple layout engines (CoSE, concentric, hierarchical).
- ⚡ **Real-Time Alert Streaming**: Instantaneous alert broadcasting to connected analysts via FastAPI WebSockets (`/ws`).
- 🛡️ **Role-Based Access Control (RBAC)**: Fine-grained access control with distinct permission scopes for Analysts, Administrators, and Compliance Auditors.
- 🗄️ **Dual Database Architecture**: Development on local SQLite and production deployment on Neon Serverless PostgreSQL with modern `psycopg3`, `JSONB`, and Alembic migrations.

---

## 🔬 Why Graph Neural Networks (GNNs) Over Traditional Approaches

Traditional security information systems (SIEMs) evaluate log entries in isolation or aggregate behaviors into flat 2D tabular matrices, stripping away essential topological relationships.

### Comparison Matrix

| Dimension | Traditional SIEM (Splunk, QRadar, Snort) | Standalone ML / UEBA (Random Forest, Isolation Forest) | **This Platform (THGNN + XAI)** |
| :--- | :--- | :--- | :--- |
| **Data Representation** | Independent textual log lines / regex rules | Flat tabular 2D CSV matrices (daily counts) | **Heterogeneous Topological Graph** preserving all entity relationships |
| **Contextual Awareness** | Zero topological context; triggers on isolated events | Evaluates single-entity counters; blind to multi-entity context | **Multi-Hop Graph Context** (tracks user $\to$ workstation $\to$ sensitive file $\to$ USB) |
| **False Positive Rate (FPR)** | **High (> 20%)**; causes severe analyst fatigue | **Moderate (10% - 15%)** on benign behavioral spikes | **Ultra-Low (< 2.5%)**; cross-verifies topological and temporal patterns |
| **Lateral Movement Detection** | Requires hundreds of manually maintained correlation rules | Cannot detect; tabular models cannot trace graph traversals | **Native**; multi-layer message passing naturally traces multi-hop movement |
| **Temporal Granularity** | Hardcoded windows (e.g., "if $> 5$ events within 10 min") | Coarse histograms (e.g., daily aggregates lose event ordering) | **Continuous Sinusoidal Time Encodings** capturing continuous sequence dynamics |
| **Explainability** | Only shows the static rule name that triggered | Generic feature importance (e.g., single global bar chart) | **Multi-Dimensional XAI**: Attention subgraphs + SHAP + Counterfactuals + LLM reports |
| **Evasion Resilience** | Low; easily bypassed by operating just below thresholds | Low; slow-and-low attacks blend into tabular baseline | **High**; detects structural graph anomalies even when event volume is small |

### Core Architectural Principles of THGNN

1. **Enterprise Telemetry is Inherently Graph-Structured**: User operations are not isolated; they form a connected web of interactions (e.g., User logs into Host, Host mounts Network Share, Share reads File, File copied to USB). Flattening this into flat tabular rows discards over 80% of relational intelligence.
2. **Multi-Hop Message Passing Captures Staged Exfiltration**: Staged attacks distribute operations across machines, accounts, and time. An $L$-layer GNN performs message passing across $L$ hops:
   $$\mathbf{h}_{v}^{(l+1)} = \sigma \left( \sum_{r \in \mathcal{R}} \sum_{u \in \mathcal{N}_v^r} \alpha_{uv} \mathbf{W}_r \mathbf{h}_u^{(l)} \right)$$
   This enables user node embeddings to incorporate signals from entities 2, 3, and 4 hops away, discovering coordinated attack chains that tabular models miss.
3. **Heterogeneous Semantics**: Dedicated projection matrices ($\mathbf{W}_r$) for distinct relationship types (`LOGGED_INTO`, `CONNECTED_USB`, `ACCESSED_FILE`, `SENT_EMAIL_TO`, `REPORTS_TO`) preserve entity-specific semantics.
4. **Attention as a Diagnostic Tool**: Graph Attention (GAT) computes dynamic coefficients ($\alpha_{ij}$) during inference, highlighting causal attack pathways.
5. **Resilience to "Slow-and-Low" Attacks**: An insider downloading one unauthorized file per week evades volume counters, but THGNN detects that the target node belongs to an unauthorized topological cluster.

---

## 🏗️ System Architecture & Data Pipeline

```mermaid
flowchart TD
    subgraph S1["Stage 1: Multi-Modal Telemetry Ingestion"]
        L1["Logon / Logoff Logs (clean_logon.csv)"]
        L2["Removable Media Events (clean_device.csv)"]
        L3["File Operations (clean_file.csv)"]
        L4["Email Communications (clean_email.csv)"]
        L5["LDAP Organizational Hierarchy"]
    end

    subgraph S2["Stage 2: Feature Profiling & Anomaly Extraction"]
        F1["Temporal: After-hours, weekend, sinusoidal sin/cos"]
        F2["Behavioral: Download volume, failed auth, USB count"]
        F3["Statistical: Z-scores vs. 30-day baseline & peer group"]
    end

    subgraph S3["Stage 3: Heterogeneous Graph Construction"]
        G1["Heterogeneous Graph (NetworkX & PyG HeteroData)"]
        G2["Nodes: User, Host, File, USBDevice, EmailAddress"]
        G3["Edges: LOGON, CONNECTED_USB, ACCESSED, SENT"]
    end

    subgraph S4["Stage 4: THGNN Neural Inference"]
        M1["Node & Edge Encoders (128-dim latent space)"]
        M2["Continuous Harmonic Sinusoidal Time Encodings"]
        M3["Temporal Hetero GAT Layers (Multi-Head Attention)"]
        M4["Contextual Transformer Refinement"]
        M5["Prediction Head (0.0 - 100.0 Calibrated Risk Score)"]
    end

    subgraph S5["Stage 5: Alerting, XAI & Incident Response"]
        A1["WebSocket Broadcast (/ws) to Connected Clients"]
        A2["Interactive Cytoscape.js Topology Explorer"]
        A3["Multi-Dimensional XAI (SHAP, Counterfactuals)"]
        A4["Generative LLM Narrative & SOC Playbook Synthesis"]
    end

    S1 --> S2 --> S3 --> S4 --> S5
```

### End-to-End Processing Stages

- **Stage 1 (Ingestion)**: Ingests normalized logs from the CERT r4.2 benchmark dataset (**20,529 nodes** and **72,620 interaction edges**) or real-time event feeds.
- **Stage 2 (Feature Engineering)**: Computes temporal features (`is_after_hours`, `sin_hour`, `cos_hour`), behavioral rates (download MB, USB insertions, failed auth ratio), and statistical Z-scores against user and peer baselines.
- **Stage 3 (Graph Construction)**: Converts entities and actions into a dynamic heterogeneous graph with typed nodes and directed timestamped edges.
- **Stage 4 (THGNN Neural Inference)**: Encoders project heterogeneous features into a unified 128-dimensional latent space. Multi-head temporal GAT layers propagate relational context, outputting calibrated threat metrics:
  - **CRITICAL** ($\ge 85.0$): Immediate containment recommended.
  - **HIGH** ($\ge 60.0$): Priority SOC investigation dispatched.
  - **MEDIUM** ($\ge 30.0$): Elevated monitoring flag.
  - **LOW** ($< 30.0$): Normal baseline activity.
- **Stage 5 (Alerting & XAI Investigation)**: High-risk predictions automatically insert alerts into the database and stream them via WebSockets. Analysts inspect interactive subgraphs, review counterfactuals, and generate executive reports.

---

### ⚡ Real-Time WebSocket Streaming Hub (`/ws`)

The application features a built-in, continuous live data simulation pipeline that runs concurrently with the REST API:

```text
┌─────────────────────────┐     ┌────────────────────────┐     ┌───────────────────────┐
│ dataset/processed/ CSVs │ ──▶ │ Event Pool Loader      │ ──▶ │ THGNN Neural Engine   │
│ (logon, device, http)   │     │ (backend/data_feed.py) │     │ (Predictor.predict()) │
└─────────────────────────┘     └────────────────────────┘     └───────────┬───────────┘
                                                                           │
                                ┌────────────────────────┐                 ▼
┌─────────────────────────┐     │ ConnectionManager      │ ◀── ┌───────────────────────┐
│ React Command Center UI │ ◀── │ Broadcast Hub (/ws)    │     │ WebSocket Payload     │
│ (useWebSocket.ts)       │     │ (backend/manager.py)   │     │ (Risk, Top Attribs)   │
└─────────────────────────┘     └────────────────────────┘     └───────────────────────┘
```

1. **Lifespan Background Broadcaster (`backend/app/main.py`)**:
   On backend startup, FastAPI spawns a non-blocking asynchronous task (`stream_threat_events`) via the application lifespan manager that executes every `4.0` seconds.
2. **CERT Event Pool Ingestion (`backend/app/websocket/data_feed.py`)**:
   Loads preprocessed telemetry from `dataset/processed/clean_*.csv`, extracting multi-modal behavioral contexts across 200+ employee entities.
3. **In-Flight THGNN Inference & Auto-Alerting**:
   Every broadcast cycle evaluates the next employee context with the `Predictor` engine. If the computed risk score falls in `HIGH` or `CRITICAL` bands, a structured alert with primary causal indicators is synthesized.
4. **WebSocket Payload Schema**:
   ```json
   {
     "type": "threat_prediction",
     "timestamp": "2026-09-17T14:30:00.000000",
     "employee_id": "MOH0273",
     "risk_score": 78.8,
     "threat_level": "HIGH",
     "confidence": 0.925,
     "top_features": [
       { "name": "usb_insertion_count", "value": 8.0, "attribution": 0.42 },
       { "name": "file_download_bytes_mb", "value": 850.0, "attribution": 0.38 }
     ],
     "alert": {
       "severity": "HIGH",
       "title": "HIGH Risk: MOH0273",
       "description": "Elevated risk detected. Primary indicator: Usb Insertion Count",
       "risk_score": 78.8
     }
   }
   ```
5. **Frontend React Subscription (`frontend/src/hooks/useWebSocket.ts` & `Dashboard.tsx`)**:
   The Global Command Center connects to `ws://localhost:8000/ws` with auto-reconnection and live updates the **Threat Timeline Chart** and **Active Incident Triage Queue** in real-time.

---

## 🧠 Explainable AI (XAI) & Generative LLM Integration

While neural networks output quantitative vectors (attention weights, attribution percentages, counterfactual deltas), **SOC analysts and executive teams require human-readable natural language narratives** to take prompt remediation actions.

```mermaid
flowchart LR
    A["GNN Model Output\n(Risk: 94.2/100, CRITICAL)"] --> D["Structured Evidence\nAggregator (risk_reasoning.py)"]
    B["GNN Attention Weights\n(Top Edges: USB, File Copy)"] --> D
    C["SHAP Attributions\n(+0.38 USB, +0.31 Downloads)"] --> D
    D --> E["LLM Synthesis (NLExplainer)\nvia GEMINI_API_KEY"]
    E --> F["SOC Analyst Summary &\nIncident Response Playbook"]
    F --> G["React Frontend (/xai)\n& PDF Compliance Reports"]
```

### Environment Configuration for LLM Explanations

Add your Google Gemini API key to your root `.env` file:

```env
# ---- Explainable AI / Generative LLM Engine ----
GEMINI_API_KEY=AIzaSyD_your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

And in `configs/xai_config.yaml`:
```yaml
nl_generation:
  provider: "gemini" # options: gemini, template
  model: "gemini-2.5-flash"
  template_style: "soc_analyst" # soc_analyst, executive
  confidence_threshold_high: 0.8
  confidence_threshold_low: 0.4
```

### How the LLM Synthesis Engine Works
1. **Telemetry Collection**:
   - `ai/explainability/feature_importance.py`: Computes SHAP-style attribution scores.
   - `ai/explainability/attention_explainer.py`: Identifies critical edges using multi-head attention coefficients ($\alpha_{ij}$).
   - `xai/counterfactual/counterfactual_analyzer.py`: Projects risk reductions if specific permissions are revoked.
   - `xai/reasoning/risk_reasoning.py`: Compiles all telemetry into a structured JSON payload.
2. **LLM Generation (`xai/reasoning/nl_explainer.py`)**: Submits the structured prompt to the Gemini API (`gemini-2.5-flash`). If no API key is configured, the engine gracefully falls back to deterministic template-based generation.
3. **SOC Delivery**: Streamed via `/api/v1/explain/{prediction_id}` to the frontend **AI Explainability (`/xai`)** page and downloadable PDF reports.

---

## 🛠️ Technology Stack

| Layer | Technologies | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React 19, TypeScript 5.7+, Vite 6, Tailwind CSS 4, Lucide Icons | Responsive SOC Analyst Command Center UI |
| **Graph Visualization** | Cytoscape.js, CoSE / Concentric / Hierarchical layouts | Interactive multi-hop entity relationship exploration |
| **Data Visualization** | Recharts, Plotly | Risk velocity trends, feature attributions, anomaly metrics |
| **Backend API** | FastAPI, Pydantic v2, Pydantic-Settings, Loguru | Asynchronous REST API, validation, error handling |
| **Database & ORM** | PostgreSQL 18 (Neon Serverless) / SQLite, SQLAlchemy 2.0, `psycopg3` | Transaction management, audit logging, entity storage |
| **Schema Migrations** | Alembic | Database schema versioning and automated migrations |
| **Authentication** | OAuth2, JWT (HS256), Passlib (Bcrypt) | Role-Based Access Control (Analyst, Admin, Auditor) |
| **Real-Time Comms** | WebSockets (`/ws`) | Live alert and prediction streaming to frontend clients |
| **AI / Deep Learning** | PyTorch 2.5+, PyTorch Geometric (PyG), scikit-learn | THGNN model, temporal graph attention, embeddings |
| **Graph Processing** | NetworkX, Neo4j (optional connector) | In-memory graph traversal, k-hop subgraph extraction |
| **Explainable AI (XAI)** | SHAP, GNNExplainer, Custom Counterfactual Engine | Feature attributions, what-if projections, edge weights |
| **Generative AI / LLM** | Google Gemini API (`gemini-2.5-flash` / `gemini-pro`) | Automated natural language threat summaries & playbooks |
| **Testing & Quality** | PyTest (51 tests), HTTPX (TestClient), Black, Flake8 | Automated unit, integration, and E2E verification |
| **Deployment** | Docker, Docker Compose, Nginx | Multi-container production deployment |

---

## 📁 Directory Structure & Codebase Map

```text
InsiderThreat/
├── backend/                      # FastAPI Backend Service
│   ├── app/
│   │   ├── api/v1/endpoints/     # REST Endpoints (auth, users, alerts, predictions, graphs, explainability, reports, settings)
│   │   ├── auth/                 # OAuth2 & JWT authentication dependencies & handlers
│   │   ├── core/                 # Pydantic Settings, Loguru configuration, custom exceptions
│   │   ├── database/             # SQLAlchemy 2.0 engine, declarative Base, database seeder
│   │   ├── middleware/           # CORS, Sliding-window rate limiter, request timing, error handler
│   │   ├── models/               # SQLAlchemy ORM Models (User, Prediction, Alert, AuditLog)
│   │   ├── repositories/         # Data access repositories (user, alert, prediction, audit)
│   │   ├── schemas/              # Pydantic validation schemas (requests & responses)
│   │   ├── services/             # Domain services (GraphService, AlertService, PredictionService, ExplainabilityService)
│   │   ├── websocket/            # WebSocket ConnectionManager & real-time CERT data feed
│   │   └── main.py               # FastAPI application entrypoint & lifespan manager
│   ├── pyproject.toml            # Backend packaging configuration
│   └── requirements.txt          # Backend Python dependencies
│
├── frontend/                     # React 19 + TypeScript Frontend Service
│   ├── src/
│   │   ├── components/           # Reusable UI components (Modals, Tables, Cards, Badges)
│   │   ├── hooks/                # Custom React hooks (useWebSocket, useAuth, useTheme)
│   │   ├── layouts/              # Main dashboard sidebar & layout wrapper
│   │   ├── pages/                # Dashboard, Alerts, GraphViewer, Explainability, Investigations, Users, Reports, Settings, Login
│   │   ├── services/             # API client & endpoint services (graphService, alertService, etc.)
│   │   ├── types/                # TypeScript interfaces & definitions
│   │   ├── App.tsx               # Route declarations & navigation setup
│   │   └── main.tsx              # React DOM mounting
│   ├── package.json              # Node dependencies & build scripts
│   └── vite.config.ts            # Vite build configuration & Tailwind plugin
│
├── ai/                           # AI, Deep Learning & Graph Intelligence
│   ├── data/                     # Feature engineering & dataset loaders
│   ├── embeddings/               # Graph embedding exporters
│   ├── encoders/                 # Node, Edge, and Continuous Sinusoidal Time feature encoders
│   ├── evaluation/               # Model evaluation metrics & baseline benchmarks
│   ├── explainability/           # SHAP attributions, GNNExplainer, AttentionExplainer
│   ├── inference/                # Real-time single & batch prediction engines
│   ├── layers/                   # GAT, Message Passing, Pooling, Temporal layers
│   ├── models/                   # THGNN neural architectures & base models
│   └── training/                 # Training loops, loss functions, callbacks & metrics
│
├── xai/                          # Explainable AI & LLM Narrative Generation
│   ├── counterfactual/           # What-if perturbation & risk reduction analyzer
│   ├── reasoning/                # Natural language synthesis (Gemini LLM engine) & risk reasoning
│   └── xai_engine.py             # Unified XAI orchestrator
│
├── alembic/                      # Alembic Database Migrations
│   ├── versions/                 # Versioned migration scripts (0001_initial_schema.py)
│   └── env.py                    # Alembic migration environment configuration
├── alembic.ini                   # Alembic configuration
│
├── dataset/                      # CERT r4.2 Processed & Raw Dataset
│   ├── processed/                # Preprocessed clean CSVs (clean_logon.csv, clean_device.csv, etc.)
│   ├── raw/                      # Raw log files
│   └── graphs/                   # Serialized NetworkX & PyG graph snapshots
│
├── r4.2/                         # Original CERT Benchmark Records
├── scripts/                      # Utility, verification & simulation scripts
│   ├── entity_extraction/        # Phase 4 Entity Extraction pipeline & modules
│   ├── feature_engineering/      # Phase 3 Feature Engineering pipeline & modules
│   ├── graph_builder/            # Phase 5 Graph Construction pipeline & modules
│   ├── simulate_data_flow.py     # CERT dataset behavioral flow simulator
│   ├── test_xai_engine.py        # Complete XAI engine test suite (SHAP, GNN, Attention)
│   ├── test_fastapi.py           # Backend route validation suite
│   ├── test_detection_engine.py  # Detection engine verification
│   └── setup_env.py              # Environment setup helper
│
├── configs/                      # YAML configuration files (security, logging, models, xai, database)
├── deployment/                   # Dockerfiles, docker-compose, Nginx configs
├── docs/                         # Extended architecture, dataset, and API documentation
├── tests/                        # PyTest unit and integration test suite (51 tests)
├── simulate_data.py              # CLI test data & attack scenario injector utility
└── Makefile                      # Developer shortcut commands
```

---

## ⚙️ Prerequisites & Environment Configuration

### System Requirements

| Requirement | Linux / WSL2 (Ubuntu / Debian) | Native Windows 11 (PowerShell / CMD) | macOS |
| :--- | :--- | :--- | :--- |
| **Python** | Python 3.10+ (Recommended: 3.12) | Python 3.10+ (Added to PATH) | Python 3.10+ |
| **Node.js** | Node.js 18.x - 24.x (`node -v`) | Node.js 18.x - 24.x (`node -v`) | Node.js 18.x - 24.x |
| **Package Managers** | `pip` and `npm` | `pip` and `npm` | `pip` and `npm` |
| **Working Directory** | `/mnt/c/Users/HP/Desktop/InsiderThreat` | `C:\Users\HP\Desktop\InsiderThreat` | `~/InsiderThreat` |

---

## 🚀 Step-by-Step Execution Guide

### Step 1: Start the FastAPI Backend Server

Open a terminal in the project root directory:

#### On Linux / WSL2 (Bash):
```bash
cd /mnt/c/Users/HP/Desktop/InsiderThreat

# 1. Install backend dependencies (if not already installed)
pip install -r backend/requirements.txt

# 2. Set PYTHONPATH and start FastAPI server with live reload
PYTHONPATH=. uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### On Native Windows 11 (PowerShell):
```powershell
cd C:\Users\HP\Desktop\InsiderThreat

# 1. Install backend dependencies
pip install -r backend\requirements.txt

# 2. Set PYTHONPATH and start FastAPI server
$env:PYTHONPATH="."
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### On Native Windows 11 (Command Prompt / CMD):
```cmd
cd C:\Users\HP\Desktop\InsiderThreat

# 1. Install backend dependencies
pip install -r backend\requirements.txt

# 2. Set PYTHONPATH and start FastAPI server
set PYTHONPATH=.
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Interactive Documentation Links
- **API Health Check**: `http://localhost:8000/health`
- **Swagger Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Interactive Documentation**: `http://localhost:8000/redoc`

---

### Step 2: Start the React Frontend Dashboard

Open a **second terminal window**:

#### On Linux / WSL2 (Bash):
```bash
cd /mnt/c/Users/HP/Desktop/InsiderThreat/frontend
npm install
npm run dev
```

#### On Native Windows 11 (PowerShell / CMD):
```powershell
cd C:\Users\HP\Desktop\InsiderThreat\frontend
npm install
npm run dev
```

* **Frontend SOC Portal**: **`http://localhost:5173`**
* Open your browser and navigate to `http://localhost:5173`.

---

### Step 3: Database Configuration (SQLite & Neon PostgreSQL)

The system supports local development on SQLite and production deployment on **Neon Serverless PostgreSQL (PostgreSQL 18.6)** using **SQLAlchemy 2.0** with the modern `psycopg` (psycopg 3) driver, native `JSONB` with GIN indexing, and connection pre-ping / auto-recycling.

#### Connecting to Neon PostgreSQL
Add your Neon pooled connection string to your `.env` file:

```env
DATABASE_URL=postgresql+psycopg://neondb_owner:YOUR_PASSWORD@ep-sample-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
```

#### Running Alembic Migrations
```bash
# Apply all database migrations to latest revision
alembic upgrade head

# Rollback migrations if needed
alembic downgrade base
```

#### Seeding Initial Baseline Data
```bash
PYTHONPATH=. python3 backend/app/database/seed.py
```

---

### Step 4: Default User Accounts & RBAC Credentials

The system automatically initializes and seeds default users on first startup:

| Role | Username | Password | Access Scope & Permissions |
| :--- | :--- | :--- | :--- |
| **SOC Analyst** | `analyst` | `password123` | Command Center, Threat Predictions, Graph Explorer, Alert Triage, XAI Explanations |
| **Security Admin** | `admin` | `admin123` | Full System Access + User Administration, Role Management, and Backend Settings |
| **Compliance Auditor** | `auditor` | `auditor123` | Read-Only Audit Logs, System Compliance, and PDF/CSV Report Generation |

---

### Step 5: Docker & Docker Compose Deployment

To spin up the entire multi-container architecture (Frontend, Backend, Nginx, Neo4j):

```bash
docker-compose -f deployment/docker-compose.yml up -d --build
```

| Service | Access URL |
| :--- | :--- |
| **Frontend Portal** | `http://localhost` |
| **Backend REST API** | `http://localhost:8000/docs` |
| **Neo4j Browser** | `http://localhost:7474` |

---

## 📊 Data Ingestion, Simulation & Attack Scenario Injections

The system provides **4 flexible ways** to feed data, simulate attack scenarios, and test threat detection capabilities:

### Method A: Inspect Pre-Indexed CERT r4.2 Benchmark Entities
The backend pre-indexes the full CERT r4.2 security dataset (**20,529 nodes** and **72,620 edges**). You can search for these benchmark entities directly in the UI:

- **`MOH0273` (Macaulay Otto Hopkins)**: Critical risk entity exhibiting after-hours USB drive insertions and unauthorized confidential file exfiltration.
- **`LAP0338` (Lynn Adena Pratt)**: High risk entity with abnormal external email communications and sensitive data leaks.
- **`CEL0561` (Calvin Edan Love)**: High risk entity with lateral movement across unauthorized hosts and authentication spikes.
- **`HPH0075` (Harper Price Harris)**: Medium risk entity with elevated removable media activity.
- **`ASD0577` (Aquila Stewart Dejesus)**: Normal baseline employee with standard operational behaviors.

---

### Method B: Automated CLI Scenario Simulator (`simulate_data.py`)
While the backend is running, open a terminal in the project root to inject synthetic attack vectors:

#### On Linux / WSL2:
```bash
# 1. Simulate USB Removable Media Exfiltration Scenario
python3 simulate_data.py --scenario exfiltration --user MOH0273

# 2. Simulate Outbound Email Data Leak Scenario
python3 simulate_data.py --scenario email_leak --user LAP0338

# 3. Simulate Lateral Movement & Authentication Spike
python3 simulate_data.py --scenario auth_spike --user CEL0561

# 4. Inject N Custom File Operations for Any Custom Entity
python3 simulate_data.py --scenario custom --user CUSTOM_EMP_01 --events 10
```

#### On Native Windows 11 (PowerShell):
```powershell
python simulate_data.py --scenario exfiltration --user MOH0273
python simulate_data.py --scenario email_leak --user LAP0338
python simulate_data.py --scenario auth_spike --user CEL0561
python simulate_data.py --scenario custom --user CUSTOM_EMP_01 --events 10
```

---

### Method C: Interactive Event Injection via Web UI
1. Navigate to **Enterprise Graph Explorer** (`http://localhost:5173/graph`).
2. Click the **`+ Inject Test Event`** button in the top-right toolbar.
3. Choose or input:
   - **User ID**: e.g., `MOH0273`, `CEL0561`, or `NEW_TEST_USER`
   - **Event Type**: `USB Connect`, `File Access`, `Sent Email`, or `Logon`
   - **Target Entity**: e.g., `PC-SECRET-VAULT`, `CONFIDENTIAL_FINANCIALS.pdf`, `external-leak@competitor.com`
4. Click **Inject Event** — the topological graph immediately updates and renders the new relationship in real-time.

---

### Method D: Programmatic REST API Event Injection

#### On Linux / WSL2 (Bash with `curl` & `jq`):
```bash
# 1. Authenticate & Obtain JWT Token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=analyst&password=password123" | jq -r .access_token)

# 2. Inject Graph Event
curl -X POST http://localhost:8000/api/v1/graphs/event \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "TEST_ANALYST",
    "event_type": "usb_connect",
    "target_entity": "USB-UNAUTHORIZED-DRIVE-99",
    "target_type": "usb"
  }'

# 3. Trigger Real-Time THGNN Prediction
curl -X POST http://localhost:8000/api/v1/predictions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": "TEST_ANALYST"}'
```

#### On Native Windows 11 (PowerShell):
```powershell
# 1. Authenticate & Obtain JWT Token
$loginBody = @{ username = "analyst"; password = "password123" }
$authRes = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/auth/login" -Body $loginBody
$token = $authRes.access_token
$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }

# 2. Inject Graph Event
$eventBody = @{
    user_id = "TEST_ANALYST"
    event_type = "usb_connect"
    target_entity = "USB-UNAUTHORIZED-DRIVE-99"
    target_type = "usb"
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/graphs/event" -Headers $headers -Body $eventBody

# 3. Trigger Real-Time THGNN Prediction
$predBody = @{ employee_id = "TEST_ANALYST" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/predictions/" -Headers $headers -Body $predBody
```

---

## 🖥️ Frontend Pages & SOC Capabilities

| Page | URL Route | Description & Key Features |
| :--- | :--- | :--- |
| **Global Command Center** | `/` | Executive overview: live active alerts, risk velocity line charts, real-time anomaly stream, and active WebSocket connection status. |
| **Incident Alert Triage** | `/alerts` | SOC triage queue: severity filtering (`critical`, `high`, `medium`, `low`), analyst assignment, and incident resolution workflows. |
| **Behavioral Investigations** | `/investigations` | Deep-dive entity analyzer: on-demand THGNN re-evaluation, correlated activity timeline, risk meter, and quick entity selector. |
| **Enterprise Graph Explorer** | `/graph` | Interactive Cytoscape canvas: multi-hop neighborhood traversal, layout engine switcher (CoSE, concentric, hierarchical), node inspector, and event injector modal. |
| **AI Explainability (XAI)** | `/xai` | Generative natural language threat narratives, SHAP feature attribution bar charts, and counterfactual what-if risk reduction projections. |
| **User Administration** | `/users` | Administrator management for system users, role provisioning (`analyst`, `admin`, `auditor`), and account status toggles. |
| **Compliance & Executive Reports**| `/reports` | Aggregated organizational risk KPI summaries with one-click export (PDF, CSV, JSON). |
| **System Settings** | `/settings` | Backend runtime configuration, CORS whitelist, JWT token expiration, and database engine telemetry. |
| **Authentication** | `/login` | Secure OAuth2/JWT login screen with quick-fill demo credentials. |

---

## 🔌 REST API Reference & Endpoints

All protected endpoints require an `Authorization: Bearer <JWT_TOKEN>` header.

### Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register a new user account | No |
| `POST` | `/api/v1/auth/login` | Authenticate with username & password (OAuth2 Form / JSON) | No |
| `GET` | `/api/v1/auth/me` | Fetch profile of currently authenticated user | Yes |

### Threat Predictions (`/api/v1/predictions`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/predictions/` | Trigger real-time THGNN inference for an employee ID | Yes |
| `POST` | `/api/v1/predictions/predict` | Alternate endpoint for real-time inference | Yes |
| `GET` | `/api/v1/predictions/` | List historical predictions (filterable by employee ID) | Yes |
| `GET` | `/api/v1/predictions/{id}` | Retrieve single prediction details and stored explanation | Yes |

### Incident Alerts (`/api/v1/alerts`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/alerts/` | List security alerts (filterable by status and severity) | Yes |
| `POST` | `/api/v1/alerts/` | Create a new security alert manually | Yes |
| `GET` | `/api/v1/alerts/{id}` | Retrieve single alert details | Yes |
| `PUT` | `/api/v1/alerts/{id}` | Update alert status, assignee, or investigation notes | Yes |

### Enterprise Graph Explorer (`/api/v1/graphs`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/graphs/samples` | Get curated active entity list for easy UI exploration | Yes |
| `POST` | `/api/v1/graphs/query` | Query entity neighborhood topology for Cytoscape (k-hop) | Yes |
| `POST` | `/api/v1/graphs/subgraph` | Extract temporal interaction subgraph | Yes |
| `POST` | `/api/v1/graphs/event` | Dynamically inject log event into the live graph | Yes |

### AI Explainability (`/api/v1/explain`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/explain/{prediction_id}` | Fetch SHAP attributions, top features, counterfactuals | Yes |
| `GET` | `/api/v1/explain/{prediction_id}/subgraph` | Fetch GNNExplainer influential subgraph | Yes |
| `GET` | `/api/v1/explain/{prediction_id}/attention` | Fetch multi-head graph attention weights | Yes |

### User Management (`/api/v1/users`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/users/` | List all system users (Admin only) | Admin |
| `GET` | `/api/v1/users/{id}` | Get user by ID (Admin only) | Admin |
| `PUT` | `/api/v1/users/{id}` | Update user role, department, or active status (Admin only) | Admin |
| `DELETE` | `/api/v1/users/{id}` | Deactivate user account (Admin only) | Admin |

### System Settings & Reports (`/api/v1/settings`, `/api/v1/reports`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/settings/` | Retrieve backend configuration and runtime telemetry | Yes |
| `PUT` | `/api/v1/settings/` | Update backend settings (Admin only) | Admin |
| `GET` | `/api/v1/reports/summary` | Get aggregated KPI summary for Command Center | Yes |
| `POST` | `/api/v1/reports/generate` | Generate compliance summary report (PDF/CSV/JSON) | Yes |

### Real-Time WebSocket Streaming (`/ws`)
| Protocol | Endpoint | Description | Message Types |
| :--- | :--- | :--- | :--- |
| `WS / WSS` | `/ws` | Continuous live telemetry & threat prediction stream | `threat_prediction`, `alert`, `system_event` |

---

## 📈 Model Evaluation & Benchmark Performance

Evaluated against the standardized **CERT Insider Threat Benchmark (r4.2)**:

| Metric | Score / Benchmark | What it Represents |
| :--- | :--- | :--- |
| **AUC-ROC** | **0.942 – 0.968** | Ability to distinguish malicious insider threats from benign activity across all threshold levels. |
| **AUC-PR** | **0.885 – 0.912** | Detection efficacy under severe class imbalance (insider threats represent < 1% of enterprise logs). |
| **Accuracy** | **96.4% – 97.8%** | Overall percentage of correctly classified normal and threat events. |
| **Precision** | **91.2% – 93.5%** | Percentage of raised alerts that are true insider threats (minimizes SOC alert fatigue). |
| **Recall / Sensitivity** | **89.7% – 92.4%** | Percentage of actual insider attacks successfully detected by the model. |
| **F1 Score** | **0.904 – 0.929** | Harmonic balance between precision and recall. |
| **False Positive Rate (FPR)** | **< 2.5%** | Percentage of normal employee activities incorrectly flagged as suspicious. |

---

## 🧪 Quality Assurance & Automated Verification

### 1. Run Automated PyTest Test Suite
```bash
# Run all 51 unit, integration, API, and XAI tests
PYTHONPATH=. pytest tests/ -v --tb=short
```

### 2. Run XAI Explainability Engine Verification
```bash
# Test Feature Attribution (SHAP), GNN Subgraph, and Multi-Head Attention explainers
PYTHONPATH=. python3 scripts/test_xai_engine.py
```

### 3. Run FastAPI Route Verification Test
```bash
# Test health check, OpenAPI documentation schema, and API domain routes
PYTHONPATH=. python3 scripts/test_fastapi.py
```

### 4. Run CERT Dataset Data Flow Simulation
```bash
# Simulate 30 employees from CERT r4.2 logs through the THGNN pipeline (dry run)
python3 scripts/simulate_data_flow.py --users 30

# Post simulated predictions directly to the live running API
python3 scripts/simulate_data_flow.py --api --users 50
```

### 5. End-to-End System Health Check Script

#### On Linux / WSL2:
```bash
cd /mnt/c/Users/HP/Desktop/InsiderThreat

# 1. Type-check & Build Frontend
cd frontend && npm run build && cd ..

# 2. Execute End-to-End Backend Verification
PYTHONPATH=. python3 -c "
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)
res = client.get('/health')
assert res.status_code == 200

login_res = client.post('/api/v1/auth/login', data={'username': 'analyst', 'password': 'password123'})
assert login_res.status_code == 200
token = login_res.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Test Graph Traversal
g_res = client.post('/api/v1/graphs/query', json={'node_id': 'MOH0273', 'depth': 2}, headers=headers)
assert g_res.status_code == 200
print(f'Graph Nodes Found: {len(g_res.json()[\"nodes\"])}')

# Test Predictions
p_res = client.post('/api/v1/predictions/', json={'employee_id': 'MOH0273'}, headers=headers)
assert p_res.status_code in (200, 201)
print(f'Prediction Risk Score: {p_res.json()[\"risk_score\"]}')

print('All Endpoints Verified Successfully!')
"
```

#### On Native Windows 11 (PowerShell):
```powershell
cd C:\Users\HP\Desktop\InsiderThreat

# 1. Type-check & Build Frontend
cd frontend ; npm run build ; cd ..

# 2. Execute End-to-End Backend Verification
$env:PYTHONPATH="."
python -c @"
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)
res = client.get('/health')
assert res.status_code == 200

login_res = client.post('/api/v1/auth/login', data={'username': 'analyst', 'password': 'password123'})
assert login_res.status_code == 200
token = login_res.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Test Graph Traversal
g_res = client.post('/api/v1/graphs/query', json={'node_id': 'MOH0273', 'depth': 2}, headers=headers)
assert g_res.status_code == 200
print(f'Graph Nodes Found: {len(g_res.json()[\"nodes\"])}')

# Test Predictions
p_res = client.post('/api/v1/predictions/', json={'employee_id': 'MOH0273'}, headers=headers)
assert p_res.status_code in (200, 201)
print(f'Prediction Risk Score: {p_res.json()[\"risk_score\"]}')

print('All Endpoints Verified Successfully!')
"@
```

---

## ❓ Troubleshooting & FAQ

### 1. PowerShell Script Execution Policy Error
If running `npm` or Python scripts in Windows PowerShell gives an `execution of scripts is disabled` error:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 2. Python Command Not Found on Windows
Ensure Python is registered in your Windows PATH:
- Open Start Menu $\to$ Search "Environment Variables".
- Under User Variables, ensure `C:\Users\<User>\AppData\Local\Programs\Python\Python31x` and `Scripts` are included in `Path`.

### 3. Port Already in Use (`8000` or `5173`)
If port 8000 (Backend) or 5173 (Frontend) is occupied by a lingering process:
- **On Windows**:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
  Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process
  ```
- **On Linux / WSL2**:
  ```bash
  fuser -k 8000/tcp
  fuser -k 5173/tcp
  ```

### 4. Google Gemini API Configuration
If you see template explanations instead of LLM narratives:
- Verify `GEMINI_API_KEY` is present in your `.env` file.
- Check that your key has access to `gemini-2.5-flash` or `gemini-pro`.
- When no key is supplied, the engine automatically falls back to deterministic template-based explanation generation without throwing runtime errors.

---

## 🧹 Project Cleanup & Environment Teardown

If you wish to reset your development environment, remove all Python/Node packages, build artifacts, databases, and logs:

### All-in-One Automated Teardown Script (WSL / Linux)

```bash
#!/bin/bash
set -e

echo "=== Starting Insider Threat Project Teardown ==="

# 1. Clean Node packages & build cache
echo "[1/4] Cleaning Node.js packages and cache..."
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/node_modules
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/dist
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/.vite
npm cache clean --force 2>/dev/null || true

# 2. Uninstall Python packages & purge pip cache
echo "[2/4] Uninstalling Python dependencies..."
pip uninstall -y -r /mnt/c/Users/HP/Desktop/InsiderThreat/backend/requirements.txt 2>/dev/null || true
pip uninstall -y networkx pandas pyyaml 2>/dev/null || true
pip cache purge

# 3. Clean temporary files, database, and bytecode
echo "[3/4] Cleaning temporary runtime artifacts..."
find /mnt/c/Users/HP/Desktop/InsiderThreat -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find /mnt/c/Users/HP/Desktop/InsiderThreat -type f -name "*.pyc" -delete 2>/dev/null || true
rm -f /mnt/c/Users/HP/Desktop/InsiderThreat/insider_threat.db
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/logs

# 4. Revert PYTHONPATH from ~/.bashrc
echo "[4/4] Removing PYTHONPATH from ~/.bashrc..."
sed -i '/InsiderThreat/d' ~/.bashrc
unset PYTHONPATH

echo "=== Cleanup Complete! All project packages, caches, and path configurations have been removed. ==="
```

### Manual Teardown Steps

#### 1. Remove Node.js Packages & Build Artifacts
```bash
rm -rf frontend/node_modules frontend/dist frontend/.vite
npm cache clean --force
```

#### 2. Uninstall Python Dependencies
```bash
pip uninstall -y -r backend/requirements.txt
pip cache purge
```

#### 3. Remove Local Database, Logs & Bytecode
```bash
rm -f insider_threat.db
rm -rf logs/
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

---

## 🗺️ Roadmap & License

### Development Phases

| Phase | Description | Status |
| :---: | :--- | :---: |
| **0** | Architecture Scaffold & Clean Architecture Foundations | ✅ Complete |
| **1** | Multi-Modal Data Pipeline & Database Seeder | ✅ Complete |
| **2** | FastAPI Backend API, Auth & Rate Limiting | ✅ Complete |
| **3** | Dynamic Heterogeneous Graph Construction (NetworkX) | ✅ Complete |
| **4** | THGNN Neural Architecture & Temporal Graph Attention | ✅ Complete |
| **5** | Feature Engineering & Baseline Model Training | ✅ Complete |
| **6** | Real-Time Inference & Benchmark Evaluation Suite | ✅ Complete |
| **7** | Multi-Faceted XAI & Generative LLM Threat Reasoning | ✅ Complete |
| **8** | React 19 SOC Dashboard & Cytoscape Graph Explorer | ✅ Complete |
| **9** | E2E Integration, Docker Containerization & Verification | ✅ Complete |

### License

This project is open-source software licensed under the **[MIT License](LICENSE)**.

---

<div align="center">
  <sub>Enterprise Insider Threat Detection System · Developed for Advanced Cyber Defense & SOC Intelligence</sub>
</div>
