import { useQuery } from "@tanstack/react-query";

import { inventoryService } from "@/services/inventory.service";

export const useInventory = (productId: string | number) =>
  useQuery({
    queryKey: ["inventory", productId],
    queryFn: () => inventoryService.getByProduct(productId),
    enabled: Boolean(productId),
    staleTime: 30_000,
  });

