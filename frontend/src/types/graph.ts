/**
 * Graph Type Definitions
 */

export type NodeType = "user" | "device" | "email" | "file" | "url" | "pc" | "usb" | "unknown";

export interface GraphNode {
  id: string;
  type: NodeType | string;
  label: string;
  properties?: Record<string, any>;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label?: string;
  timestamp?: string;
  properties?: Record<string, any>;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  metadata?: Record<string, any>;
}

export interface SampleEntity {
  id: string;
  label: string;
  type: string;
  role?: string;
  department?: string;
}
