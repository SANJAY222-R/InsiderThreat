import os
import polars as pl

class BaseEntityModule:
    """Base class for Entity Extraction modules."""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.processed_dir = cfg.paths.processed_dir
        self.features_dir = cfg.paths.features_dir

    def load_processed(self, name: str) -> pl.DataFrame | None:
        path = os.path.join(self.processed_dir, f"clean_{name}.csv")
        if os.path.exists(path):
            return pl.read_csv(path, ignore_errors=True)
        return None
        
    def load_features(self, name: str) -> pl.DataFrame | None:
        path = os.path.join(self.features_dir, f"{name}_features.csv")
        if os.path.exists(path):
            return pl.read_csv(path, ignore_errors=True)
        return None
