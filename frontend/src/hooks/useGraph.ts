/**
 * useGraph Hook
 *
 * Graph data fetching and manipulation hook for the graph viewer.
 *
 * Phase 0: Stub only.
 *
 * TODO (Phase 8): Implement graph query and Cytoscape data formatting.
 */

export function useGraph() {
  return {
    graphData: null,
    isLoading: false,
    error: null as string | null,
    queryNeighborhood: async (_nodeId: string, _depth: number) => {},
    extractSubgraph: async (_center: string, _timeStart: string, _timeEnd: string) => {},
  };
}
