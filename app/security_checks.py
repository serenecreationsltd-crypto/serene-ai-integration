"""Fail closed when production authentication settings are missing."""
from app.config import get_settings
import os

def validate_security_configuration():
    settings = get_settings()
    if settings.environment.lower() == "production":
        if len(settings.jwt_secret) < 32:
            raise RuntimeError("Set JWT_SECRET to a strong random value before production startup")
        if len(settings.admin_password) < 16:
            raise RuntimeError("Set ADMIN_PASSWORD before production startup")
        if len(os.environ.get("GATEWAY_SERVER_TOKEN", "")) < 32:
            raise RuntimeError("Set GATEWAY_SERVER_TOKEN to a strong secret before production startup")
        if not settings.cors_origins or "*" in settings.cors_origins:
            raise RuntimeError("Explicit trusted CORS origins are required")
