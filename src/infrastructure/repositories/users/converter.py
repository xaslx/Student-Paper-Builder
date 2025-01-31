from typing import Any, Mapping
from src.domain.user.entity import User


def convert_user_entity_to_document(user: User, hashed_password: str) -> dict:
    return {
        'uuid': user.uuid,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at,
        'hashed_password': hashed_password,
    }
    

def convert_document_to_user_entity(document: Mapping[str, Any]) -> User:
    return User(
        uuid=document['uuid'],
        username=document['username'],
        email=document['email'],
        created_at=document['created_at'],
    )
    


def convert_document_to_user_entity_with_hashed_password(document: Mapping[str, Any]) -> User:
    return User(
        uuid=document['uuid'],
        username=document['username'],
        email=document['email'],
        created_at=document['created_at'],
    ), document['hashed_password']