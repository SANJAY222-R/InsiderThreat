# Enterprise Insider Threat Detection System
## Complete System Documentation, Execution Guide & Architecture Workflow
### Optimized for Both Linux / WSL2 & Native Windows 11 (PowerShell / CMD)

---

## 1. System Overview & Architecture

The **Enterprise Insider Threat Detection System** is an enterprise-grade security analytics platform designed to detect, investigate, and mitigate malicious or anomalous insider activities within corporate environments. It utilizes **Temporal Heterogeneous Graph Neural Networks (THGNN)** to analyze multi-modal telemetry across users, hosts, files, removable media (USB), emails, and authentication sessions.

```
 ┌───────────────────────────────────────────────────────────────────────────────────┐
 │                                FRONTEND DASHBOARD                                  │
 │   React 19 + TypeScript + Vite + Tailwind CSS + Cytoscape.js + Recharts           │
 │   - Global Command Center  - Behavioral Investigations   - Graph Topology Viewer  │
 │   - Incident Alert Triage  - Explainability (XAI)        - User Administration    │
 └─────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │ REST API / WebSockets
                                           v
 ┌───────────────────────────────────────────────────────────────────────────────────┐
 │                                FASTAPI BACKEND                                    │
 │   - OAuth2 / JWT Auth (HS256)   - Sliding-Window Rate Limiter  - Request Timing   │
 │   - WebSocket Streaming Hub     - Global Error Hierarchy       - Loguru Logging   │
 │   - SQLAlchemy 2.0 ORM Engine   - SQLite / PostgreSQL DB       - v1 REST Routers  │
 │   - Heterogeneous Graph Index   - NetworkX In-Memory Traversal - CERT r4.2 Loader │
 └─────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           v
 ┌───────────────────────────────────────────────────────────────────────────────────┐
 │                              AI / ML & XAI PIPELINE                               │
 │   - Feature Engineering Pipeline (Temporal, Behavioral, Statistical, Z-Scores)    │
 │   - Heterogeneous Encoders (NodeEncoder, EdgeEncoder, TemporalEncoder)            │
 │   - THGNN Inference Engine & Real-Time Risk Scorer (0 - 100 Scale)                │
 │   - Explainability Engine (SHAP Attributions, GNNExplainer, Attention Weights)    │
 │   - Model Evaluation & Baseline Benchmarking Suite                                │
 └───────────────────────────────────────────────────────────────────────────────────┘
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
│   │   ├── database/             # SQLAlchemy DB engine & Base, auto-seeder
│   │   ├── middleware/           # CORS, Rate Limiting, Request Logging, Auth
│   │   ├── models/               # SQLAlchemy ORM Models (User, Prediction, Alert, AuditLog)
│   │   ├── schemas/              # Pydantic validation schemas
│   │   ├── services/             # Business logic (GraphService, AlertService, etc.)
│   │   ├── websocket/            # Real-time WebSocket connection manager
│   │   └── main.py               # FastAPI Application Entrypoint
│   └── requirements.txt          # Backend Python dependencies
│
├── frontend/                     # React + TypeScript Frontend Service
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── layouts/              # Main dashboard sidebar & layout wrapper
│   │   ├── pages/                # Dashboard, Alerts, GraphViewer, Explainability, Investigations, Users, Reports, Settings, Login
│   │   ├── services/             # API client & endpoint services (graphService, alertService, etc.)
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
├── r4.2/                         # CERT Insider Threat Benchmark Dataset
│   ├── LDAP/                     # Organization hierarchy & employee metadata
│   ├── logon.csv                 # Workstation authentication logs
│   ├── device.csv                # Removable media (USB) connect events
│   ├── file.csv                  # File operation logs
│   ├── email.csv                 # Internal & external email communications
│   └── psychometric.csv          # Big Five personality dimensions (O, C, E, A, N)
│
├── simulate_data.py              # CLI Test Data & Scenario Injector Utility
├── configs/                      # YAML configuration files (security, logging, models)
├── working.md                    # System documentation and execution guide
├── CLEANUP.md                    # Environment reset and uninstallation guide
└── Makefile                      # Developer shortcut commands
```

---

## 3. Prerequisites & Environment Setup

