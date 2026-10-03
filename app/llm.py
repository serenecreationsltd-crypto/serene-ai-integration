from openai import OpenAI
from app.config import get_settings
from typing import Optional
import json

settings = get_settings()

class LLMService:
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set. Set it in .env file.")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens
    
    def chat_with_context(
        self,
        messages: list,
        system_context: str = "",
        temperature: Optional[float] = None
    ) -> dict:
        """Send messages to OpenAI with optional system context."""
        if temperature is None:
            temperature = self.temperature
        
        system_message = {
            "role": "system",
            "content": system_context or self._get_default_system_prompt()
        }
        
        all_messages = [system_message] + messages
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=all_messages,
            temperature=temperature,
            max_tokens=self.max_tokens,
        )
        
        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "finish_reason": response.choices[0].finish_reason,
        }
    
    def _get_default_system_prompt(self) -> str:
        return """You are Serene Intelligence, an AI assistant for Serene Creations.

Serene Creations is a design-forward business focused on elegant, human-centered experiences.

Key brand attributes:
- Mission: Create elegant, human-centered experiences that blend design, strategy, and meaningful transformation
- Tone: Warm, thoughtful, premium, intentional, and measurable
- Core focus: Architecture, brand identity, digital experiences, business operations
- Values: Calm luxury, intentional design, human experience, strategic growth

Your role:
1. Answer questions about the Serene Creations ecosystem with expertise and warmth
2. Provide strategic advice on design, branding, and business operations
3. Maintain the brand voice in all communications
4. Be helpful, specific, and grounded in real business value
5. If you don't know something specific, be honest and suggest where to find that information

Always prioritize clarity, brand consistency, and actionable insights."""
    
    def generate_embedding(self, text: str) -> list:
        """Generate embeddings for semantic search."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

llm_service = LLMService() if settings.openai_api_key else None
