from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB settings
    MONGODB_URL: str
    DB_NAME: str = "auth_db"
    
    # JWT settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Optional: Add other settings as needed
    ENVIRONMENT: str = "development"
    APP_NAME: str = "Auth Service"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
