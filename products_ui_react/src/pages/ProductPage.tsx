import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { apiGet, apiSend } from "../api/http";
import type { ApiCategory, ApiProduct } from "../types";
import { Spinner } from "../components/Spinner";
import { ErrorBanner } from "../components/ErrorBanner";

type CategoriesResponse = { categories: ApiCategory[] };

type FormState = {
  name: string;
  brand: string;
  price: string;
  quantity: string;
  category: string;
};

function toForm(p: ApiProduct): FormState {
  return {
    name: p.name ?? "",
    brand: p.brand ?? "",
    price: String(p.price ?? ""),
    quantity: String(p.quantity ?? 0),
    category: p.category ?? ""
  };
}

export function ProductPage() {
  const { productId } = useParams();
  const navigate = useNavigate();

  const [product, setProduct] = useState<ApiProduct | null>(null);
  const [categories, setCategories] = useState<ApiCategory[]>([]);
  const [form, setForm] = useState<FormState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const categoryLabel = useMemo(() => {
    if (!product?.category) return null;
    return product.category_name || categories.find((c) => c.id === product.category)?.title || null;
  }, [product, categories]);

  const refresh = async () => {
    if (!productId) return;
    setIsLoading(true);
    setError(null);
    try {
      const [p, c] = await Promise.all([
        apiGet<ApiProduct>(`/api/products/${encodeURIComponent(productId)}/`),
        apiGet<CategoriesResponse>("/api/categories/")
      ]);
      setProduct(p);
      setCategories(c.categories || []);
      setForm(toForm(p));
    } catch (e: any) {
      setError(e?.payload?.error || e?.message || "Failed to load product");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refresh();
  }, [productId]);

  const onSave = async () => {
    if (!productId || !form) return;
    setIsSaving(true);
    setError(null);
    try {
      const payload = {
        name: form.name.trim(),
        brand: form.brand.trim(),
        price: Number(form.price),
        quantity: Number(form.quantity),
        category: form.category
      };
      await apiSend(`/api/products/${encodeURIComponent(productId)}/`, "PUT", payload);
      await refresh();
    } catch (e: any) {
      const p = e?.payload;
      const msg =
        p?.errors ? `Validation error: ${JSON.stringify(p.errors)}` : p?.error || e?.message || "Save failed";
      setError(msg);
    } finally {
      setIsSaving(false);
    }
  };

  const onDelete = async () => {
    if (!productId) return;
    if (!confirm("Delete this product?")) return;
    setIsSaving(true);
    setError(null);
    try {
      await apiSend(`/api/products/delete/${encodeURIComponent(productId)}/`, "DELETE");
      navigate("/products");
    } catch (e: any) {
      setError(e?.payload?.error || e?.message || "Delete failed");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <div className="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
          <div>
            <div className="fw-semibold">Product</div>
            <div className="small text-muted font-monospace">{productId}</div>
          </div>
          <div className="d-flex gap-2 flex-wrap">
            <Link className="btn btn-outline-secondary btn-sm" to="/products">
              Back to products
            </Link>
            <button className="btn btn-outline-danger btn-sm" type="button" onClick={onDelete} disabled={isSaving}>
              Delete
            </button>
          </div>
        </div>

        {error ? <ErrorBanner message={error} onDismiss={() => setError(null)} /> : null}
        {isLoading ? <Spinner label="Loading product..." /> : null}

        {!isLoading && form ? (
          <div className="row g-3">
            <div className="col-md-6">
              <label className="form-label">Name</label>
              <input
                className="form-control"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
            </div>
            <div className="col-md-6">
              <label className="form-label">Brand</label>
              <input
                className="form-control"
                value={form.brand}
                onChange={(e) => setForm({ ...form, brand: e.target.value })}
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">Price</label>
              <input
                className="form-control"
                value={form.price}
                onChange={(e) => setForm({ ...form, price: e.target.value })}
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">Quantity</label>
              <input
                className="form-control"
                value={form.quantity}
                onChange={(e) => setForm({ ...form, quantity: e.target.value })}
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">Category</label>
              <select
                className="form-select"
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
              >
                <option value="" disabled>
                  — Select —
                </option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.title}
                  </option>
                ))}
              </select>
              <div className="form-text">
                Current:{" "}
                {product?.category ? (
                  <Link to={`/categories/${encodeURIComponent(product.category)}`}>
                    {categoryLabel || product.category}
                  </Link>
                ) : (
                  "—"
                )}
              </div>
            </div>

            <div className="col-12 d-flex gap-2 align-items-center">
              <button className="btn btn-primary" type="button" onClick={onSave} disabled={isSaving}>
                Save changes
              </button>
              {isSaving ? <Spinner label="Saving..." /> : null}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}

