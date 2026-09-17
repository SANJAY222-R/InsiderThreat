from typing import Any, Optional
import polars as pl
from .base_extractor import BaseExtractor
import logging

logger = logging.getLogger("FeatureEngineering")

class SessionExtractor(BaseExtractor):
    """Module 7: Session Features"""

    def __init__(self, cfg: Any) -> None:
        super().__init__("session_features", cfg)

    def run(self) -> Optional[pl.DataFrame]:
        df = self.load_clean_data("logon")
        if df is None:
            logger.warning("clean_logon.csv not found.")
            return None
            
        logger.info("Extracting Session features...")
        
        # In CERT, we can proxy a session by user and Day (Year, Month, Day)
        # We calculate the daily session length (max timestamp - min timestamp)
        df = df.with_columns([
            pl.col("date").str.slice(0, 10).alias("Session_Date")
        ])
        
        daily_sessions = df.group_by(["user", "Session_Date"]).agg([
            pl.len().alias("Events_Per_Session"),
            (pl.col("UnixTimestamp").max() - pl.col("UnixTimestamp").min()).alias("Session_Duration")
        ])
        
        # Aggregate up to user level
        features = daily_sessions.group_by("user").agg([
            pl.col("Events_Per_Session").mean().alias("Average_Events_Per_Session"),
            pl.col("Session_Duration").mean().alias("Average_Session_Duration"),
            (pl.col("Events_Per_Session").sum() / (pl.col("Session_Duration").sum() + 1)).alias("Session_Density")
        ])
        
        return features
