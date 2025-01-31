from dataclasses import dataclass
from datetime import datetime

from src.application.services.auth import BaseAuthService
from src.application.services.jwt import JWTService
from src.domain.user.entity import User
from src.domain.user.exception import UserNotFoundException
from src.infrastructure.repositories.users.base import BaseUsersRepository


@dataclass
class LoginUserUseCase:
    auth_service: BaseAuthService
    jwt_service: JWTService
    user_repository: BaseUsersRepository
    
    async def execute(self, username: str, password: str) -> tuple[str, int]:
        user: User | None = await self.auth_service.authenticate_user(username=username, password=password)
        
        if not user:
            raise UserNotFoundException()
        
        access_token: str
        access_token, expire = self.jwt_service.create_access_token({'sub': user.uuid})
        max_age: int = (expire - datetime.now()).total_seconds()
        
        return access_token, max_age