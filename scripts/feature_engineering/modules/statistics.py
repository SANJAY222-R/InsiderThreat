from typing import Any, Optional
import polars as pl
from .base_extractor import BaseExtractor
import logging

logger = logging.getLogger("FeatureEngineering")

class StatisticsExtractor(BaseExtractor):
    """Module 8: Statistical Features"""

    def __init__(self, cfg: Any) -> None:
        super().__init__("statistical_features", cfg)

    def run(self) -> Optional[pl.DataFrame]:
        df = self.load_clean_data("logon")
        if df is None:
            logger.warning("clean_logon.csv not found.")
            return None
            
        logger.info("Extracting Statistical features...")
        
        df = df.with_columns([
            pl.col("date").str.slice(0, 10).alias("Session_Date")
        ])
        
        daily_events = df.group_by(["user", "Session_Date"]).agg([
            pl.len().alias("Daily_Event_Count")
        ])
        
        # Extract mean, std, min, max, variance for Daily Event Count
        features = daily_events.group_by("user").agg([
            pl.col("Daily_Event_Count").mean().alias("Mean_Daily_Events"),
            pl.col("Daily_Event_Count").median().alias("Median_Daily_Events"),
            pl.col("Daily_Event_Count").std().alias("Std_Daily_Events"),
            pl.col("Daily_Event_Count").min().alias("Min_Daily_Events"),
            pl.col("Daily_Event_Count").max().alias("Max_Daily_Events")
        ])
        
        return features
