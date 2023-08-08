from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

try:
    user = os.environ['MYSQL_USER']
    password = os.environ['MYSQL_PASSWORD']
    host = os.environ['MYSQL_HOST']
    database = os.environ['MYSQL_DATABASE']

    DATABASE_URL = f"mysql://{user}:{password}@{host}/{database}"
    
    try:
        engine = create_engine(DATABASE_URL, echo=True)
    except Exception as e:
        print(f"Error while creating engine: {e}")
        

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

except KeyError as ke:
    print(f"Environment variable {ke} not set")
    
except Exception as e:
    print(f"Unexpected error: {e}")
    