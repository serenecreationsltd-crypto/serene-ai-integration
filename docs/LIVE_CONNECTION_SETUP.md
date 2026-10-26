# Production integration deployment

The merged backend is not automatically hosted by either Serene website.

## Deploy the FastAPI backend
1. Provision a managed PostgreSQL database and a Docker-compatible hosting service.
2. Use the repository Dockerfile; set ENVIRONMENT=production, JWT_SECRET (at least 32 random characters), ADMIN_PASSWORD (at least 16 unique characters), DATABASE_URL and optional OPENAI_API_KEY in the hosting secret manager.
3. Deploy the container, then verify /api/health and deny unauthenticated requests to /api/admin/integrations.
4. Configure an API subdomain with HTTPS, e.g. intelligence.serenecreations.org, after verifying DNS ownership and the host.
5. Point the Studio and public website at the verified API host. Do not expose admin tokens in frontend code.

## Third-party providers
Orbix AI, ROI.dog, AIResearchPlus and PulsR AI remain disabled. Official provider API documentation, approved credentials, API endpoints, data processing permission and provider-specific tests are prerequisites. Do not scrape login pages or invent API endpoints.

## Existing users
Existing administrator records may retain earlier weak passwords. Rotate them explicitly in the database or through a reviewed administrative password-reset flow before production exposure.

## Notes
The Render blueprint is a deployment template only; no Render service or DNS entry is created by committing this file. The database is not provisioned automatically.
