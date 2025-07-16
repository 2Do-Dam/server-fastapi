import os
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
    # 필요한 필드만 추가

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }
    

settings = Settings()
print("DATABASE_URL:", settings.DATABASE_URL)
print("REDIS_URL:", settings.REDIS_URL)