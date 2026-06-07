from fastapi import FastAPI

from inventory_service.app.api.inventory_routes import router as inventory_router
from inventory_service.app.core.database import Base, engine
from inventory_service.app.models import inventory as inventory_models  # noqa: F401
from inventory_service.app.models import product as product_models  # noqa: F401

Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    application = FastAPI(title="Inventory Service", version="1.0.0")
    application.include_router(inventory_router)

    @application.get("/")
    def home() -> dict[str, str]:
        return {"message": "Inventory Service Running"}

    return application


app = create_app()

