import { createContext, useContext, useEffect, useMemo, useState } from "react";

import type { AuthUser, LoginRequest, UserRole } from "@/types/auth";
import { authService } from "@/services/auth.service";
import { decodeJwt } from "@/utils/jwt";
import { storage } from "@/utils/storage";

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  login: (payload: LoginRequest) => Promise<void>;
  logout: () => void;
  hasAnyRole: (roles: UserRole[]) => boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    const token = storage.getToken();
    if (!token) {
      return;
    }
    const payload = decodeJwt(token);
    if (!payload?.sub || !payload.role) {
      storage.clearToken();
      return;
    }
    setUser({ id: Number(payload.sub), role: payload.role, token });
  }, []);

  const login = async (payload: LoginRequest) => {
    const response = await authService.login(payload);
    const decoded = decodeJwt(response.access_token);
    if (!decoded?.sub || !decoded.role) {
      throw new Error("Invalid token payload");
    }
    storage.setToken(response.access_token);
    setUser({ id: Number(decoded.sub), role: decoded.role, token: response.access_token });
  };

  const logout = () => {
    storage.clearToken();
    setUser(null);
  };

  const hasAnyRole = (roles: UserRole[]) => {
    if (!user) {
      return false;
    }
    return roles.includes(user.role);
  };

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      login,
      logout,
      hasAnyRole,
    }),
    [user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};

