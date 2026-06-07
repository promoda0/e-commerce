export const endpoints = {
  auth: {
    signup: "/signup",
    login: "/login",
  },
  products: {
    list: "/products",
    detail: (id: number | string) => `/products/${id}`,
  },
  cart: {
    get: (userId: number | string) => `/cart/${userId}`,
  },
  orders: {
    list: "/orders",
    detail: (id: number | string) => `/orders/${id}`,
  },
  inventory: {
    detail: (productId: number | string) => `/inventory/${productId}`,
    reserve: "/inventory/reserve",
    release: "/inventory/release",
  },
  payments: {
    list: "/payments",
  },
};

