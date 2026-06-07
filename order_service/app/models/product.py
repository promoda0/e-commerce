from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from order_service.app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    seller_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

