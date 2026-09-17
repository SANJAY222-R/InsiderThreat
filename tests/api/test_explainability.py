"""
Test: XAI Explainability Endpoints
"""

import pytest


class TestExplainabilityEndpoints:
    """Tests for the /api/v1/explain endpoints."""

    @pytest.mark.api
    def test_get_explanation_requires_auth(self, client):
        response = client.get("/api/v1/explain/1")
        assert response.status_code in (401, 403)

    @pytest.mark.api
    def test_get_explanation_not_found(self, client, auth_headers):
        response = client.get("/api/v1/explain/99999", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.api
    def test_get_explanation_success(self, client, auth_headers):
        # Prediction ID 1 is seeded (MOH0273, CRITICAL)
        response = client.get("/api/v1/explain/1", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "prediction_id" in data
        assert "employee_id" in data
        assert "risk_score" in data
        assert "explanation" in data
        explanation = data["explanation"]
        assert "feature_importance" in explanation

    @pytest.mark.api
    def test_explanation_feature_importance_values(self, client, auth_headers):
        response = client.get("/api/v1/explain/1", headers=auth_headers)
        assert response.status_code == 200
        importance = response.json()["explanation"]["feature_importance"]
        assert isinstance(importance, dict)
        assert len(importance) > 0
        for name, value in importance.items():
            assert isinstance(name, str)
            assert isinstance(value, (int, float))

    @pytest.mark.api
    def test_get_subgraph_explanation_success(self, client, auth_headers):
        response = client.get("/api/v1/explain/1/subgraph", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data
        assert "edges" in data
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)

    @pytest.mark.api
    def test_get_attention_explanation_success(self, client, auth_headers):
        response = client.get("/api/v1/explain/1/attention", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "attention_heads" in data
        assert isinstance(data["attention_heads"], list)

    @pytest.mark.api
    def test_subgraph_not_found(self, client, auth_headers):
        response = client.get("/api/v1/explain/99999/subgraph", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.api
    def test_attention_not_found(self, client, auth_headers):
        response = client.get("/api/v1/explain/99999/attention", headers=auth_headers)
        assert response.status_code == 404
