from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database_operation import get_db
from models import User, UserCreate, UserLogin
from database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware

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
    
    return {"status": 200, "message": "Başarıyla giriş yapıldı"}
