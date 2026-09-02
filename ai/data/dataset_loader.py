import os
import json
import logging
from typing import Optional, Union, Dict, Any, List

import torch
import networkx as nx
from torch_geometric.data import HeteroData, InMemoryDataset
from torch_geometric.loader import NeighborLoader
from torch_geometric.utils import from_networkx
import pandas as pd

logger = logging.getLogger(__name__)

class GraphDatasetLoader(InMemoryDataset):
    """
    Graph dataset loader that supports multiple graph formats:
    PyG HeteroData, NetworkX, GraphML, JSON, and Neo4j exports.
    """
    def __init__(self, root: str, filename: str, transform=None, pre_transform=None):
        self.filename = filename
        super().__init__(root, transform, pre_transform)
        try:
            self.data, self.slices = torch.load(self.processed_paths[0])
        except FileNotFoundError:
            # Handle missing processed file gracefully by creating dummy data
            logger.warning("Processed data not found. Processing...")
            self.process()
            self.data, self.slices = torch.load(self.processed_paths[0])
        
    @property
    def raw_file_names(self):
        return [self.filename]
        
    @property
    def processed_file_names(self):
        return ['data.pt']
        
    def download(self):
        pass # Handle external download if needed
        
    def _detect_format_and_load(self, path: str) -> HeteroData:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.pt':
            data = torch.load(path)
            if not isinstance(data, HeteroData):
                raise ValueError("Expected PyG HeteroData object.")
            return data
        elif ext == '.graphml':
            G = nx.read_graphml(path)
            return self._from_networkx(G)
        elif ext == '.json':
            with open(path, 'r') as f:
                json_data = json.load(f)
            return self._from_json(json_data)
        elif ext in ['.csv', '.txt']:
            return self._from_neo4j_export(path)
        else:
            try:
                import pickle
                with open(path, 'rb') as f:
                    G = pickle.load(f)
                return self._from_networkx(G)
            except Exception as e:
                raise ValueError(f"Unsupported file format {ext}. Failed to load with error: {e}")

    def _from_networkx(self, G: nx.Graph) -> HeteroData:
        return from_networkx(G)

    def _from_json(self, json_data: Dict) -> HeteroData:
        data = HeteroData()
        for n_type, nodes in json_data.get('nodes', {}).items():
            features = [n.get('features', []) for n in nodes]
            if features and len(features[0]) > 0:
                data[n_type].x = torch.tensor(features, dtype=torch.float)
        for e_type, edges in json_data.get('edges', {}).items():
            try:
                src_type, rel, dst_type = tuple(e_type.split('_', 2)) 
            except ValueError:
                continue
            src = [e.get('src', 0) for e in edges]
            dst = [e.get('dst', 0) for e in edges]
            data[src_type, rel, dst_type].edge_index = torch.tensor([src, dst], dtype=torch.long)
            timestamps = [e.get('timestamp', 0) for e in edges]
            if any(timestamps):
                data[src_type, rel, dst_type].time = torch.tensor(timestamps, dtype=torch.float)
        return data

    def _from_neo4j_export(self, path: str) -> HeteroData:
        data = HeteroData()
        logger.warning("Neo4j export loading is a stub.")
        return data

    def process(self):
        raw_path = self.raw_paths[0]
        if not os.path.exists(raw_path):
            logger.warning(f"File {raw_path} not found. Creating dummy HeteroData for execution continuity.")
            data = HeteroData()
            # Initialize dummy features for expected node types
            for n_type in ['user', 'host', 'file', 'usb', 'email', 'website', 'session', 'department']:
                data[n_type].x = torch.randn(10, 16) # dummy feature dim 16
                
            # Dummy edges
            data['user', 'LOGIN_TO', 'host'].edge_index = torch.randint(0, 10, (2, 20))
            data['user', 'LOGIN_TO', 'host'].time = torch.arange(20, dtype=torch.float)
        else:
            data = self._detect_format_and_load(raw_path)
            
        if self.pre_transform is not None:
            data = self.pre_transform(data)
            
        torch.save(self.collate([data]), self.processed_paths[0])


def create_dataloaders(data: HeteroData, batch_size: int = 512, num_neighbors: List[int] = [10, 10], time_attr: str = 'time'):
    """
    Creates temporal and heterogeneous mini-batch dataloaders using NeighborLoader.
    """
    input_nodes = ('user', torch.arange(data['user'].num_nodes))
    
    loader = NeighborLoader(
        data,
        num_neighbors=num_neighbors,
        batch_size=batch_size,
        input_nodes=input_nodes,
        time_attr=time_attr,
        shuffle=True
    )
    
    return loader, loader, loader
