import polars as pl
from typing import Any
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class SessionPreparator(BaseModule):
    """Module 8: Session Preparation"""
    
    def __init__(self) -> None:
        super().__init__("SessionPreparator")
        
    def run(self, df: pl.DataFrame, context: dict[str, Any]) -> pl.DataFrame:
        cols = df.columns
        
        # We need user and some timestamp (UnixTimestamp generated in Module 5)
        if "user" in cols and "UnixTimestamp" in cols:
            logger.info("Preparing data for future session generation (sorting and indexing).")
            # Sort chronologically by user
            df = df.sort(["user", "UnixTimestamp"])
            
            # Add Sequential Event ID
            df = df.with_row_index(name="EventID")
            context["session_prepared"] = True
        else:
            logger.warning("Missing 'user' or 'UnixTimestamp', skipping session prep.")
            context["session_prepared"] = False
            
        return df
