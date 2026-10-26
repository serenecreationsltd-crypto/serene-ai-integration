import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("JWT_SECRET", "test-only-signing-secret-not-for-production")
os.environ.setdefault("ADMIN_PASSWORD", "test-only-admin-password-not-for-production")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_serene_integration.db")

from app.server import app

def test_public_health():
    with TestClient(app) as client:
        response = client.get("/api/health")
    assert response.status_code == 200

def test_integration_registry_requires_auth():
    with TestClient(app) as client:
        response = client.get("/api/admin/integrations")
    assert response.status_code in (401, 403)
