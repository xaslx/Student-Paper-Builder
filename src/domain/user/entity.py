from dataclasses import dataclass
from src.domain.common.entity import BaseEntity
from src.domain.user.value_object import Username


@dataclass
class User(BaseEntity):
    username: Username
    email: str
    
    @classmethod
    def create_user(cls, username: Username, email: str) -> 'User':
        return cls(
            username=username,
            email=email,
        )