from dataclasses import dataclass
from src.domain.common.entity import BaseEntity


@dataclass
class User(BaseEntity):
    username: str
    email: str
    
    @classmethod
    def create_user(cls, username: str, email: str) -> 'User':
        return cls(
            username=username,
            email=email,
        )