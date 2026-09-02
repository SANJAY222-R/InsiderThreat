# API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints (except `/auth/login`) require a Bearer JWT token.

## Endpoints

TODO (Phase 2): Auto-generate from FastAPI OpenAPI schema.

### Health Check
- `GET /health` — System health status

### Authentication
- `POST /api/v1/auth/login` — User login
- `POST /api/v1/auth/refresh` — Refresh access token
- `POST /api/v1/auth/logout` — User logout

### Users
- `GET /api/v1/users` — List users
- `POST /api/v1/users` — Create user
- `GET /api/v1/users/{id}` — Get user
- `PUT /api/v1/users/{id}` — Update user
- `DELETE /api/v1/users/{id}` — Delete user

### Predictions
- `POST /api/v1/predictions` — Request prediction
- `POST /api/v1/predictions/batch` — Batch predictions
- `GET /api/v1/predictions/{id}` — Get prediction result

### Graphs
- `POST /api/v1/graphs/query` — Query graph neighborhood
- `POST /api/v1/graphs/subgraph` — Extract temporal subgraph

### Alerts
- `GET /api/v1/alerts` — List alerts
- `PUT /api/v1/alerts/{id}` — Update alert status
- `POST /api/v1/alerts/{id}/assign` — Assign alert

### Reports
- `POST /api/v1/reports` — Generate report
- `GET /api/v1/reports/{id}` — Get report status / download

### Explainability
- `GET /api/v1/explain/{prediction_id}` — Get prediction explanation
