export type Product = {
  id: string;
  name: string;
  brand: string;
  categoryId: string | null;
  categoryLabel: string;
  price: number;
  quantity: number;
  sku: string;
  description: string;
  createdAt: string;
  updatedAt: string;
};

export type ApiProduct = {
  id: string;
  name: string;
  price: number;
  brand: string;
  category: string | null;
  category_name: string | null;
  quantity: number;
  created_at: string | null;
  updated_at: string | null;
};

export type ApiCategory = {
  id: string;
  title: string;
  created_at?: string | null;
  updated_at?: string | null;
};

