from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from src.domain.document.entity import Document


@dataclass
class BaseDocumentsRepository(ABC):

    @abstractmethod
    async def get_document_by_uuid(self, document_uuid: str) -> Document | None:
        ...
        
    @abstractmethod
    async def add_document(self, document: Document) -> None:
        ...
        
    @abstractmethod
    async def get_all_documents_by_user_uuid(self, user_uuid: str) -> list[Document] | None:
        ...
        
    @abstractmethod
    async def delete_document_by_uuid(self, document_uuid: str) -> bool:
        ...
        
    @abstractmethod
    async def delete_all_documents_by_user_uuid(self, user_uuid: str) -> bool:
        ...
        
    @abstractmethod
    async def update_document(self, document_uuid: str, document: Document) -> bool:
        ...