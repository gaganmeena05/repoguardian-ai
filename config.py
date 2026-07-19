from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env automatically
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================================================
    # GitHub
    # ==========================================================

    github_token: str = Field(..., alias="GITHUB_TOKEN")

    github_owner: str = Field(
        default="",
        alias="GITHUB_OWNER",
    )

    github_repo: str = Field(
        default="",
        alias="GITHUB_REPO",
    )

    # ==========================================================
    # LangChain / Ollama
    # ==========================================================

    ollama_base_url: str = Field(
        default="http://localhost:11434",
        alias="OLLAMA_BASE_URL",
    )

    ollama_model: str = Field(
        default="qwen2.5-coder:7b",
        alias="OLLAMA_MODEL",
    )

    temperature: float = Field(
        default=0.2,
        alias="TEMPERATURE",
    )

    # ==========================================================
    # Embeddings
    # ==========================================================

    embedding_model: str = Field(
        default="BAAI/bge-small-en-v1.5",
        alias="EMBEDDING_MODEL",
    )

    vector_store_path: str = Field(
        default=".vector_store",
        alias="VECTOR_STORE_PATH",
    )

    # ==========================================================
    # Repository
    # ==========================================================

    repository_path: str = Field(
        default=".",
        alias="REPOSITORY_PATH",
    )

    # ==========================================================
    # Logging
    # ==========================================================

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Singleton settings object.
    """
    return Settings()


settings = get_settings()