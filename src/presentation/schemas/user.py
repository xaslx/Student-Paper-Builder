from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    

class UserOut(BaseModel):
    uuid: str
    username: str
    

class UserLogin(BaseModel):
    username: str
    password: str