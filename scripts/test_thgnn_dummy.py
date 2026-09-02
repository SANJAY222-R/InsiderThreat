import torch
from torch_geometric.data import HeteroData
import yaml

from ai.models.thgnn import THGNN
from ai.data.dataset_loader import GraphDatasetLoader

def test_thgnn():
    with open("configs/model.yaml", "r") as f:
        config = yaml.safe_load(f)

    model_config = config['model']['architecture']
    node_types = config['model']['node_types']
    
    # edge_types in config are lists, convert to tuples
    edge_types = [tuple(e) for e in config['model']['edge_types']]

    model = THGNN(
        node_types=node_types,
        edge_types=edge_types,
        hidden_dim=model_config['hidden_dim'],
        num_layers=model_config['num_layers'],
        num_heads=model_config['num_heads'],
        dropout=model_config['dropout'],
        pooling_type=model_config['pooling_type'],
        time_encoding=model_config['time_encoding']
    )

    print("Model initialized successfully.")

    # Create dummy data using our loader logic
    loader = GraphDatasetLoader(root=".", filename="dummy.txt")
    
    # We should have a batch of data
    data = loader.data

    print(f"Graph Nodes: {data.num_nodes}")
    print(f"Graph Edges: {data.num_edges}")

    out = model(data)

    print(f"Prediction Output Keys: {list(out.keys())}")
    print("Test passed successfully.")

if __name__ == "__main__":
    test_thgnn()
