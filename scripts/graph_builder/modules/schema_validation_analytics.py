import json
import os
import networkx as nx
from .base_builder import BaseGraphModule
import logging

logger = logging.getLogger("GraphBuilder")

class SchemaGenerator(BaseGraphModule):
    """Module 7: Schema Generation"""
    def run(self, G: nx.MultiDiGraph) -> None:
        node_types = set(nx.get_node_attributes(G, 'node_type').values())
        edge_types = set(nx.get_edge_attributes(G, 'edge_type').values())

        schema = {
            "node_types": list(node_types),
            "edge_types": list(edge_types)
        }
        with open(os.path.join(self.cfg.paths.schemas_dir, "graph_schema.json"), "w") as f:
            json.dump(schema, f, indent=2)
        logger.info("Graph Schema Generated.")

class GraphValidator(BaseGraphModule):
    """Module 8: Graph Validation"""
    def run(self, G: nx.MultiDiGraph) -> None:
        isolates = list(nx.isolates(G))
        logger.info(f"Graph Validation: Found {len(isolates)} isolated nodes.")

class GraphAnalytics(BaseGraphModule):
    """Module 9: Graph Analytics"""
    def run(self, G: nx.MultiDiGraph) -> None:
        # Full analytics on MultiDiGraph is slow. We do a quick summary.
        logger.info(f"Graph Density: {nx.density(G):.6f}")
