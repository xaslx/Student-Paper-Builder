from dishka import Provider, Scope, from_context, provide
from fastapi import Request
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

from src.application.services.auth import AuthServiceImpl, BaseAuthService
from src.application.services.hash import BaseHashService, BCryptHashService
from src.application.services.jwt import JWTService, JWTServiceImpl
from src.application.use_cases.users.login import LoginUserUseCase
from src.application.use_cases.users.register import RegisterUserUseCase
from src.application.use_cases.users.reset_password import ResetPasswordCheckTokenUseCase, ResetPasswordUseCase
from src.domain.user.entity import User
from src.infrastructure.repositories.users.base import BaseUsersRepository
from src.infrastructure.repositories.users.mongo import MongoDBUsersRepository
from src.settings.config import Config


class AppProvider(Provider):
    config: Config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_jinja_template(self) -> Jinja2Templates:
        template: Jinja2Templates = Jinja2Templates(directory='src/presentation/static/html')
        return template
    
    @provide(scope=Scope.APP)
    def create_mongodb_client(self, config: Config) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            config.mongodb.mongodb_connection_url,
            serverSelectionTimeoutMS=3000,
        )
    
    @provide(scope=Scope.REQUEST)
    def init_users_mongodb_repository(self, client: AsyncIOMotorClient, config: Config) -> BaseUsersRepository:
        
        return MongoDBUsersRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb.mongodb_database,
            mongo_db_collection_name=config.mongodb.mongodb_users_collection,
        )

    #services
    @provide(scope=Scope.REQUEST)
    def get_hash_service(self) -> BaseHashService:
        return BCryptHashService()
    
    @provide(scope=Scope.REQUEST)
    def get_jwt_service(self, config: Config) -> JWTService:
        return JWTServiceImpl(config=config)
    
    @provide(scope=Scope.REQUEST)
    def get_auth_service(
        self,
        user_repository: BaseUsersRepository,
        hash_service: BaseHashService,
        jwt_service: JWTService,
    ) -> BaseAuthService:

        return AuthServiceImpl(
            user_repository=user_repository,
            hash_service=hash_service,
            jwt_service=jwt_service,
        )

    #UseCases
    @provide(scope=Scope.REQUEST)
    def get_register_user_use_case(
        self,
        user_repository: BaseUsersRepository,
        hash_service: BaseHashService,
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            user_repository=user_repository,
            hash_service=hash_service,
        )
        
    @provide(scope=Scope.REQUEST)
    def get_login_user_use_case(
        self,
        auth_service: BaseAuthService,
        jwt_service: JWTService,
        user_repository: BaseUsersRepository,
    ) -> LoginUserUseCase:
        
        return LoginUserUseCase(
            auth_service=auth_service,
            jwt_service=jwt_service,
            user_repository=user_repository,
        )
        
    @provide(scope=Scope.REQUEST)
    def get_reset_password_use_case(
        self,
        jwt_service: JWTService,
        user_repository: BaseUsersRepository,
    ) -> ResetPasswordUseCase:
        
        return ResetPasswordUseCase(
            user_repository=user_repository,
            jwt_service=jwt_service,
        )
    
    @provide(scope=Scope.REQUEST)
    def get_reset_password_check_token_use_case(
        self,
        jwt_service: JWTService,
        user_repository: BaseUsersRepository,
        hash_service: BaseHashService,
    ) -> ResetPasswordCheckTokenUseCase:
        
        return ResetPasswordCheckTokenUseCase(
            user_repository=user_repository,
            jwt_service=jwt_service,
            hash_service=hash_service,
        )    


    #dependencies
    @provide(scope=Scope.REQUEST)
    def get_token(self, request: Request) -> str:
        
        token: str = request.cookies.get('user_access_token')
    
        if not token:
            return None
        return token

    @provide(scope=Scope.REQUEST)
    async def get_current_user_dependency(
        self,
        auth_service: BaseAuthService,
        token: str,
    ) -> User:
        
        if not token:
            return None
        return await auth_service.get_current_user(token=token)
