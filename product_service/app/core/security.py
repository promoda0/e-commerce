import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or os.getenv("USER_SERVICE_JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"

