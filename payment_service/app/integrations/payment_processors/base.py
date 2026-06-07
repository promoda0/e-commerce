from abc import ABC, abstractmethod

from payment_service.app.integrations.payment_processors.types import PaymentProcessorRequest, PaymentProcessorResult


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, payload: PaymentProcessorRequest) -> PaymentProcessorResult:
        raise NotImplementedError

    @abstractmethod
    def process_refund(self, transaction_id: str, amount: float) -> PaymentProcessorResult:
        raise NotImplementedError

