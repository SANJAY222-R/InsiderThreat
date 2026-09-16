import { api } from "./api";
import type { GraphData, SampleEntity } from "../types/graph";

export interface GraphQueryParams {
  node_id: string;
  node_type?: string;
  depth?: number;
  max_nodes?: number;
}

export interface SubgraphParams {
  center_node: string;
  time_start?: string;
  time_end?: string;
  hop_count?: number;
}

export interface AddEventParams {
  user_id: string;
  event_type: string;
  target_entity: string;
  target_type?: string;
  timestamp?: string;
  metadata?: Record<string, any>;
}

export const graphService = {
  async getSampleEntities(): Promise<SampleEntity[]> {
    return api.get<SampleEntity[]>("/graphs/samples");
  },

  async queryNeighborhood(params: GraphQueryParams): Promise<GraphData> {
    return api.post<GraphData>("/graphs/query", params);
  },

  async extractSubgraph(params: SubgraphParams): Promise<GraphData> {
    return api.post<GraphData>("/graphs/subgraph", params);
  },

  async addEvent(params: AddEventParams): Promise<{ status: string; message: string }> {
    return api.post<{ status: string; message: string }>("/graphs/event", params);
  },
};
