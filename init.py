from models import User, UserType, Classes
from database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

def load_user_types():
    db=SessionLocal()
    ut = [
        UserType(user_type_name="standart"),
        UserType(user_type_name="admin"),
        UserType(user_type_name="superuser")
    ]
    db.add_all(ut)
    db.commit()
    db.close()
    
    
def load_users():
    db=SessionLocal()
    ut = [
        User(fullname="ulas",email="ulas@gmail.com",password="$5$rounds=535000$84ZYwGuF0TSY1MrO$e.Ej3ImjXwUSgoP/SFY24HGoK.ZO1o3FUCdQZQOuNI6", user_type_id=1)
    ]
    db.add_all(ut)
    db.commit()
    db.close()
    
    
def load_classes():
    db=SessionLocal()
    ut = [
       Classes(className="kartlar"),
       Classes(className="ödemeler")
    ]
    db.add_all(ut)
    db.commit()
    db.close()
    
    
    
if __name__ == "__main__":
    load_user_types()
    load_users()
    load_classes()