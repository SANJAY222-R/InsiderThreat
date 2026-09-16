import polars as pl
from typing import Any
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class ConsistencyChecker(BaseModule):
    """Module 9: Data Consistency Check"""
    
    def __init__(self) -> None:
        super().__init__("ConsistencyChecker")
        
    def run(self, df: pl.DataFrame, context: dict[str, Any]) -> pl.DataFrame:
        logger.info("Checking data consistency.")
        issues = []
        
        # Impossible dates
        if "UnixTimestamp" in df.columns:
            # Unix timestamp for year 1990 and 2030 roughly
            invalid_dates = df.filter((pl.col("UnixTimestamp") < 631152000) | (pl.col("UnixTimestamp") > 1893456000)).height
            if invalid_dates > 0:
                issues.append(f"Found {invalid_dates} records with impossible dates.")
                
        # Empty users
        if "user" in df.columns:
            empty_users = df.filter(pl.col("user").str.len_chars() == 0).height
            if empty_users > 0:
                issues.append(f"Found {empty_users} records with empty user.")
                
        context["consistency_issues"] = issues
        for issue in issues:
            logger.warning(issue)
            
        return df
