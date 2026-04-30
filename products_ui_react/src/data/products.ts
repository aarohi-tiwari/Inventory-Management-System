import type { Product } from "../types";

export const DUMMY_PRODUCTS: Product[] = [
  {
    id: "p-001",
    name: "Arabica Coffee Beans",
    brand: "RoastLab",
    categoryId: "c-grocery",
    categoryLabel: "Grocery",
    price: 399,
    quantity: 18,
    sku: "COF-ARAB-250G",
    description: "Medium roast, 250g. Notes of chocolate and citrus.",
    createdAt: "2026-03-12",
    updatedAt: "2026-04-03"
  },
  {
    id: "p-002",
    name: "Dish Soap",
    brand: "CleanWave",
    categoryId: "c-kitchen",
    categoryLabel: "Kitchen Essentials",
    price: 129,
    quantity: 42,
    sku: "KITCH-DSOAP-500",
    description: "500ml lemon fresh dishwashing liquid.",
    createdAt: "2026-02-19",
    updatedAt: "2026-04-15"
  },
  {
    id: "p-003",
    name: "Notebook A5",
    brand: "PaperTrail",
    categoryId: "c-stationery",
    categoryLabel: "Stationery",
    price: 79,
    quantity: 120,
    sku: "STAT-NB-A5-200",
    description: "200 pages, dotted, soft cover.",
    createdAt: "2026-01-08",
    updatedAt: "2026-02-02"
  },
  {
    id: "p-004",
    name: "LED Bulb 9W",
    brand: "BrightHome",
    categoryId: "c-home",
    categoryLabel: "Home",
    price: 149,
    quantity: 65,
    sku: "HOME-LED-9W-E27",
    description: "Warm white E27 bulb. Energy efficient.",
    createdAt: "2026-03-02",
    updatedAt: "2026-03-22"
  },
  {
    id: "p-005",
    name: "Shampoo 200ml",
    brand: "PureCare",
    categoryId: "c-personal",
    categoryLabel: "Personal Care",
    price: 219,
    quantity: 27,
    sku: "CARE-SHAM-200",
    description: "Gentle daily shampoo with aloe vera.",
    createdAt: "2026-04-01",
    updatedAt: "2026-04-20"
  }
];

