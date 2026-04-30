import type { Product } from "../types";
import { Product as ProductComponent } from "./Product";

type Props = {
  products: Product[];
  expandedId: string | null;
  onToggle: (id: string) => void;
  renderActions?: (id: string) => React.ReactNode;
};

export function ProductList({ products, expandedId, onToggle, renderActions }: Props) {
  return (
    <div className="pui-list">
      {products.map((p) => (
        <div key={p.id} className="pui-item-wrap">
          <ProductComponent product={p} expanded={p.id === expandedId} onToggle={onToggle} />
          {renderActions ? <div className="pui-actions mt-2">{renderActions(p.id)}</div> : null}
        </div>
      ))}
    </div>
  );
}

