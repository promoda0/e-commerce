from fastapi import FastAPI

from cart_service.app.api.cart_routes import router as cart_router
from cart_service.app.core.database import Base, engine
from cart_service.app.models import cart as cart_models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cart Service", version="1.0.0")
app.include_router(cart_router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"service": "cart", "status": "running"}

