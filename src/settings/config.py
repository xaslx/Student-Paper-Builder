from pydantic import Field, BaseModel
from os import environ as env


class PostgresConfig(BaseModel):
    host: str = Field(alias='POSTGRES_HOST')
    port: int = Field(alias='POSTGRES_PORT')
    user: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    database: str = Field(alias='POSTGRES_DB')


class MongoDB(BaseModel):
    mongodb_connection_url: str = Field(alias='MONGO_DB_CONNECTION_URL')
    mongodb_database: str = Field(default='builder', alias='MONGODB_DATABASE')
    mongodb_documents_collection: str = Field(default='documents', alias='MONGODB_DOCUMENTS_COLLECTION')
    mongodb_users_collection: str = Field(default='users', alias='MONGODB_USERS_COLLECTION')


class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    mongodb: MongoDB = Field(default_factory=lambda: MongoDB(**env))
