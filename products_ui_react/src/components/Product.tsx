import type { Product as ProductT } from "../types";
import { ProductDetails } from "./ProductDetails";

type Props = {
  product: ProductT;
  expanded: boolean;
  onToggle: (id: string) => void;
};

const formatINR = (n: number) =>
  n.toLocaleString("en-IN", { style: "currency", currency: "INR" });

export function Product({ product, expanded, onToggle }: Props) {
  const onKeyDown: React.KeyboardEventHandler<HTMLDivElement> = (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      onToggle(product.id);
    }
  };

  return (
    <div className="pui-item card">
      <div
        className="pui-row card-body"
        role="button"
        tabIndex={0}
        aria-expanded={expanded}
        onClick={() => onToggle(product.id)}
        onKeyDown={onKeyDown}
      >
        <div className="pui-main">
          <div className="d-flex align-items-center gap-2 flex-wrap">
            <div className="fw-semibold">{product.name}</div>
            <span className="badge rounded-pill text-bg-light">
              {product.categoryLabel}
            </span>
            <span className="badge rounded-pill text-bg-secondary">
              {product.brand}
            </span>
          </div>
          <div className="small text-muted mt-1 d-flex gap-2 flex-wrap align-items-center">
            <span>Price: {formatINR(product.price)}</span>
            <span>·</span>
            <span>Qty: {product.quantity}</span>
            <span>·</span>
            <span className="font-monospace">{product.sku}</span>
          </div>
        </div>
        <div className="pui-chev">{expanded ? "−" : "+"}</div>
      </div>

      {expanded ? <ProductDetails product={product} /> : null}
    </div>
  );
}

