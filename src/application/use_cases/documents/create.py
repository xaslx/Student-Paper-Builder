from dataclasses import dataclass

from src.domain.document.entity import Document
from src.domain.document.value_object import TitlePage
from src.infrastructure.repositories.documents.base import \
    BaseDocumentsRepository
from src.presentation.schemas.document import CreateDocument


@dataclass
class CreateDocumentUseCase:
    document_repository: BaseDocumentsRepository
    
    async def execute(self, document: CreateDocument, user_uuid: str) -> str:
        
        title_page: TitlePage = TitlePage(
            type_of_work=document.title_page.type_of_work,
            discipline=document.title_page.discipline,
            subject=document.title_page.subject,
            educational_institution=document.title_page.educational_institution,
            year=document.title_page.year,
            student_fullname=document.title_page.student_fullname,
            teacher_fullname=document.title_page.teacher_fullname,
            faculty=document.title_page.faculty,
            city=document.title_page.city,
            teaching_position=document.title_page.teaching_position,
        )
        new_document: Document = Document(
            user_uuid=user_uuid,
            name=document.name,
            title_page=title_page,
            abbreviations=document.abbreviations,
            introduction=document.introduction,
            main_sections=document.main_sections,
            conclusion=document.conclusion,
            references=document.references,
            appendices=document.appendices,
        )
        await self.document_repository.add_document(document=new_document)
        return new_document.uuid
    