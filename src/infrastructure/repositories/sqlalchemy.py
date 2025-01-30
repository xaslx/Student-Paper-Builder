from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from src.logger import logger
from src.infrastructure.repositories.base import BaseRepository, MT


class SQLAlchemyRepository(BaseRepository):
    
    async def get_one_or_none(self, **filter_by: dict) -> MT | None:
        try:
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(msg='Не удалось найти объект', exc_info=e)
            raise e

    async def get_all(self, **filter_by: dict) -> list[MT]:
        try:
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)
            return result.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(msg='Не удалось найти список объектов', exc_info=e)
            raise e

    async def add(self, model: MT) -> MT:
        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return model
        except (SQLAlchemyError, Exception) as e:
            logger.error(msg='Не удалось добавить объект', exc_info=e)
            await self.session.rollback()
            raise e

    async def update(self, id: int, **data: dict) -> MT | None:
        try:
            query = select(self.model).filter_by(id=id)
            result = await self.session.execute(query)
            model = result.scalar_one_or_none()

            if model:
                for key, value in data.items():
                    setattr(model, key, value)
                await self.session.commit()
                await self.session.refresh(model)
                return model
            return None
        except (SQLAlchemyError, Exception) as e:
            logger.error(msg='Не удалось обновить объект', extra={'obj_id': id}, exc_info=e)
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> MT | None:
        try:
            query = select(self.model).filter_by(id=id)
            result = await self.session.execute(query)
            model = result.scalar_one_or_none()

            if model:
                await self.session.delete(model)
                await self.session.commit()
                return model
            return None
        except (SQLAlchemyError, Exception) as e:
            logger.error(msg='Не удалось удалить объект', extra={'obj_id': id}, exc_info=e)
            await self.session.rollback()
            raise e