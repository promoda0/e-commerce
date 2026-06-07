from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from product_service.app.core.constants import UserRole
from product_service.app.models.product import Product
from product_service.app.repositories.product_repository import ProductRepository
from product_service.app.schemas.auth_schema import AuthenticatedUser
from product_service.app.schemas.product_schema import ProductCreate, ProductListResponse, ProductResponse, ProductUpdate


class ProductService:
    @staticmethod
    def create_product(db: Session, payload: ProductCreate, actor: AuthenticatedUser) -> ProductResponse:
        seller_id = ProductService._resolve_seller_id(payload.seller_id, actor)
        ProductService._validate_duplicate_name(db, seller_id=seller_id, product_name=payload.name)

        created = ProductRepository.create_product(db, payload, seller_id)
        return ProductResponse.model_validate(created)

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        payload: ProductUpdate,
        actor: AuthenticatedUser,
    ) -> ProductResponse:
        product = ProductService._get_product_or_404(db, product_id)
        ProductService._authorize_product_write(actor, product)

        update_data = payload.model_dump(exclude_unset=True)

        incoming_name = update_data.get("name")
        if incoming_name and incoming_name.strip().lower() != product.name.strip().lower():
            seller_id = int(product.seller_id)
            ProductService._validate_duplicate_name(db, seller_id=seller_id, product_name=incoming_name)
            update_data["name"] = incoming_name.strip()

        updated = ProductRepository.update_product(db, product, update_data)
        return ProductResponse.model_validate(updated)

    @staticmethod
    def delete_product(db: Session, product_id: int, actor: AuthenticatedUser) -> None:
        product = ProductService._get_product_or_404(db, product_id)
        ProductService._authorize_product_write(actor, product)
        ProductRepository.delete_product(db, product)

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> ProductResponse:
        product = ProductService._get_product_or_404(db, product_id)
        if not product.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductResponse.model_validate(product)

    @staticmethod
    def get_all_products(db: Session, page: int, page_size: int) -> ProductListResponse:
        items, total = ProductRepository.get_all_products(db, page=page, page_size=page_size, is_active=True)
        return ProductListResponse(
            items=[ProductResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    def search_products(
        db: Session,
        *,
        name: str | None,
        category: str | None,
        brand: str | None,
        page: int,
        page_size: int,
    ) -> ProductListResponse:
        ProductService._validate_search_params(name, category, brand)
        items, total = ProductRepository.search_products(
            db,
            name=name,
            category=category,
            brand=brand,
            page=page,
            page_size=page_size,
        )
        return ProductListResponse(
            items=[ProductResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    def get_products_by_seller(db: Session, seller_id: int, page: int, page_size: int) -> ProductListResponse:
        items, total = ProductRepository.get_products_by_seller(db, seller_id=seller_id, page=page, page_size=page_size)
        return ProductListResponse(
            items=[ProductResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    def _validate_duplicate_name(db: Session, seller_id: int, product_name: str) -> None:
        existing = ProductRepository.get_by_name_for_seller(db, seller_id=seller_id, product_name=product_name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product name already exists for this seller",
            )

    @staticmethod
    def _resolve_seller_id(requested_seller_id: int | None, actor: AuthenticatedUser) -> int:
        if actor.role == UserRole.SELLER:
            if requested_seller_id is not None and requested_seller_id != actor.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Sellers can only create products for themselves",
                )
            return actor.user_id

        if actor.role == UserRole.ADMIN:
            if requested_seller_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="seller_id is required when admin creates a product",
                )
            return requested_seller_id

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers and admins can create products",
        )

    @staticmethod
    def _authorize_product_write(actor: AuthenticatedUser, product: Product) -> None:
        if actor.role == UserRole.ADMIN:
            return
        if actor.role == UserRole.SELLER and product.seller_id == actor.user_id:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this product",
        )

    @staticmethod
    def _get_product_or_404(db: Session, product_id: int) -> Product:
        product = ProductRepository.get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    @staticmethod
    def _validate_search_params(name: str | None, category: str | None, brand: str | None) -> None:
        if not any([name, category, brand]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provide at least one search filter: name, category, or brand",
            )
