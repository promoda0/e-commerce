from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inventory_service.app.core.database import Base


class Inventory(Base):
    __tablename__ = "inventories"
    __table_args__ = (
        UniqueConstraint("product_id", name="uq_inventory_product_id"),
        CheckConstraint("total_stock >= 0", name="ck_inventory_total_stock_non_negative"),
        CheckConstraint("reserved_stock >= 0", name="ck_inventory_reserved_stock_non_negative"),
        CheckConstraint("available_stock >= 0", name="ck_inventory_available_stock_non_negative"),
        CheckConstraint("reserved_stock <= total_stock", name="ck_inventory_reserved_lte_total"),
        CheckConstraint("reorder_level >= 0", name="ck_inventory_reorder_level_non_negative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    total_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reserved_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    available_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reorder_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product: Mapped["Product"] = relationship("Product", back_populates="inventory")

