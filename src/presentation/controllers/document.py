import secrets
from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Form, HTTPException, Request, status, Query, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.application.use_cases.documents.upload_image import UploadImageUseCase
from src.application.use_cases.documents.download import DownloadDocument
from src.application.use_cases.documents.create import CreateDocumentUseCase
from src.application.use_cases.documents.delete import (
    DeleteAllDocumentsUseCase, DeleteDocumentUseCase)
from src.application.use_cases.documents.get_document import GetDocumentUseCase
from src.application.use_cases.documents.update import UpdateDocumentUseCase
from src.domain.document.entity import Document
from src.domain.user.entity import User
from src.domain.user.exception import UserNotAuthenticatedException
from src.presentation.schemas.document import CreateDocument, UpdateDocument
from typing import Annotated
from fastapi.responses import FileResponse
from src.presentation.schemas.document import Application


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

    document: Document | None = None

    if user:
        document: Document | None = await use_case.execute(document_uuid=document_uuid, user_uuid=user.uuid)
    print(document)
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
        

@router.get(
    '/{document_uuid}/download',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для скачивания документа',
    name='download:page',
)
@inject
async def download_document(
    document_uuid: str,
    format: Annotated[str, Query()],
    user: Depends[User],
    use_case: Depends[DownloadDocument],
) -> FileResponse:
    
    if not user:
        raise UserNotAuthenticatedException()

    res = await use_case.execute(document_uuid=document_uuid, user_uuid=user.uuid)
    
    if res:
        if format == 'pdf':
            return FileResponse(f'src/presentation/static/pdf/{document_uuid}.pdf')
        if format == 'docx':
            return FileResponse(f'src/presentation/static/docx/{document_uuid}.docx')
    else:
        return JSONResponse(content={'detail': 'Не удалось скачать файл'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

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
) -> JSONResponse:
    
    if not user:
        raise UserNotAuthenticatedException()

    await use_case.execute(document_uuid=document_uuid, user_uuid=user.uuid)
    return JSONResponse(content={'detail': 'Документ удален'}, status_code=status.HTTP_200_OK)


@router.delete(
    '/',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для удаления всех документов',
)
@inject
async def delete_all_documents(
    user: Depends[User],
    use_case: Depends[DeleteAllDocumentsUseCase],
) -> JSONResponse:
    
    if not user:
        raise UserNotAuthenticatedException()

    await use_case.execute(user_uuid=user.uuid)
    return JSONResponse(content={'detail': 'Все документы удалены'}, status_code=status.HTTP_200_OK)


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
) -> str:
    
    if not user:
        raise UserNotAuthenticatedException()

    return await use_case.execute(document=new_document, user_uuid=user.uuid)


@router.put(
    '/{document_uuid}',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для обновления документа',
)
@inject
async def update_document(
    document_uuid: str,
    document: UpdateDocument,
    user: Depends[User],
    use_case: Depends[UpdateDocumentUseCase],
) -> JSONResponse:
    
    if not user:
        raise UserNotAuthenticatedException()

    await use_case.execute(document_uuid=document_uuid, update_document=document, user_uuid=user.uuid)
    return JSONResponse(content={'detail': 'Документ обновлен'}, status_code=status.HTTP_200_OK)


@router.post(
    '/{document_uuid}',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для сохранения файла',
)
@inject
async def upload_image(
    document_uuid: str,
    image: Annotated[UploadFile, File()],
    user: Depends[User],
    use_case: Depends[UploadImageUseCase],
    description: str = Form(...),
) -> JSONResponse:
    
    if not user:
        raise UserNotAuthenticatedException()
    
    extension: str = image.filename.split('.')[-1]

    if extension not in ['png', 'jpg', 'jpeg', 'ico']:
        raise HTTPException(status_code=400, detail='Допустимые расширения: png, jpg, jpeg, ico')
    
    uniq_name: str = f'{secrets.token_urlsafe(10)}.{extension}'
    application: Application = Application(path=f'src/presentation/static/images/{uniq_name}', description=description, name=uniq_name)
    
    await use_case.execute(
        image=image,
        document_uuid=document_uuid,
        uniq_filename=uniq_name,
        application=application,
        user_id=user.uuid,
    )

    return JSONResponse(content={'success': True},  status_code=200)