from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from payment_service.app.core.database import Base
from payment_service.app.core.constants import PaymentStatus


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_payments_amount_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    transaction_id: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="INR")
    payment_method: Mapped[str] = mapped_column(String(32), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(32), nullable=False, default=PaymentStatus.PENDING.value)
    gateway_name: Mapped[str] = mapped_column(String(50), nullable=False, default="MOCK")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

