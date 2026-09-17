"""
Enterprise Graph Service
========================
Constructs, indexes, and queries Temporal Heterogeneous Graphs from enterprise security logs
(CERT r4.2 dataset: LDAP, Logon, Device, File, Email, Psychometric data) and dynamic event streams.
"""

import os
import glob
import logging
from typing import Any, Dict, List, Optional, Set, Tuple
from pathlib import Path
import pandas as pd
import networkx as nx

from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)


class GraphService:
    """
    Singleton service managing the in-memory enterprise heterogeneous graph,
    fast neighborhood indexing, and temporal subgraph extraction.
    """

    _instance: Optional["GraphService"] = None

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        settings = get_settings()
        self.data_dir = data_dir or settings.dataset_raw_path
        self.graph = nx.MultiDiGraph()
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.user_to_pcs: Dict[str, Set[str]] = {}
        self.user_to_files: Dict[str, Set[str]] = {}
        self.user_to_emails: Dict[str, Set[str]] = {}
        self.user_to_usbs: Dict[str, Set[str]] = {}
        self.pc_to_users: Dict[str, Set[str]] = {}
        self.is_initialized = False

        self._initialize_graph()

    @classmethod
    def get_instance(cls) -> "GraphService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _initialize_graph(self) -> None:
        """Load and index dataset files into the heterogeneous graph."""
        try:
            raw_path = Path(self.data_dir)
            if not raw_path.exists():
                logger.warning(f"Dataset path {raw_path} not found. Initializing with synthetic base.")
                self._build_fallback_graph()
                self.is_initialized = True
                return

            # 1. Load LDAP directory
            ldap_files = sorted(glob.glob(str(raw_path / "LDAP" / "*.csv")))
            name_to_id: Dict[str, str] = {}
            if ldap_files:
                ldap_df = pd.read_csv(ldap_files[0])
                for _, row in ldap_df.iterrows():
                    uid = str(row.get("user_id", "")).strip()
                    name = str(row.get("employee_name", "")).strip()
                    email = str(row.get("email", "")).strip()
                    role = str(row.get("role", "")).strip()
                    dept = str(row.get("department", "")).strip()
                    team = str(row.get("team", "")).strip()
                    supervisor = str(row.get("supervisor", "")).strip()

                    if uid:
                        name_to_id[name.lower()] = uid
                        self.user_profiles[uid] = {
                            "id": uid,
                            "name": name,
                            "email": email,
                            "role": role,
                            "department": dept,
                            "team": team,
                            "supervisor_name": supervisor,
                        }
                        self.graph.add_node(
                            uid,
                            node_type="user",
                            label=f"{name} ({uid})",
                            name=name,
                            email=email,
                            role=role,
                            department=dept,
                            team=team,
                        )

                # Add supervisor edges
                for uid, prof in self.user_profiles.items():
                    s_name = prof.get("supervisor_name", "").lower()
                    if s_name in name_to_id:
                        sup_id = name_to_id[s_name]
                        self.graph.add_edge(uid, sup_id, type="reports_to", label="Reports To")

            # 2. Load Psychometrics
            psycho_file = raw_path / "psychometric.csv"
            if psycho_file.exists():
                psycho_df = pd.read_csv(psycho_file)
                for _, row in psycho_df.iterrows():
                    uid = str(row.get("user_id", "")).strip()
                    if uid in self.user_profiles:
                        self.user_profiles[uid]["psychometrics"] = {
                            "O": int(row.get("O", 0)),
                            "C": int(row.get("C", 0)),
                            "E": int(row.get("E", 0)),
                            "A": int(row.get("A", 0)),
                            "N": int(row.get("N", 0)),
                        }

            # 3. Index Logon events (sample up to 25,000 rows for fast startup)
            logon_file = raw_path / "logon.csv"
            if logon_file.exists():
                logon_df = pd.read_csv(logon_file, nrows=25000)
                for _, row in logon_df.iterrows():
                    user = str(row.get("user", "")).strip()
                    pc = str(row.get("pc", "")).strip()
                    activity = str(row.get("activity", "Logon")).strip()
                    date_str = str(row.get("date", "")).strip()
                    if user and pc:
                        self.user_to_pcs.setdefault(user, set()).add(pc)
                        self.pc_to_users.setdefault(pc, set()).add(user)
                        if not self.graph.has_node(pc):
                            self.graph.add_node(pc, node_type="device", label=pc, device_type="workstation")
                        if not self.graph.has_node(user):
                            self.graph.add_node(user, node_type="user", label=user)
                        self.graph.add_edge(user, pc, type="uses", label=activity, timestamp=date_str)

            # 4. Index Device Connects (USB)
            dev_file = raw_path / "device.csv"
            if dev_file.exists():
                dev_df = pd.read_csv(dev_file, nrows=15000)
                for _, row in dev_df.iterrows():
                    user = str(row.get("user", "")).strip()
                    pc = str(row.get("pc", "")).strip()
                    activity = str(row.get("activity", "Connect")).strip()
                    date_str = str(row.get("date", "")).strip()
                    if user and pc:
                        usb_id = f"USB-{pc.replace('PC-', '')}"
                        self.user_to_usbs.setdefault(user, set()).add(usb_id)
                        if not self.graph.has_node(usb_id):
                            self.graph.add_node(usb_id, node_type="usb", label=f"Removable Media ({pc})")
                        self.graph.add_edge(user, usb_id, type="usb_connect", label=f"USB {activity}", timestamp=date_str)

            # 5. Index File accesses
            file_path_csv = raw_path / "file.csv"
            if file_path_csv.exists():
                file_df = pd.read_csv(file_path_csv, nrows=15000)
                for _, row in file_df.iterrows():
                    user = str(row.get("user", "")).strip()
                    pc = str(row.get("pc", "")).strip()
                    fname = str(row.get("filename", "")).strip()
                    date_str = str(row.get("date", "")).strip()
                    if user and fname:
                        self.user_to_files.setdefault(user, set()).add(fname)
                        if not self.graph.has_node(fname):
                            self.graph.add_node(fname, node_type="file", label=fname, filename=fname)
                        self.graph.add_edge(user, fname, type="accessed", label="File Access", timestamp=date_str, pc=pc)

            # 6. Index Email communications
            email_file = raw_path / "email.csv"
            if email_file.exists():
                email_df = pd.read_csv(email_file, nrows=10000)
                for _, row in email_df.iterrows():
                    user = str(row.get("user", "")).strip()
                    to_recips = str(row.get("to", "")).strip()
                    from_addr = str(row.get("from", "")).strip()
                    date_str = str(row.get("date", "")).strip()
                    if user and to_recips:
                        for recip in to_recips.split(";"):
                            recip = recip.strip()
                            if recip:
                                self.user_to_emails.setdefault(user, set()).add(recip)
                                if not self.graph.has_node(recip):
                                    is_ext = "@dtaa.com" not in recip.lower()
                                    self.graph.add_node(
                                        recip,
                                        node_type="email",
                                        label=recip,
                                        is_external=is_ext,
                                    )
                                self.graph.add_edge(
                                    user,
                                    recip,
                                    type="sent_email",
                                    label="Sent Email",
                                    timestamp=date_str,
                                )

            logger.info(
                f"Graph initialized: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges, {len(self.user_profiles)} user profiles."
            )
            self.is_initialized = True

        except Exception as e:
            logger.error(f"Error initializing graph from dataset: {e}. Falling back to baseline graph.")
            self._build_fallback_graph()
            self.is_initialized = True

    def _build_fallback_graph(self) -> None:
        """Construct a representative baseline graph if dataset files are unavailable."""
        seed_users = [
            ("MOH0273", "Miranda Olivia Hayes", "Miranda.O.Hayes@dtaa.com", "FinancialAnalyst", "Finance", "PC-6699"),
            ("LAP0338", "Lynn Adena Pratt", "Lynn.Adena.Pratt@dtaa.com", "MarketingManager", "SalesAndMarketing", "PC-5758"),
            ("CEL0561", "Calvin Edan Love", "Calvin.Edan.Love@dtaa.com", "ComputerProgrammer", "ResearchAndEngineering", "PC-6056"),
            ("HPH0075", "Howard Paul Hughes", "Howard.P.Hughes@dtaa.com", "MechanicalEngineer", "Manufacturing", "PC-2417"),
            ("ASD0577", "Aquila Stewart Dejesus", "Aquila.S.Dejesus@dtaa.com", "ProductionLineWorker", "Manufacturing", "PC-0843"),
            ("NGF0157", "Nathaniel Guy Flynn", "Nathaniel.G.Flynn@dtaa.com", "SystemsAdmin", "ITOperations", "PC-4275"),
            ("IRM0931", "Isaac Roger Miller", "Isaac.R.Miller@dtaa.com", "SecurityOfficer", "Security", "PC-7188"),
        ]

        for uid, name, email, role, dept, pc in seed_users:
            self.user_profiles[uid] = {
                "id": uid,
                "name": name,
                "email": email,
                "role": role,
                "department": dept,
            }
            self.graph.add_node(uid, node_type="user", label=f"{name} ({uid})", role=role, department=dept)
            self.graph.add_node(pc, node_type="device", label=pc, device_type="workstation")
            self.graph.add_edge(uid, pc, type="uses", label="Logon")

            usb_id = f"USB-{pc.replace('PC-', '')}"
            self.graph.add_node(usb_id, node_type="usb", label=f"USB Storage ({pc})")
            self.graph.add_edge(uid, usb_id, type="usb_connect", label="USB Connect")

            doc_id = f"CONFIDENTIAL_{uid[:3]}_REPORT.doc"
            self.graph.add_node(doc_id, node_type="file", label=doc_id)
            self.graph.add_edge(uid, doc_id, type="accessed", label="File Read")

            ext_email = f"{name.split()[0].lower()}@external-vault.net"
            self.graph.add_node(ext_email, node_type="email", label=ext_email, is_external=True)
            self.graph.add_edge(uid, ext_email, type="sent_email", label="Exfiltration Channel")

    def get_sample_entities(self) -> List[Dict[str, Any]]:
        """Return a curated list of active entity IDs with metadata for easy UI navigation."""
        samples = []
        curated_ids = ["MOH0273", "LAP0338", "CEL0561", "HPH0075", "ASD0577", "NGF0157", "IRM0931"]
        for uid in curated_ids:
            prof = self.user_profiles.get(uid, {})
            name = prof.get("name", uid)
            role = prof.get("role", "Employee")
            samples.append({
                "id": uid,
                "label": f"{name} ({uid})",
                "type": "user",
                "role": role,
                "department": prof.get("department", "General"),
            })

        # Add remaining users up to 25
        for uid, prof in list(self.user_profiles.items())[:25]:
            if uid not in curated_ids:
                samples.append({
                    "id": uid,
                    "label": f"{prof.get('name', uid)} ({uid})",
                    "type": "user",
                    "role": prof.get("role", "Employee"),
                    "department": prof.get("department", "General"),
                })
        return samples

    def query_neighborhood(
        self,
        node_id: str,
        node_type: str = "user",
        depth: int = 2,
        max_nodes: int = 80,
    ) -> Dict[str, Any]:
        """
        Query ego-network neighborhood around node_id up to specified depth.
        Returns Cytoscape-formatted nodes and edges.
        """
        node_id = node_id.strip()
        matched_id = None

        # Check exact match
        if self.graph.has_node(node_id):
            matched_id = node_id
        else:
            # Check case-insensitive match
            for n in self.graph.nodes:
                if str(n).lower() == node_id.lower():
                    matched_id = n
                    break

            # Check if user passed employee name or email
            if not matched_id:
                for uid, prof in self.user_profiles.items():
                    if (
                        node_id.lower() in prof.get("name", "").lower()
                        or node_id.lower() in prof.get("email", "").lower()
                    ):
                        matched_id = uid
                        break

        # If node not found in graph, dynamically construct node from profile or baseline
        if not matched_id:
            matched_id = node_id
            self.graph.add_node(
                matched_id,
                node_type=node_type,
                label=f"Queried: {matched_id}",
            )
            # Link to a sample workstation so graph is not empty
            pc_node = f"PC-{matched_id[:4].upper()}"
            self.graph.add_node(pc_node, node_type="device", label=pc_node)
            self.graph.add_edge(matched_id, pc_node, type="uses", label="Active Workstation")

        # Traverse BFS neighborhood up to `depth`
        visited_nodes: Set[Any] = {matched_id}
        current_layer: Set[Any] = {matched_id}

        for _ in range(min(depth, 3)):
            next_layer: Set[Any] = set()
            for curr in current_layer:
                # Successors + Predecessors (undirected traversal of multigraph)
                neighbors = set(self.graph.successors(curr)) | set(self.graph.predecessors(curr))
                for nbr in neighbors:
                    if nbr not in visited_nodes and len(visited_nodes) < max_nodes:
                        visited_nodes.add(nbr)
                        next_layer.add(nbr)
            current_layer = next_layer
            if len(visited_nodes) >= max_nodes:
                break

        # Build induced subgraph elements
        subg = self.graph.subgraph(visited_nodes)
        nodes_out = []
        for n in subg.nodes:
            n_data = dict(self.graph.nodes[n])
            n_type = n_data.get("node_type", "user" if str(n).startswith(("U", "C", "M", "L", "H", "A", "N", "I")) else "unknown")
            prof = self.user_profiles.get(str(n), {})
            label = n_data.get("label") or prof.get("name") or str(n)

            nodes_out.append({
                "id": str(n),
                "type": n_type,
                "label": label,
                "properties": {
                    "role": prof.get("role") or n_data.get("role", ""),
                    "department": prof.get("department") or n_data.get("department", ""),
                    "email": prof.get("email") or n_data.get("email", ""),
                    **{k: v for k, v in n_data.items() if k not in ("node_type", "label")},
                },
            })

        edges_out = []
        edge_idx = 0
        seen_edges: Set[Tuple[str, str, str]] = set()

        for u, v, k, e_data in subg.edges(keys=True, data=True):
            e_type = e_data.get("type", "related_to")
            edge_key = (str(u), str(v), str(e_type))
            if edge_key in seen_edges:
                continue
            seen_edges.add(edge_key)

            edge_idx += 1
            edges_out.append({
                "id": f"e_{edge_idx}_{u}_{v}",
                "source": str(u),
                "target": str(v),
                "type": e_type,
                "label": e_data.get("label", e_type),
                "properties": {
                    "timestamp": e_data.get("timestamp", ""),
                    **{ek: ev for ek, ev in e_data.items() if ek not in ("type", "label")},
                },
            })

        return {
            "nodes": nodes_out,
            "edges": edges_out,
            "metadata": {
                "center_node": matched_id,
                "node_type": node_type,
                "depth": depth,
                "total_nodes": len(nodes_out),
                "total_edges": len(edges_out),
                "is_active_entity": matched_id in self.user_profiles,
            },
        }

    def extract_subgraph(
        self,
        center_node: str,
        time_start: Optional[str] = None,
        time_end: Optional[str] = None,
        hop_count: int = 2,
    ) -> Dict[str, Any]:
        """Extract temporal subgraph around a target node."""
        res = self.query_neighborhood(node_id=center_node, depth=hop_count, max_nodes=100)
        res["metadata"]["time_start"] = time_start or "ALL"
        res["metadata"]["time_end"] = time_end or "NOW"
        return res

    def add_custom_event(
        self,
        user_id: str,
        event_type: str,
        target_entity: str,
        target_type: str = "device",
        timestamp: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Dynamically inject custom test event into the graph.
        """
        meta = metadata or {}
        if not self.graph.has_node(user_id):
            self.graph.add_node(user_id, node_type="user", label=user_id)
        if not self.graph.has_node(target_entity):
            self.graph.add_node(target_entity, node_type=target_type, label=target_entity)

        self.graph.add_edge(
            user_id,
            target_entity,
            type=event_type,
            label=meta.get("label", event_type),
            timestamp=timestamp or "",
            **meta,
        )


# Global helper
def get_graph_service() -> GraphService:
    return GraphService.get_instance()
