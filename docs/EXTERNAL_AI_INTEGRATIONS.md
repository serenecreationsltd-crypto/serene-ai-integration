# External AI integration readiness

Target properties: serenecreations.org and serene-ai.serenecreations.org/studio.

This repository provides a backend integration registry. No direct API connectivity is claimed or enabled until the provider supplies verified API documentation, credentials and usage authorization.

## Provider readiness
- Orbix AI — https://www.orbixai.com/ — ORBIXAI_API_KEY (unverified)
- ROI.dog — https://roi.dog/ — ROIDOG_API_KEY (unverified); Google Ads permissions require a separately approved OAuth flow
- AIResearchPlus — https://airesearchplus.com/ — AIRESEARCHPLUS_API_KEY (unverified)
- PulsR AI — https://pulsrai.com/ — PULSRAI_API_KEY (unverified)

All provider credentials must be stored in server-side secret storage, never in browser JavaScript, commits or logs.

## Integration endpoint
GET /api/admin/integrations requires an authenticated administrator. It returns metadata and secret-presence booleans, not secrets. All integrations are disabled by default.

## Production prerequisites
1. Obtain official API documentation, base URLs, OAuth requirements and terms for each provider.
2. Verify provider identity and authorization; implement allowlisted server-side adapters with request timeout, rate limits and audit logging.
3. Review existing default admin password, JWT secret, CORS wildcard and public chat endpoint before production.
4. Deploy backend to a trusted host, expose its URL through the studio and website, and run end-to-end smoke tests.
5. Obtain permission before transmitting customer documents or advertising account data to third parties.
