from src.domain.common.exception import DomainErrorException
from fastapi import status

# Пользователи
class UserAlreadyExistsException(DomainErrorException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Такой пользователь уже существует'


class IncorrectUsernameOrPasswordException(DomainErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный логин или пароль'


class IncorrectEmailOrPasswordExceptionNotEn(DomainErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Email или пароль должны быть на английском'


class UserNotFoundException(DomainErrorException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь не найден'


class NotAccessErrorException(DomainErrorException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Недостаточно прав'


class UserIsNotPresentException(DomainErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED

