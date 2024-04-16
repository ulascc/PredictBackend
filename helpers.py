from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models import PredictionLogs, UserType, Classes
from schemas import UserTypeCreate, ClassCreate
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
from database_operation import get_db
from sqlalchemy.orm import Session
from sqlalchemy import Integer
from fastapi import Depends
import jwt


# Şifre kontrol fonksiyonu
def verify_password(plain_password: str, hashed_password: str):
    return sha256_crypt.verify(plain_password, hashed_password)


#JWT Token oluşturma
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    

# JWT Token'ı decode eder ve user_id bilgisini return eder
def decode_jwt(token: str) -> int:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        
        user_id = payload.get("user_id")
        if user_id is None:
            raise ValueError("Invalid token: user_id not found in payload")
        return user_id
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    

    
def prediction_log(request_at: datetime, response_ms: float, text: str, class_name: str, status_code: Integer, user_id: str, class_id: Integer, db: Session):
    prediction_log = PredictionLogs(
        request_at=request_at,
        response_ms=response_ms,
        path="/predict",
        view="predict_text",
        method="POST",
        payload=text,
        response=class_name,
        status_code=status_code,
        user_id=user_id,
        class_id=class_id
    )
    db.add(prediction_log)
    db.commit()
    
    
def fetch_prediction_logs_from_db(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    prediction_logs = db.query(PredictionLogs).offset(skip).limit(limit).all()
    return prediction_logs
    
    
def create_user_type_in_db(user_type: UserTypeCreate, db: Session):
    db_user_type = UserType(**user_type.dict())
    db.add(db_user_type)
    db.commit()
    db.refresh(db_user_type)
    return db_user_type


def create_class_in_db(class_data: ClassCreate, db: Session):
    class_name = class_data.className
    new_class = Classes(className=class_name)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return {"message": "Class created successfully", "class_name": class_name}