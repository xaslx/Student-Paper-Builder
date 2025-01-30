from typing import AsyncIterator

from dishka import Provider, Scope, from_context, provide
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.repositories.base import BaseRepository
from src.infrastructure.database.postgres import new_session_maker
from src.settings.config import Config
from fastapi.templating import Jinja2Templates



class AppProvider(Provider):
    config: Config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session
            
    @provide(scope=Scope.APP)
    def get_jinja_template(self) -> Jinja2Templates:
        template: Jinja2Templates = Jinja2Templates(directory='src/presentation/static/templates')
        return template