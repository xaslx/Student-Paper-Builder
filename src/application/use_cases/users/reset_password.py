from dataclasses import dataclass


from src.domain.jwt.exception import TokenExpiredException
from src.application.services.hash import BaseHashService
from src.application.services.jwt import JWTService
from src.domain.user.entity import User
from src.domain.user.exception import UserIsNotPresentException, UserNotFoundException
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.infrastructure.broker_messages.rabbitmq.publisher import publish
import string
import random


CHARACTERS: str = string.ascii_letters + string.digits + string.punctuation


@dataclass
class ResetPasswordUseCase:
    user_repository: BaseUsersRepository
    jwt_service: JWTService
    
    async def execute(self, email: str) -> None:
        user: User | None = await self.user_repository.get_user_by_email(email=email)
        
        if not user:
            raise UserNotFoundException()
        
        token, _= self.jwt_service.create_access_token({'sub': user.uuid}, minutes=5)
        await publish(
            to=user.email,
            subject='Восстановление пароля',
            body=f'Перейдите по ссылке ниже чтобы сбросить пароль\n127.0.0.1:8000/reset_password/confirm/?token={token}'
        )
        
        
@dataclass
class ResetPasswordCheckTokenUseCase:
    user_repository: BaseUsersRepository
    jwt_service: JWTService
    hash_service: BaseHashService
    
    async def execute(self, token: str) -> bool:
        payload = self.jwt_service.valid_token(token=token)

        if payload:
            res = payload.get('sub')
        
            user: User | None = await self.user_repository.get_user_by_uuid(uuid=res)

            if user is None:
                raise UserIsNotPresentException()

            new_password: str = ''.join(random.choices(CHARACTERS, k=10))
            hashed_password: str = self.hash_service.get_password_hash(password=new_password)
            res: bool = await self.user_repository.update_user_password(uuid=user.uuid, hashed_password=hashed_password)
            if res:
                await publish(
                    to=user.email,
                    subject='Сброс пароля',
                    body=f'Вы сбросили пароль.\nВаш логин: {user.username.to_raw()}\nВаш новый пароль: {new_password}\nТеперь вы можете войти на сервис с новым паролем'
                )
            return True
        else:
            raise TokenExpiredException()
