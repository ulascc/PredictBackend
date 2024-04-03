from fastapi import Depends, FastAPI, HTTPException, Form
from sqlalchemy.orm import Session
from database_operation import get_db
from models import User, UserCreate, UserLogin, Text
from database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import jwt
import secrets

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

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
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Bu e-posta adresi zaten mevcut")

        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Beklenmeyen bir sorun ile karşılaşıldı")


@app.post("/login/")
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()

    if not user or user.password != user_login.password:
        raise HTTPException(status_code=401, detail="Geçersiz e-posta veya şifre")
    
    # Kullanıcının kimliği doğrulanmışsa access token oluştur ve return et
    access_token = create_access_token(data={"email": user.email})
    return {"access_token": access_token, "token_type": "bearer", "status": 200, "message": "Başarıyla giriş yapıldı"}



@app.post("/predict")
def predict_text(text: Text):
    predicted_result = f"Received text: {text.text}. This is just a placeholder response."
    return {"result": predicted_result}


# bu endpoint auth gerektirir
@app.get("/protected/")
def protected_route(token: str = Depends(decode_access_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "You are accessing a protected route."}
