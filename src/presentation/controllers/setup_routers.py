from fastapi import FastAPI
from src.presentation.controllers.main import router as main_router
from src.presentation.controllers.auth import router as auth_router
from src.presentation.controllers.document import router as document_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(main_router)
    app.include_router(auth_router)
    app.include_router(document_router)