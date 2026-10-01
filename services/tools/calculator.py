from __future__ import annotations

from typing import Any

from services.tools.base import Tool, ToolDefinition


class CalculatorTool(Tool):
    definition = ToolDefinition(
        name="calculator",
        description="Safely evaluate arithmetic expressions.",
        input_schema={
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
        risk_level="low",
        permissions=["math"],
    )

    async def execute(self, **kwargs: Any) -> Any:
        expression = kwargs.get("expression")
        if not isinstance(expression, str):
            raise ValueError("expression must be a string")
        allowed_characters = set("0123456789+-*/(). ")
        if any(ch not in allowed_characters for ch in expression):
            raise ValueError("expression contains unsupported characters")
        try:
            result = eval(expression, {"__builtins__": {}}, {})
        except Exception as exc:  # pragma: no cover - unsafe eval guard
            raise ValueError(f"invalid arithmetic expression: {exc}") from exc
        return result
