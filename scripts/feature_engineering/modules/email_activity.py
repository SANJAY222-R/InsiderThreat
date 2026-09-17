from typing import Any, Optional
import polars as pl
from .base_extractor import BaseExtractor
import logging

logger = logging.getLogger("FeatureEngineering")

class EmailActivityExtractor(BaseExtractor):
    """Module 4: Email Communication Features (from email.csv)"""

    def __init__(self, cfg: Any) -> None:
        super().__init__("email_features", cfg)

    def run(self) -> Optional[pl.DataFrame]:
        df = self.load_clean_data("email")
        if df is None:
            logger.warning("clean_email.csv not found.")
            return None
            
        logger.info("Extracting Email features...")
        
        # CERT typical internal domain is DTAA.com or similar based on users, 
        # we proxy internal emails by checking if 'to' contains the same domain as 'from' or lacks external domains like .net/.org (simplified).
        # We also count attachments by counting semicolons or commas if it's a list.
        # But we'll do simple high-level counts.
        
        features = df.group_by("user").agg([
            pl.len().alias("Emails_Sent"),  # the 'user' column is the sender in CERT email.csv
            
            pl.col("to").n_unique().alias("Unique_Recipients"),
            
            # External Emails Proxy: if 'to' does not end with the primary domain (e.g., .com)
            pl.col("to").str.contains(r"\.(net|org|edu|gov)", strict=False).sum().alias("External_Emails_Sent"),
            
            pl.col("pc").n_unique().alias("Email_Host_Switching")
        ])
        
        return features
