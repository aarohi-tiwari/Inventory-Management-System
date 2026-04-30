export type ApiErrorPayload =
  | { error: string }
  | { errors: Record<string, unknown> }
  | Record<string, unknown>;

export class ApiError extends Error {
  status: number;
  payload?: ApiErrorPayload;

  constructor(message: string, status: number, payload?: ApiErrorPayload) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
  }
}

