from sqlalchemy.orm import Session
from database import SessionLocal
from models import Classes

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


def get_class_by_id(db: Session, class_id: int):
    return db.query(Classes).filter(Classes.id == class_id).first()

