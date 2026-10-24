import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"To-Do List App" in rv.data

def test_get_todos_api(client):
    rv = client.get('/api/todos')
    assert rv.status_code == 200
    data = rv.get_json()
    assert "todos" in data
    assert len(data["todos"]) >= 2

def test_metrics_endpoint(client):
    rv = client.get('/metrics')
    assert rv.status_code == 200
    assert b"http_requests_total" in rv.data