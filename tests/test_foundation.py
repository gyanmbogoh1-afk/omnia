import pytest

from services.activity.logger import ActivityLogger
from services.memory import MemoryService
from services.models.provider import get_model_provider
from services.orchestrator import Orchestrator


@pytest.mark.asyncio
async def test_model_provider_returns_text() -> None:
    provider = get_model_provider("inmemory")
    response = await provider.generate([{"role": "user", "content": "hello"}])
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_orchestrator_handles_prompt() -> None:
    orchestrator = Orchestrator(model_provider="inmemory", activity_logger=ActivityLogger(), memory_service=MemoryService())
    result = await orchestrator.process("Calculate a simple expression.")
    assert isinstance(result.response, str)
    assert "plan" in result.plan


def test_memory_store_roundtrip() -> None:
    service = MemoryService()
    service.save_memory(kind="working", content="a note")
    memories = service.list_memories(limit=10)
    assert len(memories) >= 1


@pytest.mark.asyncio
async def test_tool_executor_runs_calculator() -> None:
    from services.tools import ToolExecutor

    tool_executor = ToolExecutor()
    value = await tool_executor.run("calculator", expression="2 + 3 * 4")
    assert value == 14.0


@pytest.mark.asyncio
async def test_activity_logger_records_event() -> None:
    logger = ActivityLogger()
    event = logger.log(action="test.action", component="tests", success=True)
    assert event.action == "test.action"
    assert logger.list()[-1].action == "test.action"
