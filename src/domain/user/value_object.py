from dataclasses import dataclass
from src.domain.user.exception import InvalidUsernameOrPasswordException, UsernameLengthException
from src.domain.common.value_object import BaseValueObject
import re



@dataclass(frozen=True)
class Username(BaseValueObject):
    
    def validate(self):
        if not (4 <= len(self.value) <= 10):
            raise UsernameLengthException()
        if not re.match(r'^[A-Za-z0-9_]+$', self.value):
            raise InvalidUsernameOrPasswordException()
        
    def to_raw(self) -> str:
        return str(self.value)