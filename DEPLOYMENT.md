# Serene Intelligence – Production Deployment Guide

This is a full-stack AI assistant integrating the Serene Creations ecosystem with OpenAI LLM support, admin dashboard, and production-ready deployment options.

## Quick Start (Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the server
python main.py
```

Then open:
- Chat: http://localhost:8000/
- Admin Dashboard: http://localhost:8000/dashboard.html (login with admin/change-me)
- API docs: http://localhost:8000/docs

## Production Deployment

### Option 1: Heroku

```bash
# Create Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:$PORT app.server:app" > Procfile

# Deploy
heroku create serene-intelligence
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set DATABASE_URL=postgresql://...
heroku config:set JWT_SECRET=your-random-secret
git push heroku main
```

### Option 2: Railway.app

1. Push repo to GitHub
2. Connect at railway.app
3. Set environment variables:
   - `OPENAI_API_KEY`
   - `DATABASE_URL` (PostgreSQL)
   - `JWT_SECRET`
4. Deploy

### Option 3: Self-hosted (AWS/GCP/DigitalOcean)

```bash
# Using gunicorn + nginx
gunicorn -w 4 -b 0.0.0.0:8000 app.server:app

# Or with Docker
docker build -t serene-intelligence .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... serene-intelligence
```

## Environment Variables

```
# Required
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@host:5432/serene_db
JWT_SECRET=random-secret-key-min-32-chars

# Optional
APP_ENV=production
DEBUG=False
LLM_MODEL=gpt-4o-mini
```

## Database Setup

### PostgreSQL (Recommended for production)

```bash
# Create database
createdb serene_intelligence

# Update .env
DATABASE_URL=postgresql://user:password@localhost:5432/serene_intelligence

# Run the app (tables auto-create)
python main.py
```

## API Endpoints

### Public
- `GET /api/health` – Health check
- `POST /api/chat` – Chat with AI (no auth required)
- `POST /api/auth/login` – Login

### Authenticated
- `GET /api/conversations` – List conversations
- `GET /api/conversations/{id}` – Get conversation detail

### Admin Only
- `GET /api/admin/dashboard` – Dashboard stats
- `GET /api/admin/knowledge-base` – List KB items
- `POST /api/admin/knowledge-base` – Add KB item

## Integration with serenecreations.org

### Option A: Embed Chat Widget

Add to your website HTML:

```html
<div id="serene-chat-widget"></div>
<script src="https://your-domain.com/widget.js"></script>
```

### Option B: iFrame Integration

```html
<iframe 
  src="https://your-domain.com/" 
  width="400" 
  height="600" 
  frameborder="0">
</iframe>
```

### Option C: API Integration

```javascript
const response = await fetch('https://your-domain.com/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Your question here' })
});
const data = await response.json();
console.log(data.answer);
```

## Admin Credentials

**Default (CHANGE IN PRODUCTION):**
- Username: `admin`
- Password: `change-me`

**To update:**

1. Login at `/login.html`
2. Access dashboard at `/dashboard.html`
3. Change password in settings

## Next Steps

1. **Expand Knowledge Base** – Add project descriptions, case studies, services
2. **Custom LLM Model** – Fine-tune on Serene Creations brand data
3. **Analytics** – Track user questions, sentiment, conversion
4. **Integrations** – Connect to Notion, Slack, CRM, email
5. **Monetization** – Premium support, API tier, business intelligence

## Support

For issues or questions, check the repository or contact the development team.
