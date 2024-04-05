from pydantic import BaseModel
from typing import Optional
from passlib.hash import sha256_crypt 

class UserCreate(BaseModel):
    fullname: str
    email: str
    password: str
    user_type: Optional[str] = "standard"

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

class UserType(BaseModel):
    type: str