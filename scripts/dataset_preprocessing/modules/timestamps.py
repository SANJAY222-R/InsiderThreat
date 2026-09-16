import polars as pl
from typing import Any
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class TimestampStandardizer(BaseModule):
    """Module 5: Timestamp Standardization"""
    
    def __init__(self) -> None:
        super().__init__("TimestampStandardizer")
        
    def run(self, df: pl.DataFrame, context: dict[str, Any]) -> pl.DataFrame:
        # Detect timestamp column
        time_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]
        if not time_cols:
            logger.warning("No timestamp column found.")
            return df
            
        target_col = time_cols[0]
        logger.info(f"Standardizing timestamps based on {target_col}")
        
        # In CERT datasets, date format is often like "01/02/2010 08:30:00"
        # We try to parse it
        try:
            # Try specific format first, fallback to generic parsing if possible, but Polars strict=False helps
            df = df.with_columns([
                pl.col(target_col).str.strptime(pl.Datetime, format="%m/%d/%Y %H:%M:%S", strict=False).alias("_parsed_date")
            ])
            
            # Extract features
            df = df.with_columns([
                pl.col("_parsed_date").dt.year().alias("Year"),
                pl.col("_parsed_date").dt.month().alias("Month"),
                pl.col("_parsed_date").dt.day().alias("Day"),
                pl.col("_parsed_date").dt.hour().alias("Hour"),
                pl.col("_parsed_date").dt.minute().alias("Minute"),
                pl.col("_parsed_date").dt.second().alias("Second"),
                pl.col("_parsed_date").dt.weekday().alias("Weekday"),
                # Weekend (6 = Sat, 7 = Sun)
                pl.col("_parsed_date").dt.weekday().is_in([6, 7]).alias("IsWeekend"),
                # Business Hours (8 AM to 6 PM)
                ((pl.col("_parsed_date").dt.hour() >= 8) & (pl.col("_parsed_date").dt.hour() < 18)).alias("IsBusinessHours"),
                pl.col("_parsed_date").dt.epoch("s").alias("UnixTimestamp")
            ])
            
            df = df.drop("_parsed_date")
            context["timestamp_standardized"] = True
            
        except Exception as e:
            logger.error(f"Timestamp standardizer failed: {e}")
            context["timestamp_standardized"] = False
            
        return df
