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
    
    class_info = db.query(Classes).filter(Classes.id == class_id).first()
    if class_info:
        return class_info.className
    else:
        return "Class not found"



def get_class_name_by_id(db: Session, class_id: int):
    class_info = get_class_by_id(db, class_id)
    if class_info:
        return class_info.className
    else:
        return "Class not found"