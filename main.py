from helpers import create_class_in_db, create_user_type_in_db, fetch_prediction_logs_from_db, verify_password, create_access_token, decode_jwt, prediction_log
from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserCreate, UserLogin, ClassCreate, UserTypeCreate
from fastapi import Depends, FastAPI, HTTPException, Request
from database_operation import get_db, get_class_by_id
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base
from datetime import datetime
from fastapi import Request
from models import User
import random

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


@app.post("/register/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
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




@app.post("/login/")
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()

    if not user or not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="Geçersiz e-posta veya şifre")
    
    access_token = None
    if user.user_type_id == 1:  # Standart kullanıcı
        access_token = create_access_token(data={"email": user.email, "name": user.fullname, "user_type": "standard","user_id": user.id})
    elif user.user_type_id == 2:  # Admin kullanıcı
        access_token = create_access_token(data={"email": user.email, "name": user.fullname, "user_type": "admin", "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer", "status": 200, "message": "SHA256 - SUCCESSFUL"}



@app.post("/predict")
async def predict_text(request: Request, db: Session = Depends(get_db)):
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
        prediction_log(request_at, response_ms, text, "Error", 503, user_id, db)

        return {"error": error_message}



@app.get("/get_prediction_logs/")
def get_prediction_logs_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return fetch_prediction_logs_from_db(skip, limit, db)


@app.post("/create_class/")
def create_class_endpoint(class_data: ClassCreate, db: Session = Depends(get_db)):
    return create_class_in_db(class_data, db)


@app.post("/user_types/")
def create_user_type_endpoint(user_type: UserTypeCreate, db: Session = Depends(get_db)):
    return create_user_type_in_db(user_type, db)