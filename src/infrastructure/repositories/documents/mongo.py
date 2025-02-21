from abc import ABC
from dataclasses import dataclass
from motor.core import AgnosticClient
from src.domain.document.entity import Document
from src.infrastructure.repositories.documents.base import BaseDocumentsRepository
from src.infrastructure.repositories.documents.converter import document_to_mongo, document_from_mongo


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]
    
    
    

@dataclass
class MongoDBDocumentRepository(BaseDocumentsRepository, BaseMongoDBRepository):
    
    async def get_document_by_uuid(self, document_uuid: str) -> Document | None:
        document = await self._collection.find_one({'uuid': document_uuid})
        
        if document:
            return document_from_mongo(data=document)
        return None
    
    async def add_document(self, document: Document) -> None:
        await self._collection.insert_one(document=document_to_mongo(document=document))
    
    async def get_all_documents_by_user_uuid(self, user_uuid) -> list[Document] | None:
        documents_cursor = self._collection.find({'user_uuid': user_uuid}).sort('created_at', -1)
        documents = await documents_cursor.to_list(None)
        
        return [document_from_mongo(data=doc) for doc in documents]
        
    async def delete_document_by_uuid(self, document_uuid: str) -> bool:
        result = await self._collection.delete_one({'uuid': document_uuid})
        return result.deleted_count > 0
    
    async def delete_all_documents_by_user_uuid(self, user_uuid: str) -> bool:
        result = await self._collection.delete_many({'user_uuid': user_uuid})
        return result.deleted_count > 0
    
    async def update_document(self, document_uuid: str, document: Document) -> bool:

        updated_document_data = document_to_mongo(document=document)
        

        updated_document_data.pop('uuid', None)

        result = await self._collection.update_one(
            {'uuid': document_uuid},
            {'$set': updated_document_data}
        )

        return result.modified_count > 0