from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.application.services.hash import BaseHashService
from src.application.services.jwt import JWTService
from src.domain.user.entity import User
from src.domain.user.exception import (IncorrectUsernameOrPasswordException,
                                       UserIsNotPresentException)


@dataclass
class BaseAuthService(ABC):
    
    user_repository: BaseUsersRepository
    hash_service: BaseHashService
    jwt_service: JWTService
    
    @abstractmethod
    async def authenticate_user(self, username: str, password: str):
        ...

    @abstractmethod
    async def get_current_user(self, token: str):
        ...
    

@dataclass
class AuthServiceImpl(BaseAuthService):

    async def authenticate_user(self, username: str, password: str) -> User | None:
        res = await self.user_repository.get_user_by_username(username=username)
        if res is None:
            raise IncorrectUsernameOrPasswordException()
        
        user, hashed_password = res
        if not self.hash_service.verify_password(password, hashed_password):
            raise IncorrectUsernameOrPasswordException()
        
        return user

    async def get_current_user(self, token: str) -> User | None:
        payload = self.jwt_service.valid_token(token=token)
    
        if not payload:
            return None
        
        user_uuid = payload.get('sub')
        user: User | None = await self.user_repository.get_user_by_uuid(uuid=user_uuid)

        if user is None:
            raise UserIsNotPresentException()

        return user