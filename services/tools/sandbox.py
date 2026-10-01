from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from services.tools.base import Tool, ToolDefinition


class PythonSandboxTool(Tool):
    definition = ToolDefinition(
        name="python_sandbox",
        description="Execute isolated Python snippets with time and resource limits.",
        input_schema={
            "type": "object",
            "properties": {"code": {"type": "string"}},
            "required": ["code"],
        },
        risk_level="medium",
        permissions=["sandbox"]
    )

    async def execute(self, **kwargs: Any) -> Any:
        code = kwargs.get("code")
        if not isinstance(code, str):
            raise ValueError("code must be a string")

        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = Path(tmpdir) / "app.py"
            script_path.write_text(code, encoding="utf-8")
            completed = subprocess.run(
                ["python", str(script_path)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=tmpdir,
            )
            payload = {
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
            if completed.returncode != 0:
                raise RuntimeError(json.dumps(payload))
            return payload
