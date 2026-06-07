import { Navigate, Outlet, useLocation } from "react-router-dom";

import type { UserRole } from "@/types/auth";
import { useAuth } from "@/store/AuthContext";

interface ProtectedRouteProps {
  roles?: UserRole[];
}

export const ProtectedRoute = ({ roles }: ProtectedRouteProps) => {
  const { isAuthenticated, hasAnyRole } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  if (roles && !hasAnyRole(roles)) {
    return <Navigate to="/forbidden" replace />;
  }

  return <Outlet />;
};

