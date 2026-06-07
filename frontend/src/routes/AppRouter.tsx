import { Navigate, Route, Routes } from "react-router-dom";

import { DashboardLayout } from "@/layouts/DashboardLayout";
import { AuthLayout } from "@/layouts/AuthLayout";
import { ProtectedRoute } from "@/routes/ProtectedRoute";
import { LoginPage } from "@/pages/auth/LoginPage";
import { SignupPage } from "@/pages/auth/SignupPage";
import { UnauthorizedPage } from "@/pages/auth/UnauthorizedPage";
import { ForbiddenPage } from "@/pages/auth/ForbiddenPage";
import { NotFoundPage } from "@/pages/auth/NotFoundPage";
import { HomePage } from "@/pages/customer/HomePage";
import { ProductListPage } from "@/pages/customer/ProductListPage";
import { ProductDetailsPage } from "@/pages/customer/ProductDetailsPage";
import { CartPage } from "@/pages/customer/CartPage";
import { CheckoutPage } from "@/pages/customer/CheckoutPage";
import { OrdersPage } from "@/pages/customer/OrdersPage";
import { ProfilePage } from "@/pages/customer/ProfilePage";
import { SellerDashboardPage } from "@/pages/seller/SellerDashboardPage";
import { SellerProductsPage } from "@/pages/seller/SellerProductsPage";
import { SellerInventoryPage } from "@/pages/seller/SellerInventoryPage";
import { SellerOrdersPage } from "@/pages/seller/SellerOrdersPage";
import { AdminDashboardPage } from "@/pages/admin/AdminDashboardPage";
import { AdminUsersPage } from "@/pages/admin/AdminUsersPage";
import { AdminProductsPage } from "@/pages/admin/AdminProductsPage";
import { AdminInventoryPage } from "@/pages/admin/AdminInventoryPage";
import { AdminOrdersPage } from "@/pages/admin/AdminOrdersPage";
import { AdminPaymentsPage } from "@/pages/admin/AdminPaymentsPage";
import { AdminAnalyticsPage } from "@/pages/admin/AdminAnalyticsPage";

export const AppRouter = () => (
  <Routes>
    <Route element={<AuthLayout />}>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/unauthorized" element={<UnauthorizedPage />} />
      <Route path="/forbidden" element={<ForbiddenPage />} />
    </Route>

    <Route element={<ProtectedRoute />}>
      <Route element={<DashboardLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/products" element={<ProductListPage />} />
        <Route path="/products/:productId" element={<ProductDetailsPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Route>
    </Route>

    <Route element={<ProtectedRoute roles={["seller"]} />}>
      <Route element={<DashboardLayout />}>
        <Route path="/seller/dashboard" element={<SellerDashboardPage />} />
        <Route path="/seller/products" element={<SellerProductsPage />} />
        <Route path="/seller/inventory" element={<SellerInventoryPage />} />
        <Route path="/seller/orders" element={<SellerOrdersPage />} />
      </Route>
    </Route>

    <Route element={<ProtectedRoute roles={["admin", "support_admin"]} />}>
      <Route element={<DashboardLayout />}>
        <Route path="/admin/dashboard" element={<AdminDashboardPage />} />
        <Route path="/admin/users" element={<AdminUsersPage />} />
        <Route path="/admin/products" element={<AdminProductsPage />} />
        <Route path="/admin/inventory" element={<AdminInventoryPage />} />
        <Route path="/admin/orders" element={<AdminOrdersPage />} />
        <Route path="/admin/payments" element={<AdminPaymentsPage />} />
        <Route path="/admin/analytics" element={<AdminAnalyticsPage />} />
      </Route>
    </Route>

    <Route path="/not-found" element={<NotFoundPage />} />
    <Route path="*" element={<Navigate to="/not-found" replace />} />
  </Routes>
);

