export interface Inventory {
  id: number;
  product_id: number;
  total_stock: number;
  reserved_stock: number;
  available_stock: number;
  reorder_level: number;
  is_low_stock: boolean;
  created_at: string;
  updated_at: string;
}

