# Serene AI Integration

Full-stack AI assistant that integrates all serenecreations.org buildup into one unified intelligence platform.

## Features

✅ **Public Chat Interface** – Users ask questions about Serene Creations
✅ **OpenAI LLM Integration** – Real-time AI responses with brand context
✅ **Admin Dashboard** – Manage conversations, knowledge base, and analytics
✅ **Authentication** – JWT-based auth with admin controls
✅ **Conversation History** – Persistent conversation tracking
✅ **Knowledge Base** – Curated brand and business context
✅ **Production-Ready** – Database persistence, CORS, error handling

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add OPENAI_API_KEY

# Run
python main.py
```

Open http://localhost:8000/

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production guides (Heroku, Railway, AWS, Docker).

## Admin Dashboard

Access at http://localhost:8000/dashboard.html

**Login:** admin / change-me (change in production!)

## API Documentation

View interactive docs at http://localhost:8000/docs

## Architecture

```
serene-ai-integration/
├── app/
│   ├── server.py       # FastAPI app
│   ├── routes.py       # API endpoints
│   ├── database.py     # SQLAlchemy models
│   ├── llm.py          # OpenAI integration
│   ├── auth.py         # JWT authentication
│   ├── config.py       # Settings
│   ├── schemas.py      # Pydantic models
│   └── static/
│       ├── index.html  # Chat UI
│       ├── dashboard.html  # Admin panel
│       ├── login.html  # Auth page
│       ├── styles.css
│       ├── app.js
│       └── dashboard.js
├── data/
│   └── brand_context.json  # Brand knowledge
├── main.py
├── requirements.txt
├── .env.example
└── DEPLOYMENT.md
```

## Environment Variables

```
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite:///./serene.db  # or postgresql://...
JWT_SECRET=your-secret-key
APP_ENV=development|production
```

## Integration with serenecreations.org

1. **Chat Widget** – Embed in website
2. **iFrame** – Display in sidebar
3. **API** – Integrate backend-to-backend
4. **Standalone** – Run as separate app at intelligence.serenecreations.org

## Next Steps

- Deploy to production
- Add your brand context to `data/brand_context.json`
- Connect to CRM/CMS/project management tools
- Fine-tune LLM on your specific business data
- Set up analytics and user feedback

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).
