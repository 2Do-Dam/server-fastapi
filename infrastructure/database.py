from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from redis import StrictRedis
from core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

redis_client = StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    return redis_client
