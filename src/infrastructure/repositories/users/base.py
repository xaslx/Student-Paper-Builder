from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from src.domain.user.entity import User



@dataclass
class BaseUsersRepository(ABC):

    @abstractmethod
    async def get_user_by_uuid(self, uuid: str) -> User | None:
        ...

    @abstractmethod
    async def add_user(self, user: User, hashed_password: str) -> None:
        ...
        
    @abstractmethod
    async def exists_user(self, email: str) -> bool:
        ...
        
    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        ...
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        ...
        
    @abstractmethod
    async def update_user_password(self, uuid: str, hashed_password: str) -> bool:
        ...