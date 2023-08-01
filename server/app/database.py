from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import os

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
host = os.getenv("HOST", "db") 
database = os.getenv("MYSQL_DATABASE")
port = os.getenv("MYSQL_PORT", 3306)

DATABASE_URL = f"mysql://root:{password}@{host}/{database}"

#DATABASE_URL = "mysql://root:2002@db/mydb"

time.sleep(5)

engine = create_engine(DATABASE_URL,echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

