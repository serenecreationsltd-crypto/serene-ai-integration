# Deployment checklist for Serene AI provider gateway

## Current state
The four external providers are listed but disabled. This code does not call their APIs.

## Required environment
- ADMIN_PASSWORD: unique, strong initial administrator password (at least 16 characters).
- JWT_SECRET: securely generated signing key. Do not reuse keys from other systems.
- DATABASE_URL: managed database URL for production.
- CORS_ORIGINS: JSON list of trusted website origins.

## Before merge
- Validate FastAPI startup and route authorization in CI.
- Review production JWT and administrator password requirements.
- Rotate any previously exposed credentials and review existing administrator records.
- Verify external provider API documentation and obtain explicit authorization.
- Check both websites' actual source repositories and hosting before adding UI elements.

## Before deployment
- Configure environment secrets on the hosting provider.
- Confirm that the public website and AI Studio use the intended backend URL.
- Run smoke tests for /api/health and authenticated /api/admin/integrations.
- Confirm unauthorized users cannot access admin routes.
- Keep provider adapters disabled until verified.
