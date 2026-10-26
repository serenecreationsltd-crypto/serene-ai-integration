"""Safe registry for external AI services. No unverified API calls."""
import os
from fastapi import APIRouter, Depends
from app.auth import get_admin_user

router = APIRouter(prefix="/api/admin/integrations", tags=["integrations"])
PROVIDERS = {
    "orbixai": {"name": "Orbix AI", "website": "https://www.orbixai.com/", "key_env": "ORBIXAI_API_KEY"},
    "roidog": {"name": "ROI.dog", "website": "https://roi.dog/", "key_env": "ROIDOG_API_KEY"},
    "airesearchplus": {"name": "AIResearchPlus", "website": "https://airesearchplus.com/", "key_env": "AIRESEARCHPLUS_API_KEY"},
    "pulsrai": {"name": "PulsR AI", "website": "https://pulsrai.com/", "key_env": "PULSRAI_API_KEY"},
}

@router.get("")
def list_integrations(admin=Depends(get_admin_user)):
    """Admin-only configuration status; never expose credentials."""
    return [
        {
            "id": key,
            "name": p["name"],
            "website": p["website"],
            "credential_configured": bool(os.getenv(p["key_env"])),
            "api_verified": False,
            "enabled": False,
            "status": "awaiting_official_api_documentation_and_authorization",
        }
        for key, p in PROVIDERS.items()
    ]
