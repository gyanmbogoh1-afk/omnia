from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConversationMessage:
    role: str
    content: str


@dataclass
class Conversation:
    id: str
    title: str
    messages: list[ConversationMessage] = field(default_factory=list)


class ConversationStore:
    def __init__(self) -> None:
        self._items: dict[str, Conversation] = {}

    def create(self, title: str) -> Conversation:
        conversation = Conversation(id=f"conv-{len(self._items) + 1}", title=title)
        self._items[conversation.id] = conversation
        return conversation

    def get(self, conversation_id: str) -> Conversation | None:
        return self._items.get(conversation_id)

    def list(self) -> list[Conversation]:
        return list(self._items.values())

    def add_message(self, conversation_id: str, role: str, content: str) -> ConversationMessage:
        conversation = self._items[conversation_id]
        message = ConversationMessage(role=role, content=content)
        conversation.messages.append(message)
        return message
