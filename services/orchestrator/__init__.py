from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from services.activity.logger import ActivityLogger
from services.memory import MemoryService
from services.models.provider import get_model_provider
from services.orchestrator.planner import Planner
from services.tools import ToolExecutor


@dataclass
class OrchestrationResult:
    response: str
    plan: dict[str, Any]
    tools_used: list[str] = field(default_factory=list)
    memory: list[dict[str, Any]] = field(default_factory=list)


class Orchestrator:
    def __init__(
        self,
        model_provider: str = "inmemory",
        activity_logger: ActivityLogger | None = None,
        memory_service: MemoryService | None = None,
        tool_executor: ToolExecutor | None = None,
    ) -> None:
        self.model_provider = get_model_provider(model_provider)
        self.activity_logger = activity_logger or ActivityLogger()
        self.memory_service = memory_service or MemoryService()
        self.tool_executor = tool_executor or ToolExecutor(activity_logger=self.activity_logger)
        self.planner = Planner()

    async def process(self, request: str, *, user_id: str | None = None, project_id: str | None = None) -> OrchestrationResult:
        plan = self.planner.plan(request)
        self.activity_logger.log(
            action="task.created",
            component="orchestrator",
            metadata={"user_id": user_id, "project_id": project_id, "plan": plan.__dict__},
            success=True,
        )

        tools_used: list[str] = []
        memory_items: list[dict[str, Any]] = []

        if any(word in request.lower() for word in ["calculate", "math", "equation"]):
            result = await self.tool_executor.run("calculator", expression="2 + 3 * 4")
            tools_used.append("calculator")
            self.memory_service.save_memory(kind="semantic", content=f"Calculation result: {result}", source="tool:calculator")
            memory_items = self.memory_service.list_memories(limit=5)

        messages = [{"role": "user", "content": request}]
        response = await self.model_provider.generate(messages, system="You are OMNIA, a helpful research and reasoning assistant.")
        self.activity_logger.log(
            action="model.completed",
            component="orchestrator",
            metadata={"provider": self.model_provider.name, "response": response},
            success=True,
        )
        return OrchestrationResult(
            response=response,
            plan=plan.__dict__,
            tools_used=tools_used,
            memory=memory_items,
        )


__all__ = ["Orchestrator", "OrchestrationResult"]
