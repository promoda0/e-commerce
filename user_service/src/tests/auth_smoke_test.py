import uuid

from fastapi import HTTPException

from user_service.src.auth.dependencies import get_current_admin, get_current_seller, get_current_user
from user_service.src.core.database import SessionLocal, migrate_user_table_for_signup
from user_service.src.schemas.user_schema import UserLoginRequest, UserSignupRequest
from user_service.src.services.user_service import UserService


def _unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}@test.com"


def _unique_phone(prefix: str) -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"


def run_auth_smoke_test() -> None:
    migrate_user_table_for_signup()

    db = SessionLocal()
    try:
        seller_signup = UserService.register_user(
            db,
            UserSignupRequest(
                first_name="Test",
                last_name="Seller",
                email=_unique_email("seller"),
                phone_number=_unique_phone("91"),
                password="Password123",
                role="seller",
            ),
        )
        admin_signup = UserService.register_user(
            db,
            UserSignupRequest(
                first_name="Test",
                last_name="Admin",
                email=_unique_email("admin"),
                phone_number=_unique_phone("92"),
                password="Password123",
                role="admin",
            ),
        )

        seller_token = UserService.login_user(
            db,
            UserLoginRequest(email=seller_signup.email, password="Password123"),
        )
        admin_token = UserService.login_user(
            db,
            UserLoginRequest(email=admin_signup.email, password="Password123"),
        )

        seller_user = get_current_user(seller_token.access_token, db)
        admin_user = get_current_user(admin_token.access_token, db)

        assert seller_user.role == "seller"
        assert admin_user.role == "admin"

        get_current_seller(seller_user)
        get_current_admin(admin_user)

        try:
            get_current_admin(seller_user)
            raise AssertionError("Expected admin guard to block seller")
        except HTTPException as exc:
            assert exc.status_code == 403

        try:
            get_current_seller(admin_user)
            raise AssertionError("Expected seller guard to block admin")
        except HTTPException as exc:
            assert exc.status_code == 403

        print("User auth smoke test passed")
    finally:
        db.close()


if __name__ == "__main__":
    run_auth_smoke_test()