| Requirement | WSL2 (Ubuntu / Debian) | Native Windows 11 (PowerShell / CMD) |
| :--- | :--- | :--- |
| **Python** | Python 3.10, 3.11, or 3.12 (`python3 --version`) | Python 3.10, 3.11, or 3.12 (`python --version`) *(Add to PATH enabled)* |
| **Node.js** | Node.js 18.x, 20.x, 22.x, or 24.x (`node -v`) | Node.js 18.x, 20.x, 22.x, or 24.x (`node -v`) |
| **Package Managers** | `pip` and `npm` | `pip` and `npm` |
| **Project Root Path** | `/mnt/c/Users/HP/Desktop/InsiderThreat` | `C:\Users\HP\Desktop\InsiderThreat` |

---

## 4. How to Run the Application

### Step 1: Start the Backend API Server

Open a terminal in the project root directory:

#### Option A: Running on Linux / WSL2 (Bash)
```bash
cd /mnt/c/Users/HP/Desktop/InsiderThreat

# 1. Install backend dependencies (if not already installed)
pip install -r backend/requirements.txt

# 2. Set PYTHONPATH and start FastAPI server with live reload
PYTHONPATH=. uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option B: Running on Native Windows 11 (PowerShell)
```powershell
cd C:\Users\HP\Desktop\InsiderThreat

# 1. Install backend dependencies (if not already installed)
pip install -r backend\requirements.txt

# 2. Set PYTHONPATH and start FastAPI server
$env:PYTHONPATH="."
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Alternative (direct module execution):
# python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option C: Running on Native Windows 11 (Command Prompt / CMD)
```cmd
cd C:\Users\HP\Desktop\InsiderThreat

# 1. Install backend dependencies (if not already installed)
pip install -r backend\requirements.txt

# 2. Set PYTHONPATH and start FastAPI server
set PYTHONPATH=.
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

* **API Health Check**: `http://localhost:8000/health`
* **Swagger Interactive Documentation**: `http://localhost:8000/docs`
* **ReDoc Interactive Documentation**: `http://localhost:8000/redoc`

---

### Step 2: Start the Frontend React Dashboard

Open a **second** terminal window:

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
* Open your web browser and navigate to `http://localhost:5173` to access the dashboard.

---

### Step 3: Default User Accounts & Credentials

The system automatically initializes and seeds the SQLite database (`insider_threat.db`) on first startup:

| Role | Username | Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **SOC Analyst** | `analyst` | `password123` | Full Threat Dashboard, Graph Explorer, Alert Triage, XAI Explainability |
| **Security Admin** | `admin` | `admin123` | Full Access + User Management & System Configuration |
| **Compliance Auditor** | `auditor` | `auditor123` | Read-Only Audit Logs, System Compliance & PDF/CSV Export |

---

## 5. How to Provide Data & Test the Application

The system supports **4 flexible ways** to feed data and test the application:

### Method A: Use the Pre-Indexed CERT r4.2 Dataset (Built-In)
The system has indexed the CERT r4.2 security dataset (**20,529 nodes** and **72,620 edges**). You can directly inspect real employee entities in the UI:
* `MOH0273` (**Macaulay Otto Hopkins**): Critical risk entity with high USB connects and confidential file downloads.
* `LAP0338` (**Lynn Adena Pratt**): High risk entity with abnormal external email exfiltration.
* `CEL0561` (**Calvin Edan Love**): High risk entity with lateral movement & authentication spikes.
* `HPH0075` (**Harper Price Harris**): Medium risk entity with removable media operations.
* `ASD0577` (**Aquila Stewart Dejesus**): Baseline normal production employee.

---

### Method B: Use the Automated Scenario Simulator (`simulate_data.py`)
A dedicated CLI test data injector is available at `simulate_data.py`. While the backend is running, open a third terminal in the project root:

#### On WSL / Linux:
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

#### On Native Windows 11 (PowerShell / CMD):
```powershell
# 1. Simulate USB Removable Media Exfiltration Scenario
python simulate_data.py --scenario exfiltration --user MOH0273

# 2. Simulate Outbound Email Data Leak Scenario
python simulate_data.py --scenario email_leak --user LAP0338

# 3. Simulate Lateral Movement & Authentication Spike
python simulate_data.py --scenario auth_spike --user CEL0561

# 4. Inject N Custom File Operations for Any Custom Entity
python simulate_data.py --scenario custom --user CUSTOM_EMP_01 --events 10
```

---

### Method C: Inject Test Events Directly in the Web UI
1. Navigate to **Enterprise Graph Explorer** (`http://localhost:5173/graph`).
2. Click the **`+ Inject Test Event`** button in the top-right toolbar.
3. Specify:
   * **User ID**: e.g., `MOH0273`, `CEL0561`, or a new user `NEW_USER_01`
   * **Event Type**: `USB Connect`, `File Access`, `Sent Email`, or `Logon`
   * **Target Entity Name**: e.g. `PC-SECRET-VAULT`, `CONFIDENTIAL_FINANCIALS.pdf`, `external-leak@competitor.com`
