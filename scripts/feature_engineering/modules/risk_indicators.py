import polars as pl
from .base_extractor import BaseExtractor
import logging

logger = logging.getLogger("FeatureEngineering")

class RiskIndicatorExtractor(BaseExtractor):
    """Module 9: Risk Indicator Features"""
    
    def __init__(self, cfg):
        super().__init__("risk_indicators", cfg)
        
    def run(self) -> pl.DataFrame | None:
        df = self.load_clean_data("logon")
        if df is None:
            logger.warning("clean_logon.csv not found.")
            return None
            
        logger.info("Generating Risk Indicators...")
        
        features = df.group_by("user").agg([
            pl.col("pc").n_unique().alias("Host_Switching_Score"),
            pl.col("Hour").filter((pl.col("Hour") < 6) | (pl.col("Hour") >= 20)).count().alias("Late_Night_Score"),
            pl.col("IsWeekend").filter(pl.col("IsWeekend") == True).count().alias("Weekend_Activity_Score")
        ])
        
        # Very simple normalization [0, 1] for these heuristic risk scores
        # We can do this in the Normalization module, but here we can define the preliminary ones
        # Just return raw heuristic counts here, let Module 10 normalize them.
        return features
