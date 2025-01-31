from fastapi import APIRouter, Request, status, Response
from dishka.integrations.fastapi import inject, FromDishka as Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.domain.user.entity import User
from src.application.use_cases.users.register import RegisterUserUseCase
from src.application.use_cases.users.login import LoginUserUseCase
from src.presentation.schemas.user import UserRegister, UserOut, UserLogin


router: APIRouter = APIRouter(tags=['Аутентификация и Авторизация'])


@router.get(
    '/register',
    status_code=status.HTTP_200_OK,
    name='register:page',
    description='HTML шаблон с формой регистрации',
)
@inject
async def register_template(
    request: Request,
    template: Depends[Jinja2Templates],
) -> HTMLResponse:
    
    return template.TemplateResponse(
        request=request,
        context={},
        name='register.html',
    )
    
    
@router.get(
    '/login',
    status_code=status.HTTP_200_OK,
    name='login:page',
    description='HTML шаблон с формой входа',
)
@inject
async def login_template(
    request: Request,
    template: Depends[Jinja2Templates],
) -> HTMLResponse:
    
    return template.TemplateResponse(
        request=request,
        context={},
        name='login.html',
    )
    
    
@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    description='Эндпоинт для регистрации нового пользователя',
    
)
@inject
async def register_user(
    new_user: UserRegister,
    use_case: Depends[RegisterUserUseCase],
) -> UserOut:
    res: User = await use_case.execute(user=new_user)
    return UserOut(uuid=res.uuid, username=res.username)


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для входа в систему',
)
@inject
async def login_user(
    user: UserLogin, 
    response: Response,
    use_case: Depends[LoginUserUseCase],
) -> None:
    access_token, max_age = await use_case.execute(username=user.username, password=user.password)
    response.set_cookie(key='user_access_token', value=access_token, max_age=max_age, httponly=True)
    
    
@router.post(
    '/logout', 
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для удаления куки',
)
async def logout_user(
    response: Response,
) -> None:
    
    response.delete_cookie('user_access_token')
