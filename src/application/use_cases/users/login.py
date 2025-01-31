from dataclasses import dataclass

from src.application.services.auth import BaseAuthService
from src.application.services.jwt import JWTService
from src.application.services.hash import BaseHashService
from src.domain.user.entity import User
from src.domain.user.exception import UserNotFoundException
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.presentation.schemas.user import UserRegister
from datetime import datetime

# user: UserOut = await authenticate_user(user.email, user.password, async_db=session)
#     if not user:
#         raise UserNotFound

#     access_token, expire = create_access_token({"sub": user.personal_link})
#     max_age = (expire - datetime.utcnow()).total_seconds()

#     response.set_cookie(
#         "user_access_token", access_token, httponly=True, max_age=max_age, secure=True
#     )
#     logger.info(
#         f"Пользователь вошел в систему: ID={user.id}, name={user.name}, surname={user.surname}"
#     )
#     return access_token


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