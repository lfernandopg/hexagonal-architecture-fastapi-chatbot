from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from chatbot.infrastructure.config.settings import Settings
from chatbot.infrastructure.adapters.input.api.routes import chat_routes, health_routes
from chatbot.infrastructure.adapters.input.api.dependencies import (
    init_dependencies,
    close_dependencies
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación"""
    # Startup
    await init_dependencies()
    yield
    # Shutdown
    await close_dependencies()


def create_app() -> FastAPI:
    """Factory para crear la aplicación FastAPI"""
    settings = Settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Registrar rutas
    app.include_router(health_routes.router)
    app.include_router(chat_routes.router)
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = Settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )