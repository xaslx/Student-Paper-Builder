import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.domain.user.exception import InvalidUsernameOrPasswordException, PasswordLengthException


PASSWORD_CHECK = re.compile(r"^[\w!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]{6,30}$")


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        
        if not PASSWORD_CHECK.match(value):
            raise InvalidUsernameOrPasswordException()
        
        if not (6 <= len(value) <= 30):
            raise PasswordLengthException()
        
        return value
    
    
    

class UserOut(BaseModel):
    uuid: str
    username: str
    

class UserLogin(BaseModel):
    username: str
    password: str
    

class ResetPassword(BaseModel):
    email: EmailStr