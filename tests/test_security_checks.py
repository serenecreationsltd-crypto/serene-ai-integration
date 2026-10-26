import pytest
from types import SimpleNamespace
from app import security_checks

def test_production_rejects_missing_signing_secret(monkeypatch):
    monkeypatch.setattr(security_checks, "get_settings", lambda: SimpleNamespace(environment="production", jwt_secret="", admin_password="a" * 20, cors_origins=["https://serenecreations.org"]))
    with pytest.raises(RuntimeError, match="JWT_SECRET"):
        security_checks.validate_security_configuration()

def test_production_rejects_weak_admin_password(monkeypatch):
    monkeypatch.setattr(security_checks, "get_settings", lambda: SimpleNamespace(environment="production", jwt_secret="x" * 48, admin_password="", cors_origins=["https://serenecreations.org"]))
    with pytest.raises(RuntimeError, match="ADMIN_PASSWORD"):
        security_checks.validate_security_configuration()

def test_production_rejects_wildcard_origin(monkeypatch):
    monkeypatch.setattr(security_checks, "get_settings", lambda: SimpleNamespace(environment="production", jwt_secret="x" * 48, admin_password="x" * 20, cors_origins=["*"]))
    with pytest.raises(RuntimeError, match="CORS"):
        security_checks.validate_security_configuration()

def test_production_accepts_configured_settings(monkeypatch):
    monkeypatch.setattr(security_checks, "get_settings", lambda: SimpleNamespace(environment="production", jwt_secret="x" * 48, admin_password="x" * 20, cors_origins=["https://serenecreations.org"]))
    assert security_checks.validate_security_configuration() is None
