import polars as pl
from .base_extractor import BaseExtractor
import logging

logger = logging.getLogger("FeatureEngineering")

class WebActivityExtractor(BaseExtractor):
    """Module 5: Web Activity Features (from http.csv)"""
    
    def __init__(self, cfg):
        super().__init__("web_features", cfg)
        
    def run(self) -> pl.DataFrame | None:
        df = self.load_clean_data("http")
        if df is None:
            logger.warning("clean_http.csv not found.")
            return None
            
        logger.info("Extracting Web Activity features...")
        
        features = df.group_by("user").agg([
            pl.len().alias("Total_Website_Visits"),
            
            # If URL column exists, extract domain or count uniques
            # CERT r4.2 url usually looks like http://domain.com/...
            pl.col("url").n_unique().alias("Unique_URLs_Visited"),
            
            # Off-hours web usage
            pl.col("Hour").filter((pl.col("Hour") < 6) | (pl.col("Hour") >= 20)).count().alias("After_Hours_Web_Usage")
        ])
        
        return features
