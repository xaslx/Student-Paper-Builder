from typing import Any, Mapping
from src.domain.user.entity import User
from src.domain.user.value_object import Username


def convert_user_entity_to_document(user: User, hashed_password: str) -> dict:
    return {
        'uuid': user.uuid,
        'username': user.username.to_raw(),
        'email': user.email,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
        'hashed_password': hashed_password,
    }
    

def convert_document_to_user_entity(document: Mapping[str, Any]) -> User:
    return User(
        uuid=document['uuid'],
        username=Username(value=document['username']),
        email=document['email'],
        created_at=document['created_at'],
        updated_at=document['updated_at'],
    )
    


def convert_document_to_user_entity_with_hashed_password(document: Mapping[str, Any]) -> User:
    return User(
        uuid=document['uuid'],
        username=Username(value=document['username']),
        email=document['email'],
        created_at=document['created_at'],
        updated_at=document['updated_at'],
    ), document['hashed_password']