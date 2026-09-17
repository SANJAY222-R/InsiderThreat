from typing import Any, Optional
import polars as pl
from .base_extractor import BaseExtractor
import logging

logger = logging.getLogger("FeatureEngineering")

class FileActivityExtractor(BaseExtractor):
    """Module 2: File Access Features (from file.csv)"""

    def __init__(self, cfg: Any) -> None:
        super().__init__("file_features", cfg)

    def run(self) -> Optional[pl.DataFrame]:
        df = self.load_clean_data("file")
        if df is None:
            logger.warning("clean_file.csv not found.")
            return None
            
        logger.info("Extracting File Access features...")
        
        # In r4.2 file.csv often lacks 'activity' field or has it as null, 
        # but we can count extensions and general file accesses.
        # Sensitive extensions: doc, pdf, zip, exe (common in CERT heuristics)
        sensitive_exts = r"\.(doc|pdf|zip|exe|rar)$"
        
        features = df.group_by("user").agg([
            pl.len().alias("Total_Files_Accessed"),
            pl.col("filename").n_unique().alias("Unique_Files_Accessed"),
            
            # Sensitive file access count
            pl.col("filename").str.contains(sensitive_exts, strict=False).sum().alias("Sensitive_File_Access_Count"),
            
            # PC counts
            pl.col("pc").n_unique().alias("File_Host_Switching_Count")
        ])
        
        return features
