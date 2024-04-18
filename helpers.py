from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserCreate, UserLogin, UserTypeCreate, ClassCreate
from models import PredictionLogs, User, UserType, Classes
from database_operation import get_class_by_id, get_db
from fastapi import Depends, HTTPException, Request
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
from sqlalchemy.orm import Session
from sqlalchemy import Integer
import random
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
    
    
    
def create_user_in_db(user: UserCreate, db: Session):
    try:
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Bu e-posta adresi zaten mevcut")

        user.hash_password()  
        db_user = User(**user.dict(), user_type_id=1)  # Default user_type_id: 1

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user 
    
    except HTTPException as e:
        raise e
    except Exception as ex:
        print(ex)  
        raise HTTPException(status_code=500, detail="Beklenmeyen bir sorun ile karşılaşıldı")
  
  
    
def login_user_in_db(user_login: UserLogin, db: Session):
    try:
        user = db.query(User).filter(User.email == user_login.email).first()

        if not user or not verify_password(user_login.password, user.password):
            raise HTTPException(status_code=401, detail="Geçersiz e-posta veya şifre")
        
        access_token = None
        if user.user_type_id == 1:  # Standart kullanıcı
            access_token = create_access_token(data={"email": user.email, "name": user.fullname, "user_type": "standard", "user_id": user.id})
        elif user.user_type_id == 2:  # Admin kullanıcı
            access_token = create_access_token(data={"email": user.email, "name": user.fullname, "user_type": "admin", "user_id": user.id})
        
        return {"access_token": access_token, "token_type": "bearer", "status": 200, "message": "SHA256 - SUCCESSFUL"}
    
    except HTTPException as e:
        raise e
    except Exception as ex:
        print(ex)  
        raise HTTPException(status_code=500, detail="Beklenmeyen bir sorun ile karşılaşıldı")

    
    
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
    
 

async def process_prediction(request: Request, db: Session):
    try:
        request_at = datetime.now()
        
        data = await request.json()
        text = data.get('text', '') 
        token = data.get('token', '') 
        
        random_number = random.randint(1, 7)
        class_name = get_class_by_id(db, random_number)
        class_id = random_number
        
        user_id = decode_jwt(token)   
        response_data = {"text": text, "class": class_name}   
        response_time = datetime.now()
        response_ms = "{:.2f}".format((response_time - request_at).total_seconds() * 1000)
        
        prediction_log(request_at, response_ms, text, class_name, 200, user_id, class_id, db)
        
        return response_data
    
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        
        request_at = datetime.now()
        response_ms = 0 
        prediction_log(request_at, response_ms, text, "Error", 503, None, db)

        return {"error": error_message}

 
    
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