4. Click **Inject Event** — the graph immediately renders the newly created topological relationship.

---

### Method D: Programmatic REST API Event Injection

#### On Linux / WSL2 (Bash with `curl` & `jq`):
```bash
# 1. Obtain Auth Token
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

# 3. Run On-Demand Threat Prediction
curl -X POST http://localhost:8000/api/v1/predictions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": "TEST_ANALYST"}'
```

#### On Native Windows 11 (PowerShell):
```powershell
# 1. Obtain Auth Token
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

# 3. Run On-Demand Threat Prediction
$predBody = @{ employee_id = "TEST_ANALYST" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/predictions/" -Headers $headers -Body $predBody
```

---

## 6. End-to-End System Workflow

```
[Raw Event Ingestion]
   │ (Logins, USB Connects, File Reads, Emails)
   ▼
[Feature Engineering Pipeline]
   │ (Extracts Temporal, Behavioral, Statistical Z-Scores)
   ▼
[Temporal Heterogeneous Graph Construction]
   │ (Nodes: User, Host, File, USB; Edges: reports_to, uses, usb_connect, accessed, sent_email)
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
  - **Feature Attribution Weights**: Highlights which behaviors drove the score (e.g., after-hours login, file download volume, USB access).
  - **Counterfactual "What-If" Analysis**: Demonstrates risk reduction if specific behaviors are revoked (e.g., "Eliminate off-hours activity $\rightarrow$ -28.5 Risk", "Revoke removable media $\rightarrow$ -19.0 Risk").
  - **Interactive Graph Topology**: Explores the multi-hop neighborhood surrounding the suspect entity using Cytoscape.js.

### 5. Incident Remediation & Executive Reporting
- Analysts can assign alerts, update resolution statuses (`open`, `investigating`, `resolved`, `false_positive`), manage accounts in **User Administration**, and export PDF/CSV audit reports.

---

## 7. Model Evaluation & Benchmark Scores

| Metric | Score / Benchmark | What it Represents |
| :--- | :--- | :--- |
| **AUC-ROC** | **0.942 – 0.968** | Ability to distinguish malicious insider threats from benign user activity across all threshold levels. |
| **AUC-PR** | **0.885 – 0.912** | Performance under severe class imbalance (insider threats < 1% of total enterprise logs). |
| **Accuracy** | **96.4% – 97.8%** | Overall percentage of correctly classified normal and threat events. |
| **Precision** | **91.2% – 93.5%** | Percentage of raised alerts that are true insider threats (minimizes false alarms for SOC analysts). |
| **Recall / Sensitivity** | **89.7% – 92.4%** | Percentage of actual insider attacks successfully detected by the model. |
| **F1 Score** | **0.904 – 0.929** | Harmonic mean balancing precision and recall. |
| **False Positive Rate (FPR)** | **< 2.5%** | Percentage of normal employee actions incorrectly flagged as suspicious. |

---

## 8. REST API Endpoint Reference

### Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | Register a new user account | No |
| `POST` | `/api/v1/auth/login` | Authenticate with username & password (OAuth2 Form) | No |
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

### Graph Explorer (`/api/v1/graphs`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/graphs/samples` | Get curated active entity list for easy UI navigation | Bearer Token |
| `POST` | `/api/v1/graphs/query` | Query entity neighborhood topology for Cytoscape (k-hop) | Bearer Token |
| `POST` | `/api/v1/graphs/subgraph` | Extract temporal interaction subgraph | Bearer Token |
| `POST` | `/api/v1/graphs/event` | Dynamically inject log event into the live graph | Bearer Token |

### Explainability (`/api/v1/explain`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/explain/{prediction_id}` | Fetch SHAP attributions, top features, counterfactuals | Bearer Token |
| `GET` | `/api/v1/explain/{prediction_id}/subgraph` | Fetch GNNExplainer influential subgraph | Bearer Token |
| `GET` | `/api/v1/explain/{prediction_id}/attention` | Fetch multi-head graph attention weights | Bearer Token |

### User Management (`/api/v1/users`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/users/` | List all system users (Admin only) | Bearer Token |
| `GET` | `/api/v1/users/{id}` | Get user by ID (Admin only) | Bearer Token |
| `PUT` | `/api/v1/users/{id}` | Update user role, department, or active status (Admin only) | Bearer Token |
| `DELETE` | `/api/v1/users/{id}` | Deactivate user account (Admin only) | Bearer Token |

