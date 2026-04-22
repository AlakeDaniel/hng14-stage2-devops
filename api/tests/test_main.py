import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch('redis.Redis') as mock_redis:
    mock_redis.return_value = MagicMock()
    from main import app

client = TestClient(app)

def test_health_endpoint():
    with patch('main.r') as mock_r:
        mock_r.ping.return_value = True
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

def test_create_job():
    with patch('main.r') as mock_r:
        mock_r.lpush.return_value = 1
        mock_r.hset.return_value = 1
        response = client.post("/jobs")
        assert response.status_code == 200
        assert "job_id" in response.json()

def test_get_job_found():
    with patch('main.r') as mock_r:
        mock_r.hget.return_value = "completed"
        response = client.get("/jobs/test-job-123")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

def test_get_job_not_found():
    with patch('main.r') as mock_r:
        mock_r.hget.return_value = None
        response = client.get("/jobs/nonexistent-job")
        assert response.status_code == 404
