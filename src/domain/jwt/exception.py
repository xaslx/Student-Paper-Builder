from src.domain.common.exception import DomainErrorException
from fastapi import status


# JWT token
class TokenExpiredException(DomainErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'JWT токен устарел'


class TokenAbsentException(DomainErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен отсутствует'


class IncorrectTokenException(DomainErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный формат токена'