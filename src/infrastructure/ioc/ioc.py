from dishka import Provider, Scope, from_context, provide
from fastapi import Request
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

from src.application.use_cases.documents.upload_image import UploadImageUseCase
from src.application.use_cases.documents.download import DownloadDocument
from src.application.use_cases.documents.update import UpdateDocumentUseCase
from src.application.use_cases.documents.get_document import GetDocumentUseCase
from src.application.use_cases.documents.delete import DeleteAllDocumentsUseCase, DeleteDocumentUseCase
from src.domain.document.entity import Document
from src.infrastructure.repositories.documents.mongo import MongoDBDocumentRepository
from src.infrastructure.repositories.documents.base import BaseDocumentsRepository
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
from src.application.use_cases.documents.create import CreateDocumentUseCase
from src.application.services.document_creator import DocxCreator


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
        
    @provide(scope=Scope.REQUEST)
    def init_documents_mongodb_repository(self, client: AsyncIOMotorClient, config: Config) -> BaseDocumentsRepository:
        
        return MongoDBDocumentRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb.mongodb_database,
            mongo_db_collection_name=config.mongodb.mongodb_documents_collection,
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
        
    @provide(scope=Scope.REQUEST)
    def get_docx_creator_service(self) -> DocxCreator:
        
        return DocxCreator(template_path='src/presentation/static/templates/main.docx')
        

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

    @provide(scope=Scope.REQUEST)
    def get_create_document_use_case(
        self,
        document_repository: BaseDocumentsRepository,
    ) -> CreateDocumentUseCase:
        
        return CreateDocumentUseCase(document_repository=document_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_delete_document_use_case(
        self,
        document_repository: BaseDocumentsRepository,
    ) -> DeleteDocumentUseCase:
        return DeleteDocumentUseCase(document_repository=document_repository)


    @provide(scope=Scope.REQUEST)
    def get_delete_all_documents_use_case(
        self,
        document_repository: BaseDocumentsRepository,
    ) -> DeleteAllDocumentsUseCase:
        return DeleteAllDocumentsUseCase(document_repository=document_repository)


    @provide(scope=Scope.REQUEST)
    def get_document_by_uuid_use_case(
        self,
        document_repository: BaseDocumentsRepository,
    ) -> GetDocumentUseCase:
        return GetDocumentUseCase(document_repository=document_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_update_document_use_case(
        self,
        document_repository: BaseDocumentsRepository,
    ) -> UpdateDocumentUseCase:
        return UpdateDocumentUseCase(document_repository=document_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_download_document_use_case(
        self,
        document_repository: BaseDocumentsRepository,
        document_creator: DocxCreator,
    ) -> DownloadDocument:
        return DownloadDocument(document_repository=document_repository, document_creator=document_creator)
        
        
    @provide(scope=Scope.REQUEST)
    def get_upload_image_use_case(
        self,
        document_repository: BaseDocumentsRepository,
    ) -> UploadImageUseCase:
        
        return UploadImageUseCase(document_repository=document_repository)
    

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
    
    
    @provide(scope=Scope.REQUEST)
    async def get_all_documents_for_user(
        self,
        document_repository: BaseDocumentsRepository,
        current_user: User,
    ) -> list[Document]:
        
        if current_user:
            return await document_repository.get_all_documents_by_user_uuid(current_user.uuid)