from pydantic import Field, BaseModel
from os import environ as env



class PostgresConfig(BaseModel):
    host: str = Field(alias='POSTGRES_HOST')
    port: int = Field(alias='POSTGRES_PORT')
    user: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    database: str = Field(alias='POSTGRES_DB')


class RedisConfig(BaseModel):
    redis_host: str = Field(alias='REDIS_HOST')
    redis_password: int = Field(alias='REDIS_PORT', default=6379)




class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    redis: RedisConfig = Field(default_factory=lambda: RedisConfig(**env))
