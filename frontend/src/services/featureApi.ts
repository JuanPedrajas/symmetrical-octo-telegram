import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/services/api";
import type { FeatureDetail, SaveRequest, SaveResponse, TreeResponse } from "@/types";

export function getFeatureTree(): Promise<TreeResponse> {
  return apiFetch<TreeResponse>("/api/v1/features/tree");
}

export function getFeatureDetail(path: string): Promise<FeatureDetail> {
  return apiFetch<FeatureDetail>(`/api/v1/features/detail?path=${encodeURIComponent(path)}`);
}

export function saveFeature(body: SaveRequest): Promise<SaveResponse> {
  return apiFetch<SaveResponse>("/api/v1/features/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

export function useFeatureTree() {
  return useQuery({ queryKey: ["feature-tree"], queryFn: getFeatureTree });
}

export function useFeatureDetail(path: string | null) {
  return useQuery({
    queryKey: ["feature-detail", path],
    queryFn: () => getFeatureDetail(path!),
    enabled: !!path,
  });
}

export function useSaveFeature() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: saveFeature,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["feature-tree"] });
    },
  });
}
