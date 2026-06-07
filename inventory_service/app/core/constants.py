from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    SELLER = "seller"
    ADMIN = "admin"
    SUPPORT_ADMIN = "support_admin"


class StockReleaseMode(str, Enum):
    RELEASE = "RELEASE"
    DEDUCT = "DEDUCT"

