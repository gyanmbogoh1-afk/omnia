from __future__ import annotations

import json
from typing import Any

from services.activity.logger import ActivityLogger
from services.tools.base import ToolRegistry
from services.tools.calculator import CalculatorTool
from services.tools.sandbox import PythonSandboxTool


class ToolExecutor:
    def __init__(self, registry: ToolRegistry | None = None, activity_logger: ActivityLogger | None = None) -> None:
        self.registry = registry or ToolRegistry()
        self.activity_logger = activity_logger or ActivityLogger()
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        self.registry.register(CalculatorTool())
        self.registry.register(PythonSandboxTool())

    async def run(self, tool_name: str, **kwargs: Any) -> Any:
        tool = self.registry.get(tool_name)
        self.activity_logger.log(
            action="tool.requested",
            component="tool_system",
            metadata={"tool": tool_name, "args": kwargs},
            success=True,
        )
        try:
            result = await tool.execute(**kwargs)
            self.activity_logger.log(
                action="tool.completed",
                component="tool_system",
                metadata={"tool": tool_name, "result": result},
                success=True,
            )
            return result
        except Exception as exc:
            error_payload = {"tool": tool_name, "error": str(exc)}
            self.activity_logger.log(
                action="tool.failed",
                component="tool_system",
                metadata=error_payload,
                success=False,
            )
            raise


__all__ = ["ToolExecutor"]
