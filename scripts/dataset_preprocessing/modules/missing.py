import polars as pl
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class MissingValueHandler(BaseModule):
    """Module 4: Missing Value Handling"""
    
    def __init__(self):
        super().__init__("MissingValueHandler")
        
    def run(self, df: pl.DataFrame, context: dict) -> pl.DataFrame:
        missing_stats = {}
        for col in df.columns:
            null_count = df.select(pl.col(col).is_null().sum()).item()
            if null_count > 0:
                missing_stats[col] = null_count
                
                # Handling rules
                dtype = df.schema[col]
                if dtype in [pl.Utf8, pl.Categorical]:
                    df = df.with_columns(pl.col(col).fill_null("Unknown"))
                elif dtype in [pl.Int64, pl.Int32, pl.Float64, pl.Float32]:
                    df = df.with_columns(pl.col(col).fill_null(0))
                
        context["missing_values_handled"] = missing_stats
        if missing_stats:
            logger.info(f"Handled missing values in columns: {list(missing_stats.keys())}")
            
        return df
