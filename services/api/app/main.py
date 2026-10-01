from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.activity.logger import ActivityLogger
from services.config.settings import settings
from services.memory import MemoryService
from services.orchestrator import Orchestrator

app = FastAPI(title="OMNIA API", version="0.1.0")
activity_logger = ActivityLogger()
memory_service = MemoryService()
orchestrator = Orchestrator(model_provider=settings.model_provider, activity_logger=activity_logger, memory_service=memory_service)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: str | None = None
    project_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    plan: dict
    tools_used: list[str]
    memory: list[dict]


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "omnia-api"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="message cannot be empty")
    result = await orchestrator.process(request.message, user_id=request.user_id, project_id=request.project_id)
    return ChatResponse(
        response=result.response,
        plan=result.plan,
        tools_used=result.tools_used,
        memory=result.memory,
    )


@app.get("/api/activity")
async def get_activity() -> list[dict]:
    return [event.__dict__ for event in activity_logger.list()]


@app.get("/api/memory")
async def get_memory() -> list[dict]:
    return memory_service.list_memories(limit=20)
