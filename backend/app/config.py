from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación desde variables de entorno."""

    # Database
    DATABASE_URL: str = "postgresql://postgres:0823@localhost:5432/energy_process"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # API
    ENVIRONMENT: str = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 50

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
