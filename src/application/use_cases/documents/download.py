import asyncio
from dataclasses import dataclass
from src.application.services.document_creator import DocxCreator
from src.domain.document.exception import DocumentNotFoundException
from src.domain.user.exception import NotAccessErrorException
from src.domain.document.entity import Document
from src.infrastructure.repositories.documents.base import BaseDocumentsRepository
from src.infrastructure.repositories.documents.converter import document_to_mongo


@dataclass
class DownloadDocument:
    document_repository: BaseDocumentsRepository
    document_creator: DocxCreator
    
    async def execute(self, document_uuid: str, user_uuid: str) -> str:
        
        document: Document | None = await self.document_repository.get_document_by_uuid(document_uuid=document_uuid)
        
        if not document:
            raise DocumentNotFoundException()
        
        if document.user_uuid != user_uuid:
            raise NotAccessErrorException()
        
        uniq_name: str = f'{document.uuid}'
        document_to_dict = document_to_mongo(document=document)

        await asyncio.to_thread(
            self.document_creator.fill_template_with_breaks,
            context=document_to_dict,
            output_path=uniq_name
        )
        
        return uniq_name