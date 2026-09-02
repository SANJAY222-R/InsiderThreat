import os
import json
import pandas as pd
from typing import Dict, Any

class XAIExporter:
    """
    Exports explanation JSON, CSV, attention maps, and subgraph data.
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def export_data(self, data: Any, filename: str, format: str = 'json'):
        filepath = os.path.join(self.output_dir, f"{filename}.{format}")
        
        if format == 'json':
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
        elif format == 'csv':
            if isinstance(data, list):
                df = pd.DataFrame(data)
                df.to_csv(filepath, index=False)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
                df.to_csv(filepath, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
