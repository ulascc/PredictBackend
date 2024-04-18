from helpers import create_class_in_db, create_user_in_db, create_user_type_in_db, fetch_prediction_logs_from_db, login_user_in_db, decode_jwt, prediction_log, process_prediction
from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserCreate, UserLogin, ClassCreate, UserTypeCreate
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, Request
from database_operation import get_db
from sqlalchemy.orm import Session
from database import engine, Base
from fastapi import Request


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


@app.post("/predict")
async def predict_text(request: Request, db: Session = Depends(get_db)):
    return await process_prediction(request, db)


@app.post("/register/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_in_db(user, db)


@app.post("/login/")
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    return login_user_in_db(user_login, db)


@app.get("/get_prediction_logs/")
def get_prediction_logs_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return fetch_prediction_logs_from_db(skip, limit, db)


@app.post("/create_class/")
def create_class_endpoint(class_data: ClassCreate, db: Session = Depends(get_db)):
    return create_class_in_db(class_data, db)


@app.post("/user_types/")
def create_user_type_endpoint(user_type: UserTypeCreate, db: Session = Depends(get_db)):
    return create_user_type_in_db(user_type, db)