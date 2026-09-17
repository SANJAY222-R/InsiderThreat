import os
import networkx as nx
from .base_builder import BaseGraphModule
import logging
import json
import matplotlib.pyplot as plt

logger = logging.getLogger("GraphBuilder")

class GraphExporter(BaseGraphModule):
    """Module 10: Graph Storage Export"""
    def run(self, G: nx.MultiDiGraph) -> None:
        # 1. GraphML
        graphml_path = os.path.join(self.cfg.paths.exporters_dir, "graph.graphml")
        # To avoid graphml write errors with dicts/nulls, we sanitize attributes
        H = nx.MultiDiGraph()
        for u, d in G.nodes(data=True):
            H.add_node(u, **{k: str(v) for k, v in d.items()})
        for u, v, k, d in G.edges(keys=True, data=True):
            H.add_edge(u, v, key=k, **{k_: str(v_) for k_, v_ in d.items()})

        nx.write_graphml(H, graphml_path)
        logger.info("Exported GraphML.")

        # 2. Cypher Scripts
        cypher_path = os.path.join(self.cfg.paths.exporters_dir, "neo4j_import.cypher")
        with open(cypher_path, "w") as f:
            f.write("// Neo4j Cypher Import Scripts\n")
            f.write("LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row\n")
            f.write("CALL apoc.create.node([row.node_type], row) YIELD node RETURN count(*);\n")
        logger.info("Exported Cypher Scripts.")

        # 3. PyTorch Geometric Data format serialization stub (since pytorch may not be installed on windows 3.14)
        pt_path = os.path.join(self.cfg.paths.exporters_dir, "pyg_heterodata.json")
        with open(pt_path, "w") as f:
            json.dump({"info": "HeteroData serialized here."}, f)
        logger.info("Exported PyG Stub.")

class GraphVisualizer(BaseGraphModule):
    """Module 11: Graph Visualization"""
    def run(self, G: nx.MultiDiGraph) -> None:
        # We extract a small ego graph to avoid blowing up memory with 3M edges
        if G.number_of_nodes() > 0:
            nodes_iter = iter(G.nodes())
            center = next(nodes_iter)
            ego = nx.ego_graph(G, center, radius=2)

            plt.figure(figsize=(10, 10))
            nx.draw(ego, with_labels=False, node_size=20)
            img_path = os.path.join(self.cfg.paths.visualizations_dir, "ego_graph.png")
            plt.savefig(img_path)
            plt.close()
        logger.info("Graph Visualizations Generated.")

class ReportGenerator(BaseGraphModule):
    """Module 12: Report Generation"""
    def run(self, G: nx.MultiDiGraph) -> None:
        report_path = os.path.join(self.cfg.paths.reports_dir, "graph_summary.md")
        with open(report_path, "w") as f:
            f.write("# Enterprise Temporal Heterogeneous Graph Summary\\n\\n")
            f.write(f"- **Total Nodes:** {G.number_of_nodes()}\\n")
            f.write(f"- **Total Edges:** {G.number_of_edges()}\\n")
        logger.info("Graph Summary Report Generated.")
