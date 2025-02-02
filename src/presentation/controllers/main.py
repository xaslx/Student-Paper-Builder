from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.domain.document.entity import Document
from src.domain.user.entity import User


router: APIRouter = APIRouter()


@router.get(
    '/', 
    status_code=status.HTTP_200_OK,
    name='main:page'
)
@inject
async def main_page(
    request: Request,
    template: Depends[Jinja2Templates],
    user: Depends[User],
    documents: Depends[list[Document]],
) -> HTMLResponse:

    return template.TemplateResponse(
        request=request, 
        context={'user': user, 'documents': documents},
        name='base.html',
    )


@router.get(
    '/about',
    status_code=status.HTTP_200_OK,
    name='about:page',
)
@inject
async def get_help_template(
    request: Request,
    template: Depends[Jinja2Templates],
    user: Depends[User],
    documents: Depends[list[Document]],
) -> HTMLResponse:
    
    return template.TemplateResponse(
        request=request,
        context={'user': user, 'documents': documents},
        name='about.html',
    )