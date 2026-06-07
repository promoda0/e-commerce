import { apiClient } from "@/api/client";
import { endpoints } from "@/api/endpoints";
import type { Inventory } from "@/types/inventory";

export const inventoryService = {
  getByProduct: async (productId: number | string) => {
    const response = await apiClient.get<Inventory>(endpoints.inventory.detail(productId));
    return response.data;
  },
};

