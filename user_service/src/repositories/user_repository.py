from sqlalchemy.orm import Session

from user_service.src.models.user import User


class UserRepository:

    @staticmethod
    def create_user(
        db: Session,
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        role: str,
        hashed_password: str,
    ) -> User:
        user = User(
            name=f"{first_name} {last_name}".strip(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            role=role,
            password=hashed_password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()
