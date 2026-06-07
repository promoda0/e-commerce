from fastapi import FastAPI

from user_service.src.api.admin_routes import router as admin_router
from user_service.src.api.customer_routes import router as customer_router
from user_service.src.api.seller_routes import router as seller_router
from user_service.src.api.user_routes import router as user_router
from user_service.src.core.database import Base, engine, migrate_user_table_for_signup
from user_service.src.models import user as user_models  # noqa: F401

Base.metadata.create_all(bind=engine)
migrate_user_table_for_signup()

app = FastAPI(title="User Service", version="1.0.0")

app.include_router(user_router)
app.include_router(customer_router)
app.include_router(seller_router)
app.include_router(admin_router)


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "User Service Running"}
