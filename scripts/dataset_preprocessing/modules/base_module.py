from abc import ABC, abstractmethod
import polars as pl

class BaseModule(ABC):
    """
    Abstract Base Class for all preprocessing modules.
    Follows SOLID Open-Closed Principle.
    """
    
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, df: pl.DataFrame, context: dict) -> pl.DataFrame:
        """
        Executes the module's primary logic.
        
        Args:
            df: Polars DataFrame
            context: Dictionary containing metadata like filename, dataset name.
            
        Returns:
            Processed Polars DataFrame
        """
        pass
