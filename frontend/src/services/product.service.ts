import { apiClient } from "@/api/client";
import { endpoints } from "@/api/endpoints";
import type { Product } from "@/types/product";

export const productService = {
  list: async () => {
    const response = await apiClient.get<Product[]>(endpoints.products.list);
    return response.data;
  },
  getById: async (id: number | string) => {
    const response = await apiClient.get<Product>(endpoints.products.detail(id));
    return response.data;
  },
};

