from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    SELLER = "seller"
    ADMIN = "admin"
    SUPPORT_ADMIN = "support_admin"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class PaymentMethod(str, Enum):
    CARD = "CARD"
    UPI = "UPI"
    NETBANKING = "NETBANKING"
    WALLET = "WALLET"
    COD = "COD"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    REFUNDED = "REFUNDED"

