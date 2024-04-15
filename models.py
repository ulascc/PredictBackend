from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import JSON

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
    prediction_logs = relationship("PredictionLogs", back_populates="user")



class UserType(Base):
    __tablename__ = "user_types"

    id = Column(Integer, primary_key=True, index=True)
    user_type_name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="user_type")
    
    

class PredictionLogs(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_at = Column(DateTime)  # İstek tarihi/saati
    response_ms = Column(Float)  # Yanıt süresi (milisaniye cinsinden) INTEGER
    path = Column(String)  # API URL yolu
    view = Column(String)  # Görüntü adı
    method = Column(String)  # HTTP yöntemi (GET, POST, vb.)
    payload = Column(String)  # İstek verisi (JSON formatında)
    response = Column(String)  # Yanıt verisi (JSON formatında)
    status_code = Column(Integer)  # HTTP durum kodu
    user_id = Column(Integer, ForeignKey('users.id'))  # Kullanıcı kimliği

    user = relationship("User", back_populates="prediction_logs")