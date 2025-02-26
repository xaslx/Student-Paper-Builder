from dataclasses import dataclass
from src.application.services.document_creator import DocxCreator
from src.domain.document.exception import DocumentNotFoundException
from src.domain.user.exception import NotAccessErrorException
from src.domain.document.entity import Document
from src.infrastructure.repositories.documents.base import BaseDocumentsRepository
from src.infrastructure.repositories.documents.converter import document_to_mongo
from fastapi import HTTPException


@dataclass
class DownloadDocument:
    document_repository: BaseDocumentsRepository
    document_creator: DocxCreator
    
    async def execute(self, document_uuid: str, user_uuid: str) -> bool:
        
        document: Document | None = await self.document_repository.get_document_by_uuid(document_uuid=document_uuid)
        
        if (not document.title_page) or \
            (not document.main_sections) or \
            (not document.introduction) or \
            (not document.conclusion) or \
            (not document.references):
                
            raise HTTPException(status_code=400, detail='Не все разделы заполнены')
        
        if not document:
            raise DocumentNotFoundException()
        
        if document.user_uuid != user_uuid:
            raise NotAccessErrorException()
        
        uniq_name: str = f'{document.uuid}'
        document_to_dict = document_to_mongo(document=document)
        
        self.document_creator.fill_template_with_breaks(context=document_to_dict, output_path=uniq_name)
        return True