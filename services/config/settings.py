from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OMNIA"
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://omnia:omnia@localhost:5432/omnia"
    model_provider: str = "inmemory"
    model_name: str = "mock-model"
    api_keys: dict[str, str] = Field(default_factory=dict)
    log_level: str = "INFO"
    sandbox_enabled: bool = True
    sandbox_timeout_seconds: int = 30
    sandbox_cpu_limit: int = 1
    sandbox_memory_limit: str = "512m"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
