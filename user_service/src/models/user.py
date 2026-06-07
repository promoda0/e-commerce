from sqlalchemy import Column, Integer, String
from user_service.src.core.database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True,index=True)
    # Legacy column kept for compatibility with existing databases.
    name = Column(String, nullable=False, default="")
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String,nullable=False, unique=True, index=True)
    phone_number = Column(String,nullable=False)
    role = Column(String, nullable=False, default="customer")
    password = Column(String,nullable=False)
