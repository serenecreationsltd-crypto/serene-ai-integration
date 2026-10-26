from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import secrets
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.config import get_settings
from app.routes import router
from app.provider_gateway import router as integrations_router
from app.database import get_db
from app.auth import create_admin_user
from app.security_checks import validate_security_configuration
from sqlalchemy.orm import Session

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    validate_security_configuration()
    db: Session = next(get_db())
    create_admin_user(db)
    db.close()
    print(f"Serene Intelligence {settings.app_version} started")
    yield
    # Shutdown
    print("Serene Intelligence shutting down")

app = FastAPI(
    title="Serene Intelligence",
    description="AI assistant integrating the Serene Creations ecosystem",
    version=settings.app_version,
    lifespan=lifespan,
)

@app.middleware("http")
async def protect_public_chat(request: Request, call_next):
    if request.url.path == "/api/chat" and settings.environment.lower() == "production":
        expected = os.environ.get("GATEWAY_SERVER_TOKEN", "")
        received = request.headers.get("X-Gateway-Token", "")
        if not expected or not secrets.compare_digest(received, expected):
            return JSONResponse({"detail": "Gateway authorization required"}, status_code=401)
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(integrations_router)

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
