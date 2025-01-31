from pydantic import Field, BaseModel
from os import environ as env


class MongoDB(BaseModel):
    mongodb_connection_url: str = Field(alias='MONGO_DB_CONNECTION_URL')
    mongodb_database: str = Field(default='builder', alias='MONGODB_DATABASE')
    mongodb_documents_collection: str = Field(default='documents', alias='MONGODB_DOCUMENTS_COLLECTION')
    mongodb_users_collection: str = Field(default='users', alias='MONGODB_USERS_COLLECTION')
    
    
class JwtConfig(BaseModel):
    secret_key: str = Field(alias='JWT_SECRET_KEY')
    algorithm: str = Field(alias='ALGORITHM')


class Config(BaseModel):
    mongodb: MongoDB = Field(default_factory=lambda: MongoDB(**env))
    jwt: JwtConfig = Field(default_factory=lambda: JwtConfig(**env))
