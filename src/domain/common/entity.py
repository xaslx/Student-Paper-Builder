from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class BaseEntity(ABC):
    
    id: int | None = field(
        default=None,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
    )
    updated_at: datetime = field(
        default_factory=datetime.now,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id