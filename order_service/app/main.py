from fastapi import FastAPI

from order_service.app.api.order_routes import router as order_router
from order_service.app.core.database import Base, engine
from order_service.app.models import cart as cart_models  # noqa: F401
from order_service.app.models import order as order_models  # noqa: F401
from order_service.app.models import product as product_models  # noqa: F401

Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    application = FastAPI(title="Order Service", version="1.0.0")
    application.include_router(order_router)

    @application.get("/")
    def home() -> dict[str, str]:
        return {"message": "Order Service Running"}

    return application


app = create_app()

