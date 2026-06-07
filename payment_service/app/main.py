from fastapi import FastAPI

from payment_service.app.api.payment_routes import router as payment_router
from payment_service.app.core.database import Base, engine
from payment_service.app.models import order as order_models  # noqa: F401
from payment_service.app.models import payment as payment_models  # noqa: F401

Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    application = FastAPI(title="Payment Service", version="1.0.0")
    application.include_router(payment_router)

    @application.get("/")
    def home() -> dict[str, str]:
        return {"message": "Payment Service Running"}

    return application


app = create_app()
