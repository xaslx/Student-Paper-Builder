from dishka import Provider, Scope, from_context, provide
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorClient
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.infrastructure.repositories.users.mongo import MongoDBUsersRepository
from src.settings.config import Config
from fastapi.templating import Jinja2Templates



class AppProvider(Provider):
    config: Config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)
            
    @provide(scope=Scope.APP)
    def get_jinja_template(self) -> Jinja2Templates:
        template: Jinja2Templates = Jinja2Templates(directory='src/presentation/static/html')
        return template
    
    @provide(scope=Scope.APP)
    def create_mongodb_client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            self.config.mongodb.mongodb_connection_url,
            serverSelectionTimeoutMS=3000,
        )
    
    @provide(scope=Scope.REQUEST)
    def init_chats_mongodb_repository(self, client: AsyncIOMotorClient) -> BaseUsersRepository:
        return MongoDBUsersRepository(
            mongo_db_client=client,
            mongo_db_db_name=self.config.mongodb.mongodb_database,
            mongo_db_collection_name=self.config.mongodb.mongodb_users_collection,
        )

