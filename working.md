# Enterprise Insider Threat Detection System
## Complete System Documentation, Execution Guide & Architecture Workflow

---

## 1. System Overview & Architecture

The **Enterprise Insider Threat Detection System** is a security analytics platform designed to detect, investigate, and mitigate malicious or anomalous insider activities within corporate environments. It utilizes **Temporal Heterogeneous Graph Neural Networks (THGNN)** to analyze multi-modal telemetry across users, hosts, files, removable media (USB), emails, and authentication sessions.

```
+-----------------------------------------------------------------------------------+
|                                FRONTEND DASHBOARD                                  |
|   React 19 + TypeScript + Vite + Tailwind CSS + Cytoscape.js + Recharts + Redux    |
|   - Threat Dashboard       - Behavioral Investigations    - Graph Topology Viewer  |
|   - Incident Alert Triage  - Explainability (XAI)         - User Administration    |
+-----------------------------------------+-----------------------------------------+
                                          | REST API / WebSockets
                                          v
+-----------------------------------------------------------------------------------+
|                                FASTAPI BACKEND                                    |
|   - OAuth2 / JWT Auth (HS256)   - Sliding-Window Rate Limiter  - Request Timing   |
|   - WebSocket Streaming Hub     - Global Error Hierarchy       - Loguru Logging   |
|   - SQLAlchemy 2.0 ORM Engine   - SQLite / PostgreSQL DB       - v1 REST Routers  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                              AI / ML & XAI PIPELINE                               |
|   - Feature Engineering Pipeline (Temporal, Behavioral, Statistical, Z-Scores)    |
|   - Heterogeneous Encoders (NodeEncoder, EdgeEncoder, TemporalEncoder)            |
|   - THGNN Inference Engine & Real-Time Risk Scorer (0 - 100 Scale)                |
|   - Explainability Engine (SHAP Attributions, GNNExplainer, Attention Weights)    |
|   - Model Evaluation & Baseline Benchmarking Suite                                |
+-----------------------------------------------------------------------------------+
```

---

## 2. Directory Structure

```text
InsiderThreat/
├── backend/                      # FastAPI Backend Service
│   ├── app/
│   │   ├── api/v1/endpoints/     # REST Endpoints (auth, users, alerts, predictions, graphs, xai, reports)
│   │   ├── auth/                 # OAuth2 & JWT handlers
│   │   ├── core/                 # App config (Pydantic Settings), logging, exceptions
│   │   ├── database/             # SQLAlchemy DB engine & Base
│   │   ├── middleware/           # CORS, Rate Limiting, Request Logging, Auth
│   │   ├── models/               # SQLAlchemy ORM Models (User, Prediction, Alert, AuditLog)
│   │   ├── schemas/              # Pydantic validation schemas
│   │   ├── services/             # Business logic service layer
│   │   ├── websocket/            # Real-time WebSocket connection manager
│   │   └── main.py               # FastAPI Application Entrypoint
│   └── requirements.txt          # Backend Python dependencies
│
├── frontend/                     # React + TypeScript Frontend Service
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── layouts/              # Main dashboard sidebar & layout wrapper
│   │   ├── pages/                # Dashboard, Alerts, GraphViewer, Explainability, Investigations, Users, Reports, Settings, Login
│   │   ├── services/             # Axios/Fetch API client & endpoint services
│   │   ├── store/                # Redux Toolkit store & feature slices
│   │   ├── types/                # TypeScript interfaces & definitions
│   │   ├── App.tsx               # Route declarations & navigation setup
│   │   └── main.tsx              # React DOM mounting
│   ├── package.json              # Node dependencies & Vite build scripts
│   └── vite.config.ts            # Vite build configuration & Tailwind plugin
│
├── ai/                           # AI, Machine Learning & Graph Intelligence
│   ├── data/                     # Feature engineering & dataset loaders
│   ├── encoders/                 # Node & Edge feature encoders
│   ├── evaluation/               # Model evaluation metrics & baseline benchmarks
│   ├── explainability/           # SHAP attributions, GNNExplainer, AttentionExplainer
│   ├── inference/                # Real-time single & batch prediction engines
│   ├── layers/                   # GAT, Message Passing, Pooling, Temporal layers
│   ├── models/                   # THGNN neural architectures & base models
│   └── training/                 # Trainer loop, loss functions, callbacks & metrics
│
├── configs/                      # YAML configuration files (security, logging, models)
├── WORKING.md                    # System documentation and execution guide
└── Makefile                      # Developer shortcut commands
```

