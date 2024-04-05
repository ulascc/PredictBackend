from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class Classes(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    className = Column(String, index=True)
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    user_type = Column(String, default="standart")
