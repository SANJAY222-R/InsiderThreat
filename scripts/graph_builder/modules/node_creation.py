import networkx as nx
from .base_builder import BaseGraphModule
import logging

logger = logging.getLogger("GraphBuilder")

class NodeCreator(BaseGraphModule):
    """Module 1: Node Creation"""
    def run(self, G: nx.MultiDiGraph) -> nx.MultiDiGraph:
        entities_list = ["users", "hosts", "files", "usbs", "emails", "domains", "websites"]
        
        for entity_name in entities_list:
            df = self.load_entity(entity_name)
            if df is not None and not df.is_empty():
                for row in df.iter_rows(named=True):
                    ent_id = row.get("enterprise_id")
                    if ent_id:
                        # Convert dict values to primitive python types (some polars nulls can be tricky)
                        attrs = {k: v for k, v in row.items() if v is not None}
                        attrs["node_type"] = entity_name.capitalize()
                        G.add_node(ent_id, **attrs)
                        
        logger.info(f"Node Creation Complete. Total Nodes: {G.number_of_nodes()}")
        return G
