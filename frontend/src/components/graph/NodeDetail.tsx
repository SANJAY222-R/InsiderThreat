/**
 * Node Detail Panel
 *
 * Side panel showing detailed information about a selected graph node.
 *
 * Phase 0: Stub component only.
 */

interface NodeDetailProps {
  nodeId?: string;
  nodeType?: string;
}

export function NodeDetail({ nodeId, nodeType }: NodeDetailProps) {
  return (
    <div id="node-detail" className="detail-panel">
      {/* TODO: Node properties display */}
      {/* TODO: Connected edges list */}
      {/* TODO: Temporal activity chart */}
      <p>Node: {nodeId} ({nodeType})</p>
    </div>
  );
}
