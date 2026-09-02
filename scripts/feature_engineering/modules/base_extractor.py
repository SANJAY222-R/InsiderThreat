from abc import ABC, abstractmethod
import polars as pl
from omegaconf import DictConfig

class BaseExtractor(ABC):
    """
    Abstract Base Class for all feature extractors.
    """
    def __init__(self, name: str, cfg: DictConfig):
        self.name = name
        self.cfg = cfg
        self.processed_dir = cfg.paths.processed_dir

    @abstractmethod
    def run(self) -> pl.DataFrame | None:
        """
        Executes the module's feature generation logic.
        """
        pass
        
    def load_clean_data(self, dataset_name: str) -> pl.DataFrame | None:
        """Helper to load cleaned CSVs if they exist."""
        import os
        path = os.path.join(self.processed_dir, f"clean_{dataset_name}.csv")
        if os.path.exists(path):
            return pl.read_csv(path, ignore_errors=True)
        return None
