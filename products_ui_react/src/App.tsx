import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import { ProductsPage } from "./pages/ProductsPage";
import { ProductPage } from "./pages/ProductPage";
import { CategoriesPage } from "./pages/CategoriesPage";
import { CategoryPage } from "./pages/CategoryPage";

export default function App() {
  return (
    <div className="pui-shell">
      <header className="pui-header">
        <nav className="navbar navbar-expand-lg bg-body-tertiary border rounded-3 px-3">
          <div className="container-fluid px-0">
            <NavLink className="navbar-brand fw-semibold" to="/products">
              Inventory
            </NavLink>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#puiNavbar"
              aria-controls="puiNavbar"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon" />
            </button>

            <div className="collapse navbar-collapse" id="puiNavbar">
              <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                <li className="nav-item">
                  <NavLink className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`} to="/products">
                    Products
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`} to="/categories">
                    Categories
                  </NavLink>
                </li>
              </ul>
              <div className="d-flex gap-2">
                <a className="btn btn-outline-secondary btn-sm" href="/">
                  Existing UI
                </a>
              </div>
            </div>
          </div>
        </nav>
      </header>

      <main className="pui-main-content">
        <Routes>
          <Route path="/" element={<Navigate to="/products" replace />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/products/:productId" element={<ProductPage />} />
          <Route path="/categories" element={<CategoriesPage />} />
          <Route path="/categories/:categoryId" element={<CategoryPage />} />
          <Route path="*" element={<Navigate to="/products" replace />} />
        </Routes>
      </main>
    </div>
  );
}

