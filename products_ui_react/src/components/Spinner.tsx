type Props = {
  label?: string;
};

export function Spinner({ label = "Loading..." }: Props) {
  return (
    <div className="d-flex align-items-center gap-2 text-muted">
      <div className="spinner-border spinner-border-sm" role="status" aria-label={label} />
      <span className="small">{label}</span>
    </div>
  );
}

