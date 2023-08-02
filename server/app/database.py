from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

user = os.environ["MYSQL_USER"]
password = os.environ["MYSQL_PASSWORD"]
host = os.environ["MYSQL_HOST", "db"] 
database = os.environ["MYSQL_DATABASE"]
port = os.environ["MYSQL_PORT", 3306]

DATABASE_URL = f"mysql://{user}:{password}@{host}/{database}"

engine = create_engine(DATABASE_URL,echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

