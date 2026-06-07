from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def migrate_user_table_for_signup() -> None:
    # Keep legacy SQLite databases compatible with the current user model.
    connection = engine.connect()
    transaction = connection.begin()
    try:
        columns_info = connection.exec_driver_sql("PRAGMA table_info(user)").fetchall()
        if not columns_info:
            transaction.commit()
            return

        existing_columns = {column[1] for column in columns_info}

        if "first_name" not in existing_columns:
            connection.exec_driver_sql('ALTER TABLE "user" ADD COLUMN first_name VARCHAR')
            if "name" in existing_columns:
                connection.exec_driver_sql('UPDATE "user" SET first_name = name WHERE first_name IS NULL')

        if "last_name" not in existing_columns:
            connection.exec_driver_sql('ALTER TABLE "user" ADD COLUMN last_name VARCHAR')
            connection.exec_driver_sql('UPDATE "user" SET last_name = "" WHERE last_name IS NULL')

        if "phone_number" not in existing_columns:
            connection.exec_driver_sql('ALTER TABLE "user" ADD COLUMN phone_number VARCHAR')
            connection.exec_driver_sql('UPDATE "user" SET phone_number = "" WHERE phone_number IS NULL')

        if "role" not in existing_columns:
            connection.exec_driver_sql('ALTER TABLE "user" ADD COLUMN role VARCHAR DEFAULT "customer"')

        connection.exec_driver_sql('UPDATE "user" SET role = "customer" WHERE role IS NULL OR role = ""')

        transaction.commit()
    except Exception:
        transaction.rollback()
        raise
    finally:
        connection.close()
