import { apiClient } from "@/api/client";
import { endpoints } from "@/api/endpoints";
import type { LoginRequest, LoginResponse, SignupRequest, SignupResponse } from "@/types/auth";

export const authService = {
  signup: async (payload: SignupRequest) => {
    const response = await apiClient.post<SignupResponse>(endpoints.auth.signup, payload);
    return response.data;
  },
  login: async (payload: LoginRequest) => {
    const response = await apiClient.post<LoginResponse>(endpoints.auth.login, payload);
    return response.data;
  },
};

