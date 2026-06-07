import { useQuery } from "@tanstack/react-query";

import { productService } from "@/services/product.service";

export const useProducts = () =>
  useQuery({
    queryKey: ["products"],
    queryFn: productService.list,
    staleTime: 60_000,
  });

export const useProduct = (id: string | number) =>
  useQuery({
    queryKey: ["products", id],
    queryFn: () => productService.getById(id),
    staleTime: 60_000,
  });

