import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { GraphNode, GraphEdge } from "../../types/graph";

export interface GraphSliceState {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedNode: GraphNode | null;
  layout: "cose" | "concentric" | "circle" | "grid" | "breadthfirst";
  depth: number;
  isLoading: boolean;
  error: string | null;
}

const initialState: GraphSliceState = {
  nodes: [],
  edges: [],
  selectedNode: null,
  layout: "cose",
  depth: 2,
  isLoading: false,
  error: null,
};

export const graphSlice = createSlice({
  name: "graph",
  initialState,
  reducers: {
    setGraphData(state, action: PayloadAction<{ nodes: GraphNode[]; edges: GraphEdge[] }>) {
      state.nodes = action.payload.nodes;
      state.edges = action.payload.edges;
      state.isLoading = false;
      state.error = null;
    },
    setSelectedNode(state, action: PayloadAction<GraphNode | null>) {
      state.selectedNode = action.payload;
    },
    setLayout(state, action: PayloadAction<"cose" | "concentric" | "circle" | "grid" | "breadthfirst">) {
      state.layout = action.payload;
    },
    setDepth(state, action: PayloadAction<number>) {
      state.depth = action.payload;
    },
    setGraphLoading(state, action: PayloadAction<boolean>) {
      state.isLoading = action.payload;
    },
    setGraphError(state, action: PayloadAction<string | null>) {
      state.error = action.payload;
      state.isLoading = false;
    },
    resetGraph(state) {
      state.nodes = [];
      state.edges = [];
      state.selectedNode = null;
      state.isLoading = false;
      state.error = null;
    },
  },
});

export const {
  setGraphData,
  setSelectedNode,
  setLayout,
  setDepth,
  setGraphLoading,
  setGraphError,
  resetGraph,
} = graphSlice.actions;

export default graphSlice.reducer;
