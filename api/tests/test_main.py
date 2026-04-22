import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def client():
    with patch('redis.Redis') as mock_redis:
        mock_redis.return_value = MagicMock()
        from fastapi.testclient import TestClient
        import importlib
        import main
        importlib.reload(main)
        from main import app
        return TestClient(app)


def test_health_endpoint(client):
    with patch('main.r') as mock_r:
        mock_r.ping.return_value = True
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


def test_create_job(client):
    with patch('main.r') as mock_r:
        mock_r.lpush.return_value = 1
        mock_r.hset.return_value = 1
        response = client.post("/jobs")
        assert response.status_code == 200
        assert "job_id" in response.json()


def test_get_job_found(client):
    with patch('main.r') as mock_r:
        mock_r.hget.return_value = "completed"
        response = client.get("/jobs/test-job-123")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"


def test_get_job_not_found(client):
    with patch('main.r') as mock_r:
        mock_r.hget.return_value = None
        response = client.get("/jobs/nonexistent-job")
        assert response.status_code == 404
