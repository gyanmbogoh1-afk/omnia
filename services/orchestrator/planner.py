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
        text = prompt.lower()
        steps = ["understand request", "select model", "run relevant tools if needed", "compose final answer"]
        if "calculate" in text or "math" in text:
            steps = ["understand calculation", "identify formula", "solve with tool or logic", "verify result", "explain assumptions"]
        if "research" in text or "science" in text:
            steps = ["frame question", "retrieve relevant knowledge", "check evidence", "summarize uncertainty", "answer with caveats"]
        complexity = "high" if any(k in text for k in ["research", "science", "optimize", "model", "experiment"]) else "low"
        return TaskPlan(task=prompt, steps=steps, complexity=complexity)
