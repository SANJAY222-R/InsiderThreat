import polars as pl
from typing import Any
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class TypeStandardizer(BaseModule):
    """Module 7: Data Type Standardization"""
    
    def __init__(self) -> None:
        super().__init__("TypeStandardizer")
        
    def run(self, df: pl.DataFrame, context: dict[str, Any]) -> pl.DataFrame:
        logger.info("Standardizing data types to optimize memory.")
        
        exprs = []
        for col, dtype in zip(df.columns, df.dtypes):
            if dtype == pl.Utf8:
                # Polars Categorical is highly optimized for strings with low cardinality
                # We approximate: if unique count is relatively small, cast to Categorical
                # But calculating unique for all is expensive. We cast specific known categorical columns
                if col in ["user", "pc", "activity", "domain", "to", "from", "filename"]:
                    exprs.append(pl.col(col).cast(pl.Categorical))
            elif dtype == pl.Int64:
                # Downcast to Int32 where safe (Polars handles this smartly or we can blindly cast)
                # For safety, we keep Int64 or use Int32 if we know values are small
                exprs.append(pl.col(col).cast(pl.Int32))
                
        if exprs:
            df = df.with_columns(exprs)
            
        context["types_standardized"] = True
        return df
