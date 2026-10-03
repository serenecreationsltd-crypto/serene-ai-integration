from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import (
    Conversation, Message, User, KnowledgeBase, get_db
)
from app.schemas import (
    ChatRequest, ChatResponse, ConversationResponse, ConversationDetailResponse,
    UserLogin, AuthResponse, UserResponse, KnowledgeBaseItem, DashboardStats
)
from app.auth import (
    hash_password, verify_password, create_access_token, get_current_user,
    get_admin_user, create_admin_user
)
from app.llm import llm_service
from app.config import load_brand_context
from typing import List
import json

router = APIRouter()

# ============= PUBLIC ENDPOINTS =============

@router.get("/api/health")
def health():
    return {"status": "ok", "service": "Serene Intelligence", "version": "0.2.0"}

@router.post("/api/auth/login", response_model=AuthResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(user.id, user.is_admin)
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at,
        )
    )

@router.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Public chat endpoint (uses LLM if available)."""
    conversation_id = request.conversation_id
    
    # Get or create conversation
    if conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
    else:
        conversation = Conversation(
            user_id="public",
            title=request.message[:50],
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    
    # Store user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
        source="user_input"
    )
    db.add(user_message)
    db.commit()
    
    # Generate response
    if llm_service:
        # Use OpenAI if available
        brand_context = load_brand_context()
        system_prompt = f"""You are Serene Intelligence, assistant for {brand_context['brand_name']}.
Mission: {brand_context['mission']}
Tone: {brand_context['tone']}"""
        
        messages = [{"role": "user", "content": request.message}]
        llm_response = llm_service.chat_with_context(messages, system_prompt)
        response_content = llm_response["content"]
        source = "llm"
    else:
        # Fallback to local knowledge
        response_content = _generate_local_response(request.message)
        source = "local_kb"
    
    # Store assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response_content,
        source=source
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    
    return ChatResponse(
        id=assistant_message.id,
        role="assistant",
        content=response_content,
        timestamp=assistant_message.timestamp,
        source=source
    )

# ============= AUTHENTICATED USER ENDPOINTS =============

@router.get("/api/conversations", response_model=List[ConversationResponse])
def list_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(
        Conversation.user_id == str(current_user.id),
        Conversation.archived == False
    ).order_by(Conversation.updated_at.desc()).all()
    
    return [
        ConversationResponse(
            id=c.id,
            title=c.title,
            created_at=c.created_at,
            updated_at=c.updated_at,
            archived=c.archived,
            message_count=db.query(func.count(Message.id)).filter(
                Message.conversation_id == c.id
            ).scalar()
        )
        for c in conversations
    ]

@router.get("/api/conversations/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation(conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == str(current_user.id)
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp).all()
    
    return ConversationDetailResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        archived=conversation.archived,
        messages=[
            ChatResponse(
                id=m.id,
                role=m.role,
                content=m.content,
                timestamp=m.timestamp,
                confidence=m.confidence,
                source=m.source
            )
            for m in messages
        ]
    )

# ============= ADMIN ENDPOINTS =============

@router.get("/api/admin/dashboard", response_model=DashboardStats)
def get_dashboard(admin_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    total_conversations = db.query(func.count(Conversation.id)).scalar()
    total_messages = db.query(func.count(Message.id)).scalar()
    active_users = db.query(func.count(func.distinct(Conversation.user_id))).scalar()
    
    today = datetime.utcnow().date()
    llm_calls_today = db.query(func.count(Message.id)).filter(
        Message.source == "llm",
        func.date(Message.timestamp) == today
    ).scalar()
    
    return DashboardStats(
        total_conversations=total_conversations or 0,
        total_messages=total_messages or 0,
        active_users=active_users or 0,
        llm_calls_today=llm_calls_today or 0,
        average_response_time_ms=45.2,
    )

@router.get("/api/admin/knowledge-base", response_model=List[KnowledgeBaseItem])
def list_knowledge_base(admin_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    items = db.query(KnowledgeBase).all()
    return [
        KnowledgeBaseItem(
            id=item.id,
            category=item.category,
            key=item.key,
            value=item.value,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in items
    ]

@router.post("/api/admin/knowledge-base", response_model=KnowledgeBaseItem)
def create_knowledge_item(item: KnowledgeBaseItem, admin_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    db_item = KnowledgeBase(
        category=item.category,
        key=item.key,
        value=item.value,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return KnowledgeBaseItem(
        id=db_item.id,
        category=db_item.category,
        key=db_item.key,
        value=db_item.value,
        created_at=db_item.created_at,
        updated_at=db_item.updated_at,
    )

# ============= HELPER FUNCTIONS =============

def _generate_local_response(question: str) -> str:
    """Fallback local knowledge response."""
    context = load_brand_context()
    q = question.lower()
    
    if any(keyword in q for keyword in ["brand", "vision", "mission"]):
        return f"{context['brand_name']} mission: {context['mission']}"
    
    return "I'm learning about Serene Creations. Please ask about the brand, design, or business."
