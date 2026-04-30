type Props = {
  title?: string;
  message: string;
  onDismiss?: () => void;
};

export function ErrorBanner({ title = "Action failed", message, onDismiss }: Props) {
  return (
    <div className="alert alert-danger d-flex align-items-start justify-content-between gap-3" role="alert">
      <div>
        <div className="fw-semibold">{title}</div>
        <div className="small">{message}</div>
      </div>
      {onDismiss ? (
        <button type="button" className="btn btn-sm btn-outline-danger" onClick={onDismiss}>
          Dismiss
        </button>
      ) : null}
    </div>
  );
}

