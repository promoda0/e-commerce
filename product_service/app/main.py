from fastapi import FastAPI

from product_service.app.api.product_routes import router as product_router
from product_service.app.core.database import Base, engine
from product_service.app.models import product as product_models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service", version="1.0.0")
app.include_router(product_router)


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Product Service Running"}

