from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    """Application settings, read from the environment (and from a `.env` file if present)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DEBUG: bool = Field(default=False, description="Print [DEBUG] logs on stdout")
    DOCS_PATH: Path = Field(default=Path("documentations"), description="Documentation folder")
    HOST: str = Field(default="0.0.0.0", description="HTTP bind address")
    PORT: int = Field(default=8001, description="HTTP port")
    MCP_TRANSPORT: Literal["streamable-http", "sse", "stdio"] = Field(
        default="streamable-http", description="streamable-http, sse or stdio"
    )


settings = Setting()
