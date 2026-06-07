from sqlalchemy.orm import Session

from inventory_service.app.models.product import Product


class ProductRepository:
    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Product | None:
        return db.query(Product).filter(Product.id == product_id).first()

