export type UserRole = "customer" | "seller" | "admin" | "support_admin";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  password: string;
  role: UserRole;
}

export interface SignupResponse {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  role: UserRole;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in?: number;
}

export interface AuthUser {
  id: number;
  role: UserRole;
  token: string;
}

export interface JwtPayload {
  sub: string;
  role: UserRole;
  exp?: number;
}

