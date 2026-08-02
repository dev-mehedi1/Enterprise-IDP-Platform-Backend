from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl, MongoDsn
from typing import Optional, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise IDP Platform"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = Field(default="SUPER_SECRET_CHANGE_ME_IN_PROD")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # MongoDB configuration
    MONGODB_URL: str = Field(default="mongodb://localhost:27017")
    MONGODB_DB_NAME: str = "idp_platform"
    
    # Redis configuration
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # RabbitMQ / Celery configuration
    CELERY_BROKER_URL: str = Field(default="amqp://guest:guest@localhost:5672//")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/1")
    
    # AI Providers
    AI_PROVIDER: str = Field(default="mock") # e.g., 'openai', 'gemini', 'ollama', 'mock'
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # OCR Providers
    OCR_PROVIDER: str = Field(default="tesseract") # e.g., 'tesseract', 'paddleocr'
    TESSERACT_CMD_PATH: Optional[str] = None
    
    # Storage
    STORAGE_TYPE: str = Field(default="local") # e.g., 'local', 's3'
    LOCAL_STORAGE_DIR: str = "./uploads"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
