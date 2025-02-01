from dataclasses import dataclass

from src.infrastructure.broker_messages.rabbitmq.publisher import publish
from src.application.services.hash import BaseHashService
from src.domain.user.entity import User
from src.domain.user.exception import UserAlreadyExistsException
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.presentation.schemas.user import UserRegister


@dataclass
class RegisterUserUseCase:
    user_repository: BaseUsersRepository
    hash_service: BaseHashService
    
    async def execute(
        self,
        user: UserRegister,
    ) -> User:
        
        exists_user: bool = await self.user_repository.exists_user(email=user.email, username=user.username)

        if exists_user:
            raise UserAlreadyExistsException()
        
        hashed_password: str = self.hash_service.get_password_hash(password=user.password)

        user_entity: User = User.create_user(
            username=user.username,
            email=user.email,
        )

        await self.user_repository.add_user(user=user_entity, hashed_password=hashed_password)
        
        await publish(
            to=user.email,
            subject='Успешная регистрация',
            body=f'Вы успешно зарегистрировались.\nВаш логин: {user.username}',
        )

        return user_entity