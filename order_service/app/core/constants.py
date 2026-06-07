from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    SELLER = "seller"
    ADMIN = "admin"
    SUPPORT_ADMIN = "support_admin"


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

