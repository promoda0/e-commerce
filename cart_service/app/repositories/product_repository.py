from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class ProductRepository:
    """Read-only repository for product availability checks."""

    @staticmethod
    def get_stock_by_product_id(db: Session, product_id: int) -> int | None:
        queries = [
            text("SELECT stock FROM product WHERE id = :product_id"),
            text("SELECT quantity AS stock FROM inventory WHERE product_id = :product_id"),
        ]

        for query in queries:
            try:
                result = db.execute(query, {"product_id": product_id}).mappings().first()
            except SQLAlchemyError:
                continue

            if result is not None and "stock" in result:
                return int(result["stock"])

        return None

