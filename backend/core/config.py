from __future__ import annotations

import json
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide configuration loaded from environment variables or a .env file.

    All fields have safe defaults for local development. Override via environment
    variables in production — never commit a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = (
        "postgresql+asyncpg://fasttrack:fasttrack@localhost:5432/fasttrack"
    )
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:5173"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, value: Any) -> list[str]:
        """Parse CORS origins from a Python list or a JSON-encoded string.

        Args:
            value: Raw value from the environment — either a list or a JSON string.

        Returns:
            Parsed list of allowed origin strings.
        """
        if isinstance(value, str):
            return json.loads(value)
        return value


settings = Settings()
