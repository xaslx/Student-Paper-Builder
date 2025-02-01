from dishka import AsyncContainer, make_async_container
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dishka.integrations import fastapi as fastapi_integration
from fastapi.staticfiles import StaticFiles
from src.presentation.controllers.setup_routers import setup_controllers
from src.infrastructure.ioc.ioc import AppProvider
from src.settings.config import Config


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield


def create_app() -> FastAPI:
    
    config: Config = Config()
    container: AsyncContainer = make_async_container(AppProvider(), context={Config: config})
    
    app: FastAPI = FastAPI(
        title='Student Paper Builder',
    )
    app.mount('/src/presentation/static', StaticFiles(directory='src/presentation/static'), 'static')
    setup_controllers(app=app)
    fastapi_integration.setup_dishka(container=container, app=app)
    
    return app