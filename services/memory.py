from __future__ import annotations

from typing import Any, Protocol


class MemoryStore(Protocol):
    def add(self, memory: dict[str, Any]) -> dict[str, Any]:
        ...

    def list(self, *, limit: int = 20) -> list[dict[str, Any]]:
        ...


class InMemoryMemoryStore:
    def __init__(self) -> None:
        self._items: list[dict[str, Any]] = []

    def add(self, memory: dict[str, Any]) -> dict[str, Any]:
        self._items.append(memory)
        return memory

    def list(self, *, limit: int = 20) -> list[dict[str, Any]]:
        return list(self._items)[-limit:]


class MemoryService:
    def __init__(self, store: MemoryStore | None = None) -> None:
        self.store = store or InMemoryMemoryStore()

    def save_memory(self, *, kind: str, content: str, source: str | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        memory = {
            "id": f"mem-{len(self.store.list()) + 1}",
            "type": kind,
            "content": content,
            "source": source,
            "metadata": metadata or {},
        }
        return self.store.add(memory)

    def list_memories(self, *, limit: int = 20) -> list[dict[str, Any]]:
        return self.store.list(limit=limit)


__all__ = ["MemoryService", "InMemoryMemoryStore"]
