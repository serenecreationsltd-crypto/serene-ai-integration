from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.config import get_settings
from app.routes import router
from app.provider_gateway import router as integrations_router
from app.database import get_db
from app.auth import create_admin_user
from sqlalchemy.orm import Session

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
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
