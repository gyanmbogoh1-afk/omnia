from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ActivityEvent:
    timestamp: str
    action: str
    component: str
    metadata: dict[str, Any] = field(default_factory=dict)
    success: bool = True


class ActivityLogger:
    def __init__(self) -> None:
        self.events: list[ActivityEvent] = []

    def log(self, *, action: str, component: str, metadata: dict[str, Any] | None = None, success: bool = True) -> ActivityEvent:
        event = ActivityEvent(
            timestamp="now",
            action=action,
            component=component,
            metadata=metadata or {},
            success=success,
        )
        self.events.append(event)
        return event

    def list(self) -> list[ActivityEvent]:
        return list(self.events)


__all__ = ["ActivityEvent", "ActivityLogger"]
