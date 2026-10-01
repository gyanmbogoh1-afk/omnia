"""Main FastAPI application with Supabase integration."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from services.activity.logger import ActivityLogger
from services.config.settings import settings
from services.database.service import (
    ActivityEventService,
    ConversationService,
    MemoryService as SupabaseMemoryService,
    MessageService,
    UserService,
)
from services.database.supabase import get_supabase_manager
from services.memory import MemoryService
from services.orchestrator import Orchestrator

app = FastAPI(
    title="OMNIA API",
    version="0.1.0",
    description="Universal Research Intelligence Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase_manager = get_supabase_manager()
activity_logger = ActivityLogger()
memory_service = MemoryService()
orchestrator = Orchestrator(
    model_provider=settings.model_provider,
    activity_logger=activity_logger,
    memory_service=memory_service,
)

user_service = UserService(supabase_manager)
conversation_service = ConversationService(supabase_manager)
message_service = MessageService(supabase_manager)
supabase_memory_service = SupabaseMemoryService(supabase_manager)
activity_event_service = ActivityEventService(supabase_manager)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: str | None = None
    project_id: str | None = None
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    plan: dict
    tools_used: list[str]
    memory: list[dict]
    conversation_id: str | None = None
    message_id: str | None = None


class ConversationCreateRequest(BaseModel):
    user_id: str
    title: str | None = None
    project_id: str | None = None


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    project_id: str | None = None
    created_at: str | None = None


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "omnia-api"}


@app.get("/health/supabase")
async def health_supabase() -> dict[str, str | bool]:
    """Check Supabase connectivity."""
    result = await supabase_manager.health_check()
    return result


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message and return response with planning and tool execution info."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="message cannot be empty")

    result = await orchestrator.process(
        request.message, user_id=request.user_id, project_id=request.project_id
    )

    # Log to Supabase if enabled
    if supabase_manager.is_enabled() and request.user_id:
        await activity_event_service.log_event(
            user_id=request.user_id,
            action="chat.message",
            component="api",
            metadata={"message_length": len(request.message), "tools_used": result.tools_used},
            success=True,
        )

    return ChatResponse(
        response=result.response,
        plan=result.plan,
        tools_used=result.tools_used,
        memory=result.memory,
        conversation_id=request.conversation_id,
    )


@app.post("/api/conversations", response_model=ConversationResponse)
async def create_conversation(request: ConversationCreateRequest) -> ConversationResponse:
    """Create a new conversation."""
    conversation = await conversation_service.create_conversation(
        user_id=request.user_id,
        project_id=request.project_id,
        title=request.title,
    )
    return ConversationResponse(
        id=conversation.get("id", ""),
        user_id=conversation.get("user_id", request.user_id),
        title=conversation.get("title", request.title or "Untitled"),
        project_id=conversation.get("project_id"),
        created_at=conversation.get("created_at"),
    )


@app.get("/api/conversations/{user_id}")
async def list_conversations(user_id: str, limit: int = 50) -> list[ConversationResponse]:
    """List conversations for a user."""
    conversations = await conversation_service.list_conversations(user_id, limit=limit)
    return [
        ConversationResponse(
            id=conv.get("id", ""),
            user_id=conv.get("user_id", user_id),
            title=conv.get("title", "Untitled"),
            project_id=conv.get("project_id"),
            created_at=conv.get("created_at"),
        )
        for conv in conversations
    ]


@app.get("/api/activity")
async def get_activity(user_id: str | None = None, limit: int = 100) -> list[dict]:
    """Get activity events."""
    if supabase_manager.is_enabled():
        events = await activity_event_service.list_events(user_id=user_id, limit=limit)
        return events
    return [event.__dict__ for event in activity_logger.list()]


@app.get("/api/memory")
async def get_memory(user_id: str | None = None, limit: int = 20) -> list[dict]:
    """Get memory items."""
    if supabase_manager.is_enabled() and user_id:
        memories = await supabase_memory_service.list_memories(user_id=user_id, limit=limit)
        return memories
    return memory_service.list_memories(limit=limit)
