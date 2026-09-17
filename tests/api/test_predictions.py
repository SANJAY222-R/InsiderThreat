"""
Test: Predictions Endpoints
"""

import pytest


class TestPredictionEndpoints:
    """Tests for the /api/v1/predictions endpoints."""

    @pytest.mark.api
    def test_predict_requires_auth(self, client):
        response = client.post("/api/v1/predictions/predict", json={"employee_id": "TEST001"})
        assert response.status_code in (401, 403)

    @pytest.mark.api
    def test_predict_single_employee(self, client, auth_headers, sample_prediction_payload):
        response = client.post(
            "/api/v1/predictions/predict",
            json=sample_prediction_payload,
            headers=auth_headers,
        )
        assert response.status_code in (200, 201)
        data = response.json()
        assert "employee_id" in data or "risk_score" in data

    @pytest.mark.api
    def test_get_predictions_list(self, client, auth_headers):
        response = client.get("/api/v1/predictions/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.api
    def test_get_prediction_by_id(self, client, auth_headers):
        response = client.get("/api/v1/predictions/1", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "employee_id" in data
        assert "risk_score" in data

    @pytest.mark.api
    def test_get_prediction_not_found(self, client, auth_headers):
        response = client.get("/api/v1/predictions/99999", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.api
    def test_predictions_list_contains_seeded_data(self, client, auth_headers):
        response = client.get("/api/v1/predictions/", headers=auth_headers)
        assert response.status_code == 200
        predictions = response.json()
        employee_ids = [p.get("employee_id") for p in predictions]
        assert "MOH0273" in employee_ids
