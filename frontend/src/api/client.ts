import axios from "axios";
import axiosRetry from "axios-retry";

import { storage } from "@/utils/storage";

const baseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const apiClient = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosRetry(apiClient, {
  retries: 2,
  retryDelay: axiosRetry.exponentialDelay,
  retryCondition: (error) =>
    axiosRetry.isNetworkOrIdempotentRequestError(error) ||
    error.response?.status === 503,
});

apiClient.interceptors.request.use((config) => {
  const token = storage.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Future-ready place for refresh-token flow.
      storage.clearToken();
    }
    return Promise.reject(error);
  },
);

