from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base

class Classes(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    className = Column(String, index=True)
    prediction_logs = relationship("PredictionLogs", back_populates="class_")



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    user_type_id = Column(Integer, ForeignKey('user_types.id'))

    user_type = relationship("UserType", back_populates="users")
    prediction_logs = relationship("PredictionLogs", back_populates="user")



class UserType(Base):
    __tablename__ = "user_types"

    id = Column(Integer, primary_key=True, index=True)
    user_type_name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="user_type")



class PredictionLogs(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_at = Column(DateTime) 
    response_ms = Column(Float) 
    path = Column(String) 
    view = Column(String) 
    method = Column(String) 
    payload = Column(String) 
    response = Column(String) 
    status_code = Column(Integer)  
    user_id = Column(Integer, ForeignKey('users.id')) 
    class_id = Column(Integer, ForeignKey('classes.id')) 

    user = relationship("User", back_populates="prediction_logs")
    class_ = relationship("Classes", back_populates="prediction_logs")
