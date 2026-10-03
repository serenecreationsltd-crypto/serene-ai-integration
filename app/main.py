import json
import re
from typing import Dict, List

from app.config import load_brand_context


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def generate_answer(question: str) -> str:
    context = load_brand_context()
    q = _normalize(question)

    if not q:
        return "Please ask a question about the Serene Creations ecosystem."

    if any(keyword in q for keyword in ["brand", "vision", "mission", "purpose"]):
        return (
            f"{context.get('brand_name', 'Serene Creations')} is guided by the mission: "
            f"{context.get('mission', 'create inspired human experiences.')}. "
            f"The core pillars are: {', '.join(context.get('pillars', []))}."
        )

    if any(keyword in q for keyword in ["tone", "voice", "style", "identity"]):
        return f"The brand tone is {context.get('tone', 'thoughtful and premium.')}."

    if any(keyword in q for keyword in ["what", "who", "company", "business"]):
        return (
            f"{context.get('brand_name', 'Serene Creations')} operates as a design-forward business focused on "
            "beautiful, strategic, human-centered growth across architecture, storytelling, and digital experiences."
        )

    if any(keyword in q for keyword in ["service", "offer", "product", "what do you do"]):
        return (
            "The ecosystem combines architecture, branding, strategic design, and digital experiences into "
            "one unified business model that turns vision into memorable experiences."
        )

    if any(keyword in q for keyword in ["design", "architecture", "creative"]):
        return (
            "The design layer focuses on intentional spatial and visual systems, blending aesthetic clarity with "
            "practical function and meaningful human experience."
        )

    if any(keyword in q for keyword in ["integration", "system", "platform", "ai"]):
        return (
            "The AI integration vision is to combine brand knowledge, project context, customer signals, and internal workflows into "
            "one intelligent operating layer for the business."
        )

    return (
        "Based on the available Serene Creations context, the platform is designed to unify brand identity, design strategy, "
        "and business operations into one intelligent system. Ask about the brand, design philosophy, business model, or AI integration."
    )
