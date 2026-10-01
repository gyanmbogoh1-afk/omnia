from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ToolDefinition:
    def __init__(self, name: str, description: str, input_schema: dict[str, Any], risk_level: str, permissions: list[str]) -> None:
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.risk_level = risk_level
        self.permissions = permissions


class Tool(ABC):
    definition: ToolDefinition

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError


class ToolRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.definition.name] = tool

    def get(self, name: str) -> Tool:
        return self.tools[name]

    def list(self) -> list[Tool]:
        return list(self.tools.values())
