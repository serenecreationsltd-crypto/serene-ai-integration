import json
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

class Settings(BaseSettings):
    # App config
    app_name: str = "Serene Intelligence"
    app_version: str = "0.2.0"
    environment: str = "development"
    debug: bool = True
    
    # LLM config
    openai_api_key: Optional[str] = None
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000
    
    # Database
    database_url: str = "sqlite:///./serene.db"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Auth
    jwt_secret: str = "your-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Admin
    admin_username: str = "admin"
    admin_password: str = "change-me"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()

@lru_cache()
def load_brand_context() -> dict:
    file_path = DATA_DIR / "brand_context.json"
    if not file_path.exists():
        return {
            "brand_name": "Serene Creations",
            "mission": "Create elegant, human-centered experiences and spaces.",
            "pillars": [
                "Calm luxury",
                "Intentional design",
                "Human experience",
                "Strategic growth",
            ],
            "tone": "Warm, thoughtful, premium, measurable.",
        }

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)
