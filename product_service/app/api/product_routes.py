from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from product_service.app.core.dependencies import get_current_seller_or_admin, get_current_user, get_db
from product_service.app.schemas.auth_schema import AuthenticatedUser
from product_service.app.schemas.product_schema import ProductCreate, ProductListResponse, ProductResponse, ProductUpdate
from product_service.app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_seller_or_admin),
) -> ProductResponse:
    return ProductService.create_product(db, payload, actor)


@router.get("", response_model=ProductListResponse)
def list_products(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_user),
) -> ProductListResponse:
    return ProductService.get_all_products(db, page=page, page_size=page_size)


@router.get("/search", response_model=ProductListResponse)
def search_products(
    name: str | None = Query(default=None),
    category: str | None = Query(default=None),
    brand: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_user),
) -> ProductListResponse:
    return ProductService.search_products(
        db,
        name=name,
        category=category,
        brand=brand,
        page=page,
        page_size=page_size,
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_user),
) -> ProductResponse:
    return ProductService.get_product_by_id(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_seller_or_admin),
) -> ProductResponse:
    return ProductService.update_product(db, product_id, payload, actor)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_seller_or_admin),
) -> None:
    ProductService.delete_product(db, product_id, actor)

