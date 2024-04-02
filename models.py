from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    user_type = Column(String, default="standart")


class UserCreate(BaseModel):
    fullname: str
    email: str
    password: str
    user_type: str = "standard"

class UserLogin(BaseModel):
    email: str
    password: str