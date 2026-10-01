from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence


class ModelProvider(ABC):
    name: str = "base"

    @abstractmethod
    async def generate(
        self,
        messages: Sequence[dict[str, str]],
        *,
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        stream: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        raise NotImplementedError


class InMemoryModelProvider(ModelProvider):
    name = "inmemory"

    async def generate(
        self,
        messages: Sequence[dict[str, str]],
        *,
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        stream: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        prompt = "\n".join(f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages)
        lower = prompt.lower()

        if "calculate" in lower or "math" in lower:
            return "I can help with the calculation. Please provide the exact expression or formula."
        if "time dilation" in lower or "0.99c" in lower:
            return (
                "Time dilation follows from special relativity: a moving clock runs slower by a factor "
                "gamma = 1 / sqrt(1 - v^2 / c^2). At v = 0.99c, gamma ≈ 7.09, so one Earth year corresponds "
                "to about 0.141 years of proper time for the spacecraft."
            )
        return (
            "This is a mock OMNIA model response designed for architecture validation, orchestration flow, "
            "and test automation."
        )


class OpenAIProvider(ModelProvider):
    name = "openai"

    async def generate(
        self,
        messages: Sequence[dict[str, str]],
        *,
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        stream: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        return "OpenAI provider is configured via environment variables and not yet connected in this foundation build."


PROVIDERS = {
    "inmemory": InMemoryModelProvider,
    "mock": InMemoryModelProvider,
    "openai": OpenAIProvider,
}


def get_model_provider(name: str | None = None) -> ModelProvider:
    provider_name = (name or "inmemory").lower()
    provider_cls = PROVIDERS.get(provider_name)
    if provider_cls is None:
        raise ValueError(f"Unsupported model provider: {provider_name}")
    return provider_cls()


__all__ = ["ModelProvider", "InMemoryModelProvider", "OpenAIProvider", "get_model_provider"]
