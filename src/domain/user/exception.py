from src.domain.common.exception import DomainErrorException
from fastapi import status

# Пользователи
class UserAlreadyExistsException(DomainErrorException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Такой пользователь уже существует'


class IncorrectUsernameOrPasswordException(DomainErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный логин или пароль'


class InvalidUsernameOrPasswordException(DomainErrorException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = 'Логин или Пароль должны быть на английском, из разрешенных символов разрешено только "_"'


class UserNotFoundException(DomainErrorException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь не найден'


class NotAccessErrorException(DomainErrorException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Недостаточно прав'


class UserIsNotPresentException(DomainErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Ошибка'
    

class UsernameLengthException(DomainErrorException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = 'Логин должен быть состоять от 4 до 15 символов'
    

class PasswordLengthException(DomainErrorException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = 'Пароль должен быть состоять от 6 до 30 символов'
    

class UserNotAuthenticatedException(DomainErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Пользователь не аутентифицирован'