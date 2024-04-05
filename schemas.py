from pydantic import BaseModel

class UserCreate(BaseModel):
    fullname: str
    email: str
    password: str
    user_type: str = "standard"


class UserLogin(BaseModel):
    email: str
    password: str


class ClassCreate(BaseModel):
    className: str


class Text(BaseModel):
    text: str