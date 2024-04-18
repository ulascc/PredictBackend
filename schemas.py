from pydantic import BaseModel
from passlib.hash import sha256_crypt 

class UserCreate(BaseModel):
    fullname: str
    email: str
    password: str

    def hash_password(self):
        self.password = hash_password(self.password)

def hash_password(password: str):
    return sha256_crypt.hash(password)


class UserLogin(BaseModel):
    email: str
    password: str


class ClassCreate(BaseModel):
    className: str


class Text(BaseModel):
    text: str
    

class UserTypeCreate(BaseModel):
    user_type_name: str