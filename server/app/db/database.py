from ..config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

try:
    try:
        engine = create_engine(Config.DATABASE_URL,echo=True, pool_pre_ping=True)
    except Exception as e:
        print(f"Error while creating engine: {e}")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base() 
except Exception as e:
    print(f"Unexpected error: {e}")
    