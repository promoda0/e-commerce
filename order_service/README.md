# Order Service

Order orchestration service for e-commerce checkout.

## Features
- Creates orders from cart items
- Validates inventory and reduces stock
- Stores order and order items atomically
- Clears cart after successful order placement
- JWT-based customer/admin access control

## Quick Start
```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
python -m pip install -r order_service/app/requirements.txt
python -m uvicorn order_service.app.main:app --reload --port 8005
```

## Run Smoke Test
```powershell
python -m order_service.app.tests.smoke_test
```

