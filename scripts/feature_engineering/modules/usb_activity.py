from typing import Any, Optional
import polars as pl
from .base_extractor import BaseExtractor
import logging

logger = logging.getLogger("FeatureEngineering")

class UsbActivityExtractor(BaseExtractor):
    """Module 3: USB Device Features (from device.csv)"""

    def __init__(self, cfg: Any) -> None:
        super().__init__("usb_features", cfg)

    def run(self) -> Optional[pl.DataFrame]:
        df = self.load_clean_data("device")
        if df is None:
            logger.warning("clean_device.csv not found.")
            return None
            
        logger.info("Extracting USB features...")
        
        features = df.group_by("user").agg([
            # Connect/Disconnect counts
            pl.col("activity").filter(pl.col("activity") == "Connect").count().alias("USB_Insert_Count"),
            pl.col("activity").filter(pl.col("activity") == "Disconnect").count().alias("USB_Removal_Count"),
            
            # Off-hours USB
            pl.col("Hour").filter((pl.col("Hour") < 6) | (pl.col("Hour") >= 20)).count().alias("After_Hours_USB_Usage"),
            pl.col("IsWeekend").filter(pl.col("IsWeekend") == True).count().alias("Weekend_USB_Usage"),
            
            pl.col("pc").n_unique().alias("Unique_USB_PCs")
        ])
        
        return features
