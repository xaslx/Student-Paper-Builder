from typing import TypeVar, Type, List
from src.infrastructure.models.base import Base
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


MT = TypeVar('MT', bound=Base) 


class BaseRepository(ABC):

    def __init__(self, session: AsyncSession, model: Type[MT]) -> None:
        self.session = session
        self.model = model

    @abstractmethod
    async def get_one_or_none(self, **filter_by: dict | None) -> MT | None:
        ...

    @abstractmethod
    async def get_all(self, **filter_by: dict | None) -> List[MT]:
        ...

    @abstractmethod
    async def add(self, obj: MT) -> int | None:
        ...

    @abstractmethod
    async def update(self, id: int, **data: dict | None) -> MT | None:
        ...

    @abstractmethod
    async def delete(self, id: int) -> MT | None:
        ...