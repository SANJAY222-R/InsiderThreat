import React, { useEffect, useRef, useState } from "react";
import cytoscape, { type Core } from "cytoscape";
import { graphService } from "../services/graphService";
import type { SampleEntity } from "../types/graph";

const GraphViewer: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);

  const [nodeId, setNodeId] = useState("MOH0273");
  const [nodeType, setNodeType] = useState("user");
  const [depth, setDepth] = useState(2);
  const [layoutName, setLayoutName] = useState<"cose" | "circle" | "concentric" | "breadthfirst" | "grid">("cose");
  const [selectedNodeInfo, setSelectedNodeInfo] = useState<{
    id: string;
    type?: string;
    label?: string;
    properties?: Record<string, any>;
  } | null>(null);
  const [sampleEntities, setSampleEntities] = useState<SampleEntity[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [graphStats, setGraphStats] = useState<{ totalNodes: number; totalEdges: number } | null>(null);

  // Dynamic Event Injection State
  const [isEventModalOpen, setIsEventModalOpen] = useState(false);
  const [newEventUser, setNewEventUser] = useState("MOH0273");
  const [newEventType, setNewEventType] = useState("usb_connect");
  const [newEventTarget, setNewEventTarget] = useState("USB-SECURE-BACKUP");
  const [newEventTargetType, setNewEventTargetType] = useState("usb");
  const [eventSuccessMsg, setEventSuccessMsg] = useState<string | null>(null);

  // Fetch sample entities on mount
  useEffect(() => {
    const loadSamples = async () => {
      try {
        const samples = await graphService.getSampleEntities();
        if (samples && samples.length > 0) {
          setSampleEntities(samples);
        }
      } catch (err) {
        console.warn("Could not load sample entities:", err);
      }
    };
    loadSamples();
  }, []);

  const fetchAndRenderGraph = async (targetId?: string, targetType?: string) => {
    if (!containerRef.current) return;
    setIsLoading(true);
    setErrorMessage(null);

    const qId = targetId || nodeId;
    const qType = targetType || nodeType;

    try {
      const graphData = await graphService.queryNeighborhood({
        node_id: qId,
        node_type: qType,
        depth: depth,
        max_nodes: 80,
      });

      if (!graphData.nodes || graphData.nodes.length === 0) {
        setErrorMessage(`No graph neighborhood found for entity ${qId}.`);
        setIsLoading(false);
        return;
      }

      setGraphStats({
        totalNodes: graphData.nodes.length,
        totalEdges: graphData.edges ? graphData.edges.length : 0,
      });

      const elements = [
        ...graphData.nodes.map((n) => ({
          data: {
            id: n.id,
            label: n.label || n.id,
            type: n.type || "unknown",
            properties: n.properties || {},
          },
        })),
        ...(graphData.edges || []).map((e, idx) => ({
          data: {
            id: e.id || `edge_${idx}_${e.source}_${e.target}`,
            source: e.source,
            target: e.target,
            label: e.label || e.type || "",
            type: e.type || "related_to",
            properties: e.properties || {},
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
              "font-size": "10px",
              "font-weight": "bold",
              width: 34,
              height: 34,
              "border-width": 2,
              "border-color": "#1E40AF",
              "text-background-opacity": 0.8,
              "text-background-color": "#111827",
              "text-background-padding": "2px",
              "text-background-shape": "roundrectangle",
            },
          },
          {
            selector: 'node[type="user"]',
            style: {
              "background-color": "#3B82F6",
              "border-color": "#1D4ED8",
              width: 40,
              height: 40,
            },
          },
          {
            selector: `node[id="${qId}"]`,
            style: {
              "background-color": "#EF4444",
              "border-color": "#FCA5A5",
              "border-width": 4,
              width: 48,
              height: 48,
              "font-size": "12px",
              color: "#FEF08A",
            },
          },
          {
            selector: 'node[type="device"], node[type="pc"], node[type="host"], node[type="workstation"]',
            style: {
              "background-color": "#8B5CF6",
              "border-color": "#5B21B6",
              width: 32,
              height: 32,
            },
          },
          {
            selector: 'node[type="usb"]',
            style: {
              "background-color": "#EC4899",
              "border-color": "#9D174D",
              width: 30,
              height: 30,
            },
          },
          {
            selector: 'node[type="file"]',
            style: {
              "background-color": "#10B981",
              "border-color": "#065F46",
              width: 28,
              height: 28,
            },
          },
          {
            selector: 'node[type="email"]',
            style: {
              "background-color": "#F59E0B",
              "border-color": "#B45309",
              width: 28,
              height: 28,
            },
          },
          {
            selector: "edge",
            style: {
              width: 2,
              "line-color": "#4B5563",
              "target-arrow-color": "#6B7280",
              "target-arrow-shape": "triangle",
              "arrow-scale": 0.9,
              "curve-style": "bezier",
              label: "data(label)",
              "font-size": "8px",
              color: "#9CA3AF",
              "text-rotation": "autorotate",
              "text-background-opacity": 0.85,
              "text-background-color": "#0F172A",
              "text-background-padding": "2px",
              "text-background-shape": "roundrectangle",
            },
          },
          {
            selector: 'edge[type="usb_connect"]',
            style: {
              "line-color": "#EC4899",
              "target-arrow-color": "#EC4899",
              width: 2.5,
            },
          },
          {
            selector: 'edge[type="sent_email"]',
            style: {
              "line-color": "#F59E0B",
              "target-arrow-color": "#F59E0B",
            },
          },
          {
            selector: 'edge[type="reports_to"]',
            style: {
              "line-color": "#60A5FA",
              "target-arrow-color": "#60A5FA",
              "line-style": "dashed",
            },
          },
          {
            selector: "node:selected",
            style: {
              "border-color": "#FBBF24",
              "border-width": 4,
            },
          },
        ],
        layout: {
          name: layoutName,
          padding: 50,
        },
      });

      cy.on("tap", "node", (evt) => {
        const node = evt.target;
        setSelectedNodeInfo({
          id: node.id(),
          type: node.data("type"),
          label: node.data("label"),
          properties: node.data("properties") || {},
        });
      });

      cyRef.current = cy;
    } catch (err: any) {
      console.error("Failed to query graph:", err);
      setErrorMessage(err.message || "Failed to load graph neighborhood.");
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
  }, [layoutName, depth]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchAndRenderGraph();
  };

  const handleSelectSample = (sample: SampleEntity) => {
    setNodeId(sample.id);
    setNodeType(sample.type || "user");
    fetchAndRenderGraph(sample.id, sample.type || "user");
  };

  const handleAddCustomEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await graphService.addEvent({
        user_id: newEventUser,
        event_type: newEventType,
        target_entity: newEventTarget,
        target_type: newEventTargetType,
        timestamp: new Date().toISOString(),
      });
      setEventSuccessMsg(`Injected event: ${newEventUser} -> [${newEventType}] -> ${newEventTarget}`);
      setTimeout(() => setEventSuccessMsg(null), 4000);
      setIsEventModalOpen(false);
      // Refresh current graph
      fetchAndRenderGraph();
    } catch (err: any) {
      alert("Failed to inject event: " + (err.message || err));
    }
  };

  return (
    <div className="flex flex-col h-full space-y-4 animate-in fade-in duration-500">
      {/* Top Header & Controls */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 bg-gray-900/60 backdrop-blur-md p-4 rounded-2xl border border-gray-800">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-extrabold text-white tracking-tight">Enterprise Graph Explorer</h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
              CERT r4.2 Multi-Relational Index
            </span>
          </div>
          <p className="text-gray-400 text-xs mt-1">
            Temporal Heterogeneous Graph topology: multi-hop relationships between users, devices, files, emails, and USB activity.
          </p>
        </div>

        <div className="flex flex-wrap gap-2 items-center">
          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              placeholder="Entity ID (e.g. MOH0273)"
              value={nodeId}
              onChange={(e) => setNodeId(e.target.value)}
              className="bg-gray-950 border border-gray-700 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-blue-500 w-36 font-mono"
            />
            <select
              value={nodeType}
              onChange={(e) => setNodeType(e.target.value)}
              className="bg-gray-950 border border-gray-700 rounded-xl px-2 py-1.5 text-xs text-gray-300 focus:outline-none focus:border-blue-500"
            >
              <option value="user">User</option>
              <option value="device">Device</option>
              <option value="file">File</option>
              <option value="email">Email</option>
              <option value="usb">USB</option>
            </select>
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-3 py-1.5 rounded-xl transition shadow-md shadow-blue-500/20"
            >
              Query Graph
            </button>
          </form>

          {/* Depth Control */}
          <div className="flex items-center gap-1 bg-gray-950 border border-gray-700 rounded-xl px-2 py-1">
            <span className="text-[11px] text-gray-400 font-medium">Hops:</span>
            <select
              value={depth}
              onChange={(e) => setDepth(Number(e.target.value))}
              className="bg-transparent text-xs text-white focus:outline-none"
            >
              <option value={1}>1-hop</option>
              <option value={2}>2-hop</option>
              <option value={3}>3-hop</option>
            </select>
          </div>

          {/* Layout Selector */}
          <select
            value={layoutName}
            onChange={(e) => setLayoutName(e.target.value as any)}
            className="bg-gray-950 border border-gray-700 rounded-xl px-3 py-1.5 text-xs text-gray-300 focus:outline-none focus:border-blue-500"
          >
            <option value="cose">Force-Directed (CoSE)</option>
            <option value="concentric">Concentric Circles</option>
            <option value="circle">Radial Circle</option>
            <option value="breadthfirst">Organizational Hierarchy</option>
            <option value="grid">Orthogonal Grid</option>
          </select>

          {/* Inject Dynamic Event Button */}
          <button
            onClick={() => setIsEventModalOpen(true)}
            className="bg-purple-600/20 hover:bg-purple-600/40 border border-purple-500/30 text-purple-300 text-xs font-semibold px-3 py-1.5 rounded-xl transition flex items-center gap-1.5"
          >
            <span>+</span> Inject Test Event
          </button>
        </div>
      </div>

      {/* Quick Entity Sample Chips */}
      {sampleEntities.length > 0 && (
        <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
          <span className="text-gray-400 font-semibold uppercase tracking-wider text-[10px] whitespace-nowrap">
            Curated Entities:
          </span>
          {sampleEntities.slice(0, 8).map((s) => (
            <button
              key={s.id}
              onClick={() => handleSelectSample(s)}
              className={`px-2.5 py-1 rounded-lg border text-xs font-mono transition whitespace-nowrap ${
                nodeId === s.id
                  ? "bg-blue-600 text-white border-blue-400 font-bold shadow"
                  : "bg-gray-900/80 hover:bg-gray-800 text-gray-300 border-gray-800"
              }`}
            >
              {s.id} {s.role ? `(${s.role.slice(0, 14)})` : ""}
            </button>
          ))}
        </div>
      )}

      {/* Event Success Banner */}
      {eventSuccessMsg && (
        <div className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-4 py-2 rounded-xl text-xs flex items-center justify-between animate-in fade-in">
          <span>{eventSuccessMsg}</span>
        </div>
      )}

      {/* Error Banner */}
      {errorMessage && (
        <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-2 rounded-xl text-xs flex items-center justify-between">
          <span>{errorMessage}</span>
          <button onClick={() => setErrorMessage(null)} className="text-red-300 font-bold">✕</button>
        </div>
      )}

      {/* Main Graph Canvas & Sidebar */}
      <div className="flex-1 flex gap-4 min-h-[500px]">
        {/* Graph Canvas Container */}
        <div className="flex-1 bg-gray-950/80 backdrop-blur-md rounded-2xl border border-gray-800 relative overflow-hidden shadow-2xl flex flex-col">
          {/* Legend Overlay */}
          <div className="absolute top-3 left-3 z-10 bg-gray-900/90 backdrop-blur-md px-3 py-2 rounded-xl border border-gray-800 flex items-center gap-3 text-[11px] text-gray-300 pointer-events-none">
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block" /> User</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-purple-500 inline-block" /> Workstation</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-pink-500 inline-block" /> USB</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block" /> File</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block" /> Email</span>
          </div>

          {/* Graph Stats Overlay */}
          {graphStats && (
            <div className="absolute top-3 right-3 z-10 bg-gray-900/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-gray-800 text-[11px] text-gray-400 font-mono pointer-events-none">
              Nodes: <span className="text-blue-400 font-bold">{graphStats.totalNodes}</span> | Edges: <span className="text-emerald-400 font-bold">{graphStats.totalEdges}</span>
            </div>
          )}

          {/* Zoom / Viewport Toolbar */}
          <div className="absolute bottom-3 left-3 z-10 bg-gray-900/90 backdrop-blur-md p-1.5 rounded-xl border border-gray-800 flex items-center gap-1">
            <button
              onClick={() => cyRef.current?.zoom(cyRef.current.zoom() * 1.25)}
              className="px-2 py-1 hover:bg-gray-800 text-gray-200 text-xs rounded-lg font-bold"
              title="Zoom In"
            >
              +
            </button>
            <button
              onClick={() => cyRef.current?.zoom(cyRef.current.zoom() * 0.8)}
              className="px-2 py-1 hover:bg-gray-800 text-gray-200 text-xs rounded-lg font-bold"
              title="Zoom Out"
            >
              -
            </button>
            <button
              onClick={() => cyRef.current?.fit(undefined, 30)}
              className="px-2 py-1 hover:bg-gray-800 text-gray-200 text-xs rounded-lg font-medium"
              title="Fit View"
            >
              Fit
            </button>
            <button
              onClick={() => cyRef.current?.center()}
              className="px-2 py-1 hover:bg-gray-800 text-gray-200 text-xs rounded-lg font-medium"
              title="Center View"
            >
              Center
            </button>
          </div>

          {isLoading && (
            <div className="absolute inset-0 bg-gray-950/70 z-20 flex items-center justify-center gap-2 text-blue-400 text-sm">
              <svg className="animate-spin h-5 w-5 text-blue-500" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
              </svg>
              <span>Indexing and traversing heterogeneous graph...</span>
            </div>
          )}
          <div ref={containerRef} className="flex-1 w-full h-full" />
        </div>

        {/* Node Detail Sidebar */}
        {selectedNodeInfo ? (
          <div className="w-80 bg-gray-900/90 backdrop-blur-md border border-gray-800 rounded-2xl p-5 shadow-2xl flex flex-col justify-between animate-in slide-in-from-right-4 duration-300">
            <div>
              <div className="flex justify-between items-center mb-4 pb-3 border-b border-gray-800">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-blue-500 inline-block" />
                  <h3 className="font-bold text-gray-100 text-base">Node Inspector</h3>
                </div>
                <button
                  onClick={() => setSelectedNodeInfo(null)}
                  className="text-gray-500 hover:text-gray-300 text-xs font-bold p-1"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-3.5 text-xs">
                <div>
                  <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider block">ID</span>
                  <span className="font-mono text-blue-400 font-bold text-sm">{selectedNodeInfo.id}</span>
                </div>
                <div>
                  <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider block">Type</span>
                  <span className="capitalize px-2 py-0.5 rounded bg-gray-800 text-gray-200 font-medium inline-block mt-0.5">
                    {selectedNodeInfo.type}
                  </span>
                </div>
                <div>
                  <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider block">Label</span>
                  <span className="text-gray-200 font-medium">{selectedNodeInfo.label}</span>
                </div>

                {/* Additional Properties */}
                {selectedNodeInfo.properties && Object.keys(selectedNodeInfo.properties).length > 0 && (
                  <div className="pt-2 border-t border-gray-800 space-y-1.5">
                    <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider block">
                      Attributes
                    </span>
                    {Object.entries(selectedNodeInfo.properties).map(([k, v]) => {
                      if (!v || typeof v === "object") return null;
                      return (
                        <div key={k} className="flex justify-between text-[11px] py-0.5">
                          <span className="text-gray-400 capitalize">{k.replace(/_/g, " ")}:</span>
                          <span className="text-gray-200 font-medium truncate max-w-[140px]">{String(v)}</span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>

            <div className="pt-4 border-t border-gray-800 space-y-2">
              <button
                onClick={() => {
                  setNodeId(selectedNodeInfo.id);
                  setNodeType(selectedNodeInfo.type || "user");
                  fetchAndRenderGraph(selectedNodeInfo.id, selectedNodeInfo.type || "user");
                }}
                className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-semibold transition shadow-md shadow-blue-500/20"
              >
                Focus & Expand This Node
              </button>
            </div>
          </div>
        ) : (
          <div className="w-72 bg-gray-900/40 backdrop-blur-md border border-gray-800/80 rounded-2xl p-5 flex flex-col justify-center items-center text-center text-gray-500 text-xs">
            <svg className="w-8 h-8 text-gray-600 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
            </svg>
            <p className="font-medium text-gray-400">Select any entity or connection in the graph to view properties and expand relationships.</p>
          </div>
        )}
      </div>

      {/* Dynamic Event Injection Modal */}
      {isEventModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 w-full max-w-md shadow-2xl animate-in zoom-in-95">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-bold text-white">Inject Dynamic Security Event</h2>
              <button onClick={() => setIsEventModalOpen(false)} className="text-gray-400 hover:text-white">✕</button>
            </div>
            <form onSubmit={handleAddCustomEvent} className="space-y-4 text-xs">
              <div>
                <label className="block text-gray-300 font-semibold mb-1">User ID</label>
                <input
                  type="text"
                  value={newEventUser}
                  onChange={(e) => setNewEventUser(e.target.value)}
                  className="w-full bg-gray-950 border border-gray-700 rounded-xl px-3 py-2 text-white font-mono"
                  required
                />
              </div>

              <div>
                <label className="block text-gray-300 font-semibold mb-1">Event Type</label>
                <select
                  value={newEventType}
                  onChange={(e) => setNewEventType(e.target.value)}
                  className="w-full bg-gray-950 border border-gray-700 rounded-xl px-3 py-2 text-white"
                >
                  <option value="usb_connect">USB Connect (Removable Media)</option>
                  <option value="accessed">File Access (Download / Read)</option>
                  <option value="sent_email">Sent External Email</option>
                  <option value="uses">Logon to Workstation</option>
                </select>
              </div>

              <div>
                <label className="block text-gray-300 font-semibold mb-1">Target Entity Name / ID</label>
                <input
                  type="text"
                  value={newEventTarget}
                  onChange={(e) => setNewEventTarget(e.target.value)}
                  placeholder="e.g. PC-9999, CONFIDENTIAL_PROJECT.docx, target@external.net"
                  className="w-full bg-gray-950 border border-gray-700 rounded-xl px-3 py-2 text-white font-mono"
                  required
                />
              </div>

              <div>
                <label className="block text-gray-300 font-semibold mb-1">Target Entity Type</label>
                <select
                  value={newEventTargetType}
                  onChange={(e) => setNewEventTargetType(e.target.value)}
                  className="w-full bg-gray-950 border border-gray-700 rounded-xl px-3 py-2 text-white"
                >
                  <option value="usb">USB Device</option>
                  <option value="file">File</option>
                  <option value="email">Email</option>
                  <option value="device">Workstation / Host</option>
                </select>
              </div>

              <div className="flex justify-end gap-2 pt-4">
                <button
                  type="button"
                  onClick={() => setIsEventModalOpen(false)}
                  className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-xl font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl font-semibold shadow-lg shadow-purple-500/25"
                >
                  Inject Event
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GraphViewer;
