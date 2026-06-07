from user_service.src.api.admin_routes import router as admin_router
from user_service.src.api.customer_routes import router as customer_router
from user_service.src.api.seller_routes import router as seller_router
from user_service.src.api.user_routes import router as user_router

__all__ = ["user_router", "customer_router", "seller_router", "admin_router"]

