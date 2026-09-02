import os
import torch
import numpy as np
import pandas as pd
from typing import Dict, Any

class EmbeddingExporter:
    """
    Exports Node, Graph, User, and Session embeddings 
    to NumPy, PyTorch, or CSV formats.
    """
    def __init__(self, output_dir: str = 'ai/embeddings'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def export(self, embeddings_dict: Dict[str, Any], prefix: str = 'emb', format: str = 'npy'):
        """
        embeddings_dict: Dict where keys are node types (or 'graph') and values are tensors/arrays.
        """
        for entity_type, emb in embeddings_dict.items():
            # Convert to numpy if tensor
            if isinstance(emb, torch.Tensor):
                emb = emb.cpu().detach().numpy()
                
            filename = f"{prefix}_{entity_type}.{format}"
            filepath = os.path.join(self.output_dir, filename)
            
            if format == 'npy':
                np.save(filepath, emb)
            elif format == 'pt':
                torch.save(torch.tensor(emb), filepath)
            elif format == 'csv':
                df = pd.DataFrame(emb)
                df.to_csv(filepath, index=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
