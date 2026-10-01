from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class AgentRun:
    role: str
    instructions: str
    model: str
    metadata: dict[str, Any] = field(default_factory=dict)


class Agent(Protocol):
    role: str
    instructions: str
    model: str

    async def execute(self, prompt: str) -> str:
        ...


class GeneralAgent:
    role = "general"
    instructions = "Answer directly, be concise, and explain assumptions when needed."
    model = "inmemory"

    async def execute(self, prompt: str) -> str:
        return f"GeneralAgent handled: {prompt}"


class ResearchAgent:
    role = "research"
    instructions = "Gather background knowledge, highlight uncertainty, and preserve source metadata."
    model = "inmemory"

    async def execute(self, prompt: str) -> str:
        return f"ResearchAgent processed: {prompt}"


class CodingAgent:
    role = "coding"
    instructions = "Prefer precise, testable implementation steps and verify behavior."
    model = "inmemory"

    async def execute(self, prompt: str) -> str:
        return f"CodingAgent processed: {prompt}"


class MathematicsAgent:
    role = "mathematics"
    instructions = "Prefer explicit equations and verification over unsupported claims."
    model = "inmemory"

    async def execute(self, prompt: str) -> str:
        return f"MathematicsAgent processed: {prompt}"


class CriticAgent:
    role = "critic"
    instructions = "Check for unsupported claims, missing evidence, and uncertain assumptions."
    model = "inmemory"

    async def execute(self, prompt: str) -> str:
        return f"CriticAgent reviewed: {prompt}"
