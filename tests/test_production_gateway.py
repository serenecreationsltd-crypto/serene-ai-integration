import os
from fastapi.testclient import TestClient

os.environ["ENVIRONMENT"] = "production"
os.environ["JWT_SECRET"] = "test-only-secret-of-sufficient-length-1234567890"
os.environ["ADMIN_PASSWORD"] = "test-only-password-of-sufficient-length"
os.environ["GATEWAY_SERVER_TOKEN"] = "test-gateway-secret-12345678901234567890"
os.environ["DATABASE_URL"] = "sqlite:///./test_gateway_auth.db"

from app.server import app
from app.config import get_settings

from app import server
server.settings.environment = "production"

def test_chat_requires_gateway_token():
    with TestClient(app) as client:
        r = client.post("/api/chat", json={"message": "hello"})
    assert r.status_code == 401

def test_chat_rejects_wrong_gateway_token():
    with TestClient(app) as client:
        r = client.post("/api/chat", headers={"X-Gateway-Token": "wrong"}, json={"message": "hello"})
    assert r.status_code == 401

def test_chat_rejects_conversation_id_reuse():
    with TestClient(app) as client:
        r = client.post("/api/chat", headers={"X-Gateway-Token": "test-gateway-secret-12345678901234567890"}, json={"message": "hello", "conversation_id": 123})
    assert r.status_code == 400
