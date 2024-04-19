from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", default="postgresql://postgres:1234@localhost/PredictDB")

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@postgres/PredictDB"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@db/PredictDB"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
