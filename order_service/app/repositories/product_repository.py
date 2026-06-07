from typing import cast

from sqlalchemy.orm import Session

from order_service.app.models.product import Product


class ProductRepository:
    @staticmethod
    def get_products_by_ids(db: Session, product_ids: list[int]) -> list[Product]:
        if not product_ids:
            return []
        results = db.query(Product).filter(Product.id.in_(product_ids)).all()
        return cast(list[Product], results)

    @staticmethod
    def update_stock(db: Session, product: Product, new_stock: int) -> Product:
        product.stock_quantity = new_stock
        db.flush()
        db.refresh(product)
        return product
