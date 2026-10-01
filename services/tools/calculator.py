from __future__ import annotations

import ast
import operator
from typing import Any

from services.tools.base import Tool, ToolDefinition


_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


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
        permissions=["math"]
    )

    async def execute(self, **kwargs: Any) -> Any:
        expression = kwargs.get("expression")
        if not isinstance(expression, str):
            raise ValueError("expression must be a string")
        return self._safe_eval(expression)

    def _safe_eval(self, expression: str) -> float:
        tree = ast.parse(expression, mode="eval")
        return self._eval_node(tree.body)

    def _eval_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = _ALLOWED_BINOPS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op(left, right)
        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op = _ALLOWED_UNARYOPS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op(operand)
        if isinstance(node, ast.Call):
            raise ValueError("Function calls are not allowed")
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")
