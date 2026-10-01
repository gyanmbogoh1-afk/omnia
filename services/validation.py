import re


DEFAULT_TITLE = "OMNIA"
DEFAULT_SUBTITLE = "Universal Research Intelligence"


def validate_prompt(prompt: str) -> bool:
    return bool(prompt and len(prompt.strip()) > 0 and not re.search(r"\s+", prompt.strip()) is None)
