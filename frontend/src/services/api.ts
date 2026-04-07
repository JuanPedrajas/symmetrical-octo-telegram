export const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) {
    const message = await res.text().catch(() => res.statusText);
    throw new Error(message);
  }
  return res.json() as Promise<T>;
}
