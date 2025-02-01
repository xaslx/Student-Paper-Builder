from abc import ABC
from dataclasses import dataclass
from motor.core import AgnosticClient
from src.infrastructure.repositories.users.converter import convert_document_to_user_entity_with_hashed_password, convert_user_entity_to_document, convert_document_to_user_entity
from src.domain.user.entity import User
from src.infrastructure.repositories.users.base import BaseUsersRepository



@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]
    
    
    

@dataclass
class MongoDBUsersRepository(BaseUsersRepository, BaseMongoDBRepository):
    
    async def get_user_by_uuid(self, uuid: str) -> User | None:
        user_document = await self._collection.find_one(filter={'uuid': uuid})
        
        if not user_document:
            return None

        return convert_document_to_user_entity(document=user_document)

    async def add_user(self, user: User, hashed_password: str) -> None:
        await self._collection.insert_one(convert_user_entity_to_document(user=user, hashed_password=hashed_password))
        
    async def exists_user(self, email: str, username: str) -> bool:
        user_document = await self._collection.find_one(
            {'$or': [{'email': email}, {'username': username}]},
            {'_id': 1}
        )
        return bool(user_document)

    
    async def get_user_by_username(self, username: str) -> User | None:
        user_document = await self._collection.find_one(filter={'username': username})
        if not user_document:
            return None
        
        return convert_document_to_user_entity_with_hashed_password(document=user_document)
    
    
    async def get_user_by_email(self, email: str) -> User | None:
        user_document = await self._collection.find_one(filter={'email': email})
        if not user_document:
            return None
        
        return convert_document_to_user_entity(document=user_document)
    
    async def update_user_password(self, uuid: str, hashed_password: str) -> bool:

        result = await self._collection.update_one(
            filter={'uuid': uuid},
            update={'$set': {'hashed_password': hashed_password}}
        )
        
        return result.modified_count > 0