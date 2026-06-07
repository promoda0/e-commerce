from fastapi import HTTPException, status

from payment_service.app.integrations.payment_processors.base import PaymentProcessor
from payment_service.app.integrations.payment_processors.mock_processor import MockProcessor


class PaymentProcessorFactory:
    _processors: dict[str, type[PaymentProcessor]] = {
        "MOCK": MockProcessor,
        "RAZORPAY": MockProcessor,
        "STRIPE": MockProcessor,
        "PAYPAL": MockProcessor,
        "PAYU": MockProcessor,
    }

    @classmethod
    def create(cls, gateway_name: str) -> PaymentProcessor:
        processor_class = cls._processors.get(gateway_name.upper())
        if not processor_class:
            supported = ", ".join(sorted(cls._processors))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported gateway '{gateway_name}'. Supported: {supported}",
            )
        return processor_class()

