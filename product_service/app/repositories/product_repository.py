from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from product_service.app.models.product import Product
from product_service.app.schemas.product_schema import ProductCreate


class ProductRepository:
    @staticmethod
    def create_product(db: Session, payload: ProductCreate, seller_id: int) -> Product:
        product = Product(
            name=payload.name.strip(),
            description=payload.description,
            category=payload.category,
            brand=payload.brand,
            price=payload.price,
            stock_quantity=payload.stock_quantity,
            image_url=payload.image_url,
            seller_id=seller_id,
            is_active=True,
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update_product(db: Session, product: Product, update_data: dict) -> Product:
        for field, value in update_data.items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product | None:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_all_products(
        db: Session,
        *,
        page: int,
        page_size: int,
        is_active: bool = True,
    ) -> tuple[list[Product], int]:
        query = db.query(Product).filter(Product.is_active == is_active)
        total = query.count()
        items = (
            query.order_by(Product.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    @staticmethod
    def search_products(
        db: Session,
        *,
        name: str | None,
        category: str | None,
        brand: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Product], int]:
        filters = [Product.is_active.is_(True)]

        if name:
            filters.append(Product.name.ilike(f"%{name.strip()}%"))
        if category:
            filters.append(Product.category.ilike(f"%{category.strip()}%"))
        if brand:
            filters.append(Product.brand.ilike(f"%{brand.strip()}%"))

        query = db.query(Product).filter(and_(*filters))
        total = query.count()
        items = (
            query.order_by(Product.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    @staticmethod
    def get_products_by_seller(
        db: Session,
        seller_id: int,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[Product], int]:
        query = db.query(Product).filter(Product.seller_id == seller_id)
        total = query.count()
        items = (
            query.order_by(Product.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    @staticmethod
    def get_by_name_for_seller(db: Session, seller_id: int, product_name: str) -> Product | None:
        return (
            db.query(Product)
            .filter(
                and_(
                    Product.seller_id == seller_id,
                    func.lower(Product.name) == product_name.strip().lower(),
                )
            )
            .first()
        )
