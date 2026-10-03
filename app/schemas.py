from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime
    confidence: Optional[float] = None
    source: str

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    archived: bool
    message_count: int

class ConversationDetailResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    archived: bool
    messages: List[ChatResponse]

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    is_admin: bool
    is_active: bool
    created_at: datetime

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class KnowledgeBaseItem(BaseModel):
    id: Optional[int] = None
    category: str
    key: str
    value: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DashboardStats(BaseModel):
    total_conversations: int
    total_messages: int
    active_users: int
    llm_calls_today: int
    average_response_time_ms: float
