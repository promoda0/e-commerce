# Product Service

Role-aware product catalog service for an e-commerce backend.

## Features
- JWT-protected APIs
- Seller/Admin write permissions
- Customer read/search permissions
- Layered architecture: API -> Service -> Repository -> Database
- Pagination and filtered search support

## Quick Start
```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
python -m pip install -r product_service/app/requirements.txt
python -m uvicorn product_service.app.main:app --reload --port 8002
```

## Run Smoke Test
```powershell
python -m product_service.app.tests.smoke_test
```

## Main Endpoints
- `POST /products`
- `GET /products`
- `GET /products/search`
- `GET /products/{product_id}`
- `PUT /products/{product_id}`
- `DELETE /products/{product_id}`

