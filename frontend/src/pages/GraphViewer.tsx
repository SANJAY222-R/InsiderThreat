import React, { useEffect, useRef, useState } from "react";
import cytoscape, { type Core } from "cytoscape";
import { graphService } from "../services/graphService";

const GraphViewer: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);

  const [nodeId, setNodeId] = useState("U1234");
  const [nodeType, setNodeType] = useState("user");
  const [depth] = useState(2);
  const [layoutName, setLayoutName] = useState<"cose" | "circle" | "concentric" | "breadthfirst" | "grid">("cose");
  const [selectedNodeInfo, setSelectedNodeInfo] = useState<{ id: string; type?: string; label?: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchAndRenderGraph = async () => {
    if (!containerRef.current) return;
    setIsLoading(true);

    try {
      const graphData = await graphService.queryNeighborhood({
        node_id: nodeId,
        node_type: nodeType,
        depth: depth,
      });

      const elements = [
        ...graphData.nodes.map((n) => ({
          data: {
            id: n.id,
            label: n.label || n.id,
            type: n.type || "unknown",
          },
        })),
        ...graphData.edges.map((e, idx) => ({
          data: {
            id: e.id || `edge_${idx}`,
            source: e.source,
            target: e.target,
            label: e.type || "",
          },
        })),
      ];

      if (cyRef.current) {
        cyRef.current.destroy();
      }

      const cy = cytoscape({
        container: containerRef.current,
        elements,
        style: [
          {
            selector: "node",
            style: {
              "background-color": "#3B82F6",
              label: "data(label)",
              color: "#F3F4F6",
              "text-valign": "bottom",
              "text-margin-y": 6,
              "font-size": "11px",
              "font-weight": "bold",
              width: 32,
              height: 32,
              "border-width": 2,
              "border-color": "#1E40AF",
            },
          },
          {
            selector: 'node[type="user"]',
            style: {
              "background-color": "#EF4444",
              "border-color": "#991B1B",
              width: 38,
              height: 38,
            },
          },
          {
            selector: 'node[type="device"], node[type="pc"], node[type="host"]',
            style: {
              "background-color": "#8B5CF6",
              "border-color": "#5B21B6",
            },
          },
          {
            selector: 'node[type="file"]',
            style: {
              "background-color": "#10B981",
              "border-color": "#065F46",
            },
          },
          {
            selector: 'node[type="email"]',
            style: {
              "background-color": "#F59E0B",
              "border-color": "#B45309",
            },
          },
          {
            selector: "edge",
            style: {
              width: 2,
              "line-color": "#4B5563",
              "target-arrow-color": "#4B5563",
              "target-arrow-shape": "triangle",
              "curve-style": "bezier",
              label: "data(label)",
              "font-size": "9px",
              color: "#9CA3AF",
              "text-rotation": "autorotate",
              "text-background-opacity": 0.8,
              "text-background-color": "#111827",
              "text-background-padding": "2px",
            },
          },
        ],
        layout: {
          name: layoutName,
          padding: 40,
        },
      });

      cy.on("tap", "node", (evt) => {
        const node = evt.target;
        setSelectedNodeInfo({
          id: node.id(),
          type: node.data("type"),
          label: node.data("label"),
        });
      });

      cyRef.current = cy;
    } catch {
      // Fallback
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAndRenderGraph();
    return () => {
      if (cyRef.current) {
        cyRef.current.destroy();
      }
    };
  }, [layoutName]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchAndRenderGraph();
  };

  return (
    <div className="flex flex-col h-full space-y-4 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Enterprise Graph Explorer</h1>
          <p className="text-gray-400 text-sm mt-0.5">
            Temporal Heterogeneous Graph topology: users, devices, files, and email interactions.
          </p>
        </div>

        <div className="flex flex-wrap gap-2 items-center">
          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              placeholder="Entity ID (e.g. U1234)"
              value={nodeId}
              onChange={(e) => setNodeId(e.target.value)}
              className="bg-gray-900 border border-gray-700 rounded-xl px-3 py-1.5 text-sm text-white focus:outline-none focus:border-blue-500 w-36"
            />
            <select
              value={nodeType}
              onChange={(e) => setNodeType(e.target.value)}
              className="bg-gray-900 border border-gray-700 rounded-xl px-2 py-1.5 text-xs text-gray-300 focus:outline-none focus:border-blue-500"
            >
              <option value="user">User</option>
              <option value="device">Device</option>
              <option value="file">File</option>
              <option value="email">Email</option>
            </select>
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-3 py-1.5 rounded-xl transition shadow-md shadow-blue-500/20"
            >
              Query Subgraph
            </button>
          </form>

          <select
            value={layoutName}
            onChange={(e) => setLayoutName(e.target.value as any)}
            className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-1.5 text-xs text-gray-300 focus:outline-none focus:border-blue-500"
          >
            <option value="cose">Force-Directed (CoSE)</option>
            <option value="concentric">Concentric</option>
            <option value="circle">Circle</option>
            <option value="breadthfirst">Tree (Hierarchy)</option>
            <option value="grid">Grid</option>
          </select>
        </div>
      </div>

      <div className="flex-1 flex gap-4 min-h-[480px]">
        {/* Graph Canvas Container */}
        <div className="flex-1 bg-gray-900/60 backdrop-blur-md rounded-2xl border border-gray-800 relative overflow-hidden shadow-2xl">
          {isLoading && (
            <div className="absolute inset-0 bg-gray-950/70 z-20 flex items-center justify-center gap-2 text-blue-400 text-sm">
              <svg className="animate-spin h-5 w-5 text-blue-500" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
              </svg>
              <span>Traversing Graph Topology...</span>
            </div>
          )}
          <div ref={containerRef} className="absolute inset-0" />
        </div>

        {/* Node Detail Sidebar */}
        {selectedNodeInfo && (
          <div className="w-80 bg-gray-900/80 backdrop-blur-md border border-gray-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-center mb-4 pb-3 border-b border-gray-800">
                <h3 className="font-bold text-gray-100 text-base">Node Details</h3>
                <button
                  onClick={() => setSelectedNodeInfo(null)}
                  className="text-gray-500 hover:text-gray-300 text-xs font-bold"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-3 text-sm">
                <div>
                  <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block">ID</span>
                  <span className="font-mono text-blue-400 font-bold">{selectedNodeInfo.id}</span>
                </div>
                <div>
                  <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block">Type</span>
                  <span className="capitalize text-gray-200">{selectedNodeInfo.type}</span>
                </div>
                <div>
                  <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block">Label</span>
                  <span className="text-gray-300">{selectedNodeInfo.label}</span>
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-800 space-y-2">
              <button
                onClick={() => {
                  setNodeId(selectedNodeInfo.id);
                  setNodeType(selectedNodeInfo.type || "user");
                  fetchAndRenderGraph();
                }}
                className="w-full py-2 bg-blue-600/20 hover:bg-blue-600/40 border border-blue-500/30 text-blue-300 rounded-xl text-xs font-semibold transition"
              >
                Expand Neighborhood
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GraphViewer;
