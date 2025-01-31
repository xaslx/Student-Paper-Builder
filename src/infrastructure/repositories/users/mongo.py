from abc import ABC
from dataclasses import dataclass
from motor.core import AgnosticClient
from src.infrastructure.repositories.users.converter import convert_user_entity_to_document
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
        user_document = self._collection.find_one(filter={'uuid': uuid})
        
        if not user_document:
            return None

    async def add_user(self, user: User, hashed_password: str) -> None:
        await self._collection.insert_one(convert_user_entity_to_document(user=user, hashed_password=hashed_password))