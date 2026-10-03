# serene-ai-integration

AI model that integrates all serenecreations.org buildup — a unified intelligence layer for architecture, design, content, and business operations.

## What this repo contains

This repository is an MVP foundation for a `Serene Intelligence` platform that can:

- unify brand, creative, and business context
- answer questions using a curated knowledge base
- provide a chat interface for internal/external use
- scale toward integrations with CRM, CMS, sales, and project workflows

## Architecture

- Backend: FastAPI API
- Frontend: lightweight chat UI served from the same app
- Knowledge layer: curated brand and business context in `data/brand_context.json`
- AI strategy: local-first reasoning with optional OpenAI integration in the future

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- http://localhost:8000/
- http://localhost:8000/api/health

## Example API call

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is the brand vision of serenecreations.org?"}'
```

## Next steps

1. Add a real vector database or embeddings store
2. Connect CMS/CRM/Notion/Slack integrations
3. Add authenticated admin dashboard
4. Expand knowledge base to cover projects, services, and sales workflows
5. Add LLM integration with Azure OpenAI or OpenAI

## License

MIT
