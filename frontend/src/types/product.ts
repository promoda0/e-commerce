export interface Product {
  id: number;
  name: string;
  description?: string;
  category?: string;
  brand?: string;
  price: number;
  stock_quantity: number;
  image_url?: string;
  seller_id: number;
  is_active: boolean;
}

