import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/services/api";
import type { ItemResponse } from "@/types";

export function getItems(): Promise<ItemResponse[]> {
  return apiFetch<ItemResponse[]>("/api/v1/items/");
}

export function getItem(id: number): Promise<ItemResponse> {
  return apiFetch<ItemResponse>(`/api/v1/items/${id}`);
}

export function useItems() {
  return useQuery({ queryKey: ["items"], queryFn: getItems });
}
