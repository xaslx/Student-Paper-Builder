from fastapi import APIRouter, status, Request
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.application.use_cases.documents.get_document import GetDocumentUseCase
from src.application.use_cases.documents.delete import DeleteAllDocumentsUseCase, DeleteDocumentUseCase
from src.application.use_cases.documents.create import CreateDocumentUseCase
from src.domain.user.entity import User
from src.domain.document.entity import Document
from src.presentation.schemas.document import CreateDocument
from src.domain.user.exception import UserNotAuthenticatedException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router: APIRouter = APIRouter(prefix='/documents', tags=['Документы'])


@router.get(
    '/{document_uuid}',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для получения документа по uuid',
    name='documents:page',
)
@inject
async def get_document(
    request: Request,
    document_uuid: str,
    user: Depends[User],
    use_case: Depends[GetDocumentUseCase],
    template: Depends[Jinja2Templates],
    documents: Depends[list[Document]],
) -> HTMLResponse:
    
    if not user:
        raise UserNotAuthenticatedException()
    
    document: Document | None = await use_case.execute(document_uuid=document_uuid, user_uuid=user.uuid)
    if document:
        return template.TemplateResponse(
            request=request,
            context={'user': user, 'documents': documents, 'document': document},
            name='create_document.html',
        )
    return template.TemplateResponse(
        request=request,
        context={'user': user, 'documents': documents},
        name='404.html',
    )
        
    
@router.delete(
    '/{document_uuid}',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для удаления документа по uuid',
)
@inject
async def delete_document(
    document_uuid: str,
    user: Depends[User],
    use_case: Depends[DeleteDocumentUseCase],
    
) -> None:
    
    if not user:
        raise UserNotAuthenticatedException()
    
    await use_case.execute(document_uuid=document_uuid, user_uuid=user.uuid)


@router.delete(
    '/',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для удаления всех документов',
)
@inject
async def delete_all_documents(
    user: Depends[User],
    use_case: Depends[DeleteAllDocumentsUseCase],
) -> None:
    
    if not user:
        raise UserNotAuthenticatedException()
    
    await use_case.execute(user_uuid=user.uuid)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description='Эндпоинт для создания документа',
)
@inject
async def add_document(
    new_document: CreateDocument,
    user: Depends[User],
    use_case: Depends[CreateDocumentUseCase],
):
    if not user:
        raise UserNotAuthenticatedException()
    res : str = await use_case.execute(document=new_document, user_uuid=user.uuid)
    