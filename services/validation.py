import re


DEFAULT_TITLE = "OMNIA"
DEFAULT_SUBTITLE = "Universal Research Intelligence"


def validate_prompt(prompt: str) -> bool:
    stripped = prompt.strip()
    return bool(stripped) and not re.search(r"\s+", stripped) is None
