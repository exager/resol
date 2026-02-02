from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "applied-ai-system"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

class RetrievalConfig(BaseSettings):
    min_top_score: float = 0.6
    min_chunks_above_threshold: int = 1

    class Config:
        env_prefix = "RAG_"

