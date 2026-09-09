import { useState, useCallback } from "react";
import { graphService, type GraphQueryParams, type SubgraphParams } from "../services/graphService";
import type { GraphData } from "../types/graph";

export function useGraph() {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const queryNeighborhood = useCallback(async (params: GraphQueryParams) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await graphService.queryNeighborhood(params);
      setGraphData(data);
      return data;
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Failed to query graph neighborhood";
      setError(msg);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const extractSubgraph = useCallback(async (params: SubgraphParams) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await graphService.extractSubgraph(params);
      setGraphData(data);
      return data;
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Failed to extract subgraph";
      setError(msg);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    graphData,
    isLoading,
    error,
    setGraphData,
    queryNeighborhood,
    extractSubgraph,
  };
}
