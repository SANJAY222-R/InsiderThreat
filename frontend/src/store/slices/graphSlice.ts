/**
 * Graph Slice
 *
 * Redux state for graph viewer data and controls.
 *
 * Phase 0: Stub only.
 */

export interface GraphSliceState {
  nodes: unknown[];
  edges: unknown[];
  selectedNode: string | null;
  layout: string;
  isLoading: boolean;
}

export const initialGraphState: GraphSliceState = {
  nodes: [],
  edges: [],
  selectedNode: null,
  layout: "cose",
  isLoading: false,
};

// TODO: Implement with createSlice
