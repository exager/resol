from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "applied-ai-system"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
