from fastapi import FastAPI

from app.config import settings
from app.routers import collection, item


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "app": settings.app_name}

    app.include_router(collection.router)
    app.include_router(item.router)

    return app


app = create_app()
