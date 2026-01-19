from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/stats_db"
    
    # Redis (for Celery)
    redis_url: str = "redis://localhost:6379/0"
    
    # API
    api_title: str = "Stats Aggregation API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api"
    
    # Scraping
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 5
    rate_limit_delay: float = 1.0
    
    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
