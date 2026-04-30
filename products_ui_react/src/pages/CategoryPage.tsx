import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { apiGet, apiSend } from "../api/http";
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

export function CategoryPage() {
  const { categoryId } = useParams();
  const [category, setCategory] = useState<ApiCategory | null>(null);
  const [categories, setCategories] = useState<ApiCategory[]>([]);
  const [products, setProducts] = useState<ApiProduct[]>([]);
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
    if (!categoryId) return;
    setIsLoading(true);
    setError(null);
    try {
      const [cat, clist, plist] = await Promise.all([
        apiGet<ApiCategory>(`/api/categories/${encodeURIComponent(categoryId)}/`),
        apiGet<{ categories: ApiCategory[] }>("/api/categories/"),
        apiGet<ProductsListResponse>(
          `/api/products/list/?page=1&limit=100&category=${encodeURIComponent(categoryId)}`
        )
      ]);
      setCategory(cat);
      setCategories(clist.categories || []);
      setProducts(plist.products || []);
    } catch (e: any) {
      setError(e?.payload?.error || e?.message || "Failed to load category");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refresh();
  }, [categoryId]);

  const moveProduct = async (productId: string, newCategoryId: string) => {
    setError(null);
    try {
      // Interactivity: move products across categories by updating product.category
      await apiSend(`/api/products/${encodeURIComponent(productId)}/`, "PUT", { category: newCategoryId });
      await refresh();
    } catch (e: any) {
      const p = e?.payload;
      setError(p?.errors ? JSON.stringify(p.errors) : p?.error || e?.message || "Move failed");
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <div className="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
          <div>
            <div className="fw-semibold">Category</div>
            <div className="small text-muted">
              {category ? (
                <>
                  <span className="fw-semibold">{category.title}</span>{" "}
                  <span className="font-monospace">({category.id})</span>
                </>
              ) : (
                <span className="font-monospace">{categoryId}</span>
              )}
            </div>
          </div>
          <div className="d-flex gap-2 flex-wrap">
            <Link className="btn btn-outline-secondary btn-sm" to="/categories">
              Back to categories
            </Link>
            <button className="btn btn-outline-primary btn-sm" type="button" onClick={refresh} disabled={isLoading}>
              Refresh
            </button>
          </div>
        </div>

        {error ? <ErrorBanner message={error} onDismiss={() => setError(null)} /> : null}
        {isLoading ? <Spinner label="Loading category..." /> : null}

        {!isLoading ? (
          <>
            <div className="small text-muted mb-3">
              Products in this category: {products.length}. Click a row to expand. “Edit” opens the dedicated product
              page.
            </div>

            <ProductList
              products={productsForList}
              expandedId={expandedId}
              onToggle={(id) => setExpandedId((cur) => (cur === id ? null : id))}
              renderActions={(id) => (
                <div className="d-flex gap-2 flex-wrap align-items-center">
                  <Link className="btn btn-sm btn-outline-primary" to={`/products/${id}`}>
                    Edit
                  </Link>
                  <select
                    className="form-select form-select-sm"
                    defaultValue={categoryId}
                    onChange={(e) => moveProduct(id, e.target.value)}
                  >
                    {categories.map((c) => (
                      <option key={c.id} value={c.id}>
                        Move to: {c.title}
                      </option>
                    ))}
                  </select>
                </div>
              )}
            />
          </>
        ) : null}
      </div>
    </div>
  );
}

