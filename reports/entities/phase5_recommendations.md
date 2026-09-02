# Phase 5 Recommendations: Temporal Graph Construction

## 1. Graph Storage
- **Recommendation:** Neo4j Community Edition or Neo4j Aura.
- **Rationale:** Neo4j's property graph model perfectly aligns with the generated schemas, supporting node features easily.

## 2. Temporal Windows
- **Recommendation:** 24-hour sliding windows with 12-hour overlap.
- **Rationale:** Captures day-to-day anomalous drifts effectively without massive graph explosion.

## 3. Graph Schema Topology
- Nodes: User, Host, File, USB, Email, Domain, Website
- Edges: LOGS_ON (User->Host), ACCESSES (User->File), SENDS (User->Email), CONNECTS (Host->USB)

