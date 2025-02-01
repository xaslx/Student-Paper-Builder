import pytest

from src.domain.user.entity import User
from src.domain.user.exception import (InvalidUsernameOrPasswordException,
                                       UsernameLengthException)
from src.domain.user.value_object import Username


def test_create_user_success():
    
    username: Username = Username(value='Thomas')
    email: str = 'testexample@gmail.com'
    
    user: User = User.create_user(username=username, email=email)
    assert user
    assert user.username == username
    assert user.email == email
    

def test_create_user_username_to_short():
    
    with pytest.raises(UsernameLengthException):
        username: Username = Username(value='Sam')
        email: str = 'testexample@gmail.com'
        User.create_user(username=username, email=email)
            
        
def test_create_user_username_too_long():
    
    with pytest.raises(UsernameLengthException):
        username: Username = Username(value='Thomas'*10)
        email: str = 'testexample@gmail.com'
        User.create_user(username=username, email=email)
        

def test_create_user_username_invalid():
    
    with pytest.raises(InvalidUsernameOrPasswordException):
        username: Username = Username(value='Андрей')
        email: str = 'testexample@gmail.com'
        User.create_user(username=username, email=email)
        
        
def test_create_user_username_invalid_symbols():
    
    with pytest.raises(InvalidUsernameOrPasswordException):
        username: Username = Username(value='Sam!@#$%^&*()')
        email: str = 'testexample@gmail.com'
        User.create_user(username=username, email=email)