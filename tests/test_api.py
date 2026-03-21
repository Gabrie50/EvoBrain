import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_health():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_stats():
    response = client.get('/api/stats')
    assert response.status_code == 200
    assert 'status' in response.json()


def test_agents():
    response = client.get('/api/agents')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_predict():
    response = client.get('/api/predict/current')
    assert response.status_code == 200


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()['name'] == 'EvoBrain'
