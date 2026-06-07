# Inventory Service

Dedicated stock management service for e-commerce operations.

## Features
- Inventory initialization per product
- Stock increase/decrease controls
- Reservation and release/deduction flow
- Low-stock detection via reorder threshold
- JWT-protected write operations

## Quick Start
```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
python -m pip install -r inventory_service/app/requirements.txt
python -m uvicorn inventory_service.app.main:app --reload --port 8003
```

## Run Smoke Test
```powershell
python -m inventory_service.app.tests.smoke_test
```