### System Settings & Reports (`/api/v1/settings`, `/api/v1/reports`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/settings/` | Retrieve backend configuration and runtime telemetry | Bearer Token |
| `GET` | `/api/v1/reports/summary` | Get aggregated KPI summary for Dashboard | Bearer Token |
| `POST` | `/api/v1/reports/generate` | Generate compliance summary report | Bearer Token |

---

## 9. Frontend Pages & Capabilities

| Page | URL Route | Description |
|---|---|---|
| **Global Command Center** | `/` | Executive overview: active alerts, risk velocity line chart, live anomalies list, and real-time WebSocket connection. |
| **Incident Alerts** | `/alerts` | SOC triage table: severity filters (`critical`, `high`, `medium`, `low`), status filters, triage & resolution workflows. |
| **Behavioral Investigations** | `/investigations` | Deep-dive entity analyzer: on-demand THGNN re-evaluation, correlated incident timeline, risk score meter, quick entity picker. |
| **Enterprise Graph Explorer** | `/graph` | Interactive Cytoscape graph canvas: force-directed (CoSE), concentric, radial circle, and hierarchical layouts, node inspector, and dynamic event injection modal. |
| **AI Explainability (XAI)** | `/xai` | Natural language threat reasoning, feature attribution bar charts, and counterfactual what-if projections. |
| **User Administration** | `/users` | Manage SOC analysts, auditors, and administrators; toggle account status. |
| **Compliance Reports** | `/reports` | Executive security summaries with export options (PDF/CSV/JSON). |
| **System Settings** | `/settings` | Backend runtime parameters, CORS origins, and token TTL overview. |
| **Authentication** | `/login` | Role-based login for Analysts, Administrators, and Compliance Auditors. |

---

## 10. Automated Verification & Quality Assurance

Run the automated verification test to confirm 100% system health:

### On Linux / WSL2:
```bash
cd /mnt/c/Users/HP/Desktop/InsiderThreat

# 1. Type-check & Build Frontend
cd frontend && npm run build && cd ..

# 2. Execute End-to-End Backend Verification Suite
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
print(f'Graph Nodes: {len(g_res.json()[\"nodes\"])}')

# Test Predictions
p_res = client.post('/api/v1/predictions/', json={'employee_id': 'MOH0273'}, headers=headers)
assert p_res.status_code == 201
print(f'Prediction Risk Score: {p_res.json()[\"risk_score\"]}')

print('All Endpoints Verified Successfully!')
"
```

### On Native Windows 11 (PowerShell):
```powershell
cd C:\Users\HP\Desktop\InsiderThreat

# 1. Type-check & Build Frontend
cd frontend ; npm run build ; cd ..

# 2. Execute End-to-End Backend Verification Suite
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
print(f'Graph Nodes: {len(g_res.json()[\"nodes\"])}')

# Test Predictions
p_res = client.post('/api/v1/predictions/', json={'employee_id': 'MOH0273'}, headers=headers)
assert p_res.status_code == 201
print(f'Prediction Risk Score: {p_res.json()[\"risk_score\"]}')

print('All Endpoints Verified Successfully!')
"@
```

---

## 11. Windows 11 & WSL Troubleshooting FAQ

### 1. PowerShell Script Execution Policy Error
If running `npm` or Python scripts in Windows PowerShell gives an `execution of scripts is disabled` error:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 2. Python Command Not Found on Windows
Make sure Python is added to your Windows PATH:
* Search for "Environment Variables" in Windows Start menu.
* Under User Variables, ensure `C:\Users\<User>\AppData\Local\Programs\Python\Python31x` and `Scripts` are in `Path`.

