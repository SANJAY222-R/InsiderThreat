import polars as pl
from typing import Any
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class DuplicateRemoval(BaseModule):
    """Module 3: Duplicate Removal"""
    
    def __init__(self) -> None:
        super().__init__("DuplicateRemoval")
        
    def run(self, df: pl.DataFrame, context: dict[str, Any]) -> pl.DataFrame:
        initial_count = df.height
        df = df.unique()
        final_count = df.height
        duplicates_removed = initial_count - final_count
        
        context["duplicates_removed"] = duplicates_removed
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate rows.")
            
        return df
