import polars as pl
from .base_extractor import BaseExtractor
import logging

logger = logging.getLogger("FeatureEngineering")

class TemporalExtractor(BaseExtractor):
    """Module 6: Temporal Features"""
    
    def __init__(self, cfg):
        super().__init__("temporal_features", cfg)
        
    def run(self) -> pl.DataFrame | None:
        df = self.load_clean_data("logon")
        if df is None:
            logger.warning("clean_logon.csv not found.")
            return None
            
        logger.info("Extracting Temporal features...")
        
        # Sort by user and time
        df = df.sort(["user", "UnixTimestamp"])
        
        # Calculate time since previous event
        df = df.with_columns([
            pl.col("UnixTimestamp").diff().over("user").alias("Time_Since_Previous_Event")
        ])
        
        features = df.group_by("user").agg([
            pl.col("Time_Since_Previous_Event").mean().alias("Mean_Time_Between_Events"),
            pl.col("Time_Since_Previous_Event").max().alias("Max_Time_Between_Events"),
            
            # Hourly Activity Vector proxy: count of events per hour block
            # For simplicity, we just extract peak activity hour
            pl.col("Hour").mode().first().alias("Peak_Activity_Hour")
        ])
        
        return features
