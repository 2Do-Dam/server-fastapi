import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    SUPABASE_DB_URL: str
    OPENAI_API_KEY: str
    HOST: str
    PORT: str
    DEBUG: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int  # ← str → int로 변경!
    REDIS_URL: str
    EMAIL_SENDER: str
    EMAIL_APP_PASSWORD: str
    CORS_ALLOWED_ORIGINS: List[str]
    # 필요한 필드만 추가

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }
    

settings = Settings()
print("DATABASE_URL:", settings.DATABASE_URL)
print("REDIS_URL:", settings.REDIS_URL)
print("EMAIL_SENDER:", settings.EMAIL_SENDER)
print("EMAIL_APP_PASSWORD:", "설정됨" if settings.EMAIL_APP_PASSWORD else "설정되지 않음")
print("SUPABASE_URL:", settings.SUPABASE_URL)
print("OPENAI_API_KEY:", "설정됨" if settings.OPENAI_API_KEY else "설정되지 않음")