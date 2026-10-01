from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaskPlan:
    task: str
    steps: list[str] = field(default_factory=list)
    complexity: str = "low"


class Planner:
    def plan(self, prompt: str) -> TaskPlan:
        normalized = prompt.lower()
        steps = ["understand request", "select model", "run relevant tools if needed", "compose response"]
        if "calculate" in normalized or "math" in normalized:
            steps = ["understand calculation", "identify formula", "solve with tool", "verify result", "explain assumptions"]
        if "research" in normalized or "science" in normalized or "theoretical" in normalized:
            steps = ["frame question", "retrieve relevant knowledge", "check evidence", "summarize uncertainty", "answer with caveats"]
        complexity = "high" if any(token in normalized for token in ["research", "science", "theory", "optimize", "experiment", "simulation"]) else "low"
        return TaskPlan(task=prompt, steps=steps, complexity=complexity)


__all__ = ["TaskPlan", "Planner"]
