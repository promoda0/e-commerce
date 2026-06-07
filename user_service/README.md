# User Service

Role-aware authentication and authorization service using FastAPI, SQLAlchemy, and JWT.

## Layer Responsibilities
- `api/`: transport layer only (request mapping, dependency wiring, response models)
- `services/`: business rules (signup/login validation, password verification, token issuance)
- `repositories/`: pure database operations (`create_user`, `get_by_email`, `get_by_id`)
- `auth/`: JWT and role guard dependencies (`get_current_user`, `get_current_admin`, `get_current_seller`)
- `core/`: database/session setup and security constants
- `schemas/`: request/response contracts with no password exposure

## Endpoints
- `POST /signup`
- `POST /login`
- `GET /customer/me` (authenticated user)
- `GET /seller/me` (seller only)
- `GET /admin/me` (admin only)

## Run
```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
python -m pip install -r user_service/src/requirements.txt
python -m uvicorn user_service.src.main:app --reload --port 8001
```

## Smoke Test
```powershell
python -m user_service.src.tests.auth_smoke_test
```

