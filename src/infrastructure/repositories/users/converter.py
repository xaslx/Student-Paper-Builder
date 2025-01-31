from src.domain.user.entity import User


def convert_user_entity_to_document(user: User, hashed_password: str) -> dict:
    return {
        'uuid': user.uuid,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at,
        'hashed_password': hashed_password,
    }