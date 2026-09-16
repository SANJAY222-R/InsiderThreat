import polars as pl
from typing import Any
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class TextNormalizer(BaseModule):
    """Module 6: Text Normalization"""
    
    def __init__(self) -> None:
        super().__init__("TextNormalizer")
        
    def run(self, df: pl.DataFrame, context: dict[str, Any]) -> pl.DataFrame:
        str_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype == pl.Utf8]
        
        if str_cols:
            logger.info(f"Normalizing text columns: {str_cols}")
            exprs = []
            for col in str_cols:
                # Lowercase and strip whitespace
                exprs.append(pl.col(col).str.strip_chars().str.to_lowercase())
                
            df = df.with_columns(exprs)
            
        context["text_normalized"] = len(str_cols)
        return df
