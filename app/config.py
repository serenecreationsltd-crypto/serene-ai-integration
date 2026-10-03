from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

@dataclass
class AppSettings:
    app_name: str = "Serene Intelligence"
    app_version: str = "0.1.0"
    environment: str = "development"
    openai_api_key: str | None = None

@lru_cache
def get_settings() -> AppSettings:
    import os
    return AppSettings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        environment=os.getenv("APP_ENV", "development"),
    )

@lru_cache
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
