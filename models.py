from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

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
    user_type_id = Column(Integer, ForeignKey('user_types.id'))

    user_type = relationship("UserType", back_populates="users")



class UserType(Base):
    __tablename__ = "user_types"

    id = Column(Integer, primary_key=True, index=True)
    user_type_name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="user_type")
    