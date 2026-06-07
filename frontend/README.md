# E-Commerce Frontend (React + TypeScript)

Production-style frontend for a multi-role e-commerce platform.

## Tech Stack
- React + TypeScript + Vite
- React Router
- Axios + axios-retry
- TanStack Query
- Material UI
- JWT auth + role-based route protection

## Folder Structure
```text
src/
  api/
  components/
    common/
    dashboard/
  hooks/
  layouts/
  pages/
    auth/
    customer/
    seller/
    admin/
  routes/
  services/
  store/
  types/
  utils/
  App.tsx
  main.tsx
```

## Environment
Create `.env` from `.env.example`:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8001
```

## Run
```powershell
Set-Location "C:\Users\SaPr598\PycharmProjects\PythonProject\ecommerce_project\frontend"
Copy-Item ".env.example" ".env" -Force
npm install
npm run dev
```

## Build
```powershell
npm run build
npm run preview
```

## Auth Flow
1. Login page calls `POST /login`.
2. Access token is stored in `localStorage`.
3. Axios request interceptor attaches bearer token.
4. Protected routes verify login + role.
5. Unauthorized users are redirected to `/login` or `/forbidden`.

## Role Routes
- Customer: `/`, `/products`, `/cart`, `/checkout`, `/orders`, `/profile`
- Seller: `/seller/dashboard`, `/seller/products`, `/seller/inventory`, `/seller/orders`
- Admin/Support Admin: `/admin/*`

## Scalability Hooks
The architecture is ready for adding:
- Notifications
- Wishlist
- Reviews
- Coupons
- Shipping

Add new features using `services/` + `hooks/` + role-specific `pages/` without changing shared auth or router internals.

