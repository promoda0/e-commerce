from dataclasses import dataclass


@dataclass
class PaymentProcessorRequest:
    order_id: int
    user_id: int
    amount: float
    currency: str
    payment_method: str
    simulate_failure: bool = False


@dataclass
class PaymentProcessorResult:
    success: bool
    transaction_id: str
    message: str

