import { Link } from "react-router-dom";
import type { Product } from "../types";

type Props = {
  product: Product;
};

const formatINR = (n: number) =>
  n.toLocaleString("en-IN", { style: "currency", currency: "INR" });

export function ProductDetails({ product }: Props) {
  return (
    <div className="pui-details">
      <div className="pui-kv">
        <div className="text-muted">Product ID</div>
        <div className="font-monospace">{product.id}</div>

        <div className="text-muted">SKU</div>
        <div className="font-monospace">{product.sku}</div>

        <div className="text-muted">Category</div>
        <div>
          {product.categoryId ? (
            <Link to={`/categories/${encodeURIComponent(product.categoryId)}`}>
              {product.categoryLabel}
            </Link>
          ) : (
            "—"
          )}
        </div>

        <div className="text-muted">Brand</div>
        <div>{product.brand}</div>

        <div className="text-muted">Price</div>
        <div className="fw-semibold">{formatINR(product.price)}</div>

        <div className="text-muted">Quantity</div>
        <div>{product.quantity}</div>

        <div className="text-muted">Description</div>
        <div>{product.description}</div>

        <div className="text-muted">Created</div>
        <div>{product.createdAt}</div>

        <div className="text-muted">Updated</div>
        <div>{product.updatedAt}</div>
      </div>
    </div>
  );
}

