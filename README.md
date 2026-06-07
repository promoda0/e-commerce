# E-Commerce Platform - Local Run Guide

This repository contains a multi-service FastAPI backend and a React frontend.

## Prerequisites
- Python 3.11+ (project currently uses 3.14 in local setup)
- Node.js and npm
- Windows PowerShell (commands below are PowerShell-friendly)

## 1) Backend setup (one time)
Run from project root:

```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r user_service/src/requirements.txt
python -m pip install -r product_service/app/requirements.txt
python -m pip install -r inventory_service/app/requirements.txt
python -m pip install -r cart_service/app/requirements.txt
python -m pip install -r order_service/app/requirements.txt
python -m pip install -r payment_service/app/requirements.txt
```

## 2) Start backend services (separate terminals)
Use one terminal per service:

```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
.\.venv\Scripts\Activate.ps1
python -m uvicorn user_service.src.main:app --reload --port 8001
```

```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
.\.venv\Scripts\Activate.ps1
python -m uvicorn product_service.app.main:app --reload --port 8002
```

```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
.\.venv\Scripts\Activate.ps1
python -m uvicorn inventory_service.app.main:app --reload --port 8003
```

```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
.\.venv\Scripts\Activate.ps1
python -m uvicorn cart_service.app.main:app --reload --port 8004
```

```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
.\.venv\Scripts\Activate.ps1
python -m uvicorn order_service.app.main:app --reload --port 8005
```

```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project"
.\.venv\Scripts\Activate.ps1
python -m uvicorn payment_service.app.main:app --reload --port 8006
```

## 3) Frontend setup and run

```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project\frontend"
Copy-Item ".env.example" ".env" -Force
npm install
npm run dev
```

Frontend default URL:
- `http://127.0.0.1:5173`

## 4) Smoke tests (optional)
Run from project root:

```powershell
python -m user_service.src.tests.auth_smoke_test
python -m product_service.app.tests.smoke_test
python -m inventory_service.app.tests.smoke_test
python -m cart_service.app.tests.smoke_test
python -m order_service.app.tests.smoke_test
python -m payment_service.app.tests.smoke_test
```

## Notes
- `api_gateway/main.py` is currently empty in this workspace, so services are started directly.
- If a port is already in use, change `--port` value and update frontend API base URL accordingly.

