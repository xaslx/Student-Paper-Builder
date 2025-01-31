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