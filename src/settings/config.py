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


class RabbitMQ(BaseModel):
    rabbitmq_user: str = Field(alias='RABBITMQ_DEFAULT_USER')
    rabbitmq_password: str = Field(alias='RABBITMQ_DEFAULT_PASS')


class SMTP(BaseModel):
    smtp_host: str = Field(alias='SMTP_HOST')
    smtp_port: int = Field(alias='SMTP_PORT', default=465)
    smtp_user: str = Field(alias='SMTP_USER')
    smtp_pass: str = Field(alias='SMTP_PASS')
        

class Config(BaseModel):
    mongodb: MongoDB = Field(default_factory=lambda: MongoDB(**env))
    jwt: JwtConfig = Field(default_factory=lambda: JwtConfig(**env))
    rabbitmq: RabbitMQ = Field(default_factory=lambda: RabbitMQ(**env))
    smtp: SMTP = Field(default_factory=lambda: SMTP(**env))