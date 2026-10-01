"""Database service layer for OMNIA using Supabase."""
from __future__ import annotations

from typing import Any

from services.database.supabase import SupabaseManager


class UserService:
    """Manage user records in Supabase."""

    def __init__(self, manager: SupabaseManager | None = None) -> None:
        self.manager = manager or SupabaseManager()

    async def get_user(self, user_id: str) -> dict[str, Any] | None:
        """Retrieve a user by ID."""
        if not self.manager.is_enabled():
            return None
        try:
            response = self.manager.client.table("users").select("*").eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to fetch user: {exc}") from exc

    async def create_user(self, email: str, name: str | None = None) -> dict[str, Any]:
        """Create a new user in Supabase."""
        if not self.manager.is_enabled():
            return {"id": "local-user", "email": email, "name": name}
        try:
            response = self.manager.client.table("users").insert({"email": email, "name": name}).execute()
            return response.data[0] if response.data else {}
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to create user: {exc}") from exc

    async def list_users(self, limit: int = 100) -> list[dict[str, Any]]:
        """List all users with pagination."""
        if not self.manager.is_enabled():
            return []
        try:
            response = self.manager.client.table("users").select("*").limit(limit).execute()
            return response.data or []
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to list users: {exc}") from exc


class ConversationService:
    """Manage conversation records in Supabase."""

    def __init__(self, manager: SupabaseManager | None = None) -> None:
        self.manager = manager or SupabaseManager()

    async def create_conversation(self, user_id: str, project_id: str | None = None, title: str | None = None) -> dict[str, Any]:
        """Create a new conversation."""
        if not self.manager.is_enabled():
            return {"id": f"conv-local-{user_id}", "user_id": user_id, "project_id": project_id, "title": title or "Untitled"}
        try:
            response = self.manager.client.table("conversations").insert({
                "user_id": user_id,
                "project_id": project_id,
                "title": title or "Untitled Conversation",
            }).execute()
            return response.data[0] if response.data else {}
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to create conversation: {exc}") from exc

    async def get_conversation(self, conversation_id: str) -> dict[str, Any] | None:
        """Retrieve a conversation by ID."""
        if not self.manager.is_enabled():
            return None
        try:
            response = self.manager.client.table("conversations").select("*").eq("id", conversation_id).execute()
            return response.data[0] if response.data else None
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to fetch conversation: {exc}") from exc

    async def list_conversations(self, user_id: str, limit: int = 50) -> list[dict[str, Any]]:
        """List conversations for a user."""
        if not self.manager.is_enabled():
            return []
        try:
            response = self.manager.client.table("conversations").select("*").eq("user_id", user_id).limit(limit).execute()
            return response.data or []
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to list conversations: {exc}") from exc


class MessageService:
    """Manage message records in Supabase."""

    def __init__(self, manager: SupabaseManager | None = None) -> None:
        self.manager = manager or SupabaseManager()

    async def add_message(self, conversation_id: str, role: str, content: str) -> dict[str, Any]:
        """Add a message to a conversation."""
        if not self.manager.is_enabled():
            return {"id": f"msg-{role}", "conversation_id": conversation_id, "role": role, "content": content}
        try:
            response = self.manager.client.table("messages").insert({
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
            }).execute()
            return response.data[0] if response.data else {}
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to add message: {exc}") from exc

    async def list_messages(self, conversation_id: str, limit: int = 100) -> list[dict[str, Any]]:
        """List messages in a conversation."""
        if not self.manager.is_enabled():
            return []
        try:
            response = (
                self.manager.client.table("messages")
                .select("*")
                .eq("conversation_id", conversation_id)
                .order("created_at")
                .limit(limit)
                .execute()
            )
            return response.data or []
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to list messages: {exc}") from exc


class MemoryService:
    """Manage memory records in Supabase."""

    def __init__(self, manager: SupabaseManager | None = None) -> None:
        self.manager = manager or SupabaseManager()

    async def save_memory(self, user_id: str | None, kind: str, content: str, source: str | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        """Save a memory record."""
        if not self.manager.is_enabled():
            return {
                "id": f"mem-{kind}",
                "user_id": user_id,
                "type": kind,
                "content": content,
                "source": source,
                "metadata": metadata or {},
            }
        try:
            response = self.manager.client.table("memories").insert({
                "user_id": user_id,
                "type": kind,
                "content": content,
                "source": source,
                "metadata": metadata or {},
            }).execute()
            return response.data[0] if response.data else {}
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to save memory: {exc}") from exc

    async def list_memories(self, user_id: str | None, limit: int = 50) -> list[dict[str, Any]]:
        """List memories for a user."""
        if not self.manager.is_enabled():
            return []
        try:
            query = self.manager.client.table("memories").select("*")
            if user_id:
                query = query.eq("user_id", user_id)
            response = query.order("created_at", desc=True).limit(limit).execute()
            return response.data or []
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to list memories: {exc}") from exc


class ActivityEventService:
    """Manage activity events in Supabase."""

    def __init__(self, manager: SupabaseManager | None = None) -> None:
        self.manager = manager or SupabaseManager()

    async def log_event(self, user_id: str | None, action: str, component: str, metadata: dict[str, Any] | None = None, success: bool = True) -> dict[str, Any]:
        """Log an activity event."""
        if not self.manager.is_enabled():
            return {
                "id": f"evt-{action}",
                "user_id": user_id,
                "action": action,
                "component": component,
                "success": success,
                "metadata": metadata or {},
            }
        try:
            response = self.manager.client.table("activity_events").insert({
                "user_id": user_id,
                "action": action,
                "component": component,
                "success": success,
                "metadata": metadata or {},
            }).execute()
            return response.data[0] if response.data else {}
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to log event: {exc}") from exc

    async def list_events(self, user_id: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        """List activity events."""
        if not self.manager.is_enabled():
            return []
        try:
            query = self.manager.client.table("activity_events").select("*")
            if user_id:
                query = query.eq("user_id", user_id)
            response = query.order("created_at", desc=True).limit(limit).execute()
            return response.data or []
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to list events: {exc}") from exc