---

## 3. Prerequisites & Environment Setup

### System Requirements
- **Python**: 3.10, 3.11, or 3.12
- **Node.js**: 18.x, 20.x, or 22.x
- **Package Managers**: `pip` and `npm`

---

## 4. How to Run the Application

### Step 1: Start the Backend API Server

Open a terminal in the project root:

```bash
# 1. Install backend dependencies
pip install -r backend/requirements.txt

# 2. Start the FastAPI server with hot-reload
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

- **API Base URL**: `http://localhost:8000/api/v1`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Alternative ReDoc UI**: `http://localhost:8000/redoc`

---

### Step 2: Start the Frontend React Dashboard

Open a second terminal window:

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install node dependencies
npm install

# 3. Start Vite development server
npm run dev
```

- **Frontend Application URL**: `http://localhost:5173`
- Open your browser and navigate to `http://localhost:5173` to access the SOC portal.

---

### Step 3: Run AI / Machine Learning & Inference Modules

You can execute AI pipelines, feature extraction, predictions, and model benchmarking directly via CLI:

#### 1. Single Entity Threat Prediction
```bash
python3 -c "from ai.inference.predictor import Predictor; p = Predictor(); print(p.predict('U1234'))"
```

#### 2. Enterprise Batch Evaluation & Summary
```bash
python3 -c "from ai.inference.batch_predictor import BatchPredictor; bp = BatchPredictor(); print(bp.summarize_batch(bp.predict_batch(['U1001', 'U1002', 'U1003'])))"
```

#### 3. Model Benchmark & Comparative Leaderboard
```bash
python3 -c "from ai.evaluation.benchmark import Benchmark; import json; print(json.dumps(Benchmark().get_leaderboard(), indent=2))"
```

#### 4. Explainable AI (XAI) Reasoning & Counterfactual Simulations
```bash
python3 -c "from ai.explainability.feature_importance import FeatureImportance; fi = FeatureImportance(); print(fi.explain('U1234'))"
```

#### 5. Extract Feature Vector from Logs
```bash
python3 -c "from ai.data.feature_engineer import FeatureEngineer; fe = FeatureEngineer(); print(fe.transform('U1234', events=[{'type': 'login'}, {'type': 'usb'}]))"
```

---

## 5. End-to-End System Workflow

```
[Raw Event Ingestion]
   │ (Logins, USB Connects, File Reads, Emails)
   ▼
[Feature Engineering Pipeline]
   │ (Extracts Temporal, Behavioral, Statistical Z-Scores)
   ▼
[Temporal Heterogeneous Graph Construction]
   │ (Nodes: User, Host, File, USB; Edges: LOGIN_TO, ACCESS_FILE, SEND_EMAIL)
   ▼
[THGNN Neural Inference Engine]
   │ (Calculates 0-100 Continuous Risk Score & Threat Level)
   ▼
[Automated Alert Generation & WebSocket Broadcast]
   │ (Emits HIGH/CRITICAL alerts to connected SOC Analysts)
   ▼
[SOC Analyst Investigation & XAI Reasoning]
   │ (Inspects Cytoscape Subgraph, SHAP feature weights, What-If Counterfactuals)
   ▼
[Resolution & Incident Reporting]
   │ (Assigns analyst, updates status, generates compliance audit report)
```

