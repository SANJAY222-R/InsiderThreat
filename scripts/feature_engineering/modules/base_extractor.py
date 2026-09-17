from abc import ABC, abstractmethod
from typing import Optional
import polars as pl
from omegaconf import DictConfig

class BaseExtractor(ABC):
    """
    Abstract Base Class for all feature extractors.
    """
    def __init__(self, name: str, cfg: DictConfig) -> None:
        self.name = name
        self.cfg = cfg
        self.processed_dir = cfg.paths.processed_dir

    @abstractmethod
    def run(self) -> Optional[pl.DataFrame]:
        """
        Executes the module's feature generation logic.
        """
        pass

    def load_clean_data(self, dataset_name: str) -> Optional[pl.DataFrame]:
        """Helper to load cleaned CSVs if they exist."""
        import os
        path = os.path.join(self.processed_dir, f"clean_{dataset_name}.csv")
        if os.path.exists(path):
            return pl.read_csv(path, ignore_errors=True)
        return None
