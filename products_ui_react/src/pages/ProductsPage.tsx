import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet } from "../api/http";
import type { ApiCategory, ApiProduct } from "../types";
import { ProductList } from "../components/ProductList";
import { Spinner } from "../components/Spinner";
import { ErrorBanner } from "../components/ErrorBanner";

type ProductsListResponse = {
  products: ApiProduct[];
  total: number;
  page: number;
  total_pages: number;
};

type CategoriesResponse = { categories: ApiCategory[] };

export function ProductsPage() {
  const [products, setProducts] = useState<ApiProduct[]>([]);
  const [categories, setCategories] = useState<ApiCategory[]>([]);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const productsForList = useMemo(
    () =>
      products.map((p) => ({
        id: p.id,
        name: p.name,
        brand: p.brand,
        categoryId: p.category,
        categoryLabel: p.category_name ?? "—",
        price: p.price,
        quantity: p.quantity,
        sku: p.id,
        description: "Loaded from API list endpoint",
        createdAt: p.created_at ?? "",
        updatedAt: p.updated_at ?? ""
      })),
    [products]
  );

  const refresh = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [plist, clist] = await Promise.all([
        apiGet<ProductsListResponse>("/api/products/list/?page=1&limit=50"),
        apiGet<CategoriesResponse>("/api/categories/")
      ]);
      setProducts(plist.products || []);
      setCategories(clist.categories || []);
    } catch (e: any) {
      setError(e?.payload?.error || e?.message || "Failed to load products");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  return (
    <div className="card">
      <div className="card-body">
        {error ? <ErrorBanner message={error} onDismiss={() => setError(null)} /> : null}

        <div className="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
          <div className="fw-semibold">Products</div>
          <div className="d-flex align-items-center gap-2">
            <button className="btn btn-outline-primary btn-sm" type="button" onClick={refresh} disabled={isLoading}>
              Refresh
            </button>
            {isLoading ? <Spinner label="Refreshing..." /> : null}
          </div>
        </div>

        <div className="small text-muted mb-3">
          Click a row to expand. Use the “Edit” link to open the dedicated product page.
        </div>

        <ProductList
          products={productsForList}
          expandedId={expandedId}
          onToggle={(id) => setExpandedId((cur) => (cur === id ? null : id))}
          renderActions={(id) => (
            <div className="d-flex gap-2 flex-wrap">
              <Link className="btn btn-sm btn-outline-primary" to={`/products/${id}`}>
                Edit
              </Link>
            </div>
          )}
        />

        <div className="mt-3 small text-muted">
          Categories loaded: {categories.length}. Visit <Link to="/categories">Categories</Link>.
        </div>
      </div>
    </div>
  );
}

