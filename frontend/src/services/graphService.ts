import { api } from "./api";
import type { GraphData } from "../types/graph";

export interface GraphQueryParams {
  node_id: string;
  node_type: string;
  depth?: number;
  max_nodes?: number;
}

export interface SubgraphParams {
  center_node: string;
  time_start: string;
  time_end: string;
  hop_count?: number;
}

export const graphService = {
  async queryNeighborhood(params: GraphQueryParams): Promise<GraphData> {
    return api.post<GraphData>("/graphs/query", params);
  },

  async extractSubgraph(params: SubgraphParams): Promise<GraphData> {
    return api.post<GraphData>("/graphs/subgraph", params);
  },
};
