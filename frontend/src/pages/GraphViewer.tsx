import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';

const GraphViewer: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Dummy elements representing Temporal Heterogeneous Graph
    const elements = [
      { data: { id: 'U1234', label: 'User: U1234', type: 'user' } },
      { data: { id: 'H4001', label: 'Host: PC-4001', type: 'host' } },
      { data: { id: 'F999', label: 'File: Secret.pdf', type: 'file' } },
      { data: { id: 'USB01', label: 'USB: Device_1', type: 'device' } },
      
      { data: { source: 'U1234', target: 'H4001', label: 'LOGIN_TO (03:00)' } },
      { data: { source: 'H4001', target: 'F999', label: 'ACCESS_FILE' } },
      { data: { source: 'H4001', target: 'USB01', label: 'INSERT_USB' } },
    ];

    const cy = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#3B82F6',
            'label': 'data(label)',
            'color': '#fff',
            'text-valign': 'bottom',
            'text-margin-y': 5,
            'font-size': '12px',
          }
        },
        {
          selector: 'node[type="user"]',
          style: { 'background-color': '#EF4444' } // High risk user
        },
        {
          selector: 'node[type="file"]',
          style: { 'background-color': '#10B981' }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#4B5563',
            'target-arrow-color': '#4B5563',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': '10px',
            'color': '#9CA3AF',
            'text-rotation': 'autorotate'
          }
        }
      ],
      layout: {
        name: 'cose',
        padding: 50
      }
    });

    return () => {
      cy.destroy();
    };
  }, []);

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-white">Enterprise Graph Viewer</h1>
        <div className="space-x-2">
          <button className="bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded text-sm">Filter</button>
          <button className="bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded text-sm">Export Subgraph</button>
        </div>
      </div>
      
      {/* Cytoscape Container */}
      <div className="flex-1 bg-gray-800 rounded-lg border border-gray-700 relative overflow-hidden">
        <div ref={containerRef} className="absolute inset-0" />
      </div>
    </div>
  );
};

export default GraphViewer;
