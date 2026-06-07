import { useQuery } from "@tanstack/react-query";

import { orderService } from "@/services/order.service";

export const useOrders = () =>
  useQuery({
    queryKey: ["orders"],
    queryFn: orderService.list,
    staleTime: 30_000,
  });

