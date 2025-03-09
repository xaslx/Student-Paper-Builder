from dataclasses import dataclass
import os
import aiofiles
from fastapi import HTTPException, UploadFile
from src.domain.user.exception import NotAccessErrorException
from src.domain.document.entity import Document
from src.domain.document.exception import DocumentNotFoundException
from src.infrastructure.repositories.documents.base import BaseDocumentsRepository
from src.presentation.schemas.document import Application


UPLOAD_DIR = 'src/presentation/static/images'
os.makedirs(UPLOAD_DIR, exist_ok=True)


@dataclass
class UploadImageUseCase:
    document_repository: BaseDocumentsRepository

    async def execute(
            self,
            image: UploadFile,
            document_uuid: str,
            uniq_filename: str,
            application: Application,
            user_id: str,
        ) -> bool:

        try:
            document: Document | None = await self.document_repository.get_document_by_uuid(document_uuid=document_uuid)
            
            if not document:
                raise DocumentNotFoundException()
            
            if not user_id == document.user_uuid:
                raise NotAccessErrorException()

            file_path = os.path.join(UPLOAD_DIR, uniq_filename)

            async with aiofiles.open(file_path, 'wb') as buffer:
                while chunk := await image.read(1024 * 1024):
                    await buffer.write(chunk)

            document.appendices.append(application)
            await self.document_repository.update_document(document=document, document_uuid=document_uuid)
            return True

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))