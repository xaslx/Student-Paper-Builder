from abc import ABC, abstractmethod
from passlib.context import CryptContext
from dataclasses import dataclass


pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


@dataclass
class BaseHashService(ABC):
    
    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass
    

@dataclass 
class BCryptHashService(BaseHashService):

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)