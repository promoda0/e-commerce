import { apiClient } from "@/api/client";
import { endpoints } from "@/api/endpoints";
import type { Order } from "@/types/order";

export const orderService = {
  list: async () => {
    const response = await apiClient.get<Order[]>(endpoints.orders.list);
    return response.data;
  },
};

