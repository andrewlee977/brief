from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    NEWS_API_KEY: str
    OPENAI_API_KEY: str
    TTS_API_KEY: str
    google_application_credentials: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 