### 1. Ingestion & Feature Engineering
- Raw events from endpoints (logons, file accesses, USB events, email logs) are processed by `FeatureEngineer`.
- Features are categorized into:
  - **Temporal**: `hour_of_day`, `is_after_hours`, `is_weekend`, `sin_hour`, `cos_hour`.
  - **Behavioral**: `login_frequency`, `failed_login_ratio`, `file_download_bytes_mb`, `usb_insertion_count`, `email_external_ratio`.
  - **Statistical**: Deviation percentage and Z-score vs. historical entity baseline.

### 2. Graph Construction & THGNN Inference
- Entities and their relationships form a heterogeneous graph.
- The `Predictor` evaluates behavioral anomaly weights and graph structure to output:
  - **Risk Score** (0.0 to 100.0)
  - **Threat Classification**:
    - `CRITICAL`: Risk Score $\ge$ 85.0
    - `HIGH`: Risk Score $\ge$ 60.0
    - `MEDIUM`: Risk Score $\ge$ 30.0
    - `LOW`: Risk Score < 30.0
  - **Confidence Metric** (0.0 to 1.0)

### 3. Real-Time Alert Streaming & Dashboard Notification
- High-risk predictions trigger automated security alerts saved in the database (`alerts` table).
- The FastAPI WebSocket server (`/ws`) broadcasts new threat predictions and alert events to all active dashboard clients in real-time.

### 4. Interactive Behavioral Investigation & XAI Reasoning
- The analyst opens the **Behavioral Investigation** or **AI Explainability** page.
- The system presents:
  - **Feature Attribution Weights**: Highlights which behaviors drove the score (e.g., 42% after-hours login, 35% file download volume, 28% USB access).
  - **Counterfactual "What-If" Analysis**: Demonstrates risk reduction if specific behaviors are revoked (e.g., "Eliminate off-hours activity $\rightarrow$ -28.5 Risk", "Revoke removable media $\rightarrow$ -19.0 Risk").
  - **Interactive Graph Topology**: Explores the 2-hop neighborhood surrounding the suspect entity using Cytoscape.js.

### 5. Incident Remediation & Executive Reporting
- Analysts can assign alerts, update resolution statuses (`open`, `in_progress`, `resolved`, `dismissed`), deactivate compromised accounts in **User Administration**, and export PDF/CSV audit reports.

---

## 6. REST API Endpoint Reference

### Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | Register a new user account | No |
| `POST` | `/api/v1/auth/login` | Authenticate with username & password (OAuth2 Form) | No |
| `POST` | `/api/v1/auth/refresh` | Refresh an expired access token | No |
| `GET` | `/api/v1/auth/me` | Fetch currently authenticated user profile | Bearer Token |

### Threat Predictions (`/api/v1/predictions`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/predictions/` | Trigger real-time THGNN inference for an employee ID | Bearer Token |
| `GET` | `/api/v1/predictions/` | List historical predictions (filterable by employee ID) | Bearer Token |
| `GET` | `/api/v1/predictions/{id}` | Get prediction details and stored explanation | Bearer Token |

### Alerts & Incidents (`/api/v1/alerts`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/alerts/` | List security alerts (filter by status, severity) | Bearer Token |
| `POST` | `/api/v1/alerts/` | Create a new security alert | Bearer Token |
| `GET` | `/api/v1/alerts/{id}` | Retrieve single alert details | Bearer Token |
| `PUT` | `/api/v1/alerts/{id}` | Update alert status, assignee, or investigation notes | Bearer Token |
| `DELETE` | `/api/v1/alerts/{id}` | Delete an alert | Bearer Token |

### Graph Explorer (`/api/v1/graphs`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/graphs/query` | Query entity neighborhood topology for Cytoscape | Bearer Token |
| `POST` | `/api/v1/graphs/subgraph` | Extract k-hop ego subgraph around target node | Bearer Token |

