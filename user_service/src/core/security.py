import os
from datetime import timedelta

JWT_SECRET_KEY = os.getenv("USER_SERVICE_JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("USER_SERVICE_JWT_EXPIRE_MINUTES", "30"))
ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

