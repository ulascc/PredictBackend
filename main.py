from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserCreate, UserLogin, ClassCreate, UserTypeCreate
from fastapi import Depends, FastAPI, HTTPException, Request
from database_operation import get_db, get_class_by_id
from fastapi.middleware.cors import CORSMiddleware
from models import User, Classes, UserType
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
from sqlalchemy.orm import Session
from database import engine, Base
import random
import jwt

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Şifre kontrol fonksiyonu
def verify_password(plain_password: str, hashed_password: str):
    return sha256_crypt.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
    


@app.post("/register/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        print(user.dict())  # İsteği kontrol etmek için
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
        print(ex)  # Hata mesajını kontrol etmek için
        raise HTTPException(status_code=500, detail="Beklenmeyen bir sorun ile karşılaşıldı")




@app.post("/login/")
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()

    if not user or not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="Geçersiz e-posta veya şifre")
    
    access_token = None
    if user.user_type_id == 1:  # Standart kullanıcı
        access_token = create_access_token(data={"email": user.email, "name": user.fullname, "user_type": "standard"})
    elif user.user_type_id == 2:  # Admin kullanıcı
        access_token = create_access_token(data={"email": user.email, "name": user.fullname, "user_type": "admin"})
    return {"access_token": access_token, "token_type": "bearer", "status": 200, "message": "SHA256 - SUCCESSFUL"}





def get_class_name_by_id(db: Session, class_id: int):
    class_info = get_class_by_id(db, class_id)
    if class_info:
        return class_info.className
    else:
        return "Class not found"



@app.post("/predict")
async def predict_text(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    text = data.get('text', '') 
    
    random_number = random.randint(1, 7)
    class_name = get_class_name_by_id(db, random_number)
  
    #predicted_result = f"Received text: {text}. Random number between 1 and 7: {random_number}. Class name: {class_name}"  
    return {"text": text, "class": class_name}




@app.post("/create_class/")
def create_class(class_data: ClassCreate, db: Session = Depends(get_db)):
    class_name = class_data.className
    
    new_class = Classes(className=class_name)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    
    return {"message": "Class created successfully", "class_name": class_name}




@app.post("/user_types/")
def create_user_type(user_type: UserTypeCreate, db: Session = Depends(get_db)):
    db_user_type = UserType(**user_type.dict())
    db.add(db_user_type)
    db.commit()
    db.refresh(db_user_type)
    return db_user_type



# bu endpoint auth gerektirir ÖRNEK
@app.get("/protected/")
def protected_route(token: str = Depends(decode_access_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "You are accessing a protected route."}
