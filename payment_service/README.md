# Payment Service

Role-aware payment processing service for the e-commerce backend.

## Features
- Payment initiation with order and ownership validation
- Simulated payment processing via strategy pattern
- Refund flow for successful payments
- JWT-based user authentication
- Transaction-safe payment + order-status updates

## Quick Start
```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
python -m pip install -r payment_service/app/requirements.txt
python -m uvicorn payment_service.app.main:app --reload --port 8006
```

## Run Smoke Test
```powershell
python -m payment_service.app.tests.smoke_test
```

