from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    LOG_LEVEL: str = "info"
    
    # Model Configuration
    MODEL_NAME: str = "distilbert-base-uncased-finetuned-sst-2-english"
    TOKENIZER_NAME: str = "distilbert-base-uncased"
    DEVICE: str = "auto"  # auto, cuda, cpu
    MAX_SEQUENCE_LENGTH: int = 512
    
    # CORS Configuration
    CORS_ORIGINS: str = "*"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Application Settings
    APP_NAME: str = "DistilBERT Sentiment Analysis API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
