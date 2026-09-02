import networkx as nx
import polars as pl
from .base_builder import BaseGraphModule
import logging

logger = logging.getLogger("GraphBuilder")

class EdgeCreator(BaseGraphModule):
    """Module 2: Edge Creation"""
    
    def _create_mapping(self, entity_name: str, key_col: str) -> dict:
        df = self.load_entity(entity_name)
        if df is None or df.is_empty():
            return {}
        # standard_id or raw_id -> enterprise_id
        return dict(zip(df[key_col].to_list(), df["enterprise_id"].to_list()))
        
    def run(self, G: nx.MultiDiGraph) -> nx.MultiDiGraph:
        # Load mappings
        user_map = self._create_mapping("users", "raw_id")
        host_map = self._create_mapping("hosts", "raw_id")
        file_map = self._create_mapping("files", "raw_id")
        usb_map = self._create_mapping("usbs", "raw_id")
        email_map = self._create_mapping("emails", "raw_id")
        url_map = self._create_mapping("urls", "raw_id")
        
        # 1. LOGON Edges
        logon_df = self.load_processed("logon")
        if logon_df is not None:
            for row in logon_df.iter_rows(named=True):
                u_id = user_map.get(row.get("user"))
                h_id = host_map.get(row.get("pc"))
                if u_id and h_id:
                    rel = "LOGIN_TO" if row.get("activity") == "Logon" else "LOGOUT_FROM"
                    G.add_edge(u_id, h_id, edge_type=rel, timestamp=row.get("date"), weight=1.0)
                    
        # 2. FILE Edges
        file_df = self.load_processed("file")
        if file_df is not None:
            for row in file_df.iter_rows(named=True):
                u_id = user_map.get(row.get("user"))
                f_id = file_map.get(row.get("filename"))
                if u_id and f_id:
                    G.add_edge(u_id, f_id, edge_type="ACCESS_FILE", activity=row.get("activity"), timestamp=row.get("date"), weight=1.0)
                    
        # 3. USB Edges
        dev_df = self.load_processed("device")
        if dev_df is not None:
            for row in dev_df.iter_rows(named=True):
                h_id = host_map.get(row.get("pc"))
                usb_raw = row.get("id") or row.get("pc") # fallback
                usb_id = usb_map.get(usb_raw)
                if h_id and usb_id:
                    rel = "INSERT_USB" if row.get("activity") == "Connect" else "REMOVE_USB"
                    G.add_edge(h_id, usb_id, edge_type=rel, timestamp=row.get("date"), weight=1.0)
                    
        # 4. EMAIL Edges
        email_df = self.load_processed("email")
        if email_df is not None:
            for row in email_df.iter_rows(named=True):
                u_id = user_map.get(row.get("user"))
                to_email = email_map.get(row.get("to"))
                if u_id and to_email:
                    G.add_edge(u_id, to_email, edge_type="SEND_EMAIL", timestamp=row.get("date"), weight=1.0)
                    
        # 5. HTTP Edges
        http_df = self.load_processed("http")
        if http_df is not None:
            for row in http_df.iter_rows(named=True):
                u_id = user_map.get(row.get("user"))
                url_id = url_map.get(row.get("url"))
                if u_id and url_id:
                    G.add_edge(u_id, url_id, edge_type="VISIT_WEBSITE", timestamp=row.get("date"), weight=1.0)
                    
        logger.info(f"Edge Creation Complete. Total Edges: {G.number_of_edges()}")
        return G
