from abc import ABC
from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime


@dataclass(kw_only=True)
class BaseEntity(ABC):
    
    uuid: str = field(
        default_factory=lambda: str(uuid4()),
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    updated_at: datetime = field(
        default=None,
        kw_only=True,
    )
    
    def __hash__(self) -> int:
        return hash(self.uuid)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.uuid == __value.uuid