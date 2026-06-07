export type OrderStatus =
  | "CREATED"
  | "PENDING_PAYMENT"
  | "PAID"
  | "PROCESSING"
  | "SHIPPED"
  | "DELIVERED"
  | "CANCELLED"
  | "REFUNDED";

export interface OrderItem {
  id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  total_price: number;
}

export interface Order {
  id: number;
  user_id: number;
  total_amount: number;
  status: OrderStatus;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

