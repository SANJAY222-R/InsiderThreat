import polars as pl
from .base_extractor import BaseExtractor
import logging

logger = logging.getLogger("FeatureEngineering")

class UserBehaviorExtractor(BaseExtractor):
    """Module 1: User Behavior Features (from logon.csv)"""
    
    def __init__(self, cfg):
        super().__init__("user_features", cfg)
        
    def run(self) -> pl.DataFrame | None:
        df = self.load_clean_data("logon")
        if df is None:
            logger.warning("clean_logon.csv not found, skipping User Behavior Features.")
            return None
            
        logger.info("Extracting User Behavior features...")
        
        # Group by user to aggregate features
        features = df.group_by("user").agg([
            # Logon/Logoff counts
            pl.col("activity").filter(pl.col("activity") == "Logon").count().alias("Total_Login_Count"),
            pl.col("activity").filter(pl.col("activity") == "Logoff").count().alias("Total_Logout_Count"),
            
            # Host switching
            pl.col("pc").n_unique().alias("Host_Switching_Count"),
            
            # Night activity (Hour < 6 or Hour >= 20)
            pl.col("Hour").filter((pl.col("Hour") < 6) | (pl.col("Hour") >= 20)).count().alias("Night_Activity_Count"),
            
            # Weekend Activity
            pl.col("IsWeekend").filter(pl.col("IsWeekend") == True).count().alias("Weekend_Activity_Count"),
            
            # Date range for per-day aggregations
            pl.col("UnixTimestamp").max().alias("Last_Event"),
            pl.col("UnixTimestamp").min().alias("First_Event")
        ])
        
        # Calculate rates
        features = features.with_columns([
            (((pl.col("Last_Event") - pl.col("First_Event")) / 86400) + 1).alias("Days_Active")
        ])
        
        features = features.with_columns([
            (pl.col("Total_Login_Count") / pl.col("Days_Active")).alias("Average_Logins_Per_Day")
        ])
        
        # Drop temporary columns
        features = features.drop(["First_Event", "Last_Event", "Days_Active"])
        
        return features
