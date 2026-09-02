import polars as pl
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class DataValidation(BaseModule):
    """Module 2: Data Validation"""
    
    def __init__(self):
        super().__init__("DataValidation")
        
    def run(self, df: pl.DataFrame, context: dict) -> pl.DataFrame:
        filename = context.get("filename", "")
        logger.info(f"Validating schema for {filename}")
        
        cols = df.columns
        # Generic mandatory columns based on CERT datasets
        expected_generic = []
        if "logon" in filename.lower():
            expected_generic = ["id", "date", "user", "pc", "activity"]
        elif "device" in filename.lower():
            expected_generic = ["id", "date", "user", "pc", "activity"]
        elif "file" in filename.lower():
            expected_generic = ["id", "date", "user", "pc", "filename", "activity"]
        elif "email" in filename.lower():
            expected_generic = ["id", "date", "user", "pc", "to", "from"]
        elif "http" in filename.lower():
            expected_generic = ["id", "date", "user", "pc", "url"]
            
        missing = [c for c in expected_generic if c not in cols]
        if missing:
            logger.warning(f"Missing expected columns in {filename}: {missing}")
            context["validation_warnings"] = f"Missing: {missing}"
        else:
            context["validation_warnings"] = "None"
            
        return df
