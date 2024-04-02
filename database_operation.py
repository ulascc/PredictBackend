from sqlalchemy.orm import Session
from database import SessionLocal

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()
