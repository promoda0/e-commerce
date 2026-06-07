import uuid

from payment_service.app.integrations.payment_processors.base import PaymentProcessor
from payment_service.app.integrations.payment_processors.types import PaymentProcessorRequest, PaymentProcessorResult


class MockProcessor(PaymentProcessor):
    def process_payment(self, payload: PaymentProcessorRequest) -> PaymentProcessorResult:
        if payload.simulate_failure:
            return PaymentProcessorResult(
                success=False,
                transaction_id=f"txn_fail_{uuid.uuid4().hex[:12]}",
                message="Payment failed in mock processor",
            )

        return PaymentProcessorResult(
            success=True,
            transaction_id=f"txn_{uuid.uuid4().hex[:12]}",
            message="Payment processed successfully",
        )

    def process_refund(self, transaction_id: str, amount: float) -> PaymentProcessorResult:
        return PaymentProcessorResult(
            success=True,
            transaction_id=f"rfnd_{uuid.uuid4().hex[:12]}",
            message="Refund processed successfully",
        )

