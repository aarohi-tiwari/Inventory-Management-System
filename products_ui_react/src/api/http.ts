import { ApiError } from "./types";

async function readJsonSafe(res: Response): Promise<unknown> {
  const text = await res.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export async function apiGet<T>(url: string): Promise<T> {
  const res = await fetch(url, { method: "GET" });
  const payload = await readJsonSafe(res);
  if (!res.ok) throw new ApiError(`GET ${url} failed`, res.status, payload as any);
  return payload as T;
}

export async function apiSend<T>(
  url: string,
  method: "POST" | "PUT" | "DELETE",
  body?: unknown
): Promise<T> {
  const res = await fetch(url, {
    method,
    headers: body != null ? { "Content-Type": "application/json" } : undefined,
    body: body != null ? JSON.stringify(body) : undefined
  });
  const payload = await readJsonSafe(res);
  if (!res.ok) throw new ApiError(`${method} ${url} failed`, res.status, payload as any);
  return payload as T;
}

