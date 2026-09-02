/**
 * Graph Type Definitions
 */

export type NodeType = "user" | "device" | "email" | "file" | "url" | "pc";

export interface GraphNode {
  id: string;
  type: NodeType;
  label: string;
  properties: Record<string, unknown>;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  timestamp?: string;
  properties: Record<string, unknown>;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  metadata: Record<string, unknown>;
}
