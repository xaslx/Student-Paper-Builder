from dataclasses import dataclass

from src.domain.user.exception import NotAccessErrorException
from src.domain.document.exception import DocumentNotFoundException
from src.presentation.schemas.document import UpdateDocument
from src.infrastructure.repositories.documents.base import BaseDocumentsRepository
from src.domain.document.entity import Document


@dataclass
class UpdateDocumentUseCase:
    document_repository: BaseDocumentsRepository
    
    async def execute(self, document_uuid: str, update_document: UpdateDocument, user_uuid: str) -> None:
        
        document: Document | None = await self.document_repository.get_document_by_uuid(document_uuid=document_uuid)
        
        if not document:
            raise DocumentNotFoundException()
        
        if user_uuid != document.user_uuid:
            raise NotAccessErrorException()

        document.update(new_data=update_document)
        await self.document_repository.update_document(document_uuid=document_uuid, document=document)