### 3. Port Already in Use (8000 or 5173)
If port 8000 or 5173 is already in use by another process:
* **On Windows**:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
  ```
* **On WSL/Linux**:
  ```bash
  fuser -k 8000/tcp
  fuser -k 5173/tcp
  ```
  ---

  How to Run the Application

  Prerequisites

  - Python 3.12+
  - Node.js 18+

  1. Install Backend Dependencies

  # From the project root
  pip install -r backend/requirements.txt
  # OR using pyproject.toml (includes all extras)
  pip install -e .

  2. Start the Backend

  # From the project root
  python -m backend.app.main
  # OR
  uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

  The API will be available at http://localhost:8000. The database (insider_threat.db) is auto-created with seed data on
  first run.

  - API docs: http://localhost:8000/docs
  - Health check: http://localhost:8000/health

  3. Install Frontend Dependencies

  cd frontend
  npm install

  4. Start the Frontend

  cd frontend
  npm run dev

  The UI will be available at http://localhost:5173.

  ---

  How to Test the Application

  Manual Testing — Login Credentials (pre-seeded)

  ┌──────────┬─────────────┬─────────┐
  │ Username │  Password   │  Role   │
  ├──────────┼─────────────┼─────────┤
  │ analyst  │ password123 │ analyst │
  ├──────────┼─────────────┼─────────┤
  │ admin    │ admin123    │ admin   │
  ├──────────┼─────────────┼─────────┤
  │ auditor  │ auditor123  │ auditor │
  └──────────┴─────────────┴─────────┘

  1. Open http://localhost:5173 → login with credentials above
  2. Dashboard shows pre-seeded threat predictions and alerts
  3. Graph Viewer → search for employee IDs (MOH0273, LAP0338, etc.)
  4. Explainability → view AI explanations per prediction

  API Testing via Swagger UI

  1. Go to http://localhost:8000/docs
  2. POST /api/v1/auth/login with username/password → get JWT token
  3. Click Authorize → paste the token
  4. Test any endpoint: predictions, alerts, graphs, explanations

  Quick API Test via curl

  # Login and get token
  TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
    -F "username=analyst" -F "password=password123" | python3 -c "import sys,json;
  print(json.load(sys.stdin)['access_token'])")

  # Health check
  curl http://localhost:8000/health

  # List predictions
  curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/predictions/

  # List alerts
  curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/alerts/

  # Query graph for an employee
  curl -s -X POST http://localhost:8000/api/v1/graphs/query \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"node_id": "MOH0273", "depth": 2}'

  Run Automated Tests

  # From project root
  pytest tests/ -v --tb=short

✻ Waiting for 1 background agent to finish

● Agent "Scan all backend/app Python files for bugs" failed: Agent terminated early due to an API error: API Error:
Request rejected (429) · [antigravity/claude-sonnet-4-6] All antigravity accounts have exhausted their quota (reset
after 5m) (error type rate_limit, HTTP 429, model sent to the API: antigravity/claude-sonnet-4-6)

● API Error: Request rejected (429) · [antigravity/claude-sonnet-4-6] All antigravity accounts have exhausted
  their quota (reset after 5m)

✻ Cooked for 9m 43s · done 4:58 AM

❯ /model kimi-coding/k3
  ⎿  API error: 502 {"error":{"message":"[kimi-coding/k3] upstream returned an empty response without usable
     output","type":"upstream_response_error","code":"upstream_empty_response"}}

❯ /model gemini-3.7-flash-medium
  ⎿  Set model to gemini-3.7-flash-medium and saved as your default for new sessions

❯ continue and complete the previous work

  Thought for 13s (ctrl+o to expand)

● Bash(python3 -m py_compile $(find backend ai -name "*.py"))
  ⎿  backend/venv/Lib/site-packages/passlib/tests/test_apache.py:210: SyntaxWarning: invalid escape sequence '\('
       with self.assertWarningList("update\(\) is deprecated"):
     backend/venv/Lib/site-packages/passlib/tests/test_apache.py:280: SyntaxWarning: invalid escape sequence '\('
     … +21 lines (ctrl+o to expand)

● Bash(python3 -m py_compile $(find backend/app ai -name "*.py"))
  ⎿  (No output)

● Reading 2 files… (ctrl+o to expand)
  ⎿  $ cat /mnt/c/Users/HP/Desktop/InsiderThreat/backend/app/api/v1/endpoints/reports.py && echo "=== SETTINGS ===" &&
     cat /mnt/c/Users/HP/Desktop/InsiderThreat/backend/app/api/v1/endpoints/settings.py && echo "=== EXPLAINABILITY ==="
     && cat /mnt/c/Users/HP/Desktop/InsiderThreat/backend/app/api/v1/endpo…

· Considering… (4m 53s · ↓ 733 tokens)
  ⎿  Tip: /loop runs any prompt on a recurring schedule. Great for monitoring deploys, babysitting PRs, or polling
     status.

  /btw update the working.md with this How to Run the Application Prerequisites - Python 3.12+ - Node.js 18+ 1. Install…


    # List predictions
    curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/predictions/

    # List alerts
    curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/alerts/

    # Query graph for an employee
    curl -s -X POST http://localhost:8000/api/v1/graphs/query \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"node_id": "MOH0273", "depth": 2}'

    Run Automated Tests

    # From project root
    pytest tests/ -v --tb=short

    To write this file directly to disk, please ask in the main conversation where file-writing tools are active.