### Explainability (`/api/v1/explain`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/explain/{prediction_id}` | Fetch SHAP attributions, top features, counterfactuals | Bearer Token |
| `GET` | `/api/v1/explain/{prediction_id}/subgraph` | Fetch GNNExplainer influential subgraph | Bearer Token |
| `GET` | `/api/v1/explain/{prediction_id}/attention` | Fetch multi-head graph attention weights | Bearer Token |

### User Management (`/api/v1/users`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/users/` | List all system users | Bearer Token |
| `GET` | `/api/v1/users/{id}` | Get user by ID | Bearer Token |
| `PUT` | `/api/v1/users/{id}` | Update user role, department, or active status | Bearer Token |
| `DELETE` | `/api/v1/users/{id}` | Deactivate user account | Bearer Token |

### System Settings & Reports (`/api/v1/settings`, `/api/v1/reports`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/settings/` | Retrieve backend configuration and runtime telemetry | Bearer Token |
| `POST` | `/api/v1/reports/generate` | Generate compliance summary report | Bearer Token |
| `GET` | `/api/v1/reports/{id}` | Fetch generated report metadata and metrics | Bearer Token |

---

## 7. Frontend Pages & Capabilities

| Page | URL Route | Description |
|---|---|---|
| **Threat Dashboard** | `/` | Executive overview: active alerts, threat distribution pie chart, weekly risk trends, real-time WebSocket event feed. |
| **Incident Alerts** | `/alerts` | SOC triage table: severity filters (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), assignee assignment, status workflow. |
| **Behavioral Investigations** | `/investigations` | Deep-dive entity analyzer: on-demand THGNN re-evaluation, correlated incident timeline, risk score meter. |
| **Enterprise Graph Explorer** | `/graph` | Interactive Cytoscape graph canvas: force-directed (CoSE), concentric, and hierarchical layouts with node detail inspector. |
| **AI Explainability (XAI)** | `/xai` | Natural language threat reasoning, SHAP attribution bar charts, and counterfactual what-if projections. |
| **User Administration** | `/users` | Manage SOC analysts, auditors, and administrators; toggle account status. |
| **Compliance Reports** | `/reports` | Executive security summaries with export options (PDF/CSV). |
| **System Settings** | `/settings` | Backend runtime parameters, CORS origins, and token TTL overview. |
| **Authentication** | `/login` | Role-based login for Analysts, Administrators, and Compliance Auditors. |

---

## 8. Verification & Quality Assurance Commands

Run the test suite and compilation verification:

```bash
# 1. Type-check Frontend
cd frontend && npx tsc --noEmit

# 2. Verify Python Syntax & Import Integrity
python3 -m py_compile backend/app/**/*.py ai/**/*.py

# 3. Execute End-to-End AI Unit & Verification Suite
python3 -c "
from ai.data.feature_engineer import FeatureEngineer
from ai.models.node_encoder import NodeEncoder
from ai.inference.predictor import Predictor
from ai.evaluation.evaluator import Evaluator
from ai.explainability.feature_importance import FeatureImportance

fe = FeatureEngineer()
pred = Predictor()
evaluator = Evaluator()
fi = FeatureImportance()

print('Feature extraction:', len(fe.transform('U1234')))
print('Inference score:', pred.predict('U1234')['risk_score'])
print('Evaluator AUC:', evaluator.evaluate([1, 0], [0.9, 0.1])['auroc'])
print('XAI target:', fi.explain('U1234')['target_id'])
print('Verification Successful!')
"
```

---

## 9. Default User Roles & Credentials

For local development and testing:
- **Analyst**: `username: analyst`, `role: analyst`
- **Admin**: `username: admin`, `role: admin`
- **Auditor**: `username: auditor_1`, `role: auditor`

---

## 10. Summary

The Insider Threat Detection System is fully integrated across its **FastAPI backend**, **React 19 frontend**, and **AI/XAI pipeline**. It offers an end-to-end operational workflow for SOC teams to monitor, investigate, and explain behavioral insider threats in real-time.
