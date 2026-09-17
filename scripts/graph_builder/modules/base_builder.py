import os
from typing import Any, Optional
import polars as pl
import networkx as nx

class BaseGraphModule:
    def __init__(self, cfg: Any) -> None:
        self.cfg = cfg
        self.entities_dir = cfg.paths.entities_dir
        self.processed_dir = cfg.paths.processed_dir

    def load_entity(self, name: str) -> Optional[pl.DataFrame]:
        path = os.path.join(self.entities_dir, f"{name}.csv")
        if os.path.exists(path):
            return pl.read_csv(path, ignore_errors=True)
        return None

    def load_processed(self, name: str) -> Optional[pl.DataFrame]:
        path = os.path.join(self.processed_dir, f"clean_{name}.csv")
        if os.path.exists(path):
            return pl.read_csv(path, ignore_errors=True)
        return None
