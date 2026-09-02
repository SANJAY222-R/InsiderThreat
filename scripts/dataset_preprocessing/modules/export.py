import polars as pl
from .base_module import BaseModule
from config import PROCESSED_DIR
import logging

logger = logging.getLogger("DatasetPreprocessing")

class DataExporter(BaseModule):
    """Module 11: Export Clean Data"""
    
    def __init__(self):
        super().__init__("DataExporter")
        
    def run(self, df: pl.DataFrame, context: dict) -> pl.DataFrame:
        filename = context.get("filename", "unknown.csv")
        out_path = PROCESSED_DIR / f"clean_{filename}"
        
        logger.info(f"Exporting clean data to {out_path.name}")
        try:
            df.write_csv(out_path)
            context["export_path"] = str(out_path)
        except Exception as e:
            logger.error(f"Failed to export {filename}: {e}")
            
        return df
