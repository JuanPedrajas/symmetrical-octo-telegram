export interface ItemResponse {
  id: number;
  name: string;
  description: string;
}

// Feature tree — leaf values are relative path strings; folders are nested objects
export type TreeNode = { [key: string]: TreeNode | string };

export interface TreeResponse {
  tree: TreeNode;
}

export interface StepModel {
  keyword: string;
  text: string;
}

export interface ScenarioModel {
  name: string;
  tags: string[];
  steps: StepModel[];
}

export interface FeatureDetail {
  feature: string;
  description: string;
  tags: string[];
  background: StepModel[];
  scenarios: ScenarioModel[];
}

export interface SaveRequest {
  path: string;
  author: string;
  data: FeatureDetail;
}

export interface SaveResponse {
  status: string;
  path: string;
}
