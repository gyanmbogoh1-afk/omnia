# Supabase configuration and client management
from __future__ import annotations

from typing import Any

try:
    from supabase import create_client
    from supabase.client import Client as SupabaseClient
except ImportError:
    SupabaseClient = Any  # type: ignore

from services.config.settings import settings


class SupabaseManager:
    """Manages Supabase client connection and operations."""

    _instance: SupabaseManager | None = None
    _client: SupabaseClient | None = None

    def __new__(cls) -> SupabaseManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._client is None and settings.supabase_enabled:
            if not settings.supabase_url or not settings.supabase_key:
                raise ValueError("Supabase URL and key are required when enabled")
            self._client = create_client(settings.supabase_url, settings.supabase_key)

    @property
    def client(self) -> SupabaseClient | None:
        """Returns the Supabase client instance."""
        return self._client

    def is_enabled(self) -> bool:
        """Check if Supabase is enabled and connected."""
        return self._client is not None and settings.supabase_enabled

    async def health_check(self) -> dict[str, Any]:
        """Perform a basic health check."""
        if not self.is_enabled():
            return {"status": "disabled", "message": "Supabase is not enabled"}
        try:
            response = self.client.table("users").select("*").limit(1).execute()
            return {"status": "healthy", "connected": True}
        except Exception as exc:  # pragma: no cover
            return {"status": "unhealthy", "error": str(exc)}


def get_supabase_manager() -> SupabaseManager:
    """Get the Supabase manager singleton."""
    return SupabaseManager()
