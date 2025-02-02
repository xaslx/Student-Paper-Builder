from src.domain.common.exception import DomainErrorException
from fastapi import status


class DocumentNotFoundException(DomainErrorException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Документ не найден'
    
    
class DocumentAccessErrorException(DomainErrorException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'У вас нет разрешения на просмотр этого документа'