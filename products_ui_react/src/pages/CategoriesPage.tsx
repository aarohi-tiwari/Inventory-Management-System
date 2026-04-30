import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet, apiSend } from "../api/http";
import type { ApiCategory } from "../types";
import { Spinner } from "../components/Spinner";
import { ErrorBanner } from "../components/ErrorBanner";

type CategoriesResponse = { categories: ApiCategory[] };

export function CategoriesPage() {
  const [categories, setCategories] = useState<ApiCategory[]>([]);
  const [newTitle, setNewTitle] = useState("");
  const [editing, setEditing] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await apiGet<CategoriesResponse>("/api/categories/");
      setCategories(res.categories || []);
    } catch (e: any) {
      setError(e?.payload?.error || e?.message || "Failed to load categories");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const create = async () => {
    setError(null);
    try {
      await apiSend("/api/categories/", "POST", { title: newTitle.trim() });
      setNewTitle("");
      await refresh();
    } catch (e: any) {
      const p = e?.payload;
      setError(p?.errors ? JSON.stringify(p.errors) : p?.error || e?.message || "Create failed");
    }
  };

  const save = async (id: string) => {
    setError(null);
    try {
      await apiSend(`/api/categories/${encodeURIComponent(id)}/update/`, "PUT", { title: editing[id]?.trim() });
      setEditing((m) => {
        const next = { ...m };
        delete next[id];
        return next;
      });
      await refresh();
    } catch (e: any) {
      const p = e?.payload;
      setError(p?.errors ? JSON.stringify(p.errors) : p?.error || e?.message || "Update failed");
    }
  };

  const del = async (id: string) => {
    if (!confirm("Delete this category?")) return;
    setError(null);
    try {
      await apiSend(`/api/categories/${encodeURIComponent(id)}/delete/`, "DELETE");
      await refresh();
    } catch (e: any) {
      setError(e?.payload?.error || e?.message || "Delete failed");
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        {error ? <ErrorBanner message={error} onDismiss={() => setError(null)} /> : null}

        <div className="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
          <div className="fw-semibold">Categories</div>
          <div className="d-flex align-items-center gap-2">
            <button className="btn btn-outline-primary btn-sm" type="button" onClick={refresh} disabled={isLoading}>
              Refresh
            </button>
            {isLoading ? <Spinner label="Refreshing..." /> : null}
          </div>
        </div>

        <div className="row g-2 align-items-end mb-3">
          <div className="col-md-8">
            <label className="form-label">New category title</label>
            <input className="form-control" value={newTitle} onChange={(e) => setNewTitle(e.target.value)} />
          </div>
          <div className="col-md-4 d-flex gap-2">
            <button className="btn btn-primary w-100" type="button" onClick={create} disabled={!newTitle.trim()}>
              Create
            </button>
          </div>
        </div>

        <div className="list-group">
          {categories.map((c) => {
            const value = editing[c.id] ?? c.title;
            const isEditing = editing[c.id] != null;
            return (
              <div key={c.id} className="list-group-item">
                <div className="d-flex justify-content-between gap-2 flex-wrap">
                  <div>
                    <div className="fw-semibold">
                      <Link to={`/categories/${encodeURIComponent(c.id)}`}>{c.title}</Link>
                    </div>
                    <div className="small text-muted font-monospace">{c.id}</div>
                  </div>
                  <div className="d-flex gap-2 flex-wrap">
                    <button className="btn btn-outline-danger btn-sm" type="button" onClick={() => del(c.id)}>
                      Delete
                    </button>
                  </div>
                </div>

                <div className="mt-2 d-flex gap-2 flex-wrap">
                  <input
                    className="form-control"
                    value={value}
                    onChange={(e) => setEditing((m) => ({ ...m, [c.id]: e.target.value }))}
                  />
                  <button
                    className="btn btn-outline-secondary"
                    type="button"
                    onClick={() =>
                      setEditing((m) => {
                        const next = { ...m };
                        if (next[c.id] == null) next[c.id] = c.title;
                        return next;
                      })
                    }
                  >
                    Edit
                  </button>
                  <button className="btn btn-success" type="button" onClick={() => save(c.id)} disabled={!isEditing}>
                    Save
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-3 small text-muted">
          Back to <Link to="/products">Products</Link>
        </div>
      </div>
    </div>
  );
}

