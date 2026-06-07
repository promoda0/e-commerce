# Cart Service

Cart Service implements `API -> Service -> Repository -> Database` with FastAPI and SQLAlchemy.

## Why each layer exists
- `api/`: HTTP transport only, request parsing and response formatting.
- `services/`: business rules and validations (quantity checks, stock checks).
- `repositories/`: persistence only, isolated database access.
- `models/`: SQLAlchemy entities and table relationships.
- `schemas/`: request/response DTOs for input and output contracts.
- `core/`: DB engine/session configuration and DI helpers.

## Run
```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
python -m pip install -r cart_service/app/requirements.txt
python -m uvicorn cart_service.app.main:app --reload --port 8004
```

## Smoke test
```powershell
python -m cart_service.app.tests.smoke_test
```

## Endpoints
- `POST /cart/add`
- `DELETE /cart/remove`
- `PUT /cart/update`
- `GET /cart/{user_id}`

## Note on product validation
`ProductRepository` validates product stock by reading either:
- `product(id, stock)`
- `inventory(product_id, quantity)`

If neither source exists, add/update operations return product-not-found to keep cart rules strict.
