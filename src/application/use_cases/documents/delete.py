from dataclasses import dataclass
from src.domain.user.exception import NotAccessErrorException
from src.domain.document.exception import DocumentNotFoundException
from src.domain.document.entity import Document
from src.infrastructure.repositories.documents.base import BaseDocumentsRepository



@dataclass
class DeleteDocumentUseCase:
    document_repository: BaseDocumentsRepository
    
    async def execute(self, document_uuid: str, user_uuid: str) -> bool:
        document: Document | None = await self.document_repository.get_document_by_uuid(document_uuid=document_uuid)
        
        if not document:
            raise DocumentNotFoundException()
        
        if document.user_uuid != user_uuid:
            raise NotAccessErrorException()

        return await self.document_repository.delete_document_by_uuid(document_uuid=document.uuid)
    
    
@dataclass
class DeleteAllDocumentsUseCase:
    document_repository: BaseDocumentsRepository
    
    async def execute(self, user_uuid: str) -> bool:
        
        res = await self.document_repository.delete_all_documents_by_user_uuid(user_uuid=user_uuid)
        if not res:
            raise DocumentNotFoundException()